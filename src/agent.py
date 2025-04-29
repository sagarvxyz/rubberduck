"""
Agent module for LLM-powered conversational agents.

This module provides functions for creating and interacting with agents
that can process messages and interact with users or other agents.
It uses a functional approach with closures for state management.
"""

__all__ = ["create_agent", "get_agent"]

import os
import yaml
from typing import Dict, List, Any, Callable, Awaitable, Optional, Union

from src.llm import create_llm_client
from src.mcp import create_mcp_client

# Type aliases for better readability
AgentConfig = Dict[str, Any]  # Agent configuration
LLMContent = Any  # Content in the format expected by the LLM
LLMResponse = Any  # Response from the LLM
MCPTool = Any  # MCP tool definition

# Type for the Agent dictionary
AgentDict = Dict[str, Union[str, AgentConfig, Callable, Awaitable[Any]]]


def create_agent(agent_id: str) -> AgentDict:
    """
    Create an agent with the specified ID.
    
    Args:
        agent_id: The ID of the agent to create
        
    Returns:
        A dictionary of functions and properties for interacting with the agent
        
    Raises:
        ValueError: If the model provider is unsupported
    """
    agent_config = get_agent_config(agent_id)
    
    if agent_config["model_provider"] != "google":
        raise ValueError(f"Unsupported model provider: {agent_config['model_provider']}")
    
    # Create clients
    llm_client = create_llm_client(agent_id)
    mcp_client = create_mcp_client(agent_id)
    
    # Initialize state
    history: List[LLMContent] = []
    name = agent_config["name"]
    
    async def run() -> None:
        """
        Initialize the agent by setting up the LLM and MCP clients.
        """
        llm_client["run"]()
        await mcp_client["run"]()
    
    async def post(message: str) -> LLMContent:
        """
        Post a message to the agent and return the response.
        
        Args:
            message: The message to post to the agent
            
        Returns:
            The agent's response content
            
        Raises:
            ValueError: If no response is received or a tool session is not found
        """
        nonlocal history
        
        # Create content from user message
        new_content = llm_client["create_content"](
            content=message,
            type="text",
            role="user"
        )
        history.append(new_content)
        
        # Get available tools and format them for the LLM
        mcp_tools = await mcp_client["get_tool_list"]()
        llm_tools = llm_client["create_tools"](mcp_tools)
        
        # Send message to LLM
        response = await llm_client["post"](
            contents=history,
            agent_config=agent_config,
            tools=llm_tools
        )
        
        if not response:
            raise ValueError("No response received from the LLM client.")
        
        # Handle tool calls if present
        if response.candidates[0].content.parts[0].function_call:
            function_call = response.candidates[0].content.parts[0].function_call
            
            session = await mcp_client["get_tool_session"](function_call.name)
            if not session:
                raise ValueError(f"Session for tool {function_call.name} not found.")
                
            # Call the MCP server with the predicted tool
            result = await session.call_tool(function_call.name, arguments=function_call.args)
            response = result.content[0]
        
        # Create content from model response
        content = llm_client["create_content"](
            content=response.text,
            type="text",
            role="model"
        )
        history.append(content)
        return content
    
    async def clear_history() -> None:
        """
        Clear the conversation history.
        """
        nonlocal history
        history = []
    
    async def close() -> None:
        """
        Close the agent and release resources.
        """
        await mcp_client["close"]()
        await clear_history()
    
    # Return a dictionary with agent properties and functions
    return {
        "name": name,
        "agent_id": agent_id,
        "config": agent_config,
        "run": run,
        "post": post,
        "clear_history": clear_history,
        "close": close
    }


def get_agent_config(agent_id: str) -> AgentConfig:
    """
    Get the configuration for a given agent_id from the config.yml file.
    
    Args:
        agent_id: The ID of the agent to get configuration for
        
    Returns:
        The agent's configuration
        
    Raises:
        FileNotFoundError: If the config file is not found
        ValueError: If there's an error loading the configuration
    """
    import os
    import yaml

    try:
        config_path = "./config.yml"
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"config.yml not found at {config_path}.")

        with open(config_path, "r") as config_file:
            config = yaml.safe_load(config_file)
            return config["agents"][agent_id]

    except Exception as e:
        raise ValueError(f"Error loading agent configuration: {e}")


# For backward compatibility
def get_agent(agent_id: str) -> AgentDict:
    """
    Get the agent with the specified ID.
    This function is maintained for backward compatibility.
    
    Args:
        agent_id: The ID of the agent to create
        
    Returns:
        A dictionary of functions and properties for interacting with the agent
    """
    return create_agent(agent_id)
