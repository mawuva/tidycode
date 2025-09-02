"""
TidyCode Input Utilities
"""

from typing import List, Optional, Sequence, Union

import questionary
import typer
from questionary import Choice

from .printing import pretty_print


def ask_confirm(message: str) -> bool:
    """
    Prompt a yes/no confirmation and return the answer.
    """
    return questionary.confirm(message).ask()


def ask_text(message: str, default: Optional[str] = None) -> str:
    """
    Prompt the user to enter a text value.
    """
    return questionary.text(message, default=default or "").ask()


def ask_checkbox(
    message: str, choices: List[str], default: str | None = None
) -> List[str]:
    """
    Prompt the user to select multiple choices.
    """
    return questionary.checkbox(message, choices=choices, default=default).ask()


def ask_action(message: str, actions: Optional[List[str]]) -> str:
    """
    Prompt the user to choose an action (like add/edit).

    Args:
        message: The question to display
        actions: List of options (default ['add', 'edit'])

    Returns:
        The selected action as a string.
    """
    choices: Sequence[Union[str, Choice, dict]] = actions or []
    return questionary.select(message, choices=choices).ask()


def ask_choice(prompt: str, choices: list[str]) -> str:
    """Ask the user to choose from a list of options."""
    pretty_print(f"👉 {prompt}", fg=typer.colors.CYAN)
    return ask_action(prompt, choices)
