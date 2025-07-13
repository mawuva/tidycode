"""
Test toml_helpers.py
"""

from tidycode.utils import (
    get_tool_section,
    has_tool_section,
    load_toml_file,
    remove_tool_section,
    remove_tool_section_and_return,
    save_toml_file,
    set_tool_section,
)


def test_load_empty_toml_file(empty_tmp_toml_file):
    data = load_toml_file(empty_tmp_toml_file)
    assert data == {}


def test_save_and_reload(tmp_path):
    path = tmp_path / "pyproject.toml"
    original = {"tool": {"black": {"line-length": 88}}}
    save_toml_file(original, path)
    loaded = load_toml_file(path)
    assert loaded["tool"]["black"]["line-length"] == 88


def test_has_tool_config():
    data = {"tool": {"black": {"line-length": 88}}}
    assert has_tool_section(data, "black") is True
    assert has_tool_section(data, "ruff") is False


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
