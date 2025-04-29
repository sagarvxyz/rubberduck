"""
Model Context Protocol (MCP) client module.

This module provides functions for interacting with MCP servers,
which enable LLMs to use external tools and resources.
It uses a functional approach with closures for state management.
"""

__all__ = ["create_mcp_client", "get_mcp"]

import os
import yaml
import asyncio
from typing import Dict, List, Any, Callable, Awaitable, Optional, Union
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from contextlib import AsyncExitStack

# Type aliases for better readability
MCPSession = Any  # Represents an MCP client session
MCPTool = Any  # Represents an MCP tool definition
MCPServerParams = List[StdioServerParameters]  # List of server parameters

# Type for the MCP client dictionary
MCPClientDict = Dict[str, Union[Callable, Awaitable[Any]]]


def create_mcp_client(agent_id: str = "chat") -> MCPClientDict:
    """
    Create an MCP client for the specified agent ID.
    
    Args:
        agent_id: The ID of the agent to create a client for
        
    Returns:
        A dictionary of functions for interacting with MCP servers
    """
    server_params = get_mcp_servers(agent_id)
    exit_stack = AsyncExitStack()
    sessions: List[MCPSession] = []
    tool_session_map: Dict[str, MCPSession] = {}
    
    async def run() -> None:
        """
        Connect to MCP servers.
        
        Initializes connections to all configured MCP servers for the agent.
        """
        nonlocal sessions, tool_session_map
        
        try:
            for server in server_params:
                stdio_transport = await exit_stack.enter_async_context(stdio_client(server))
                (stdio, write) = stdio_transport
                session = await exit_stack.enter_async_context(
                    ClientSession(
                        read_stream=stdio,
                        write_stream=write,
                    )
                )
                sessions.append(session)
            # initialize all sessions at once async
            await asyncio.gather(*[session.initialize() for session in sessions])
            print("Connected to MCP servers.")
        except Exception as e:
            print(f"Failed to connect to MCP server: {e}")
    
    async def get_tool_list() -> List[MCPTool]:
        """
        Get the list of tools available in MCP server sessions.
        
        Returns:
            List of available tools
            
        Raises:
            RuntimeError: If MCP sessions are not initialized
        """
        nonlocal sessions, tool_session_map
        tools = []
        
        for session in sessions:
            if not session:
                raise RuntimeError("MCP sessions are not initialized. Please run the server first.")
                
            session_list = await session.list_tools()
            
            for tool in session_list.tools:
                tools.append(tool)
                tool_session_map[tool.name] = session
                
        return tools
    
    async def get_tool_session(tool_name: str) -> MCPSession:
        """
        Get the session for a specific tool.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            Session for the specified tool
            
        Raises:
            ValueError: If the tool is not found in MCP sessions
        """
        if tool_name in tool_session_map:
            return tool_session_map[tool_name]
        else:
            raise ValueError(f"Tool {tool_name} not found in MCP sessions.")
    
    async def close() -> None:
        """
        Close all MCP sessions and clean up resources.
        """
        await exit_stack.aclose()
        sessions.clear()
        tool_session_map.clear()
    
    return {
        "run": run,
        "get_tool_list": get_tool_list,
        "get_tool_session": get_tool_session,
        "close": close
    }


def get_mcp_servers(agent_id: str) -> MCPServerParams:
    """
    Get the MCP server parameters for a given agent ID from the config file.
    
    Args:
        agent_id: The ID of the agent to get server parameters for
        
    Returns:
        List of StdioServerParameters for the agent's tools
        
    Raises:
        FileNotFoundError: If the config file is not found
        ValueError: If there's an error loading the configuration
    """
    try:
        config_path = "./config.yml"
        server_params = []
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"config.yml not found at {config_path}.")

        tool_names = []
        with open(config_path, "r") as config_file:
            config = yaml.safe_load(config_file)
            mcp_servers = config["mcp_servers"]
            tool_names = config["agents"][agent_id]["tools"]

        for tool_name in tool_names:
            if tool_name in mcp_servers:
                # Support for custom function server
                if tool_name == "custom_functions":
                    function_dirs = mcp_servers[tool_name].get("function_dirs", ["src/functions"])
                    function_dirs_str = " ".join([f'"{d}"' for d in function_dirs])
                    command = f"python -m src.mcp_server.server --function-dirs {function_dirs_str}"
                    
                    # Add debug flag if specified
                    if mcp_servers[tool_name].get("debug", False):
                        command += " --debug"
                        
                    server_params.append(StdioServerParameters(
                        command=command,
                        working_dir=".",
                        env=os.environ.copy()
                    ))
                else:
                    server_params.append(StdioServerParameters(**mcp_servers[tool_name]))
            else:
                raise ValueError(f"Tool {tool_name} not found in MCP tools configuration.")
        return server_params

    except Exception as e:
        raise ValueError(f"Error loading agent configuration: {e}")


# For backward compatibility
def get_mcp(agent_id: str = "chat") -> MCPClientDict:
    """
    Get the MCP client for the specified agent ID.
    This function is maintained for backward compatibility.
    
    Args:
        agent_id: The ID of the agent to create a client for
        
    Returns:
        A dictionary of functions for interacting with MCP servers
    """
    return create_mcp_client(agent_id)
