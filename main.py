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
    args = parser.parse_args()

    environment = args.env

    if environment == "dev":
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        logging.info(f"Starting application in '{environment}' environment...")
    else:
        print("Starting...")
    try:
        asyncio.run(run())

        if environment == "dev":
            logging.info("Application finished successfully.")

    except FileNotFoundError as e:
        if environment == "dev":
            logging.error(f"Configuration file not found: {e}")
        sys.exit(1)

    except ImportError as e:
        if environment == "dev":
            logging.error(f"Failed to import necessary module: {e}")
        sys.exit(1)

    except Exception as e:
        if environment == "dev":
            logging.exception(f"An unexpected error occurred during application execution: {e}")
        sys.exit(1)
