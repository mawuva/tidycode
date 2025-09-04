"""
TidyCode Pre-commit Manager Operations Tests
"""

from tidycode.core.yaml import save_yaml_file
from tidycode.core.pre_commit.manager import PreCommitManager


def test_get_operation(tmp_path):
    """
    Scenario:
        Get a value from the pre-commit file using dot notation.

    Expected:
        Returns the correct value.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(file_path, {
        "repos": [
            {
                "repo": "https://github.com/pre-commit/pre-commit-hooks",
                "rev": "v4.4.0",
                "hooks": [{"id": "trailing-whitespace"}]
            }
        ],
        "default_language_version": {
            "python": "python3.9"
        }
    })

    manager = PreCommitManager(file_path)
    
    # Test getting repos
    repos = manager.get("repos")
    assert len(repos) == 1
    assert repos[0]["repo"] == "https://github.com/pre-commit/pre-commit-hooks"
    
    # Test getting nested value
    python_version = manager.get("default_language_version.python")
    assert python_version == "python3.9"
    
    # Test getting non-existent value with default
    missing_value = manager.get("missing.key", default="default_value")
    assert missing_value == "default_value"


def test_set_operation(tmp_path):
    """
    Scenario:
        Set a value in the pre-commit file using dot notation.

    Expected:
        Value is set correctly.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(file_path, {"repos": []})

    manager = PreCommitManager(file_path)
    
    # Test setting a simple value
    manager.set("default_language_version.python", "python3.10")
    python_version = manager.get("default_language_version.python")
    assert python_version == "python3.10"
    
    # Test setting a complex value
    new_repos = [
        {
            "repo": "https://github.com/psf/black",
            "rev": "v22.0.0",
            "hooks": [{"id": "black"}]
        }
    ]
    manager.set("repos", new_repos)
    repos = manager.get("repos")
    assert len(repos) == 1
    assert repos[0]["repo"] == "https://github.com/psf/black"


def test_delete_operation(tmp_path):
    """
    Scenario:
        Delete a value from the pre-commit file using dot notation.

    Expected:
        Value is deleted successfully.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(file_path, {
        "repos": [
            {
                "repo": "https://github.com/pre-commit/pre-commit-hooks",
                "rev": "v4.4.0",
                "hooks": [{"id": "trailing-whitespace"}]
            }
        ],
        "default_language_version": {
            "python": "python3.9"
        }
    })

    manager = PreCommitManager(file_path)
    
    # Test deleting a nested value
    manager.delete("default_language_version.python")
    python_version = manager.get("default_language_version.python")
    assert python_version is None
    
    # Test deleting a top-level value
    manager.delete("repos")
    repos = manager.get("repos")
    assert repos is None


def test_save_operation(tmp_path):
    """
    Scenario:
        Save changes to the pre-commit file.

    Expected:
        Changes are persisted to disk.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(file_path, {"repos": []})

    manager = PreCommitManager(file_path)
    
    # Make changes
    manager.set("default_language_version.python", "python3.11")
    manager.set("repos", [
        {
            "repo": "https://github.com/psf/black",
            "rev": "v22.0.0",
            "hooks": [{"id": "black"}]
        }
    ])
    
    # Save changes
    manager.save()
    
    # Verify changes are persisted
    import yaml
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
    
    assert data["default_language_version"]["python"] == "python3.11"
    assert len(data["repos"]) == 1
    assert data["repos"][0]["repo"] == "https://github.com/psf/black"


def test_normalize_operation(tmp_path):
    """
    Scenario:
        Normalize the pre-commit file and reload it.

    Expected:
        File is normalized and manager is reloaded.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(file_path, {
        "repos": [
            "https://github.com/pre-commit/pre-commit-hooks"
        ]
    })

    manager = PreCommitManager(file_path, default_rev="v1.0.0")
    
    # Verify initial state
    repos = manager.get("repos")
    assert len(repos) == 1
    assert repos[0]["repo"] == "https://github.com/pre-commit/pre-commit-hooks"
    assert repos[0]["rev"] == "v1.0.0"
    
    # Manually modify the file to be malformed
    import yaml
    with open(file_path, 'w') as f:
        yaml.dump({
            "repos": [
                "https://github.com/psf/black"
            ]
        }, f)
    
    # Normalize and reload
    manager.normalize()
    
    # Verify normalization worked
    repos = manager.get("repos")
    assert len(repos) == 1
    assert repos[0]["repo"] == "https://github.com/psf/black"
    assert repos[0]["rev"] == "v1.0.0"  # Uses the manager's default_rev


def test_complex_operations_workflow(tmp_path):
    """
    Scenario:
        Perform a complex workflow of operations on the pre-commit file.

    Expected:
        All operations work correctly together.
    """
    file_path = tmp_path / "test.yaml"
    save_yaml_file(file_path, {"repos": []})

    manager = PreCommitManager(file_path)
    
    # Add some configuration
    manager.set("default_language_version.python", "python3.9")
    manager.set("ci.autofix_commit_msg", "Auto-fix from pre-commit")
    
    # Add hooks
    hooks = [{"id": "trailing-whitespace"}, {"id": "end-of-file-fixer"}]
    manager.add_hook("https://github.com/pre-commit/pre-commit-hooks", "v4.4.0", hooks)
    
    # Add more hooks
    black_hooks = [{"id": "black", "language_version": "python3.9"}]
    manager.add_hook("https://github.com/psf/black", "v22.0.0", black_hooks)
    
    # Verify state
    assert manager.get("default_language_version.python") == "python3.9"
    assert manager.get("ci.autofix_commit_msg") == "Auto-fix from pre-commit"
    
    all_hooks = manager.list_hooks()
    assert set(all_hooks) == {"trailing-whitespace", "end-of-file-fixer", "black"}
    
    # Remove a hook
    manager.remove_hook("end-of-file-fixer")
    remaining_hooks = manager.list_hooks()
    assert set(remaining_hooks) == {"trailing-whitespace", "black"}
    
    # Save and verify persistence
    manager.save()
    
    import yaml
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
    
    assert data["default_language_version"]["python"] == "python3.9"
    assert data["ci"]["autofix_commit_msg"] == "Auto-fix from pre-commit"
    assert len(data["repos"]) == 2
    
    # Verify hooks were properly managed
    hook_ids = []
    for repo in data["repos"]:
        for hook in repo["hooks"]:
            hook_ids.append(hook["id"])
    assert set(hook_ids) == {"trailing-whitespace", "black"}
