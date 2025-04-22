import sys
import os
import urllib3
import yaml

from src.app import app


urllib3.disable_warnings()
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))


def load_config():
    """
    Load the configuration from the config.json file.
    """
    config_path = os.path.join(os.path.dirname(__file__), "config.yml")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path, "r") as config_file:
        config = yaml.safe_load(config_file)

        return config["main"]


if __name__ == "__main__":
    print("Starting RubberDuck...")
    config = load_config()
    # Pass the loaded config dictionary to the app function
    app(config)
