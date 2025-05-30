# test_LLM_assignment
Technical Summary: 
🧠 HealthQA Agent: Conversational Agent for Patient-Level Health Data
This repository implements a modular, conversational AI agent capable of answering complex, multi-turn questions over structured health data. It is built using LangChain and Azure OpenAI, and is fully integrated with MLflow for experiment tracking, evaluation, and deployment.

This project focuses on developing a custom conversational AI agent wrapped as an MLflow Python model. The agent supports multi-turn dialogue processing by consuming structured chat messages and configurable parameters. It is designed for easy deployment, version control, and evaluation using MLflow’s model lifecycle features.\📊 ConvFinQA Agent: Conversational Financial QA Agent with LangChain, Azure OpenAI, and MLflow
This repository contains a modular, production-ready implementation of a custom LLM agent designed to tackle the ConvFinQA challenge. The agent can engage in multi-turn conversations grounded in financial documents to answer complex quantitative reasoning questions.


🔍 Use Case
The agent reasons over patient records involving:

👤 Demographics (age, sex, race, etc.)
💊 Exposures (e.g., drug/treatment history)
🏥 Diagnoses (ICD codes, conditions, comorbidities)

It is capable of answering queries like:
"how many asian patients?"
“Which patients above 65 have been diagnosed with hypertension and exposed to drug X?”



🚀 Features
🗣️ Conversational Multi-Turn QA over structured health data

🧠 Custom LangChain Agent using planner + executor design

🔌 Azure OpenAI GPT-4 for reasoning and natural language understanding

🛠️ Custom Tools for table retrieval, filtering, and numeric computation

📊 Evaluation Pipeline for agent accuracy and reasoning correctness

📦 MLflow Integration for model tracking, logging, and deployment




Architecture & Implementation Details
1. 🧠 Agent Architecture
The agent uses a Planner + Executor approach:

Planner: GPT-4 decomposes the user's query into tool-invokable steps
Executor: Executes steps using tools like:
TableLookup: filters and retrieves rows from a CSV
Calculator: performs numeric logic

Memory & Scratchpad: Maintains context for multi-turn reasoning
My_Agent_function class extends mlflow.pyfunc.PythonModel, serving as the MLflow model interface.
Core function (my_agent_function): Implements the conversational logic, taking in a list of ChatMessage objects and ChatParams for configurable behavior such as temperature.

Data structures:
ChatMessage encapsulates individual messages with role (user/assistant) and content.
ChatParams holds generation parameters like temperature, max_tokens, and custom inputs (e.g., client type).
ChatCompletionResponse wraps the output response text and any additional metadata.



2. Input/Output Handling
Inputs to the agent are passed as serialized JSON strings representing nested message lists and parameter dictionaries. This serialization is necessary because MLflow’s predict expects tabular input formats.
The predict method deserializes these inputs into typed Python objects for processing, then returns responses in structured JSON/dict format.



3. MLflow Integration
The model is logged and versioned using mlflow.pyfunc.log_model(), ensuring:
Reproducibility of the agent across environments.
Integration with MLflow’s model registry for deployment and governance.
Example:
python

with mlflow.start_run() as run:
    mlflow.pyfunc.log_model(
        artifact_path="my_agent_model",
        python_model=my_agent_instance,
        signature=model_signature
    )

    
4. 📊 Evaluation
Evaluation is done over a curated set of health QA queries with ground-truth answers.
Using MLflow’s built-in evaluate() API, the agent is tested against a labeled dataset containing example conversations and expected responses.
Metrics:

✅ Answer Accuracy
📋 Tool Invocation Trace
🧠 Reasoning Chain Consistency
Evaluation outputs are logged to MLflow automatically.Evaluation metrics (e.g., accuracy, BLEU, ROUGE

System Diagram
<img width="744" alt="Screenshot 2025-05-28 at 23 38 47" src="https://github.com/user-attachments/assets/0f56b787-78dc-4c83-8f27-e704286bfa87" />
<img width="630" alt="Screenshot 2025-05-28 at 23 37 51" src="https://github.com/user-attachments/assets/7b685892-e543-4e64-a627-af417ab25be1" />




Future Directions: Comparative LLM Model Evaluation
To systematically improve and benchmark conversational performance, a future roadmap includes:

1. Integration of Multiple LLM Agents:

Wrap other open-source or proprietary LLMs (e.g., GPT-4, Claude, Llama2) in a similar MLflow PyFunc interface.
Standardize input/output formats to allow interchangeable testing.

2.Automated Multi-Model Evaluation Pipeline:

Develop a testing framework to run the same evaluation dataset through multiple models.
Compute and compare metrics side-by-side (accuracy, response coherence, latency, etc.).
Use MLflow model registry to version and compare model iterations.

3.Human-in-the-Loop (HITL) Testing:
Integrate feedback mechanisms to capture human evaluator scores for quality and relevance.
Combine automated metrics with human judgment for comprehensive evaluation.

4.Performance and Cost Analysis:
Track inference latency and resource usage across models.
Analyze trade-offs between response quality and operational costs.

Summary
This project delivers a robust, modular conversational agent integrated with MLflow for deployment and evaluation. It supports multi-turn dialogues with configurable parameters and returns structured responses suitable for downstream tasks. The evaluation framework allows quantitative benchmarking against expected outputs, laying a strong foundation for scaling to multiple LLMs and continuous improvement.

