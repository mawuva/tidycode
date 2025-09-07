"""
TidyCode Printing Utilities
"""

import shutil

import pyfiglet
import typer

from tidycode.settings import PrettyHeaderStyle

SCOPE_STYLES = {
    "style": {"icon": "✨", "color": typer.colors.CYAN},
    "type": {"icon": "🧩", "color": typer.colors.MAGENTA},
    "security": {"icon": "🛡", "color": typer.colors.RED},
    "complexity": {"icon": "📊", "color": typer.colors.YELLOW},
    "default": {"icon": "🔍", "color": typer.colors.GREEN},
    "clean": {"icon": "🧹", "color": typer.colors.BLUE},
}


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
    Wrapper around typer.secho with color, prefix and space management.
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
# Helpers specialized
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


def pretty_header(
    scope: str,
    message: str,
    style: PrettyHeaderStyle = PrettyHeaderStyle.BOX,
    font: str = "slant",
    err: bool = False,
) -> None:
    """
    Pretty print a header for CLI with two styles:
    - box: Full screen box
    - figlet: ASCII art with pyfiglet
    """
    terminal_width = shutil.get_terminal_size((80, 20)).columns
    meta = SCOPE_STYLES.get(scope, SCOPE_STYLES["default"])
    icon, color = meta["icon"], meta["color"]

    text = f"{icon} {message} {icon}"

    if style == PrettyHeaderStyle.BOX:
        border = "─" * (terminal_width - 2)
        typer.secho("╭" + border + "╮", fg=color, bold=True, err=err)
        typer.secho(text.center(terminal_width), fg=color, bold=True, err=err)
        typer.secho("╰" + border + "╯", fg=color, bold=True, err=err)

    elif style == PrettyHeaderStyle.BANNER:
        padding = (terminal_width - len(text)) // 2
        line = f"{'═' * padding}{text}{'═' * (terminal_width - len(text) - padding)}"
        typer.secho(line, fg=color, bold=True, err=err)

    elif style == PrettyHeaderStyle.ALERT:
        line = "!" * terminal_width
        typer.secho(line, fg=color, bold=True, err=err)
        typer.secho(text.center(terminal_width), fg=color, bold=True, err=err)
        typer.secho(line, fg=color, bold=True, err=err)

    elif style == PrettyHeaderStyle.FIGLET:
        ascii_art = pyfiglet.figlet_format(message, width=terminal_width)
        typer.secho(ascii_art, fg=color, bold=True, err=err)

    else:  # fallback
        typer.secho(text, fg=color, bold=True, err=err)
