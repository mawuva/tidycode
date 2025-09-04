"""
TidyCode YAML Loader Tests
"""

from pathlib import Path
from unittest import mock

import pytest

from tidycode.core.yaml import load_yaml_file, save_yaml_file


# ---------------------------
# Unit tests
# ---------------------------


def test_load_yaml_file_file_not_found():
    """
    Scenario:
        Attempt to load a YAML file that does not exist.

    Expected:
        FileNotFoundError is raised.
    """
    with pytest.raises(FileNotFoundError):
        load_yaml_file("non_existent_file.yaml")


def test_load_yaml_file_generic_exception(tmp_path):
    """
    Scenario:
        Mock the file open operation to raise a generic exception.

    Expected:
        Exception is raised with the mocked error message.
    """
    file_path = tmp_path / "test.yaml"
    file_path.write_text("key: value")

    with mock.patch("pathlib.Path.open", side_effect=Exception("Boom")):
        with pytest.raises(Exception) as exc_info:
            load_yaml_file(file_path)
        assert "Boom" in str(exc_info.value)


def test_save_yaml_file_permission_error(tmp_path):
    """
    Scenario:
        Mock mkdir to raise PermissionError when creating parent directories.

    Expected:
        PermissionError is raised.
    """
    file_path = tmp_path / "subdir" / "test.yaml"
    data = {"key": "value"}

    with mock.patch("pathlib.Path.mkdir", side_effect=PermissionError):
        with pytest.raises(PermissionError):
            save_yaml_file(file_path, data)


def test_save_yaml_file_generic_exception(tmp_path):
    """
    Scenario:
        Mock file open to raise a generic exception during writing.

    Expected:
        Exception is raised with the mocked error message.
    """
    file_path = tmp_path / "test.yaml"
    data = {"key": "value"}

    with mock.patch("pathlib.Path.open", side_effect=Exception("Boom")):
        with pytest.raises(Exception) as exc_info:
            save_yaml_file(file_path, data)
        assert "Boom" in str(exc_info.value)


# ---------------------------
# Integration tests
# ---------------------------


def test_save_and_load_yaml_file(tmp_path):
    """
    Scenario:
        Save a dictionary to a YAML file and then load it back.

    Expected:
        The file exists.
        Loaded values match the original data.
    """
    file_path = tmp_path / "test.yaml"
    data = {"key1": "value1", "key2": 123, "nested": {"a": True}}

    save_yaml_file(file_path, data)
    assert file_path.exists()

    loaded_doc = load_yaml_file(file_path)
    assert loaded_doc["key1"] == "value1"
    assert loaded_doc["key2"] == 123
    assert loaded_doc["nested"]["a"] is True


def test_save_dict_and_load(tmp_path):
    """
    Scenario:
        Save a simple dictionary to a YAML file and load it.

    Expected:
        Loaded value matches the original dictionary.
    """
    file_path = tmp_path / "dict_test.yaml"
    data = {"foo": "bar"}

    save_yaml_file(file_path, data)
    loaded_doc = load_yaml_file(file_path)
    assert loaded_doc["foo"] == "bar"


def test_save_and_load_relative_and_absolute_paths(tmp_path):
    """
    Scenario:
        Save files using relative and absolute paths.

    Expected:
        Files are correctly created and loaded.
    """
    # Relative path
    rel_path = Path("relative.yaml")
    save_yaml_file(tmp_path / rel_path, {"x": 1})
    loaded_rel = load_yaml_file(tmp_path / rel_path)
    assert loaded_rel["x"] == 1

    # Absolute path
    abs_path = tmp_path / "absolute.yaml"
    save_yaml_file(abs_path, {"y": 2})
    loaded_abs = load_yaml_file(abs_path)
    assert loaded_abs["y"] == 2


def test_save_and_load_special_characters(tmp_path):
    """
    Scenario:
        Save values with special characters to a YAML file.

    Expected:
        Values are correctly preserved when loading.
    """
    file_path = tmp_path / "special_chars.yaml"
    data = {"quote": 'This "is" tricky', "newline": "Line1\nLine2", "unicode": "ñöç"}

    save_yaml_file(file_path, data)
    loaded = load_yaml_file(file_path)

    assert loaded["quote"] == 'This "is" tricky'
    assert loaded["newline"] == "Line1\nLine2"
    assert loaded["unicode"] == "ñöç"


def test_save_and_load_complex_nested_structure(tmp_path):
    """
    Scenario:
        Save a complex nested structure with lists and dictionaries.

    Expected:
        Complex structure is correctly preserved when loading.
    """
    file_path = tmp_path / "complex.yaml"
    data = {
        "users": [
            {"name": "Alice", "age": 30, "hobbies": ["reading", "swimming"]},
            {"name": "Bob", "age": 25, "hobbies": ["gaming", "cooking"]}
        ],
        "config": {
            "database": {
                "host": "localhost",
                "port": 5432,
                "ssl": True
            },
            "features": ["auth", "logging", "metrics"]
        }
    }

    save_yaml_file(file_path, data)
    loaded = load_yaml_file(file_path)

    assert len(loaded["users"]) == 2
    assert loaded["users"][0]["name"] == "Alice"
    assert loaded["users"][0]["hobbies"] == ["reading", "swimming"]
    assert loaded["config"]["database"]["port"] == 5432
    assert loaded["config"]["features"] == ["auth", "logging", "metrics"]


def test_save_and_load_empty_structures(tmp_path):
    """
    Scenario:
        Save empty dictionaries and lists to a YAML file.

    Expected:
        Empty structures are correctly preserved when loading.
    """
    file_path = tmp_path / "empty.yaml"
    data = {"empty_dict": {}, "empty_list": [], "null_value": None}

    save_yaml_file(file_path, data)
    loaded = load_yaml_file(file_path)

    assert loaded["empty_dict"] == {}
    assert loaded["empty_list"] == []
    assert loaded["null_value"] is None
