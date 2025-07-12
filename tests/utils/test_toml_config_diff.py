"""
Test toml_config_diff.py
"""

from tidycode.utils import diff_configs, format_config_diff


def test_diff_configs_added():
    old = {"tool": {}}
    new = {"tool": {"black": {"line-length": 88}}}
    diff = diff_configs(old, new)
    assert ("added", "black", None, {"line-length": 88}) in diff


def test_diff_configs_added_removed_changed():
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

    diffs = diff_configs(old, new)
    assert ("changed", "black", {"line-length": 88}, {"line-length": 120}) in diffs
    assert ("removed", "ruff", {"select": ["E", "F"]}, None) in diffs
    assert ("added", "isort", None, {"profile": "black"}) in diffs


def test_format_config_diff_plaintext_output():
    diff = [
        ("added", "isort", None, {"profile": "black"}),
        ("removed", "ruff", {"select": ["E"]}, None),
        ("changed", "black", {"line-length": 88}, {"line-length": 100}),
    ]
    result = format_config_diff(diff)
    assert "+ [tool.isort]" in result
    assert "+ profile = 'black'" in result
    assert "- [tool.ruff]" in result
    assert "~ [tool.black]" in result
    assert "~ line-length: 88 → 100" in result
