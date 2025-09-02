"""
TidyCode TOML Merger Tests
"""

from pathlib import Path

from tomlkit import document as toml_document
from tomlkit import table as toml_table

from tidycode.core.toml import (
    load_toml_file,
    merge_toml,
    save_toml_file,
    update_toml_file,
)

# ---------------------------
# merge_toml tests
# ---------------------------


def test_merge_toml_overwrite():
    """
    Scenario:
        Merge a dictionary into a TOML document with overwrite=True.

    Expected:
        Existing keys are replaced.
        Nested dictionaries are merged.
    """
    base = toml_document()
    base["a"] = 1
    base["nested"] = {"x": 10}

    new_data = {"a": 2, "nested": {"y": 20}}
    merged = merge_toml(base, new_data, overwrite=True)

    assert merged["a"] == 2
    assert merged["nested"]["x"] == 10
    assert merged["nested"]["y"] == 20


def test_merge_toml_no_overwrite():
    """
    Scenario:
        Merge a dictionary into a TOML document with overwrite=False.

    Expected:
        Existing keys are preserved.
        New keys are added.
    """
    base = toml_document()
    base["a"] = 1

    new_data = {"a": 2, "b": 3}
    merged = merge_toml(base, new_data, overwrite=False)

    assert merged["a"] == 1
    assert merged["b"] == 3


# ---------------------------
# update_toml_file tests
# ---------------------------


def test_update_toml_file_creates_merge(tmp_path):
    """
    Scenario:
        Create a TOML file, update it with new data.

    Expected:
        File exists with merged content.
        Existing values are overwritten.
    """
    file_path = tmp_path / "test.toml"
    save_toml_file(file_path, {"a": 1, "nested": {"x": 10}})

    update_toml_file(file_path, {"a": 2, "nested": {"y": 20}})
    loaded = load_toml_file(file_path)

    assert loaded["a"] == 2
    assert loaded["nested"]["x"] == 10
    assert loaded["nested"]["y"] == 20


def test_update_toml_file_no_overwrite(tmp_path):
    """
    Scenario:
        Update a TOML file with overwrite=False.

    Expected:
        Existing values are preserved.
        New keys are added.
    """
    file_path = tmp_path / "test.toml"
    save_toml_file(file_path, {"a": 1})

    update_toml_file(file_path, {"a": 2, "b": 3}, overwrite=False)
    loaded = load_toml_file(file_path)

    assert loaded["a"] == 1
    assert loaded["b"] == 3


# ---------------------------
# Advanced merge_toml tests
# ---------------------------


def test_merge_toml_with_special_characters():
    """
    Scenario:
        Merge a dictionary containing special characters and Unicode into a TOML document.

    Expected:
        Special characters are preserved correctly.
    """
    base = toml_document()
    base["text"] = "hello"
    new_data = {"text": 'Quote "inside"', "unicode": "ñöç"}

    merged = merge_toml(base, new_data, overwrite=True)
    assert merged["text"] == 'Quote "inside"'
    assert merged["unicode"] == "ñöç"


# ---------------------------
# Advanced update_toml_file tests
# ---------------------------


def test_update_toml_file_with_tomldoc(tmp_path):
    """
    Scenario:
        Update a TOML file using a TOMLDocument directly as the base.

    Expected:
        File is updated correctly with merged content.
    """
    file_path = tmp_path / "tomldoc.toml"
    base_doc = toml_document()
    base_doc["a"] = 1
    save_toml_file(file_path, base_doc)

    update_toml_file(file_path, {"a": 2, "b": 3})
    loaded = load_toml_file(file_path)
    assert loaded["a"] == 2
    assert loaded["b"] == 3


def test_update_toml_file_with_table(tmp_path):
    """
    Scenario:
        Update a TOML file using a nested Table as base.

    Expected:
        Nested table values are merged correctly.
    """
    file_path = tmp_path / "nested.toml"
    base_doc = toml_document()
    base_doc["nested"] = toml_table()
    base_doc["nested"]["x"] = 10
    save_toml_file(file_path, base_doc)

    update_toml_file(file_path, {"nested": {"y": 20}})
    loaded = load_toml_file(file_path)
    assert loaded["nested"]["x"] == 10
    assert loaded["nested"]["y"] == 20


def test_update_toml_file_relative_and_absolute_paths(tmp_path):
    """
    Scenario:
        Save and update TOML files using relative and absolute paths.

    Expected:
        Files are correctly merged regardless of path type.
    """
    # Relative path
    rel_path = Path("relative.toml")
    save_toml_file(tmp_path / rel_path, {"x": 1})
    update_toml_file(tmp_path / rel_path, {"y": 2})
    loaded_rel = load_toml_file(tmp_path / rel_path)
    assert loaded_rel["x"] == 1
    assert loaded_rel["y"] == 2

    # Absolute path
    abs_path = tmp_path / "absolute.toml"
    save_toml_file(abs_path, {"a": 10})
    update_toml_file(abs_path, {"b": 20})
    loaded_abs = load_toml_file(abs_path)
    assert loaded_abs["a"] == 10
    assert loaded_abs["b"] == 20


def test_update_toml_file_special_characters(tmp_path):
    """
    Scenario:
        Merge values with special characters and Unicode into a TOML file.

    Expected:
        Special characters and Unicode are preserved correctly in the file.
    """
    file_path = tmp_path / "special.toml"
    save_toml_file(file_path, {"greeting": "Hello"})
    new_data = {"greeting": 'Quote "inside"', "emoji": "😎", "unicode": "ñöç"}

    update_toml_file(file_path, new_data)
    loaded = load_toml_file(file_path)
    assert loaded["greeting"] == 'Quote "inside"'
    assert loaded["emoji"] == "😎"
    assert loaded["unicode"] == "ñöç"
