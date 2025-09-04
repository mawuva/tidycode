"""
TidyCode YAML Module Initialization Tests
"""

import pytest

from tidycode.core.yaml import load_yaml_file, save_yaml_file, YamlFileManager


def test_yaml_module_imports():
    """
    Scenario:
        Import the YAML module and check that all expected functions and classes are available.

    Expected:
        All expected functions and classes are imported correctly.
    """
    # Test that functions are callable
    assert callable(load_yaml_file)
    assert callable(save_yaml_file)
    
    # Test that class is available
    assert YamlFileManager is not None
    
    # Test that class can be instantiated (with proper file)
    # This is a basic import test, actual functionality is tested in other test files


def test_yaml_module_all_exports():
    """
    Scenario:
        Check that the module's __all__ list contains all expected exports.

    Expected:
        All expected items are in __all__.
    """
    from tidycode.core.yaml import __all__
    
    expected_exports = [
        "load_yaml_file",
        "save_yaml_file", 
        "YamlFileManager"
    ]
    
    for export in expected_exports:
        assert export in __all__
    
    # Ensure no unexpected exports
    assert len(__all__) == len(expected_exports)
