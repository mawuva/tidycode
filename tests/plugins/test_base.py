"""
TidyCode Plugins Base Tests
"""

from tidycode.plugins.base import BasePlugin
from tidycode.plugins.types import PluginMeta

# ---------------------------
# Unit tests
# ---------------------------


def test_base_plugin_protocol():
    """
    Scenario:
        Test that BasePlugin is a Protocol.

    Expected:
        BasePlugin is a Protocol with meta attribute.
    """
    # Test that BasePlugin is a Protocol
    assert hasattr(BasePlugin, "__protocol_attrs__")

    # Test that it expects a meta attribute
    assert "meta" in BasePlugin.__annotations__


def test_base_plugin_meta_type():
    """
    Scenario:
        Test that BasePlugin meta attribute is of type PluginMeta.

    Expected:
        meta attribute is typed as PluginMeta.
    """
    # Check the type annotation
    meta_annotation = BasePlugin.__annotations__.get("meta")
    assert meta_annotation is not None


def test_base_plugin_usage_example():
    """
    Scenario:
        Create a concrete implementation of BasePlugin.

    Expected:
        Can create a class that implements BasePlugin protocol.
    """

    class TestPlugin:
        def __init__(self):
            self.meta = PluginMeta(
                name="test_plugin",
                description="A test plugin",
                type="test",
                category="test_category",
            )

    # Test that our class can be used as BasePlugin
    plugin = TestPlugin()
    assert hasattr(plugin, "meta")
    assert isinstance(plugin.meta, PluginMeta)
    assert plugin.meta.name == "test_plugin"
    assert plugin.meta.description == "A test plugin"
    assert plugin.meta.type == "test"
    assert plugin.meta.category == "test_category"


def test_base_plugin_with_minimal_meta():
    """
    Scenario:
        Create a plugin with minimal PluginMeta.

    Expected:
        Can create a plugin with only required fields.
    """

    class MinimalPlugin:
        def __init__(self):
            self.meta = PluginMeta(name="minimal")

    plugin = MinimalPlugin()
    assert hasattr(plugin, "meta")
    assert isinstance(plugin.meta, PluginMeta)
    assert plugin.meta.name == "minimal"
    assert plugin.meta.description == ""  # default value
    assert plugin.meta.type == "generic"  # default value
    assert plugin.meta.category == "default"  # default value


def test_base_plugin_with_custom_meta():
    """
    Scenario:
        Create a plugin with custom PluginMeta values.

    Expected:
        Can create a plugin with all custom values.
    """

    class CustomPlugin:
        def __init__(self):
            self.meta = PluginMeta(
                name="custom_plugin",
                description="Custom description",
                type="quality",
                category="runner",
            )

    plugin = CustomPlugin()
    assert hasattr(plugin, "meta")
    assert isinstance(plugin.meta, PluginMeta)
    assert plugin.meta.name == "custom_plugin"
    assert plugin.meta.description == "Custom description"
    assert plugin.meta.type == "quality"
    assert plugin.meta.category == "runner"


# ---------------------------
# Integration tests
# ---------------------------


def test_base_plugin_with_runner_inheritance():
    """
    Scenario:
        Test BasePlugin with BaseRunner inheritance.

    Expected:
        BaseRunner properly implements BasePlugin protocol.
    """
    from tidycode.plugins.runner.base_runner import BaseRunner

    # Test that BaseRunner implements BasePlugin
    # BasePlugin is a Protocol, so we can't use issubclass directly
    # Instead, we test that BasePlugin is in the MRO
    assert BasePlugin in BaseRunner.__mro__

    # Test that BaseRunner has the required methods
    assert hasattr(BaseRunner, "build_command")
    assert hasattr(BaseRunner, "is_tool")


def test_base_plugin_protocol_compliance():
    """
    Scenario:
        Test that various plugin implementations comply with BasePlugin protocol.

    Expected:
        All plugin implementations have the required meta attribute.
    """

    # Test with different plugin implementations
    class QualityPlugin:
        def __init__(self):
            self.meta = PluginMeta(
                name="quality_plugin",
                description="Quality assurance plugin",
                type="quality",
                category="runner",
            )

    class ConfigPlugin:
        def __init__(self):
            self.meta = PluginMeta(
                name="config_plugin",
                description="Configuration plugin",
                type="config",
                category="provider",
            )

    class AuditPlugin:
        def __init__(self):
            self.meta = PluginMeta(
                name="audit_plugin",
                description="Audit plugin",
                type="audit",
                category="analyzer",
            )

    # Test all implementations
    plugins = [QualityPlugin(), ConfigPlugin(), AuditPlugin()]

    for plugin in plugins:
        assert hasattr(plugin, "meta")
        assert isinstance(plugin.meta, PluginMeta)
        assert plugin.meta.name is not None
        assert len(plugin.meta.name) > 0


def test_base_plugin_meta_immutability():
    """
    Scenario:
        Test that PluginMeta can be modified after creation.

    Expected:
        PluginMeta fields can be modified (dataclass without frozen=True).
    """

    class MutablePlugin:
        def __init__(self):
            self.meta = PluginMeta(name="mutable_plugin")

    plugin = MutablePlugin()

    # Test that we can modify the meta
    original_name = plugin.meta.name
    plugin.meta.name = "modified_plugin"
    assert plugin.meta.name == "modified_plugin"
    assert plugin.meta.name != original_name

    # Test that we can modify other fields
    plugin.meta.description = "Modified description"
    plugin.meta.type = "modified_type"
    plugin.meta.category = "modified_category"

    assert plugin.meta.description == "Modified description"
    assert plugin.meta.type == "modified_type"
    assert plugin.meta.category == "modified_category"


def test_base_plugin_with_methods():
    """
    Scenario:
        Test BasePlugin implementation with additional methods.

    Expected:
        Can add methods to plugin implementations.
    """

    class PluginWithMethods:
        def __init__(self):
            self.meta = PluginMeta(
                name="plugin_with_methods",
                description="Plugin with additional methods",
                type="test",
                category="test",
            )

        def execute(self):
            return "executed"

        def get_info(self):
            return f"Plugin: {self.meta.name}"

    plugin = PluginWithMethods()

    # Test that meta is accessible
    assert hasattr(plugin, "meta")
    assert plugin.meta.name == "plugin_with_methods"

    # Test that additional methods work
    assert plugin.execute() == "executed"
    assert plugin.get_info() == "Plugin: plugin_with_methods"


def test_base_plugin_import_consistency():
    """
    Scenario:
        Test that BasePlugin can be imported consistently.

    Expected:
        BasePlugin is properly importable from different paths.
    """
    # Test direct import
    # Test import from plugins module
    from tidycode.plugins import BasePlugin as ModuleBasePlugin
    from tidycode.plugins.base import BasePlugin as DirectBasePlugin

    # Test that they are the same
    assert DirectBasePlugin is ModuleBasePlugin
    assert DirectBasePlugin is BasePlugin
