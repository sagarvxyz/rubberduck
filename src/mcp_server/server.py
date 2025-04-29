"""
Main FastMCP server implementation.

This module provides the main FastMCP server implementation that handles
discovering and registering custom functions, and running the server.
"""

from mcp.server.fastmcp import FastMCP, Context
import argparse
import logging
import os
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional

from src.mcp_server.discovery import FunctionDiscovery
from src.mcp_server.context import AppContext

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("mcp_server")

# Create the FastMCP server
mcp = FastMCP("Custom Function Server")

def load_config() -> Dict[str, Any]:
    """
    Load configuration from config.yml.
    
    Returns:
        Dictionary containing configuration values
    """
    config_path = "./config.yml"
    if not os.path.exists(config_path):
        logger.warning(f"Config file not found at {config_path}, using default configuration")
        return {}
    
    try:
        with open(config_path, "r") as config_file:
            config = yaml.safe_load(config_file)
            return config.get("custom_functions", {})
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        return {}

def run_server(function_dirs: List[str], debug: bool = False) -> None:
    """
    Run the MCP server with the specified function directories.
    
    Args:
        function_dirs: List of directories containing function modules
        debug: Whether to run in debug mode
    """
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Running in debug mode")
    
    # Load configuration
    config = load_config()
    logger.info(f"Loaded configuration: {config}")
    
    # Create application context
    app_context = AppContext(config=config)
    
    # Discover functions
    discovery = FunctionDiscovery(function_dirs)
    discovery.discover()
    
    # Run the server
    logger.info("Starting MCP server")
    mcp.run()

def main() -> None:
    """
    Main entry point for the MCP server.
    """
    parser = argparse.ArgumentParser(description="Run the MCP server with custom functions")
    parser.add_argument("--function-dirs", nargs="+", default=["src/functions"], 
                        help="Directories containing function modules to discover")
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    args = parser.parse_args()
    
    try:
        run_server(args.function_dirs, args.debug)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.exception(f"Error running server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()