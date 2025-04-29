"""
Client module for command-line interface.

This module provides functions for creating and interacting with a CLI client
that connects to an agent for processing messages.
It uses a functional approach with closures for state management.
"""

__all__ = ["create_client", "get_client"]

from typing import Dict, Any, Callable, Awaitable, Optional, Union
from src.agent import create_agent

# Type aliases for better readability
AgentDict = Dict[str, Any]  # Agent dictionary
AgentResponse = Any  # Response from the agent

# Type for the Client dictionary
ClientDict = Dict[str, Union[str, Callable, Awaitable[Any]]]


def create_client(agent_id: str = "chat") -> ClientDict:
    """
    Create a client with the specified agent ID.
    
    Args:
        agent_id: The ID of the agent to connect to
        
    Returns:
        A dictionary of functions for interacting with the client
    """
    agent: Optional[AgentDict] = None
    
    async def run() -> None:
        """
        Initialize the client by creating and running the agent.
        """
        nonlocal agent
        agent = create_agent(agent_id)
        await agent["run"]()
        print(f"Connected to {agent['name']}.")
    
    async def get_user_message() -> str:
        """
        Get a message from the user via the command line.
        
        Returns:
            The user's message
            
        Raises:
            KeyboardInterrupt: If the user enters 'exit' or 'quit'
        """
        message = input("You: ")
        if message.lower() in ["exit", "quit"]:
            raise KeyboardInterrupt
        elif not message:
            print("Please enter a message.")
            return await get_user_message()
        return message
    
    async def post(message: str) -> AgentResponse:
        """
        Post a message to the agent and return the response.
        
        Args:
            message: The message to post to the agent
            
        Returns:
            The agent's response
            
        Raises:
            ValueError: If the agent is not initialized
        """
        if agent is None:
            raise ValueError("Agent not initialized. Call run() first.")
        return await agent["post"](message)
    
    async def get_agent_message(response: AgentResponse) -> None:
        """
        Display the agent's message from the response.
        
        Args:
            response: The response from the agent
        """
        if agent is None:
            raise ValueError("Agent not initialized. Call run() first.")
            
        message = f"{agent['name']}: "
        for part in response.parts:
            if hasattr(part, 'text') and part.text is not None:
                message += part.text
        print(message, end="\n", flush=True)
    
    async def close() -> None:
        """
        Close the client and release resources.
        """
        if agent is not None:
            await agent["close"]()
    
    return {
        "agent_id": agent_id,
        "run": run,
        "get_user_message": get_user_message,
        "post": post,
        "get_agent_message": get_agent_message,
        "close": close
    }


# For backward compatibility
def get_client(agent_id: str = "chat") -> ClientDict:
    """
    Get a client with the specified agent ID.
    This function is maintained for backward compatibility.
    
    Args:
        agent_id: The ID of the agent to connect to
        
    Returns:
        A dictionary of functions for interacting with the client
    """
    return create_client(agent_id)
