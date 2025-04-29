# MCP Server with Custom Functions

This directory contains the implementation of a locally running MCP (Model Context Protocol) server with custom functions that integrates with the existing Python application.

## Overview

The MCP server allows you to define custom functions that can be discovered and used by LLMs (Large Language Models) through the Model Context Protocol. The server follows the FastMCP patterns from the Python SDK and provides a flexible architecture for adding custom functions.

## Directory Structure

```
src/
  mcp_server/
    __init__.py       # Package initialization
    server.py         # Main FastMCP server implementation
    discovery.py      # Function discovery mechanism
    context.py        # Context provider for functions
  functions/          # Directory for custom functions
    utils/            # Utility functions
      file_ops.py     # File operation functions
      web_utils.py    # Web utility functions
    examples/         # Example functions
      hello_world.py  # Simple example functions
```

## How It Works

1. The server is initialized with a list of directories to scan for functions
2. The function discovery mechanism scans these directories for Python modules
3. Functions decorated with `@mcp.tool()` are automatically registered with the server
4. The server exposes these functions to LLMs through the MCP protocol

## Adding Custom Functions

To add a custom function, create a new Python module in the `src/functions` directory (or any directory specified in the configuration) and define your function using the `@mcp.tool()` decorator:

```python
from src.mcp_server.server import mcp

@mcp.tool()
def my_custom_function(param1: str, param2: int) -> dict:
    """
    Description of what your function does.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of the return value
    """
    # Your function implementation
    result = {"param1": param1, "param2": param2}
    return result
```

## Adding Resources

Resources are similar to functions but are accessed through URIs. To add a resource, use the `@mcp.resource()` decorator:

```python
from src.mcp_server.server import mcp

@mcp.resource("my-resource://path/{param}")
def my_custom_resource(param: str) -> dict:
    """
    Description of what your resource provides.
    
    Args:
        param: Description of param
        
    Returns:
        Description of the return value
    """
    # Your resource implementation
    return {"param": param, "data": "Some data"}
```

## Configuration

The MCP server is configured in the `config.yml` file:

```yaml
mcp_servers:
  custom_functions:
    function_dirs:
      - "src/functions"
      - "path/to/other/functions"  # Additional directories can be added
    debug: false  # Set to true for debug logging
```

To use the custom functions server with an agent, add it to the agent's tools list:

```yaml
agents:
  chat:
    name: "Assistant"
    tools:
      - custom_functions
```

## Running the Server

The server is automatically started when the main application runs and the agent is configured to use the custom functions.

You can also run the server directly for testing:

```bash
python test_mcp_server.py
```

Or with specific function directories:

```bash
python test_mcp_server.py src/functions path/to/other/functions
```

## Development

For development and testing, you can use the MCP Inspector:

```bash
mcp dev src/mcp_server/server.py --with-editable .
```

This will allow you to test your server with the MCP Inspector UI, making it easier to debug and develop your custom functions.