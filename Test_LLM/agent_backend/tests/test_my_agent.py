import pytest
from src.agents.my_agent import my_agent_function
from mlflow.types.llm import ChatMessage

def test_agent_basic_response():
    messages = [ChatMessage(role="user", content="How many asian patients in the dataset?")]
    response = my_agent_function(messages)
    assert "choices" in response
    assert response["choices"][0]["message"]["content"]
