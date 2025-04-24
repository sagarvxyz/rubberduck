import sys
import os
import asyncio
from src.agent.core import Agent

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
sys.path.append(os.path.join(file_dir, "src"))


async def run():
    """
    Run the main function of the RubberDuck agent.
    """
    # Load the agent configuration
    agent_id = "Duck"
    agent = Agent(agent_id)

    # Send a message to the agent and handle streaming
    print("...", end="", flush=True)  # Print indicator and flush buffer
    first_chunk_received = False

    async for chunk in agent.send_message("Tell me about yourself."):
        if not first_chunk_received:
            # Clear the "..." indicator by printing backspaces or spaces
            # This is a simple way, more robust methods exist for terminals
            print("\b" * 3 + "   " + "\b" * 3, end="", flush=True)
            first_chunk_received = True

        print(chunk, end="", flush=True)  # Print chunk and flush buffer

    print()  # Print a final newline after the stream ends


if __name__ == "__main__":
    print("Starting RubberDuck...")
    asyncio.run(run())
