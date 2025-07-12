"""
Test commitizen commands
"""

from typer.testing import CliRunner
from tidycode.cli.main import app

runner = CliRunner()

def test_commitizen_setup(tmp_path):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("[tool.poetry]\nname = \"demo\"\n")

    result = runner.invoke(app, ["commitizen", "setup", "--pyproject", str(pyproject)])
    assert result.exit_code == 0
    assert "[tool.commitizen]" in pyproject.read_text()
