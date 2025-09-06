"""
Types for the runner.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from tidycode.utils import BaseEnum


@dataclass
class SubprocessResult:
    """
    Subprocess result.
    """

    display_name: str
    status: str
    stdout: str = ""
    stderr: str = ""
    category: Optional[str] = None
    summary: Optional[str] = None
    details: Optional[str] = None


class SubprocessDisplayMode(BaseEnum):
    """Subprocess display mode"""

    TABLE_FULL = "table_full"
    TABLE_MINIMAL = "table_minimal"
    TEXT = "text"
    LIST = "list"


@dataclass
class CommandSpec:
    """Command specification"""

    command: List[str]
    display_name: Optional[str]
    cwd: Optional[Path]
    is_tool: bool
