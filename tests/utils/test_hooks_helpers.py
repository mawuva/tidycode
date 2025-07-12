"""
Test hooks helpers.
"""

import pytest
from tidycode.utils import (
    get_installed_hook_keys,
    add_hooks,
    remove_hooks,
    HOOKS
)

@pytest.fixture
def empty_config():
    return {"repos": []}

@pytest.fixture
def config_with_hooks():
    return {
        "repos": [
            HOOKS["linting"]["yaml"],
            HOOKS["format_black"]["yaml"]
        ]
    }

def test_get_installed_hook_keys_with_hooks(config_with_hooks):
    installed_keys = get_installed_hook_keys(config_with_hooks)
    assert "linting" in installed_keys
    assert "format_black" in installed_keys

def test_get_installed_hook_keys_empty(empty_config):
    installed_keys = get_installed_hook_keys(empty_config)
    assert installed_keys == []

def test_add_hooks_to_empty_config(empty_config):
    updated_config = add_hooks(empty_config.copy(), ["linting"])
    assert updated_config["repos"][-1] == HOOKS["linting"]["yaml"]

def test_add_hooks_avoids_duplicates(config_with_hooks):
    updated = add_hooks(config_with_hooks.copy(), ["linting", "format_black"])
    assert len(updated["repos"]) == 2  # unchanged

def test_add_hooks_with_unknown_key_raises(empty_config):
    with pytest.raises(KeyError):
        add_hooks(empty_config, ["unknown"])

def test_remove_hooks(config_with_hooks):
    updated = remove_hooks(config_with_hooks.copy(), ["linting"])
    assert all(r["repo"] != HOOKS["linting"]["yaml"]["repo"] for r in updated["repos"])

def test_remove_hooks_skips_missing(empty_config):
    updated = remove_hooks(empty_config.copy(), ["linting"])
    assert updated == empty_config

def test_add_and_then_remove(empty_config):
    config = add_hooks(empty_config.copy(), ["linting", "format_black"])
    config = remove_hooks(config, ["format_black"])
    remaining_repos = [r["repo"] for r in config["repos"]]
    assert HOOKS["linting"]["yaml"]["repo"] in remaining_repos
    assert HOOKS["format_black"]["yaml"]["repo"] not in remaining_repos
