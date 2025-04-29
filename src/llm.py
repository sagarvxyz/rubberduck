"""
LLM (Large Language Model) client module.

This module provides functions for interacting with various LLM providers.
It uses a functional approach with closures for state management.
"""

__all__ = ["create_llm_client"]

import os
import mimetypes
from typing import Dict, List, Any, Callable, Awaitable, Optional, Union
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Default configuration
default_model_name = "gemini-2.0-flash"
default_config = types.GenerateContentConfigDict()

# Type aliases for better readability
LLMContent = Any  # Represents content in the format expected by the LLM
LLMResponse = Any  # Represents a response from the LLM
LLMTool = Any  # Represents a tool definition for the LLM

# Type for the LLM client dictionary
LLMClientDict = Dict[str, Union[Callable, Awaitable[Any]]]


def create_llm_client(agent_id: str) -> LLMClientDict:
    """
    Create an LLM client based on the agent ID.
    
    Args:
        agent_id: The ID of the agent to create a client for
        
    Returns:
        A dictionary of functions for interacting with the LLM
        
    Raises:
        ValueError: If the agent ID corresponds to an unsupported model provider
    """
    if agent_id:
        return create_google_llm_client()
    else:
        raise ValueError(f"Unsupported model provider: {agent_id}")


def create_google_llm_client() -> LLMClientDict:
    """
    Create a Google LLM client.
    
    Returns:
        A dictionary of functions for interacting with Google's Gemini model
    """
    client = None
    
    def run() -> None:
        """
        Initialize the Google GenAI client.
        
        Raises:
            ValueError: If the API key is not found in environment variables
        """
        nonlocal client
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError(
                "API key not found. Please set the GOOGLE_API_KEY environment variable."
            )
        client = genai.Client(api_key=api_key)
    
    def create_content(content: Any, type: str = "text", role: str = "user") -> LLMContent:
        """
        Convert content into the proper format for the Google API.
        
        Args:
            content: The content to convert
            type: The type of content ('text' or 'file')
            role: The role of the content creator ('user' or 'model')
            
        Returns:
            Formatted content object for the Google API
            
        Raises:
            ValueError: If the message type is unsupported or MIME type cannot be determined
        """
        if type == "text":
            return types.Content(parts=[types.Part.from_text(text=content)], role=role)
        elif type == "file":
            (mime_type, _encoding) = mimetypes.guess_type(content)
            if mime_type is None:
                raise ValueError(f"Could not determine MIME type for file: {content}")
            return types.Content(
                role, parts=[types.Part.from_uri(file_uri=content, mime_type=mime_type)]
            )
        else:
            raise ValueError(f"Unsupported message type: {type}")
    
    def create_tools(tools: List[Any]) -> List[LLMTool]:
        """
        Convert tools from MCP to Gemini format.
        
        Args:
            tools: List of MCP tool definitions
            
        Returns:
            List of tools formatted for the Google API
        """
        llm_tools = []
        for tool in tools:
            parameters = {}
            for key, value in tool.inputSchema.items():
                if key not in ["additionalProperties", "$schema"]:
                    # Process the schema to handle null types
                    processed_value = _process_schema_value(value)
                    parameters[key] = processed_value
            try:
                llm_tool = types.Tool(
                    function_declarations=[
                        {
                            "name": tool.name,
                            "description": tool.description,
                            "parameters": parameters,
                        }
                    ]
                )
                llm_tools.append(llm_tool)
            except Exception:
                continue
        return llm_tools
    
    def _process_schema_value(value: Any) -> Any:
        """
        Process a schema value to handle null types properly.
        
        Args:
            value: The schema value to process
            
        Returns:
            The processed schema value
        """
        # Handle anyOf with null type
        if isinstance(value, dict) and "anyOf" in value:
            # Check if any of the anyOf options is a null type
            has_null_type = any(
                isinstance(option, dict) and
                option.get("type") == "null"
                for option in value["anyOf"]
            )
            
            if has_null_type:
                # Find the non-null type option
                non_null_options = [
                    option for option in value["anyOf"]
                    if not (isinstance(option, dict) and option.get("type") == "null")
                ]
                
                if non_null_options:
                    # Use the first non-null option as the base
                    result = non_null_options[0].copy() if isinstance(non_null_options[0], dict) else non_null_options[0]
                    
                    # If it's a dict, set nullable=True
                    if isinstance(result, dict):
                        result["nullable"] = True
                        
                    # Copy other properties from the original value
                    if isinstance(value, dict) and isinstance(result, dict):
                        for k, v in value.items():
                            if k != "anyOf" and k not in result:
                                result[k] = v
                                
                    return result
        
        # Recursively process nested dictionaries
        if isinstance(value, dict):
            result = {}
            for k, v in value.items():
                result[k] = _process_schema_value(v)
            return result
        
        # Recursively process lists
        if isinstance(value, list):
            return [_process_schema_value(item) for item in value]
            
        return value
    
    async def post(contents: List[LLMContent], agent_config: Dict[str, Any] = {}, tools: List[LLMTool] = []) -> LLMResponse:
        """
        Post contents to the Google GenAI client.
        
        Args:
            contents: The contents to post
            agent_config: Configuration for the agent
            tools: List of tools to make available
            
        Returns:
            Response from the LLM
            
        Raises:
            ValueError: If no contents are provided or client is not initialized
        """
        if client is None:
            raise ValueError("Client not initialized. Call run() first.")
            
        merged_config = default_config | agent_config.get("config", {})
        
        if not contents:
            raise ValueError("No contents provided to post.")
            
        response = await client.aio.models.generate_content(
            model=agent_config.get("model_name", default_model_name),
            contents=contents,
            config=types.GenerateContentConfig(**merged_config, tools=tools),
        )
        
        return response
    
    # Return a dictionary of functions
    return {
        "run": run,
        "create_content": create_content,
        "create_tools": create_tools,
        "post": post
    }


# For backward compatibility
def get_llm_client(agent_id: str) -> LLMClientDict:
    """
    Get the LLM client based on the agent ID.
    This function is maintained for backward compatibility.
    
    Args:
        agent_id: The ID of the agent to create a client for
        
    Returns:
        A dictionary of functions for interacting with the LLM
    """
    return create_llm_client(agent_id)
