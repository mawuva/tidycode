"""
TidyCode Runner Executor Tests
"""

from pathlib import Path
from unittest import mock

from tidycode.runner.executor import run_command, run_command_live
from tidycode.runner.types import SubprocessResult

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


def test_run_command_with_cwd():
    """
    Scenario:
        Run a command with a specific working directory.

    Expected:
        Command runs in the specified directory.
    """
    with mock.patch("subprocess.run") as mock_run:
        mock_process = mock.MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = "output"
        mock_process.stderr = ""
        mock_run.return_value = mock_process

        run_command(["pwd"], display_name="test", cwd=Path("/tmp"), verbose=False)

        mock_run.assert_called_once()
        call_args = mock_run.call_args
        assert call_args[1]["cwd"] == Path("/tmp")


def test_run_command_verbose():
    """
    Scenario:
        Run a command with verbose output.

    Expected:
        Command runs with verbose logging.
    """
    with (
        mock.patch("subprocess.run") as mock_run,
        mock.patch("tidycode.runner.executor.pretty_print") as mock_print,
    ):
        mock_process = mock.MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = "output"
        mock_process.stderr = ""
        mock_run.return_value = mock_process

        result = run_command(["echo", "test"], display_name="test", verbose=True)

        # Should print the command
        mock_print.assert_called()
        assert "✅" in result.status or "Passed" in result.status


def test_run_command_live_success():
    """
    Scenario:
        Run a successful command in live mode.

    Expected:
        Returns SubprocessResult with success status.
    """
    with (
        mock.patch("subprocess.Popen") as mock_popen,
        mock.patch("typer.echo"),
        mock.patch("tidycode.runner.executor.print_success") as mock_success,
    ):
        mock_process = mock.MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = iter(["line1\n", "line2\n"])
        mock_process.wait.return_value = None
        mock_popen.return_value = mock_process

        result = run_command_live(["echo", "test"], display_name="test")

        assert isinstance(result, SubprocessResult)
        assert result.display_name == "test"
        assert "✅" in result.status or "Passed" in result.status
        mock_success.assert_called_once()


def test_run_command_live_failure():
    """
    Scenario:
        Run a failing command in live mode.

    Expected:
        Returns SubprocessResult with failure status.
    """
    with (
        mock.patch("subprocess.Popen") as mock_popen,
        mock.patch("typer.echo"),
        mock.patch("tidycode.runner.executor.print_error") as mock_error,
    ):
        mock_process = mock.MagicMock()
        mock_process.returncode = 1
        mock_process.stdout = iter(["error line\n"])
        mock_process.wait.return_value = None
        mock_popen.return_value = mock_process

        result = run_command_live(["false"], display_name="test")

        assert isinstance(result, SubprocessResult)
        assert result.display_name == "test"
        assert "❌" in result.status or "Failed" in result.status
        mock_error.assert_called_once()


def test_run_command_live_with_cwd():
    """
    Scenario:
        Run a command in live mode with a specific working directory.

    Expected:
        Command runs in the specified directory.
    """
    with (
        mock.patch("subprocess.Popen") as mock_popen,
        mock.patch("typer.echo"),
    ):
        mock_process = mock.MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = iter([])
        mock_process.wait.return_value = None
        mock_popen.return_value = mock_process

        run_command_live(["pwd"], display_name="test", cwd=Path("/tmp"))

        mock_popen.assert_called_once()
        call_args = mock_popen.call_args
        assert call_args[1]["cwd"] == Path("/tmp")


def test_run_command_exception_handling():
    """
    Scenario:
        Run a command that raises an exception.

    Expected:
        Exception is handled and returns error result.
    """
    with mock.patch("subprocess.run", side_effect=OSError("Command not found")):
        result = run_command(["nonexistent"], display_name="test", verbose=False)

        assert isinstance(result, SubprocessResult)
        assert result.display_name == "test"
        assert "❌" in result.status or "Failed" in result.status


def test_run_command_live_exception_handling():
    """
    Scenario:
        Run a command in live mode that raises an exception.

    Expected:
        Exception is handled and returns error result.
    """
    with mock.patch("subprocess.Popen", side_effect=OSError("Command not found")):
        result = run_command_live(["nonexistent"], display_name="test")

        assert isinstance(result, SubprocessResult)
        assert result.display_name == "test"
        assert "❌" in result.status or "Failed" in result.status


def test_run_command_default_display_name():
    """
    Scenario:
        Run a command without specifying display_name.

    Expected:
        Uses command[0] as display name.
    """
    result = run_command(["echo", "test"], verbose=False)

    assert result.display_name == "echo"


def test_run_command_live_default_display_name():
    """
    Scenario:
        Run a command in live mode without specifying display_name.

    Expected:
        Uses command[0] as display name.
    """
    with (
        mock.patch("subprocess.Popen") as mock_popen,
        mock.patch("typer.echo"),
    ):
        mock_process = mock.MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = iter([])
        mock_process.wait.return_value = None
        mock_popen.return_value = mock_process

        result = run_command_live(["echo", "test"])

        assert result.display_name == "echo"


def test_run_command_is_tool_parameter():
    """
    Scenario:
        Run a command with is_tool parameter.

    Expected:
        is_tool parameter is passed correctly to build_result.
    """
    with (
        mock.patch("subprocess.run") as mock_run,
        mock.patch("tidycode.runner.executor.build_result") as mock_build_result,
    ):
        mock_process = mock.MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = "output"
        mock_process.stderr = ""
        mock_run.return_value = mock_process

        run_command(["echo", "test"], is_tool=False, verbose=False)

        mock_build_result.assert_called_once()
        call_args = mock_build_result.call_args
        # build_result is called with positional arguments and is_tool as keyword argument
        assert call_args[1]["is_tool"] is False


def test_run_command_live_is_tool_parameter():
    """
    Scenario:
        Run a command in live mode with is_tool parameter.

    Expected:
        is_tool parameter is passed correctly to build_result.
    """
    with (
        mock.patch("subprocess.Popen") as mock_popen,
        mock.patch("typer.echo"),
        mock.patch("tidycode.runner.executor.build_result") as mock_build_result,
    ):
        mock_process = mock.MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = iter([])
        mock_process.wait.return_value = None
        mock_popen.return_value = mock_process

        run_command_live(["echo", "test"], is_tool=False)

        mock_build_result.assert_called_once()
        call_args = mock_build_result.call_args
        # build_result is called with positional arguments: display_name, returncode, stdout, stderr, is_tool
        assert call_args[0][4] is False  # is_tool is the 5th positional argument
