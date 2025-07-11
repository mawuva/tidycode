"""
Run Dependabot setup
"""

from pathlib import Path
from tidycode.utils import DEPENDABOT, write_file_if_missing


DEFAULT_DEPENDABOT_YML = """
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
""".strip()


def setup_dependabot(path: Path = DEPENDABOT) -> bool:
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
    created = write_file_if_missing(path, DEFAULT_DEPENDABOT_YML)
    return created
