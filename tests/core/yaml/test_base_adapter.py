"""
Test the base adapter interface.
"""

from tidycode.core.yaml import YAMLAdapter, PyYAMLAdapter, RuamelYAMLAdapter


def test_adapters_implement_interface():
    for backend_cls in [PyYAMLAdapter, RuamelYAMLAdapter]:
        backend = backend_cls()
        assert isinstance(backend, YAMLAdapter)
