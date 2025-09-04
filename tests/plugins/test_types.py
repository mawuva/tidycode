"""
TidyCode Plugins Types Tests
"""

import pytest

from tidycode.plugins.types import PluginMeta

# ---------------------------
# Unit tests
# ---------------------------


def test_plugin_meta_creation():
    """
    Scenario:
        Create a PluginMeta with all fields.

    Expected:
        All fields are properly set.
    """
    meta = PluginMeta(
        name="test_plugin",
        description="A test plugin",
        type="quality",
        category="runner",
    )

    assert meta.name == "test_plugin"
    assert meta.description == "A test plugin"
    assert meta.type == "quality"
    assert meta.category == "runner"


def test_plugin_meta_minimal_creation():
    """
    Scenario:
        Create a PluginMeta with only required fields.

    Expected:
        Required fields are set, optional fields have defaults.
    """
    meta = PluginMeta(name="minimal_plugin")

    assert meta.name == "minimal_plugin"
    assert meta.description == ""  # default value
    assert meta.type == "generic"  # default value
    assert meta.category == "default"  # default value


def test_plugin_meta_with_description():
    """
    Scenario:
        Create a PluginMeta with name and description.

    Expected:
        Name and description are set, other fields have defaults.
    """
    meta = PluginMeta(name="described_plugin", description="A plugin with description")

    assert meta.name == "described_plugin"
    assert meta.description == "A plugin with description"
    assert meta.type == "generic"  # default value
    assert meta.category == "default"  # default value


def test_plugin_meta_with_type():
    """
    Scenario:
        Create a PluginMeta with name and type.

    Expected:
        Name and type are set, other fields have defaults.
    """
    meta = PluginMeta(name="typed_plugin", type="audit")

    assert meta.name == "typed_plugin"
    assert meta.description == ""  # default value
    assert meta.type == "audit"
    assert meta.category == "default"  # default value


def test_plugin_meta_with_category():
    """
    Scenario:
        Create a PluginMeta with name and category.

    Expected:
        Name and category are set, other fields have defaults.
    """
    meta = PluginMeta(name="categorized_plugin", category="config_provider")

    assert meta.name == "categorized_plugin"
    assert meta.description == ""  # default value
    assert meta.type == "generic"  # default value
    assert meta.category == "config_provider"


def test_plugin_meta_with_type_and_category():
    """
    Scenario:
        Create a PluginMeta with name, type, and category.

    Expected:
        Name, type, and category are set, description has default.
    """
    meta = PluginMeta(name="full_plugin", type="extension", category="analyzer")

    assert meta.name == "full_plugin"
    assert meta.description == ""  # default value
    assert meta.type == "extension"
    assert meta.category == "analyzer"


def test_plugin_meta_empty_name():
    """
    Scenario:
        Create a PluginMeta with empty name.

    Expected:
        Empty name is allowed.
    """
    meta = PluginMeta(name="")

    assert meta.name == ""
    assert meta.description == ""
    assert meta.type == "generic"
    assert meta.category == "default"


def test_plugin_meta_unicode_name():
    """
    Scenario:
        Create a PluginMeta with unicode characters in name.

    Expected:
        Unicode characters are properly handled.
    """
    meta = PluginMeta(name="plugin_测试", description="Plugin with unicode: café ñöç")

    assert meta.name == "plugin_测试"
    assert meta.description == "Plugin with unicode: café ñöç"
    assert meta.type == "generic"
    assert meta.category == "default"


def test_plugin_meta_long_values():
    """
    Scenario:
        Create a PluginMeta with long values.

    Expected:
        Long values are properly handled.
    """
    long_name = "a" * 100
    long_description = "b" * 200
    long_type = "c" * 50
    long_category = "d" * 50

    meta = PluginMeta(
        name=long_name,
        description=long_description,
        type=long_type,
        category=long_category,
    )

    assert meta.name == long_name
    assert meta.description == long_description
    assert meta.type == long_type
    assert meta.category == long_category


def test_plugin_meta_special_characters():
    """
    Scenario:
        Create a PluginMeta with special characters.

    Expected:
        Special characters are properly handled.
    """
    meta = PluginMeta(
        name="plugin-with_special.chars",
        description="Description with special chars: @#$%^&*()",
        type="type-with-dashes",
        category="category_with_underscores",
    )

    assert meta.name == "plugin-with_special.chars"
    assert meta.description == "Description with special chars: @#$%^&*()"
    assert meta.type == "type-with-dashes"
    assert meta.category == "category_with_underscores"


# ---------------------------
# Integration tests
# ---------------------------


def test_plugin_meta_immutability():
    """
    Scenario:
        Test that PluginMeta fields can be modified after creation.

    Expected:
        PluginMeta fields can be modified (dataclass without frozen=True).
    """
    meta = PluginMeta(name="mutable_plugin")

    # Test that we can modify the fields
    original_name = meta.name
    meta.name = "modified_plugin"
    assert meta.name == "modified_plugin"
    assert meta.name != original_name

    # Test that we can modify other fields
    meta.description = "Modified description"
    meta.type = "modified_type"
    meta.category = "modified_category"

    assert meta.description == "Modified description"
    assert meta.type == "modified_type"
    assert meta.category == "modified_category"


