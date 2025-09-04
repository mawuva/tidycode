"""
Display module.
"""

from typing import List

import typer
from rich.console import Console
from rich.table import Table

from tidycode.runner.helpers import status_color
from tidycode.runner.types import SubprocessDisplayMode, SubprocessResult
from tidycode.utils.printing import pretty_print

console = Console()


def display_table_full(results: List[SubprocessResult]) -> None:
    """Display results as a Rich Table (full mode)."""
    table = Table(title="TidyCode Execution Summary", show_lines=True)
    table.add_column("Tool", style="bold cyan")
    table.add_column("Category", style="magenta")
    table.add_column("Status", style="bold")
    table.add_column("Summary", style="white")
    table.add_column("Stdout", style="white")
    table.add_column("Stderr", style="red")

    for result in results:
        color = status_color(result.status)
        table.add_row(
            result.display_name,
            result.category or "",
            f"[{color}]{result.status}[/{color}]",
            result.summary or "",
            result.stdout,
            result.stderr,
        )
    console.print(table)


def display_table_minimal(results: List[SubprocessResult]) -> None:
    """Display results as a Rich Table (minimal mode)."""
    table = Table(title="TidyCode Execution Summary", show_lines=False)
    table.add_column("Tool", style="bold cyan")
    table.add_column("Status", style="bold")
    table.add_column("Summary", style="white")

    for result in results:
        color = status_color(result.status)
        table.add_row(
            result.display_name,
            f"[{color}]{result.status}[/{color}]",
            result.summary or "",
        )
    console.print(table)


def display_text_summary(results: List[SubprocessResult]) -> None:
    """Display results as compact text (one line per tool)."""
    for result in results:
        color = status_color(result.status)
        pretty_print(
            f"{result.display_name}: {result.status} | {result.summary or ''}",
            fg=getattr(typer.colors, color.upper()),
        )


def display_list(results: List[SubprocessResult]) -> None:
    """Display results as a colored list (stdout/stderr included)."""
    for result in results:
        color = status_color(result.status)

        pretty_print(
            f"{result.display_name}: {result.status}",
            fg=getattr(typer.colors, color.upper()),
        )
        if result.category:
            pretty_print(result.category, fg=typer.colors.MAGENTA)
        if result.summary:
            pretty_print(result.summary, fg=typer.colors.WHITE)
        if result.details:
            pretty_print(result.details, fg=typer.colors.WHITE)
        if result.stdout:
            pretty_print(result.stdout, fg=typer.colors.WHITE)
        if result.stderr:
            pretty_print(result.stderr, fg=typer.colors.RED)


def print_summary(results: List[SubprocessResult], mode: SubprocessDisplayMode) -> None:
    """Print a summary of results using different display modes."""
    passed = sum(1 for r in results if "✅" in r.status)
    warning = sum(1 for r in results if "⚠️" in r.status)
    failed = sum(1 for r in results if "❌" in r.status)

    if mode == SubprocessDisplayMode.TABLE_FULL:
        display_table_full(results)
    elif mode == SubprocessDisplayMode.TABLE_MINIMAL:
        display_table_minimal(results)
    elif mode == SubprocessDisplayMode.TEXT:
        display_text_summary(results)
    elif mode == SubprocessDisplayMode.LIST:
        display_list(results)
    else:
        raise ValueError(f"Unknown display mode: {mode}")

    console.print(f"\nSummary: ✅ {passed}  ⚠️ {warning}  ❌ {failed}", style="bold")
