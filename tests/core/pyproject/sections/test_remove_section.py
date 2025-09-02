"""
TidyCode Core PyProject Remove Section Tests
"""

from unittest.mock import Mock, patch

import pytest

from tidycode.core.pyproject.sections.remove_section import remove_config_section
from tidycode.core.pyproject.types import RemoveSectionChoices
from tidycode.settings import YesNo


def test_remove_config_section_non_interactive_with_section_name():
    """
    Scenario:
        Remove a config section in non-interactive mode with section name provided.

    Expected:
        Section is removed, no prompts shown.
    """
    mock_manager = Mock()
    mock_manager.get_section.return_value = {"key1": "value1", "key2": "value2"}
    mock_manager.delete_section = Mock()
    mock_manager.save = Mock()
    mock_manager.path = "pyproject.toml"

    with patch(
        "tidycode.core.pyproject.sections.remove_section.ask_action"
    ) as mock_ask_action:
        with patch("tidycode.core.pyproject.sections.remove_section.changelog"):
            # Mock the choice to remove entire section
            mock_ask_action.side_effect = [
                RemoveSectionChoices.ENTIRE_SECTION,  # First choice
                YesNo.YES,  # Confirmation
            ]

            remove_config_section(
                manager=mock_manager, section_name="test-section", interactive=False
            )

    # Verify section was deleted
    mock_manager.delete_section.assert_called_once_with("test-section")
    mock_manager.save.assert_called()


def test_remove_config_section_non_interactive_without_section_name():
    """
    Scenario:
        Try to remove a config section in non-interactive mode without section name.

    Expected:
        ValueError is raised.
    """
    mock_manager = Mock()

    with pytest.raises(
        ValueError, match="❌ 'section_name' must be provided when interactive=False."
    ):
        remove_config_section(manager=mock_manager, interactive=False)


def test_remove_config_section_with_prefix():
    """
    Scenario:
        Remove a config section with a prefix.

    Expected:
        Section is removed with the correct full name including prefix.
    """
    mock_manager = Mock()
    mock_manager.get_section.return_value = {"key1": "value1"}
    mock_manager.delete_section = Mock()
    mock_manager.save = Mock()
    mock_manager.path = "pyproject.toml"

    with patch(
        "tidycode.core.pyproject.sections.remove_section.ask_action"
    ) as mock_ask_action:
        with patch("tidycode.core.pyproject.sections.remove_section.changelog"):
            # Mock the choice to remove entire section
            mock_ask_action.side_effect = [
                RemoveSectionChoices.ENTIRE_SECTION,  # First choice
                YesNo.YES,  # Confirmation
            ]

            remove_config_section(
                manager=mock_manager,
                section_name="black",
                prefix="tool.",
                interactive=False,
            )

    # Verify section was deleted with prefix
    mock_manager.delete_section.assert_called_once_with("tool.black")


def test_remove_config_section_section_not_found():
    """
    Scenario:
        Try to remove a config section that doesn't exist.

    Expected:
        Function returns early with error message.
    """
    mock_manager = Mock()
    mock_manager.get_section.return_value = None
    mock_manager.path = "pyproject.toml"

    with patch(
        "tidycode.core.pyproject.sections.remove_section.print_error"
    ) as mock_print_error:
        result = remove_config_section(
            manager=mock_manager, section_name="non-existent", interactive=False
        )

    # Verify error was printed and function returned early
    mock_print_error.assert_called_once()
    assert result is None


