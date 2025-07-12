"""
Editor for toml files
"""

from typing import Any, Dict
from copy import deepcopy
from tomlkit import table
from .toml_config_diff import diff_configs, format_config_diff
from .toml_helpers import load_toml_file, save_toml_file, PYPROJECT_PATH
from pathlib import Path


def inject_toml_config(
    base: Dict[str, Any],
    new_data: Dict[str, Any],
    overwrite: bool = False,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """
    Inject a configuration into the existing TOML content.
    Inject potentially multiple configurations into the tool key of a new_data dict.

    It reads the tool key in new_data["tool"] with potentially multiple tools (sections),
    and injects each of these sections into updated["tool"].

    - `overwrite=False` will raise an error if the section exists.
    - `dry_run=True` does not modify the content, but returns the theoretical result.
    """
    updated = deepcopy(base)
    tool_data = new_data.get("tool", {})

    if "tool" not in updated:
        updated["tool"] = table()

    for section, value in tool_data.items():
        if section in updated["tool"] and not overwrite:
            raise ValueError(f"[tool.{section}] already exists in toml file")
        updated["tool"][section] = value

    if dry_run:
        diff = diff_configs(base, updated)
        output = format_config_diff(diff)
        print(output)

    return updated

def inject_tool_config(
    base: Dict[str, Any],
    tool_name: str,
    tool_config: Dict[str, Any],
    overwrite: bool = False,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """
    Inject the config for a tool in the [tool.<tool_name>] section of toml file.

    - overwrite=False will raise an error if the config exists.
    - dry_run=True will print the diff without modifying the config.
    """
    updated = deepcopy(base)

    if "tool" not in updated:
        updated["tool"] = table()

    if tool_name in updated["tool"] and not overwrite:
        raise ValueError(f"[tool.{tool_name}] already exists in toml file")

    updated["tool"][tool_name] = tool_config

    if dry_run:
        diff = diff_configs(base, updated)
        print(format_config_diff(diff))

    return updated

def merge_dict_minimal(base: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
    """Add only keys absent from update, without overwriting."""
    merged = deepcopy(base)

    for k, v in update.items():
        if k not in merged:
            merged[k] = v
    return merged


def inject_tool_config_in_file(
    toml_file_path: Path,
    tool_name: str,
    config: Dict[str, Any],
    update_if_exists: bool = False,
    dry_run: bool = False,
) -> None:
    """
    High-level function to manipulate the toml file directly.
    Inject the config for a tool in the [tool.<tool_name>] section of toml file.
    If config is a dict, it will be injected into the tool key of the toml file.

    Parameters:
    - toml_file_path: Path to the toml file.
    - tool_name: Name of the tool to inject the config for.
    - config: Config to inject.
    - update_if_exists: If True, the config will be merged with the existing config.
    - dry_run: If True, the diff will be printed without modifying the config.
    """

    toml_file_path = toml_file_path or PYPROJECT_PATH
    toml_data = load_toml_file(toml_file_path)
    tool_section = toml_data.get("tool", {}).get(tool_name)

    if tool_section is not None:
        if update_if_exists:
            merged_section = merge_dict_minimal(tool_section, config)
            new_tool_data = {tool_name: merged_section}
            updated = inject_toml_config(toml_data, {"tool": new_tool_data}, overwrite=True)
        else:
            raise ValueError(
                f"[tool.{tool_name}] already exists in {toml_file_path}. "
                f"Pass update_if_exists=True to merge."
            )
    else:
        new_tool_data = {tool_name: config}
        updated = inject_toml_config(toml_data, {"tool": new_tool_data}, overwrite=False)

    diff = diff_configs(toml_data, updated)

    if dry_run:
        print(format_config_diff(diff))
    else:
        if diff:
            save_toml_file(updated, toml_file_path)
            print(f"[tool.{tool_name}] injected/updated in {toml_file_path}")
        else:
            print(f"No change for [tool.{tool_name}] in {toml_file_path}")
