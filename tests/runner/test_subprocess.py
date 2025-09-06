"""
TidyCode Runner Subprocess Tests
"""

from unittest import mock

from tidycode.runner.subprocess import run_multiple_commands
from tidycode.runner.types import CommandSpec, SubprocessDisplayMode

# ---------------------------
# Unit tests
# ---------------------------


# ---------------------------
# Integration tests
# ---------------------------


def test_run_multiple_commands_success():
    """
    Scenario:
        Run multiple successful commands.

    Expected:
        All commands execute and return results.
    """
    commands = [
        CommandSpec(
            command=["echo", "hello"],
            display_name="echo1",
            cwd=None,
            is_tool=True,
        ),
        CommandSpec(
            command=["echo", "world"],
            display_name="echo2",
            cwd=None,
            is_tool=True,
        ),
    ]

    results = run_multiple_commands(
        commands=commands,
        live=False,
        verbose=False,
        summary_display_mode=None,
    )

    assert (
        results is not None
    )  # run_multiple_commands returns results when no display mode
    assert len(results) == 2


def test_run_multiple_commands_mixed_results():
    """
    Scenario:
        Run multiple commands with mixed success/failure.

    Expected:
        Commands execute and results are processed.
    """
    commands = [
        CommandSpec(
            command=["echo", "hello"],
            display_name="echo",
            cwd=None,
            is_tool=True,
        ),
        CommandSpec(
            command=["false"],
            display_name="false",
            cwd=None,
            is_tool=True,
        ),
    ]

    results = run_multiple_commands(
        commands=commands,
        live=False,
        verbose=False,
        summary_display_mode=SubprocessDisplayMode.TEXT,
    )

    assert results is None  # run_multiple_commands returns None


def test_run_multiple_commands_live_mode():
    """
    Scenario:
        Run multiple commands in live mode.

    Expected:
        Commands execute in live mode.
    """
    commands = [
        CommandSpec(
            command=["echo", "hello"],
            display_name="echo",
            cwd=None,
            is_tool=True,
        ),
    ]

    results = run_multiple_commands(
        commands=commands,
        live=True,
        verbose=False,
        summary_display_mode=None,
    )

    assert (
        results is not None
    )  # run_multiple_commands returns results when no display mode
    assert len(results) == 1


def test_run_multiple_commands_with_cwd(tmp_path):
    """
    Scenario:
        Run multiple commands with specific working directory.

    Expected:
        Commands execute in the specified directory.
    """
    # Create test files
    test_file1 = tmp_path / "file1.txt"
    test_file2 = tmp_path / "file2.txt"
    test_file1.write_text("content1")
    test_file2.write_text("content2")

    commands = [
        CommandSpec(
            command=["ls", "file1.txt"],
            display_name="ls1",
            cwd=tmp_path,
            is_tool=True,
        ),
        CommandSpec(
            command=["ls", "file2.txt"],
            display_name="ls2",
            cwd=tmp_path,
            is_tool=True,
        ),
    ]

    results = run_multiple_commands(
        commands=commands,
        live=False,
        verbose=False,
        summary_display_mode=SubprocessDisplayMode.TABLE_MINIMAL,
    )

    assert results is None  # run_multiple_commands returns None


def test_run_multiple_commands_empty_list():
    """
    Scenario:
        Run multiple commands with empty command list.

    Expected:
        No commands are executed.
    """
    results = run_multiple_commands(
        commands=[],
        live=False,
        verbose=False,
        summary_display_mode=None,
    )

    assert results == []  # run_multiple_commands returns empty list when no commands


def test_run_multiple_commands_different_display_modes():
    """
    Scenario:
        Run commands with different display modes.

    Expected:
        Commands execute with appropriate display modes.
    """
    commands = [
        CommandSpec(
            command=["echo", "hello"],
            display_name="echo",
            cwd=None,
            is_tool=True,
        ),
    ]

    # Test all display modes
    modes = [
        SubprocessDisplayMode.TABLE_FULL,
        SubprocessDisplayMode.TABLE_MINIMAL,
        SubprocessDisplayMode.TEXT,
        SubprocessDisplayMode.LIST,
    ]

    for mode in modes:
        results = run_multiple_commands(
            commands=commands,
            live=False,
            verbose=False,
            summary_display_mode=mode,
        )
        assert results is None  # run_multiple_commands returns None


def test_run_multiple_commands_verbose():
    """
    Scenario:
        Run multiple commands with verbose output.

    Expected:
        Commands execute with verbose output.
    """
    commands = [
        CommandSpec(
            command=["echo", "hello"],
            display_name="echo",
            cwd=None,
            is_tool=True,
        ),
    ]

    with mock.patch("tidycode.runner.executor.pretty_print") as mock_print:
        results = run_multiple_commands(
            commands=commands,
            live=False,
            verbose=True,
            summary_display_mode=None,
        )

        assert (
            results is not None
        )  # run_multiple_commands returns results when no display mode
        assert len(results) == 1
        # Should have called pretty_print for verbose output
        assert mock_print.called


def test_run_multiple_commands_with_tool_and_non_tool():
    """
    Scenario:
        Run commands with both tool and non-tool commands.

    Expected:
        Commands execute with appropriate status handling.
    """
    commands = [
        CommandSpec(
            command=["echo", "hello"],
            display_name="echo",
            cwd=None,
            is_tool=True,
        ),
        CommandSpec(
            command=["echo", "world"],
            display_name="echo",
            cwd=None,
            is_tool=False,
        ),
    ]

    results = run_multiple_commands(
        commands=commands,
        live=False,
        verbose=False,
        summary_display_mode=SubprocessDisplayMode.TEXT,
    )

    assert results is None  # run_multiple_commands returns None
