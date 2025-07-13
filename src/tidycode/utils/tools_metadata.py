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
                    "target-version": "py38",
                    "exclude": [
                        "migrations",
                        ".venv",
                        "venv",
                        "env",
                        ".env",
                        "dist",
                        "build",
                    ],
                },
                "ruff.lint": {
                    "select": ["E", "F", "W", "I"],
                    "ignore": ["E501"],
                },
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
    "mypy": {
        "pyproject_config": {
            "tool": {
                "mypy": {
                    "python_version": "3.8",
                    "strict": True,
                    "ignore_missing_imports": True,
                    "disallow_untyped_defs": False,
                    "check_untyped_defs": True,
                    "no_implicit_optional": True,
                    "warn_unused_ignores": True,
                    "warn_return_any": True,
                    "warn_redundant_casts": True,
                    "warn_unused_configs": True,
                    "show_error_codes": True,
                    "pretty": True,
                }
            }
        }
    },
}
