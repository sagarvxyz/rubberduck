"""
Function discovery module for the MCP server.

This module provides functionality for discovering and importing Python modules
containing MCP functions, which triggers the registration of decorated functions
with the MCP server.
"""

import importlib
import importlib.util
import inspect
import os
import sys
import logging
from pathlib import Path
from typing import List, Optional

# Configure logging
logger = logging.getLogger("mcp_server.discovery")

class FunctionDiscovery:
    """
    Discovers and imports Python modules containing MCP functions.
    
    This class handles scanning directories for Python modules and importing them,
    which triggers the registration of decorated functions with the MCP server.
    """
    
    def __init__(self, directories: List[str]):
        """
        Initialize the function discovery with a list of directories to scan.
        
        Args:
            directories: List of directory paths to scan for Python modules
        """
        self.directories = directories
    
    def discover(self) -> None:
        """
        Discover and import all Python modules in the specified directories.
        """
        for directory in self.directories:
            self._discover_in_directory(directory)
    
    def _discover_in_directory(self, directory_path: str) -> None:
        """
        Discover and import all Python modules in a directory and its subdirectories.
        
        Args:
            directory_path: Path to the directory to scan
        """
        directory = Path(directory_path)
        if not directory.exists():
            logger.warning(f"Directory not found: {directory}")
            return
        
        # Add directory to path for importing
        parent_dir = str(directory.parent)
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
        
        # Walk through the directory
        for module_path in directory.glob('**/*.py'):
            if module_path.name.startswith('_'):
                continue
                
            # Convert path to module name
            try:
                relative_path = module_path.relative_to(directory.parent)
                module_name = str(relative_path).replace('/', '.').replace('\\', '.')[:-3]
                
                # Import the module
                module = importlib.import_module(module_name)
                logger.info(f"Imported module: {module_name}")
            except Exception as e:
                logger.error(f"Error importing module {module_path}: {e}")