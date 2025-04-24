from src.llm_client.get_llm_client import get_llm_client
from src.project_types import Message
from typing import AsyncIterator  # Added for streaming type hint


class Agent:
    "An interactive, LLM connected 'agent'."

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self._llm_client = get_llm_client(agent_id)

    async def send_message(
        self, txt: str
    ) -> AsyncIterator[str]:  # Changed return type to AsyncIterator
        """
        Process a message and stream response chunks.
        """
        message = Message(role="user", author="You", parts=[txt])
        # Iterate over the async iterator returned by the client
        async for chunk in self._llm_client.handle_message([message]):
            yield chunk  # Yield each chunk received
