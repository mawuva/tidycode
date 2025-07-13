"""
Test the base adapter interface.
"""

from tidycode.core.yaml import PyYAMLAdapter, RuamelYAMLAdapter, YAMLAdapter


def test_adapters_implement_interface():
    for backend_cls in [PyYAMLAdapter, RuamelYAMLAdapter]:
        backend = backend_cls()
        assert isinstance(backend, YAMLAdapter)
