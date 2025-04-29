"""
File operation utility functions for the MCP server.

This module provides functions for file operations such as reading,
writing, and listing files.
"""

import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from src.mcp_server.server import mcp

@mcp.tool()
def read_file(file_path: str) -> Dict[str, Any]:
    """
    Read the contents of a file.
    
    Args:
        file_path: Path to the file to read
        
    Returns:
        Dictionary containing the file contents or error information
    """
    try:
        # Validate input
        if not file_path:
            return {
                "success": False,
                "error": "File path cannot be empty",
                "content": None
            }
            
        path = Path(file_path)
        if not path.exists():
            return {
                "success": False,
                "error": f"File not found: {file_path}",
                "content": None
            }
            
        if not path.is_file():
            return {
                "success": False,
                "error": f"Path is not a file: {file_path}",
                "content": None
            }
        
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        return {
            "success": True,
            "error": None,
            "content": content
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "content": None
        }

@mcp.tool()
def write_file(file_path: str, content: str) -> Dict[str, Any]:
    """
    Write content to a file.
    
    Args:
        file_path: Path to the file to write
        content: Content to write to the file
        
    Returns:
        Dictionary indicating success or error information
    """
    try:
        # Validate input
        if not file_path:
            return {
                "success": False,
                "error": "File path cannot be empty"
            }
        
        # Create directory if it doesn't exist
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
        # Write the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return {
            "success": True,
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
def list_files(directory_path: str, recursive: bool = False) -> Dict[str, Any]:
    """
    List files in a directory.
    
    Args:
        directory_path: Path to the directory to list
        recursive: Whether to list files recursively
        
    Returns:
        Dictionary containing the list of files or error information
    """
    try:
        # Validate input
        if not directory_path:
            return {
                "success": False,
                "error": "Directory path cannot be empty",
                "files": None
            }
            
        path = Path(directory_path)
        if not path.exists():
            return {
                "success": False,
                "error": f"Directory not found: {directory_path}",
                "files": None
            }
            
        if not path.is_dir():
            return {
                "success": False,
                "error": f"Path is not a directory: {directory_path}",
                "files": None
            }
        
        # List files
        if recursive:
            files = [str(p.relative_to(path)) for p in path.glob('**/*') if p.is_file()]
        else:
            files = [p.name for p in path.iterdir() if p.is_file()]
            
        return {
            "success": True,
            "error": None,
            "files": files
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "files": None
        }