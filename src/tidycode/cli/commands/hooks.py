"""
Hooks commands
"""

from pathlib import Path
import typer

from tidycode.core.bootstrap import setup_hooks, setup_hooks_minimal

app = typer.Typer(help="Setup hooks")

@app.command("setup")
def setup(config_path: Path = Path(".pre-commit-config.yaml")):
    """Run interactive hook setup"""
    setup_hooks(config_path=config_path)

@app.command("setup-minimal")
def setup_minimal(config_path: Path = Path(".pre-commit-config.yaml")):
    """Run minimal hook setup"""
    setup_hooks_minimal(config_path=config_path)

