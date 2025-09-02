"""
Commands for the pyproject.toml file.
"""

import typer

from tidycode.core.pyproject.sections import add_config_section
from tidycode.core.toml import TomlFileManager
from tidycode.settings import PYPROJECT_FILE_PATH

app = typer.Typer(
    help="Manage the pyproject.toml file",
    no_args_is_help=True,
)

pyproject_manager = TomlFileManager(PYPROJECT_FILE_PATH)


@app.command("add-section", help="Add a new section in the pyproject.toml")
def add_section(
    section_name: str = typer.Argument(None, help="The section name to add")
):
    """
    Add a new section interactively to the pyproject.toml file and log all changes.
    """

    add_config_section(pyproject_manager, section_name)
