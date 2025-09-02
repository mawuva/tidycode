"""
TidyCode TOML Behavior Tests
"""

from tomlkit import document as toml_document

from tidycode.core.toml import (
    load_toml_file,
    merge_toml,
    save_toml_file,
    update_toml_file,
)

# ---------------------------
# Behaviour tests
# ---------------------------


def test_behavior_save_and_load(tmp_path):
    """
    Scenario:
        Save a TOML file with initial data and then load it back.

    Expected:
        Loaded data matches exactly the original data.
    """
    file_path = tmp_path / "behavior1.toml"
    data = {"a": 1, "nested": {"x": 10, "y": 20}}

    # Save
    save_toml_file(file_path, data)

    # Load
    loaded = load_toml_file(file_path)

    assert loaded["a"] == 1
    assert loaded["nested"]["x"] == 10
    assert loaded["nested"]["y"] == 20
    # Check double newline at end
    text = file_path.read_text(encoding="utf-8")
    assert text.endswith("\n\n")


def test_behavior_merge_toml(tmp_path):
    """
    Scenario:
        Merge new data into an existing TOML document.

    Expected:
        Original keys are preserved or overwritten based on 'overwrite'.
        Nested keys are correctly merged.
    """
    base = toml_document()
    base["a"] = 1
    base["nested"] = {"x": 10}

    new_data = {"a": 2, "nested": {"y": 20}, "b": 3}
    merged = merge_toml(base, new_data, overwrite=True)

    assert merged["a"] == 2  # overwritten
    assert merged["b"] == 3  # new key added
    assert merged["nested"]["x"] == 10
    assert merged["nested"]["y"] == 20


def test_behavior_update_toml_file(tmp_path):
    """
    Scenario:
        Update a TOML file multiple times using update_toml_file.

    Expected:
        All merges are applied correctly.
        Existing values are overwritten if 'overwrite=True'.
        Nested structures are preserved and extended.
    """
    file_path = tmp_path / "behavior2.toml"
    initial_data = {"a": 1, "nested": {"x": 10}}
    save_toml_file(file_path, initial_data)

    # First update
    update_toml_file(file_path, {"a": 2, "nested": {"y": 20}})
    loaded1 = load_toml_file(file_path)
    assert loaded1["a"] == 2
    assert loaded1["nested"]["x"] == 10
    assert loaded1["nested"]["y"] == 20

    # Second update with overwrite=False
    update_toml_file(file_path, {"a": 5, "nested": {"x": 99, "z": 30}}, overwrite=False)
    loaded2 = load_toml_file(file_path)
    assert loaded2["a"] == 2  # preserved
    assert loaded2["nested"]["x"] == 10  # preserved
    assert loaded2["nested"]["y"] == 20
    assert loaded2["nested"]["z"] == 30  # new key added


def test_behavior_merge_and_save(tmp_path):
    """
    Scenario:
        Merge data into a loaded TOML document, then save manually.

    Expected:
        File content reflects the merged changes.
    """
    file_path = tmp_path / "behavior3.toml"
    save_toml_file(file_path, {"foo": "bar", "nested": {"key1": 1}})

    # Load and merge manually
    doc = load_toml_file(file_path)
    merge_toml(doc, {"foo": "baz", "nested": {"key2": 2}})
    save_toml_file(file_path, doc)

    # Verify file content
    loaded = load_toml_file(file_path)
    assert loaded["foo"] == "baz"
    assert loaded["nested"]["key1"] == 1
    assert loaded["nested"]["key2"] == 2
