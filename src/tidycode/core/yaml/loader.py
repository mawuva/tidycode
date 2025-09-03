"""
YAML file loader.
"""

from pathlib import Path
from typing import Dict, Union

from yaml import safe_load as yaml_safe_load, safe_dump as yaml_safe_dump



def load_yaml_file(file_path: Union[str, Path]) -> Dict:
    """
    Load a YAML file and parse it into a Python object.
    
    Args:
        file_path (Union[str, Path]): Path to the YAML file.
        
    Returns:
        Dict: Parsed YAML content.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        Exception: If there is an error reading or parsing the file.
    """
    file_path = Path(file_path)
    
    try:
        with file_path.open("r", encoding="utf-8") as f:
            return yaml_safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error reading file: {file_path}, {e}")


def save_yaml_file(file_path: Union[str, Path], data: Dict) -> None:
    """
    Save a dictionary to a YAML file.
    
    Args:
        file_path (Union[str, Path]): Path to the YAML file.
        data (Dict): Dictionary to save.
        
    Raises:
        PermissionError: If the file cannot be written due to permissions.
        Exception: If there is an error during writing.
    """
    file_path = Path(file_path)
    
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("w", encoding="utf-8") as f:
            yaml_safe_dump(data, f, encoding="utf-8")
    except PermissionError:
        raise PermissionError(f"Impossible to write file: {file_path}. Check permissions")
    except Exception as e:
        raise Exception(f"Error writing file: {file_path}, {e}")