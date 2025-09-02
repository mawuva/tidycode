"""
TidyCode TOML Manager Initialization Tests
"""

from unittest import mock

import pytest

from tidycode.core.toml.manager import TomlFileManager


def test_toml_file_manager_init_file_not_found():
    """
    Scenario:
        Initialize TomlFileManager with a non-existent file.

    Expected:
        FileNotFoundError is raised.
    """
    with pytest.raises(FileNotFoundError):
        TomlFileManager("non_existent_file.toml")


def test_toml_file_manager_init_generic_exception(tmp_path):
    """
    Scenario:
        Mock the load_toml_file function to raise a generic exception.

    Expected:
        Exception is raised with the mocked error message.
    """
    file_path = tmp_path / "test.toml"
    file_path.write_text("key = 'value'")

    with mock.patch(
        "tidycode.core.toml.manager.load_toml_file", side_effect=Exception("Boom")
    ):
        with pytest.raises(Exception) as exc_info:
            TomlFileManager(file_path)
        assert "Boom" in str(exc_info.value)
