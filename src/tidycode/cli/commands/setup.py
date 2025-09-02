"""
TidyCode CLI setup commands.
"""

import typer

from tidycode.utils import print_info


def register_commands(app: typer.Typer) -> None:

    @app.command(name="init", help="Initialize TidyCode.")
    def setup() -> None:
        print_info("Initializing TidyCode...")
        pass
