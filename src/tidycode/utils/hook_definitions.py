"""
Hook definitions
"""

HOOKS = {
    "commitizen": {
        "name": "Commitizen (conventional commits)",
    },
    "linting": {
        "name": "Ruff Linter",
        "yaml": {
            "repo": "https://github.com/charliermarsh/ruff-pre-commit",
            "rev": "v0.3.7",
            "hooks": [{"id": "ruff"}]
        }
    },
    "format_black": {
        "name": "Black Formatter",
        "yaml": {
            "repo": "https://github.com/psf/black",
            "rev": "24.3.0",
            "hooks": [{"id": "black"}]
        }
    },
    "format_isort": {
        "name": "isort Import Sorter",
        "yaml": {
            "repo": "https://github.com/pre-commit/mirrors-isort",
            "rev": "v5.12.0",
            "hooks": [{"id": "isort"}]
        }
    },
}
