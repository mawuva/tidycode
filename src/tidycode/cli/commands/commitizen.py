"""
Commitizen commands
"""


import typer
from pathlib import Path
from tidycode.core.bootstrap import setup_commitizen
from tidycode.utils import PYPROJECT_PATH

app = typer.Typer(help="Setup Commitizen")

@app.command("setup")
def setup(pyproject: Path = None, dry_run: bool = False):
    """
    Add Commitizen config to pyproject.toml

    Args:
        pyproject (Path): Path to pyproject.toml file
        dry_run (bool): Show changes without writing to file or running commands
    """
    pyproject = pyproject or PYPROJECT_PATH
    
    try:
        success = setup_commitizen(pyproject, dry_run=dry_run)
    except Exception as e:
        print(f"Error in setup_commitizen: {e}")
        raise
    
    if not success:
        raise typer.Exit(code=1)

