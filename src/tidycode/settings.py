"""
TidyCode settings.
"""

from pathlib import Path

from tidycode.utils import BaseEnum

PYPROJECT_FILE_PATH = Path("pyproject.toml")
PRE_COMMIT_FILE_PATH = Path(".pre-commit-config.yaml")


class YesNo(BaseEnum):
    """Yes/No type actions"""

    YES = "yes"
    NO = "no"
