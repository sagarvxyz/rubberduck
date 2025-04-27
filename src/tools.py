def read_file(file_path: str) -> str:
    """
    Read the contents of a file and return it as a string.
    Args:
        file_path (str): The path to the file to read.
    Returns:
        str: The contents of the file.
    Raises:
        FileNotFoundError: If the file does not exist.
        IOError: If there is an error reading the file.
    """
    try:
        with open(file_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except IOError:
        raise IOError(f"Error reading file: {file_path}")
    except Exception as e:
        raise Exception(f"An error occurred while reading the file: {e}")


def write_file(file_path: str, content: str) -> None:
    """
    Write content to a file.
    Args:
        file_path (str): The path to the file to write.
        content (str): The content to write to the file.
    Raises:
        IOError: If there is an error writing to the file.
    """
    try:
        with open(file_path, "w") as f:
            f.write(content)
    except IOError:
        raise IOError(f"Error writing to file: {file_path}")
    except Exception as e:
        raise Exception(f"An error occurred while writing to the file: {e}")
