"""
Test utils for YAML.
"""

import pytest

from tidycode.core.yaml.adapters.pyyaml_adapter import PyYAMLAdapter
from tidycode.core.yaml.adapters.ruamel_adapter import RuamelYAMLAdapter
from tidycode.core.yaml.manager import YAMLManager
from tidycode.core.yaml.utils import get_manager


def test_get_manager_default_returns_ruamel_adapter():
    manager = get_manager()
    assert isinstance(manager, YAMLManager)
    assert isinstance(manager.adapter, RuamelYAMLAdapter)


def test_get_manager_with_string_ruamel():
    manager = get_manager("ruamel")
    assert isinstance(manager.adapter, RuamelYAMLAdapter)


def test_get_manager_with_string_pyyaml():
    manager = get_manager("pyyaml")
    assert isinstance(manager.adapter, PyYAMLAdapter)


def test_get_manager_with_instance():
    adapter = PyYAMLAdapter()
    manager = get_manager(adapter)
    assert manager.adapter is adapter


def test_get_manager_with_invalid_string():
    with pytest.raises(ValueError, match="Unsupported YAML adapter: fake"):
        get_manager("fake")
