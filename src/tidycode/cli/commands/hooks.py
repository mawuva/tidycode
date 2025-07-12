"""
Hooks commands
"""

from pathlib import Path
import typer

from tidycode.core.bootstrap import setup_hooks, setup_hooks_minimal
from tidycode.utils import (
    run_command,
    load_config,
    get_installed_hook_keys,
    HOOKS,
    CONFIG_FILE,
    remove_hooks,
    save_config,
    print_msg,
    add_hooks,
)

app = typer.Typer(help="Setup hooks")

@app.command("setup")
def setup(config_path: Path = Path(".pre-commit-config.yaml")):
    """Run interactive hook setup"""
    setup_hooks(config_path=config_path)

@app.command("setup-minimal")
def setup_minimal(config_path: Path = Path(".pre-commit-config.yaml")):
    """Run minimal hook setup"""
    setup_hooks_minimal(config_path=config_path)

@app.command()
def install():
    """Install them into .git/hooks"""
    typer.echo("🔧 Installing hooks...")
    run_command(["pre-commit", "install"])
    typer.echo("✅ Hooks installed.")

@app.command()
def uninstall():
    """Uninstall hooks from .git/hooks"""
    run_command(["pre-commit", "uninstall"])
    typer.echo("🗑️ Hooks removed.")

@app.command()
def update():
    """Update installed hooks"""
    run_command(["pre-commit", "autoupdate"])
    typer.echo("🔄 Hooks updated.")

@app.command("list-installed")
def list_installed(config_path: Path = CONFIG_FILE):
    """List installed hooks from config"""
    config = load_config(config_path)
    keys = get_installed_hook_keys(config)
    if not keys:
        typer.echo("❌ No hooks installed in config.")
    else:
        typer.echo("✅ Installed hooks:")
        for k in keys:
            typer.echo(f" - {k}: {HOOKS[k]['name']}")

@app.command("list-available")
def list_available():
    """List all available hooks from registry"""
    typer.echo("📦 Available hooks:")
    for key, meta in HOOKS.items():
        typer.echo(f" - {key}: {meta['name']}")

@app.command()
def clean(config_path: Path = CONFIG_FILE):
    """Remove all hooks from the config file"""
    config = load_config(config_path)
    keys = get_installed_hook_keys(config)
    config = remove_hooks(config, keys)
    save_config(config, config_path)
    typer.echo(f"🧹 Removed {len(keys)} hooks from {config_path.name}.")

@app.command()
def check():
    """Run all hooks against the full project"""
    typer.echo("🔍 Running all hooks (pre-commit run --all-files)...")
    run_command(["pre-commit", "run", "--all-files"])

@app.command()
def sync(
    config_path: Path = CONFIG_FILE,
    quiet: bool = False,
    debug: bool = False,
):
    """Install hooks if none, else update"""
    print_msg(f"Loading config from {config_path}", quiet, debug)
    config = load_config(config_path)
    installed = get_installed_hook_keys(config)

    if installed:
        print_msg("Hooks installed, updating...", quiet, debug)
        run_command(["pre-commit", "autoupdate"])
        print_msg("Hooks updated.", quiet, debug)
    else:
        print_msg("No hooks installed, installing...", quiet, debug)
        keys_to_add = [k for k in HOOKS if "yaml" in HOOKS[k]]
        config = add_hooks(config, keys_to_add)
        save_config(config, config_path)
        run_command(["pre-commit", "install"])
        print_msg("Hooks installed.", quiet, debug)


@app.command()
def reset(
    config_path: Path = CONFIG_FILE,
    quiet: bool = False,
    debug: bool = False,
):
    """Remove all hooks config and uninstall hooks"""
    print_msg(f"Resetting hooks, cleaning config {config_path}...", quiet, debug)
    config = load_config(config_path)
    keys = get_installed_hook_keys(config)
    config = remove_hooks(config, keys)
    save_config(config, config_path)
    print_msg("Config cleaned.", quiet, debug)

    print_msg("Uninstalling hooks...", quiet, debug)
    run_command(["pre-commit", "uninstall"])
    print_msg("Hooks uninstalled.", quiet, debug)
