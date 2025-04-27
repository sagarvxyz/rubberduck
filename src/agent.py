__all__ = ["get_agent"]


def get_agent_config(agent_id: str):
    """
    Get the configuration for a given agent_id (key) from the agent_config.yml file at the project root.
    """
    import os
    import yaml

    try:
        config_path = "./agent_config.yml"
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"agent_config.yml not found at {config_path}.")

        with open(config_path, "r") as config_file:
            config = yaml.safe_load(config_file)
            return config[agent_id]

    except Exception as e:
        raise ValueError(f"Error loading agent configuration: {e}")


def get_agent(agent_id: str):
    """
    Get the agent instance based on the agent_id.
    """

    agent_config = get_agent_config(agent_id)
    if agent_config["model_provider"] == "google":
        from src.llm import get_llm_client

        return Agent(
            agent_config=agent_config,
            llm_client=get_llm_client(agent_id),
        )

    else:
        raise ValueError(f"Unsupported model provider: {agent_config['model_provider']}")


class Agent:
    """
    An LLM connected agent that can process messages and interact with a user or other agents.
    Each agent maintains a full history of messages and responses.
    """

    def __init__(self, agent_config, llm_client):
        self.name = agent_config["name"]
        self.config = agent_config
        self._llm_client = llm_client
        self._history = []

    async def post(self, message):
        """
        Post a message to the agent and return the response.
        """

        new_content = self._llm_client.create_content(
            content=message,
            type="text",
            role="user",
        )

        self._history.append(new_content)

        response = await self._llm_client.post(contents=self._history, config=self.config)
        if not response:
            raise ValueError("No response received from the LLM client.")
        content = self._llm_client.create_content(
            content=response.text,
            type="text",
            role="model",
        )
        self._history.append(content)
        return content
