"""
TidyCode TOML Manager Integration Tests
"""

from tidycode.core.toml import save_toml_file
from tidycode.core.toml.manager import TomlFileManager


def test_complex_toml_operations(tmp_path):
    """
    Scenario:
        Perform complex operations: create sections, set keys, delete items, and save.

    Expected:
        All operations work correctly and changes are persisted.
    """
    file_path = tmp_path / "complex.toml"
    save_toml_file(file_path, {})

    manager = TomlFileManager(file_path)

    # Create nested structure
    manager.set_section({"key1": "value1"}, "section1")
    manager.set_section({"key2": "value2"}, "section1.subsection")
    manager.set_key("value3", "section1.subsection.key3")

    # Verify structure
    assert manager.has_section("section1")
    assert manager.has_section("section1.subsection")
    assert manager.has_key("section1.subsection.key3")

    # Delete some items
    manager.delete_key("section1.subsection.key2")
    manager.delete_section("section1.subsection")

    # Verify deletions
    assert not manager.has_section("section1.subsection")
    assert not manager.has_key("section1.subsection.key3")

    # Save and reload
    manager.save()
    new_manager = TomlFileManager(file_path)

    assert new_manager.has_section("section1")
    assert not new_manager.has_section("section1.subsection")
    assert new_manager.get_key("section1.key1") == "value1"


def test_dot_notation_vs_path_key_name_equivalence(tmp_path):
    """
    Scenario:
        Test that dot notation and path/key_name parameters produce equivalent results.

    Expected:
        Both methods produce the same results.
    """
    file_path = tmp_path / "equivalence.toml"
    save_toml_file(file_path, {"section": {"subsection": {"key": "value"}}})

    manager = TomlFileManager(file_path)

    # Test get operations
    dot_result = manager.get_key("section.subsection.key")
    path_result = manager.get_key(path=["section", "subsection"], key_name="key")
    assert dot_result == path_result

    # Test has operations
    dot_has = manager.has_key("section.subsection.key")
    path_has = manager.has_key(path=["section", "subsection"], key_name="key")
    assert dot_has == path_has

    # Test section operations
    dot_section = manager.get_section("section.subsection")
    path_section = manager.get_section(path=["section"], key_name="subsection")
    assert dot_section == path_section
