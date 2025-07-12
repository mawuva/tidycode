"""
Manage project configuration files like pyproject.toml
"""

import typer
from pathlib import Path
from tidycode.utils import (
    load_pyproject,
    diff_pyproject_config,
    format_pyproject_diff_plaintext,
    PYPROJECT,
    remove_tool_section_and_return,
    save_pyproject,
)

app = typer.Typer(help="Manage pyproject.toml and other configs")

@app.command("diff-pyproject")
def diff_pyproject(
    config_path: Path = None,
):
    """Show diff between current pyproject.toml and injected sample config"""
    config_path = config_path or PYPROJECT
    
    if not config_path.exists():
        typer.echo(f"❌ {config_path} not found")
        raise typer.Exit(1)

    base = load_pyproject(config_path)
    sample = {
        "tool": {
            "black": {"line-length": 88},
            "ruff": {"select": ["E", "F"]},
        }
    }

    diff = diff_pyproject_config(base, sample)
    if not diff:
        typer.echo("✅ No differences found.")
        raise typer.Exit()

    output = format_pyproject_diff_plaintext(diff)
    typer.echo(output)

@app.command("list-sections")
def list_sections(
    config_path: Path = None,
):
    """List sections under [tool]"""
    config_path = config_path or PYPROJECT
    
    if not config_path.exists():
        typer.echo(f"❌ {config_path} not found")
        raise typer.Exit(1)

    config = load_pyproject(config_path)
    tool = config.get("tool", {})

    if not tool:
        typer.echo("❌ No sections found under [tool].")
        raise typer.Exit(code=1)

    typer.echo("🔧 Sections under [tool]:")
    for key in sorted(tool.keys()):
        typer.echo(f" - {key}")

@app.command("show-section")
def show_section(
    section: str,
    config_path: Path = None,
):
    """Show the content of a section under [tool]"""
    config_path = config_path or PYPROJECT
    
    if not config_path.exists():
        typer.echo(f"❌ {config_path} not found")
        raise typer.Exit(1)

    config = load_pyproject(config_path)
    tool = config.get("tool", {})
    data = tool.get(section)

    if not data:
        typer.echo(f"❌ Section [tool.{section}] not found.")
        raise typer.Exit(code=1)

    typer.echo(f"[tool.{section}]")
    for key, value in data.items():
        typer.echo(f"{key} = {value!r}")

@app.command("remove-section")
def remove_section(
    section: str,
    config_path: Path = None,
):
    """Remove a section under [tool.<section>]"""
    config_path = config_path or PYPROJECT

    if not config_path.exists():
        typer.echo(f"❌ {config_path} not found")
        raise typer.Exit(1)

    pyproject = load_pyproject(config_path)
    original_sections = list(pyproject.get("tool", {}).keys())
    
    pyproject = remove_tool_section_and_return(pyproject, section)
    new_sections = list(pyproject.get("tool", {}).keys())

    if section not in original_sections:
        typer.echo(f"⚠️ Section [tool.{section}] not found in pyproject.toml")
        raise typer.Exit(code=1)

    save_pyproject(pyproject, config_path)
    typer.echo(f"🗑️ Removed section: [tool.{section}]")
