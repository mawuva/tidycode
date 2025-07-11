"""
Dependabot commands
"""

import typer
from pathlib import Path
from tidycode.core.bootstrap import setup_dependabot

app = typer.Typer(help="Setup dependabot.yml")

@app.command("setup")
def setup(path: Path = Path(".github/dependabot.yml")):
    """Create dependabot.yml config"""
    setup_dependabot(path)
