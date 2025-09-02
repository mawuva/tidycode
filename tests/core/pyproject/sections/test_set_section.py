"""
TidyCode Core PyProject Set Section Tests
"""

from unittest.mock import Mock, patch

import pytest

from tidycode.core.pyproject.sections.set_section import set_config_section


def test_set_config_section_non_interactive_with_section_name():
    """
    Scenario:
        Set a config section in non-interactive mode with section name provided.

    Expected:
        Section is set with initial data, no prompts shown.
    """
    mock_manager = Mock()
    mock_manager.get_section.return_value = {"existing": "data"}
    mock_manager.set_section = Mock()
    mock_manager.path = "pyproject.toml"

    initial_data = {"key": "value", "existing": "data"}

    with patch(
        "tidycode.core.pyproject.sections.set_section.print_section_summary"
    ) as mock_print_summary:
        with patch(
            "tidycode.core.pyproject.sections.set_section.changelog"
        ) as mock_changelog:
            set_config_section(
                manager=mock_manager,
                section_name="test-section",
                initial_data=initial_data,
                interactive=False,
            )

    # Verify section summary was printed
    mock_print_summary.assert_called_once()

    # Verify changelog capture was used
    mock_changelog.capture.assert_called_once()

    # Verify section was set
    mock_manager.set_section.assert_called_once()
    call_args = mock_manager.set_section.call_args
    assert call_args[1]["dot_key"] == "test-section"
    assert call_args[1]["overwrite"] is True


def test_set_config_section_non_interactive_without_section_name():
    """
    Scenario:
        Try to set a config section in non-interactive mode without section name.

    Expected:
        ValueError is raised.
    """
    mock_manager = Mock()

    with pytest.raises(
        ValueError, match="❌ 'section_name' must be provided when interactive=False."
    ):
        set_config_section(manager=mock_manager, interactive=False)


def test_set_config_section_with_prefix():
    """
    Scenario:
        Set a config section with a prefix.

    Expected:
        Section is set with the correct full name including prefix.
    """
    mock_manager = Mock()
    mock_manager.get_section.return_value = {"existing": "data"}
    mock_manager.set_section = Mock()
    mock_manager.path = "pyproject.toml"

    initial_data = {"key": "value"}

    with patch("tidycode.core.pyproject.sections.set_section.print_section_summary"):
        with patch("tidycode.core.pyproject.sections.set_section.changelog"):
            set_config_section(
                manager=mock_manager,
                section_name="black",
                prefix="tool.",
                initial_data=initial_data,
                interactive=False,
            )

    # Verify section was set with prefix
    mock_manager.set_section.assert_called_once()
    call_args = mock_manager.set_section.call_args
    assert call_args[1]["dot_key"] == "tool.black"


def test_set_config_section_section_not_found():
    """
    Scenario:
        Try to set a config section that doesn't exist.

    Expected:
        Function returns early with error message.
    """
    mock_manager = Mock()
    mock_manager.get_section.return_value = None
    mock_manager.path = "pyproject.toml"

    with patch(
        "tidycode.core.pyproject.sections.set_section.print_error"
    ) as mock_print_error:
        result = set_config_section(
            manager=mock_manager, section_name="non-existent", interactive=False
        )

    # Verify error was printed and function returned early
    mock_print_error.assert_called_once()
    assert result is None


def test_set_config_section_changelog_capture():
    """
    Scenario:
        Set a config section and verify changelog capture.

    Expected:
        Changelog capture is used with correct prefix.
    """
    mock_manager = Mock()
    mock_manager.get_section.return_value = {"existing": "data"}
    mock_manager.set_section = Mock()
    mock_manager.path = "pyproject.toml"

    initial_data = {"key": "value"}

    with patch("tidycode.core.pyproject.sections.set_section.print_section_summary"):
        with patch(
            "tidycode.core.pyproject.sections.set_section.changelog"
        ) as mock_changelog:
            set_config_section(
                manager=mock_manager,
                section_name="test-section",
                initial_data=initial_data,
                interactive=False,
            )

    # Verify changelog capture was called with correct prefix
    mock_changelog.capture.assert_called_once()
    capture_call = mock_changelog.capture.call_args
    # The exact data structure depends on the implementation
    assert capture_call[1]["prefix"] == "test-section."  # Keyword argument (prefix)


