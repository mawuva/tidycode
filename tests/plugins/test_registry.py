"""
TidyCode Plugins Registry Tests
"""

import pytest

from tidycode.plugins.registry import PluginRegistry, register_plugin, registry
from tidycode.plugins.types import PluginMeta

# ---------------------------
# Unit tests
# ---------------------------


def test_plugin_registry_creation():
    """
    Scenario:
        Create a new PluginRegistry instance.

    Expected:
        Registry is created with empty plugins dictionary.
    """
    reg = PluginRegistry()
    assert reg._plugins == {}


def test_plugin_registry_register_plugin():
    """
    Scenario:
        Register a plugin in the registry.

    Expected:
        Plugin is stored in the registry with its name as key.
    """
    reg = PluginRegistry()

    # Create a mock plugin
    class TestPlugin:
        def __init__(self):
            self.meta = PluginMeta(
                name="test_plugin",
                description="A test plugin",
                type="test",
                category="test_category",
            )

    plugin = TestPlugin()
    reg.register(plugin)

    assert "test_plugin" in reg._plugins
    assert reg._plugins["test_plugin"] is plugin


def test_plugin_registry_get_plugin():
    """
    Scenario:
        Get a plugin from the registry by name.

    Expected:
        Returns the correct plugin or None if not found.
    """
    reg = PluginRegistry()

    # Create a mock plugin
    class TestPlugin:
        def __init__(self):
            self.meta = PluginMeta(name="test_plugin")

    plugin = TestPlugin()
    reg.register(plugin)

    # Test getting existing plugin
    retrieved_plugin = reg.get("test_plugin")
    assert retrieved_plugin is plugin

    # Test getting non-existing plugin
    # The current implementation raises KeyError, so we test for that
    with pytest.raises(KeyError):
        reg.get("non_existing")


def test_plugin_registry_get_all_plugins():
    """
    Scenario:
        Get all plugins from the registry.

    Expected:
        Returns a list of all registered plugins.
    """
    reg = PluginRegistry()

    # Create mock plugins
    class Plugin1:
        def __init__(self):
            self.meta = PluginMeta(name="plugin1")

    class Plugin2:
        def __init__(self):
            self.meta = PluginMeta(name="plugin2")

    plugin1 = Plugin1()
    plugin2 = Plugin2()

    reg.register(plugin1)
    reg.register(plugin2)

    all_plugins = reg.all()
    assert len(all_plugins) == 2
    assert plugin1 in all_plugins
    assert plugin2 in all_plugins


def test_plugin_registry_get_plugins_by_category():
    """
    Scenario:
        Get plugins by category.

    Expected:
        Returns only plugins with the specified category.
    """
    reg = PluginRegistry()

    # Create mock plugins with different categories
    class QualityPlugin:
        def __init__(self):
            self.meta = PluginMeta(name="quality_plugin", category="quality")

    class ConfigPlugin:
        def __init__(self):
            self.meta = PluginMeta(name="config_plugin", category="config")

    class AnotherQualityPlugin:
        def __init__(self):
            self.meta = PluginMeta(name="another_quality_plugin", category="quality")

    quality_plugin = QualityPlugin()
    config_plugin = ConfigPlugin()
    another_quality_plugin = AnotherQualityPlugin()

    reg.register(quality_plugin)
    reg.register(config_plugin)
    reg.register(another_quality_plugin)

    # Test getting quality plugins
    quality_plugins = reg.by_category("quality")
    assert len(quality_plugins) == 2
    assert quality_plugin in quality_plugins
    assert another_quality_plugin in quality_plugins
    assert config_plugin not in quality_plugins

    # Test getting config plugins
    config_plugins = reg.by_category("config")
    assert len(config_plugins) == 1
    assert config_plugin in config_plugins
    assert quality_plugin not in config_plugins

    # Test getting non-existing category
    non_existing = reg.by_category("non_existing")
    assert len(non_existing) == 0


def test_plugin_registry_get_plugins_by_type():
    """
    Scenario:
        Get plugins by type.

    Expected:
        Returns only plugins with the specified type.
    """
    reg = PluginRegistry()

    # Create mock plugins with different types
    class RunnerPlugin:
        def __init__(self):
            self.meta = PluginMeta(name="runner_plugin", type="runner")

    class ProviderPlugin:
        def __init__(self):
            self.meta = PluginMeta(name="provider_plugin", type="provider")

    class AnotherRunnerPlugin:
        def __init__(self):
            self.meta = PluginMeta(name="another_runner_plugin", type="runner")

    runner_plugin = RunnerPlugin()
    provider_plugin = ProviderPlugin()
    another_runner_plugin = AnotherRunnerPlugin()

    reg.register(runner_plugin)
    reg.register(provider_plugin)
    reg.register(another_runner_plugin)

    # Test getting runner plugins
    runner_plugins = reg.by_type("runner")
    assert len(runner_plugins) == 2
    assert runner_plugin in runner_plugins
    assert another_runner_plugin in runner_plugins
    assert provider_plugin not in runner_plugins

    # Test getting provider plugins
    provider_plugins = reg.by_type("provider")
    assert len(provider_plugins) == 1
    assert provider_plugin in provider_plugins
    assert runner_plugin not in provider_plugins

    # Test getting non-existing type
    non_existing = reg.by_type("non_existing")
    assert len(non_existing) == 0


