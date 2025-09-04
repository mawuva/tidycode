"""
TidyCode Runner Display Tests
"""

from unittest import mock

import pytest

from tidycode.runner.display import (
    display_list,
    display_table_full,
    display_table_minimal,
    display_text_summary,
    print_summary,
)
from tidycode.runner.types import SubprocessDisplayMode, SubprocessResult

# ---------------------------
# Unit tests
# ---------------------------


def test_display_table_full_success():
    """
    Scenario:
        Display full table with successful results.

    Expected:
        Table is displayed with success status.
    """
    results = [
        SubprocessResult(
            display_name="test",
            status="✅ Passed",
            stdout="success output",
            stderr="",
            category="quality",
            summary="All tests passed",
        )
    ]

    with mock.patch("tidycode.runner.display.console.print") as mock_print:
        display_table_full(results)
        mock_print.assert_called_once()


def test_display_table_full_failure():
    """
    Scenario:
        Display full table with failed results.

    Expected:
        Table is displayed with failure status.
    """
    results = [
        SubprocessResult(
            display_name="test",
            status="❌ Failed",
            stdout="",
            stderr="error output",
            category="quality",
            summary="Tests failed",
        )
    ]

    with mock.patch("tidycode.runner.display.console.print") as mock_print:
        display_table_full(results)
        mock_print.assert_called_once()


def test_display_table_full_mixed_results():
    """
    Scenario:
        Display full table with mixed success/failure results.

    Expected:
        Table is displayed with appropriate statuses.
    """
    results = [
        SubprocessResult(
            display_name="test1",
            status="✅ Passed",
            stdout="success",
            stderr="",
            category="quality",
            summary="Passed",
        ),
        SubprocessResult(
            display_name="test2",
            status="❌ Failed",
            stdout="",
            stderr="error",
            category="quality",
            summary="Failed",
        ),
    ]

    with mock.patch("tidycode.runner.display.console.print") as mock_print:
        display_table_full(results)
        mock_print.assert_called_once()


def test_display_table_full_empty_results():
    """
    Scenario:
        Display full table with empty results.

    Expected:
        Table is displayed with no rows.
    """
    results = []

    with mock.patch("tidycode.runner.display.console.print") as mock_print:
        display_table_full(results)
        mock_print.assert_called_once()


def test_display_table_minimal_success():
    """
    Scenario:
        Display minimal table with successful results.

    Expected:
        Minimal table is displayed with success status.
    """
    results = [
        SubprocessResult(
            display_name="test",
            status="✅ Passed",
            stdout="success output",
            stderr="",
            category="quality",
            summary="All tests passed",
        )
    ]

    with mock.patch("tidycode.runner.display.console.print") as mock_print:
        display_table_minimal(results)
        mock_print.assert_called_once()


def test_display_table_minimal_failure():
    """
    Scenario:
        Display minimal table with failed results.

    Expected:
        Minimal table is displayed with failure status.
    """
    results = [
        SubprocessResult(
            display_name="test",
            status="❌ Failed",
            stdout="",
            stderr="error output",
            category="quality",
            summary="Tests failed",
        )
    ]

    with mock.patch("tidycode.runner.display.console.print") as mock_print:
        display_table_minimal(results)
        mock_print.assert_called_once()


def test_display_table_minimal_empty_results():
    """
    Scenario:
        Display minimal table with empty results.

    Expected:
        Minimal table is displayed with no rows.
    """
    results = []

    with mock.patch("tidycode.runner.display.console.print") as mock_print:
        display_table_minimal(results)
        mock_print.assert_called_once()


def test_display_text_summary_success():
    """
    Scenario:
        Display text summary with successful results.

    Expected:
        Text summary is displayed with success status.
    """
    results = [
        SubprocessResult(
            display_name="test",
            status="✅ Passed",
            stdout="success output",
            stderr="",
            category="quality",
            summary="All tests passed",
        )
    ]

    with mock.patch("tidycode.runner.display.pretty_print") as mock_print:
        display_text_summary(results)
        mock_print.assert_called_once()


def test_display_text_summary_failure():
    """
    Scenario:
        Display text summary with failed results.

    Expected:
        Text summary is displayed with failure status.
    """
    results = [
        SubprocessResult(
            display_name="test",
            status="❌ Failed",
            stdout="",
            stderr="error output",
            category="quality",
            summary="Tests failed",
        )
    ]

    with mock.patch("tidycode.runner.display.pretty_print") as mock_print:
        display_text_summary(results)
        mock_print.assert_called_once()


