"""
Pre-commit manager.
"""

from typing import Any, Dict, List, Union
from pathlib import Path
from tidycode.core.yaml import YamlFileManager
from tidycode.core.pre_commit import normalize_pre_commit_file
from tidycode.settings import PRE_COMMIT_FILE_PATH

class PreCommitManager:
    """
    Object-oriented manager for .pre-commit.yaml files.
    Uses YamlFileManager internally for all get/set/delete operations.
    Handles normalization, hook management, and persistence.
    """
    
    def __init__(self, file_path: Union[str, Path] = PRE_COMMIT_FILE_PATH, default_rev: str = "v1.0.0"):
        """
        Initialize the PreCommitManager.
        """
        self.file_path = Path(file_path)
        self.default_rev = default_rev
        # Normalize the file first
        normalize_pre_commit_file(self.file_path, self.default_rev)
        # Use YamlFileManager for all operations
        self.yaml_file_manager = YamlFileManager(self.file_path)

    # -----------------------
    # Hooks management
    # -----------------------
    def list_hooks(self) -> List[str]:
        """Return a list of all hook IDs defined in the YAML file."""
        hooks = []
        for repo in self.yaml_file_manager.get_key("repos", default=[]):
            hooks.extend([h["id"] for h in repo.get("hooks", [])])
        return hooks

    def add_hook(self, repo: str, rev: str, hooks: List[Dict]) -> None:
        """
        Add one or multiple hooks to a repo, avoiding duplicates.
        
        Args:
            repo (str): The repository to add the hooks to.
            rev (str): The revision of the repository to use.
            hooks (List[Dict]): The hooks to add.
        """
        repos = self.yaml_file_manager.get_key("repos", default=[])
        # Find existing repo entry
        repo_entry = next((r for r in repos if r.get("repo") == repo), None)
        if repo_entry:
            repo_entry.setdefault("hooks", [])
            existing_ids = {h["id"] for h in repo_entry["hooks"]}
            for hook in hooks:
                if hook["id"] not in existing_ids:
                    repo_entry["hooks"].append(hook)
        else:
            repos.append({"repo": repo, "rev": rev, "hooks": hooks})
        self.yaml_file_manager.set_key(repos, "repos")

    def remove_hook(self, hook_id: str):
        """
        Remove a hook by ID from all repos.
        
        Args:
            hook_id (str): The ID of the hook to remove.
        """
        repos = self.yaml_file_manager.get_key("repos", default=[])
        for repo in repos:
            repo["hooks"] = [h for h in repo.get("hooks", []) if h.get("id") != hook_id]
        self.yaml_file_manager.set_key(repos, "repos")

    # -----------------------
    # Dot-notation access
    # -----------------------
    def get(self, path: str, default: Any = None) -> Any:
        """Get a value from the YAML file."""
        return self.yaml_file_manager.get_key(path, default=default)

    def set(self, path: str, value: Any) -> None:
        """Set a value in the YAML file."""
        self.yaml_file_manager.set_key(value, path)

    def delete(self, path: str) -> None:
        """Delete a value from the YAML file."""
        self.yaml_file_manager.delete_key(path)

    # -----------------------
    # Persistence
    # -----------------------
    def save(self):
        """Save changes back to .pre-commit.yaml."""
        self.yaml_file_manager.save()

    # -----------------------
    # Normalization
    # -----------------------
    def normalize(self):
        """Normalize the YAML file and reload it."""
        normalize_pre_commit_file(self.file_path, self.default_rev)
        self.yaml_file_manager = YamlFileManager(self.file_path)
