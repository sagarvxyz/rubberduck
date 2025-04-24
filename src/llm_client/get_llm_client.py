from src.utils.get_agent_config import get_agent_config
from src.project_types import ILLMClient
from src.llm_client.google_client import GoogleLLMClient


def get_llm_client(agent_id: str) -> ILLMClient:
    """Get an appropriate LLM client instance based on the agent configuration."""
    agent_config = get_agent_config(agent_id)

    if agent_config["model_provider"] == "google":
        return GoogleLLMClient(agent_id)
    elif agent_config["model_provider"] == "openai":
        raise NotImplementedError("OpenAI client is not implemented yet.")
    else:
        raise ValueError(f"Unknown agent ID: {agent_id}")