def test_set_config_section_display_label():
    """
    Scenario:
        Set a config section with custom display label.

    Expected:
        Display label is used in error messages.
    """
    mock_manager = Mock()
    mock_manager.get_section.return_value = {"existing": "data"}
    mock_manager.set_section = Mock()
    mock_manager.path = "pyproject.toml"

    initial_data = {"key": "value"}

    with patch("tidycode.core.pyproject.sections.set_section.print_section_summary"):
        with patch("tidycode.core.pyproject.sections.set_section.changelog"):
            set_config_section(
                manager=mock_manager,
                section_name="test-section",
                display_label="configuration block",
                initial_data=initial_data,
                interactive=False,
            )

    # Verify section was set
    mock_manager.set_section.assert_called_once()


def test_set_config_section_manager_integration():
    """
    Scenario:
        Test integration with TomlFileManager methods.

    Expected:
        All manager methods are called correctly.
    """
    mock_manager = Mock()
    mock_manager.get_section.return_value = {"existing": "data"}
    mock_manager.set_section = Mock()
    mock_manager.path = "pyproject.toml"

    initial_data = {"key": "value"}

    with patch("tidycode.core.pyproject.sections.set_section.print_section_summary"):
        with patch("tidycode.core.pyproject.sections.set_section.changelog"):
            set_config_section(
                manager=mock_manager,
                section_name="test-section",
                initial_data=initial_data,
                interactive=False,
            )

    # Verify all manager methods were called
    mock_manager.get_section.assert_called_once_with("test-section")
    mock_manager.set_section.assert_called_once()

    # Verify set_section was called with correct parameters
    set_section_call = mock_manager.set_section.call_args
    assert set_section_call[1]["overwrite"] is True
    assert set_section_call[1]["dot_key"] == "test-section"


def test_set_config_section_initial_data_override():
    """
    Scenario:
        Set a config section with initial data that overrides existing data.

    Expected:
        Initial data is used instead of existing data from manager.
    """
    mock_manager = Mock()
    mock_manager.get_section.return_value = {"existing": "old_data"}
    mock_manager.set_section = Mock()
    mock_manager.path = "pyproject.toml"

    initial_data = {"new_key": "new_value", "existing": "new_data"}

    with patch(
        "tidycode.core.pyproject.sections.set_section.print_section_summary"
    ) as mock_print_summary:
        with patch("tidycode.core.pyproject.sections.set_section.changelog"):
            set_config_section(
                manager=mock_manager,
                section_name="test-section",
                initial_data=initial_data,
                interactive=False,
            )

    # Verify section summary was printed with initial data
    mock_print_summary.assert_called_once()

    # Verify section was set with initial data
    mock_manager.set_section.assert_called_once()


def test_set_config_section_no_initial_data():
    """
    Scenario:
        Set a config section without initial data.

    Expected:
        Existing data from manager is used.
    """
    existing_data = {"existing": "data"}
    mock_manager = Mock()
    mock_manager.get_section.return_value = existing_data
    mock_manager.set_section = Mock()
    mock_manager.path = "pyproject.toml"

    with patch(
        "tidycode.core.pyproject.sections.set_section.print_section_summary"
    ) as mock_print_summary:
        with patch("tidycode.core.pyproject.sections.set_section.changelog"):
            set_config_section(
                manager=mock_manager, section_name="test-section", interactive=False
            )

    # Verify section summary was printed with existing data
    mock_print_summary.assert_called_once()

    # Verify section was set with existing data
    mock_manager.set_section.assert_called_once()


def test_set_config_section_changelog_context():
    """
    Scenario:
        Set a config section and verify changelog context manager usage.

    Expected:
        Changelog capture is used as a context manager.
    """
    mock_manager = Mock()
    mock_manager.get_section.return_value = {"existing": "data"}
    mock_manager.set_section = Mock()
    mock_manager.path = "pyproject.toml"

    initial_data = {"key": "value"}

    mock_changelog = Mock()
    mock_changelog.capture.return_value.__enter__ = Mock()
    mock_changelog.capture.return_value.__exit__ = Mock()

    with patch(
        "tidycode.core.pyproject.sections.set_section.changelog", mock_changelog
    ):
        with patch(
            "tidycode.core.pyproject.sections.set_section.print_section_summary"
        ):
            set_config_section(
                manager=mock_manager,
                section_name="test-section",
                initial_data=initial_data,
                interactive=False,
            )

    # Verify changelog capture was used as context manager
    mock_changelog.capture.assert_called_once()
    mock_changelog.capture.return_value.__enter__.assert_called_once()
    mock_changelog.capture.return_value.__exit__.assert_called_once()
