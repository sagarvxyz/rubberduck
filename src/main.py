import asyncio
from src.client import get_client


async def run(agent_id="main"):
    """
    Starts the conversation loop between the user and agent(s).
    """
    try:
        client = get_client(agent_id)
        while True:
            user_message = client.get_user_message()
            if user_message.lower() in ["exit", "quit"]:
                raise KeyboardInterrupt

            # Process the user message
            response = await client.post(user_message)
            print(f"{client.agent.name}: ", end="", flush=True)
            for part in response.parts:
                print(part.text, end="", flush=True)

    except KeyboardInterrupt:
        print("\nGoodbye!")
        exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)


if __name__ == "__main__":
    asyncio.run(run("main"))
