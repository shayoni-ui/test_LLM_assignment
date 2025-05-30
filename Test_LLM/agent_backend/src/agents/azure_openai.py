import os
import requests
from langchain_openai import AzureChatOpenAI
from openai import AzureOpenAI

# ✅ Import the config from agent_config.py
from agent_config import config 
#from agents.agent_config import config 



class CustomTokenProvider:
    def __init__(self, access_token: str):
        self.access_token = access_token

    def __call__(self, *scopes):
        return self.access_token

def create_bearer_token() -> str:
    federation_url = "https://federation-qa.gsk.com/as/token.oauth2"
    #client_id = keyvault.get_secret(name="flow-ai-id")
    #client_secret = keyvault.get_secret(name="flow-ai-access")
    client_id = config.secret_value
    client_secret = config.secret_id

    token_data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(federation_url, data=token_data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise RuntimeError(f"Token request failed: {response.text}")

def model_client() -> AzureChatOpenAI:
    access_token = create_bearer_token()
    token_provider = CustomTokenProvider(access_token)
    return AzureChatOpenAI(
        model="o1",
        azure_endpoint="https://dev.api.gsk.com/co/psc/azureopenai/us6/",
        azure_deployment="o1",
        api_version="2024-12-01-preview",
        #model_capabilities={"function_calling": True, "vision": True, "json_output": True},
        azure_ad_token_provider=token_provider
    )

def create_openai_client() -> AzureOpenAI:
    return AzureOpenAI(
        api_version="2024-12-01-preview",
        azure_endpoint="https://dev.api.gsk.com/co/psc/azureopenai/us6/",
        azure_ad_token=create_bearer_token(),
        max_retries=4
    )
