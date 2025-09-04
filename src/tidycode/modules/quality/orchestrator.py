"""
Orchestrator for quality tools.
"""

from pathlib import Path
from typing import List, Optional

from tidycode.core.pyproject.utils.helpers import load_tidycode_config
from tidycode.plugins import BasePlugin, load_plugins_from, registry
from tidycode.runner import CommandSpec, SubprocessDisplayMode, run_multiple_commands
from tidycode.utils import print_warning


def run_quality_tools(
    tools: Optional[List[str]] = None,
    check_only: bool = False,
    live: bool = False,
    verbose: bool = True,
    summary_display_mode: Optional[SubprocessDisplayMode] = None,
) -> None:
    """
    Run quality tools.
    """

    configs: dict = load_tidycode_config()
    commands_to_run: List[CommandSpec] = []

    target: Path = configs.get("target", ".")
    check_only: bool = configs.get("check_only", check_only)
    tools = configs.get("tools", []) if tools is None else tools

    load_plugins_from("tidycode.modules.quality")

    plugins: List[BasePlugin] = registry.by_category("quality")

    for tool_name in tools:
        if tool_name not in [p.meta.name for p in plugins]:
            print_warning(f"Tool {tool_name} not found")
            continue

        tool = next(p for p in plugins if p.meta.name == tool_name)

        if tool:
            commands_to_run.append(
                CommandSpec(
                    command=tool.build_command(target, check_only),
                    tool_name=tool_name,
                    cwd=target,
                    is_tool=tool.is_tool(),
                )
            )

    # Determine the summary display mode
    if summary_display_mode is None:
        summary_display_mode = (
            SubprocessDisplayMode.TABLE_MINIMAL
            if live
            else SubprocessDisplayMode.TABLE_FULL
        )

    run_multiple_commands(
        commands=commands_to_run,
        live=live,
        verbose=verbose,
        summary_display_mode=summary_display_mode,
    )
