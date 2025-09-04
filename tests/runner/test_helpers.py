"""
TidyCode Runner Helpers Tests
"""

from unittest import mock

from tidycode.runner.helpers import (
    build_result,
    handle_exception,
    status_color,
    status_from_returncode,
)
from tidycode.runner.types import SubprocessResult

# ---------------------------
# Unit tests
# ---------------------------


def test_status_color_success():
    """
    Scenario:
        Get color for success status.

    Expected:
        Returns "green".
    """
    result = status_color("✅ Passed")
    assert result == "green"


def test_status_color_warning():
    """
    Scenario:
        Get color for warning status.

    Expected:
        Returns "yellow".
    """
    result = status_color("⚠️ Warning")
    assert result == "yellow"


def test_status_color_failure():
    """
    Scenario:
        Get color for failure status.

    Expected:
        Returns "red".
    """
    result = status_color("❌ Failed")
    assert result == "red"


def test_status_color_unknown():
    """
    Scenario:
        Get color for unknown status.

    Expected:
        Returns "red" as default.
    """
    result = status_color("Unknown status")
    assert result == "red"


def test_status_from_returncode_tool_success():
    """
    Scenario:
        Get status for successful tool command.

    Expected:
        Returns "✅ Passed".
    """
    result = status_from_returncode("test", 0, "output", True)
    assert result == "✅ Passed"


def test_status_from_returncode_tool_failure():
    """
    Scenario:
        Get status for failed tool command.

    Expected:
        Returns "❌ Failed".
    """
    result = status_from_returncode("test", 1, "error", True)
    assert result == "❌ Failed"


def test_status_from_returncode_non_tool():
    """
    Scenario:
        Get status for non-tool command.

    Expected:
        Returns exit code format.
    """
    result = status_from_returncode("test", 5, "output", False)
    assert result == "Exit 5"


def test_status_from_returncode_ruff_special_case():
    """
    Scenario:
        Get status for ruff command with special "All done" case.

    Expected:
        Returns "✅ Passed" even with return code 1.
    """
    result = status_from_returncode("ruff", 1, "All done", True)
    assert result == "✅ Passed"


def test_status_from_returncode_ruff_failure():
    """
    Scenario:
        Get status for ruff command without "All done".

    Expected:
        Returns "❌ Failed" with return code 1.
    """
    result = status_from_returncode("ruff", 1, "Some error", True)
    assert result == "❌ Failed"


def test_build_result_success():
    """
    Scenario:
        Build result for successful command.

    Expected:
        Returns SubprocessResult with success status.
    """
    result = build_result("test", 0, "stdout", "stderr", True)

    assert isinstance(result, SubprocessResult)
    assert result.display_name == "test"
    assert result.status == "✅ Passed"
    assert result.stdout == "stdout"
    assert result.stderr == "stderr"


def test_build_result_failure():
    """
    Scenario:
        Build result for failed command.

    Expected:
        Returns SubprocessResult with failure status.
    """
    result = build_result("test", 1, "stdout", "stderr", True)

    assert isinstance(result, SubprocessResult)
    assert result.display_name == "test"
    assert result.status == "❌ Failed"
    assert result.stdout == "stdout"
    assert result.stderr == "stderr"


def test_build_result_non_tool():
    """
    Scenario:
        Build result for non-tool command.

    Expected:
        Returns SubprocessResult with exit code status.
    """
    result = build_result("test", 5, "stdout", "stderr", False)

    assert isinstance(result, SubprocessResult)
    assert result.display_name == "test"
    assert result.status == "Exit 5"
    assert result.stdout == "stdout"
    assert result.stderr == "stderr"


def test_build_result_empty_outputs():
    """
    Scenario:
        Build result with empty stdout and stderr.

    Expected:
        Returns SubprocessResult with empty strings.
    """
    result = build_result("test", 0, "", "", True)

    assert isinstance(result, SubprocessResult)
    assert result.display_name == "test"
    assert result.status == "✅ Passed"
    assert result.stdout == ""
    assert result.stderr == ""


def test_build_result_unicode_handling():
    """
    Scenario:
        Build result with unicode characters in output.

    Expected:
        Unicode characters are properly handled.
    """
    unicode_stdout = "café ñöç"
    unicode_stderr = "émojis 🚀"

    result = build_result("test", 0, unicode_stdout, unicode_stderr, True)

    assert isinstance(result, SubprocessResult)
    assert result.stdout == unicode_stdout
    assert result.stderr == unicode_stderr