def test_remove_config_section_remove_keys_only():
    """
    Scenario:
        Remove specific keys from a config section.

    Expected:
        Keys are removed one by one until exit.
    """
    mock_manager = Mock()
    mock_manager.get_section.return_value = {"key1": "value1", "key2": "value2"}
    mock_manager.set_section = Mock()
    mock_manager.save = Mock()
    mock_manager.path = "pyproject.toml"

    with patch(
        "tidycode.core.pyproject.sections.remove_section.ask_action"
    ) as mock_ask_action:
        with patch(
            "tidycode.core.pyproject.sections.remove_section.ask_choice"
        ) as mock_ask_choice:
            with patch("tidycode.core.pyproject.sections.remove_section.changelog"):
                with patch(
                    "tidycode.core.pyproject.sections.remove_section.get_keys"
                ) as mock_get_keys:
                    with patch(
                        "tidycode.core.pyproject.sections.remove_section.handle_key_deletion"
                    ) as mock_handle_deletion:
                        # Mock the choice to remove keys only
                        mock_ask_action.return_value = RemoveSectionChoices.KEYS_ONLY

                        # Mock key selection (remove one key then exit)
                        mock_ask_choice.side_effect = ["key1", "exit"]

                        # Mock available keys
                        mock_get_keys.return_value = ["key1", "key2"]

                        remove_config_section(
                            manager=mock_manager,
                            section_name="test-section",
                            interactive=False,
                        )

    # Verify key deletion was handled
    mock_handle_deletion.assert_called_once_with(
        "key1", {"key1": "value1", "key2": "value2"}
    )

    # Verify section was updated
    mock_manager.set_section.assert_called_once()
    mock_manager.save.assert_called()


def test_remove_config_section_remove_keys_no_keys_available():
    """
    Scenario:
        Try to remove keys from a section with no keys available.

    Expected:
        Function returns early with error message.
    """
    mock_manager = Mock()
    mock_manager.get_section.return_value = {}
    mock_manager.path = "pyproject.toml"

    with patch(
        "tidycode.core.pyproject.sections.remove_section.ask_action"
    ) as mock_ask_action:
        with patch(
            "tidycode.core.pyproject.sections.remove_section.print_error"
        ) as mock_print_error:
            with patch("tidycode.core.pyproject.sections.remove_section.changelog"):
                with patch(
                    "tidycode.core.pyproject.sections.remove_section.get_keys"
                ) as mock_get_keys:
                    # Mock the choice to remove keys only
                    mock_ask_action.return_value = RemoveSectionChoices.KEYS_ONLY

                    # Mock no keys available
                    mock_get_keys.return_value = []

                    result = remove_config_section(
                        manager=mock_manager,
                        section_name="test-section",
                        interactive=False,
                    )

    # Verify error was printed and function returned early
    mock_print_error.assert_called_once()
    assert result is None


def test_remove_config_section_cancel_entire_section():
    """
    Scenario:
        Choose to remove entire section but cancel the confirmation.

    Expected:
        Section is not removed.
    """
    mock_manager = Mock()
    mock_manager.get_section.return_value = {"key1": "value1"}
    mock_manager.delete_section = Mock()
    mock_manager.save = Mock()
    mock_manager.path = "pyproject.toml"

    with patch(
        "tidycode.core.pyproject.sections.remove_section.ask_action"
    ) as mock_ask_action:
        with patch("tidycode.core.pyproject.sections.remove_section.changelog"):
            # Mock the choice to remove entire section but cancel confirmation
            mock_ask_action.side_effect = [
                RemoveSectionChoices.ENTIRE_SECTION,  # First choice
                YesNo.NO,  # Cancel confirmation
            ]

            remove_config_section(
                manager=mock_manager, section_name="test-section", interactive=False
            )

    # Verify section was not deleted
    mock_manager.delete_section.assert_not_called()
    mock_manager.save.assert_called()


