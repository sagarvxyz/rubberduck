from datetime import datetime
from abc import ABC, abstractmethod
from typing import AsyncIterator


class PartType:
    TEXT = "text"
    FILE = "file"
    DATA = "data"


class Part:
    def __init__(self, type: PartType, payload):
        self.type = type
        self.payload = payload
        self.created_at = datetime.now()


class RoleType:
    USER = "user"
    AGENT = "agent"


class Message:
    def __init__(self, author: str, role: RoleType, parts: list[Part], metadata: dict = {}):
        self.role = role
        self.author = author
        self.parts = parts
        self.metadata = metadata
        self.created_at = datetime.now()


class TaskState:
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class TaskStatus:
    def __init__(self, state: TaskState, message: Message = None):
        self.state = state
        self.message = message


class Task:
    def __init__(self, id, sessionId, status: TaskStatus, history, results):
        self.id = id
        self.sessionId = sessionId
        self.status = status
        self.history = history
        self.results = results
        self.createdAt = datetime.now()


class ILLMClient(ABC):
    """Abstract base class for LLM clients."""

    @abstractmethod
    async def handle_message(
        self, messages: list[Message | None] = [], task: Task | None = None
    ) -> AsyncIterator[str]:  # Changed return type to AsyncIterator
        """Handle prompt using the LLM and stream response chunks."""
        pass
