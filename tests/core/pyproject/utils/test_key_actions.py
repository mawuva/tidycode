"""
TidyCode Core PyProject Key Actions Tests
"""

from unittest.mock import patch

from tidycode.core.pyproject.types import KeyActions, Mode
from tidycode.core.pyproject.utils.key_actions import (
    handle_key_action,
    handle_key_action_full_mode,
    handle_key_creation,
    handle_key_deletion,
    handle_key_edition,
    select_and_handle_section_keys,
)


def test_handle_key_creation():
    """
    Scenario:
        Handle the creation of a new key.

    Expected:
        Key is added to data with the entered value.
    """
    data = {}

    with patch("tidycode.core.pyproject.utils.key_actions.ask_text") as mock_ask_text:
        with patch(
            "tidycode.core.pyproject.utils.key_actions.print_success"
        ) as mock_print_success:
            # Mock user input
            mock_ask_text.return_value = "test_value"

            handle_key_creation("test_key", data)

    # Verify key was added
    assert data["test_key"] == "test_value"

    # Verify success message was printed
    mock_print_success.assert_called_once_with(
        "Key 'test_key' added with value 'test_value'"
    )


def test_handle_key_edition():
    """
    Scenario:
        Handle the edit action for an existing key.

    Expected:
        Key value is updated with the new value.
    """
    data = {"test_key": "old_value"}

    with patch("tidycode.core.pyproject.utils.key_actions.ask_text") as mock_ask_text:
        with patch(
            "tidycode.core.pyproject.utils.key_actions.print_success"
        ) as mock_print_success:
            # Mock user input
            mock_ask_text.return_value = "new_value"

            handle_key_edition("test_key", data)

    # Verify key was updated
    assert data["test_key"] == "new_value"

    # Verify success message was printed
    mock_print_success.assert_called_once_with("Key 'test_key' updated to 'new_value'")


def test_handle_key_deletion():
    """
    Scenario:
        Handle the deletion of an existing key.

    Expected:
        Key is removed from data.
    """
    data = {"test_key": "test_value", "other_key": "other_value"}

    with patch(
        "tidycode.core.pyproject.utils.key_actions.print_success"
    ) as mock_print_success:
        handle_key_deletion("test_key", data)

    # Verify key was removed
    assert "test_key" not in data
    assert "other_key" in data  # Other keys should remain

    # Verify success message was printed
    mock_print_success.assert_called_once_with("Key 'test_key' removed.")


def test_handle_key_action_full_mode_edit():
    """
    Scenario:
        Handle key action in full mode with edit choice.

    Expected:
        Key is edited.
    """
    data = {"test_key": "old_value"}

    with patch(
        "tidycode.core.pyproject.utils.key_actions.ask_action"
    ) as mock_ask_action:
        with patch(
            "tidycode.core.pyproject.utils.key_actions.ask_text"
        ) as mock_ask_text:
            with patch(
                "tidycode.core.pyproject.utils.key_actions.print_success"
            ) as mock_print_success:
                # Mock user choice to edit
                mock_ask_action.return_value = KeyActions.EDIT

                # Mock new value input
                mock_ask_text.return_value = "new_value"

                handle_key_action_full_mode("test_key", data)

    # Verify key was updated
    assert data["test_key"] == "new_value"

    # Verify success message was printed
    mock_print_success.assert_called_once_with("Key 'test_key' updated to 'new_value'")


def test_handle_key_action_full_mode_remove():
    """
    Scenario:
        Handle key action in full mode with remove choice.

    Expected:
        Key is removed.
    """
    data = {"test_key": "test_value"}

    with patch(
        "tidycode.core.pyproject.utils.key_actions.ask_action"
    ) as mock_ask_action:
        with patch(
            "tidycode.core.pyproject.utils.key_actions.print_success"
        ) as mock_print_success:
            # Mock user choice to remove
            mock_ask_action.return_value = KeyActions.REMOVE

            handle_key_action_full_mode("test_key", data)

    # Verify key was removed
    assert "test_key" not in data

    # Verify success message was printed
    mock_print_success.assert_called_once_with("Key 'test_key' removed.")


