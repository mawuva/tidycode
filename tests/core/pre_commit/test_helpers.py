"""
TidyCode Pre-commit Helpers Tests
"""

from pathlib import Path
from unittest import mock

import pytest

from tidycode.core.pre_commit.helpers import normalize_pre_commit_file


# ---------------------------
# Unit tests
# ---------------------------


def test_normalize_pre_commit_file_file_not_found():
    """
    Scenario:
        Attempt to normalize a pre-commit file that does not exist.

    Expected:
        FileNotFoundError is raised.
    """
    with pytest.raises(FileNotFoundError):
        normalize_pre_commit_file("non_existent_file.yaml")


def test_normalize_pre_commit_file_generic_exception(tmp_path):
    """
    Scenario:
        Mock the load_yaml_file function to raise a generic exception.

    Expected:
        Exception is raised with the mocked error message.
    """
    file_path = tmp_path / "test.yaml"
    file_path.write_text("repos: []")

    with mock.patch(
        "tidycode.core.pre_commit.helpers.load_yaml_file", side_effect=Exception("Boom")
    ):
        with pytest.raises(Exception) as exc_info:
            normalize_pre_commit_file(file_path)
        assert "Boom" in str(exc_info.value)


def test_normalize_pre_commit_file_save_exception(tmp_path):
    """
    Scenario:
        Mock the save_yaml_file function to raise a generic exception.

    Expected:
        Exception is raised with the mocked error message.
    """
    file_path = tmp_path / "test.yaml"
    file_path.write_text("repos: []")

    with mock.patch(
        "tidycode.core.pre_commit.helpers.save_yaml_file", side_effect=Exception("Save error")
    ):
        with pytest.raises(Exception) as exc_info:
            normalize_pre_commit_file(file_path)
        assert "Save error" in str(exc_info.value)


# ---------------------------
# Integration tests
# ---------------------------


def test_normalize_pre_commit_file_string_repos(tmp_path):
    """
    Scenario:
        Normalize a pre-commit file with string repository entries.

    Expected:
        String entries are converted to proper dict format with default revision.
    """
    file_path = tmp_path / ".pre-commit.yaml"
    file_path.write_text("""
repos:
  - https://github.com/pre-commit/pre-commit-hooks
  - https://github.com/psf/black
""")

    normalize_pre_commit_file(file_path, default_rev="v2.0.0")

    import yaml
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)

    assert len(data["repos"]) == 2
    assert data["repos"][0] == {
        "repo": "https://github.com/pre-commit/pre-commit-hooks",
        "rev": "v2.0.0",
        "hooks": []
    }
    assert data["repos"][1] == {
        "repo": "https://github.com/psf/black",
        "rev": "v2.0.0",
        "hooks": []
    }


def test_normalize_pre_commit_file_dict_repos_complete(tmp_path):
    """
    Scenario:
        Normalize a pre-commit file with complete dict repository entries.

    Expected:
        Complete dict entries are preserved as-is.
    """
    file_path = tmp_path / ".pre-commit.yaml"
    file_path.write_text("""
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
""")

    normalize_pre_commit_file(file_path, default_rev="v1.0.0")

    import yaml
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)

    assert len(data["repos"]) == 1
    assert data["repos"][0] == {
        "repo": "https://github.com/pre-commit/pre-commit-hooks",
        "rev": "v4.4.0",
        "hooks": [
            {"id": "trailing-whitespace"},
            {"id": "end-of-file-fixer"}
        ]
    }


def test_normalize_pre_commit_file_dict_repos_incomplete(tmp_path):
    """
    Scenario:
        Normalize a pre-commit file with incomplete dict repository entries.

    Expected:
        Missing keys are filled with defaults, hooks are converted to list if needed.
    """
    file_path = tmp_path / ".pre-commit.yaml"
    file_path.write_text("""
repos:
  - repo: https://github.com/psf/black
    hooks: trailing-whitespace
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
""")

    normalize_pre_commit_file(file_path, default_rev="v3.0.0")

    import yaml
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)

    assert len(data["repos"]) == 2
    assert data["repos"][0] == {
        "repo": "https://github.com/psf/black",
        "rev": "v3.0.0",
        "hooks": ["trailing-whitespace"]
    }
    assert data["repos"][1] == {
        "repo": "https://github.com/pre-commit/pre-commit-hooks",
        "rev": "v4.4.0",
        "hooks": []
    }


