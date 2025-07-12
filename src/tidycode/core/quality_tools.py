"""
Quality tools.
"""

from pathlib import Path
import subprocess
from tidycode.utils import run_command


def run_black(path: Path = Path("."), check: bool = False) -> bool:
    """
    Run black formatter.

    Args:
        path (Path): Directory or file to format (default: current directory).
        check (bool): If True, only check for formatting without modifying.

    Returns:
        bool: True if success, False otherwise.
    """
    command = ["black", str(path)]
    if check:
        command.append("--check")

    try:
        run_command(command, check=True)
        print("✅ Formatting succeeded.")
        return True
    except subprocess.CalledProcessError:
        print("❌ Formatting failed.")
        return False
