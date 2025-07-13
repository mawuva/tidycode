"""
Test commitizen commands
"""

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from tidycode.cli.main import app

runner = CliRunner()


def test_commitizen_setup(tmp_path):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text('[tool.poetry]\nname = "demo"\n')

    result = runner.invoke(app, ["commitizen", "setup", "--pyproject", str(pyproject)])
    print(result.output)
    assert result.exit_code == 0
    assert "[tool.commitizen]" in pyproject.read_text()


@patch("subprocess.run")
def test_cz_init(mock_run):
    mock_run.return_value = MagicMock(returncode=0)
    result = runner.invoke(app, ["commitizen", "init", "--yes"])
    assert result.exit_code == 0
    mock_run.assert_called()
    called_args, called_kwargs = mock_run.call_args
    assert called_args[0] == [
        "cz",
        "init",
        "--name",
        "cz_conventional_commits",
        "--yes",
    ]
    assert called_kwargs.get("check") is True


@patch("subprocess.run")
def test_cz_changelog(mock_run):
    mock_run.return_value = MagicMock(returncode=0)
    result = runner.invoke(app, ["commitizen", "changelog"])
    assert result.exit_code == 0
    mock_run.assert_called_with(["cz", "changelog"], cwd=Path("."), check=True)


@patch("subprocess.run")
def test_cz_changelog_with_tag(mock_run):
    mock_run.return_value = MagicMock(returncode=0)
    result = runner.invoke(app, ["commitizen", "changelog", "--tag", "v1.2.3"])
    assert result.exit_code == 0
    mock_run.assert_called_with(
        ["cz", "changelog", "--tag", "v1.2.3"], cwd=Path("."), check=True
    )


@patch("subprocess.run")
def test_cz_bump(mock_run):
    mock_run.return_value = MagicMock(returncode=0)
    result = runner.invoke(app, ["commitizen", "bump", "--yes", "--no-verify"])
    assert result.exit_code == 0
    mock_run.assert_called_with(
        ["cz", "bump", "--no-verify", "--yes"], cwd=Path("."), check=True
    )


@patch("subprocess.run")
def test_cz_check(mock_run, tmp_path):
    mock_run.return_value = MagicMock(returncode=0)
    commit_msg_file = tmp_path / "COMMIT_EDITMSG"
    commit_msg_file.write_text("feat: add new feature")
    result = runner.invoke(app, ["commitizen", "check", str(commit_msg_file)])
    assert result.exit_code == 0
    mock_run.assert_called()
    called_args, called_kwargs = mock_run.call_args
    assert called_args[0] == ["cz", "check", "--commit-msg-file", str(commit_msg_file)]
    assert called_kwargs.get("check") is True


@patch("subprocess.run")
def test_cz_command_failure(mock_run):
    mock_run.side_effect = subprocess.CalledProcessError(1, ["cz", "bump"])
    result = runner.invoke(app, ["commitizen", "bump"])
    assert result.exit_code != 0
    assert "Commitizen command failed" in result.stderr
