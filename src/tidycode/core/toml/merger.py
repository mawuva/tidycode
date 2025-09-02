"""
TOML file merger.
"""

from pathlib import Path
from typing import Any, Mapping, Union

from tomlkit import TOMLDocument, table
from tomlkit.items import Table

from .loader import load_toml_file, save_toml_file

TomlLike = Union[TOMLDocument, Table]


def merge_toml(
    base: TomlLike, new: Mapping[str, Any], overwrite: bool = True
) -> TomlLike:
    """
    Deep merge a dictionary-like mapping into a TOMLDocument or Table.

    Args:
        base (TomlLike): The existing TOML structure (TOMLDocument or Table).
        new (Mapping[str, Any]): The dictionary to merge into `base`.
        overwrite (bool): Whether to overwrite existing keys.

    Returns:
        TomlLike: The merged TOML object.
    """
    for key, value in new.items():
        if isinstance(value, dict):
            if key not in base or not isinstance(base[key], (TOMLDocument, Table)):
                base[key] = table()
            merge_toml(base[key], value, overwrite)  # type: ignore[arg-type]
        else:
            if overwrite or key not in base:
                base[key] = value
            elif value is None and key in base:
                base[key] = table()
    return base


def update_toml_file(
    path: Union[str, Path], new_data: Mapping[str, Any], overwrite: bool = True
) -> TomlLike:
    """
    Load a TOML file, merge new data into it, and save the updated content.

    Args:
        path (Union[str, Path]): Path to the TOML file.
        new_data (Mapping[str, Any]): Data to merge into the TOML.
        overwrite (bool): Whether to overwrite existing keys.

    Returns:
        TomlLike: The merged TOML object.
    """
    doc = load_toml_file(path)
    merged = merge_toml(doc, new_data, overwrite)
    save_toml_file(path, merged)
    return merged
