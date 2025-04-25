import sys
import os
import asyncio
from src.cli.main import run

if __name__ == "__main__":
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(project_root)

    print("Starting RubberDuck...")
    asyncio.run(run())
