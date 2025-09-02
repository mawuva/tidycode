"""
Interactive CLI prompts for pyproject.toml key/value management.

This module provides functions to interactively prompt the user
to add, edit, or remove keys in a pyproject.toml section. It
handles global actions, key-by-key prompts, fixed-count key
inputs, and displays summaries of sections.

It integrates with a ChangeLog to capture and display changes
made during the interactive session.

Functions:
- prompt_global_action()
- prompt_key_action(key, current_value)
- prompt_key_values(existing=None, mode=Mode.FULL)
- print_section_summary(section_name, data)
"""

from typing import Dict, Optional

from tidycode.settings import YesNo
from tidycode.core.pyproject.types import GlobalActions, Mode
from tidycode.core.pyproject.utils.key_actions import handle_key_action
from tidycode.utils import (
    ask_action,
    ask_text,
    pretty_print,
    print_error,
    print_info,
    print_title,
    print_warning,
)


def prompt_global_action() -> str:
    """Ask the user for the global action (add / edit / nothing)."""
    pretty_print("👉 Choose an action:", fg="cyan", bold=True)
    return ask_action("Action:", GlobalActions.to_list())


def prompt_key_values(
    existing: Optional[Dict[str, str]] = None, mode: Mode = Mode.FULL
) -> Dict[str, str]:
    """
    Prompt the user to add, edit, remove, or skip key/value input interactively.

    Args:
        existing (dict, optional): Existing key/value pairs to check for conflicts.
        mode (str): "add" = only add new keys, "full" = allow edit/remove existing keys.

    Returns:
        dict: Updated key/value pairs.
    """

    data = existing.copy() if existing else {}

    while True:
        if mode == Mode.ADD:
            GlobalActions.ADD_KEYS
        else:
            action_str = prompt_global_action()
            if action_str == GlobalActions.EXIT:
                break
            GlobalActions.from_value(action_str)

        raw_count = ask_text(
            "How many keys do you want to add/edit/remove? (leave empty to enter keys one by one) :"
        ).strip()

        if raw_count == "":
            # Mode "keys one by one"
            while True:
                key = ask_text("Enter the key name (leave empty to stop):").strip()
                if not key:
                    print_info("Stopping key input.")
                    break
                handle_key_action(key, data, mode)

        else:
            # Mode with fixed number
            try:
                number_of_keys = int(raw_count)
            except ValueError:
                print_error(
                    "Invalid number, please enter a valid integer or leave empty."
                )
                continue

            if number_of_keys <= 0:
                print_warning("No keys to add/edit/remove.")
                break

            for i in range(number_of_keys):
                print_title(f"🔑 Key {i+1} / {number_of_keys}:")
                key = ask_text("Enter the key name:").strip()

                if not key:
                    print_warning("Empty key skipped.")
                    continue

                handle_key_action(key, data, mode)

        # Exit condition for add mode
        if mode == Mode.ADD:
            more = ask_action("Do you want to add more keys?", YesNo.to_list())
            if more == YesNo.NO:
                break

    return data
