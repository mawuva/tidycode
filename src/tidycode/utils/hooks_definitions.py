"""
Hook definitions
"""

HOOKS = {
    "pre-commit": {
        "name": "Pre-commit",
        "yaml": {
            "repo": "https://github.com/pre-commit/pre-commit-hooks",
            "rev": "v5.0.0",
            "hooks": [
                {"id": "trailing-whitespace"},
                {"id": "end-of-file-fixer"},
                {"id": "check-yaml"},
                {"id": "check-added-large-files"},
                {"id": "name-tests-test"},
            ]
        }
    },
    "commitizen": {
        "name": "Commitizen (conventional commits)",
        "yaml": {
            "repo": "https://github.com/commitizen-tools/commitizen",
            "rev": "v4.8.3",
            "hooks": [
                {"id": "commitizen"},
                {
                    "id": "commitizen-branch",
                    "stages": ["pre-push"],
                },
            ]
        }
    },
    "commitizen-message": {
        "name": "Commitizen Message",
        "yaml": {
            "repo": "local",
            "hooks": [
                {
                    "id": "commitizen-message-check",
                    "name": "Commitizen message check",
                    "entry": "cz check -- --commit-msg-file",
                    "language": "system",
                    "stages": "[commit-msg]",
                    "args": ["{commit_msg_file}"],
                }
            ],
        }
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
