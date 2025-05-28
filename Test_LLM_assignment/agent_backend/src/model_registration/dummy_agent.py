from typing import List
from model import ChatMessage, ChatParams, ChatCompletionResponse

def dummy_agent_function(messages: List[ChatMessage], params: ChatParams, verbose=False) -> ChatCompletionResponse:
    last_user_msg = next((m.content for m in reversed(messages) if m.role == "user"), "")
    reply = f"Echo: {last_user_msg} (temp={params.temperature})"
    return ChatCompletionResponse(response=reply, metadata={"echoed": True})
