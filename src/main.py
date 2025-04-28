import asyncio
from src.client import get_client


async def run():
    """
    Starts the conversation loop between the user and agent(s).
    """
    try:
        client = get_client()
        await client.run()

        while True:
            user_message = await client.get_user_message()

            if user_message.lower() in ["exit", "quit"]:
                raise KeyboardInterrupt

            # Process the user message
            response = await client.post(user_message)
            await client.get_agent_message(response)

    except KeyboardInterrupt:
        print("\nGoodbye!")
        exit(0)
    except EOFError:
        print("\nGoodbye!")
        exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)


if __name__ == "__main__":
    asyncio.run(run("main"))
