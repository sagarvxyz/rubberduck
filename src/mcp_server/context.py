"""
Context provider for the MCP server.

This module provides the application context for custom functions,
allowing them to access shared resources and configuration.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass
class AppContext:
    """
    Application context for custom functions.
    
    This class provides access to shared resources and configuration
    for custom functions.
    
    Attributes:
        config: Dictionary containing configuration values
    """
    config: Dict[str, Any]
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: The configuration key to retrieve
            default: Default value to return if the key is not found
            
        Returns:
            The configuration value or the default if not found
        """
        return self.config.get(key, default)