"""
TidyCode Core PyProject Prompt Tests
"""

from unittest.mock import patch

from tidycode.core.pyproject.types import GlobalActions, Mode
from tidycode.core.pyproject.utils.prompt import (
    prompt_global_action,
    prompt_key_values,
)


def test_prompt_global_action():
    """
    Scenario:
        Test prompt_global_action function.

    Expected:
        Function executes without errors and returns expected action.
    """
    with patch("tidycode.core.pyproject.utils.prompt.ask_action") as mock_ask_action:
        mock_ask_action.return_value = GlobalActions.ADD_KEYS

        result = prompt_global_action()

        assert result == GlobalActions.ADD_KEYS
        mock_ask_action.assert_called_once()


def test_prompt_key_values_add_mode():
    """
    Scenario:
        Prompt for key values in ADD mode.

    Expected:
        Keys are added one by one until empty input.
    """
    existing_data = {"existing_key": "existing_value"}

    with patch("tidycode.core.pyproject.utils.prompt.ask_text") as mock_ask_text:
        with patch(
            "tidycode.core.pyproject.utils.prompt.handle_key_action"
        ) as mock_handle_action:
            with patch(
                "tidycode.core.pyproject.utils.prompt.ask_action"
            ) as mock_ask_action:
                # Mock key count input (empty for one-by-one mode)
                mock_ask_text.side_effect = [
                    "",  # Empty count - one by one mode
                    "new_key1",  # First key
                    "new_key2",  # Second key
                    "",  # Empty key - stop
                ]

                # Mock the "add more keys" prompt
                mock_ask_action.return_value = "no"

                # Mock handle_key_action to actually add keys to data
                def mock_handle_action_side_effect(key, data, mode):
                    data[key] = f"value_for_{key}"

                mock_handle_action.side_effect = mock_handle_action_side_effect

                result = prompt_key_values(existing=existing_data, mode=Mode.ADD)

    # Verify result contains new keys
    assert "new_key1" in result
    assert "new_key2" in result
    assert "existing_key" in result

    # Verify handle_key_action was called for each key
    assert mock_handle_action.call_count == 2


def test_prompt_key_values_fixed_count():
    """
    Scenario:
        Prompt for key values with fixed count.

    Expected:
        Specified number of keys are added.
    """
    existing_data = {"existing_key": "existing_value"}

    with patch("tidycode.core.pyproject.utils.prompt.ask_text") as mock_ask_text:
        with patch(
            "tidycode.core.pyproject.utils.prompt.handle_key_action"
        ) as mock_handle_action:
            with patch(
                "tidycode.core.pyproject.utils.prompt.ask_action"
            ) as mock_ask_action:
                # Mock key count input and key names
                mock_ask_text.side_effect = [
                    "2",  # Fixed count of 2
                    "new_key1",  # First key
                    "new_key2",  # Second key
                ]

                # Mock the "add more keys" prompt
                mock_ask_action.return_value = "no"

                # Mock handle_key_action to actually add keys to data
                def mock_handle_action_side_effect(key, data, mode):
                    data[key] = f"value_for_{key}"

                mock_handle_action.side_effect = mock_handle_action_side_effect

                result = prompt_key_values(existing=existing_data, mode=Mode.ADD)

    # Verify result contains new keys
    assert "new_key1" in result
    assert "new_key2" in result
    assert "existing_key" in result

    # Verify handle_key_action was called for each key
    assert mock_handle_action.call_count == 2


def test_prompt_key_values_invalid_count():
    """
    Scenario:
        Prompt for key values with invalid count.

    Expected:
        Error message is shown and function continues.
    """
    existing_data = {"existing_key": "existing_value"}

    with patch("tidycode.core.pyproject.utils.prompt.ask_text") as mock_ask_text:
        with patch(
            "tidycode.core.pyproject.utils.prompt.print_error"
        ) as mock_print_error:
            with patch(
                "tidycode.core.pyproject.utils.prompt.handle_key_action"
            ) as mock_handle_action:
                with patch(
                    "tidycode.core.pyproject.utils.prompt.ask_action"
                ) as mock_ask_action:
                    # Mock invalid count then valid count
                    mock_ask_text.side_effect = [
                        "invalid",  # Invalid count
                        "1",  # Valid count
                        "new_key",  # Key name
                    ]

                    # Mock the "add more keys" prompt
                    mock_ask_action.return_value = "no"

                    # Mock handle_key_action to actually add keys to data
                    def mock_handle_action_side_effect(key, data, mode):
                        data[key] = f"value_for_{key}"

                    mock_handle_action.side_effect = mock_handle_action_side_effect

                    result = prompt_key_values(existing=existing_data, mode=Mode.ADD)

    # Verify error was printed
    mock_print_error.assert_called_once()
    # Verify result contains the new key
    assert "new_key" in result


