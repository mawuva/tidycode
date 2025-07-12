"""
Helper functions for pyproject.toml
"""

from pathlib import Path
from typing import Any, Dict, List, Tuple
from .constants import PYPROJECT
from .helpers import toml_load, toml_dump
from tomlkit import table
from copy import deepcopy

def load_pyproject(path: Path) -> Dict[str, Any]:
    """Load the pyproject.toml file and return it as a TOMLKit dict."""
    pyproject_path = path or PYPROJECT
    if not pyproject_path.exists():
        return {}
    with pyproject_path.open("r", encoding="utf-8") as f:
        return toml_load(f.read())

def save_pyproject(data: Dict[str, Any], path: Path) -> None:
    """Save the pyproject.toml file."""
    pyproject_path = path or PYPROJECT
    with pyproject_path.open("w", encoding="utf-8") as f:
        f.write(toml_dump(data))

def has_tool_section(pyproject_data: Dict[str, Any], tool: str) -> bool:
    """Check if a tool section exists in pyproject.toml."""
    return "tool" in pyproject_data and tool in pyproject_data["tool"]

def get_tool_section(pyproject_data: Dict[str, Any], tool: str) -> Dict[str, Any]:
    """Get the tool configuration from pyproject.toml."""
    return pyproject_data.get("tool", {}).get(tool)

def set_tool_section(pyproject_data: Dict[str, Any], tool: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Set the tool configuration in pyproject.toml."""
    if "tool" not in pyproject_data:
        pyproject_data["tool"] = table()
    pyproject_data["tool"][tool] = config
    return pyproject_data

def remove_tool_section(pyproject_data: Dict[str, Any], tool: str) -> bool:
    """
    Remove the section [tool.<section>] from pyproject.toml.
    Return True if removed, False otherwise.
    """
    if "tool" in pyproject_data and tool in pyproject_data["tool"]:
        del pyproject_data["tool"][tool]
        return True
    return False

def remove_tool_section_and_return(
    pyproject_data: Dict[str, Any], tool: str
) -> Dict[str, Any]:
    """
    Remove the section [tool.<section>] from pyproject.toml.
    Returns the modified pyproject_data.
    """
    if "tool" in pyproject_data and tool in pyproject_data["tool"]:
        del pyproject_data["tool"][tool]
    return pyproject_data

def diff_pyproject_config(
    old: Dict[str, Any], new: Dict[str, Any]
) -> List[Tuple[str, str, Any, Any]]:
    """
    Return a list of (type, key, old_value, new_value)
    type = "added", "removed", "changed"
    """
    diffs = []

    old_tools = old.get("tool", {})
    new_tools = new.get("tool", {})

    all_keys = set(old_tools.keys()) | set(new_tools.keys())

    for key in sorted(all_keys):
        old_val = old_tools.get(key)
        new_val = new_tools.get(key)

        if old_val is None and new_val is not None:
            diffs.append(("added", key, None, new_val))
        elif old_val is not None and new_val is None:
            diffs.append(("removed", key, old_val, None))
        elif old_val != new_val:
            diffs.append(("changed", key, old_val, new_val))

    return diffs    

def format_pyproject_diff_plaintext(
    diff: List[Tuple[str, str, Any, Any]]
) -> str:
    """
    Return a readable plain-text version of the pyproject diff.
    """
    lines = []
    for change_type, section, old_val, new_val in diff:
        if change_type == "added":
            lines.append(f"+ [tool.{section}]")
            for k, v in new_val.items():
                lines.append(f"+ {k} = {repr(v)}")
        elif change_type == "removed":
            lines.append(f"- [tool.{section}]")
        elif change_type == "changed":
            lines.append(f"~ [tool.{section}]")
            for k in sorted(set(old_val.keys()) | set(new_val.keys())):
                old_v = old_val.get(k)
                new_v = new_val.get(k)
                if old_v != new_v:
                    lines.append(f"~ {k}: {old_v!r} → {new_v!r}")
    return "\n".join(lines)


def inject_pyproject_config(
    base: Dict[str, Any],
    new_data: Dict[str, Any],
    overwrite: bool = False,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """
    Inject a configuration into the existing TOML content.

    - `overwrite=False` will raise an error if the section exists.
    - `dry_run=True` does not modify the content, but returns the theoretical result.
    """
    updated = deepcopy(base)
    tool_data = new_data.get("tool", {})

    if "tool" not in updated:
        updated["tool"] = table()

    for section, value in tool_data.items():
        if section in updated["tool"] and not overwrite:
            raise ValueError(f"[tool.{section}] already exists in pyproject.toml")
        updated["tool"][section] = value

    if dry_run:
        diff = diff_pyproject_config(base, updated)
        output = format_pyproject_diff_plaintext(diff)
        print(output)

    return updated

