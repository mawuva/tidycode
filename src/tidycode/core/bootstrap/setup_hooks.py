"""
Run hooks
"""

from pathlib import Path
from typing import Callable, Optional
from tidycode.utils import (
    HOOKS,
    load_config,
    get_installed_hook_keys,
    add_hooks,
    remove_hooks,
    save_config,
    ask_checkbox,
    run_command,
    ask_confirm,
)

def setup_hooks(
    ask_checkbox_fn: Callable = None,
    run_command_fn: Callable = None,
    config_path: Optional[Path] = None,
) -> None:
    ask_checkbox_fn = ask_checkbox_fn or ask_checkbox
    run_command_fn = run_command_fn or run_command

    config = load_config(config_path)
    installed_keys = get_installed_hook_keys(config)

    if installed_keys:
        to_remove = ask_checkbox_fn(
            "❌ Select hooks to REMOVE (uncheck all to skip):",
            [(key, HOOKS[key]["name"]) for key in installed_keys],
        )
        if to_remove:
            config = remove_hooks(config, to_remove)
            print(f"🗑️ Removed hooks: {[HOOKS[k]['name'] for k in to_remove]}")

    to_add = ask_checkbox_fn(
        "✅ Select hooks to ADD (uncheck all to skip):",
        [(k, v["name"]) for k, v in HOOKS.items() if "yaml" in v],
    )
    if to_add:
        config = add_hooks(config, to_add)
        print(f"➕ Added hooks: {[HOOKS[k]['name'] for k in to_add]}")

    save_config(config, config_path)
    print("✅ .pre-commit-config.yaml updated.")

    if ask_checkbox_fn("Run `pre-commit autoupdate`?", [("yes", "Yes")]):
        run_command_fn(["pre-commit", "autoupdate"])


def setup_hooks_minimal(
    config_path: Optional[Path] = None,
    run_command_fn: Callable = None,
    ask_confirm_fn: Callable = None,
) -> None:
    run_command_fn = run_command_fn or run_command
    ask_confirm_fn = ask_confirm_fn or ask_confirm

    config = load_config(config_path)

    keys_to_add = [k for k in HOOKS if "yaml" in HOOKS[k]]
    config = add_hooks(config, keys_to_add)
    save_config(config, config_path)

    print("✅ All hooks added to .pre-commit-config.yaml.")
    
    if ask_confirm_fn("Run `pre-commit autoupdate` now?"):
        run_command_fn(["pre-commit", "autoupdate"])
        print("🔄 Hooks updated.")

