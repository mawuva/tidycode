"""
Utils functions
"""
import subprocess
from pathlib import Path
from typing import List, Tuple
import questionary

def run_command(command: list[str], check: bool = True) -> None:
    """Wrapper around subprocess.run with print."""
    print(f"📦 Running: {' '.join(command)}")
    subprocess.run(command, check=check)

def write_file_if_missing(path: Path, content: str) -> bool:
    """Write a file if it doesn't exist."""
    if not path.exists():
        with path.open("w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        print(f"✅ File created: {path}")
        return True
    else:
        print(f"⚠️  File already exists: {path}")
        return False
    
def ask_checkbox(message: str, choices: List[Tuple[str, str]]) -> List[str]:
    """Ask a checkbox question."""
    q_choices = [questionary.Choice(title=name, value=value) for value, name in choices]
    return questionary.checkbox(message, choices=q_choices).ask() or []

def ask_confirm(message: str) -> bool:
    """Ask a confirm question."""
    return questionary.confirm(message).ask()

