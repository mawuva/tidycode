"""
Helpers for the pyproject module.
"""

from typing import Dict, Any, Generator
from pathlib import Path

from tidycode.core.pyproject.types import (
    PyProjectHiddenSections,
    SensitiveKeys,
    SensitiveKeywords,
)
from tidycode.core.toml import TomlFileManager
from tidycode.settings import PYPROJECT_FILE_PATH

def has_subsections(data: Dict[str, Any]) -> bool:
    """Check if the data has subsections."""
    return any(isinstance(value, dict) for value in data.values())


def list_subsections(data: Dict[str, Any]) -> list[str]:
    """List the subsections of the data."""
    return [key for key, value in data.items() if isinstance(value, dict)]



def get_section_keys(data: Dict[str, Any], hidden_keys: list[str] = []) -> list[str]:
    """Get the keys of the data."""
    hidden_keys = hidden_keys if hidden_keys else PyProjectHiddenSections.to_list()
    return [key for key in data.keys() if key not in hidden_keys]


def is_sensitive_key(key: str, path: str | None = None) -> bool:
    """
    Check if a key (or its full dotted path) should be considered sensitive.

    Args:
        key: Current key name (case-insensitive).
        path: Full dotted path (e.g. "tool.poetry.dependencies.requests")

    Returns:
        True if the key or path matches a sensitive key/keyword, False otherwise.
    """
    lower_key = key.lower()

    # Match simple sensitive keys (api_key, token, etc.)
    if lower_key in SensitiveKeys.to_list():
        return True

    if path:
        lower_path = path.lower()
        # Match sensitive keywords anywhere in the dotted path
        for kw in SensitiveKeywords.to_list():
            if kw in lower_path:
                return True

    return False


def iter_keys(
    data: dict,
    *,
    parent_path: str = "",
    hide_sensitive: bool = True,
) -> Generator[tuple[str, str], None, None]:
    """
    Yield (path, key) for keys in a nested dict, respecting hide_sensitive.

    Args:
        data: The dictionary to inspect.
        parent_path: Current dot path prefix.
        hide_sensitive: Whether to hide sensitive keys/paths.

    Yields:
        Tuples of (full_path, key).
        Example: ("tool.poetry.dependencies.requests", "requests")
    """
    for key, value in data.items():
        current_path = f"{parent_path}.{key}" if parent_path else key

        if hide_sensitive and is_sensitive_key(key, path=current_path):
            continue

        yield current_path, key

        if isinstance(value, dict):
            yield from iter_keys(
                value, parent_path=current_path, hide_sensitive=hide_sensitive
            )


def get_keys(data: dict, *, hide_sensitive: bool = True) -> list[str]:
    """
    Return a list of full dotted keys that are visible in the given dict.

    Args:
        data: The dictionary to inspect.
        hide_sensitive: Whether to hide sensitive keys/paths.

    Returns:
        A list of dotted keys.
    """
    return [path for path, _ in iter_keys(data, hide_sensitive=hide_sensitive)]


def iter_key_values(
    data: dict,
    *,
    parent_path: str = "",
    hide_sensitive: bool = True,
) -> Generator[tuple[str, str, object], None, None]:
    """
    Yield (path, key, value) for keys in a nested dict, respecting hide_sensitive.

    Args:
        data: The dictionary to inspect.
        parent_path: Current dot path prefix.
        hide_sensitive: Whether to hide sensitive keys/paths.

    Yields:
        Tuples of (full_path, key, value).
        Example: ("tool.poetry.dependencies.requests", "requests", "^2.31.0")
    """
    for key, value in data.items():
        current_path = f"{parent_path}.{key}" if parent_path else key

        if hide_sensitive and is_sensitive_key(key, path=current_path):
            continue

        yield current_path, key, value

        if isinstance(value, dict):
            yield from iter_key_values(
                value, parent_path=current_path, hide_sensitive=hide_sensitive
            )


def get_key_values(data: dict, *, hide_sensitive: bool = True) -> dict[str, object]:
    """
    Return a dict of dotted key -> value pairs that are visible in the given dict.

    Args:
        data: The dictionary to inspect.
        hide_sensitive: Whether to hide sensitive keys/paths.

    Returns:
        Dict mapping full dotted keys to values.
    """
    return {
        path: value
        for path, _, value in iter_key_values(data, hide_sensitive=hide_sensitive)
    }


def filter_dict(data: dict, *, hide_sensitive: bool, show_values: bool) -> dict:
    """Return a filtered dict (hierarchical) according to flags."""
    result = {}
    for key, value in data.items():
        # ignore sensitive keys
        if hide_sensitive and is_sensitive_key(key):
            continue

        if isinstance(value, dict):
            nested = filter_dict(
                value, hide_sensitive=hide_sensitive, show_values=show_values
            )
            if nested:
                result[key] = nested
        else:
            if show_values:
                result[key] = value
            else:
                result[key] = {}
    return result


def load_tidycode_config(pyproject_path: Path | str = PYPROJECT_FILE_PATH) -> dict:
    """
    Load only the tidycode config:
    {
        "target": ".",
        "verbose": False,
        "check-only": False,
        "tools": ["black", "isort", "ruff", "mypy"]
        ...
    }
    """
    manager = TomlFileManager(pyproject_path)
    return manager.get_section("tool.tidycode", default={})
