"""
TidyCode CLI setup commands.
"""

import typer

from tidycode.core.pyproject import load_default_tools
from tidycode.core.toml import TomlFileManager
from tidycode.settings import PYPROJECT_FILE_PATH
from tidycode.utils import print_info

pyproject_manager = TomlFileManager(PYPROJECT_FILE_PATH)


def register_commands(app: typer.Typer) -> None:

    @app.command(name="init", help="Initialize TidyCode.")
    def setup() -> None:
        print_info("Initializing TidyCode...")

        load_default_tools(pyproject_manager)
