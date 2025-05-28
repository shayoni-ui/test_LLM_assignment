from typing import List, Callable
import json
import pandas as pd
import duckdb
from typing import Any, Optional, Type, List
from pydantic import BaseModel, Field
from langchain_core.tools import Tool
from langchain.tools import BaseTool
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI

from agents.utils import files_metadata, csv_files_data
from agents.azure_openai import *




# 1. Tool: GetDatasetMetadaTool
class GetDatasetMetadaInput(BaseModel):
    question: Optional[str] = Field(description="The prompt/request from the user", default=None)

class GetDatasetMetadaTool(BaseTool):
    name: str = "get_file_metadata"
    description: str = "Provides the metadata (description, schema and sample) of the dataset (CSV files)."
    args_schema: Type[BaseModel] = GetDatasetMetadaInput

    def _run(self, question: Optional[str] = None) -> Any:
        return json.dumps(files_metadata)


# 2. Tool: GetTargetFileSchemaTool
class GetTargetFileSchemaInput(BaseModel):
    question: str = Field(description="The user's question.")
    files_metadata: str = Field(description="Metadata dictionary of the dataset.")

class GetTargetFileSchemaTool(BaseTool):
    name: str = "get_target_file_schema"
    description: str = "Selects the most likely file name and schema based on the user's question."
    args_schema: Type[BaseModel] = GetTargetFileSchemaInput

    def _run(self, question: str, files_metadata: str) -> Any:
        response_schemas = [
            ResponseSchema(name="file_name", description="Selected file's name."),
            ResponseSchema(name="file_schema", description="Schema for the selected file."),
        ]
        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions = output_parser.get_format_instructions() + ' Make sure strings are enclosed with ".'

        prompt_text = '''
        Given the following files and their schemas:
        {files_metadata}
        
        Select the most relevant file to answer:
        "{question}"

        Remove sample data from schema (just column names, comma-separated).
        {format_instructions}
        '''

        prompt = PromptTemplate.from_template(
            template=prompt_text,
            partial_variables={
                "format_instructions": format_instructions,
                "files_metadata": files_metadata
            }
        )
        
        model = model_client()
       # model = AzureChatOpenAI(
       #     model="o1",
       #     azure_endpoint="https://dev.api.gsk.com/co/psc/azureopenai/us6/",
       #     azure_deployment="o1",
       #     api_version="2024-12-01-preview",
       #     azure_ad_token_provider=token_provider
        #)
        chain = prompt | model | output_parser
        return chain.invoke({"question": question})


# 3. Tool: GenerateSQLForFileTool
class GenerateSQLForFileInput(BaseModel):
    question: str = Field(description="User's request to generate SQL.")
    file_name: str = Field(description="The table name (CSV file name).")
    file_schema: str = Field(description="A string representing the table's columns.")

class GenerateSQLForFileTool(BaseTool):
    name: str = "generate_sql_for_file"
    description: str = "Generates SQL query based on file name and schema."
    args_schema: Type[BaseModel] = GenerateSQLForFileInput

    def _run(self, question: str, file_name: str, file_schema: str) -> Any:
        response_schemas = [
            ResponseSchema(name="sql_query", description="Generated SQL query."),
        ]
        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions = output_parser.get_format_instructions() + " Format it as a plain SQL string."

        prompt_text = """
        Given table name '{file_name}' and column schema:
        {file_schema}

        Write a SQL query to answer:
        "{question}"

        Lowercase column names and string values to avoid case sensitivity issues.
        {format_instructions}
        """

        prompt = PromptTemplate.from_template(
            template=prompt_text,
            partial_variables={"format_instructions": format_instructions}
        )
        model = model_client()
        chain = prompt | model | output_parser
        result = chain.invoke({"question": question, "file_name": file_name, "file_schema": file_schema})
        return result["sql_query"]


# 4. Tool: GenerateAnswerforQuestionTool
class GenerateAnswerforQuestionInput(BaseModel):
    question: str = Field(description="The initial user prompt.")
    sql_query: str = Field(description="SQL query to run.")
    file_name: str = Field(description="CSV file name representing the table.")
    file_schema: str = Field(description="Sample schema string (not used in query).")

class GenerateAnswerforQuestionTool(BaseTool):
    name: str = "generate_answer_for_question"
    description: str = "Executes SQL on dataframe and returns answer."
    args_schema: Type[BaseModel] = GenerateAnswerforQuestionInput

    def _run(self, question: str, sql_query: str, file_name: str, file_schema: str) -> Any:
        # Replace table name with in-memory table
        tokens = sql_query.split()
        try:
            idx = [i for i, t in enumerate(tokens) if t.upper() == "FROM"][0]
            tokens[idx + 1] = "dftbl"
        except IndexError:
            raise ValueError("SQL query missing FROM clause.")
        query = " ".join(tokens)

        # Execute on dataframe
        dftbl = pd.DataFrame(csv_files_data[file_name])
        return duckdb.query(query).to_df().to_dict()


# Aggregate
def get_tools() -> List[BaseTool]:
    return [
        GetDatasetMetadaTool(),
        GetTargetFileSchemaTool(),
        GenerateSQLForFileTool(),
        GenerateAnswerforQuestionTool()
    ]
