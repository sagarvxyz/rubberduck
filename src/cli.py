__all__ = ["get_cli"]

from src.agent import get_agent


def get_cli(agent_id="cli"):
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
        self._agent = get_agent(agent_id=agent_id)

    def _get_user_message(self):
        return input("You: ").strip()

    async def _post(self, message):
        """
        Post a message to the agent and return the response.
        """
        response = await self._agent.post(message)
        return response

    async def run(self):
        try:
            while True:
                user_message = self._get_user_message()

                if user_message.lower() == "exit" or user_message.lower() == "quit":
                    raise KeyboardInterrupt

                # Process the user message
                response = await self._post(user_message)
                print(f"{self._agent.name}: ", end="", flush=True)
                for part in response.parts:
                    print(part.text, end="", flush=True)

                print("")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            exit(0)
        except Exception as e:
            print(f"An error occurred: {e}")
            exit(1)