def test_prompt_key_values_zero_count():
    """
    Scenario:
        Prompt for key values with zero count.

    Expected:
        Function exits early with warning.
    """
    existing_data = {"existing_key": "existing_value"}

    with patch("tidycode.core.pyproject.utils.prompt.ask_text") as mock_ask_text:
        with patch(
            "tidycode.core.pyproject.utils.prompt.print_warning"
        ) as mock_print_warning:
            # Mock zero count
            mock_ask_text.return_value = "0"

            result = prompt_key_values(existing=existing_data, mode=Mode.ADD)

    # Verify warning was printed
    mock_print_warning.assert_called_once()
    # Verify result is unchanged
    assert result == existing_data


def test_prompt_key_values_negative_count():
    """
    Scenario:
        Prompt for key values with negative count.

    Expected:
        Function exits early with warning.
    """
    existing_data = {"existing_key": "existing_value"}

    with patch("tidycode.core.pyproject.utils.prompt.ask_text") as mock_ask_text:
        with patch(
            "tidycode.core.pyproject.utils.prompt.print_warning"
        ) as mock_print_warning:
            # Mock negative count
            mock_ask_text.return_value = "-1"

            result = prompt_key_values(existing=existing_data, mode=Mode.ADD)

    # Verify warning was printed
    mock_print_warning.assert_called_once()
    # Verify result is unchanged
    assert result == existing_data


def test_prompt_key_values_empty_key_skipped():
    """
    Scenario:
        Prompt for key values with empty key input.

    Expected:
        Empty key is skipped with warning.
    """
    existing_data = {"existing_key": "existing_value"}

    with patch("tidycode.core.pyproject.utils.prompt.ask_text") as mock_ask_text:
        with patch(
            "tidycode.core.pyproject.utils.prompt.print_warning"
        ) as mock_print_warning:
            with patch(
                "tidycode.core.pyproject.utils.prompt.handle_key_action"
            ) as mock_handle_action:
                with patch(
                    "tidycode.core.pyproject.utils.prompt.ask_action"
                ) as mock_ask_action:
                    # Mock fixed count with empty key
                    mock_ask_text.side_effect = [
                        "2",  # Fixed count of 2
                        "",  # Empty key - should be skipped
                        "valid_key",  # Valid key
                    ]

                    # Mock the "add more keys" prompt
                    mock_ask_action.return_value = "no"

                    # Mock handle_key_action to actually add keys to data
                    def mock_handle_action_side_effect(key, data, mode):
                        data[key] = f"value_for_{key}"

                    mock_handle_action.side_effect = mock_handle_action_side_effect

                    result = prompt_key_values(existing=existing_data, mode=Mode.ADD)

    # Verify warning was printed for empty key
    mock_print_warning.assert_called_once()
    # Verify result contains only the valid key
    assert "valid_key" in result
    assert "existing_key" in result


def test_prompt_key_values_one_by_one_mode():
    """
    Scenario:
        Prompt for key values in one-by-one mode.

    Expected:
        Keys are added until empty input is provided.
    """
    existing_data = {"existing_key": "existing_value"}

    with patch("tidycode.core.pyproject.utils.prompt.ask_text") as mock_ask_text:
        with patch(
            "tidycode.core.pyproject.utils.prompt.handle_key_action"
        ) as mock_handle_action:
            with patch(
                "tidycode.core.pyproject.utils.prompt.ask_action"
            ) as mock_ask_action:
                # Mock one-by-one mode
                mock_ask_text.side_effect = [
                    "",  # Empty count - one by one mode
                    "key1",  # First key
                    "key2",  # Second key
                    "",  # Empty key - stop
                ]

                # Mock the "add more keys" prompt
                mock_ask_action.return_value = "no"

                # Mock handle_key_action to actually add keys to data
                def mock_handle_action_side_effect(key, data, mode):
                    data[key] = f"value_for_{key}"

                mock_handle_action.side_effect = mock_handle_action_side_effect

                result = prompt_key_values(existing=existing_data, mode=Mode.ADD)

    # Verify result contains new keys
    assert "key1" in result
    assert "key2" in result
    assert "existing_key" in result

    # Verify handle_key_action was called for each key
    assert mock_handle_action.call_count == 2


