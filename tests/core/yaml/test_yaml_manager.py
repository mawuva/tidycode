"""
Test the YAML manager.
"""

from pathlib import Path

from tidycode.core.yaml import PyYAMLAdapter, RuamelYAMLAdapter, YAMLManager


def test_manager_with_pyyaml():
    manager = YAMLManager(PyYAMLAdapter())
    data = {"hello": "world"}
    s = manager.dump_str(data)
    assert "hello" in s
    loaded = manager.load_str(s)
    assert loaded == data


def test_manager_with_ruamel():
    manager = YAMLManager(RuamelYAMLAdapter())
    data = {"hello": ["a", "b", "c"]}
    s = manager.dump_str(data)
    assert "hello" in s
    loaded = manager.load_str(s)
    assert loaded == data


def test_manager_file_roundtrip(tmp_path: Path):
    manager = YAMLManager()
    d = {"a": 123, "b": {"x": True}}
    file_path = tmp_path / "config.yaml"
    manager.save_file(d, file_path)
    reloaded = manager.load_file(file_path)
    assert reloaded == d
