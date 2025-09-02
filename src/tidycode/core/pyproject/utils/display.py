"""
Print a summary of a section.
"""

import json
from typing import Any, Dict

import typer
from rich.console import Console
from rich.table import Table

from tidycode.core.pyproject.types import PrintSectionSummaryMode
from tidycode.core.pyproject.utils.helpers import (
    filter_dict,
    get_keys,
    iter_key_values,
)
from tidycode.utils import pretty_print, print_info, print_title

console = Console()


def _print_tree(
    data: dict,
    *,
    show_values: bool,
    hide_sensitive: bool,
    prefix: str = "",
    is_last: bool = True,
    indent_size: int = 2,
) -> None:
    """
    Print a tree of the section data.

    Args:
        data: The section data.
        show_values: Whether to show values.
        hide_sensitive: Whether to hide sensitive keys.
        prefix: The prefix to use for the tree.
        is_last: Whether the current item is the last in the list.
        indent_size: The size of the indentation.
    """

    items = list(data.items())
    last_index = len(items) - 1

    for i, (key, value) in enumerate(items):
        branch = "└─" if i == last_index else "├─"
        current_prefix = f"{prefix}{branch} "

        if isinstance(value, dict):
            print_title(
                f"{current_prefix}{key}:", newline_after=False, padding=indent_size
            )
            next_prefix = f"{prefix}{'   ' if i == last_index else '│  '}"
            _print_tree(
                value,
                show_values=show_values,
                hide_sensitive=hide_sensitive,
                prefix=next_prefix,
                is_last=(i == last_index),
            )
        else:
            text = f"{current_prefix}{key}"
            if show_values:
                text += f": {value}"
            pretty_print(
                text,
                fg=typer.colors.BLUE,
                newline_before=False,
                newline_after=False,
                padding=indent_size,
            )


def _print_list(data: dict, *, show_values: bool, hide_sensitive: bool) -> None:
    """Print a list of the section data.

    Args:
        data (dict): The section data.
        show_values (bool): Whether to show values.
        hide_sensitive (bool): Whether to hide sensitive keys.
    """
    for path, key, value in iter_key_values(data, hide_sensitive=hide_sensitive):
        if show_values:
            pretty_print(f"- {path} → {value}", fg=typer.colors.BLUE)
        else:
            pretty_print(f"- {path}", fg=typer.colors.BLUE)


def _print_table(data: dict, *, show_values: bool, hide_sensitive: bool) -> None:
    """Print a table of the section data.

    Args:
        data (dict): The section data.
        show_values (bool): Whether to show values.
        hide_sensitive (bool): Whether to hide sensitive keys.
    """
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Path", style="cyan")

    if show_values:
        table.add_column("Value", style="blue")

    for path, key, value in iter_key_values(data, hide_sensitive=hide_sensitive):
        if show_values:
            table.add_row(path, str(value))
        else:
            table.add_row(path)

    console.print(table)


def _print_json(data: dict, *, show_values: bool, hide_sensitive: bool) -> None:
    """Pretty-print section as JSON (respecting show_values & hide_sensitive)."""
    filtered = filter_dict(data, hide_sensitive=hide_sensitive, show_values=show_values)
    pretty_print(
        json.dumps(filtered, indent=2, ensure_ascii=False), newline_before=True
    )


def print_section_summary(
    section_name: str,
    data: Dict[str, Any],
    *,
    display_content: bool = True,
    mode: PrintSectionSummaryMode = PrintSectionSummaryMode.TREE,
    show_values: bool = True,
    hide_sensitive: bool = True,
    indent_size: int = 2,
) -> None:
    """
    Print a summary of a section in different formats (tree, list, or table).

    Args:
        section_name: Name of the section.
        data: Section data (dict).
        display_content: Whether to display the content of the section.
        mode: Display mode: PrintSectionSummaryMode.TREE, PrintSectionSummaryMode.LIST, or PrintSectionSummaryMode.TABLE.
        show_values: Whether to display values alongside keys.
        hide_sensitive: Whether to hide sensitive keys/paths.
        indent_size: Indentation size (tree mode only).
    """
    if not data:
        print_info(f"Section '{section_name}' is empty.")
        return

    keys = get_keys(data, hide_sensitive=hide_sensitive)
    print_info(
        f"Section '{section_name}' contains {len(keys)} keys:", newline_before=True
    )

    if display_content:
        if mode == PrintSectionSummaryMode.TREE:
            _print_tree(
                data,
                show_values=show_values,
                hide_sensitive=hide_sensitive,
                indent_size=indent_size,
            )
        elif mode == PrintSectionSummaryMode.LIST:
            _print_list(data, show_values=show_values, hide_sensitive=hide_sensitive)
        elif mode == PrintSectionSummaryMode.TABLE:
            _print_table(data, show_values=show_values, hide_sensitive=hide_sensitive)
        elif mode == PrintSectionSummaryMode.JSON:
            _print_json(data, show_values=show_values, hide_sensitive=hide_sensitive)
        else:
            raise ValueError(f"Unknown mode: {mode.value}")
