__all__ = ["get_client"]

from src.agent import get_agent


def get_client(agent_id="chat"):
    """
    Get the CLI instance.
    """
    return Client(agent_id=agent_id)


class Client:
    """
    Command Line Interface (CLI), with a built in agent to interact with
    other tools and agents.
    """

    def __init__(self, agent_id="chat"):
        self.agent_id = agent_id
        self.agent = None

    async def run(self):

        self.agent = get_agent(agent_id=self.agent_id)
        await self.agent.run()
        print(f"Connected to {self.agent.name}.")

    async def get_user_message(self):
        message = input("You: ")
        if message.lower() in ["exit", "quit"]:
            raise KeyboardInterrupt
        elif not message:
            print("Please enter a message.")
            return await self.get_user_message()
        else:
            print(f"You: {message}")
        return message

    async def post(self, message):
        """
        Post a message to the agent and return the response.
        """
        response = await self.agent.post(message)
        return response

    async def get_agent_message(self, response):
        """
        Get the agent's message from the response.
        """
        message = f"{self.agent.name}: "
        for part in response.parts:
            if part.text:
                message += part.text
        print(message, end="\n", flush=True)
