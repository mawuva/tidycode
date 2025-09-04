"""
TidyCode Pre-commit Manager Integration Tests
"""

from tidycode.core.pre_commit.manager import PreCommitManager
from tidycode.core.yaml import save_yaml_file


def test_full_pre_commit_workflow(tmp_path):
    """
    Scenario:
        Perform a complete pre-commit configuration workflow.

    Expected:
        All operations work together seamlessly.
    """
    file_path = tmp_path / ".pre-commit.yaml"
    save_yaml_file(file_path, {"repos": []})

    manager = PreCommitManager(file_path, default_rev="v4.4.0")

    # Set up basic configuration
    manager.set("default_language_version.python", "python3.9")
    manager.set("default_language_version.node", "18.0.0")

    # Add pre-commit hooks
    pre_commit_hooks = [
        {"id": "trailing-whitespace"},
        {"id": "end-of-file-fixer"},
        {"id": "check-yaml"},
        {"id": "check-added-large-files"},
    ]
    manager.add_hook(
        "https://github.com/pre-commit/pre-commit-hooks", "v4.4.0", pre_commit_hooks
    )

    # Add Python-specific hooks
    python_hooks = [
        {"id": "black", "language_version": "python3.9"},
        {"id": "isort", "args": ["--profile", "black"]},
        {"id": "flake8", "args": ["--max-line-length=88"]},
    ]
    manager.add_hook("https://github.com/psf/black", "v22.0.0", [python_hooks[0]])
    manager.add_hook("https://github.com/pycqa/isort", "v5.12.0", [python_hooks[1]])
    manager.add_hook("https://github.com/pycqa/flake8", "v6.0.0", [python_hooks[2]])

    # Add CI configuration
    manager.set("ci.autofix_commit_msg", "Auto-fix from pre-commit hooks")
    manager.set("ci.autofix_prs", True)

    # Verify configuration
    assert manager.get("default_language_version.python") == "python3.9"
    assert manager.get("default_language_version.node") == "18.0.0"
    assert manager.get("ci.autofix_commit_msg") == "Auto-fix from pre-commit hooks"
    assert manager.get("ci.autofix_prs") is True

    # Verify hooks
    all_hooks = manager.list_hooks()
    expected_hooks = {
        "trailing-whitespace",
        "end-of-file-fixer",
        "check-yaml",
        "check-added-large-files",
        "black",
        "isort",
        "flake8",
    }
    assert set(all_hooks) == expected_hooks

    # Save configuration
    manager.save()

    # Verify persistence by creating a new manager
    new_manager = PreCommitManager(file_path, default_rev="v4.4.0")
    assert new_manager.get("default_language_version.python") == "python3.9"
    assert new_manager.get("ci.autofix_prs") is True

    new_hooks = new_manager.list_hooks()
    assert set(new_hooks) == expected_hooks


def test_hook_management_edge_cases(tmp_path):
    """
    Scenario:
        Test edge cases in hook management.

    Expected:
        Edge cases are handled correctly.
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
                }
            ]
        },
    )

    manager = PreCommitManager(file_path)

    # Test adding hooks with complex configurations
    complex_hooks = [
        {"id": "black", "language_version": "python3.9", "args": ["--line-length=88"]},
        {"id": "isort", "args": ["--profile", "black", "--line-length=88"]},
    ]
    manager.add_hook("https://github.com/psf/black", "v22.0.0", complex_hooks)

    # Verify complex hooks were added
    repos = manager.get("repos")
    black_repo = next(r for r in repos if r["repo"] == "https://github.com/psf/black")
    assert len(black_repo["hooks"]) == 2
    assert black_repo["hooks"][0]["id"] == "black"
    assert black_repo["hooks"][0]["language_version"] == "python3.9"
    assert black_repo["hooks"][0]["args"] == ["--line-length=88"]

    # Test removing hooks from specific repos
    manager.remove_hook("trailing-whitespace")
    remaining_hooks = manager.list_hooks()
    assert "trailing-whitespace" not in remaining_hooks
    assert "end-of-file-fixer" in remaining_hooks
    assert "black" in remaining_hooks


def test_configuration_persistence_and_reload(tmp_path):
    """
    Scenario:
        Test that configuration changes persist across manager instances.

    Expected:
        Changes are properly persisted and can be reloaded.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(file_path, {"repos": []})

    # First manager instance
    manager1 = PreCommitManager(file_path)
    manager1.set("default_language_version.python", "python3.10")
    manager1.add_hook("https://github.com/psf/black", "v22.0.0", [{"id": "black"}])
    manager1.save()

    # Second manager instance
    manager2 = PreCommitManager(file_path)
    assert manager2.get("default_language_version.python") == "python3.10"
    assert "black" in manager2.list_hooks()

    # Make changes with second manager
    manager2.set("default_language_version.python", "python3.11")
    manager2.add_hook(
        "https://github.com/pre-commit/pre-commit-hooks",
        "v4.4.0",
        [{"id": "trailing-whitespace"}],
    )
    manager2.save()

    # Third manager instance to verify persistence
    manager3 = PreCommitManager(file_path)
    assert manager3.get("default_language_version.python") == "python3.11"
    all_hooks = manager3.list_hooks()
    assert "black" in all_hooks
    assert "trailing-whitespace" in all_hooks


