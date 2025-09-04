"""
TidyCode Plugins Runner Module Initialization Tests
"""

from tidycode.plugins.runner import BaseRunner


def test_runner_module_imports():
    """
    Scenario:
        Import the runner module and check that all expected classes are available.

    Expected:
        All expected classes are imported correctly.
    """
    # Test that class is available
    assert BaseRunner is not None

    # Test that class can be imported (with proper parameters)
    # This is a basic import test, actual functionality is tested in other test files
    assert isinstance(BaseRunner, type)


def test_runner_module_all_exports():
    """
    Scenario:
        Check that the module's __all__ list contains all expected exports.

    Expected:
        All expected items are in __all__.
    """
    from tidycode.plugins.runner import __all__

    expected_exports = ["BaseRunner"]

    for export in expected_exports:
        assert export in __all__

    # Ensure no unexpected exports
    assert len(__all__) == len(expected_exports)


def test_runner_module_import_consistency():
    """
    Scenario:
        Test that imports work consistently from different paths.

    Expected:
        All imports work correctly.
    """
    # Test direct imports
    from tidycode.plugins.runner import BaseRunner

    assert BaseRunner is not None

    # Test that they are the same objects
    from tidycode.plugins.runner.base_runner import BaseRunner as base_runner_BaseRunner

    assert BaseRunner is base_runner_BaseRunner


def test_runner_module_class_attributes():
    """
    Scenario:
        Test that imported classes have expected attributes.

    Expected:
        Classes have the expected attributes.
    """
    # Test BaseRunner attributes
    assert hasattr(BaseRunner, "__abstractmethods__")
    assert hasattr(BaseRunner, "build_command")
    assert hasattr(BaseRunner, "is_tool")

    # Test that build_command is abstract
    assert "build_command" in BaseRunner.__abstractmethods__


def test_runner_module_inheritance():
    """
    Scenario:
        Test that BaseRunner inherits from BasePlugin.

    Expected:
        BaseRunner properly inherits from BasePlugin.
    """
    from tidycode.plugins.base import BasePlugin

    # BasePlugin is a Protocol, so we can't use issubclass directly
    # Instead, we test that BasePlugin is in the MRO
    assert BasePlugin in BaseRunner.__mro__
