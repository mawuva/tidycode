"""
TidyCode Core PyProject Display Tests
"""

from unittest.mock import patch

from tidycode.core.pyproject.types import PrintSectionSummaryMode
from tidycode.core.pyproject.utils.display import print_section_summary


def test_print_section_summary_default_mode():
    """
    Scenario:
        Test print_section_summary with default mode (TREE).

    Expected:
        Function executes without errors and displays tree format.
    """
    data = {"key1": "value1", "key2": {"nested": "value2"}}

    with patch("tidycode.core.pyproject.utils.display.print_info") as mock_print_info:
        with patch(
            "tidycode.core.pyproject.utils.display._print_tree"
        ) as mock_print_tree:
            print_section_summary("test-section", data)

            # Verify print_info was called for section info
            mock_print_info.assert_called()
            # Verify _print_tree was called for content
            mock_print_tree.assert_called_once()


def test_print_section_summary_tree_mode():
    """
    Scenario:
        Test print_section_summary with TREE mode.

    Expected:
        Function executes without errors and displays tree format.
    """
    data = {"key1": "value1", "key2": {"nested": "value2"}}

    with patch("tidycode.core.pyproject.utils.display.print_info"):
        with patch(
            "tidycode.core.pyproject.utils.display._print_tree"
        ) as mock_print_tree:
            print_section_summary(
                "test-section", data, mode=PrintSectionSummaryMode.TREE
            )

            mock_print_tree.assert_called_once()


def test_print_section_summary_list_mode():
    """
    Scenario:
        Test print_section_summary with LIST mode.

    Expected:
        Function executes without errors and displays list format.
    """
    data = {"key1": "value1", "key2": {"nested": "value2"}}

    with patch("tidycode.core.pyproject.utils.display.print_info"):
        with patch(
            "tidycode.core.pyproject.utils.display._print_list"
        ) as mock_print_list:
            print_section_summary(
                "test-section", data, mode=PrintSectionSummaryMode.LIST
            )

            mock_print_list.assert_called_once()


def test_print_section_summary_table_mode():
    """
    Scenario:
        Test print_section_summary with TABLE mode.

    Expected:
        Function executes without errors and displays table format.
    """
    data = {"key1": "value1", "key2": {"nested": "value2"}}

    with patch("tidycode.core.pyproject.utils.display.print_info"):
        with patch(
            "tidycode.core.pyproject.utils.display._print_table"
        ) as mock_print_table:
            print_section_summary(
                "test-section", data, mode=PrintSectionSummaryMode.TABLE
            )

            mock_print_table.assert_called_once()


def test_print_section_summary_json_mode():
    """
    Scenario:
        Test print_section_summary with JSON mode.

    Expected:
        Function executes without errors and displays JSON format.
    """
    data = {"key1": "value1", "key2": {"nested": "value2"}}

    with patch("tidycode.core.pyproject.utils.display.print_info"):
        with patch(
            "tidycode.core.pyproject.utils.display._print_json"
        ) as mock_print_json:
            print_section_summary(
                "test-section", data, mode=PrintSectionSummaryMode.JSON
            )

            mock_print_json.assert_called_once()


def test_print_section_summary_without_content():
    """
    Scenario:
        Test print_section_summary with display_content=False.

    Expected:
        Function executes without errors and only shows section info.
    """
    data = {"key1": "value1", "key2": {"nested": "value2"}}

    with patch("tidycode.core.pyproject.utils.display.print_info") as mock_print_info:
        with patch(
            "tidycode.core.pyproject.utils.display._print_tree"
        ) as mock_print_tree:
            print_section_summary("test-section", data, display_content=False)

            # Verify print_info was called for section info
            mock_print_info.assert_called()
            # Verify _print_tree was NOT called
            mock_print_tree.assert_not_called()


def test_print_section_summary_complex_data():
    """
    Scenario:
        Test print_section_summary with complex nested data.

    Expected:
        Function executes without errors and handles complex structures.
    """
    data = {
        "tool": {
            "black": {"line-length": 88, "target-version": ["py37", "py38", "py39"]},
            "ruff": {"select": ["E", "F", "I"], "ignore": ["E501"]},
        }
    }

    with patch("tidycode.core.pyproject.utils.display.print_info"):
        with patch(
            "tidycode.core.pyproject.utils.display._print_tree"
        ) as mock_print_tree:
            print_section_summary("complex-section", data)

            mock_print_tree.assert_called_once()


def test_print_section_summary_empty_data():
    """
    Scenario:
        Test print_section_summary with empty data.

    Expected:
        Function executes without errors and shows empty section message.
    """
    data = {}

    with patch("tidycode.core.pyproject.utils.display.print_info") as mock_print_info:
        print_section_summary("empty-section", data)

        # Should call print_info for empty section message
        mock_print_info.assert_called_once()


def test_print_section_summary_none_data():
    """
    Scenario:
        Test print_section_summary with None data.

    Expected:
        Function executes without errors and shows empty section message.
    """
    with patch("tidycode.core.pyproject.utils.display.print_info") as mock_print_info:
        print_section_summary("none-section", None)

        # Should call print_info for empty section message
        mock_print_info.assert_called_once()


def test_print_section_summary_special_characters():
    """
    Scenario:
        Test print_section_summary with special characters in section name.

    Expected:
        Function executes without errors and handles special characters.
    """
    data = {"key": "value"}

    with patch("tidycode.core.pyproject.utils.display.print_info"):
        with patch(
            "tidycode.core.pyproject.utils.display._print_tree"
        ) as mock_print_tree:
            print_section_summary("section-with-special-chars!@#$%", data)

            mock_print_tree.assert_called_once()


def test_print_section_summary_integration():
    """
    Scenario:
        Test print_section_summary with all parameters and real data.

    Expected:
        Function executes without errors and displays content correctly.
    """
    data = {
        "simple": "value",
        "nested": {"level1": {"level2": "deep_value"}},
        "list": [1, 2, 3],
    }

    with patch("tidycode.core.pyproject.utils.display.print_info"):
        with patch(
            "tidycode.core.pyproject.utils.display._print_tree"
        ) as mock_print_tree:
            print_section_summary(
                "integration-test",
                data,
                display_content=True,
                mode=PrintSectionSummaryMode.TREE,
                show_values=True,
                hide_sensitive=True,
                indent_size=4,
            )

            # Verify _print_tree was called with correct parameters
            mock_print_tree.assert_called_once_with(
                data, show_values=True, hide_sensitive=True, indent_size=4
            )
