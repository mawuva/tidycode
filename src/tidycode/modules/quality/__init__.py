"""
Quality module.
"""

from pathlib import Path
from typing import List, Optional

from tidycode.runner.subprocess import run_plugins
from tidycode.runner.types import SubprocessDisplayMode

__all__ = ["run_quality_tools"]


def run_quality_tools(
    tools: Optional[List[str]] = None,
    check_only: bool = False,
    live: bool = False,
    verbose: bool = True,
    summary_display_mode: Optional[SubprocessDisplayMode] = None,
) -> None:
    """
    Run quality tools.

    Args:
        tools: List of tools to run. If None, uses tools from configuration.
        check_only: Whether to run in check-only mode.
        live: Whether to run commands live.
        verbose: Whether to display verbose output.
        summary_display_mode: Display mode for summary.
    """
    run_plugins(
        category="quality",
        tools=tools,
        check_only=check_only,
        live=live,
        verbose=verbose,
        summary_display_mode=summary_display_mode,
    )
