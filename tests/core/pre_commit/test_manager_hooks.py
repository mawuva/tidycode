"""
TidyCode Pre-commit Manager Hooks Management Tests
"""

from tidycode.core.pre_commit.manager import PreCommitManager
from tidycode.core.yaml import save_yaml_file


def test_list_hooks_empty_repos(tmp_path):
    """
    Scenario:
        List hooks from a pre-commit file with empty repos.

    Expected:
        Returns empty list.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(file_path, {"repos": []})

    manager = PreCommitManager(file_path)
    hooks = manager.list_hooks()
    assert hooks == []


def test_list_hooks_with_hooks(tmp_path):
    """
    Scenario:
        List hooks from a pre-commit file with multiple hooks.

    Expected:
        Returns list of all hook IDs.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(
        file_path,
        {
            "repos": [
                {
                    "repo": "https://github.com/pre-commit/pre-commit-hooks",
                    "rev": "v4.4.0",
                    "hooks": [
                        {"id": "trailing-whitespace"},
                        {"id": "end-of-file-fixer"},
                    ],
                },
                {
                    "repo": "https://github.com/psf/black",
                    "rev": "v22.0.0",
                    "hooks": [{"id": "black"}],
                },
            ]
        },
    )

    manager = PreCommitManager(file_path)
    hooks = manager.list_hooks()
    assert set(hooks) == {"trailing-whitespace", "end-of-file-fixer", "black"}


def test_list_hooks_missing_repos_key(tmp_path):
    """
    Scenario:
        List hooks from a pre-commit file without repos key.

    Expected:
        Returns empty list.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(file_path, {})

    manager = PreCommitManager(file_path)
    hooks = manager.list_hooks()
    assert hooks == []


def test_add_hook_new_repo(tmp_path):
    """
    Scenario:
        Add hooks to a new repository.

    Expected:
        New repository entry is created with the hooks.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(file_path, {"repos": []})

    manager = PreCommitManager(file_path)
    hooks = [{"id": "black", "language_version": "python3.9"}]
    manager.add_hook("https://github.com/psf/black", "v22.0.0", hooks)

    repos = manager.yaml_file_manager.get_key("repos")
    assert len(repos) == 1
    assert repos[0]["repo"] == "https://github.com/psf/black"
    assert repos[0]["rev"] == "v22.0.0"
    assert repos[0]["hooks"] == hooks


def test_add_hook_existing_repo(tmp_path):
    """
    Scenario:
        Add hooks to an existing repository.

    Expected:
        Hooks are added to the existing repository entry.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(
        file_path,
        {
            "repos": [
                {
                    "repo": "https://github.com/pre-commit/pre-commit-hooks",
                    "rev": "v4.4.0",
                    "hooks": [{"id": "trailing-whitespace"}],
                }
            ]
        },
    )

    manager = PreCommitManager(file_path)
    new_hooks = [{"id": "end-of-file-fixer"}]
    manager.add_hook(
        "https://github.com/pre-commit/pre-commit-hooks", "v4.4.0", new_hooks
    )

    repos = manager.yaml_file_manager.get_key("repos")
    assert len(repos) == 1
    assert len(repos[0]["hooks"]) == 2
    assert repos[0]["hooks"][0]["id"] == "trailing-whitespace"
    assert repos[0]["hooks"][1]["id"] == "end-of-file-fixer"


def test_add_hook_duplicate_prevention(tmp_path):
    """
    Scenario:
        Add hooks that already exist in the repository.

    Expected:
        Duplicate hooks are not added.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(
        file_path,
        {
            "repos": [
                {
                    "repo": "https://github.com/pre-commit/pre-commit-hooks",
                    "rev": "v4.4.0",
                    "hooks": [{"id": "trailing-whitespace"}],
                }
            ]
        },
    )

    manager = PreCommitManager(file_path)
    duplicate_hooks = [{"id": "trailing-whitespace"}]
    manager.add_hook(
        "https://github.com/pre-commit/pre-commit-hooks", "v4.4.0", duplicate_hooks
    )

    repos = manager.yaml_file_manager.get_key("repos")
    assert len(repos) == 1
    assert len(repos[0]["hooks"]) == 1
    assert repos[0]["hooks"][0]["id"] == "trailing-whitespace"