def test_handle_key_action_full_mode_skip():
    """
    Scenario:
        Handle key action in full mode with skip choice.

    Expected:
        Key is skipped (not modified).
    """
    data = {"test_key": "test_value"}

    with patch(
        "tidycode.core.pyproject.utils.key_actions.ask_action"
    ) as mock_ask_action:
        with patch(
            "tidycode.core.pyproject.utils.key_actions.print_warning"
        ) as mock_print_warning:
            # Mock user choice to skip
            mock_ask_action.return_value = KeyActions.SKIP

            handle_key_action_full_mode("test_key", data)

    # Verify key was not modified
    assert data["test_key"] == "test_value"

    # Verify warning message was printed
    mock_print_warning.assert_called_once_with("⚠️ Skipping key 'test_key'")


def test_handle_key_action_add_mode_existing_key():
    """
    Scenario:
        Handle key action in ADD mode with existing key.

    Expected:
        Key is skipped with warning.
    """
    data = {"test_key": "existing_value"}

    with patch(
        "tidycode.core.pyproject.utils.key_actions.print_warning"
    ) as mock_print_warning:
        handle_key_action("test_key", data, Mode.ADD)

    # Verify key was not modified
    assert data["test_key"] == "existing_value"

    # Verify warning message was printed
    mock_print_warning.assert_called_once_with(
        "⚠️ Key 'test_key' already exists, skipping."
    )


def test_handle_key_action_add_mode_new_key():
    """
    Scenario:
        Handle key action in ADD mode with new key.

    Expected:
        Key is created.
    """
    data = {}

    with patch("tidycode.core.pyproject.utils.key_actions.ask_text") as mock_ask_text:
        with patch(
            "tidycode.core.pyproject.utils.key_actions.print_success"
        ) as mock_print_success:
            # Mock user input
            mock_ask_text.return_value = "new_value"

            handle_key_action("test_key", data, Mode.ADD)

    # Verify key was created
    assert data["test_key"] == "new_value"

    # Verify success message was printed
    mock_print_success.assert_called_once_with(
        "Key 'test_key' added with value 'new_value'"
    )


def test_handle_key_action_edit_mode():
    """
    Scenario:
        Handle key action in EDIT mode.

    Expected:
        Key is edited.
    """
    data = {"test_key": "old_value"}

    with patch("tidycode.core.pyproject.utils.key_actions.ask_text") as mock_ask_text:
        with patch(
            "tidycode.core.pyproject.utils.key_actions.print_success"
        ) as mock_print_success:
            # Mock user input
            mock_ask_text.return_value = "new_value"

            handle_key_action("test_key", data, Mode.EDIT)

    # Verify key was updated
    assert data["test_key"] == "new_value"

    # Verify success message was printed
    mock_print_success.assert_called_once_with("Key 'test_key' updated to 'new_value'")


def test_handle_key_action_remove_mode():
    """
    Scenario:
        Handle key action in REMOVE mode.

    Expected:
        Key is removed.
    """
    data = {"test_key": "test_value"}

    with patch(
        "tidycode.core.pyproject.utils.key_actions.print_success"
    ) as mock_print_success:
        handle_key_action("test_key", data, Mode.REMOVE)

    # Verify key was removed
    assert "test_key" not in data

    # Verify success message was printed
    mock_print_success.assert_called_once_with("Key 'test_key' removed.")


def test_handle_key_action_full_mode():
    """
    Scenario:
        Handle key action in FULL mode.

    Expected:
        Full mode handling is used.
    """
    data = {"test_key": "test_value"}

    with patch(
        "tidycode.core.pyproject.utils.key_actions.handle_key_action_full_mode"
    ) as mock_full_mode:
        handle_key_action("test_key", data, Mode.FULL)

    # Verify full mode handling was called
    mock_full_mode.assert_called_once_with("test_key", data)


def test_select_and_handle_section_keys_no_keys():
    """
    Scenario:
        Select and handle section keys when no keys are available.

    Expected:
        Warning message is printed.
    """
    section_data = {}

    with patch("tidycode.core.pyproject.utils.key_actions.get_keys") as mock_get_keys:
        with patch(
            "tidycode.core.pyproject.utils.key_actions.print_warning"
        ) as mock_print_warning:
            # Mock no keys available
            mock_get_keys.return_value = []

            select_and_handle_section_keys(section_data, Mode.FULL)

    # Verify warning was printed
    mock_print_warning.assert_called_once_with("No keys available.")


