"""
YAML file manager.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from tidycode.utils import split_dot_key
from .loader import load_yaml_file, save_yaml_file

class YamlFileManager:
    """
    High-level manager for any YAML file.
    Provides methods to get/set/delete keys or sections,
    with support for dot notation or path/key_name.
    """
    def __init__(self, path: Union[str, Path]) -> None:
        """
        Initialize the YAML file manager.
        """
        self.path = Path(path)
        self.document: Dict = load_yaml_file(path)

    # -----------------------
    # Internal helpers
    # -----------------------
    def _resolve(
        self,
        dot_key: Optional[str],
        path: Optional[List[str]],
        key_name: Optional[str],
    ) -> Tuple[List[str], str]:
        """
        Normalize input: either dot_key or (path + key_name).
        
        Args:
            dot_key (Optional[str]): The dot-separated key.
            path (Optional[List[str]]): The path to the key.
            key_name (Optional[str]): The name of the key.

        Returns:
            Tuple[List[str], str]: The path and key_name.

        Raises:
            ValueError: If neither dot_key nor (path + key_name) is provided.
        """
        if dot_key is not None:
            return split_dot_key(dot_key)
        if path is not None and key_name is not None:
            return path, key_name
        raise ValueError("You must provide either dot_key or (path + key_name)")

    def _navigate(
        self, path: List[str], create: bool = False
    ) -> Optional[Union[Dict[str, Any], List[Any]]]:
        """
        Descend into the YAML structure, optionally creating intermediate dicts.
        
        Args:
            path (List[str]): The path to the key.
            create (bool): Whether to create intermediate dicts if they don't exist.

        Returns:
            Optional[Union[Dict[str, Any], List[Any]]]: The current node in the YAML structure.
            None if the path doesn't exist and create is False.
        """
        # Start from the root of the YAML document
        current: Union[Dict[str, Any], List[Any]] = self.document

        # Iterate over each part of the path
        for part in path:
            # -----------------------------
            # Case 1: current node is a dictionary
            # -----------------------------
            if isinstance(current, dict):
                if part not in current:
                    if create:
                        # Create a new dict if missing
                        current[part] = {}
                    else:
                        # Stop traversal if key is missing and creation is not allowed
                        return None
                # Move down into the dict
                current = current[part]

            # -----------------------------
            # Case 2: current node is a list
            # -----------------------------
            elif isinstance(current, list):
                try:
                    # Convert the path part to an integer index
                    idx = int(part)
                except ValueError:
                    # If not an integer, path is invalid for a list
                    return None

                # Extend the list with empty dicts if index is out of bounds
                while len(current) <= idx:
                    if create:
                        current.append({})
                    else:
                        # Index out of bounds and creation not allowed
                        return None

                # Move down into the list element
                current = current[idx]

            # -----------------------------
            # Case 3: current node is neither dict nor list
            # -----------------------------
            else:
                # Cannot descend further into a scalar value
                return None

        # Return the final node reached
        return current
    
    def _resolve_and_navigate(
        self,
        dot_key: Optional[str] = None,
        path: Optional[List[str]] = None,
        key_name: Optional[str] = None,
        create: bool = False,
    ) -> Optional[Tuple[Union[Dict[str, Any], List[Any]], str]]:
        """
        Resolve input and navigate to the parent node.
        
        Args:
            dot_key (Optional[str]): The dot-separated key.
            path (Optional[List[str]]): The path to the key.
            key_name (Optional[str]): The name of the key.
            create (bool): Whether to create intermediate dicts if they don't exist.

        Returns:
            Optional[Tuple[Union[Dict[str, Any], List[Any]], str]]: The parent node and the key name, or None if path doesn't exist.
        """
        path, key_name = self._resolve(dot_key, path, key_name)
        parent = self._navigate(path, create=create)
        if parent is None:
            return None
        return parent, key_name
    
    # -----------------------
    # Key-level operations
    # -----------------------
    def get_key(
        self,
        dot_key: Optional[str] = None,
        *,
        path: Optional[List[str]] = None,
        key_name: Optional[str] = None,
        default: Any = None,
    ) -> Any:
        """Retrieve the value of a key from the YAML document."""
        result = self._resolve_and_navigate(dot_key, path, key_name)
        if result is None:
            return default
        parent, key = result
        if isinstance(parent, dict):
            return parent.get(key, default)
        elif isinstance(parent, list):
            try:
                idx = int(key)
                return parent[idx]
            except (ValueError, IndexError):
                return default
        return default

    def set_key(
        self,
        value: Any,
        dot_key: Optional[str] = None,
        *,
        path: Optional[List[str]] = None,
        key_name: Optional[str] = None,
        overwrite: bool = True,
    ) -> None:
        """Set or overwrite a key value in the YAML document."""
        result = self._resolve_and_navigate(dot_key, path, key_name, create=True)
        if result is None:
            raise ValueError(f"Could not navigate to key: {dot_key or path}")
        parent, key = result
        if isinstance(parent, dict):
            if overwrite or key not in parent:
                parent[key] = value
        elif isinstance(parent, list):
            idx = int(key)
            while len(parent) <= idx:
                parent.append(None)
            if overwrite or parent[idx] is None:
                parent[idx] = value

    def delete_key(
        self,
        dot_key: Optional[str] = None,
        *,
        path: Optional[List[str]] = None,
        key_name: Optional[str] = None,
    ) -> bool:
        """Delete a key from the YAML document. Returns True if deleted."""
        result = self._resolve_and_navigate(dot_key, path, key_name)
        if result is None:
            return False
        parent, key = result
        if isinstance(parent, dict) and key in parent:
            del parent[key]
            return True
        elif isinstance(parent, list):
            try:
                idx = int(key)
                parent.pop(idx)
                return True
            except (ValueError, IndexError):
                return False
        return False

    def has_key(
        self,
        dot_key: Optional[str] = None,
        *,
        path: Optional[List[str]] = None,
        key_name: Optional[str] = None,
    ) -> bool:
        """Check if a key exists in the YAML document."""
        result = self._resolve_and_navigate(dot_key, path, key_name)
        if result is None:
            return False
        parent, key = result
        if isinstance(parent, dict):
            return key in parent
        elif isinstance(parent, list):
            try:
                idx = int(key)
                return 0 <= idx < len(parent)
            except ValueError:
                return False
        return False
    
    # -----------------------
    # Persistence
    # -----------------------
    def save(self) -> None:
        """Save changes back to the YAML file.
        
        Raises:
            PermissionError: If the file cannot be written due to permissions.
            Exception: If there is an error during writing.
        """
        save_yaml_file(self.path, self.document)