def test_plugin_meta_equality():
    """
    Scenario:
        Test PluginMeta equality comparison.

    Expected:
        PluginMeta instances with same values are equal.
    """
    meta1 = PluginMeta(
        name="test_plugin",
        description="Test description",
        type="quality",
        category="runner",
    )

    meta2 = PluginMeta(
        name="test_plugin",
        description="Test description",
        type="quality",
        category="runner",
    )

    meta3 = PluginMeta(
        name="different_plugin",
        description="Test description",
        type="quality",
        category="runner",
    )

    # Test equality
    assert meta1 == meta2
    assert meta1 != meta3
    assert meta2 != meta3


def test_plugin_meta_repr():
    """
    Scenario:
        Test PluginMeta string representation.

    Expected:
        PluginMeta has proper string representation.
    """
    meta = PluginMeta(
        name="test_plugin",
        description="Test description",
        type="quality",
        category="runner",
    )

    repr_str = repr(meta)
    assert "PluginMeta" in repr_str
    assert "test_plugin" in repr_str
    assert "Test description" in repr_str
    assert "quality" in repr_str
    assert "runner" in repr_str


def test_plugin_meta_str():
    """
    Scenario:
        Test PluginMeta string conversion.

    Expected:
        PluginMeta has proper string conversion.
    """
    meta = PluginMeta(
        name="test_plugin",
        description="Test description",
        type="quality",
        category="runner",
    )

    str_repr = str(meta)
    assert "PluginMeta" in str_repr
    assert "test_plugin" in str_repr


def test_plugin_meta_hash():
    """
    Scenario:
        Test PluginMeta hash functionality.

    Expected:
        PluginMeta instances cannot be hashed (dataclass without frozen=True).
    """
    meta1 = PluginMeta(
        name="test_plugin",
        description="Test description",
        type="quality",
        category="runner",
    )

    meta2 = PluginMeta(
        name="test_plugin",
        description="Test description",
        type="quality",
        category="runner",
    )

    # Test that PluginMeta cannot be hashed (mutable dataclass)
    with pytest.raises(TypeError, match="unhashable type"):
        hash(meta1)

    with pytest.raises(TypeError, match="unhashable type"):
        hash(meta2)


def test_plugin_meta_in_dict():
    """
    Scenario:
        Test PluginMeta usage in dictionaries and sets.

    Expected:
        PluginMeta cannot be used in sets or as dict keys (not hashable).
    """
    meta1 = PluginMeta(name="plugin1")
    meta2 = PluginMeta(name="plugin2")
    meta3 = PluginMeta(name="plugin1")  # Same as meta1

    # Test that PluginMeta cannot be used in sets (not hashable)
    with pytest.raises(TypeError, match="unhashable type"):
        {meta1, meta2, meta3}

    # Test in list (this should work)
    meta_list = [meta1, meta2, meta3]
    assert len(meta_list) == 3

    # Test that PluginMeta cannot be used as dictionary keys (not hashable)
    with pytest.raises(TypeError, match="unhashable type"):
        {meta1: "value1", meta2: "value2", meta3: "value3"}


def test_plugin_meta_common_types():
    """
    Scenario:
        Test PluginMeta with common plugin types and categories.

    Expected:
        Common plugin types and categories work correctly.
    """
    # Test quality plugins
    quality_meta = PluginMeta(
        name="black_runner",
        description="Black code formatter",
        type="quality",
        category="runner",
    )
    assert quality_meta.type == "quality"
    assert quality_meta.category == "runner"

    # Test config plugins
    config_meta = PluginMeta(
        name="dict_provider",
        description="Dictionary config provider",
        type="config",
        category="provider",
    )
    assert config_meta.type == "config"
    assert config_meta.category == "provider"

    # Test audit plugins
    audit_meta = PluginMeta(
        name="security_audit",
        description="Security audit tool",
        type="audit",
        category="analyzer",
    )
    assert audit_meta.type == "audit"
    assert audit_meta.category == "analyzer"

    # Test extension plugins
    extension_meta = PluginMeta(
        name="custom_extension",
        description="Custom extension",
        type="extension",
        category="custom",
    )
    assert extension_meta.type == "extension"
    assert extension_meta.category == "custom"


def test_plugin_meta_import_consistency():
    """
    Scenario:
        Test that PluginMeta can be imported consistently.

    Expected:
        PluginMeta is properly importable.
    """
    # Test direct import
    from tidycode.plugins.types import PluginMeta as DirectPluginMeta

    # Test that it's the same class
    assert DirectPluginMeta is PluginMeta

    # Test that we can create instances
    meta = PluginMeta(name="test")
    assert isinstance(meta, PluginMeta)