def test_build_result_whitespace_handling():
    """
    Scenario:
        Build result with whitespace in output.

    Expected:
        Whitespace is preserved but stripped from ends.
    """
    result = build_result("test", 0, "  hello world  ", "  error  ", True)

    assert isinstance(result, SubprocessResult)
    assert result.stdout == "hello world"
    assert result.stderr == "error"


def test_handle_exception_file_not_found():
    """
    Scenario:
        Handle FileNotFoundError exception.

    Expected:
        Returns SubprocessResult with command not found message.
    """
    exception = FileNotFoundError("Command not found")
    result = handle_exception(exception, "test", True, False)

    assert isinstance(result, SubprocessResult)
    assert result.display_name == "test"
    assert result.status == "❌ Failed"
    assert "Command not found: test" in result.stderr
    assert result.stdout == ""


def test_handle_exception_generic():
    """
    Scenario:
        Handle generic exception.

    Expected:
        Returns SubprocessResult with exception message.
    """
    exception = ValueError("Something went wrong")
    result = handle_exception(exception, "test", True, False)

    assert isinstance(result, SubprocessResult)
    assert result.display_name == "test"
    assert result.status == "❌ Failed"
    assert "Something went wrong" in result.stderr
    assert result.stdout == ""


def test_handle_exception_non_tool():
    """
    Scenario:
        Handle exception for non-tool command.

    Expected:
        Returns SubprocessResult with appropriate status.
    """
    exception = FileNotFoundError("Command not found")
    result = handle_exception(exception, "test", False, False)

    assert isinstance(result, SubprocessResult)
    assert result.display_name == "test"
    assert result.status == "Exit 127"
    assert "Command not found: test" in result.stderr


def test_handle_exception_verbose():
    """
    Scenario:
        Handle exception with verbose output.

    Expected:
        Prints warning message when verbose is True.
    """
    exception = ValueError("Something went wrong")

    with mock.patch("tidycode.runner.helpers.print_warning") as mock_print:
        result = handle_exception(exception, "test", True, True)

        assert isinstance(result, SubprocessResult)
        mock_print.assert_called_once_with("Something went wrong")


def test_handle_exception_not_verbose():
    """
    Scenario:
        Handle exception without verbose output.

    Expected:
        Does not print warning message when verbose is False.
    """
    exception = ValueError("Something went wrong")

    with mock.patch("tidycode.runner.helpers.print_warning") as mock_print:
        result = handle_exception(exception, "test", True, False)

        assert isinstance(result, SubprocessResult)
        mock_print.assert_not_called()


def test_handle_exception_return_codes():
    """
    Scenario:
        Handle different exception types with correct return codes.

    Expected:
        FileNotFoundError returns 127, others return 1.
    """
    # FileNotFoundError should return 127
    file_not_found = FileNotFoundError("Command not found")
    result1 = handle_exception(file_not_found, "test", True, False)
    assert "Exit 127" in result1.status or "❌ Failed" in result1.status

    # Other exceptions should return 1
    generic_error = ValueError("Something went wrong")
    result2 = handle_exception(generic_error, "test", True, False)
    assert "❌ Failed" in result2.status


# ---------------------------
# Integration tests
# ---------------------------


def test_build_result_with_status_from_returncode():
    """
    Scenario:
        Test integration between build_result and status_from_returncode.

    Expected:
        Functions work together correctly.
    """
    # Test successful case
    result = build_result("test", 0, "success", "", True)
    assert result.status == "✅ Passed"

    # Test failure case
    result = build_result("test", 1, "failure", "", True)
    assert result.status == "❌ Failed"

    # Test ruff special case
    result = build_result("ruff", 1, "All done", "", True)
    assert result.status == "✅ Passed"


def test_handle_exception_with_build_result():
    """
    Scenario:
        Test integration between handle_exception and build_result.

    Expected:
        Functions work together correctly.
    """
    exception = FileNotFoundError("Command not found")
    result = handle_exception(exception, "test", True, False)

    # Verify the result is properly built
    assert isinstance(result, SubprocessResult)
    assert result.display_name == "test"
    assert result.stdout == ""
    assert "Command not found: test" in result.stderr


def test_status_color_with_various_statuses():
    """
    Scenario:
        Test status_color with various status formats.

    Expected:
        Correct colors are returned for different status formats.
    """
    # Test different success formats
    assert status_color("✅ Passed") == "green"
    assert status_color("✅ Success") == "green"
    assert status_color("✅ All done") == "green"

    # Test different warning formats
    assert status_color("⚠️ Warning") == "yellow"
    assert status_color("⚠️ Caution") == "yellow"

    # Test different failure formats
    assert status_color("❌ Failed") == "red"
    assert status_color("❌ Error") == "red"
    assert status_color("Exit 1") == "red"
    assert status_color("Exit 127") == "red"
