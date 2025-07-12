"""
Test configs.py
"""

from typer.testing import CliRunner
from tidycode.cli.commands.configs import app as configs_app
from tidycode.utils import load_toml_file

runner = CliRunner()

def test_diff_pyproject_empty(tmp_path):
    """
    Test that the diff is shown and the file is not updated.
    """
    path = tmp_path / "pyproject.toml"
    path.write_text("[tool.dummy]\n")

    result = runner.invoke(configs_app, ["diff-pyproject", "--config-path", str(path)])
    assert result.exit_code == 0
    assert "+ [tool.black]" in result.output
    assert "+ [tool.ruff]" in result.output


def test_list_sections(tmp_path):
    """
    Test that the sections are listed and the file is not updated.
    """
    path = tmp_path / "pyproject.toml"
    path.write_text(
        """
[tool.black]
line-length = 88

[tool.ruff]
select = ["E"]
"""
    )
    result = runner.invoke(configs_app, ["list-sections", "--config-path", str(path)])
    assert result.exit_code == 0
    assert "black" in result.output
    assert "ruff" in result.output


def test_show_section(tmp_path):
    """
    Test that the section is shown and the file is not updated.
    """
    path = tmp_path / "pyproject.toml"
    path.write_text("[tool.black]\nline-length = 88\n")

    result = runner.invoke(configs_app, ["show-section", "black", "--config-path", str(path)])
    assert result.exit_code == 0
    assert "[tool.black]" in result.output
    assert "line-length" in result.output


def test_show_section_not_found(tmp_path):
    path = tmp_path / "pyproject.toml"
    path.write_text("[tool.dummy]\n")

    result = runner.invoke(configs_app, ["show-section", "missing", "--config-path", str(path)])
    assert result.exit_code == 1
    assert "not found" in result.output


def test_remove_section(tmp_path):
    """
    Test that the section is removed and the file is updated.
    """
    path = tmp_path / "pyproject.toml"
    path.write_text(
        """
[tool.black]
line-length = 88

[tool.ruff]
select = ["E"]
"""
    )
    result = runner.invoke(configs_app, ["remove-section", "black", "--config-path", str(path)])
    assert result.exit_code == 0
    assert "Removed section" in result.output

    data = load_toml_file(path)
    assert "black" not in data["tool"]
    assert "ruff" in data["tool"]


def test_remove_section_not_found(tmp_path):
    """
    Test that the section is not found and the file is not updated.
    """
    path = tmp_path / "pyproject.toml"
    path.write_text("[tool.dummy]\n")

    result = runner.invoke(configs_app, ["remove-section", "nonexistent", "--config-path", str(path)])
    assert result.exit_code == 1
    assert "not found" in result.output


