# Gen AI Agents

This repository sets up a custom AI Agent backend . The intenet is to also, serve it as an endpoint, 

## Project Repository Scope


- How to register a custom AI Agent in MLflow using your preferred Agentic Framework library
- How to serve the model as an inference endpoint


⚙️ How to Run
1. Clone the repository
git clone https://github.com/your-org/healthqa-agent.git
cd healthqa-agent

2. Install dependencies
pip install -r requirements.txt

3. Prepare config and data
Ensure these CSV files are present in agent_backend/datasources/:

demographics.csv
exposures.csv
diagnosis.csv

Update agent_config.py and azure_openai.py with your Azure OpenAI keys, azure key vault secrets and tool configs.

4. Run a test query or evaluation with main.py & main_evaluation_agent.py
   test_cases = [
    TestCase(
        question="How many asian patients in the dataset?",
        expected_sql="SELECT COUNT(*) FROM demographics WHERE LOWER(race) = 'asian';",
        expected_answer_substr="627",
        expected_answer_text="There are 627 Asian patients in the dataset.",
    )
]

results = [evaluate_agent_on_test_case(my_agent_function, tc) for tc in test_cases]

5. 📦 Deployment
To serve the agent using MLflow:
mlflow models serve -m runs:/<run-id>/agent_model -p 5000

6.🧪 Run Tests








