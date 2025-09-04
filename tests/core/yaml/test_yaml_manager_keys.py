"""
TidyCode YAML Manager Key Operations Tests
"""

from tidycode.core.yaml import save_yaml_file
from tidycode.core.yaml.manager import YamlFileManager


def test_get_key_with_dot_notation(tmp_path):
    """
    Scenario:
        Get a key value using dot notation.

    Expected:
        Returns the correct value.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(file_path, {"section": {"subsection": {"key": "value"}}})

    manager = YamlFileManager(file_path)
    result = manager.get_key("section.subsection.key")
    assert result == "value"


def test_get_key_with_path_key_name(tmp_path):
    """
    Scenario:
        Get a key value using path and key_name parameters.

    Expected:
        Returns the correct value.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(file_path, {"section": {"subsection": {"key": "value"}}})

    manager = YamlFileManager(file_path)
    result = manager.get_key(path=["section", "subsection"], key_name="key")
    assert result == "value"


def test_get_key_nonexistent_default(tmp_path):
    """
    Scenario:
        Get a non-existent key with a default value.

    Expected:
        Returns the default value.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(file_path, {"key": "value"})

    manager = YamlFileManager(file_path)
    result = manager.get_key("nonexistent.key", default="default_value")
    assert result == "default_value"


def test_get_key_from_list(tmp_path):
    """
    Scenario:
        Get a value from a list using index.

    Expected:
        Returns the correct value.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(file_path, {"items": ["item1", "item2", "item3"]})

    manager = YamlFileManager(file_path)
    result = manager.get_key("items.1")
    assert result == "item2"


def test_set_key_with_dot_notation(tmp_path):
    """
    Scenario:
        Set a key value using dot notation.

    Expected:
        Key is created and value is set correctly.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(file_path, {})

    manager = YamlFileManager(file_path)
    manager.set_key("new_value", "section.subsection.key")

    result = manager.get_key("section.subsection.key")
    assert result == "new_value"


def test_set_key_with_path_key_name(tmp_path):
    """
    Scenario:
        Set a key value using path and key_name parameters.

    Expected:
        Key is created and value is set correctly.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(file_path, {})

    manager = YamlFileManager(file_path)
    manager.set_key("new_value", path=["section", "subsection"], key_name="key")

    result = manager.get_key("section.subsection.key")
    assert result == "new_value"


def test_set_key_overwrite_existing(tmp_path):
    """
    Scenario:
        Set a key value with overwrite=True for existing key.

    Expected:
        Existing value is overwritten.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(file_path, {"key": "old_value"})

    manager = YamlFileManager(file_path)
    manager.set_key("new_value", "key", overwrite=True)

    result = manager.get_key("key")
    assert result == "new_value"


def test_set_key_no_overwrite_existing(tmp_path):
    """
    Scenario:
        Set a key value with overwrite=False for existing key.

    Expected:
        Existing value is preserved.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(file_path, {"key": "old_value"})

    manager = YamlFileManager(file_path)
    manager.set_key("new_value", "key", overwrite=False)

    result = manager.get_key("key")
    assert result == "old_value"


def test_set_key_in_list(tmp_path):
    """
    Scenario:
        Set a value in a list using index.

    Expected:
        Value is set at the correct index.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(file_path, {"items": ["item1", "item2"]})

    manager = YamlFileManager(file_path)
    manager.set_key("new_item", "items.1")

    result = manager.get_key("items.1")
    assert result == "new_item"


def test_set_key_extend_list(tmp_path):
    """
    Scenario:
        Set a value at an index beyond the current list length.

    Expected:
        List is extended and value is set at the correct index.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(file_path, {"items": ["item1"]})

    manager = YamlFileManager(file_path)
    manager.set_key("item3", "items.2")

    result = manager.get_key("items.2")
    assert result == "item3"
    assert len(manager.document["items"]) == 3


def test_delete_key_existing(tmp_path):
    """
    Scenario:
        Delete an existing key.

    Expected:
        Key is deleted and returns True.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(file_path, {"key": "value"})

    manager = YamlFileManager(file_path)
    result = manager.delete_key("key")

    assert result is True
    assert not manager.has_key("key")


def test_delete_key_nonexistent(tmp_path):
    """
    Scenario:
        Delete a non-existent key.

    Expected:
        Returns False and no changes are made.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(file_path, {"key": "value"})

    manager = YamlFileManager(file_path)
    result = manager.delete_key("nonexistent.key")

    assert result is False
    assert manager.has_key("key")


def test_delete_key_from_list(tmp_path):
    """
    Scenario:
        Delete an element from a list using index.

    Expected:
        Element is removed and returns True.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(file_path, {"items": ["item1", "item2", "item3"]})

    manager = YamlFileManager(file_path)
    result = manager.delete_key("items.1")

    assert result is True
    assert len(manager.document["items"]) == 2
    assert manager.document["items"] == ["item1", "item3"]


def test_delete_key_from_list_invalid_index(tmp_path):
    """
    Scenario:
        Delete an element from a list using invalid index.

    Expected:
        Returns False and no changes are made.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(file_path, {"items": ["item1", "item2"]})

    manager = YamlFileManager(file_path)
    result = manager.delete_key("items.invalid")

    assert result is False
    assert len(manager.document["items"]) == 2


def test_has_key_existing(tmp_path):
    """
    Scenario:
        Check if an existing key exists.

    Expected:
        Returns True.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(file_path, {"key": "value"})

    manager = YamlFileManager(file_path)
    result = manager.has_key("key")

    assert result is True


def test_has_key_nonexistent(tmp_path):
    """
    Scenario:
        Check if a non-existent key exists.

    Expected:
        Returns False.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(file_path, {"key": "value"})

    manager = YamlFileManager(file_path)
    result = manager.has_key("nonexistent.key")

    assert result is False


def test_has_key_in_list_valid_index(tmp_path):
    """
    Scenario:
        Check if a list element exists at valid index.

    Expected:
        Returns True.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(file_path, {"items": ["item1", "item2"]})

    manager = YamlFileManager(file_path)
    result = manager.has_key("items.1")

    assert result is True


def test_has_key_in_list_invalid_index(tmp_path):
    """
    Scenario:
        Check if a list element exists at invalid index.

    Expected:
        Returns False.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(file_path, {"items": ["item1", "item2"]})

    manager = YamlFileManager(file_path)
    result = manager.has_key("items.5")

    assert result is False


def test_has_key_in_list_non_numeric_index(tmp_path):
    """
    Scenario:
        Check if a list element exists with non-numeric index.

    Expected:
        Returns False.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(file_path, {"items": ["item1", "item2"]})

    manager = YamlFileManager(file_path)
    result = manager.has_key("items.invalid")

    assert result is False
