"""
Manager for the changelog.
"""

import copy
from typing import Any, List, Set

from rich import box
from rich.console import Console
from rich.table import Table

from .types import ChangeActions, ChangeLogEntry


class ChangeLogManager:
    """Tracks changes in nested Python structures (dicts, lists, tuples, objects)."""

    def __init__(self) -> None:
        self.entries: List[ChangeLogEntry] = []

    def add(
        self,
        action: ChangeActions,
        key_path: str,
        old_value: Any = None,
        new_value: Any = None,
    ) -> None:
        """Add a new entry to the changelog."""
        self.entries.append(ChangeLogEntry(action, key_path, old_value, new_value))

    def capture(self, data: Any, prefix: str = "") -> Any:
        """
        Context manager to capture changes in `data`.
        Works for nested dicts, lists, tuples, and objects with __dict__.

        Args:
            data: The data to capture changes from.
            prefix: The prefix to add to the key path.
        """

        class _CaptureContext:
            def __init__(_self, original_data):
                _self.original_data = original_data
                _self.before = None

            def __enter__(_self):
                _self.before = copy.deepcopy(_self.original_data)
                return _self.original_data

            def __exit__(_self, exc_type, exc_val, exc_tb):
                _self._diff(prefix, _self.before, _self.original_data, self, set())

            def _diff(
                _self,
                path: str,
                before: Any,
                after: Any,
                changelog: ChangeLogManager,
                visited: Set[int],
            ) -> None:
                # Handle circular references
                before_id = id(before)
                after_id = id(after)

                if before_id in visited or after_id in visited:
                    return

                visited.add(before_id)
                visited.add(after_id)

                # Handle type changes
                if not isinstance(after, type(before)):
                    changelog.add(
                        ChangeActions.EDITED,
                        path.rstrip("."),
                        old_value=before,
                        new_value=after,
                    )
                    return

                # Handle dict
                if isinstance(before, dict):
                    before_keys = set(before.keys())
                    after_keys = set(after.keys())
                    for key in after_keys - before_keys:
                        changelog.add(
                            ChangeActions.ADDED, f"{path}{key}", new_value=after[key]
                        )
                    for key in before_keys - after_keys:
                        changelog.add(
                            ChangeActions.REMOVED, f"{path}{key}", old_value=before[key]
                        )
                    for key in before_keys & after_keys:
                        _self._diff(
                            f"{path}{key}.", before[key], after[key], changelog, visited
                        )

                # Handle list or tuple
                elif isinstance(before, (list, tuple)):
                    # For lists, we need to handle removals and additions more carefully
                    # since indices change when items are removed
                    before_len = len(before)
                    after_len = len(after)

                    # Find common prefix length
                    common_len = min(before_len, after_len)

                    # Check items in common range
                    for i in range(common_len):
                        _self._diff(
                            f"{path}[{i}].", before[i], after[i], changelog, visited
                        )

                    # Handle additions (items added at the end)
                    for i in range(common_len, after_len):
                        changelog.add(
                            ChangeActions.ADDED, f"{path}[{i}]", new_value=after[i]
                        )

                    # Handle removals (items removed from the end)
                    for i in range(common_len, before_len):
                        changelog.add(
                            ChangeActions.REMOVED, f"{path}[{i}]", old_value=before[i]
                        )

                # Handle objects with __dict__
                elif hasattr(before, "__dict__") and hasattr(after, "__dict__"):
                    _self._diff(
                        f"{path}", before.__dict__, after.__dict__, changelog, visited
                    )

                # Handle simple values
                else:
                    if before != after:
                        changelog.add(
                            ChangeActions.EDITED,
                            path.rstrip("."),
                            old_value=before,
                            new_value=after,
                        )

        return _CaptureContext(data)

    def display(
        self,
        clear_after: bool = False,
        silent: bool = False,
        show_values: bool = True,
    ) -> Any:
        """
        Display the change log in a clean tabular format using Rich.

        Args:
            clear_after: Clear log after display
            silent: Return entries instead of printing
            show_values: If True, display old/new values. If False, hide them.
        """
        if not self.entries:
            if silent:
                return []
            console = Console()
            console.print("\n✅ No changes made.\n", style="green")
            return

        if silent:
            entries = list(self.entries)
            if clear_after:
                self.reset()
            return entries

        console = Console()
        table = Table(title="📋 Change Summary", box=box.SIMPLE_HEAVY, show_lines=True)

        # Always show these columns
        table.add_column(
            "Action", style="bold", no_wrap=True, justify="center", width=10
        )
        table.add_column(
            "Key Path", style="cyan", justify="left", min_width=25, overflow="fold"
        )

        # Conditionally show value columns
        if show_values:
            table.add_column(
                "Old Value",
                style="yellow",
                justify="left",
                min_width=15,
                overflow="fold",
            )
            table.add_column(
                "New Value",
                style="green",
                justify="left",
                min_width=15,
                overflow="fold",
            )

        action_icons = {
            ChangeActions.ADDED: "➕ Added",
            ChangeActions.EDITED: "✏️ Edited",
            ChangeActions.REMOVED: "❌ Removed",
        }

        for entry in self.entries:
            action_icon = action_icons.get(entry.action, str(entry.action))

            if show_values:
                old_val = str(entry.old_value) if entry.old_value is not None else "-"
                new_val = str(entry.new_value) if entry.new_value is not None else "-"
                table.add_row(action_icon, entry.key_path, old_val, new_val)
            else:
                table.add_row(action_icon, entry.key_path)

        console.print(table)

        if clear_after:
            self.reset()

    def reset(self) -> None:
        """Clear all stored entries."""
        self.entries.clear()
