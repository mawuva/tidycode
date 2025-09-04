"""
TidyCode Pre-commit Manager Initialization Tests
"""

from pathlib import Path
from unittest import mock

import pytest

from tidycode.core.pre_commit.manager import PreCommitManager


def test_pre_commit_manager_init_file_not_found():
    """
    Scenario:
        Initialize PreCommitManager with a non-existent file.

    Expected:
        FileNotFoundError is raised during normalization.
    """
    with pytest.raises(FileNotFoundError):
        PreCommitManager("non_existent_file.yaml")


def test_pre_commit_manager_init_generic_exception(tmp_path):
    """
    Scenario:
        Mock the normalize_pre_commit_file function to raise a generic exception.

    Expected:
        Exception is raised with the mocked error message.
    """
    file_path = tmp_path / "test.yaml"
    file_path.write_text("repos: []")

    with mock.patch(
        "tidycode.core.pre_commit.manager.normalize_pre_commit_file", side_effect=Exception("Boom")
    ):
        with pytest.raises(Exception) as exc_info:
            PreCommitManager(file_path)
        assert "Boom" in str(exc_info.value)


def test_pre_commit_manager_init_with_default_path(tmp_path):
    """
    Scenario:
        Initialize PreCommitManager with default path.

    Expected:
        Manager is initialized successfully with default settings.
    """
    file_path = tmp_path / ".pre-commit.yaml"
    file_path.write_text("repos: []")

    # Test that we can initialize with the default path by passing it explicitly
    manager = PreCommitManager(file_path)
    assert manager.file_path == file_path
    assert manager.default_rev == "v1.0.0"
    assert manager.yaml_file_manager is not None


def test_pre_commit_manager_init_with_custom_default_rev(tmp_path):
    """
    Scenario:
        Initialize PreCommitManager with custom default revision.

    Expected:
        Manager is initialized with custom default revision.
    """
    file_path = tmp_path / "test.yaml"
    file_path.write_text("repos: []")

    manager = PreCommitManager(file_path, default_rev="v2.0.0")
    assert manager.file_path == file_path
    assert manager.default_rev == "v2.0.0"


def test_pre_commit_manager_init_normalizes_file(tmp_path):
    """
    Scenario:
        Initialize PreCommitManager with a file that needs normalization.

    Expected:
        File is normalized during initialization.
    """
    file_path = tmp_path / "test.yaml"
    file_path.write_text("""
repos:
  - https://github.com/pre-commit/pre-commit-hooks
""")

    manager = PreCommitManager(file_path, default_rev="v3.0.0")

    # Verify the file was normalized
    import yaml
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)

    assert len(data["repos"]) == 1
    assert data["repos"][0]["repo"] == "https://github.com/pre-commit/pre-commit-hooks"
    assert data["repos"][0]["rev"] == "v3.0.0"
    assert data["repos"][0]["hooks"] == []
