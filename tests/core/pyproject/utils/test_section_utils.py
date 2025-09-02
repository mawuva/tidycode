"""
TidyCode Core PyProject Section Utils Tests
"""

from unittest.mock import Mock, patch

from tidycode.core.pyproject.types import OverwriteChoice
from tidycode.core.pyproject.utils.section_utils import (
    collect_section_data,
    collect_subsection_data,
)
from tidycode.settings import YesNo


def test_collect_subsection_data_with_name():
    """
    Scenario:
        Collect subsection data with a valid subsection name.

    Expected:
        Subsection data is collected and returned correctly.
    """
    with patch("tidycode.core.pyproject.utils.section_utils.ask_text") as mock_ask_text:
        with patch(
            "tidycode.core.pyproject.utils.section_utils.changelog"
        ) as mock_changelog:
            with patch(
                "tidycode.core.pyproject.utils.section_utils.prompt_key_values"
            ) as mock_prompt:
                # Mock subsection name input
                mock_ask_text.return_value = "dependencies"

                # Mock key values prompt
                mock_prompt.return_value = {"requests": "^2.28.0", "pytest": "^7.0.0"}

                # Mock changelog capture
                mock_changelog.capture.return_value.__enter__ = Mock()
                mock_changelog.capture.return_value.__exit__ = Mock()

                result = collect_subsection_data("tool.poetry", "poetry")

    # Verify result structure
    assert "dependencies" in result
    assert result["dependencies"] == {"requests": "^2.28.0", "pytest": "^7.0.0"}


def test_collect_subsection_data_empty_name():
    """
    Scenario:
        Collect subsection data with an empty subsection name.

    Expected:
        Empty dictionary is returned.
    """
    with patch("tidycode.core.pyproject.utils.section_utils.ask_text") as mock_ask_text:
        # Mock empty subsection name
        mock_ask_text.return_value = ""

        result = collect_subsection_data("tool.poetry", "poetry")

    # Verify empty result
    assert result == {}


def test_collect_subsection_data_whitespace_name():
    """
    Scenario:
        Collect subsection data with whitespace-only subsection name.

    Expected:
        Empty dictionary is returned.
    """
    with patch("tidycode.core.pyproject.utils.section_utils.ask_text") as mock_ask_text:
        # Mock whitespace-only subsection name
        mock_ask_text.return_value = "   "

        result = collect_subsection_data("tool.poetry", "poetry")

    # Verify empty result
    assert result == {}


def test_collect_section_data_with_plugin():
    """
    Scenario:
        Collect section data using a plugin in non-interactive mode.

    Expected:
        Plugin data is used and returned.
    """
    mock_manager = Mock()
    mock_plugin = Mock()
    mock_plugin.get_data.return_value = {"key1": "value1", "key2": "value2"}

    with patch(
        "tidycode.core.pyproject.utils.section_utils.changelog"
    ) as mock_changelog:
        # Mock changelog capture
        mock_changelog.capture.return_value.__enter__ = Mock()
        mock_changelog.capture.return_value.__exit__ = Mock()

        result = collect_section_data(
            manager=mock_manager,
            full_name="test-section",
            section_name="test",
            display_label="section",
            existing={},
            overwrite_choice=None,
            plugin=mock_plugin,
            initial_data=None,
            interactive=False,
        )

    # Verify plugin data was used
    mock_plugin.get_data.assert_called_once()
    assert result == {"key1": "value1", "key2": "value2"}


def test_collect_section_data_with_initial_data():
    """
    Scenario:
        Collect section data using initial data in non-interactive mode.

    Expected:
        Initial data is used and returned.
    """
    mock_manager = Mock()
    initial_data = {"key1": "value1", "key2": "value2"}

    with patch(
        "tidycode.core.pyproject.utils.section_utils.changelog"
    ) as mock_changelog:
        # Mock changelog capture
        mock_changelog.capture.return_value.__enter__ = Mock()
        mock_changelog.capture.return_value.__exit__ = Mock()

        result = collect_section_data(
            manager=mock_manager,
            full_name="test-section",
            section_name="test",
            display_label="section",
            existing={},
            overwrite_choice=None,
            plugin=None,
            initial_data=initial_data,
            interactive=False,
        )

    # Verify initial data was used
    assert result == initial_data