def test_normalize_pre_commit_file_missing_repo_key(tmp_path):
    """
    Scenario:
        Normalize a pre-commit file with dict entries missing the repo key.

    Expected:
        Missing repo key is replaced with "MISSING_REPO".
    """
    file_path = tmp_path / ".pre-commit.yaml"
    file_path.write_text("""
repos:
  - rev: v4.4.0
    hooks:
      - id: trailing-whitespace
""")

    normalize_pre_commit_file(file_path, default_rev="v1.0.0")

    import yaml
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)

    assert len(data["repos"]) == 1
    assert data["repos"][0] == {
        "repo": "MISSING_REPO",
        "rev": "v4.4.0",
        "hooks": [{"id": "trailing-whitespace"}]
    }


def test_normalize_pre_commit_file_mixed_repos(tmp_path):
    """
    Scenario:
        Normalize a pre-commit file with mixed string and dict repository entries.

    Expected:
        All entries are normalized to proper dict format.
    """
    file_path = tmp_path / ".pre-commit.yaml"
    file_path.write_text("""
repos:
  - https://github.com/pre-commit/pre-commit-hooks
  - repo: https://github.com/psf/black
    rev: v22.0.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/flake8
""")

    normalize_pre_commit_file(file_path, default_rev="v1.0.0")

    import yaml
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)

    assert len(data["repos"]) == 3
    assert data["repos"][0] == {
        "repo": "https://github.com/pre-commit/pre-commit-hooks",
        "rev": "v1.0.0",
        "hooks": []
    }
    assert data["repos"][1] == {
        "repo": "https://github.com/psf/black",
        "rev": "v22.0.0",
        "hooks": [{"id": "black"}]
    }
    assert data["repos"][2] == {
        "repo": "https://github.com/pycqa/flake8",
        "rev": "v1.0.0",
        "hooks": []
    }


def test_normalize_pre_commit_file_empty_repos(tmp_path):
    """
    Scenario:
        Normalize a pre-commit file with empty repos list.

    Expected:
        Empty repos list is preserved.
    """
    file_path = tmp_path / ".pre-commit.yaml"
    file_path.write_text("""
repos: []
""")

    normalize_pre_commit_file(file_path, default_rev="v1.0.0")

    import yaml
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)

    assert data["repos"] == []


def test_normalize_pre_commit_file_missing_repos_key(tmp_path):
    """
    Scenario:
        Normalize a pre-commit file without repos key.

    Expected:
        Empty repos list is added.
    """
    file_path = tmp_path / ".pre-commit.yaml"
    file_path.write_text("""
default_language_version:
  python: python3.9
""")

    normalize_pre_commit_file(file_path, default_rev="v1.0.0")

    import yaml
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)

    assert "repos" in data
    assert data["repos"] == []
    assert data["default_language_version"]["python"] == "python3.9"


def test_normalize_pre_commit_file_hooks_not_list(tmp_path):
    """
    Scenario:
        Normalize a pre-commit file where hooks is not a list.

    Expected:
        Hooks are converted to a list.
    """
    file_path = tmp_path / ".pre-commit.yaml"
    file_path.write_text("""
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks: trailing-whitespace
""")

    normalize_pre_commit_file(file_path, default_rev="v1.0.0")

    import yaml
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)

    assert len(data["repos"]) == 1
    assert data["repos"][0]["hooks"] == ["trailing-whitespace"]


def test_normalize_pre_commit_file_custom_default_rev(tmp_path):
    """
    Scenario:
        Normalize a pre-commit file with a custom default revision.

    Expected:
        Custom default revision is used for entries without rev.
    """
    file_path = tmp_path / ".pre-commit.yaml"
    file_path.write_text("""
repos:
  - https://github.com/pre-commit/pre-commit-hooks
  - repo: https://github.com/psf/black
    hooks: []
""")

    normalize_pre_commit_file(file_path, default_rev="v5.0.0")

    import yaml
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)

    assert len(data["repos"]) == 2
    assert data["repos"][0]["rev"] == "v5.0.0"
    assert data["repos"][1]["rev"] == "v5.0.0"


def test_normalize_pre_commit_file_preserves_other_keys(tmp_path):
    """
    Scenario:
        Normalize a pre-commit file with other configuration keys.

    Expected:
        Other keys are preserved during normalization.
    """
    file_path = tmp_path / ".pre-commit.yaml"
    file_path.write_text("""
repos:
  - https://github.com/pre-commit/pre-commit-hooks

default_language_version:
  python: python3.9

ci:
  autofix_commit_msg: |
    [pre-commit.ci] auto fixes from pre-commit.com hooks

    for more information, see https://pre-commit.ci
""")

    normalize_pre_commit_file(file_path, default_rev="v1.0.0")

    import yaml
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)

    assert "repos" in data
    assert "default_language_version" in data
    assert "ci" in data
    assert data["default_language_version"]["python"] == "python3.9"
    assert "autofix_commit_msg" in data["ci"]
