"""
TidyCode TOML File Manager
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union, cast

from tomlkit import TOMLDocument, table
from tomlkit.items import Table

from tidycode.utils import split_dot_key

from .loader import load_toml_file, save_toml_file
from .merger import merge_toml

TomlLike = Union[TOMLDocument, Table]


class TomlFileManager:
    """
    High-level manager for any TOML file.
    Provides methods to get/set/delete keys or sections,
    with support for dot notation or path/key_name.
    """

    def __init__(self, path: Union[str, Path]) -> None:
        """Initialize the manager and load the TOML document."""
        self.path = Path(path)
        self.document: TOMLDocument = load_toml_file(path)

    # -----------------------
    # Internal helpers
    # -----------------------
    def _resolve(
        self, dot_key: Optional[str], path: Optional[List[str]], key_name: Optional[str]
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

        Usage:
            # Resolve a dot-separated key
            path, key_name = manager._resolve("section.subsection.key")

            # Resolve a path/key_name pair
            path, key_name = manager._resolve(path=["section", "subsection"], key_name="key")

            # Resolve with both dot_key and path/key_name
            path, key_name = manager._resolve(dot_key="section.subsection.key", path=["section", "subsection"], key_name="key")
        """
        if dot_key is not None:
            return split_dot_key(dot_key)
        if path is not None and key_name is not None:
            return path, key_name
        raise ValueError("You must provide either dot_key or (path + key_name)")

    def _navigate(self, path: List[str], create: bool = False) -> Optional[TomlLike]:
        """
        Descend into the TOML structure, optionally creating intermediate tables.

        Args:
            path (List[str]): The path to the key.
            create (bool): Whether to create intermediate tables if they don't exist.

        Returns:
            Optional[TomlLike]: The current node in the TOML structure.
            None if the path doesn't exist and create is False.

        Usage:
            # Navigate to a section
            table_ = manager._navigate(["section", "subsection"])

            # Navigate to a section with creation
            table_ = manager._navigate(["section", "subsection"], create=True)

            # Navigate to a key
            table_ = manager._navigate(["section", "subsection", "key"])

            # Navigate to a key with creation
            table_ = manager._navigate(["section", "subsection", "key"], create=True)
        """
        current: TomlLike = self.document

        for part in path:
            if part not in current or not isinstance(
                current[part], (TOMLDocument, Table)
            ):
                if create:
                    current[part] = table()
                else:
                    return None
            current = cast(TomlLike, current[part])
        return current

    def _resolve_and_navigate(
        self,
        dot_key: Optional[str] = None,
        path: Optional[List[str]] = None,
        key_name: Optional[str] = None,
        create: bool = False,
    ) -> Optional[Tuple[TomlLike, str]]:
        """Resolve input and navigate to the parent table.

        Args:
            dot_key (Optional[str]): The dot-separated key.
            path (Optional[List[str]]): The path to the key.
            key_name (Optional[str]): The name of the key.
            create (bool): Whether to create intermediate tables if they don't exist.

        Returns:
            Optional[Tuple[TomlLike, str]]: The parent table and the key name, or None if path doesn't exist.

        Usage:
            # Resolve and navigate to a key
            table_, key_name = manager._resolve_and_navigate("section.subsection.key")

            # Resolve and navigate to a key with creation
            table_, key_name = manager._resolve_and_navigate("section.subsection.key", create=True)

            # Resolve and navigate to a key with both dot_key and path/key_name
            table_, key_name = manager._resolve_and_navigate(dot_key="section.subsection.key", path=["section", "subsection"], key_name="key")
        """
        path, key_name = self._resolve(dot_key, path, key_name)
        table_ = self._navigate(path, create=create)
        if table_ is None:
            return None
        return table_, key_name

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
        """Retrieve the value of a key from the TOML document."""
        result = self._resolve_and_navigate(dot_key, path, key_name)
        if result is None:
            return default
        table_, key = result
        return table_.get(key, default) if table_ else default

    def set_key(
        self,
        value: Any,
        dot_key: Optional[str] = None,
        *,
        path: Optional[List[str]] = None,
        key_name: Optional[str] = None,
        overwrite: bool = True,
    ) -> None:
        """Set or overwrite a key value in the TOML document."""
        result = self._resolve_and_navigate(dot_key, path, key_name, create=True)
        if result is None:
            raise ValueError(
                f"Could not navigate to path for key: {dot_key or '.'.join(path or []) + '.' + (key_name or '')}"
            )
        table_, key = result
        if overwrite or key not in table_:
            table_[key] = value

    def delete_key(
        self,
        dot_key: Optional[str] = None,
        *,
        path: Optional[List[str]] = None,
        key_name: Optional[str] = None,
    ) -> bool:
        """Delete a key from the TOML document. Returns True if deleted."""
        result = self._resolve_and_navigate(dot_key, path, key_name)
        if result is None:
            return False
        table_, key = result
        if table_ and key in table_:
            del table_[key]
            return True
        return False

    def has_key(
        self,
        dot_key: Optional[str] = None,
        *,
        path: Optional[List[str]] = None,
        key_name: Optional[str] = None,
    ) -> bool:
        """Check if a key exists in the TOML document."""
        result = self._resolve_and_navigate(dot_key, path, key_name)
        if result is None:
            return False
        table_, key = result
        return table_ is not None and key in table_

    # -----------------------
    # Section-level operations
    # -----------------------
    def get_section(
        self,
        dot_key: Optional[str] = None,
        *,
        path: Optional[List[str]] = None,
        key_name: Optional[str] = None,
        default: Any = None,
    ) -> Any:
        """Retrieve a whole section/table from the TOML document."""
        result = self._resolve_and_navigate(dot_key, path, key_name)
        if result is None:
            return default
        table_, key = result
        if table_ is None or key not in table_:
            return default
        return table_[key]

    def set_section(
        self,
        data: Dict[str, Any],
        dot_key: Optional[str] = None,
        *,
        path: Optional[List[str]] = None,
        key_name: Optional[str] = None,
        overwrite: bool = True,
    ) -> None:
        """Set or merge a whole section/table in the TOML document."""
        result = self._resolve_and_navigate(dot_key, path, key_name, create=True)
        if result is None:
            raise ValueError(
                f"Could not navigate to path for section: {dot_key or '.'.join(path or []) + '.' + (key_name or '')}"
            )
        table_, key = result
        if key in table_:
            # Ensure the existing value is a table before merging
            existing_value = table_[key]
            if isinstance(existing_value, (TOMLDocument, Table)):
                merge_toml(existing_value, data, overwrite=overwrite)
            else:
                # If it's not a table, replace it completely
                table_[key] = data
        else:
            table_[key] = data

    def delete_section(
        self,
        dot_key: Optional[str] = None,
        *,
        path: Optional[List[str]] = None,
        key_name: Optional[str] = None,
    ) -> bool:
        """Delete a whole section/table. Returns True if deleted."""
        result = self._resolve_and_navigate(dot_key, path, key_name)
        if result is None:
            return False
        table_, key = result
        if table_ and key in table_:
            del table_[key]
            return True
        return False

    def has_section(
        self,
        dot_key: Optional[str] = None,
        *,
        path: Optional[List[str]] = None,
        key_name: Optional[str] = None,
    ) -> bool:
        """Check if a section/table exists in the TOML document."""
        result = self._resolve_and_navigate(dot_key, path, key_name)
        if result is None:
            return False
        table_, key = result
        return table_ is not None and key in table_

    # -----------------------
    # Utility
    # -----------------------
    def keys(
        self, dot_prefix: Optional[str] = None, *, path: Optional[List[str]] = None
    ) -> List[str]:
        """List keys at a given path or section."""
        if dot_prefix is not None:
            path, _ = split_dot_key(dot_prefix + ".dummy")
        elif path is None:
            path = []
        table_ = self._navigate(path)
        return list(table_.keys()) if table_ else []

    # -----------------------
    # Persistence
    # -----------------------
    def save(self) -> None:
        """Save changes back to the TOML file."""
        save_toml_file(self.path, self.document)
