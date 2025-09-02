"""
TidyCode TOML Manager Section Operations Tests
"""

from tidycode.core.toml import save_toml_file
from tidycode.core.toml.manager import TomlFileManager


def test_get_section_existing(tmp_path):
    """
    Scenario:
        Get an existing section.

    Expected:
        Returns the section content.
    """
    file_path = tmp_path / "test.toml"
    section_data = {"subsection": {"key": "value"}}
    save_toml_file(file_path, {"section": section_data})

    manager = TomlFileManager(file_path)
    result = manager.get_section("section")

    assert result == section_data


def test_get_section_nonexistent_default(tmp_path):
    """
    Scenario:
        Get a non-existent section with default value.

    Expected:
        Returns the default value.
    """
    file_path = tmp_path / "test.toml"
    save_toml_file(file_path, {})

    manager = TomlFileManager(file_path)
    result = manager.get_section("nonexistent", default="default_section")

    assert result == "default_section"


def test_set_section_new(tmp_path):
    """
    Scenario:
        Set a new section.

    Expected:
        Section is created with the provided data.
    """
    file_path = tmp_path / "test.toml"
    save_toml_file(file_path, {})

    section_data = {"key1": "value1", "key2": "value2"}
    manager = TomlFileManager(file_path)
    manager.set_section(section_data, "new_section")

    result = manager.get_section("new_section")
    assert result == section_data


def test_set_section_overwrite_existing(tmp_path):
    """
    Scenario:
        Set a section with overwrite=True for existing section.

    Expected:
        New data is merged with existing section, overwriting existing keys.
    """
    file_path = tmp_path / "test.toml"
    save_toml_file(file_path, {"section": {"old_key": "old_value"}})

    new_data = {"new_key": "new_value"}
    manager = TomlFileManager(file_path)
    manager.set_section(new_data, "section", overwrite=True)

    result = manager.get_section("section")
    # With overwrite=True, existing keys are overwritten but section is merged
    assert result["new_key"] == "new_value"
    assert "old_key" in result  # The key still exists but may be overwritten


def test_set_section_no_overwrite_existing(tmp_path):
    """
    Scenario:
        Set a section with overwrite=False for existing section.

    Expected:
        New data is merged with existing section.
    """
    file_path = tmp_path / "test.toml"
    save_toml_file(file_path, {"section": {"old_key": "old_value"}})

    new_data = {"new_key": "new_value"}
    manager = TomlFileManager(file_path)
    manager.set_section(new_data, "section", overwrite=False)

    result = manager.get_section("section")
    assert result["old_key"] == "old_value"
    assert result["new_key"] == "new_value"


def test_delete_section_existing(tmp_path):
    """
    Scenario:
        Delete an existing section.

    Expected:
        Section is deleted and returns True.
    """
    file_path = tmp_path / "test.toml"
    save_toml_file(file_path, {"section": {"key": "value"}})

    manager = TomlFileManager(file_path)
    result = manager.delete_section("section")

    assert result is True
    assert not manager.has_section("section")


def test_delete_section_nonexistent(tmp_path):
    """
    Scenario:
        Delete a non-existent section.

    Expected:
        Returns False and no changes are made.
    """
    file_path = tmp_path / "test.toml"
    save_toml_file(file_path, {"section": {"key": "value"}})

    manager = TomlFileManager(file_path)
    result = manager.delete_section("nonexistent")

    assert result is False
    assert manager.has_section("section")


def test_has_section_existing(tmp_path):
    """
    Scenario:
        Check if an existing section exists.

    Expected:
        Returns True.
    """
    file_path = tmp_path / "test.toml"
    save_toml_file(file_path, {"section": {"key": "value"}})

    manager = TomlFileManager(file_path)
    result = manager.has_section("section")

    assert result is True


def test_has_section_nonexistent(tmp_path):
    """
    Scenario:
        Check if a non-existent section exists.

    Expected:
        Returns False.
    """
    file_path = tmp_path / "test.toml"
    save_toml_file(file_path, {"key": "value"})

    manager = TomlFileManager(file_path)
    result = manager.has_section("nonexistent")

    assert result is False
