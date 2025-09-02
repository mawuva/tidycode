"""
TidyCode TOML Manager Utility and Persistence Tests
"""

from unittest import mock

import pytest

from tidycode.core.toml import load_toml_file, save_toml_file
from tidycode.core.toml.manager import TomlFileManager


def test_keys_root_level(tmp_path):
    """
    Scenario:
        List keys at the root level.

    Expected:
        Returns list of root-level keys.
    """
    file_path = tmp_path / "test.toml"
    save_toml_file(file_path, {"key1": "value1", "key2": "value2", "section": {}})

    manager = TomlFileManager(file_path)
    result = manager.keys()

    assert "key1" in result
    assert "key2" in result
    assert "section" in result
    assert len(result) == 3


def test_keys_with_dot_prefix(tmp_path):
    """
    Scenario:
        List keys with a dot prefix.

    Expected:
        Returns list of keys at the specified section.
    """
    file_path = tmp_path / "test.toml"
    save_toml_file(file_path, {"section": {"key1": "value1", "key2": "value2"}})

    manager = TomlFileManager(file_path)
    result = manager.keys("section")

    assert "key1" in result
    assert "key2" in result
    assert len(result) == 2


def test_keys_with_path(tmp_path):
    """
    Scenario:
        List keys with a path parameter.

    Expected:
        Returns list of keys at the specified path.
    """
    file_path = tmp_path / "test.toml"
    save_toml_file(
        file_path, {"section": {"subsection": {"key1": "value1", "key2": "value2"}}}
    )

    manager = TomlFileManager(file_path)
    result = manager.keys(path=["section", "subsection"])

    assert "key1" in result
    assert "key2" in result
    assert len(result) == 2


def test_keys_nonexistent_path(tmp_path):
    """
    Scenario:
        List keys at a non-existent path.

    Expected:
        Returns empty list.
    """
    file_path = tmp_path / "test.toml"
    save_toml_file(file_path, {"key": "value"})

    manager = TomlFileManager(file_path)
    result = manager.keys("nonexistent")

    assert result == []


def test_save_changes(tmp_path):
    """
    Scenario:
        Make changes to the TOML document and save them.

    Expected:
        Changes are persisted to the file.
    """
    file_path = tmp_path / "test.toml"
    save_toml_file(file_path, {"key": "old_value"})

    manager = TomlFileManager(file_path)
    manager.set_key("new_value", "key")
    manager.save()

    # Reload the file to verify changes
    loaded = load_toml_file(file_path)
    assert loaded["key"] == "new_value"


def test_save_with_new_sections(tmp_path):
    """
    Scenario:
        Create new sections and save them.

    Expected:
        New sections are persisted to the file.
    """
    file_path = tmp_path / "test.toml"
    save_toml_file(file_path, {})

    manager = TomlFileManager(file_path)
    manager.set_section({"key1": "value1", "key2": "value2"}, "new_section")
    manager.save()

    # Reload the file to verify changes
    loaded = load_toml_file(file_path)
    assert "new_section" in loaded
    assert loaded["new_section"]["key1"] == "value1"
    assert loaded["new_section"]["key2"] == "value2"


def test_save_permission_error(tmp_path):
    """
    Scenario:
        Mock save_toml_file to raise PermissionError.

    Expected:
        PermissionError is raised.
    """
    file_path = tmp_path / "test.toml"
    save_toml_file(file_path, {"key": "value"})

    manager = TomlFileManager(file_path)

    with mock.patch(
        "tidycode.core.toml.manager.save_toml_file", side_effect=PermissionError
    ):
        with pytest.raises(PermissionError):
            manager.save()
