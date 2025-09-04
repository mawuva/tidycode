"""
Run the tools
"""

from typing import List, Optional

import typer

from tidycode.modules.quality import run_quality_tools
from tidycode.runner.types import SubprocessDisplayMode
from tidycode.utils.printing import pretty_print

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
    summary_mode: Optional[SubprocessDisplayMode] = typer.Option(
        SubprocessDisplayMode.TABLE_MINIMAL,
        help="Summary display mode (TABLE_FULL, TABLE_MINIMAL, TEXT, LIST)",
    ),
) -> None:
    """
    Run formatting, linting, and type checking tools (black, isort, ruff, mypy)
    """
    tool_list: Optional[List[str]] = tools.split(",") if tools else None

    pretty_print("🔍 Running selected tools...", fg=typer.colors.CYAN)

    # Execute the tools with automatic summary
    run_quality_tools(
        tools=tool_list,
        check_only=check_only,
        live=live,
        verbose=verbose,
        summary_display_mode=summary_mode,
    )
