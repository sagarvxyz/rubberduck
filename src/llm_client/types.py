from abc import ABC, abstractmethod
from typing import AsyncIterator


class ILLMClient(ABC):
    """Abstract base class for LLM clients."""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        # Assuming get_agent_config is defined elsewhere or will be implemented
        # self._agent_config = self.get_agent_config(agent_id)
        self._client: any = None

        @abstractmethod
        async def post_message(self, *args, **kwargs) -> AsyncIterator[str]:
            pass

        @abstractmethod
        async def post_task(self, *args, **kwargs) -> AsyncIterator[str]:
            pass
