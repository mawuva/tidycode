"""
TidyCode Core PyProject Plugins Base Tests
"""

import pytest

from tidycode.plugins.config import ConfigProvider


class TestConfigProvider(ConfigProvider):
    """Test implementation of ConfigProvider for testing."""

    def __init__(self, name: str, data: dict):
        self.name = name
        self.data = data

    def get_name(self) -> str:
        return self.name

    def get_data(self) -> dict:
        return self.data


def test_config_provider_has_abstract_methods():
    """
    Scenario:
        Test that ConfigProvider has the required abstract methods.

    Expected:
        ConfigProvider has get_name and get_data as abstract methods.
    """
    # Check that methods exist
    assert hasattr(ConfigProvider, "get_name")
    assert hasattr(ConfigProvider, "get_data")

    # Check that methods are abstract
    assert ConfigProvider.get_name.__isabstractmethod__
    assert ConfigProvider.get_data.__isabstractmethod__


def test_config_provider_cannot_be_instantiated():
    """
    Scenario:
        Try to instantiate ConfigProvider directly.

    Expected:
        TypeError is raised because it's an abstract class.
    """
    with pytest.raises(TypeError):
        ConfigProvider()


def test_config_provider_concrete_implementation():
    """
    Scenario:
        Test a concrete implementation of ConfigProvider.

    Expected:
        Concrete implementation works correctly.
    """
    test_data = {"key1": "value1", "key2": "value2"}
    provider = TestConfigProvider("test-tool", test_data)

    # Test get_name method
    assert provider.get_name() == "test-tool"

    # Test get_data method
    assert provider.get_data() == test_data


def test_config_provider_multiple_instances():
    """
    Scenario:
        Test multiple instances of ConfigProvider implementations.

    Expected:
        Each instance maintains its own data.
    """
    provider1 = TestConfigProvider("tool1", {"key1": "value1"})
    provider2 = TestConfigProvider("tool2", {"key2": "value2"})

    # Verify each instance has its own data
    assert provider1.get_name() == "tool1"
    assert provider1.get_data() == {"key1": "value1"}

    assert provider2.get_name() == "tool2"
    assert provider2.get_data() == {"key2": "value2"}


def test_config_provider_complex_data():
    """
    Scenario:
        Test ConfigProvider with complex nested data.

    Expected:
        Complex data is handled correctly.
    """
    complex_data = {
        "dependencies": {"requests": "^2.28.0", "pytest": "^7.0.0"},
        "dev-dependencies": {"black": "^22.0.0", "ruff": "^0.1.0"},
        "scripts": {"test": "pytest", "format": "black .", "lint": "ruff check ."},
    }

    provider = TestConfigProvider("complex-tool", complex_data)

    # Test get_name method
    assert provider.get_name() == "complex-tool"

    # Test get_data method returns the exact data
    returned_data = provider.get_data()
    assert returned_data == complex_data

    # Test that returned data is a reference (this is the actual behavior)
    assert returned_data is complex_data


def test_config_provider_empty_data():
    """
    Scenario:
        Test ConfigProvider with empty data.

    Expected:
        Empty data is handled correctly.
    """
    provider = TestConfigProvider("empty-tool", {})

    # Test get_name method
    assert provider.get_name() == "empty-tool"

    # Test get_data method returns empty dict
    assert provider.get_data() == {}


def test_config_provider_special_characters_in_name():
    """
    Scenario:
        Test ConfigProvider with special characters in name.

    Expected:
        Special characters are handled correctly.
    """
    special_name = "tool.with.dots-and-dashes"
    provider = TestConfigProvider(special_name, {"key": "value"})

    # Test get_name method
    assert provider.get_name() == special_name

    # Test get_data method
    assert provider.get_data() == {"key": "value"}


def test_config_provider_data_types():
    """
    Scenario:
        Test ConfigProvider with various data types.

    Expected:
        Various data types are handled correctly.
    """
    mixed_data = {
        "string": "value",
        "integer": 42,
        "float": 3.14,
        "boolean": True,
        "list": [1, 2, 3],
        "dict": {"nested": "value"},
        "none": None,
    }

    provider = TestConfigProvider("mixed-tool", mixed_data)

    # Test get_name method
    assert provider.get_name() == "mixed-tool"

    # Test get_data method returns all data types
    returned_data = provider.get_data()
    assert returned_data["string"] == "value"
    assert returned_data["integer"] == 42
    assert returned_data["float"] == 3.14
    assert returned_data["boolean"] is True
    assert returned_data["list"] == [1, 2, 3]
    assert returned_data["dict"] == {"nested": "value"}
    assert returned_data["none"] is None
