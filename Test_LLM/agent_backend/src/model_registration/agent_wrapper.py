import json
import pandas as pd
from mlflow.types.llm import ChatMessage

class MyAgentWrapper(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        from my_agent import my_agent_function  # Your agent function
        self.agent_fn = my_agent_function

    def predict(self, context, model_input: pd.DataFrame) -> pd.Series:
        return model_input.apply(lambda row: self.agent_fn(
            messages=[ChatMessage(**m) for m in json.loads(row["messages"])],
            params=json.loads(row["params"]) if "params" in row and row["params"] else None
        )["choices"][0]["message"]["content"], axis=1)