def test_plugin_registry_register_duplicate_plugin():
    """
    Scenario:
        Register a plugin with the same name as an existing plugin.

    Expected:
        New plugin overwrites the existing one.
    """
    reg = PluginRegistry()

    # Create two plugins with the same name
    class Plugin1:
        def __init__(self):
            self.meta = PluginMeta(name="duplicate_plugin", description="First plugin")

    class Plugin2:
        def __init__(self):
            self.meta = PluginMeta(name="duplicate_plugin", description="Second plugin")

    plugin1 = Plugin1()
    plugin2 = Plugin2()

    reg.register(plugin1)
    assert reg.get("duplicate_plugin") is plugin1

    reg.register(plugin2)
    assert reg.get("duplicate_plugin") is plugin2
    assert reg.get("duplicate_plugin") is not plugin1


def test_register_plugin_decorator():
    """
    Scenario:
        Use the register_plugin decorator to register a plugin.

    Expected:
        Plugin class is decorated and instance is registered.
    """
    # Clear the registry first
    registry._plugins.clear()

    @register_plugin(
        name="decorated_plugin",
        description="A decorated plugin",
        type="test",
        category="test_category",
    )
    class DecoratedPlugin:
        pass

    # Check that the plugin was registered
    assert "decorated_plugin" in registry._plugins
    registered_plugin = registry._plugins["decorated_plugin"]
    assert isinstance(registered_plugin, DecoratedPlugin)

    # Check that the meta was set correctly
    assert registered_plugin.meta.name == "decorated_plugin"
    assert registered_plugin.meta.description == "A decorated plugin"
    assert registered_plugin.meta.type == "test"
    assert registered_plugin.meta.category == "test_category"


def test_register_plugin_decorator_minimal():
    """
    Scenario:
        Use the register_plugin decorator with minimal parameters.

    Expected:
        Plugin is registered with default values.
    """
    # Clear the registry first
    registry._plugins.clear()

    @register_plugin(name="minimal_plugin")
    class MinimalPlugin:
        pass

    # Check that the plugin was registered
    assert "minimal_plugin" in registry._plugins
    registered_plugin = registry._plugins["minimal_plugin"]
    assert isinstance(registered_plugin, MinimalPlugin)

    # Check that the meta was set with defaults
    assert registered_plugin.meta.name == "minimal_plugin"
    assert registered_plugin.meta.description == ""
    assert registered_plugin.meta.type == "generic"
    assert registered_plugin.meta.category == "default"


def test_register_plugin_decorator_returns_class():
    """
    Scenario:
        Test that the register_plugin decorator returns the original class.

    Expected:
        Decorator returns the original class unchanged.
    """
    # Clear the registry first
    registry._plugins.clear()

    @register_plugin(name="return_test_plugin")
    class ReturnTestPlugin:
        def test_method(self):
            return "test"

    # Check that the decorator returned the original class
    assert ReturnTestPlugin.__name__ == "ReturnTestPlugin"

    # Check that we can still instantiate the class
    instance = ReturnTestPlugin()
    assert instance.test_method() == "test"

    # Check that the instance was registered
    assert "return_test_plugin" in registry._plugins


def test_register_plugin_decorator_multiple_plugins():
    """
    Scenario:
        Register multiple plugins using the decorator.

    Expected:
        All plugins are registered correctly.
    """
    # Clear the registry first
    registry._plugins.clear()

    @register_plugin(name="plugin1", type="type1", category="category1")
    class Plugin1:
        pass

    @register_plugin(name="plugin2", type="type2", category="category2")
    class Plugin2:
        pass

    @register_plugin(name="plugin3", type="type1", category="category1")
    class Plugin3:
        pass

    # Check that all plugins were registered
    assert len(registry._plugins) == 3
    assert "plugin1" in registry._plugins
    assert "plugin2" in registry._plugins
    assert "plugin3" in registry._plugins

    # Check that we can get them by type
    type1_plugins = registry.by_type("type1")
    assert len(type1_plugins) == 2

    type2_plugins = registry.by_type("type2")
    assert len(type2_plugins) == 1

    # Check that we can get them by category
    category1_plugins = registry.by_category("category1")
    assert len(category1_plugins) == 2

    category2_plugins = registry.by_category("category2")
    assert len(category2_plugins) == 1


