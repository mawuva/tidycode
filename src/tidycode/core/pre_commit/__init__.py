"""
Pre-commit core.
"""

from .helpers import normalize_pre_commit_file
from .manager import PreCommitManager

__all__ = ["normalize_pre_commit_file", "PreCommitManager"]
