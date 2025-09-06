"""
Subprocess runner.
"""

from pathlib import Path
from typing import List, Optional

from tidycode.core.pyproject.utils.helpers import load_tidycode_config
from tidycode.plugins import load_plugins_from, registry
from tidycode.plugins.base import BasePlugin
from tidycode.plugins.runner.base_runner import BaseRunner
from tidycode.utils.printing import print_warning

from .display import print_summary
from .executor import run_command, run_command_live
from .types import CommandSpec, SubprocessDisplayMode, SubprocessResult


def run_multiple_commands(
    commands: List[CommandSpec],
    live: bool = False,
    verbose: bool = False,
    summary_display_mode: Optional[SubprocessDisplayMode] = None,
) -> List[SubprocessResult] | None:
    """
    Run multiple commands sequentially.

    Args:
        commands: list of commands to run
        live: run the commands live
        verbose: display the outputs
        summary_display_mode: display mode
    Returns:
        List of standardized results or None if summary_display_mode is provided
    """
    results: List[SubprocessResult] = []

    for spec in commands:
        cmd: List[str] = spec.command
        display_name: Optional[str] = spec.display_name
        cwd: Optional[Path] = spec.cwd
        is_tool: bool = spec.is_tool

        if live:
            result = run_command_live(
                command=cmd, display_name=display_name, cwd=cwd, is_tool=is_tool
            )
        else:
            result = run_command(
                command=cmd,
                display_name=display_name,
                cwd=cwd,
                verbose=verbose,
                is_tool=is_tool,
            )

        results.append(result)

    if summary_display_mode:
        print_summary(results, summary_display_mode)
        return None

    return results


def run_plugins(
    category: Optional[str] = None,
    scope: Optional[str] = None,
    tools: Optional[List[str]] = None,
    path: Optional[Path] = None,
    check_only: bool = False,
    live: bool = False,
    verbose: bool = True,
    dry_run: bool = False,
    summary_display_mode: Optional[SubprocessDisplayMode] = None,
) -> None:
    """
    Run plugins.
    """

    configs: dict = load_tidycode_config()
    commands_to_run: List[CommandSpec] = []

    target: Path = Path(path or configs.get("target", "."))
    config_check_only: bool = configs.get("check_only", check_only)
    tools = configs.get("tools", []) if tools is None else tools

    load_plugins_from(f"tidycode.modules.{category}")

    # Build filter criteria, only including non-None values
    filter_criteria = {"type": "runner"}
    if category is not None:
        filter_criteria["category"] = category
    if scope is not None:
        filter_criteria["scope"] = scope

    plugins: List[BasePlugin] = registry.filter(**filter_criteria)

    # Get the tools to run
    for tool_name in tools:
        tool = next((p for p in plugins if p.meta.name == tool_name), None)

        if not tool:
            print_warning(f"Tool {tool_name} not found")
            continue

        if isinstance(tool, BaseRunner):
            # If dry run, run the tool and continue
            if dry_run:
                tool.run(
                    target=target,
                    check_only=config_check_only,
                    dry_run=True,
                    live=live,
                    verbose=verbose,
                )
                continue

            # Otherwise, add the command to the list of commands to run
            commands_to_run.append(
                tool.get_command_spec(target=target, check_only=config_check_only)
            )

    # Run the commands if not dry run and there are commands to run
    if not dry_run and commands_to_run:
        run_multiple_commands(
            commands=commands_to_run,
            live=live,
            verbose=verbose,
            summary_display_mode=summary_display_mode
            or (
                # Determine the summary display mode if not provided
                SubprocessDisplayMode.TABLE_MINIMAL
                if live
                else SubprocessDisplayMode.TABLE_FULL
            ),
        )
