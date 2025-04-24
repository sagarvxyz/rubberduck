from google import genai
from google.genai import types as genai_types
from src.utils.get_agent_config import get_agent_config
from src.project_types import ILLMClient, Message, Task
from typing import AsyncIterator


class GoogleLLMClient(ILLMClient):
    """Google GenAI client wrapper."""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self._agent_config = get_agent_config(agent_id)
        self._client = genai.Client(
            api_key=self._agent_config["api_key"],
            http_options=genai_types.HttpOptions(
                api_version=self._agent_config["http_options"]["api_version"]
            ),
        )

    async def handle_message(
        self, messages: list[Message | None] = [], task: Task | None = None
    ) -> AsyncIterator[str]:  # Changed return type to AsyncIterator
        """Handle prompt using Google GenAI and stream response chunks."""
        try:
            # Convert messages to the format expected by Google GenAI
            contents = []
            for message in messages:
                contents.extend(message.parts)  # Extend if parts is a list

            # Call the streaming API
            async for chunk in await self._client.aio.models.generate_content_stream(
                model=self._agent_config["model_name"],
                contents=contents,
                config=genai_types.GenerateContentConfig(
                    temperature=self._agent_config["temperature"],
                    max_output_tokens=self._agent_config["max_output_tokens"],
                    thinking_config=genai_types.ThinkingConfig(
                        thinking_budget=self._agent_config["thinking_budget"],
                    ),
                ),
            ):
                # Yield the text content of each chunk
                if chunk.text:  # Check if chunk has text content
                    yield chunk.text

        except Exception as e:
            print(f"Error in GoogleLLMClient: {e}")
