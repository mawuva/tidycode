"""
Clean command.
"""

from typing import Optional

import typer

from tidycode.runner.types import SubprocessDisplayMode
from tidycode.modules.clean.clean_task import run_clean_task
from tidycode.utils import pretty_header
from tidycode.settings import PrettyHeaderStyle


def register_commands(app: typer.Typer) -> None:

    @app.command(name="clean", help="Clean temporary files and folders")
    def clean(
        mode: Optional[SubprocessDisplayMode] = typer.Option(
            SubprocessDisplayMode.TEXT,
            "--mode",
            "-m",
            help="Summary display mode (TABLE_FULL, TABLE_MINIMAL, TEXT, LIST)",
        ),
        dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Preview what would be deleted without actually deleting",
    ),
    target: Optional[str] = typer.Option(
        None,
        "--target",
        "-t",
        help="Override root directory to clean (CLI > pyproject)",
    ),
    exclude: Optional[str] = typer.Option(
        None,
        "--exclude",
        "-e",
        help="Comma-separated list of files/directories to exclude",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show detailed output",
    ),
    ):
        """
        Clean files/folders defined under [tool.tidycode.clean] in pyproject.toml.
        """
        excludes_list = exclude.split(",") if exclude is not None else None
        
        pretty_header(
            scope="clean",
            message="Running clean task...",
            style=PrettyHeaderStyle.FIGLET,
            err=True,
        )
        
        run_clean_task(
            summary_mode=mode,
            dry_run=dry_run,
            target=target,
            excludes=excludes_list,
            verbose=verbose,
        )


    
