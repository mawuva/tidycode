"""
Test hooks_helpers.py
"""

from tidycode.utils import (
    load_config,
    save_config,
    get_installed_hook_keys,
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