def test_select_and_handle_section_keys_with_keys():
    """
    Scenario:
        Select and handle section keys when keys are available.

    Expected:
        Key selection and handling works correctly.
    """
    section_data = {"key1": "value1", "key2": "value2"}

    with patch("tidycode.core.pyproject.utils.key_actions.get_keys") as mock_get_keys:
        with patch(
            "tidycode.core.pyproject.utils.key_actions.ask_choice"
        ) as mock_ask_choice:
            with patch(
                "tidycode.core.pyproject.utils.key_actions.ask_action"
            ) as mock_ask_action:
                with patch(
                    "tidycode.core.pyproject.utils.key_actions.ask_text"
                ) as mock_ask_text:
                    with patch(
                        "tidycode.core.pyproject.utils.key_actions.print_success"
                    ) as mock_print_success:
                        # Mock available keys
                        mock_get_keys.return_value = ["key1", "key2"]

                        # Mock key selection
                        mock_ask_choice.return_value = "key1"

                        # Mock action choice (edit)
                        mock_ask_action.return_value = KeyActions.EDIT

                        # Mock new value input
                        mock_ask_text.return_value = "new_value"

                        select_and_handle_section_keys(section_data, Mode.FULL)

    # Verify key was updated
    assert section_data["key1"] == "new_value"

    # Verify success message was printed
    mock_print_success.assert_called_once_with("Key 'key1' updated to 'new_value'")


def test_select_and_handle_section_keys_hide_sensitive():
    """
    Scenario:
        Select and handle section keys with sensitive key hiding.

    Expected:
        get_keys is called with hide_sensitive=True.
    """
    section_data = {"key1": "value1"}

    with patch("tidycode.core.pyproject.utils.key_actions.get_keys") as mock_get_keys:
        with patch(
            "tidycode.core.pyproject.utils.key_actions.ask_choice"
        ) as mock_ask_choice:
            with patch(
                "tidycode.core.pyproject.utils.key_actions.ask_action"
            ) as mock_ask_action:
                with patch("tidycode.core.pyproject.utils.key_actions.ask_text"):
                    with patch(
                        "tidycode.core.pyproject.utils.key_actions.print_success"
                    ):
                        # Mock available keys
                        mock_get_keys.return_value = ["key1"]

                        # Mock user choices
                        mock_ask_choice.return_value = "key1"
                        mock_ask_action.return_value = "edit"

                        select_and_handle_section_keys(
                            section_data, Mode.FULL, hide_sensitive=True
                        )

    # Verify get_keys was called with hide_sensitive=True
    mock_get_keys.assert_called_once_with(section_data, hide_sensitive=True)


def test_select_and_handle_section_keys_show_sensitive():
    """
    Scenario:
        Select and handle section keys without sensitive key hiding.

    Expected:
        get_keys is called with hide_sensitive=False.
    """
    section_data = {"key1": "value1"}

    with patch("tidycode.core.pyproject.utils.key_actions.get_keys") as mock_get_keys:
        with patch(
            "tidycode.core.pyproject.utils.key_actions.ask_choice"
        ) as mock_ask_choice:
            with patch(
                "tidycode.core.pyproject.utils.key_actions.ask_action"
            ) as mock_ask_action:
                with patch("tidycode.core.pyproject.utils.key_actions.ask_text"):
                    with patch(
                        "tidycode.core.pyproject.utils.key_actions.print_success"
                    ):
                        # Mock available keys
                        mock_get_keys.return_value = ["key1"]

                        # Mock user choices
                        mock_ask_choice.return_value = "key1"
                        mock_ask_action.return_value = "edit"

                        select_and_handle_section_keys(
                            section_data, Mode.FULL, hide_sensitive=False
                        )

    # Verify get_keys was called with hide_sensitive=False
    mock_get_keys.assert_called_once_with(section_data, hide_sensitive=False)
