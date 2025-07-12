"""
Commitizen commands
"""


import typer
from pathlib import Path
from tidycode.core.bootstrap import setup_commitizen
from tidycode.utils import PYPROJECT_PATH

app = typer.Typer(help="Setup Commitizen")

@app.command("setup")
def setup(pyproject: Path = PYPROJECT_PATH, dry_run: bool = False):
    """
    Add Commitizen config to pyproject.toml

    Args:
        pyproject (Path): Path to pyproject.toml file
        dry_run (bool): Show changes without writing to file or running commands
    """
    success = setup_commitizen(pyproject, dry_run=dry_run)
    if not success:
        raise typer.Exit(code=1)

