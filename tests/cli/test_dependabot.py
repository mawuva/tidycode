"""
Test dependabot commands
"""

from typer.testing import CliRunner

from tidycode.cli.main import app

runner = CliRunner()


def test_dependabot_setup(tmp_path):
    path = tmp_path / ".github" / "dependabot.yml"
    result = runner.invoke(app, ["dependabot", "setup", "--path", str(path)])
    assert result.exit_code == 0
    assert path.exists()
    assert "version: 2" in path.read_text()
