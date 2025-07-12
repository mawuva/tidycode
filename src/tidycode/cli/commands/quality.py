"""
Quality commands.
"""

from pathlib import Path
import typer
from tidycode.core.bootstrap.setup_tools import setup_tool_from_metadata
from tidycode.core.quality_tools import run_black
from tidycode.utils import PYPROJECT_PATH

app = typer.Typer(help="Code quality commands")


@app.command("setup-black")
def setup_black(
    pyproject: Path = PYPROJECT_PATH,
    update_if_exists: bool = typer.Option(False),
    dry_run: bool = typer.Option(False),
):
    """Inject black config into pyproject.toml"""
    success = setup_tool_from_metadata(
        key="format_black",
        pyproject_path=pyproject,
        update_if_exists=update_if_exists,
        dry_run=dry_run,
    )
    if not success:
        raise typer.Exit(code=1)


@app.command()
def format(
    path: Path = typer.Argument(Path("."), help="Path to run black on."),
    check: bool = typer.Option(False, "--check", help="Only check without modifying."),
):
    """Run Black formatter."""
    success = run_black(path=path, check=check)
    if not success:
        raise typer.Exit(code=1)
