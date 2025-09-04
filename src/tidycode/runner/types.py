"""
Types for the runner.
"""

from dataclasses import dataclass
from typing import Optional


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


