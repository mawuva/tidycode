"""
Test hooks_helpers.py
"""

from tidycode.utils import (
    load_config,
    save_config,
    get_installed_hook_keys,
    add_hooks,
    remove_hooks,
)

def test_load_config_empty(temp_config_file):
    loaded = load_config(temp_config_file)
    assert loaded == {"repos": []}

def test_load_and_save_config(temp_config_file, orig_config):
    save_config(orig_config, temp_config_file)
    loaded = load_config(temp_config_file)
    assert loaded == orig_config

def test_get_installed_hook_keys(temp_config_file, orig_config_with_hooks):
    save_config(orig_config_with_hooks, temp_config_file)
    installed_keys = get_installed_hook_keys(orig_config_with_hooks)
    assert installed_keys == ["linting", "format_black"]

def test_get_installed_hook_keys_empty(temp_config_file, orig_config):
    save_config(orig_config, temp_config_file)
    installed_keys = get_installed_hook_keys(orig_config)
    assert installed_keys == []

def test_add_hooks(temp_config_file, orig_config):
    save_config(orig_config, temp_config_file)
    config = add_hooks(orig_config, ["linting", "format_black"])
    assert config == orig_config

def test_add_hooks_empty(temp_config_file, orig_config):
    save_config(orig_config, temp_config_file)
    config = add_hooks(orig_config, [])
    assert config == orig_config

def test_remove_hooks(temp_config_file, orig_config_with_hooks):
    save_config(orig_config_with_hooks, temp_config_file)
    config = remove_hooks(orig_config_with_hooks, ["linting", "format_black"])
    assert config == orig_config_with_hooks

def test_add_and_remove_hooks(temp_config_file, orig_config_with_hooks):
    save_config(orig_config_with_hooks, temp_config_file)
    config = add_hooks(orig_config_with_hooks, ["linting", "format_black"])
    assert config == orig_config_with_hooks
    config = remove_hooks(orig_config_with_hooks, ["linting", "format_black"])
    assert config == orig_config_with_hooks