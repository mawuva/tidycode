"""
Metadata for dev tools (used in hooks, pyproject.toml injection, etc.)
"""

from tomlkit import string

TOOLS_METADATA = {
    "commitizen": {
        "pyproject_config": {
            "tool": {
                "commitizen": {
                    "name": "cz_conventional_commits",
                    "version": "0.1.0",
                    "tag_format": "v$version",
                }
            }
        }
    },
    "ruff": {
        "pyproject_config": {
            "tool": {
                "ruff": {
                    "line-length": 88,
                    "target-version": ["py38"],
                    "select": ["E", "F", "W", "I"],
                    "ignore": ["E501"],
                    "quote-style": "double",
                    "exclude": [
                        "migrations",
                        ".venv",
                        "venv",
                        "env",
                        ".env",
                        "dist",
                        "build",
                    ],
                }
            }
        }
    },
    "black": {
        "pyproject_config": {
            "tool": {
                "black": {
                    "line-length": 88,
                    "target-version": ["py38"],
                    "skip-string-normalization": False,
                    "preview": True,
                    "exclude": string(
                        r"""
/(
    \.git
  | \.venv
  | build
  | dist
)/
""",
                        multiline=True,
                    ),
                }
            }
        }
    },
    "isort": {
        "pyproject_config": {
            "tool": {
                "isort": {
                    "profile": "black",
                    "line_length": 88,
                }
            }
        }
    },
}
