"""
Main entry point for the application.

This module parses command-line arguments and starts the application.
"""

import asyncio
import sys
import logging
import argparse
from src.main import run

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the application CLI.")
    parser.add_argument(
        "--env",
        default="prod",
        help="The environment to run in (e.g., dev, prod). Defaults to 'prod'.",
    )
    parser.add_argument(
        "--agent",
        default="chat",
        help="The agent ID to use. Defaults to 'chat'.",
    )
    args = parser.parse_args()

    environment = args.env
    agent_id = args.agent

    # Configure logging based on environment
    if environment == "dev":
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        logging.info(f"Starting application in '{environment}' environment with agent '{agent_id}'...")
    else:
        print("Starting...")
    
    try:
        # Run the application and get the exit code
        exit_code = asyncio.run(run(agent_id))
        
        if environment == "dev":
            if exit_code == 0:
                logging.info("Application finished successfully.")
            else:
                logging.warning(f"Application finished with exit code: {exit_code}")
        
        sys.exit(exit_code)

    except FileNotFoundError as e:
        if environment == "dev":
            logging.error(f"Configuration file not found: {e}")
        else:
            print(f"Error: Configuration file not found.")
        sys.exit(1)

    except ImportError as e:
        if environment == "dev":
            logging.error(f"Failed to import necessary module: {e}")
        else:
            print(f"Error: Failed to import necessary module.")
        sys.exit(1)

    except Exception as e:
        if environment == "dev":
            logging.exception(f"An unexpected error occurred during application execution: {e}")
        else:
            print(f"Error: An unexpected error occurred.")
        sys.exit(1)
