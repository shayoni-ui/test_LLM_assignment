import pandas as pd
import json
import mlflow
from difflib import SequenceMatcher

def string_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def evaluate_agent_manually(model_uri, eval_data: pd.DataFrame, target_column: str = "target"):
    model = mlflow.pyfunc.load_model(model_uri)

    all_scores = []
    predictions = []
    targets = []

    for _, row in eval_data.iterrows():
        # Parse JSON string if needed
        messages = json.loads(row["messages"]) if isinstance(row["messages"], str) else row["messages"]
        params = {"temperature": 0.5}

        # Build input for predict method
        input_df = pd.DataFrame([{
            "messages": json.dumps(messages),
            "params": json.dumps(params)
        }])

        # Run prediction
        try:
            prediction = model.predict(input_df)[0].get("response", "")
        except Exception as e:
            prediction = f"[ERROR] {str(e)}"

        target = row[target_column]
        score = string_similarity(prediction, target)

        all_scores.append(score)
        predictions.append(prediction)
        targets.append(target)

    # Summary
    metrics = {
        "mean_similarity": sum(all_scores) / len(all_scores),
        "predictions": predictions,
        "targets": targets,
        "scores": all_scores
    }

    return metrics
