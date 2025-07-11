"""
Setup Commitizen
"""

from pathlib import Path
from tidycode.utils import HOOKS, PYPROJECT, run_command

def setup_commitizen(pyproject_path: Path = PYPROJECT):
    if not pyproject_path.exists():
        print("❌ pyproject.toml not found")
        return False
    
    content = pyproject_path.read_text(encoding="utf-8")

    if "[tool.commitizen]" in content:
        print("⚠️ Commitizen already present in pyproject.toml")
        return False

    new_config = HOOKS["commitizen"]["config"]
    content += "\n" + new_config
    pyproject_path.write_text(content.strip() + "\n", encoding="utf-8")
    print("✅ Commitizen config added to pyproject.toml")

    try:
        run_command(["cz", "init", "--name", "cz_conventional_commits", "--yes"])
    except Exception as e:
        print(f"⚠️ Commitizen CLI init failed: {e}")
    return True


