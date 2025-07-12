"""
Test the fake YAML adapter.
"""

from tidycode.core.yaml import YAMLAdapter, YAMLManager
from pathlib import Path
from typing import Dict
import yaml


class FakeYamlAdapter(YAMLAdapter):
    def __init__(self):
        self.last_loaded = None
        self.last_dumped = None

    def load(self, stream) -> Dict:
        content = stream.read()
        self.last_loaded = content
        return yaml.safe_load(content) or {}

    def dump(self, data: Dict, stream):
        self.last_dumped = data
        yaml.safe_dump(data, stream)

    def dump_str(self, data: Dict) -> str:
        self.last_dumped = data
        return yaml.safe_dump(data)

    def load_str(self, string: str) -> Dict:
        self.last_loaded = string
        return yaml.safe_load(string) or {}

    def load_file(self, path: Path) -> Dict:
        content = path.read_text(encoding="utf-8")
        self.last_loaded = content
        return yaml.safe_load(content) or {}

    def save_file(self, data: Dict, path: Path):
        self.last_dumped = data
        yaml_str = yaml.safe_dump(data)
        path.write_text(yaml_str, encoding="utf-8")


def test_load_file_reads_content(tmp_path: Path):
    adapter = FakeYamlAdapter()
    manager = YAMLManager(adapter=adapter)

    file = tmp_path / "config.yaml"
    file.write_text("repos:\n  - repo: fake-repo", encoding="utf-8")

    config = manager.load_file(file)

    assert config == {"repos": [{"repo": "fake-repo"}]}
    assert adapter.last_loaded == "repos:\n  - repo: fake-repo"


def test_save_file_writes_content(tmp_path: Path):
    adapter = FakeYamlAdapter()
    manager = YAMLManager(adapter=adapter)

    file = tmp_path / "config.yaml"

    config = {"repos": [{"repo": "another-repo"}]}
    manager.save_file(config, file)

    assert adapter.last_dumped == config
    assert "another-repo" in file.read_text(encoding="utf-8")


def test_load_file_returns_dict_on_empty_file(tmp_path: Path):
    empty_file = tmp_path / "empty.yaml"
    empty_file.write_text("")

    adapter = FakeYamlAdapter()
    manager = YAMLManager(adapter=adapter)

    result = manager.load_file(empty_file)
    assert isinstance(result, dict)
    assert (
        "repos" not in result
        or result.get("repos") is None
        or result.get("repos") == []
    )  # selon contenu vide
