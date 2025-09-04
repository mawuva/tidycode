"""
Subprocess runner.
"""

import subprocess
from pathlib import Path
from typing import List, Optional

import typer

from tidycode.utils.printing import pretty_print, print_error, print_success

from .helpers import build_result, handle_exception
from .types import SubprocessResult


def run_command(
    command: str,
    display_name: Optional[str] = None,
    cwd: Optional[Path] = None,
    verbose: bool = False,
    is_tool: bool = True,
) -> SubprocessResult:
    """
    Run a command and return a standardized result.

    Args:
        command: list of the command
        display_name: name of the tool
        cwd: current working directory
        verbose: display the outputs
        is_tool: if the command is a tool
    Returns:
        SubprocessResult: standardized result
    """

    display_name = display_name or (command[0] if command else "<cmd>")

    if verbose:
        pretty_print(
            f"🔍 Running command: {' '.join(command)}", fg=typer.colors.YELLOW, err=True
        )

    try:
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            cwd=cwd,
            encoding="utf-8",
            errors="replace",
        )

        result = build_result(
            display_name,
            process.returncode,
            process.stdout,
            process.stderr,
            is_tool=is_tool,
        )

        if verbose:
            if result.stdout:
                pretty_print(result.stdout, fg=typer.colors.BRIGHT_WHITE, err=True)
            if result.stderr:
                pretty_print(result.stderr, fg=typer.colors.BRIGHT_WHITE, err=True)

            pretty_print(
                result.display_name + ": " + result.status,
                fg=typer.colors.GREEN if process.returncode == 0 else typer.colors.RED,
                err=True,
            )

        return result
    except Exception as e:
        return handle_exception(e, display_name, is_tool=is_tool, verbose=verbose)


def run_command_live(
    command: List[str],
    display_name: Optional[str] = None,
    cwd: Optional[Path] = None,
    is_tool: bool = True,
) -> SubprocessResult:
    """
    Run a command and print the outputs live.

    Args:
        command: list of the command
        display_name: name of the tool
        cwd: current working directory
        is_tool: if the command is a tool
    Returns:
        SubprocessResult: standardized result
    """

    display_name = display_name or (command[0] if command else "<cmd>")

    pretty_print(
        f"🔍 Running command: {' '.join(command)}", fg=typer.colors.YELLOW, err=True
    )

    try:
        process = subprocess.Popen(
            command,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",  # force UTF-8
            errors="replace",  # replace invalid characters
        )

        assert process.stdout is not None

        for line in process.stdout:
            typer.echo(line, nl=False)

        process.wait()

        result = build_result(display_name, process.returncode, "", "", is_tool)

        if process.returncode == 0:
            print_success(
                f"{display_name}: {result.status} (exit {process.returncode})"
            )
        else:
            print_error(f"{display_name}: {result.status} (exit {process.returncode})")

        return result
    except Exception as e:
        print_error(f"Error running command: {' '.join(command)}", err=True)
        return handle_exception(e, display_name, is_tool=is_tool, verbose=True)
