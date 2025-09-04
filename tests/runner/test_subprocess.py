"""
TidyCode Runner Subprocess Tests
"""

from unittest import mock

from tidycode.runner.subprocess import (
    run_command,
    run_command_live,
    run_multiple_commands,
)
from tidycode.runner.types import CommandSpec, SubprocessDisplayMode, SubprocessResult

# ---------------------------
# Unit tests
# ---------------------------


def test_run_command_success():
    """
    Scenario:
        Run a successful command.

    Expected:
        Returns SubprocessResult with success status.
    """
    result = run_command(["echo", "hello"], display_name="test", verbose=False)

    assert isinstance(result, SubprocessResult)
    assert result.display_name == "test"
    assert "✅" in result.status or "Passed" in result.status
    assert "hello" in result.stdout


def test_run_command_failure():
    """
    Scenario:
        Run a failing command.

    Expected:
        Returns SubprocessResult with failure status.
    """
    result = run_command(["false"], display_name="test", verbose=False)

    assert isinstance(result, SubprocessResult)
    assert result.display_name == "test"
    assert "❌" in result.status or "Failed" in result.status


def test_run_command_not_found():
    """
    Scenario:
        Run a command that doesn't exist.

    Expected:
        Returns SubprocessResult with error status.
    """
    result = run_command(
        ["nonexistent_command_12345"], display_name="test", verbose=False
    )

    assert isinstance(result, SubprocessResult)
    assert result.display_name == "test"
    assert "❌" in result.status or "Failed" in result.status
    assert "Command not found" in result.stderr or "not found" in result.stderr


def test_run_command_with_cwd(tmp_path):
    """
    Scenario:
        Run a command with a specific working directory.

    Expected:
        Command runs in the specified directory.
    """
    # Create a test file in the temp directory
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")

    # Run ls command in the temp directory
    result = run_command(
        ["ls", "test.txt"], display_name="test", cwd=tmp_path, verbose=False
    )

    assert isinstance(result, SubprocessResult)
    assert "test.txt" in result.stdout


def test_run_command_verbose():
    """
    Scenario:
        Run a command with verbose output.

    Expected:
        Command runs and verbose output is handled.
    """
    with mock.patch("tidycode.runner.subprocess.pretty_print") as mock_print:
        result = run_command(["echo", "hello"], display_name="test", verbose=True)

        assert isinstance(result, SubprocessResult)
        # pretty_print is called multiple times in verbose mode
        assert mock_print.call_count >= 1


def test_run_command_default_display_name():
    """
    Scenario:
        Run a command without specifying display_name.

    Expected:
        Uses the command name as display_name.
    """
    result = run_command(["echo", "hello"], verbose=False)

    assert isinstance(result, SubprocessResult)
    assert result.display_name == "echo"


def test_run_command_live_success():
    """
    Scenario:
        Run a successful command in live mode.

    Expected:
        Returns SubprocessResult with success status.
    """
    result = run_command_live(["echo", "hello"], display_name="test")

    assert isinstance(result, SubprocessResult)
    assert result.display_name == "test"
    assert "✅" in result.status or "Passed" in result.status
    # run_command_live doesn't capture stdout in the result, it displays it live
    assert result.stdout == ""


def test_run_command_live_failure():
    """
    Scenario:
        Run a failing command in live mode.

    Expected:
        Returns SubprocessResult with failure status.
    """
    result = run_command_live(["false"], display_name="test")

    assert isinstance(result, SubprocessResult)
    assert result.display_name == "test"
    assert "❌" in result.status or "Failed" in result.status


def test_run_command_live_with_cwd(tmp_path):
    """
    Scenario:
        Run a command in live mode with a specific working directory.

    Expected:
        Command runs in the specified directory.
    """
    # Create a test file in the temp directory
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")

    result = run_command_live(["ls", "test.txt"], display_name="test", cwd=tmp_path)

    assert isinstance(result, SubprocessResult)
    # run_command_live doesn't capture stdout in the result, it displays it live
    assert result.stdout == ""


def test_run_command_live_default_display_name():
    """
    Scenario:
        Run a command in live mode without specifying display_name.

    Expected:
        Uses the command name as display_name.
    """
    result = run_command_live(["echo", "hello"])

    assert isinstance(result, SubprocessResult)
    assert result.display_name == "echo"


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
            tool_name="echo1",
            cwd=None,
            is_tool=True,
        ),
        CommandSpec(
            command=["echo", "world"],
            tool_name="echo2",
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
            tool_name="echo",
            cwd=None,
            is_tool=True,
        ),
        CommandSpec(
            command=["false"],
            tool_name="false",
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
            tool_name="echo",
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
            tool_name="ls1",
            cwd=tmp_path,
            is_tool=True,
        ),
        CommandSpec(
            command=["ls", "file2.txt"],
            tool_name="ls2",
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
            tool_name="echo",
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
            tool_name="echo",
            cwd=None,
            is_tool=True,
        ),
    ]

    with mock.patch("tidycode.runner.subprocess.pretty_print") as mock_print:
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
            tool_name="echo",
            cwd=None,
            is_tool=True,
        ),
        CommandSpec(
            command=["echo", "world"],
            tool_name="echo",
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
