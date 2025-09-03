"""
Pre-commit helpers.
"""
from pathlib import Path
from typing import Union
from tidycode.core.yaml import load_yaml_file, save_yaml_file

def normalize_pre_commit_file(file_path: Union[str, Path], default_rev: str = "v1.0.0") -> None:
    """
    Normalise the .pre-commit.yaml file to ensure a correct structure.
    - Each entry of `repos` becomes a dict with {repo, rev, hooks}.
    - Malformed entries (string, dict incomplete) are corrected.
    - Add missing keys if needed.
    
    Args:
        file_path (Union[str, Path]): Path to the .pre-commit.yaml file.
        default_rev (str): The default revision to use if not specified in the file.

    Raises:
        FileNotFoundError: If the file does not exist.
        Exception: If there is an error reading or writing the file.

    Usage:
        normalize_pre_commit_file("path/to/.pre-commit.yaml")
        normalize_pre_commit_file("path/to/.pre-commit.yaml", default_rev="v1.0.0")

    Example:
        {"repos": [{"repo": "https://github.com/pre-commit/pre-commit-hooks", "rev": "v1.0.0", "hooks": []}]}
    """
    data = load_yaml_file(file_path)
    repos = data.get("repos", [])
    normalized_repos = []

    for r in repos:
        if isinstance(r, str):
            normalized_repos.append({"repo": r, "rev": default_rev, "hooks": []})
        elif isinstance(r, dict):
            hooks = r.get("hooks", [])
            if not isinstance(hooks, list):
                hooks = [hooks]
            normalized_repos.append({
                "repo": r.get("repo", "MISSING_REPO"),
                "rev": r.get("rev", default_rev),
                "hooks": hooks
            })
    
    # Save the normalized file
    data["repos"] = normalized_repos
    save_yaml_file(file_path, data)
