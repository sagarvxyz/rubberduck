"""
Main entry point for the application.

This module starts the conversation loop between the user and agent(s).
"""

import asyncio
from typing import Optional
from src.client import create_client


async def run(agent_id: str = "chat") -> None:
    """
    Starts the conversation loop between the user and agent(s).
    
    Args:
        agent_id: The ID of the agent to connect to
    """
    client = None
    try:
        # Create and initialize the client
        client = create_client(agent_id)
        await client["run"]()

        # Main conversation loop
        while True:
            user_message = await client["get_user_message"]()

            if user_message.lower() in ["exit", "quit"]:
                raise KeyboardInterrupt

            # Process the user message
            response = await client["post"](user_message)
            await client["get_agent_message"](response)

    except KeyboardInterrupt:
        print("\nGoodbye!")
    except EOFError:
        print("\nGoodbye!")
    except Exception as e:
        print(f"An error occurred: {e}")
        return 1
    finally:
        # Clean up resources
        if client:
            try:
                await client["close"]()
            except Exception as e:
                print(f"Error during cleanup: {e}")
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(run())
    exit(exit_code)
