"""
Test toml_config_editor.py
"""

import pytest
from tidycode.utils import (
    inject_toml_config,
    inject_tool_config,
    inject_tool_config_in_file,
    load_toml_file,
)


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


def test_inject_tool_config_in_file_add_new(tmp_path):
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text("[tool.other]\nkey = 'value'\n")

    black_conf = {
        "line-length": 88,
        "target-version": ["py38"],
    }

    inject_tool_config_in_file(
        pyproject_path, "black", black_conf, update_if_exists=False, dry_run=False
    )

    data = load_toml_file(pyproject_path)
    assert "black" in data.get("tool", {})
    assert data["tool"]["black"]["line-length"] == 88
    assert data["tool"]["black"]["target-version"] == ["py38"]


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


def test_inject_tool_config_in_file_update_merge(tmp_path):
    pyproject_path = tmp_path / "pyproject.toml"
    content = """
[tool.black]
line-length = 80
"""

    pyproject_path.write_text(content)

    black_conf = {
        "target-version": ["py38"],
    }

    inject_tool_config_in_file(
        pyproject_path, "black", black_conf, update_if_exists=True, dry_run=False
    )

    data = load_toml_file(pyproject_path)
    assert data["tool"]["black"]["line-length"] == 80
    assert data["tool"]["black"]["target-version"] == ["py38"]
