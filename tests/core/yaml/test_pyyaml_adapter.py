"""
Test the PyYAML adapter.
"""

import tempfile
from pathlib import Path

from tidycode.core.yaml import PyYAMLAdapter


def test_pyyaml_adapter_load_and_dump_str():
    backend = PyYAMLAdapter()
    data = {"name": "Ephraïm", "version": 1}
    dumped = backend.dump_str(data)
    loaded = backend.load_str(dumped)
    assert loaded == data


def test_pyyaml_adapter_load_and_save_file():
    backend = PyYAMLAdapter()
    data = {"a": 1, "b": {"c": 2}}
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test.yaml"
        backend.save_file(data, path)
        loaded = backend.load_file(path)
        assert loaded == data