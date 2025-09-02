"""
Default tools for the pyproject.toml file.
"""

from typing import Any, Dict

from tidycode.core.pyproject.sections import add_config_section
from tidycode.core.toml import TomlFileManager
from tidycode.plugins.config import DictPlugin
from tidycode.settings import ToolsSupported
from tidycode.utils import print_info

DEFAULT_TOOLS_CONFIG: Dict[str, Dict[str, Any]] = {
    "tidycode": {
        "name": "TidyCode",
        "description": (
            "A tool to keep your Python projects clean and secure (format, lint, test, etc.)"
        ),
        "config": {
            "target": ".",
            "check-only": False,
            "verbose": False,
            "tools": ToolsSupported.to_list(),
            "clean": {
                "target": ".",
                "cleanable_dirs": [
                    "__pycache__",
                    ".pytest_cache",
                    ".ruff_cache",
                    ".mypy_cache",
                    ".tox",
                    "build",
                    "dist",
                ],
                "cleanable_files": [
                    ".coverage",
                    "coverage.xml",
                ],
                "patterns": [
                    "*.pyc",
                    "*.log",
                ],
                "excludes": [
                    "docs",
                    "migrations",
                ],
            },
        },
    },
    "black": {
        "name": "Black",
        "description": "The uncompromising Python code formatter",
        "config": {
            "line-length": 88,
            "target-version": ["py310"],
            "skip-string-normalization": False,
            "preview": True,
        },
    },
    "ruff": {
        "name": "Ruff",
        "description": "A fast Python linter, compatible with Flake8 rules",
        "config": {
            "line-length": 88,
            "target-version": "py310",
            "exclude": [
                "migrations",
                ".venv",
                "venv",
                "env",
                ".env",
                ".bzr",
                ".direnv",
                ".eggs",
                ".git",
                ".git-rewrite",
                ".hg",
                ".ipynb_checkpoints",
                ".mypy_cache",
                ".nox",
                ".pants.d",
                ".pyenv",
                ".pytest_cache",
                ".pytype",
                ".ruff_cache",
                ".svn",
                ".tox",
                ".venv",
                ".vscode",
                "__pypackages__",
                "_build",
                "buck-out",
                "build",
                "dist",
                "node_modules",
                "site-packages",
            ],
            "lint": {
                "select": ["E", "F", "W", "I"],
                "ignore": ["E501"],
                "fixable": ["ALL"],
            },
            "format": {
                "quote-style": "double",
                "skip-magic-trailing-comma": False,
                "line-ending": "auto",
            },
        },
    },
    "isort": {
        "name": "isort",
        "description": "Python utility for sorting imports",
        "config": {
            "profile": "black",
            "line_length": 88,
        },
    },
}


def load_default_tools(manager: TomlFileManager) -> None:
    """Load default tools into the pyproject.toml file."""
    for tool_name, tool_data in DEFAULT_TOOLS_CONFIG.items():
        print_info(f"Loading default tool: {tool_name}")

        config: Dict[str, Any] = tool_data["config"]

        add_config_section(
            manager=manager,
            section_name=tool_name,
            prefix="tool.",
            display_label="tool",
            plugin=DictPlugin(tool_name, config),
            interactive=False,
        )
