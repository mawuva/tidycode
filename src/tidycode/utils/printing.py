"""
TidyCode Printing Utilities
"""

import typer


def pretty_print(
    message: str,
    *,
    fg: str = typer.colors.WHITE,
    bold: bool = False,
    prefix: str = "",
    padding: int = 0,
    newline_before: bool = False,
    newline_after: bool = True,
    err: bool = False,
):
    """
    Wrapper autour de typer.secho avec gestion des couleurs, préfixes et espaces.
    """
    text = message.strip()

    if prefix:
        text = f"{prefix} {text}"

    text = f"{' ' * padding}{text}{' ' * padding}"

    if newline_before:
        typer.echo()

    typer.secho(text, fg=fg, bold=bold, err=err)

    if newline_after:
        typer.echo()


# ----------------------------
# Helpers spécialisés
# ----------------------------


def print_success(message: str, **kwargs):
    pretty_print(message, fg=typer.colors.GREEN, prefix="✅", **kwargs)


def print_warning(message: str, **kwargs):
    pretty_print(message, fg=typer.colors.YELLOW, prefix="⚠️", **kwargs)


def print_error(message: str, **kwargs):
    pretty_print(message, fg=typer.colors.RED, prefix="❌", bold=True, **kwargs)


def print_info(message: str, **kwargs):
    pretty_print(message, fg=typer.colors.CYAN, prefix="ℹ️", **kwargs)


def print_title(message: str, **kwargs):
    pretty_print(
        message.upper(),
        fg=typer.colors.MAGENTA,
        bold=True,
        **kwargs,
    )
