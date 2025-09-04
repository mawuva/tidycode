"""
TidyCode YAML Manager Integration Tests
"""

from tidycode.core.yaml import save_yaml_file
from tidycode.core.yaml.manager import YamlFileManager


def test_complex_yaml_operations(tmp_path):
    """
    Scenario:
        Perform complex operations: set keys, delete items, and save.

    Expected:
        All operations work correctly and changes are persisted.
    """
    file_path = tmp_path / "complex.yaml"
    save_yaml_file(file_path, {})

    manager = YamlFileManager(file_path)

    # Create nested structure
    manager.set_key("value1", "section1.key1")
    manager.set_key("value2", "section1.subsection.key2")
    manager.set_key("value3", "section1.subsection.key3")

    # Verify structure
    assert manager.has_key("section1.key1")
    assert manager.has_key("section1.subsection.key2")
    assert manager.has_key("section1.subsection.key3")

    # Delete some items
    manager.delete_key("section1.subsection.key2")

    # Verify deletions
    assert not manager.has_key("section1.subsection.key2")
    assert manager.has_key("section1.subsection.key3")

    # Save and reload
    manager.save()
    new_manager = YamlFileManager(file_path)

    assert new_manager.has_key("section1.key1")
    assert not new_manager.has_key("section1.subsection.key2")
    assert new_manager.get_key("section1.key1") == "value1"


def test_dot_notation_vs_path_key_name_equivalence(tmp_path):
    """
    Scenario:
        Test that dot notation and path/key_name parameters produce equivalent results.

    Expected:
        Both methods produce the same results.
    """
    file_path = tmp_path / "equivalence.yaml"
    save_yaml_file(file_path, {"section": {"subsection": {"key": "value"}}})

    manager = YamlFileManager(file_path)

    # Test get operations
    dot_result = manager.get_key("section.subsection.key")
    path_result = manager.get_key(path=["section", "subsection"], key_name="key")
    assert dot_result == path_result

    # Test has operations
    dot_has = manager.has_key("section.subsection.key")
    path_has = manager.has_key(path=["section", "subsection"], key_name="key")
    assert dot_has == path_has

    # Test set operations
    manager.set_key("new_value", "section.subsection.new_key")
    dot_get = manager.get_key("section.subsection.new_key")
    path_get = manager.get_key(path=["section", "subsection"], key_name="new_key")
    assert dot_get == path_get


def test_list_operations(tmp_path):
    """
    Scenario:
        Test operations on YAML lists.

    Expected:
        List operations work correctly.
    """
    file_path = tmp_path / "lists.yaml"
    save_yaml_file(file_path, {
        "items": ["item1", "item2", "item3"],
        "nested": {
            "list": [{"name": "obj1"}, {"name": "obj2"}]
        }
    })

    manager = YamlFileManager(file_path)

    # Test getting list elements
    assert manager.get_key("items.0") == "item1"
    assert manager.get_key("items.2") == "item3"
    assert manager.get_key("nested.list.0.name") == "obj1"

    # Test setting list elements
    manager.set_key("new_item", "items.1")
    assert manager.get_key("items.1") == "new_item"

    # Test extending list
    manager.set_key("item4", "items.3")
    assert manager.get_key("items.3") == "item4"
    assert len(manager.document["items"]) == 4

    # Test deleting list elements
    manager.delete_key("items.0")
    assert manager.get_key("items.0") == "new_item"
    assert len(manager.document["items"]) == 3


def test_mixed_data_types(tmp_path):
    """
    Scenario:
        Test operations with mixed data types.

    Expected:
        All data types are handled correctly.
    """
    file_path = tmp_path / "mixed.yaml"
    save_yaml_file(file_path, {
        "string": "hello",
        "number": 42,
        "float": 3.14,
        "boolean": True,
        "null_value": None,
        "list": [1, 2, 3],
        "dict": {"nested": "value"}
    })

    manager = YamlFileManager(file_path)

    # Test getting different types
    assert manager.get_key("string") == "hello"
    assert manager.get_key("number") == 42
    assert manager.get_key("float") == 3.14
    assert manager.get_key("boolean") is True
    assert manager.get_key("null_value") is None
    assert manager.get_key("list") == [1, 2, 3]
    assert manager.get_key("dict.nested") == "value"

    # Test setting different types
    manager.set_key(False, "boolean")
    manager.set_key(100, "number")
    manager.set_key("world", "string")

    assert manager.get_key("boolean") is False
    assert manager.get_key("number") == 100
    assert manager.get_key("string") == "world"


def test_save_and_reload_persistence(tmp_path):
    """
    Scenario:
        Test that changes are properly persisted to disk.

    Expected:
        Changes are saved and can be reloaded.
    """
    file_path = tmp_path / "persistence.yaml"
    save_yaml_file(file_path, {"initial": "value"})

    # First manager instance
    manager1 = YamlFileManager(file_path)
    manager1.set_key("new_value", "new_key")
    manager1.set_key("nested_value", "nested.key")
    manager1.save()

    # Second manager instance
    manager2 = YamlFileManager(file_path)
    assert manager2.get_key("initial") == "value"
    assert manager2.get_key("new_key") == "new_value"
    assert manager2.get_key("nested.key") == "nested_value"

    # Verify file content
    import yaml
    with open(file_path, 'r') as f:
        content = yaml.safe_load(f)
    
    assert content["initial"] == "value"
    assert content["new_key"] == "new_value"
    assert content["nested"]["key"] == "nested_value"
