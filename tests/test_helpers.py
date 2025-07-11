"""
Test utils functions
"""
import subprocess

import pytest
from pytest_mock import MockerFixture

from tidycode.utils import (
    run_command,
    write_file_if_missing,
    ask_checkbox,
    ask_confirm,
)

def test_run_command_default_check(mocker: MockerFixture, capsys):
    """Test run_command with default check=True."""
    mock_run = mocker.patch("subprocess.run")
    command = ["echo", "hello"]

    run_command(command)

    mock_run.assert_called_once_with(command, check=True)
    captured = capsys.readouterr()
    assert "📦 Running: echo hello" in captured.out

def test_run_command_check_false(mocker: MockerFixture):
    """Test run_command with check=False."""
    mock_run = mocker.patch("subprocess.run")
    command = ["ls", "-la"]

    run_command(command, check=False)

    mock_run.assert_called_once_with(command, check=False)

def test_run_command_raises_error(mocker: MockerFixture):
    """Test run_command raises CalledProcessError."""
    mock_run = mocker.patch("subprocess.run")
    mock_run.side_effect = subprocess.CalledProcessError(1, ["badcommand"])

    with pytest.raises(subprocess.CalledProcessError):
        run_command(["badcommand"])

def test_write_file_if_missing(tmp_path):
    """Test the write_file_if_missing function."""
    file = tmp_path / "file.txt"
    assert write_file_if_missing(file, "abc") is True
    assert file.read_text() == "abc\n"
    # Second call returns False
    assert write_file_if_missing(file, "def") is False

def test_ask_checkbox(mocker: MockerFixture):
    """Test the ask_checkbox function."""
    mock_ask = mocker.MagicMock()
    mock_ask.ask.return_value = ["a"]
    mocker.patch("questionary.checkbox", return_value=mock_ask)

    result = ask_checkbox("Test", [("a", "A"), ("b", "B")])
    assert result == ["a"]

def test_ask_checkbox_empty_selection(mocker: MockerFixture):
    """Test ask_checkbox when user selects nothing (returns None)."""
    mock_ask = mocker.MagicMock()
    mock_ask.ask.return_value = None
    mocker.patch("questionary.checkbox", return_value=mock_ask)

    result = ask_checkbox("Test", [("a", "A"), ("b", "B")])
    assert result == []

def test_ask_confirm(mocker: MockerFixture):
    """Test the ask_confirm function."""
    mock_ask = mocker.MagicMock()
    mock_ask.ask.return_value = True
    mocker.patch("questionary.confirm", return_value=mock_ask)

    result = ask_confirm("Test")
    assert result is True

def test_ask_confirm_negative(mocker: MockerFixture):
    """Test ask_confirm when user declines (False)."""
    mock_ask = mocker.MagicMock()
    mock_ask.ask.return_value = False
    mocker.patch("questionary.confirm", return_value=mock_ask)

    result = ask_confirm("Test")
    assert result is False
