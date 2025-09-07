"""
Run the tools
"""

from typing import List, Optional

import typer

from tidycode.runner.subprocess import run_plugins
from tidycode.runner.types import SubprocessDisplayMode
from tidycode.utils.printing import pretty_header
from tidycode.settings import PrettyHeaderStyle

app = typer.Typer(
    help="Run formatting, linting, and type checking tools (black, isort, ruff, mypy)",
    no_args_is_help=True,
)


@app.command(name="check")
def check_quality(
    tools: Optional[str] = typer.Option(
        None, help="Comma-separated list of tools to run"
    ),
    check_only: bool = typer.Option(
        False, "--check-only", "-c", help="Run tools in check-only mode"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed output"),
    live: bool = typer.Option(True, "--live", "-l", help="Stream outputs live"),
    mode: Optional[SubprocessDisplayMode] = typer.Option(
        SubprocessDisplayMode.TABLE_MINIMAL,
        "--mode",
        "-m",
        help="Summary display mode (TABLE_FULL, TABLE_MINIMAL, TEXT, LIST)",
    ),
) -> None:
    """
    Run formatting, linting, and type checking tools (black, isort, ruff, mypy) with automatic summary
    """
    tool_list: Optional[List[str]] = tools.split(",") if tools else None

    pretty_header("quality", "Running quality checks...", style=PrettyHeaderStyle.BANNER, err=True)

    run_plugins(
        category="quality",
        tools=tool_list,
        check_only=check_only,
        live=live,
        verbose=verbose,
        summary_display_mode=mode,
    )


@app.command(name="style", help="Perform code style checking")
def style_quality(
    tools: Optional[str] = typer.Option(
        None, help="Comma-separated list of tools to run"
    ),
    check_only: bool = typer.Option(
        False, "--check-only", "-c", help="Run tools in check-only mode"
    ),
    live: bool = typer.Option(True, "--live", "-l", help="Stream outputs live"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed output"),
    mode: Optional[SubprocessDisplayMode] = typer.Option(
        SubprocessDisplayMode.TABLE_MINIMAL,
        "--mode",
        "-m",
        help="Summary display mode (TABLE_FULL, TABLE_MINIMAL, TEXT, LIST)",
    ),
) -> None:
    """
    Run style checking tools (black, isort, ruff) with automatic summary
    """

    tool_list: Optional[List[str]] = (
        tools.split(",") if tools else ["black", "isort", "ruff"]
    )

    pretty_header(
        scope="style", message="Running style checks...", style=PrettyHeaderStyle.BANNER, err=True
    )

    run_plugins(
        category="quality",
        scope="style",
        tools=tool_list,
        check_only=check_only,
        live=live,
        verbose=verbose,
        summary_display_mode=mode,
    )


@app.command(name="type", help="Perform type checking")
def run_type_checking(
    tools: Optional[str] = typer.Option(
        None, help="Comma-separated list of tools to run"
    ),
    check_only: bool = typer.Option(
        False, "--check-only", "-c", help="Run tools in check-only mode"
    ),
    live: bool = typer.Option(True, "--live", "-l", help="Stream outputs live"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed output"),
    mode: Optional[SubprocessDisplayMode] = typer.Option(
        SubprocessDisplayMode.TABLE_MINIMAL,
        "--mode",
        "-m",
        help="Summary display mode (TABLE_FULL, TABLE_MINIMAL, TEXT, LIST)",
    ),
) -> None:
    """
    Run type checking tools (mypy) with automatic summary
    """

    tool_list: Optional[List[str]] = tools.split(",") if tools else ["mypy"]

    pretty_header(
        scope="type", message="Running type checking...", style=PrettyHeaderStyle.BANNER, err=True
    )

    run_plugins(
        category="quality",
        scope="type",
        tools=tool_list,
        check_only=check_only,
        live=live,
        verbose=verbose,
        summary_display_mode=mode,
    )
