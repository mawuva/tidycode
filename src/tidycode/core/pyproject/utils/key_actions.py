"""
Functions to handle key actions for the pyproject module.
"""

from typing import Any, Dict

from tidycode.core.pyproject.types import KeyActions, Mode
from tidycode.core.pyproject.utils.helpers import get_keys
from tidycode.utils import (
    ask_action,
    ask_choice,
    ask_text,
    print_success,
    print_warning,
)


def handle_key_creation(key: str, data: Dict[str, str]) -> None:
    """Handle the creation of a new key."""
    value = ask_text(f"Enter value for '{key}':")
    data[key] = value
    print_success(f"Key '{key}' added with value '{value}'")


def handle_key_edition(key: str, data: Dict[str, str]) -> None:
    """Handle the edit action for a given key."""
    value = ask_text(f"Enter new value for '{key}':", default=str(data[key]))
    data[key] = value
    print_success(f"Key '{key}' updated to '{value}'")


def handle_key_deletion(key: str, data: Dict[str, str]) -> None:
    """Handle the deletion of a given key."""
    del data[key]
    print_success(f"Key '{key}' removed.")


def handle_key_action_full_mode(key: str, data: Dict[str, str]) -> None:
    """Handle key actions in full mode."""

    key_action = ask_action(
        f"Key '{key}' already exists with value '{data[key]}'. What do you want to do?",
        KeyActions.to_list(),
    )

    if key_action == KeyActions.EDIT:
        handle_key_edition(key, data)

    elif key_action == KeyActions.REMOVE:
        handle_key_deletion(key, data)
    else:  # skip
        print_warning(f"⚠️ Skipping key '{key}'")


def handle_key_action(key: str, data: Dict[str, str], mode: Mode) -> None:
    """
    Handle add/edit/remove/skip logic for a given key.

    Args:
        key (str): Key name to process.
        data (dict): Existing key/value pairs (mutated in place).
        mode (Mode): Mode for the CLI (add / edit / remove / full).
    """
    if key in data:
        if mode == Mode.ADD:
            print_warning(f"⚠️ Key '{key}' already exists, skipping.")
            return

        if mode == Mode.EDIT:
            handle_key_edition(key, data)
            return

        if mode == Mode.REMOVE:
            handle_key_deletion(key, data)
            return

        handle_key_action_full_mode(key, data)
    else:
        handle_key_creation(key, data)


def select_and_handle_section_keys(
    section_data: Dict[str, Any], mode: Mode, hide_sensitive: bool = True
):
    keys_list = get_keys(section_data, hide_sensitive=hide_sensitive)

    if not keys_list:
        print_warning("No keys available.")
        return

    else:
        key_to_handle = ask_choice("Select a key:", keys_list)

    if mode == Mode.FULL:
        key_action = ask_action(
            f"Key '{key_to_handle}' exists with value '{section_data[key_to_handle]}'. What do you want to do?",
            KeyActions.to_list(),
        )

        if key_action == KeyActions.EDIT:
            handle_key_edition(key_to_handle, section_data)

        elif key_action == KeyActions.REMOVE:
            handle_key_deletion(key_to_handle, section_data)

        else:
            print_warning(f"Skipping key '{key_to_handle}'.")

    else:
        handle_key_action(key_to_handle, section_data, mode)
