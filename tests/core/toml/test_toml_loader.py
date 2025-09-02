"""
TidyCode TOML Loader Tests
"""

from pathlib import Path
from unittest import mock

import pytest
from tomlkit import document as TOMLDocument
from tomlkit import document as toml_document

from tidycode.core.toml import load_toml_file, save_toml_file

# ---------------------------
# Unit tests
# ---------------------------


def test_load_toml_file_file_not_found():
    """
    Scenario:
        Attempt to load a TOML file that does not exist.

    Expected:
        FileNotFoundError is raised.
    """
    with pytest.raises(FileNotFoundError):
        load_toml_file("non_existent_file.toml")


def test_load_toml_file_generic_exception(tmp_path):
    """
    Scenario:
        Mock the file open operation to raise a generic exception.

    Expected:
        Exception is raised with the mocked error message.
    """
    file_path = tmp_path / "test.toml"
    file_path.write_text("key = 'value'")

    with mock.patch("pathlib.Path.open", side_effect=Exception("Boom")):
        with pytest.raises(Exception) as exc_info:
            load_toml_file(file_path)
        assert "Boom" in str(exc_info.value)


def test_save_toml_file_permission_error(tmp_path):
    """
    Scenario:
        Mock mkdir to raise PermissionError when creating parent directories.

    Expected:
        PermissionError is raised.
    """
    file_path = tmp_path / "subdir" / "test.toml"
    data = {"key": "value"}

    with mock.patch("pathlib.Path.mkdir", side_effect=PermissionError):
        with pytest.raises(PermissionError):
            save_toml_file(file_path, data)


def test_save_toml_file_generic_exception(tmp_path):
    """
    Scenario:
        Mock file open to raise a generic exception during writing.

    Expected:
        Exception is raised with the mocked error message.
    """
    file_path = tmp_path / "test.toml"
    data = {"key": "value"}

    with mock.patch("pathlib.Path.open", side_effect=Exception("Boom")):
        with pytest.raises(Exception) as exc_info:
            save_toml_file(file_path, data)
        assert "Boom" in str(exc_info.value)


# ---------------------------
# Integration tests
# ---------------------------


def test_save_and_load_toml_file(tmp_path):
    """
    Scenario:
        Save a dictionary to a TOML file and then load it back.

    Expected:
        The file exists.
        The file ends with a double newline.
        Loaded values match the original data.
    """
    file_path = tmp_path / "test.toml"
    data = {"key1": "value1", "key2": 123, "nested": {"a": True}}

    save_toml_file(file_path, data)
    assert file_path.exists()

    text = file_path.read_text(encoding="utf-8")
    assert text.endswith("\n\n")

    loaded_doc = load_toml_file(file_path)
    assert loaded_doc["key1"] == "value1"
    assert loaded_doc["key2"] == 123
    assert loaded_doc["nested"]["a"] is True


def test_save_dict_and_load(tmp_path):
    """
    Scenario:
        Save a simple dictionary to a TOML file and load it.

    Expected:
        Loaded value matches the original dictionary.
    """
    file_path = tmp_path / "dict_test.toml"
    data = {"foo": "bar"}

    save_toml_file(file_path, data)
    loaded_doc = load_toml_file(file_path)
    assert loaded_doc["foo"] == "bar"


def test_save_toml_document_directly(tmp_path):
    """
    Scenario:
        Save a TOMLDocument object directly to a file.

    Expected:
        File is created and can be loaded with correct values.
    """
    file_path = tmp_path / "tomldoc.toml"
    doc: TOMLDocument = toml_document()
    doc["a"] = 123
    doc["b"] = "hello"

    save_toml_file(file_path, doc)
    loaded = load_toml_file(file_path)
    assert loaded["a"] == 123
    assert loaded["b"] == "hello"


def test_save_and_load_relative_and_absolute_paths(tmp_path):
    """
    Scenario:
        Save files using relative and absolute paths.

    Expected:
        Files are correctly created and loaded.
    """
    # Relative path
    rel_path = Path("relative.toml")
    save_toml_file(tmp_path / rel_path, {"x": 1})
    loaded_rel = load_toml_file(tmp_path / rel_path)
    assert loaded_rel["x"] == 1

    # Absolute path
    abs_path = tmp_path / "absolute.toml"
    save_toml_file(abs_path, {"y": 2})
    loaded_abs = load_toml_file(abs_path)
    assert loaded_abs["y"] == 2


def test_save_and_load_special_characters(tmp_path):
    """
    Scenario:
        Save values with special characters to a TOML file.

    Expected:
        Values are correctly preserved when loading.
    """
    file_path = tmp_path / "special_chars.toml"
    data = {"quote": 'This "is" tricky', "newline": "Line1\nLine2", "unicode": "ñöç"}

    save_toml_file(file_path, data)
    loaded = load_toml_file(file_path)

    assert loaded["quote"] == 'This "is" tricky'
    assert loaded["newline"] == "Line1\nLine2"
    assert loaded["unicode"] == "ñöç"
