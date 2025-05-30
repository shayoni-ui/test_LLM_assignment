import os
import mlflow  # type: ignore
import pandas as pd
import json
from typing import Any, List, Optional, Type

from mlflow.types.llm import ChatMessage, ChatParams, ChatChoice
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.agents.agent import RunnableAgent, RunnableMultiActionAgent
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from pydantic import BaseModel
from langchain.tools import BaseTool
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
)
from langchain_openai import AzureChatOpenAI
#add agents.
from tools import (
    GetDatasetMetadaTool,
    GetTargetFileSchemaTool,
    GenerateSQLForFileTool,
    GenerateAnswerforQuestionTool,
)
from azure_openai import *

# my_agent.py (or your entry point)
from utils import *




def my_agent_function(
    messages: List[ChatMessage],
    params: Optional[ChatParams] = None,
    verbose: bool = False
) -> dict:
    """
    Executes a request using a chat agent with designated tools to generate responses.
    """
    if not messages:
        raise ValueError("The messages list cannot be empty.")

    ask = messages[-1].content
    chat_history = [
        {"role": message.role, "content": message.content}
        for message in messages[:-1]
    ]

    # Define the tools
    agent_tools = [
        GetDatasetMetadaTool(),
        GetTargetFileSchemaTool(),
        GenerateSQLForFileTool(),
        GenerateAnswerforQuestionTool(),
    ]

    # Prompt template with placeholders
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a helpful agent who receives questions and answers them
                with the tools available. If none of your tools are able to provide
                the necessary answer, respond saying you are not able to assist with
                that question based on the tools available to you.""",
            ),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )
    
    #creat model
    model = model_client()
    # Create model with token provider
    #token = create_bearer_token()
    #token_provider = CustomTokenProvider(token)
    
   

    #model = AzureChatOpenAI(
    #    model="o1",
     #   azure_endpoint="https://dev.api.gsk.com/co/psc/azureopenai/us6/",
      #  azure_deployment="o1",
      #  api_version="2024-12-01-preview",
      #  azure_ad_token_provider=token_provider,
    #)

    # Create the agent
    agent = create_openai_tools_agent(model, agent_tools, prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=agent_tools,
        verbose=verbose,
        return_intermediate_steps=True,
        handle_parsing_errors=True,
    )

    # Ensure compatibility with MLflow (disable streaming)
    if isinstance(agent_executor.agent, (RunnableMultiActionAgent, RunnableAgent)):
        agent_executor.agent.stream_runnable = False

    # Run the agent
    res = agent_executor.invoke({"input": ask, "chat_history": chat_history})["output"]

    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": res
                }
            }
        ]
    }