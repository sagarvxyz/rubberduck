"""
File system utility functions for reading and writing files.

This module provides pure functions for common file operations used throughout the application.
"""

from typing import Optional, Union, TextIO, BinaryIO
import os

def read_file(file_path: str, binary: bool = False) -> Union[str, bytes]:
    """
    Read the contents of a file and return it as a string or bytes.
    
    Args:
        file_path (str): The path to the file to read.
        binary (bool, optional): Whether to read the file in binary mode. Defaults to False.
        
    Returns:
        Union[str, bytes]: The contents of the file as a string or bytes.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        IOError: If there is an error reading the file.
    """
    mode = "rb" if binary else "r"
    try:
        with open(file_path, mode) as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except IOError:
        raise IOError(f"Error reading file: {file_path}")
    except Exception as e:
        raise Exception(f"An error occurred while reading the file: {e}")



def write_file(file_path: str, content: Union[str, bytes], binary: bool = False) -> None:
    """
    Write content to a file.
    
    Args:
        file_path (str): The path to the file to write.
        content (Union[str, bytes]): The content to write to the file.
        binary (bool, optional): Whether to write the file in binary mode. Defaults to False.
        
    Raises:
        IOError: If there is an error writing to the file.
    """
    # Create directory if it doesn't exist
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
        
    mode = "wb" if binary else "w"
    try:
        with open(file_path, mode) as f:
            f.write(content)
    except IOError:
        raise IOError(f"Error writing to file: {file_path}")
    except Exception as e:
        raise Exception(f"An error occurred while writing to the file: {e}")


def ensure_directory(directory_path: str) -> None:
    """
    Ensure that a directory exists, creating it if necessary.
    
    Args:
        directory_path (str): The path to the directory to ensure exists.
        
    Raises:
        IOError: If there is an error creating the directory.
    """
    try:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
    except IOError:
        raise IOError(f"Error creating directory: {directory_path}")
    except Exception as e:
        raise Exception(f"An error occurred while creating the directory: {e}")
