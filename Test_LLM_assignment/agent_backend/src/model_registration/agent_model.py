import mlflow.pyfunc
from langchain.schema import ChatMessage
from src.agents.my_agent import my_agent_function

class LangChainAgent(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        pass

    def predict(self, context, model_input):
        messages = [ChatMessage(**msg) for msg in model_input["messages"]]
        params = model_input.get("params")
        return my_agent_function(messages, params)
