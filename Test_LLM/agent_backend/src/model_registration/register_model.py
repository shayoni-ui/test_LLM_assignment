import mlflow
import pandas as pd
from mlflow.models.signature import infer_signature
from agent_wrapper import MyAgentWrapper
from dummy_agent import dummy_agent_function

example_input = pd.DataFrame([{
    "messages": '[{"role": "user", "content": "hello"}]',
    "params": '{"temperature": 0.5}'
}])
example_output = pd.DataFrame([{"response": "Echo: hello", "metadata": '{"echoed": true}'}])
signature = infer_signature(example_input, example_output)

agent = MyAgentWrapper(agent_name="echo-agent", agent_function=dummy_agent_function)

mlflow.pyfunc.save_model(
    path="my_agent_model_v2",
    python_model=agent,
    signature=signature,
    conda_env=mlflow.pyfunc.get_default_conda_env(),
    input_example=example_input
)
