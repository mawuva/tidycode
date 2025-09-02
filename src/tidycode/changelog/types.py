"""
Types for the changelog.
"""

from dataclasses import dataclass
from typing import Any

from tidycode.utils import BaseEnum


class ChangeActions(BaseEnum):
    ADDED = "added"
    EDITED = "edited"
    REMOVED = "removed"


@dataclass
class ChangeLogEntry:
    action: ChangeActions
    key_path: str
    old_value: Any = None
    new_value: Any = None