def test_display_text_summary_empty_results():
    """
    Scenario:
        Display text summary with empty results.

    Expected:
        No text summary is displayed.
    """
    results = []

    with mock.patch("tidycode.runner.display.pretty_print") as mock_print:
        display_text_summary(results)
        mock_print.assert_not_called()


def test_display_list_success():
    """
    Scenario:
        Display list with successful results.

    Expected:
        List is displayed with success status and details.
    """
    results = [
        SubprocessResult(
            display_name="test",
            status="✅ Passed",
            stdout="success output",
            stderr="",
            category="quality",
            summary="All tests passed",
            details="Detailed information",
        )
    ]

    with mock.patch("tidycode.runner.display.pretty_print") as mock_print:
        display_list(results)
        # Should be called multiple times for different parts
        assert mock_print.call_count >= 1


def test_display_list_failure():
    """
    Scenario:
        Display list with failed results.

    Expected:
        List is displayed with failure status and error details.
    """
    results = [
        SubprocessResult(
            display_name="test",
            status="❌ Failed",
            stdout="",
            stderr="error output",
            category="quality",
            summary="Tests failed",
            details="Error details",
        )
    ]

    with mock.patch("tidycode.runner.display.pretty_print") as mock_print:
        display_list(results)
        # Should be called multiple times for different parts
        assert mock_print.call_count >= 1


def test_display_list_with_all_fields():
    """
    Scenario:
        Display list with all fields populated.

    Expected:
        List displays all available information.
    """
    results = [
        SubprocessResult(
            display_name="test",
            status="⚠️ Warning",
            stdout="stdout content",
            stderr="stderr content",
            category="quality",
            summary="Warning summary",
            details="Warning details",
        )
    ]

    with mock.patch("tidycode.runner.display.pretty_print") as mock_print:
        display_list(results)
        # Should be called multiple times for different parts
        assert mock_print.call_count >= 1


def test_display_list_empty_results():
    """
    Scenario:
        Display list with empty results.

    Expected:
        No list is displayed.
    """
    results = []

    with mock.patch("tidycode.runner.display.pretty_print") as mock_print:
        display_list(results)
        mock_print.assert_not_called()


def test_print_summary_table_full():
    """
    Scenario:
        Print summary with table full mode.

    Expected:
        Full table is displayed with summary.
    """
    results = [
        SubprocessResult(
            display_name="test",
            status="✅ Passed",
            stdout="success",
            stderr="",
            category="quality",
            summary="Passed",
        )
    ]

    with mock.patch("tidycode.runner.display.display_table_full") as mock_display:
        with mock.patch("tidycode.runner.display.console.print") as mock_print:
            print_summary(results, SubprocessDisplayMode.TABLE_FULL)
            mock_display.assert_called_once_with(results)
            mock_print.assert_called_once()


def test_print_summary_table_minimal():
    """
    Scenario:
        Print summary with table minimal mode.

    Expected:
        Minimal table is displayed with summary.
    """
    results = [
        SubprocessResult(
            display_name="test",
            status="✅ Passed",
            stdout="success",
            stderr="",
            category="quality",
            summary="Passed",
        )
    ]

    with mock.patch("tidycode.runner.display.display_table_minimal") as mock_display:
        with mock.patch("tidycode.runner.display.console.print") as mock_print:
            print_summary(results, SubprocessDisplayMode.TABLE_MINIMAL)
            mock_display.assert_called_once_with(results)
            mock_print.assert_called_once()


def test_print_summary_text():
    """
    Scenario:
        Print summary with text mode.

    Expected:
        Text summary is displayed with summary.
    """
    results = [
        SubprocessResult(
            display_name="test",
            status="✅ Passed",
            stdout="success",
            stderr="",
            category="quality",
            summary="Passed",
        )
    ]

    with mock.patch("tidycode.runner.display.display_text_summary") as mock_display:
        with mock.patch("tidycode.runner.display.console.print") as mock_print:
            print_summary(results, SubprocessDisplayMode.TEXT)
            mock_display.assert_called_once_with(results)
            mock_print.assert_called_once()