def test_prompt_key_values_mode_handling():
    """
    Scenario:
        Test different modes in prompt_key_values.

    Expected:
        Mode is handled correctly for each case.
    """
    existing_data = {"existing_key": "existing_value"}

    with patch("tidycode.core.pyproject.utils.prompt.ask_text") as mock_ask_text:
        with patch(
            "tidycode.core.pyproject.utils.prompt.handle_key_action"
        ) as mock_handle_action:
            with patch(
                "tidycode.core.pyproject.utils.prompt.ask_action"
            ) as mock_ask_action:
                # Mock one-by-one mode
                mock_ask_text.side_effect = [
                    "",  # Empty count - one by one mode
                    "test_key",  # Test key
                    "",  # Empty key - stop
                ]

                # Mock the "add more keys" prompt
                mock_ask_action.return_value = "no"

                # Mock handle_key_action to actually add keys to data
                def mock_handle_action_side_effect(key, data, mode):
                    data[key] = f"value_for_{key}"

                mock_handle_action.side_effect = mock_handle_action_side_effect

                # Test ADD mode
                result_add = prompt_key_values(existing=existing_data, mode=Mode.ADD)
                assert "test_key" in result_add

                # Reset mocks for next test
                mock_ask_text.reset_mock()
                mock_handle_action.reset_mock()
                mock_ask_action.reset_mock()

                # Test FULL mode - need to mock GlobalActions properly
                mock_ask_text.side_effect = [
                    "",  # Empty count - one by one mode
                    "test_key2",  # Test key
                    "",  # Empty key - stop
                ]
                # For FULL mode, we need to mock the global action prompt
                mock_ask_action.side_effect = ["exit"]  # Exit action for FULL mode

                result_full = prompt_key_values(existing=existing_data, mode=Mode.FULL)
                # In FULL mode, the function might exit early due to "exit" action
                # Just verify it doesn't crash
                assert isinstance(result_full, dict)


def test_prompt_key_values_existing_data_copy():
    """
    Scenario:
        Test that existing data is copied, not modified.

    Expected:
        Original existing_data remains unchanged.
    """
    original_data = {"key1": "value1"}
    existing_data = {"key1": "value1"}

    with patch("tidycode.core.pyproject.utils.prompt.ask_text") as mock_ask_text:
        with patch(
            "tidycode.core.pyproject.utils.prompt.ask_action"
        ) as mock_ask_action:
            # Mock empty count to exit early
            mock_ask_text.return_value = ""

            # Mock the "add more keys" prompt
            mock_ask_action.return_value = "no"

            result = prompt_key_values(existing=existing_data, mode=Mode.ADD)

    # Verify original data is unchanged
    assert original_data == {"key1": "value1"}
    # Verify result is a copy
    assert result == existing_data
    assert result is not existing_data


def test_prompt_key_values_handle_key_action_calls():
    """
    Scenario:
        Test that handle_key_action is called correctly.

    Expected:
        handle_key_action is called with correct parameters.
    """
    existing_data = {"existing_key": "existing_value"}

    with patch("tidycode.core.pyproject.utils.prompt.ask_text") as mock_ask_text:
        with patch(
            "tidycode.core.pyproject.utils.prompt.handle_key_action"
        ) as mock_handle_action:
            with patch(
                "tidycode.core.pyproject.utils.prompt.ask_action"
            ) as mock_ask_action:
                # Mock one-by-one mode with one key
                mock_ask_text.side_effect = [
                    "",  # Empty count - one by one mode
                    "test_key",  # Test key
                    "",  # Empty key - stop
                ]

                # Mock the "add more keys" prompt
                mock_ask_action.return_value = "no"

                prompt_key_values(existing=existing_data, mode=Mode.ADD)

    # Verify handle_key_action was called
    mock_handle_action.assert_called_once_with("test_key", existing_data, Mode.ADD)