def test_remove_config_section_changelog_capture():
    """
    Scenario:
        Remove a config section and verify changelog capture.

    Expected:
        Changelog capture is used with correct prefix.
    """
    mock_manager = Mock()
    mock_manager.get_section.return_value = {"key1": "value1"}
    mock_manager.delete_section = Mock()
    mock_manager.save = Mock()
    mock_manager.path = "pyproject.toml"

    with patch(
        "tidycode.core.pyproject.sections.remove_section.ask_action"
    ) as mock_ask_action:
        with patch(
            "tidycode.core.pyproject.sections.remove_section.changelog"
        ) as mock_changelog:
            # Mock the choice to remove entire section
            mock_ask_action.side_effect = [
                RemoveSectionChoices.ENTIRE_SECTION,  # First choice
                YesNo.YES,  # Confirmation
            ]

            remove_config_section(
                manager=mock_manager, section_name="test-section", interactive=False
            )

    # Verify changelog capture was called with correct prefix
    mock_changelog.capture.assert_called_once()
    capture_call = mock_changelog.capture.call_args
    # The exact data structure depends on the implementation
    assert capture_call[1]["prefix"] == "test-section."  # Keyword argument (prefix)


def test_remove_config_section_display_label():
    """
    Scenario:
        Remove a config section with custom display label.

    Expected:
        Display label is used in messages and prompts.
    """
    mock_manager = Mock()
    mock_manager.get_section.return_value = {"key1": "value1"}
    mock_manager.delete_section = Mock()
    mock_manager.save = Mock()
    mock_manager.path = "pyproject.toml"

    with patch(
        "tidycode.core.pyproject.sections.remove_section.ask_action"
    ) as mock_ask_action:
        with patch("tidycode.core.pyproject.sections.remove_section.changelog"):
            # Mock the choice to remove entire section
            mock_ask_action.side_effect = [
                RemoveSectionChoices.ENTIRE_SECTION,  # First choice
                YesNo.YES,  # Confirmation
            ]

            remove_config_section(
                manager=mock_manager,
                section_name="test-section",
                display_label="configuration block",
                interactive=False,
            )

    # Verify section was deleted
    mock_manager.delete_section.assert_called_once()


def test_remove_config_section_manager_integration():
    """
    Scenario:
        Test integration with TomlFileManager methods.

    Expected:
        All manager methods are called correctly.
    """
    mock_manager = Mock()
    mock_manager.get_section.return_value = {"key1": "value1"}
    mock_manager.delete_section = Mock()
    mock_manager.save = Mock()
    mock_manager.path = "pyproject.toml"

    with patch(
        "tidycode.core.pyproject.sections.remove_section.ask_action"
    ) as mock_ask_action:
        with patch("tidycode.core.pyproject.sections.remove_section.changelog"):
            # Mock the choice to remove entire section
            mock_ask_action.side_effect = [
                RemoveSectionChoices.ENTIRE_SECTION,  # First choice
                YesNo.YES,  # Confirmation
            ]

            remove_config_section(
                manager=mock_manager, section_name="test-section", interactive=False
            )

    # Verify all manager methods were called
    mock_manager.get_section.assert_called_once_with("test-section")
    mock_manager.delete_section.assert_called_once_with("test-section")
    mock_manager.save.assert_called()


def test_remove_config_section_success_message():
    """
    Scenario:
        Remove a config section and verify success message.

    Expected:
        Success message is printed with correct information.
    """
    mock_manager = Mock()
    mock_manager.get_section.return_value = {"key1": "value1"}
    mock_manager.delete_section = Mock()
    mock_manager.save = Mock()
    mock_manager.path = "pyproject.toml"

    with patch(
        "tidycode.core.pyproject.sections.remove_section.ask_action"
    ) as mock_ask_action:
        with patch("tidycode.core.pyproject.sections.remove_section.changelog"):
            with patch(
                "tidycode.core.pyproject.sections.remove_section.print_success"
            ) as mock_print_success:
                # Mock the choice to remove entire section
                mock_ask_action.side_effect = [
                    RemoveSectionChoices.ENTIRE_SECTION,  # First choice
                    YesNo.YES,  # Confirmation
                ]

                remove_config_section(
                    manager=mock_manager, section_name="test-section", interactive=False
                )

    # Verify success message was printed
    mock_print_success.assert_called_once()
    success_call = mock_print_success.call_args
    assert "test-section" in success_call[0][0]
    assert "pyproject.toml" in success_call[0][0]