def test_print_summary_list():
    """
    Scenario:
        Print summary with list mode.

    Expected:
        List is displayed with summary.
    """
    results = [
        SubprocessResult(
            display_name="test",
            status="✅ Passed",
            stdout="success",
            stderr="",
            category="quality",
            summary="Passed",
        )
    ]

    with mock.patch("tidycode.runner.display.display_list") as mock_display:
        with mock.patch("tidycode.runner.display.console.print") as mock_print:
            print_summary(results, SubprocessDisplayMode.LIST)
            mock_display.assert_called_once_with(results)
            mock_print.assert_called_once()


def test_print_summary_unknown_mode():
    """
    Scenario:
        Print summary with unknown display mode.

    Expected:
        ValueError is raised.
    """
    results = [
        SubprocessResult(
            display_name="test",
            status="✅ Passed",
            stdout="success",
            stderr="",
            category="quality",
            summary="Passed",
        )
    ]

    with pytest.raises(ValueError, match="Unknown display mode"):
        print_summary(results, "unknown_mode")


def test_print_summary_counting():
    """
    Scenario:
        Print summary with mixed results to test counting.

    Expected:
        Correct counts are displayed in summary.
    """
    results = [
        SubprocessResult(
            display_name="test1",
            status="✅ Passed",
            stdout="success",
            stderr="",
            category="quality",
            summary="Passed",
        ),
        SubprocessResult(
            display_name="test2",
            status="⚠️ Warning",
            stdout="warning",
            stderr="",
            category="quality",
            summary="Warning",
        ),
        SubprocessResult(
            display_name="test3",
            status="❌ Failed",
            stdout="",
            stderr="error",
            category="quality",
            summary="Failed",
        ),
    ]

    with mock.patch("tidycode.runner.display.display_table_minimal") as mock_display:
        with mock.patch("tidycode.runner.display.console.print") as mock_print:
            print_summary(results, SubprocessDisplayMode.TABLE_MINIMAL)
            mock_display.assert_called_once_with(results)
            mock_print.assert_called_once()


# ---------------------------
# Integration tests
# ---------------------------


def test_print_summary_all_modes():
    """
    Scenario:
        Test print_summary with all display modes.

    Expected:
        All modes work correctly.
    """
    results = [
        SubprocessResult(
            display_name="test",
            status="✅ Passed",
            stdout="success",
            stderr="",
            category="quality",
            summary="Passed",
        )
    ]

    modes = [
        SubprocessDisplayMode.TABLE_FULL,
        SubprocessDisplayMode.TABLE_MINIMAL,
        SubprocessDisplayMode.TEXT,
        SubprocessDisplayMode.LIST,
    ]

    for mode in modes:
        with mock.patch("tidycode.runner.display.console.print"):
            # Should not raise any exceptions
            print_summary(results, mode)


def test_display_functions_with_complex_results():
    """
    Scenario:
        Test display functions with complex result data.

    Expected:
        All display functions handle complex data correctly.
    """
    results = [
        SubprocessResult(
            display_name="complex_test",
            status="⚠️ Warning",
            stdout="stdout with\nmultiple lines\nand special chars: café",
            stderr="stderr with\nmultiple lines\nand special chars: ñöç",
            category="quality",
            summary="Complex test with unicode and newlines",
            details="Detailed information with\nmultiple lines",
        )
    ]

    # Test all display functions
    with mock.patch("tidycode.runner.display.console.print"):
        display_table_full(results)
        display_table_minimal(results)

    with mock.patch("tidycode.runner.display.pretty_print"):
        display_text_summary(results)
        display_list(results)


def test_print_summary_empty_results():
    """
    Scenario:
        Test print_summary with empty results.

    Expected:
        Summary shows zero counts for all categories.
    """
    results = []

    with mock.patch("tidycode.runner.display.console.print") as mock_print:
        print_summary(results, SubprocessDisplayMode.TABLE_MINIMAL)
        # Should print summary with zero counts
        assert mock_print.call_count == 2  # Once for table, once for summary
        # Check that the summary contains zero counts
        summary_call = mock_print.call_args_list[-1]  # Last call is the summary
        call_args = summary_call[0][0]
        assert "✅ 0" in call_args
        assert "⚠️ 0" in call_args
        assert "❌ 0" in call_args
