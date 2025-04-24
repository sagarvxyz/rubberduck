import os
import yaml


def get_agent_config(agent_id: str):
    """
    Get the configuration for a given agent_id (key) from the config.yml file at the project root.
    """
    # project_root = from utils.find_nearest_file import find_nearest_file("agent_config.yml")
    config_path = "./agent_config.yml"
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"agent_config.yml not found at {config_path}.")

    with open(config_path, "r") as config_file:
        config = yaml.safe_load(config_file)
        return config[agent_id]
