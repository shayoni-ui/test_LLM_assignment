## Manual test of the AI Agent

<details>

<summary>1. Using Langchain</summary>

### Using Langchain

1. From within your folder, go to [/agent_langchain](./agent_langchain.ipynb) and connect to your started compute.

2. The tree below describes high level interactions between the classes, methods and functions within the notebook.

                                 ┌─────────────────────────────────────┐
                              │         Developer Interaction       │
                              │  (Notebook / API / CLI / Inference) │
                              └─────────────────────────────────────┘
                                               │
                          ┌────────────────────▼─────────────────────┐
                          │         MLflow Model Serving             │
                          │    (LangChainAgent - PyFunc Model)       │
                          └────────────────────┬─────────────────────┘
                                               │
                   ┌───────────────────────────▼─────────────────────────────┐
                   │                      my_agent.py                        │
                   │   - Loads AzureChatOpenAI with Azure AD Token           │
                   │   - Uses LangChain Tools + AgentExecutor                │
                   └───────────────────────────┬─────────────────────────────┘
                                               │
                 ┌─────────────────────────────▼────────────────────────────────┐
                 │                          Tools                               │
                 │  ├── GetDatasetMetadataTool                                  │
                 │  ├── GetTargetFileSchemaTool                                 │
                 │  ├── GenerateSQLForFileTool                                  │
                 │  └── GenerateAnswerforQuestionTool                           │
                 └─────────────────────────────┬────────────────────────────────┘
                                               │
                 ┌─────────────────────────────▼────────────────────────┐
                 │                Azure OpenAI + GSK Federation         │
                 │  - Token via federation-qa.gsk.com                    │
                 │  - model: gpt-4 / o1                                  │
                 └─────────────────────────────┬────────────────────────┘
                                               │
                                ┌──────────────▼───────────────┐
                                │     Agent Configuration      │
                                │     agent_config.py          │
                                │  - Azure KeyVault Access     │
                                │  - Secrets for Federation    │
                                └──────────────────────────────┘

Optional (Dev Tools):

   ┌────────────┐  ┌─────────────┐  ┌─────────────┐  ┌───────────────┐
   │   tests/   │  │   Makefile  │  │ GitHub CI   │  │   llm_evaluate│
   └────────────┘  └─────────────┘  └─────────────┘  └───────────────┘
