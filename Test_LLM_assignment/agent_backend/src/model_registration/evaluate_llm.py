import pandas as pd
from mlflow.models import evaluate
from typing import Union
import os

def evaluate_agent(model_uri: str, eval_dataset: Union[str, pd.DataFrame], target_column: str = "target") -> dict:
    """
    Evaluates a deployed or local LLM agent using MLflow's evaluation utilities.

    Args:
        model_uri (str): URI of the MLflow model (e.g. "runs:/<run_id>/my_agent_model" or registered name).
        eval_dataset (Union[str, pd.DataFrame]): Path to a JSONL/CSV file or a DataFrame of evaluation examples.
        target_column (str): Column name containing the expected output. Default is 'target'.

    Returns:
        dict: Evaluation metrics.
    """
    # Load evaluation data
    if isinstance(eval_dataset, str):
        if eval_dataset.endswith(".jsonl"):
            data = pd.read_json(eval_dataset, lines=True)
        elif eval_dataset.endswith(".csv"):
            data = pd.read_csv(eval_dataset)
        else:
            raise ValueError("Unsupported file format. Provide a .jsonl or .csv file.")
    elif isinstance(eval_dataset, pd.DataFrame):
        data = eval_dataset.copy()
    else:
        raise TypeError("eval_dataset must be a file path or pandas DataFrame.")

    if target_column not in data.columns:
        raise ValueError(f"Target column '{target_column}' not found in dataset.")

    # Evaluate the model
    results = evaluate(
        model=model_uri,
        data=data,
        targets=target_column,
        model_type="chat",  # can also be "text" or "classifier" if appropriate
        evaluators=["default"],
    )

    print("\nEvaluation Results:\n", results.metrics)
    return results.metrics