def test_collect_section_data_overwrite_choice():
    """
    Scenario:
        Collect section data with OVERWRITE choice in interactive mode.

    Expected:
        Section is deleted and new keys are added.
    """
    mock_manager = Mock()
    mock_manager.delete_section = Mock()

    with patch(
        "tidycode.core.pyproject.utils.section_utils.changelog"
    ) as mock_changelog:
        with patch(
            "tidycode.core.pyproject.utils.section_utils.ask_action"
        ) as mock_ask_action:
            with patch(
                "tidycode.core.pyproject.utils.section_utils.prompt_key_values"
            ) as mock_prompt:
                # Mock changelog capture
                mock_changelog.capture.return_value.__enter__ = Mock()
                mock_changelog.capture.return_value.__exit__ = Mock()

                # Mock user choice to add keys
                mock_ask_action.return_value = YesNo.YES

                # Mock key values prompt
                mock_prompt.return_value = {"new_key": "new_value"}

                result = collect_section_data(
                    manager=mock_manager,
                    full_name="test-section",
                    section_name="test",
                    display_label="section",
                    existing={"old_key": "old_value"},
                    overwrite_choice=OverwriteChoice.OVERWRITE,
                    plugin=None,
                    initial_data=None,
                    interactive=True,
                )

    # Verify section was deleted
    mock_manager.delete_section.assert_called_once_with("test-section")

    # Verify new keys were added
    assert result == {"new_key": "new_value"}


def test_collect_section_data_add_keys_choice():
    """
    Scenario:
        Collect section data with ADD_KEYS choice in interactive mode.

    Expected:
        New keys are added to existing data.
    """
    mock_manager = Mock()

    with patch(
        "tidycode.core.pyproject.utils.section_utils.changelog"
    ) as mock_changelog:
        with patch(
            "tidycode.core.pyproject.utils.section_utils.prompt_key_values"
        ) as mock_prompt:
            # Mock changelog capture
            mock_changelog.capture.return_value.__enter__ = Mock()
            mock_changelog.capture.return_value.__exit__ = Mock()

            # Mock key values prompt
            mock_prompt.return_value = {"new_key": "new_value"}

            result = collect_section_data(
                manager=mock_manager,
                full_name="test-section",
                section_name="test",
                display_label="section",
                existing={"old_key": "old_value"},
                overwrite_choice=OverwriteChoice.ADD_KEYS,
                plugin=None,
                initial_data=None,
                interactive=True,
            )

    # Verify new keys were added
    assert result == {"new_key": "new_value"}


def test_collect_section_data_add_subsection_choice():
    """
    Scenario:
        Collect section data with ADD_SUBSECTION choice in interactive mode.

    Expected:
        Subsection data is collected and returned.
    """
    mock_manager = Mock()

    with patch(
        "tidycode.core.pyproject.utils.section_utils.changelog"
    ) as mock_changelog:
        with patch(
            "tidycode.core.pyproject.utils.section_utils.collect_subsection_data"
        ) as mock_collect_subsection:
            # Mock changelog capture
            mock_changelog.capture.return_value.__enter__ = Mock()
            mock_changelog.capture.return_value.__exit__ = Mock()

            # Mock subsection data collection
            mock_collect_subsection.return_value = {
                "dependencies": {"requests": "^2.28.0"}
            }

            result = collect_section_data(
                manager=mock_manager,
                full_name="test-section",
                section_name="test",
                display_label="section",
                existing={"old_key": "old_value"},
                overwrite_choice=OverwriteChoice.ADD_SUBSECTION,
                plugin=None,
                initial_data=None,
                interactive=True,
            )

    # Verify subsection data was collected
    assert result == {"dependencies": {"requests": "^2.28.0"}}


