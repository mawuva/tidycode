"""
Setup Commitizen
"""
from typing import Callable, Optional
from pathlib import Path

from tidycode.utils import (
    run_command,
    load_pyproject,
    save_pyproject,
    inject_pyproject_config,
    get_tool_section,
    PYPROJECT_PATH,
    TOOLS_METADATA
)


def setup_commitizen(
        pyproject_path: Path = None,
        dry_run: bool = False,
        run_command_fn: Callable = None,
    ) -> bool:
    """
    Injects Commitizen configuration into pyproject.toml and runs cz init.
    """
    pyproject_path = pyproject_path or PYPROJECT_PATH   
    run_command_fn = run_command_fn or run_command
    
    if not pyproject_path.exists():
        print(f"❌ {pyproject_path} not found")
        return False

    pyproject_data = load_pyproject(pyproject_path)

    # Skip if already present
    if get_tool_section(pyproject_data, "commitizen") is not None:
        print("⚠️ Commitizen already present in pyproject.toml")
        return False

    # Inject configuration
    new_config = TOOLS_METADATA["commitizen"]["pyproject_config"]
    updated = inject_pyproject_config(pyproject_data, new_config, dry_run=dry_run)

    if dry_run:
        print("🧪 Dry run enabled. Showing what would change: \n")
        from tidycode.utils import diff_pyproject_config, format_pyproject_diff_plaintext
        diffs = diff_pyproject_config(pyproject_data, updated)
        print(format_pyproject_diff_plaintext(diffs))
        return True

    # Save
    save_pyproject(updated, pyproject_path)
    print("✅ Commitizen config added to pyproject.toml")

    # Run cz init
    try:
        run_command_fn(["cz", "init", "--name", "cz_conventional_commits", "--yes"])
    except Exception as e:
        print(f"⚠️ Commitizen CLI init failed: {e}")

    return True
