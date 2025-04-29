"""
Web utility functions for the MCP server.

This module provides functions for web operations such as fetching data
from URLs and making API requests.
"""

import json
from typing import Dict, Any, Optional
from src.mcp_server.server import mcp

@mcp.tool()
async def fetch_url(url: str) -> Dict[str, Any]:
    """
    Fetch data from a URL.
    
    Args:
        url: URL to fetch data from
        
    Returns:
        Dictionary containing the response data or error information
    """
    try:
        # Validate input
        if not url:
            return {
                "success": False,
                "error": "URL cannot be empty",
                "content": None
            }
        
        # Import here to avoid dependency issues
        import aiohttp
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                content = await response.text()
                
                return {
                    "success": True,
                    "error": None,
                    "status": response.status,
                    "content": content
                }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "content": None
        }

@mcp.tool()
async def fetch_json(url: str) -> Dict[str, Any]:
    """
    Fetch JSON data from a URL.
    
    Args:
        url: URL to fetch JSON data from
        
    Returns:
        Dictionary containing the parsed JSON data or error information
    """
    try:
        # Validate input
        if not url:
            return {
                "success": False,
                "error": "URL cannot be empty",
                "data": None
            }
        
        # Import here to avoid dependency issues
        import aiohttp
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return {
                        "success": False,
                        "error": f"HTTP error: {response.status}",
                        "data": None
                    }
                
                try:
                    data = await response.json()
                    return {
                        "success": True,
                        "error": None,
                        "data": data
                    }
                except json.JSONDecodeError as e:
                    return {
                        "success": False,
                        "error": f"Invalid JSON: {str(e)}",
                        "data": None
                    }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "data": None
        }

@mcp.tool()
async def post_json(url: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Post JSON data to a URL.
    
    Args:
        url: URL to post data to
        data: JSON data to post
        
    Returns:
        Dictionary containing the response data or error information
    """
    try:
        # Validate input
        if not url:
            return {
                "success": False,
                "error": "URL cannot be empty",
                "response": None
            }
        
        # Import here to avoid dependency issues
        import aiohttp
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                content = await response.text()
                
                try:
                    response_data = await response.json()
                except json.JSONDecodeError:
                    response_data = content
                
                return {
                    "success": True,
                    "error": None,
                    "status": response.status,
                    "response": response_data
                }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "response": None
        }

@mcp.resource("weather://{city}")
async def get_weather(city: str) -> Dict[str, Any]:
    """
    Get weather information for a city.
    
    Args:
        city: Name of the city
        
    Returns:
        Weather information for the city
    """
    try:
        # This is a mock implementation
        # In a real application, you would call a weather API
        weather_data = {
            "city": city,
            "temperature": 72,
            "condition": "sunny",
            "humidity": 50,
            "wind_speed": 5
        }
        
        return weather_data
    except Exception as e:
        return {
            "error": str(e)
        }