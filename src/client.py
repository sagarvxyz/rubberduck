__all__ = ["get_client"]

from src.agent import get_agent


def get_client(agent_id="client"):
    """
    Get the CLI instance.
    """
    return CLI(agent_id=agent_id)


class CLI:
    """
    Command Line Interface (CLI), with a built in agent to interact with
    other tools and agents.
    """

    def __init__(self, agent_id="cli"):
        self.agent = get_agent(agent_id=agent_id)

    def get_user_message(self):
        return input("You: ").strip()

    async def post(self, message):
        """
        Post a message to the agent and return the response.
        """
        response = await self.agent.post(message)
        return response
