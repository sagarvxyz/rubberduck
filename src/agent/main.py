from typing import Dict, List, Optional

from src.llm_client.main import get_llm_client
from src.agent.types import Message, Task, Artifact


class Agent:
    "An interactive, LLM connected 'agent'."

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self._llm_client = get_llm_client(agent_id)

        # Internal storage for server data
        self._messages: List[Message] = []
        self._tasks: Dict[str, Task] = {}
        self._artifacts: Dict[str, Dict[int, Artifact]] = {}  # task_id -> index -> Artifact

    async def post_message(self, message: Message):
        """Processes an incoming Message."""
        self._messages.append(message)
        chunks = self._llm_client.handle_message(message)
        async for chunk in chunks:
            yield chunk
        return

    def post_task(self, task: Task):
        """Processes an incoming Task."""
        print(f"Received Task: {task}")
        self._tasks[task.id] = task
        # Add actual processing logic here

    def post_artifact(self, artifact: Artifact):
        """Processes an incoming Artifact."""
        print(f"Received Artifact: {artifact}")
        if artifact.taskId not in self._artifacts:  # Assuming Artifact dataclass has taskId
            self._artifacts[artifact.taskId] = {}
        self._artifacts[artifact.taskId][artifact.index] = artifact
        # Add actual processing logic here

    def _get_task_by_id(self, task_id: str) -> Optional[Task]:
        """Retrieves a Task by its ID."""
        print(f"Retrieving Task with ID: {task_id}")
        return self._tasks.get(task_id)

    def _get_artifact(self, task_id: str, artifact_index: int) -> Optional[Artifact]:
        """Retrieves an Artifact by Task ID and index."""
        print(f"Retrieving Artifact for Task {task_id} at index {artifact_index}")
        return self._artifacts.get(task_id, {}).get(artifact_index)
