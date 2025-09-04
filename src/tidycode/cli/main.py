"""
TidyCode CLI main entry point.
"""

import typer

from tidycode.cli.commands import pyproject, quality, setup

app = typer.Typer(
    help="{🧹} tidycode - A fun and simple CLI to keep your Python projects clean and secure (format, lint, test, doctor, etc.)",
    no_args_is_help=True,
)

app.add_typer(pyproject.app, name="pyproject")
app.add_typer(quality.app, name="quality")

setup.register_commands(app)


if __name__ == "__main__":
    app()
