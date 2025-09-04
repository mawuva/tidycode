"""
TidyCode YAML Manager Internal Methods Tests
"""

from pathlib import Path

import pytest

from tidycode.core.yaml.manager import YamlFileManager


def test_yaml_file_manager_resolve_dot_key():
    """
    Scenario:
        Use _resolve method with dot_key parameter.

    Expected:
        Returns correct path and key_name tuple.
    """
    file_path = Path("dummy.yaml")
    manager = YamlFileManager.__new__(YamlFileManager)
    manager.path = file_path
    manager.document = {}

    path, key_name = manager._resolve("section.subsection.key", None, None)
    assert path == ["section", "subsection"]
    assert key_name == "key"


def test_yaml_file_manager_resolve_path_key_name():
    """
    Scenario:
        Use _resolve method with path and key_name parameters.

    Expected:
        Returns correct path and key_name tuple.
    """
    file_path = Path("dummy.yaml")
    manager = YamlFileManager.__new__(YamlFileManager)
    manager.path = file_path
    manager.document = {}

    path, key_name = manager._resolve(None, ["section", "subsection"], "key")
    assert path == ["section", "subsection"]
    assert key_name == "key"


def test_yaml_file_manager_resolve_no_parameters():
    """
    Scenario:
        Use _resolve method without any parameters.

    Expected:
        ValueError is raised.
    """
    file_path = Path("dummy.yaml")
    manager = YamlFileManager.__new__(YamlFileManager)
    manager.path = file_path
    manager.document = {}

    with pytest.raises(
        ValueError, match="You must provide either dot_key or \\(path \\+ key_name\\)"
    ):
        manager._resolve(None, None, None)


def test_yaml_file_manager_navigate_existing_path():
    """
    Scenario:
        Navigate to an existing path in the YAML structure.

    Expected:
        Returns the correct dict at the specified path.
    """
    file_path = Path("dummy.yaml")
    manager = YamlFileManager.__new__(YamlFileManager)
    manager.path = file_path
    manager.document = {
        "section": {
            "subsection": {"key": "value"}
        }
    }

    result = manager._navigate(["section", "subsection"])
    assert result is not None
    assert isinstance(result, dict)
    assert result["key"] == "value"


def test_yaml_file_manager_navigate_nonexistent_path():
    """
    Scenario:
        Navigate to a non-existent path without creating.

    Expected:
        Returns None.
    """
    file_path = Path("dummy.yaml")
    manager = YamlFileManager.__new__(YamlFileManager)
    manager.path = file_path
    manager.document = {}

    result = manager._navigate(["section", "subsection"])
    assert result is None


def test_yaml_file_manager_navigate_create_path():
    """
    Scenario:
        Navigate to a non-existent path with create=True.

    Expected:
        Creates intermediate dicts and returns the final dict.
    """
    file_path = Path("dummy.yaml")
    manager = YamlFileManager.__new__(YamlFileManager)
    manager.path = file_path
    manager.document = {}

    result = manager._navigate(["section", "subsection"], create=True)
    assert result is not None
    assert isinstance(result, dict)
    assert "section" in manager.document
    assert "subsection" in manager.document["section"]


def test_yaml_file_manager_navigate_list_with_index():
    """
    Scenario:
        Navigate to a list element using index.

    Expected:
        Returns the correct list element.
    """
    file_path = Path("dummy.yaml")
    manager = YamlFileManager.__new__(YamlFileManager)
    manager.path = file_path
    manager.document = {
        "items": [
            {"name": "item1"},
            {"name": "item2"}
        ]
    }

    result = manager._navigate(["items", "0"])
    assert result is not None
    assert isinstance(result, dict)
    assert result["name"] == "item1"


def test_yaml_file_manager_navigate_list_invalid_index():
    """
    Scenario:
        Navigate to a list with invalid index (non-numeric).

    Expected:
        Returns None.
    """
    file_path = Path("dummy.yaml")
    manager = YamlFileManager.__new__(YamlFileManager)
    manager.path = file_path
    manager.document = {
        "items": [{"name": "item1"}]
    }

    result = manager._navigate(["items", "invalid"])
    assert result is None


def test_yaml_file_manager_navigate_list_out_of_bounds():
    """
    Scenario:
        Navigate to a list element with out-of-bounds index.

    Expected:
        Returns None when create=False.
    """
    file_path = Path("dummy.yaml")
    manager = YamlFileManager.__new__(YamlFileManager)
    manager.path = file_path
    manager.document = {
        "items": [{"name": "item1"}]
    }

    result = manager._navigate(["items", "5"])
    assert result is None


def test_yaml_file_manager_navigate_list_out_of_bounds_create():
    """
    Scenario:
        Navigate to a list element with out-of-bounds index and create=True.

    Expected:
        Extends list and returns the new element.
    """
    file_path = Path("dummy.yaml")
    manager = YamlFileManager.__new__(YamlFileManager)
    manager.path = file_path
    manager.document = {
        "items": [{"name": "item1"}]
    }

    result = manager._navigate(["items", "2"], create=True)
    assert result is not None
    assert isinstance(result, dict)
    assert len(manager.document["items"]) == 3


def test_yaml_file_manager_navigate_scalar_value():
    """
    Scenario:
        Try to navigate into a scalar value.

    Expected:
        Returns None.
    """
    file_path = Path("dummy.yaml")
    manager = YamlFileManager.__new__(YamlFileManager)
    manager.path = file_path
    manager.document = {
        "scalar": "value"
    }

    result = manager._navigate(["scalar", "subkey"])
    assert result is None


def test_yaml_file_manager_resolve_and_navigate():
    """
    Scenario:
        Use _resolve_and_navigate method with dot_key.

    Expected:
        Returns the correct parent node and key name.
    """
    file_path = Path("dummy.yaml")
    manager = YamlFileManager.__new__(YamlFileManager)
    manager.path = file_path
    manager.document = {
        "section": {
            "subsection": {"key": "value"}
        }
    }

    result = manager._resolve_and_navigate("section.subsection.key")
    assert result is not None
    parent, key = result
    assert isinstance(parent, dict)
    assert key == "key"
    assert parent["key"] == "value"


def test_yaml_file_manager_resolve_and_navigate_nonexistent():
    """
    Scenario:
        Use _resolve_and_navigate method with non-existent path.

    Expected:
        Returns None.
    """
    file_path = Path("dummy.yaml")
    manager = YamlFileManager.__new__(YamlFileManager)
    manager.path = file_path
    manager.document = {}

    result = manager._resolve_and_navigate("section.subsection.key")
    assert result is None
