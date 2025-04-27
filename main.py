import asyncio
from src.cli import CLI


if __name__ == "__main__":
    print("Starting...")
    cli = CLI()
    asyncio.run(cli.run())
