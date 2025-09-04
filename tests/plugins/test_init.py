"""
TidyCode Plugins Module Initialization Tests
"""

from tidycode.plugins import BasePlugin, load_plugins_from, register_plugin, registry


def test_plugins_module_imports():
    """
    Scenario:
        Import the plugins module and check that all expected functions and classes are available.

    Expected:
        All expected functions and classes are imported correctly.
    """
    # Test that functions are callable
    assert callable(load_plugins_from)
    assert callable(register_plugin)

    # Test that classes are available
    assert BasePlugin is not None
    assert registry is not None

    # Test that classes can be used (with proper parameters)
    # This is a basic import test, actual functionality is tested in other test files
    assert hasattr(BasePlugin, "__protocol_attrs__")
    assert hasattr(registry, "register")


def test_plugins_module_all_exports():
    """
    Scenario:
        Check that the module's __all__ list contains all expected exports.

    Expected:
        All expected items are in __all__.
    """
    from tidycode.plugins import __all__

    expected_exports = [
        "registry",
        "register_plugin",
        "load_plugins_from",
        "BasePlugin",
    ]

    for export in expected_exports:
        assert export in __all__

    # Ensure no unexpected exports
    assert len(__all__) == len(expected_exports)


def test_plugins_module_import_consistency():
    """
    Scenario:
        Test that imports work consistently from different paths.

    Expected:
        All imports work correctly.
    """
    # Test direct imports
    from tidycode.plugins import (
        BasePlugin,
        load_plugins_from,
        register_plugin,
        registry,
    )

    assert BasePlugin is not None
    assert load_plugins_from is not None
    assert register_plugin is not None
    assert registry is not None

    # Test that they are the same objects
    from tidycode.plugins.base import BasePlugin as base_BasePlugin
    from tidycode.plugins.loader import load_plugins_from as loader_load_plugins_from
    from tidycode.plugins.registry import register_plugin as registry_register_plugin
    from tidycode.plugins.registry import registry as registry_registry

    assert BasePlugin is base_BasePlugin
    assert load_plugins_from is loader_load_plugins_from
    assert register_plugin is registry_register_plugin
    assert registry is registry_registry


def test_plugins_module_function_signatures():
    """
    Scenario:
        Test that imported functions have expected signatures.

    Expected:
        Functions have the expected signatures.
    """
    import inspect

    # Test load_plugins_from signature
    load_plugins_from_sig = inspect.signature(load_plugins_from)
    expected_params = ["package"]
    for param in expected_params:
        assert param in load_plugins_from_sig.parameters

    # Test register_plugin signature
    register_plugin_sig = inspect.signature(register_plugin)
    expected_params = ["name", "description", "type", "category"]
    for param in expected_params:
        assert param in register_plugin_sig.parameters


def test_plugins_module_class_attributes():
    """
    Scenario:
        Test that imported classes have expected attributes.

    Expected:
        Classes have the expected attributes.
    """
    # Test BasePlugin attributes
    assert hasattr(BasePlugin, "__protocol_attrs__")
    assert "meta" in BasePlugin.__annotations__

    # Test registry attributes
    assert hasattr(registry, "register")
    assert hasattr(registry, "get")
    assert hasattr(registry, "all")
    assert hasattr(registry, "by_category")
    assert hasattr(registry, "by_type")


def test_plugins_module_registry_instance():
    """
    Scenario:
        Test that the registry is properly initialized.

    Expected:
        Registry is a PluginRegistry instance.
    """
    from tidycode.plugins.registry import PluginRegistry

    assert isinstance(registry, PluginRegistry)
    assert hasattr(registry, "_plugins")


def test_plugins_module_protocol_compliance():
    """
    Scenario:
        Test that BasePlugin is a proper Protocol.

    Expected:
        BasePlugin is a Protocol with the expected structure.
    """
    # Test that it's a Protocol
    assert hasattr(BasePlugin, "__protocol_attrs__")

    # Test that it expects a meta attribute
    assert "meta" in BasePlugin.__annotations__

    # Test that the meta attribute is typed
    meta_annotation = BasePlugin.__annotations__.get("meta")
    assert meta_annotation is not None


def test_plugins_module_decorator_functionality():
    """
    Scenario:
        Test that register_plugin is a proper decorator.

    Expected:
        register_plugin is callable and returns a decorator.
    """
    # Test that register_plugin is callable
    assert callable(register_plugin)

    # Test that it returns a decorator (callable)
    decorator = register_plugin("test_plugin")
    assert callable(decorator)

    # Test that the decorator can be applied to a class
    @decorator
    class TestPlugin:
        pass

    # The decorator should have registered the plugin
    assert "test_plugin" in registry._plugins


def test_plugins_module_loader_functionality():
    """
    Scenario:
        Test that load_plugins_from is a proper function.

    Expected:
        load_plugins_from is callable and accepts package parameter.
    """
    # Test that load_plugins_from is callable
    assert callable(load_plugins_from)

    # Test that it accepts a string parameter
    import inspect

    sig = inspect.signature(load_plugins_from)
    assert "package" in sig.parameters

    # Test that the parameter accepts Union[str, ModuleType]
    package_param = sig.parameters["package"]
    assert package_param.annotation is not None


def test_plugins_module_integration():
    """
    Scenario:
        Test that all components work together.

    Expected:
        All components can be used together.
    """
    # Clear the registry first
    registry._plugins.clear()

    # Test using register_plugin decorator
    @register_plugin(
        name="integration_test_plugin",
        description="A plugin for integration testing",
        type="test",
        category="integration",
    )
    class IntegrationTestPlugin:
        pass

    # Test that the plugin was registered
    assert "integration_test_plugin" in registry._plugins
    registered_plugin = registry._plugins["integration_test_plugin"]
    assert isinstance(registered_plugin, IntegrationTestPlugin)

    # Test that we can get it from the registry
    retrieved_plugin = registry.get("integration_test_plugin")
    assert retrieved_plugin is registered_plugin

    # Test that we can get it by category
    integration_plugins = registry.by_category("integration")
    assert len(integration_plugins) == 1
    assert registered_plugin in integration_plugins

    # Test that we can get it by type
    test_plugins = registry.by_type("test")
    assert len(test_plugins) == 1
    assert registered_plugin in test_plugins


def test_plugins_module_enum_values():
    """
    Scenario:
        Test that the module exports work with common plugin types.

    Expected:
        All exports work with common plugin types and categories.
    """
    # Clear the registry first
    registry._plugins.clear()

    # Test with quality plugin
    @register_plugin(
        name="quality_test_plugin",
        description="A quality plugin",
        type="quality",
        category="runner",
    )
    class QualityTestPlugin:
        pass

    # Test with config plugin
    @register_plugin(
        name="config_test_plugin",
        description="A config plugin",
        type="config",
        category="provider",
    )
    class ConfigTestPlugin:
        pass

    # Test that both plugins were registered
    assert len(registry.all()) == 2
    assert "quality_test_plugin" in registry._plugins
    assert "config_test_plugin" in registry._plugins

    # Test getting by type
    quality_plugins = registry.by_type("quality")
    assert len(quality_plugins) == 1

    config_plugins = registry.by_type("config")
    assert len(config_plugins) == 1

    # Test getting by category
    runner_plugins = registry.by_category("runner")
    assert len(runner_plugins) == 1

    provider_plugins = registry.by_category("provider")
    assert len(provider_plugins) == 1
