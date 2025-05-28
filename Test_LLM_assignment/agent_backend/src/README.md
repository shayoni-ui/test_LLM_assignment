# AI Agent Setup Instructions for Azure Machine Learning

This section of the repository will guide you through the development, registration, deployment, and testing of a fully functional AI Agent using Azure Machine Learning.

## Prerequisites and Assumptions

1. You must have access to an Azure Machine learning instance, project and a functional AML Compute Instance. Additionally, you should have the required level of access to create folders, files, register models with MLFlow, and create Real-time endpoints.

2. Required Python, library management, Agent Frameworks (chains, agents, and tools), and Azure Machine Learning features, notebooks, and CLI.

3. You should have your Client ID, Secret, and an Azure OpenAI model deployment name

4. You should have a setup Azure Key Vault, have access level to adding secrets to it and have access level to retrieve secret values from a remote source using a managed identity.

## Setup Your KeyVault Secret Scope

This step by step will demonstrate how to manually add secrets to your Key Vault, but if you prefer you can use the [Azure Key Vault Python SDK](https://learn.microsoft.com/en-us/azure/key-vault/secrets/quick-create-python?tabs=azure-cli) to create and manage your secrets from your local environment.

1. Go to your Key Vault under the `Secrets` tab:

![alt text](../../readme-src/keyvault-1.png)

2. Click the button `+ Generate/Import` 

3. Fill the fields `Name` and `Secret value` with the name and value of your secret:

![alt text](../../readme-src/keyvault-2.png)

4. Repeat the process for the following secret keys in agent_config.py



The name of the secrets should match exactly with the above to make sure the code runs. If you change any of the names, make sure to update that secret name in across your whole repository.


## (Optional) Manually test the agent

If you wish to manually experiment with the AI agents using different frameworks, you can follow the steps described [here](./agents/README.md).

## AI Agent Model Registration and Serving

azure_openai.py and evaluate_llm.py