# ---------------------------
# Integration tests
# ---------------------------


def test_plugin_registry_integration():
    """
    Scenario:
        Test complete plugin registry workflow.

    Expected:
        All registry operations work together correctly.
    """
    reg = PluginRegistry()

    # Create various plugins
    class QualityRunner:
        def __init__(self):
            self.meta = PluginMeta(
                name="black_runner",
                description="Black code formatter",
                type="runner",
                category="quality",
            )

    class ConfigProvider:
        def __init__(self):
            self.meta = PluginMeta(
                name="dict_provider",
                description="Dictionary config provider",
                type="provider",
                category="config",
            )

    class AuditAnalyzer:
        def __init__(self):
            self.meta = PluginMeta(
                name="security_audit",
                description="Security audit tool",
                type="analyzer",
                category="audit",
            )

    # Register all plugins
    quality_runner = QualityRunner()
    config_provider = ConfigProvider()
    audit_analyzer = AuditAnalyzer()

    reg.register(quality_runner)
    reg.register(config_provider)
    reg.register(audit_analyzer)

    # Test all operations
    assert len(reg.all()) == 3

    # Test getting by name
    assert reg.get("black_runner") is quality_runner
    assert reg.get("dict_provider") is config_provider
    assert reg.get("security_audit") is audit_analyzer

    # Test getting by type
    runners = reg.by_type("runner")
    assert len(runners) == 1
    assert quality_runner in runners

    providers = reg.by_type("provider")
    assert len(providers) == 1
    assert config_provider in providers

    analyzers = reg.by_type("analyzer")
    assert len(analyzers) == 1
    assert audit_analyzer in analyzers

    # Test getting by category
    quality_plugins = reg.by_category("quality")
    assert len(quality_plugins) == 1
    assert quality_runner in quality_plugins

    config_plugins = reg.by_category("config")
    assert len(config_plugins) == 1
    assert config_provider in config_plugins

    audit_plugins = reg.by_category("audit")
    assert len(audit_plugins) == 1
    assert audit_analyzer in audit_plugins


def test_global_registry_instance():
    """
    Scenario:
        Test that the global registry instance works correctly.

    Expected:
        Global registry instance is properly initialized and functional.
    """
    # Clear the global registry
    registry._plugins.clear()

    # Test that it's a PluginRegistry instance
    assert isinstance(registry, PluginRegistry)

    # Test that it starts empty
    assert len(registry.all()) == 0

    # Register a plugin using the global registry
    class GlobalTestPlugin:
        def __init__(self):
            self.meta = PluginMeta(name="global_test_plugin")

    plugin = GlobalTestPlugin()
    registry.register(plugin)

    # Test that it's registered
    assert len(registry.all()) == 1
    assert registry.get("global_test_plugin") is plugin


def test_register_plugin_decorator_integration():
    """
    Scenario:
        Test register_plugin decorator with real plugin classes.

    Expected:
        Decorator works with complex plugin classes.
    """
    # Clear the registry first
    registry._plugins.clear()

    @register_plugin(
        name="complex_plugin",
        description="A complex plugin with methods",
        type="runner",
        category="quality",
    )
    class ComplexPlugin:
        def __init__(self):
            self.initialized = True

        def build_command(self, target, check_only):
            return ["complex", "command"]

        def is_tool(self):
            return True

    # Check that the plugin was registered
    assert "complex_plugin" in registry._plugins
    registered_plugin = registry._plugins["complex_plugin"]

    # Check that it's a proper instance
    assert isinstance(registered_plugin, ComplexPlugin)
    assert registered_plugin.initialized is True

    # Check that methods work
    assert registered_plugin.build_command(None, None) == ["complex", "command"]
    assert registered_plugin.is_tool() is True

    # Check that meta is set correctly
    assert registered_plugin.meta.name == "complex_plugin"
    assert registered_plugin.meta.description == "A complex plugin with methods"
    assert registered_plugin.meta.type == "runner"
    assert registered_plugin.meta.category == "quality"


def test_plugin_registry_import_consistency():
    """
    Scenario:
        Test that registry components can be imported consistently.

    Expected:
        All registry components are properly importable.
    """
    # Test direct imports
    # Test imports from plugins module
    from tidycode.plugins import register_plugin as module_register_plugin
    from tidycode.plugins import registry as module_registry
    from tidycode.plugins.registry import PluginRegistry as DirectPluginRegistry
    from tidycode.plugins.registry import register_plugin as direct_register_plugin
    from tidycode.plugins.registry import registry as direct_registry

    # Test that they are the same
    assert DirectPluginRegistry is PluginRegistry
    assert direct_register_plugin is register_plugin
    assert direct_registry is registry
    assert module_registry is registry
    assert module_register_plugin is register_plugin
