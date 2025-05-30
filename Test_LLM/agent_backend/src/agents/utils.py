import json
import os
from typing import Any, Callable, Dict, List, Tuple

import pandas as pd
import requests
import os
from azure.identity import DefaultAzureCredential
#from azure.keyvault.secrets import SecretClient
from azureml.core import Workspace


files_metadata: Dict[str, Any] = {}
csv_files_data: Dict[str, List[Dict[str, Any]]] = {}

def generate_source_data(datasources_path: str = "./datasources") -> Tuple[Dict[str, Any], Dict[str, List[Dict[str, Any]]]]:
    global files_metadata, csv_files_data

    with open(f"{datasources_path}/datasources_metadata.json", "r") as fp:
        files_metadata = json.load(fp)

    csv_files_data = {
        f: pd.read_csv(f"{datasources_path}/{f}.csv").to_dict(orient="records")
        for f in files_metadata
    }

    return files_metadata, csv_files_data

def get_bearer_token_provider_kong() -> Callable[[], str]:
    """
    Provides a callable function that retrieves a bearer token from the Kong OAuth service.

    Returns:
        Callable[[], str]: A function that, when called, returns a bearer token as a string.

    Raises:
        EnvironmentError: If any required environment variables are missing.
        Exception: If the HTTP request to the OAuth service fails.
    """

    def wrapper() -> str:
        """
        Retrieves a bearer token using client credentials from environment variables.

        Returns:
            str: The retrieved bearer token.

        Raises:
            EnvironmentError: If any required environment variables are missing.
            Exception: If the HTTP request to the OAuth service fails.
            
        """
        # Load the workspace from config or directly
        ws = Workspace.from_config()
        # Access the linked Key Vault
        keyvault = ws.get_default_keyvault()
# Retrieve a secret
        # Validate workspace variables
        try:
            #client_id = os.environ["KONG_CLIENT_ID"]
            #client_secret = os.environ["KONG_CLIENT_SECRET"]
            # Retrieve a secret
            secret_value = keyvault.get_secret(name="flow-ai-id")
            secret_id= keyvault.get_secret(name="flow-ai-access")
        except KeyError as e:
            raise EnvironmentError(f"Missing required environment variable: {e}")

        data = {
            "client_id": secret_value,
            "client_secret": secret_id,
            "grant_type": "client_credentials",
            
        }

        response = requests.post(
            "https://federation-qa.gsk.com/as/token.oauth2",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=data,
        )
        if not response.ok:
            raise Exception(f"Error: {response.status_code}, {response.text}")

        return json.loads(response.text).get("access_token")

    return wrapper

# For this simple example, we will use files commited to memory simplify
# the interactions of the agent.
# You custom agent can be adapted to interact with files, APIs and databases as needed.


