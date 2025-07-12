"""
Helper functions for toml files
"""

from pathlib import Path
from typing import Any, Dict
from ..constants import PYPROJECT_PATH
from tomlkit import table, dumps, parse
import re


def toml_dump(data: dict) -> str:
    """Dump a dictionary to a TOML string."""
    return dumps(data)


def toml_load(text: str) -> dict:
    """Load a TOML string to a dictionary."""
    return parse(text)


def load_toml_file(path: Path = None) -> Dict[str, Any]:
    """Load the toml file and return it as a TOMLKit dict."""
    toml_file_path = path or PYPROJECT_PATH
    if not toml_file_path.exists():
        return {}
    with toml_file_path.open("r", encoding="utf-8") as f:
        return toml_load(f.read())


def save_toml_file(data: Dict[str, Any], path: Path = None) -> None:
    """Save the toml file."""
    toml_file_path = path or PYPROJECT_PATH
    raw = toml_dump(data)

    formatted = re.sub(r"\n(?=\[)", "\n\n", raw)

    with toml_file_path.open("w", encoding="utf-8") as f:
        f.write(formatted.strip() + "\n")


def has_tool_section(data: Dict[str, Any], tool: str) -> bool:
    """Check if a tool section exists in toml file."""
    return "tool" in data and tool in data["tool"]


def get_tool_section(data: Dict[str, Any], tool: str) -> Dict[str, Any]:
    """Get the tool configuration from toml file."""
    return data.get("tool", {}).get(tool)


def set_tool_section(
    data: Dict[str, Any], tool: str, config: Dict[str, Any]
) -> Dict[str, Any]:
    """Set the tool configuration in toml file."""
    if "tool" not in data:
        data["tool"] = table()
    data["tool"][tool] = config
    return data


def remove_tool_section(data: Dict[str, Any], tool: str) -> bool:
    """
    Remove the section [tool.<section>] from toml file.
    Return True if removed, False otherwise.
    """
    if "tool" in data and tool in data["tool"]:
        del data["tool"][tool]
        return True
    return False


def remove_tool_section_and_return(data: Dict[str, Any], tool: str) -> Dict[str, Any]:
    """
    Remove the section [tool.<section>] from toml file.
    Returns the modified data
    """
    if "tool" in data and tool in data["tool"]:
        del data["tool"][tool]
    return data
