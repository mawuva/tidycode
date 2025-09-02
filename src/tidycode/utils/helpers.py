"""
TidyCode utility helpers.
"""

from typing import List, Tuple, Union
from pathlib import Path


def split_dot_key(dot_key: str) -> Tuple[List[str], str]:
    """
    Split a dot-separated key into a list of strings and the last part.
    """
    parts = dot_key.split(".")
    return parts[:-1], parts[-1]


def join_dot_key(path: List[str], key_name: str) -> str:
    """
    Join a list of strings with a dot separator.
    """
    return ".".join(path + [key_name])


def ensure_file_exists(file_path: Union[str, Path], content: str = "") -> Path:
    """
    Ensure a file exists and create it if it doesn't.
    
    Args:
        file_path (Union[str, Path]): Path to the file.
        content (str): Content to write to the file.
    
    Returns:
        Path: Path to the file.
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
    
    return file_path