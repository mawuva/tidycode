"""
TidyCode Core PyProject Show Section Tests
"""

from unittest.mock import Mock, patch

import pytest

from tidycode.core.pyproject.sections.show_section import show_config_section


def test_show_config_section_non_interactive_with_section_name():
    """
    Scenario:
        Show a config section in non-interactive mode with section name provided.

    Expected:
        Section is displayed with display_content=True.
    """
    mock_manager = Mock()
    mock_manager.get_section.return_value = {"key1": "value1", "key2": "value2"}
    mock_manager.path = "pyproject.toml"

    with patch(
        "tidycode.core.pyproject.sections.show_section.print_section_summary"
    ) as mock_print_summary:
        result = show_config_section(
            manager=mock_manager, section_name="test-section", interactive=False
        )

    # Verify section summary was printed
    mock_print_summary.assert_called_once()
    call_args = mock_print_summary.call_args
    assert call_args[1]["section_name"] == "test-section"
    assert call_args[1]["data"] == {"key1": "value1", "key2": "value2"}
    assert call_args[1]["display_content"] is True

    # Function should return None
    assert result is None


def test_show_config_section_non_interactive_without_section_name():
    """
    Scenario:
        Try to show a config section in non-interactive mode without section name.

    Expected:
        ValueError is raised.
    """
    mock_manager = Mock()

    with pytest.raises(
        ValueError, match="❌ 'section_name' must be provided when interactive=False."
    ):
        show_config_section(manager=mock_manager, interactive=False)


def test_show_config_section_with_prefix():
    """
    Scenario:
        Show a config section with a prefix.

    Expected:
        Section is displayed with the correct full name including prefix.
    """
    mock_manager = Mock()
    mock_manager.get_section.return_value = {"key1": "value1"}
    mock_manager.path = "pyproject.toml"

    with patch(
        "tidycode.core.pyproject.sections.show_section.print_section_summary"
    ) as mock_print_summary:
        show_config_section(
            manager=mock_manager,
            section_name="black",
            prefix="tool.",
            interactive=False,
        )

    # Verify section summary was printed with prefix
    mock_print_summary.assert_called_once()
    call_args = mock_print_summary.call_args
    assert call_args[1]["section_name"] == "tool.black"


def test_show_config_section_section_not_found():
    """
    Scenario:
        Try to show a config section that doesn't exist.

    Expected:
        Function returns early with error message.
    """
    mock_manager = Mock()
    mock_manager.get_section.return_value = None
    mock_manager.path = "pyproject.toml"

    with patch(
        "tidycode.core.pyproject.sections.show_section.print_error"
    ) as mock_print_error:
        result = show_config_section(
            manager=mock_manager, section_name="non-existent", interactive=False
        )

    # Verify error was printed and function returned early
    mock_print_error.assert_called_once()
    assert result is None


def test_show_config_section_display_label():
    """
    Scenario:
        Show a config section with custom display label.

    Expected:
        Display label is used in error messages.
    """
    mock_manager = Mock()
    mock_manager.get_section.return_value = {"key1": "value1"}
    mock_manager.path = "pyproject.toml"

    with patch("tidycode.core.pyproject.sections.show_section.print_section_summary"):
        show_config_section(
            manager=mock_manager,
            section_name="test-section",
            display_label="configuration block",
            interactive=False,
        )

    # Verify section was displayed
    mock_manager.get_section.assert_called_once_with("test-section")


def test_show_config_section_manager_integration():
    """
    Scenario:
        Test integration with TomlFileManager methods.

    Expected:
        All manager methods are called correctly.
    """
    mock_manager = Mock()
    mock_manager.get_section.return_value = {"key1": "value1"}
    mock_manager.path = "pyproject.toml"

    with patch("tidycode.core.pyproject.sections.show_section.print_section_summary"):
        show_config_section(
            manager=mock_manager, section_name="test-section", interactive=False
        )

    # Verify all manager methods were called
    mock_manager.get_section.assert_called_once_with("test-section")


def test_show_config_section_complex_data():
    """
    Scenario:
        Show a config section with complex nested data.

    Expected:
        Complex data is displayed correctly.
    """
    complex_data = {
        "dependencies": {"requests": "^2.28.0", "pytest": "^7.0.0"},
        "dev-dependencies": {"black": "^22.0.0", "ruff": "^0.1.0"},
        "scripts": {"test": "pytest", "format": "black .", "lint": "ruff check ."},
    }

    mock_manager = Mock()
    mock_manager.get_section.return_value = complex_data
    mock_manager.path = "pyproject.toml"

    with patch(
        "tidycode.core.pyproject.sections.show_section.print_section_summary"
    ) as mock_print_summary:
        show_config_section(
            manager=mock_manager, section_name="tool.poetry", interactive=False
        )

    # Verify section summary was printed with complex data
    mock_print_summary.assert_called_once()
    call_args = mock_print_summary.call_args
    assert call_args[1]["data"] == complex_data


def test_show_config_section_interactive_mode():
    """
    Scenario:
        Show a config section in interactive mode.

    Expected:
        Section selection works correctly.
    """
    mock_manager = Mock()
    mock_manager.get_section.return_value = {"key1": "value1"}
    mock_manager.path = "pyproject.toml"

    with patch(
        "tidycode.core.pyproject.sections.show_section.select_section"
    ) as mock_select_section:
        with patch(
            "tidycode.core.pyproject.sections.show_section.print_section_summary"
        ):
            # Mock section selection
            mock_select_section.return_value = "selected-section"

            show_config_section(manager=mock_manager, interactive=True)

    # Verify section was selected and displayed
    mock_select_section.assert_called_once_with(mock_manager)
    mock_manager.get_section.assert_called_once_with("selected-section")


def test_show_config_section_no_section_selected():
    """
    Scenario:
        Show a config section but no section is selected.

    Expected:
        Function returns early with error message.
    """
    mock_manager = Mock()
    mock_manager.path = "pyproject.toml"

    with patch(
        "tidycode.core.pyproject.sections.show_section.select_section"
    ) as mock_select_section:
        with patch(
            "tidycode.core.pyproject.sections.show_section.print_error"
        ) as mock_print_error:
            # Mock no section selected
            mock_select_section.return_value = None

            result = show_config_section(manager=mock_manager, interactive=True)

    # Verify error was printed and function returned early
    mock_print_error.assert_called_once()
    assert result is None


def test_show_config_section_display_list_mode():
    """
    Scenario:
        Show a config section with display_list=True in non-interactive mode.

    Expected:
        Function works correctly with display_list mode.
    """
    mock_manager = Mock()
    mock_manager.get_section.return_value = {"key1": "value1"}
    mock_manager.path = "pyproject.toml"

    with patch(
        "tidycode.core.pyproject.sections.show_section.select_section"
    ) as mock_select_section:
        with patch(
            "tidycode.core.pyproject.sections.show_section.print_section_summary"
        ):
            # Mock section selection
            mock_select_section.return_value = "selected-section"

            show_config_section(
                manager=mock_manager, interactive=False, display_list=True
            )

    # Verify section was selected and displayed
    mock_select_section.assert_called_once_with(mock_manager)
    mock_manager.get_section.assert_called_once_with("selected-section")
