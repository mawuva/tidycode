"""
Commitizen commands
"""


import typer
from pathlib import Path
from tidycode.core.bootstrap import setup_commitizen

app = typer.Typer(help="Setup Commitizen")

@app.command("setup")
def setup(pyproject: Path = Path("pyproject.toml")):
    """Add Commitizen config to pyproject.toml"""
    setup_commitizen(pyproject)
