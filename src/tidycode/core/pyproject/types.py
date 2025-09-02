"""
Types for the pyproject module.
"""

from tidycode.utils import BaseEnum


class OverwriteChoice(BaseEnum):
    """Choice for overwriting an existing section."""

    OVERWRITE = "overwrite"
    ADD_KEYS = "add keys"
    ADD_SUBSECTION = "add subsection"
    CANCEL = "cancel"


class GlobalActions(BaseEnum):
    """Global actions for pyproject sections."""

    ADD_KEYS = "add keys"
    ADD_SUBSECTION = "add subsection"
    EDIT = "edit"
    REMOVE = "remove"
    EXIT = "exit"


class Mode(BaseEnum):
    """Mode for CLI."""

    ADD = "add"
    EDIT = "edit"
    REMOVE = "remove"
    FULL = "full"


class KeyActions(BaseEnum):
    """Actions for individual keys in a section"""

    EDIT = "edit"
    REMOVE = "remove"
    SKIP = "skip"


class PyProjectHiddenSections(BaseEnum):
    """Sections to hide in CLI (like 'project', 'tool.poetry', 'build-system')"""

    PROJECT = "project"
    POETRY = "tool.poetry"
    BUILD_SYSTEM = "build-system"


class PyProjectHiddenSubsections(BaseEnum):
    """Subsections to hide in CLI (like 'poetry')"""

    POETRY = "poetry"


class SensitiveKeys(BaseEnum):
    """Keys that can be optionally hidden in section summaries."""

    API_KEY = "api_key"
    TOKEN = "token"
    PASSWORD = "password"
    SECRET = "secret"
    BLACK = "black"
    POETRY = "poetry"


class SensitiveKeywords(BaseEnum):
    """Keywords that can be optionally hidden in section summaries."""

    POETRY = "poetry"
    BLACK = "black"
    RUFF = "ruff"
    ISORT = "isort"


class PrintSectionSummaryMode(BaseEnum):
    """Mode for printing section summaries."""

    TREE = "tree"
    LIST = "list"
    TABLE = "table"
    JSON = "json"


class RemoveSectionChoices(BaseEnum):
    """Choices for remove_section flow (remove section or skip)"""

    ENTIRE_SECTION = "entire section"
    KEYS_ONLY = "keys only"
    EXIT = "exit"