def test_add_hook_existing_repo_no_hooks(tmp_path):
    """
    Scenario:
        Add hooks to an existing repository that has no hooks key.

    Expected:
        Hooks key is created and hooks are added.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(
        file_path,
        {
            "repos": [
                {
                    "repo": "https://github.com/pre-commit/pre-commit-hooks",
                    "rev": "v4.4.0",
                }
            ]
        },
    )

    manager = PreCommitManager(file_path)
    hooks = [{"id": "trailing-whitespace"}]
    manager.add_hook("https://github.com/pre-commit/pre-commit-hooks", "v4.4.0", hooks)

    repos = manager.yaml_file_manager.get_key("repos")
    assert len(repos) == 1
    assert "hooks" in repos[0]
    assert repos[0]["hooks"] == hooks


def test_remove_hook_existing(tmp_path):
    """
    Scenario:
        Remove an existing hook from repositories.

    Expected:
        Hook is removed from all repositories.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(
        file_path,
        {
            "repos": [
                {
                    "repo": "https://github.com/pre-commit/pre-commit-hooks",
                    "rev": "v4.4.0",
                    "hooks": [
                        {"id": "trailing-whitespace"},
                        {"id": "end-of-file-fixer"},
                    ],
                },
                {
                    "repo": "https://github.com/psf/black",
                    "rev": "v22.0.0",
                    "hooks": [{"id": "black"}, {"id": "trailing-whitespace"}],
                },
            ]
        },
    )

    manager = PreCommitManager(file_path)
    manager.remove_hook("trailing-whitespace")

    repos = manager.yaml_file_manager.get_key("repos")
    assert len(repos[0]["hooks"]) == 1
    assert repos[0]["hooks"][0]["id"] == "end-of-file-fixer"
    assert len(repos[1]["hooks"]) == 1
    assert repos[1]["hooks"][0]["id"] == "black"


def test_remove_hook_nonexistent(tmp_path):
    """
    Scenario:
        Remove a non-existent hook.

    Expected:
        No changes are made to the repositories.
    """
    file_path = tmp_path / "test.yaml"
    original_data = {
        "repos": [
            {
                "repo": "https://github.com/pre-commit/pre-commit-hooks",
                "rev": "v4.4.0",
                "hooks": [{"id": "trailing-whitespace"}],
            }
        ]
    }
    save_yaml_file(file_path, original_data)

    manager = PreCommitManager(file_path)
    manager.remove_hook("nonexistent-hook")

    repos = manager.yaml_file_manager.get_key("repos")
    assert len(repos) == 1
    assert len(repos[0]["hooks"]) == 1
    assert repos[0]["hooks"][0]["id"] == "trailing-whitespace"


def test_remove_hook_empty_repos(tmp_path):
    """
    Scenario:
        Remove a hook from empty repositories.

    Expected:
        No changes are made.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(file_path, {"repos": []})

    manager = PreCommitManager(file_path)
    manager.remove_hook("any-hook")

    repos = manager.yaml_file_manager.get_key("repos")
    assert repos == []


def test_remove_hook_repo_without_hooks_key(tmp_path):
    """
    Scenario:
        Remove a hook from repositories that don't have hooks key.

    Expected:
        No changes are made, but hooks key is added during normalization.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(
        file_path,
        {
            "repos": [
                {
                    "repo": "https://github.com/pre-commit/pre-commit-hooks",
                    "rev": "v4.4.0",
                }
            ]
        },
    )

    manager = PreCommitManager(file_path)
    manager.remove_hook("any-hook")

    repos = manager.yaml_file_manager.get_key("repos")
    assert len(repos) == 1
    # The normalization process adds the hooks key, so it will be present
    assert "hooks" in repos[0]
    assert repos[0]["hooks"] == []


def test_add_multiple_hooks_at_once(tmp_path):
    """
    Scenario:
        Add multiple hooks to a repository at once.

    Expected:
        All hooks are added to the repository.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(file_path, {"repos": []})

    manager = PreCommitManager(file_path)
    hooks = [
        {"id": "trailing-whitespace"},
        {"id": "end-of-file-fixer"},
        {"id": "check-yaml"},
    ]
    manager.add_hook("https://github.com/pre-commit/pre-commit-hooks", "v4.4.0", hooks)

    repos = manager.yaml_file_manager.get_key("repos")
    assert len(repos) == 1
    assert len(repos[0]["hooks"]) == 3
    hook_ids = [h["id"] for h in repos[0]["hooks"]]
    assert set(hook_ids) == {"trailing-whitespace", "end-of-file-fixer", "check-yaml"}