def test_malformed_file_recovery(tmp_path):
    """
    Scenario:
        Test recovery from malformed pre-commit files.

    Expected:
        Malformed files are normalized and can be used.
    """
    file_path = tmp_path / "test.yaml"
    # Create a malformed file
    file_path.write_text(
        """
repos:
  - https://github.com/pre-commit/pre-commit-hooks
  - repo: https://github.com/psf/black
    hooks: black
  - repo: https://github.com/pycqa/flake8
    rev: v6.0.0
"""
    )

    manager = PreCommitManager(file_path, default_rev="v1.0.0")

    # Verify normalization worked
    repos = manager.get("repos")
    assert len(repos) == 3

    # First repo should be normalized from string
    assert repos[0]["repo"] == "https://github.com/pre-commit/pre-commit-hooks"
    assert repos[0]["rev"] == "v1.0.0"
    assert repos[0]["hooks"] == []

    # Second repo should have hooks converted to list
    assert repos[1]["repo"] == "https://github.com/psf/black"
    assert repos[1]["rev"] == "v1.0.0"
    assert repos[1]["hooks"] == ["black"]

    # Third repo should have missing hooks key added
    assert repos[2]["repo"] == "https://github.com/pycqa/flake8"
    assert repos[2]["rev"] == "v6.0.0"
    assert repos[2]["hooks"] == []

    # Verify we can still use the manager normally
    manager.add_hook(
        "https://github.com/pre-commit/pre-commit-hooks",
        "v4.4.0",
        [{"id": "trailing-whitespace"}],
    )

    hooks = manager.list_hooks()
    assert "trailing-whitespace" in hooks
    # Note: "black" hook from the malformed file should also be present
    assert "black" in hooks


def test_large_configuration_management(tmp_path):
    """
    Scenario:
        Test management of a large pre-commit configuration.

    Expected:
        Large configurations are handled efficiently.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(file_path, {"repos": []})

    manager = PreCommitManager(file_path)

    # Add many repositories with multiple hooks
    repositories = [
        (
            "https://github.com/pre-commit/pre-commit-hooks",
            "v4.4.0",
            [
                {"id": "trailing-whitespace"},
                {"id": "end-of-file-fixer"},
                {"id": "check-yaml"},
                {"id": "check-added-large-files"},
                {"id": "check-merge-conflict"},
            ],
        ),
        (
            "https://github.com/psf/black",
            "v22.0.0",
            [{"id": "black", "language_version": "python3.9"}],
        ),
        (
            "https://github.com/pycqa/isort",
            "v5.12.0",
            [{"id": "isort", "args": ["--profile", "black"]}],
        ),
        (
            "https://github.com/pycqa/flake8",
            "v6.0.0",
            [{"id": "flake8", "args": ["--max-line-length=88"]}],
        ),
        (
            "https://github.com/pre-commit/mirrors-mypy",
            "v1.0.0",
            [{"id": "mypy", "additional_dependencies": ["types-requests"]}],
        ),
    ]

    for repo, rev, hooks in repositories:
        manager.add_hook(repo, rev, hooks)

    # Verify all hooks are present
    all_hooks = manager.list_hooks()
    expected_hooks = {
        "trailing-whitespace",
        "end-of-file-fixer",
        "check-yaml",
        "check-added-large-files",
        "check-merge-conflict",
        "black",
        "isort",
        "flake8",
        "mypy",
    }
    assert set(all_hooks) == expected_hooks

    # Test selective removal
    manager.remove_hook("check-merge-conflict")
    remaining_hooks = manager.list_hooks()
    assert "check-merge-conflict" not in remaining_hooks
    assert len(remaining_hooks) == len(expected_hooks) - 1

    # Save and verify persistence
    manager.save()

    # Reload and verify
    new_manager = PreCommitManager(file_path)
    reloaded_hooks = new_manager.list_hooks()
    assert set(reloaded_hooks) == expected_hooks - {"check-merge-conflict"}
