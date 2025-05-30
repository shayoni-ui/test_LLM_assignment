import os
from azure.identity import DefaultAzureCredential
from azureml.core import Workspace

class AgentConfig:
    def __init__(self):
        self.ws = Workspace.from_config()
        self.keyvault = self.ws.get_default_keyvault()
        self.credential = DefaultAzureCredential()
        self._load_secrets()

        self.MODEL_NAME = "agent_demo"
        self.DEPLOYMENT_NAME = "gpt-4"
        self.ARTIFACT_PATH = f"{self.MODEL_NAME}_artifact"
        self.SECRET_SCOPE = "agents_demo"

    def _load_secrets(self):
        self.secret_value = self.keyvault.get_secret(name="flow-ai-id")
        self.secret_id = self.keyvault.get_secret(name="flow-ai-access")

    def print_secrets(self):
        print(f"Secret flow-ai-id: {self.secret_value}")
        print(f"Secret flow-ai-access: {self.secret_id}")

# Create singleton config instance
config = AgentConfig()
