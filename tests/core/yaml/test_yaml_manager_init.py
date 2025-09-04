"""
TidyCode YAML Manager Initialization Tests
"""

from unittest import mock

import pytest

from tidycode.core.yaml.manager import YamlFileManager


def test_yaml_file_manager_init_file_not_found():
    """
    Scenario:
        Initialize YamlFileManager with a non-existent file.

    Expected:
        FileNotFoundError is raised.
    """
    with pytest.raises(FileNotFoundError):
        YamlFileManager("non_existent_file.yaml")


def test_yaml_file_manager_init_generic_exception(tmp_path):
    """
    Scenario:
        Mock the load_yaml_file function to raise a generic exception.

    Expected:
        Exception is raised with the mocked error message.
    """
    file_path = tmp_path / "test.yaml"
    file_path.write_text("key: value")

    with mock.patch(
        "tidycode.core.yaml.manager.load_yaml_file", side_effect=Exception("Boom")
    ):
        with pytest.raises(Exception) as exc_info:
            YamlFileManager(file_path)
        assert "Boom" in str(exc_info.value)
