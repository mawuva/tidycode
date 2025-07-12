"""
Metadata for dev tools (used in hooks, pyproject.toml injection, etc.)
"""

TOOLS_METADATA = {
    "commitizen": {
        "pyproject_config": {
            "tool": {
                "commitizen": {
                    "name": "cz_conventional_commits",
                    "version": "0.1.0",
                    "tag_format": "v$version"
                }
            }
        }
    },
    "linting": {
        "pyproject_config": {
            "tool": {
                "ruff": {
                    "line-length": 88,
                    "select": ["E", "F", "W", "I"],
                    "ignore": ["E501"]
                }
            }
        }
    },
    "format_black": {
        "pyproject_config": {
            "tool": {
                "black": {
                    "line-length": 88,
                    "target-version": ["py38"]
                }
            }
        }
    },
    "format_isort": {
        "pyproject_config": {
            "tool": {
                "isort": {
                    "profile": "black",
                    "line_length": 88
                }
            }
        }
    }
}
