# test_LLM_assignment
Technical Summary: Custom Conversational Agent with MLflow Deployment & Evaluation
Project Overview
This project focuses on developing a custom conversational AI agent wrapped as an MLflow Python model. The agent supports multi-turn dialogue processing by consuming structured chat messages and configurable parameters. It is designed for easy deployment, version control, and rigorous evaluation using MLflow’s model lifecycle features.

Architecture & Implementation Details
1. Agent Core
MyAgent class extends mlflow.pyfunc.PythonModel, serving as the MLflow model interface.

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
Copy
Edit
with mlflow.start_run() as run:
    mlflow.pyfunc.log_model(
        artifact_path="my_agent_model",
        python_model=my_agent_instance,
        signature=model_signature
    )
4. Evaluation Framework
Using MLflow’s built-in evaluate() API, the agent is tested against a labeled dataset containing example conversations and expected responses.

The dataset structure:

messages (JSON)	params (JSON)	target (str)
Serialized list of chat messages	Serialized params	Expected answer

Evaluation metrics 
(e.g., accuracy, BLEU, ROUGE) are automatically computed and logged.

System Diagram
<img width="744" alt="Screenshot 2025-05-28 at 23 38 47" src="https://github.com/user-attachments/assets/0f56b787-78dc-4c83-8f27-e704286bfa87" />
<img width="630" alt="Screenshot 2025-05-28 at 23 37 51" src="https://github.com/user-attachments/assets/7b685892-e543-4e64-a627-af417ab25be1" />




Future Directions: Comparative LLM Model Evaluation
To systematically improve and benchmark conversational performance, a future roadmap includes:

Integration of Multiple LLM Agents:

Wrap other open-source or proprietary LLMs (e.g., GPT-4, Claude, Llama2) in a similar MLflow PyFunc interface.

Standardize input/output formats to allow interchangeable testing.

Automated Multi-Model Evaluation Pipeline:

Develop a testing framework to run the same evaluation dataset through multiple models.

Compute and compare metrics side-by-side (accuracy, response coherence, latency, etc.).

Use MLflow model registry to version and compare model iterations.

Human-in-the-Loop (HITL) Testing:

Integrate feedback mechanisms to capture human evaluator scores for quality and relevance.

Combine automated metrics with human judgment for comprehensive evaluation.

Performance and Cost Analysis:

Track inference latency and resource usage across models.

Analyze trade-offs between response quality and operational costs.

Summary
This project delivers a robust, modular conversational agent integrated with MLflow for deployment and evaluation. It supports multi-turn dialogues with configurable parameters and returns structured responses suitable for downstream tasks. The evaluation framework allows quantitative benchmarking against expected outputs, laying a strong foundation for scaling to multiple LLMs and continuous improvement.

