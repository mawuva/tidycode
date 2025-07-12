"""
Test pyproject_helpers.py
"""

import pytest
from tidycode.utils import (
    load_pyproject,
    save_pyproject,
    has_tool_section,
    get_tool_section,
    set_tool_section,
    remove_tool_section,
    inject_pyproject_config,
    diff_pyproject_config,
    format_pyproject_diff_plaintext,
    remove_tool_section_and_return,
)

def test_load_empty_pyproject(empty_tmp_pyproject):
    data = load_pyproject(empty_tmp_pyproject)
    assert data == {}

def test_save_and_reload(tmp_path):
    path = tmp_path / "pyproject.toml"
    original = {"tool": {"black": {"line-length": 88}}}
    save_pyproject(original, path)
    loaded = load_pyproject(path)
    assert loaded["tool"]["black"]["line-length"] == 88

def test_has_tool_config():
    data = {"tool": {"black": {"line-length": 88}}}
    assert has_tool_section(data, "black") is True
    assert has_tool_section(data, "ruff") is False

def test_inject_without_conflict():
    base = {}
    new = {"tool": {"black": {"line-length": 88}}}
    result = inject_pyproject_config(base, new)
    assert result["tool"]["black"]["line-length"] == 88

def test_inject_with_conflict_error():
    base = {"tool": {"black": {"line-length": 88}}}
    new = {"tool": {"black": {"line-length": 120}}}
    with pytest.raises(ValueError):
        inject_pyproject_config(base, new, overwrite=False) 

def test_inject_with_overwrite():
    base = {"tool": {"black": {"line-length": 88}}}
    new = {"tool": {"black": {"line-length": 120}}}
    result = inject_pyproject_config(base, new, overwrite=True)
    assert result["tool"]["black"]["line-length"] == 120

def test_dry_run_does_not_modify_original():
    base = {"tool": {"black": {"line-length": 88}}}
    new = {"tool": {"ruff": {"line-length": 100}}}
    result = inject_pyproject_config(base, new, dry_run=True)
    assert "ruff" in result["tool"]
    assert "ruff" not in base["tool"]

def test_get_and_set_tool_section():
    data = {}
    assert get_tool_section(data, "black") is None

    data = set_tool_section(data, "black", {"line-length": 88})
    assert get_tool_section(data, "black") == {"line-length": 88}

def test_remove_tool_section():
    data = {"tool": {"black": {"line-length": 88}}}
    result = remove_tool_section(data, "black")
    assert result is True
    assert "black" not in data["tool"]

def test_remove_nonexistent_tool_section_no_crash():
    data = {"tool": {"black": {"line-length": 88}}}
    result = remove_tool_section(data, "ruff")  # does nothing
    assert result is False
    assert "black" in data["tool"]

def test_remove_tool_section_and_return():
    data = {"tool": {"black": {"line-length": 88}}}
    result = remove_tool_section_and_return(data, "black")
    assert "black" not in result.get("tool", {})


def test_remove_tool_section_and_return_no_change():
    data = {"tool": {"black": {"line-length": 88}}}
    result = remove_tool_section_and_return(data, "ruff")
    assert "black" in result.get("tool", {})

def test_diff_pyproject_config_added():
    old = {"tool": {}}
    new = {
        "tool": {
            "black": {
                "line-length": 88
            }
        }
    }
    diff = diff_pyproject_config(old, new)
    assert ("added", "black", None, {"line-length": 88}) in diff


def test_diff_pyproject_config_added_removed_changed():
    old = {
        "tool": {
            "black": {"line-length": 88},
            "ruff": {"select": ["E", "F"]},
        }
    }

    new = {
        "tool": {
            "black": {"line-length": 120},  # changed
            "isort": {"profile": "black"},  # added
        }
    }

    diffs = diff_pyproject_config(old, new)
    assert ("changed", "black", {"line-length": 88}, {"line-length": 120}) in diffs
    assert ("removed", "ruff", {"select": ["E", "F"]}, None) in diffs
    assert ("added", "isort", None, {"profile": "black"}) in diffs

def test_format_pyproject_diff_plaintext_output():
    diff = [
        ("added", "isort", None, {"profile": "black"}),
        ("removed", "ruff", {"select": ["E"]}, None),
        ("changed", "black", {"line-length": 88}, {"line-length": 100}),
    ]
    result = format_pyproject_diff_plaintext(diff)
    assert "+ [tool.isort]" in result
    assert "+ profile = 'black'" in result
    assert "- [tool.ruff]" in result
    assert "~ [tool.black]" in result
    assert "~ line-length: 88 → 100" in result