def test_collect_section_data_manager_delete_section_error():
    """
    Scenario:
        Collect section data with OVERWRITE choice but manager has no delete_section method.

    Expected:
        Section is cleared using set_section with empty data.
    """
    mock_manager = Mock()
    mock_manager.delete_section = Mock(
        side_effect=AttributeError("No delete_section method")
    )
    mock_manager.set_section = Mock()

    with patch(
        "tidycode.core.pyproject.utils.section_utils.changelog"
    ) as mock_changelog:
        with patch(
            "tidycode.core.pyproject.utils.section_utils.ask_action"
        ) as mock_ask_action:
            with patch(
                "tidycode.core.pyproject.utils.section_utils.prompt_key_values"
            ) as mock_prompt:
                # Mock changelog capture
                mock_changelog.capture.return_value.__enter__ = Mock()
                mock_changelog.capture.return_value.__exit__ = Mock()

                # Mock user choice to add keys
                mock_ask_action.return_value = YesNo.YES

                # Mock key values prompt
                mock_prompt.return_value = {"new_key": "new_value"}

                result = collect_section_data(
                    manager=mock_manager,
                    full_name="test-section",
                    section_name="test",
                    display_label="section",
                    existing={"old_key": "old_value"},
                    overwrite_choice=OverwriteChoice.OVERWRITE,
                    plugin=None,
                    initial_data=None,
                    interactive=True,
                )

    # Verify set_section was called with empty data
    mock_manager.set_section.assert_called_once_with(
        data={}, dot_key="test-section", overwrite=True
    )

    # Verify new keys were added
    assert result == {"new_key": "new_value"}


def test_collect_section_data_no_add_keys():
    """
    Scenario:
        Collect section data with OVERWRITE choice but user doesn't want to add keys.

    Expected:
        Empty data is returned.
    """
    mock_manager = Mock()
    mock_manager.delete_section = Mock()

    with patch(
        "tidycode.core.pyproject.utils.section_utils.changelog"
    ) as mock_changelog:
        with patch(
            "tidycode.core.pyproject.utils.section_utils.ask_action"
        ) as mock_ask_action:
            # Mock changelog capture
            mock_changelog.capture.return_value.__enter__ = Mock()
            mock_changelog.capture.return_value.__exit__ = Mock()

            # Mock user choice not to add keys
            mock_ask_action.return_value = YesNo.NO

            result = collect_section_data(
                manager=mock_manager,
                full_name="test-section",
                section_name="test",
                display_label="section",
                existing={"old_key": "old_value"},
                overwrite_choice=OverwriteChoice.OVERWRITE,
                plugin=None,
                initial_data=None,
                interactive=True,
            )

    # Verify section was deleted
    mock_manager.delete_section.assert_called_once_with("test-section")

    # Verify empty data is returned
    assert result == {}


def test_collect_section_data_changelog_integration():
    """
    Scenario:
        Test that changelog capture is used correctly.

    Expected:
        Changelog capture is called with correct prefix.
    """
    mock_manager = Mock()
    initial_data = {"key": "value"}

    with patch(
        "tidycode.core.pyproject.utils.section_utils.changelog"
    ) as mock_changelog:
        # Mock changelog capture
        mock_changelog.capture.return_value.__enter__ = Mock()
        mock_changelog.capture.return_value.__exit__ = Mock()

        collect_section_data(
            manager=mock_manager,
            full_name="test-section",
            section_name="test",
            display_label="section",
            existing={},
            overwrite_choice=None,
            plugin=None,
            initial_data=initial_data,
            interactive=False,
        )

    # Verify changelog capture was called with correct prefix
    mock_changelog.capture.assert_called_once()
    capture_call = mock_changelog.capture.call_args
    # The exact data structure depends on the implementation
    assert capture_call[1]["prefix"] == "test-section."  # Keyword argument (prefix)
