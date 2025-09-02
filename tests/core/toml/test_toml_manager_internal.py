"""
TidyCode TOML Manager Internal Methods Tests
"""

from pathlib import Path

import pytest
from tomlkit import document as toml_document
from tomlkit import table as toml_table
from tomlkit.items import Table

from tidycode.core.toml.manager import TomlFileManager


def test_toml_file_manager_resolve_dot_key():
    """
    Scenario:
        Use _resolve method with dot_key parameter.

    Expected:
        Returns correct path and key_name tuple.
    """
    file_path = Path("dummy.toml")
    manager = TomlFileManager.__new__(TomlFileManager)
    manager.path = file_path
    manager.document = toml_document()

    path, key_name = manager._resolve("section.subsection.key", None, None)
    assert path == ["section", "subsection"]
    assert key_name == "key"


def test_toml_file_manager_resolve_path_key_name():
    """
    Scenario:
        Use _resolve method with path and key_name parameters.

    Expected:
        Returns correct path and key_name tuple.
    """
    file_path = Path("dummy.toml")
    manager = TomlFileManager.__new__(TomlFileManager)
    manager.path = file_path
    manager.document = toml_document()

    path, key_name = manager._resolve(None, ["section", "subsection"], "key")
    assert path == ["section", "subsection"]
    assert key_name == "key"


def test_toml_file_manager_resolve_no_parameters():
    """
    Scenario:
        Use _resolve method without any parameters.

    Expected:
        ValueError is raised.
    """
    file_path = Path("dummy.toml")
    manager = TomlFileManager.__new__(TomlFileManager)
    manager.path = file_path
    manager.document = toml_document()

    with pytest.raises(
        ValueError, match="You must provide either dot_key or \\(path \\+ key_name\\)"
    ):
        manager._resolve(None, None, None)


def test_toml_file_manager_navigate_existing_path():
    """
    Scenario:
        Navigate to an existing path in the TOML structure.

    Expected:
        Returns the correct table at the specified path.
    """
    file_path = Path("dummy.toml")
    manager = TomlFileManager.__new__(TomlFileManager)
    manager.path = file_path
    manager.document = toml_document()
    manager.document["section"] = toml_table()
    manager.document["section"]["subsection"] = toml_table()

    result = manager._navigate(["section", "subsection"])
    assert result is not None
    assert isinstance(result, Table)


def test_toml_file_manager_navigate_nonexistent_path():
    """
    Scenario:
        Navigate to a non-existent path without creating.

    Expected:
        Returns None.
    """
    file_path = Path("dummy.toml")
    manager = TomlFileManager.__new__(TomlFileManager)
    manager.path = file_path
    manager.document = toml_document()

    result = manager._navigate(["section", "subsection"])
    assert result is None


def test_toml_file_manager_navigate_create_path():
    """
    Scenario:
        Navigate to a non-existent path with create=True.

    Expected:
        Creates intermediate tables and returns the final table.
    """
    file_path = Path("dummy.toml")
    manager = TomlFileManager.__new__(TomlFileManager)
    manager.path = file_path
    manager.document = toml_document()

    result = manager._navigate(["section", "subsection"], create=True)
    assert result is not None
    assert isinstance(result, Table)
    assert "section" in manager.document
    assert "subsection" in manager.document["section"]
