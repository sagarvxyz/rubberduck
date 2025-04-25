"""
Project Types for LLM Agent.
Borrowed from the Google A2A Protocol: https://google.github.io/A2A/#/documentation
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from typing import Literal, Union


@dataclass
class Provider:
    organization: str
    url: str


@dataclass
class Capabilities:
    streaming: Optional[bool] = field(default=None)
    pushNotifications: Optional[bool] = field(default=None)
    stateTransitionHistory: Optional[bool] = field(default=None)


@dataclass
class Skill:
    id: str
    name: str
    description: str
    tags: List[str]
    examples: Optional[List[str]] = field(default=None)
    inputModes: Optional[List[str]] = field(default=None)
    outputModes: Optional[List[str]] = field(default=None)


@dataclass
class Authentication:
    schemes: List[str]
    credentials: Optional[str] = field(default=None)


@dataclass
class AgentCard:
    name: str
    description: str
    url: str
    version: str
    capabilities: Capabilities
    authentication: Authentication
    defaultInputModes: List[str]
    defaultOutputModes: List[str]
    skills: List[Skill]
    provider: Optional[Provider] = field(default=None)
    documentationUrl: Optional[str] = field(default=None)


# Type Aliases
TaskState = Literal[
    "submitted",
    "working",
    "input-required",
    "completed",
    "canceled",
    "failed",
    "unknown",
]


# Part Types
@dataclass
class TextPart:
    type: Literal["text"]
    text: str
    metadata: Optional[Dict[str, Any]] = field(default=None)


@dataclass
class FileData:
    name: Optional[str] = field(default=None)
    mimeType: Optional[str] = field(default=None)
    bytes: Optional[str] = field(default=None)  # base64 encoded content
    uri: Optional[str] = field(default=None)


@dataclass
class FilePart:
    type: Literal["file"]
    file: FileData
    metadata: Optional[Dict[str, Any]] = field(default=None)


@dataclass
class DataPart:
    type: Literal["data"]
    data: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = field(default=None)


Part = Union[TextPart, FilePart, DataPart]


# Core Interfaces as Dataclasses
@dataclass
class Message:
    role: Literal["user", "agent"]
    parts: List[Part]
    metadata: Optional[Dict[str, Any]] = field(default=None)


@dataclass
class Artifact:
    parts: List[Part]
    index: int
    name: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)
    metadata: Optional[Dict[str, Any]] = field(default=None)
    append: Optional[bool] = field(default=None)
    lastChunk: Optional[bool] = field(default=None)


@dataclass
class TaskStatus:
    state: TaskState
    message: Optional[Message] = field(default=None)
    timestamp: Optional[str] = field(default=None)  # Consider using datetime


@dataclass
class Task:
    id: str
    sessionId: str
    status: TaskStatus
    history: Optional[List[Message]] = field(default=None)
    artifacts: Optional[List[Artifact]] = field(default=None)
    metadata: Optional[Dict[str, Any]] = field(default=None)


# Event and Parameter Interfaces as Dataclasses
@dataclass
class TaskStatusUpdateEvent:
    id: str
    status: TaskStatus
    final: bool
    metadata: Optional[Dict[str, Any]] = field(default=None)


@dataclass
class TaskArtifactUpdateEvent:
    id: str
    artifact: Artifact
    metadata: Optional[Dict[str, Any]] = field(default=None)


@dataclass
class Authentication:
    schemes: List[str]
    credentials: Optional[str] = field(default=None)


@dataclass
class PushNotificationConfig:
    url: str
    token: Optional[str] = field(default=None)
    authentication: Optional[Authentication] = field(default=None)


@dataclass
class TaskSendParams:
    id: str
    message: Message
    sessionId: Optional[str] = field(default=None)
    historyLength: Optional[int] = field(default=None)
    pushNotification: Optional[PushNotificationConfig] = field(default=None)
    metadata: Optional[Dict[str, Any]] = field(default=None)


@dataclass
class TaskPushNotificationConfig:
    id: str
    pushNotificationConfig: PushNotificationConfig
