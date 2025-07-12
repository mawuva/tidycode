"""
Test the ruamel.yaml adapter.
"""

from tidycode.core.yaml import RuamelYAMLAdapter
from pathlib import Path
import tempfile


def test_ruamel_adapter_load_and_dump_str():
    backend = RuamelYAMLAdapter()
    data = {"name": "Ephraïm", "list": [1, 2, 3]}
    dumped = backend.dump_str(data)
    loaded = backend.load_str(dumped)
    assert loaded == data


def test_ruamel_adapter_load_and_save_file():
    backend = RuamelYAMLAdapter()
    data = {"project": {"name": "tidycode", "version": "1.0.0"}}
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "config.yaml"
        backend.save_file(data, path)
        loaded = backend.load_file(path)
        assert loaded == data


