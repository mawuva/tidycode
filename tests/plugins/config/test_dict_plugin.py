"""
TidyCode Core PyProject Dict Plugin Tests
"""

from tidycode.plugins.config import ConfigProvider, DictPlugin


def test_dict_plugin_inherits_from_config_provider():
    """
    Scenario:
        Test that DictPlugin inherits from ConfigProvider.

    Expected:
        DictPlugin is a subclass of ConfigProvider.
    """
    assert issubclass(DictPlugin, ConfigProvider)


def test_dict_plugin_initialization():
    """
    Scenario:
        Test DictPlugin initialization with name and data.

    Expected:
        DictPlugin is initialized correctly with the provided name and data.
    """
    test_data = {"key1": "value1", "key2": "value2"}
    plugin = DictPlugin("test-tool", test_data)

    # Verify internal attributes are set correctly
    assert plugin._name == "test-tool"
    assert plugin._data == test_data


def test_dict_plugin_get_name():
    """
    Scenario:
        Test DictPlugin get_name method.

    Expected:
        get_name returns the correct name.
    """
    plugin = DictPlugin("black", {"line-length": 88})

    assert plugin.get_name() == "black"


def test_dict_plugin_get_data():
    """
    Scenario:
        Test DictPlugin get_data method.

    Expected:
        get_data returns the correct data.
    """
    test_data = {"line-length": 88, "target-version": "py39"}
    plugin = DictPlugin("black", test_data)

    assert plugin.get_data() == test_data


def test_dict_plugin_data_is_reference():
    """
    Scenario:
        Test that DictPlugin get_data returns a reference to the original data.

    Expected:
        Modifying the returned data affects the original (this is the actual behavior).
    """
    original_data = {"key": "value"}
    plugin = DictPlugin("test-tool", original_data)

    returned_data = plugin.get_data()

    # Modify returned data
    returned_data["key"] = "modified"

    # Original data should be modified (reference behavior)
    assert original_data["key"] == "modified"
    assert plugin.get_data()["key"] == "modified"


def test_dict_plugin_empty_data():
    """
    Scenario:
        Test DictPlugin with empty data.

    Expected:
        Empty data is handled correctly.
    """
    plugin = DictPlugin("empty-tool", {})

    assert plugin.get_name() == "empty-tool"
    assert plugin.get_data() == {}


def test_dict_plugin_complex_data():
    """
    Scenario:
        Test DictPlugin with complex nested data.

    Expected:
        Complex data is handled correctly.
    """
    complex_data = {
        "dependencies": {"requests": "^2.28.0", "pytest": "^7.0.0"},
        "dev-dependencies": {"black": "^22.0.0", "ruff": "^0.1.0"},
        "scripts": {"test": "pytest", "format": "black .", "lint": "ruff check ."},
    }

    plugin = DictPlugin("complex-tool", complex_data)

    assert plugin.get_name() == "complex-tool"
    assert plugin.get_data() == complex_data


def test_dict_plugin_special_characters_in_name():
    """
    Scenario:
        Test DictPlugin with special characters in name.

    Expected:
        Special characters are handled correctly.
    """
    special_name = "tool.with.dots-and-dashes"
    plugin = DictPlugin(special_name, {"key": "value"})

    assert plugin.get_name() == special_name
    assert plugin.get_data() == {"key": "value"}


def test_dict_plugin_multiple_instances():
    """
    Scenario:
        Test multiple instances of DictPlugin.

    Expected:
        Each instance maintains its own data.
    """
    plugin1 = DictPlugin("tool1", {"key1": "value1"})
    plugin2 = DictPlugin("tool2", {"key2": "value2"})

    # Verify each instance has its own data
    assert plugin1.get_name() == "tool1"
    assert plugin1.get_data() == {"key1": "value1"}

    assert plugin2.get_name() == "tool2"
    assert plugin2.get_data() == {"key2": "value2"}


def test_dict_plugin_data_types():
    """
    Scenario:
        Test DictPlugin with various data types.

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

    plugin = DictPlugin("mixed-tool", mixed_data)

    returned_data = plugin.get_data()
    assert returned_data["string"] == "value"
    assert returned_data["integer"] == 42
    assert returned_data["float"] == 3.14
    assert returned_data["boolean"] is True
    assert returned_data["list"] == [1, 2, 3]
    assert returned_data["dict"] == {"nested": "value"}
    assert returned_data["none"] is None


def test_dict_plugin_unicode_data():
    """
    Scenario:
        Test DictPlugin with unicode data.

    Expected:
        Unicode data is handled correctly.
    """
    unicode_data = {
        "name": "tidycode",
        "description": "Un outil pour gérer les fichiers pyproject.toml",
        "emoji": "🚀",
    }

    plugin = DictPlugin("unicode-tool", unicode_data)

    assert plugin.get_name() == "unicode-tool"
    assert plugin.get_data() == unicode_data


def test_dict_plugin_none_name():
    """
    Scenario:
        Test DictPlugin with None as name.

    Expected:
        None name is handled correctly.
    """
    plugin = DictPlugin(None, {"key": "value"})

    assert plugin.get_name() is None
    assert plugin.get_data() == {"key": "value"}


def test_dict_plugin_none_data():
    """
    Scenario:
        Test DictPlugin with None as data.

    Expected:
        None data is handled correctly.
    """
    plugin = DictPlugin("test-tool", None)

    assert plugin.get_name() == "test-tool"
    assert plugin.get_data() is None
