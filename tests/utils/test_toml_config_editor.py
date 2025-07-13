"""
Test toml_config_editor.py
"""

from pathlib import Path

import pytest

from tidycode.utils import (
    inject_toml_config,
    inject_tool_config,
    inject_tool_config_in_file,
)


@pytest.fixture
def tmp_pyproject(tmp_path: Path):
    file = tmp_path / "pyproject.toml"
    file.write_text("[tool.poetry]\nname = 'demo'\n", encoding="utf-8")
    return file


def test_inject_without_conflict():
    base = {}
    new = {"tool": {"black": {"line-length": 88}}}
    result = inject_toml_config(base, new)
    assert result["tool"]["black"]["line-length"] == 88


def test_inject_with_conflict_error():
    base = {"tool": {"black": {"line-length": 88}}}
    new = {"tool": {"black": {"line-length": 120}}}
    with pytest.raises(ValueError):
        inject_toml_config(base, new, overwrite=False)


def test_inject_with_overwrite():
    base = {"tool": {"black": {"line-length": 88}}}
    new = {"tool": {"black": {"line-length": 120}}}
    result = inject_toml_config(base, new, overwrite=True)
    assert result["tool"]["black"]["line-length"] == 120


def test_dry_run_does_not_modify_original():
    base = {"tool": {"black": {"line-length": 88}}}
    new = {"tool": {"ruff": {"line-length": 100}}}
    result = inject_toml_config(base, new, dry_run=True)
    assert "ruff" in result["tool"]
    assert "ruff" not in base["tool"]


def test_inject_tool_config():
    base = {"tool": {"black": {"line-length": 80}}}
    new_config = {"line-length": 88, "target-version": ["py38"]}

    with pytest.raises(ValueError):
        inject_tool_config(base, "black", new_config, overwrite=False)

    updated = inject_tool_config(base, "black", new_config, overwrite=True)
    assert updated["tool"]["black"]["line-length"] == 88
    assert updated["tool"]["black"]["target-version"] == ["py38"]


def test_inject_tool_config_in_file_error_on_existing(tmp_path):
    pyproject_path = tmp_path / "pyproject.toml"
    content = """
[tool.black]
line-length = 80
"""
    pyproject_path.write_text(content)

    black_conf = {
        "line-length": 88,
    }

    with pytest.raises(ValueError):
        inject_tool_config_in_file(
            pyproject_path, "black", black_conf, update_if_exists=False, dry_run=False
        )
