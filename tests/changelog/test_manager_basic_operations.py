"""
TidyCode Changelog Manager Basic Operations Tests
"""

from tidycode.changelog.manager import ChangeLogManager
from tidycode.changelog.types import ChangeActions


def test_add_entry():
    """
    Scenario:
        Add a single entry to the changelog.

    Expected:
        Entry is added with correct values.
    """
    manager = ChangeLogManager()
    manager.add(ChangeActions.ADDED, "test.key", old_value=None, new_value="new_value")

    assert len(manager.entries) == 1
    entry = manager.entries[0]
    assert entry.action == ChangeActions.ADDED
    assert entry.key_path == "test.key"
    assert entry.old_value is None
    assert entry.new_value == "new_value"


def test_add_multiple_entries():
    """
    Scenario:
        Add multiple entries to the changelog.

    Expected:
        All entries are added in correct order.
    """
    manager = ChangeLogManager()

    manager.add(ChangeActions.ADDED, "key1", new_value="value1")
    manager.add(ChangeActions.EDITED, "key2", old_value="old", new_value="new")
    manager.add(ChangeActions.REMOVED, "key3", old_value="removed")

    assert len(manager.entries) == 3

    assert manager.entries[0].action == ChangeActions.ADDED
    assert manager.entries[0].key_path == "key1"

    assert manager.entries[1].action == ChangeActions.EDITED
    assert manager.entries[1].key_path == "key2"

    assert manager.entries[2].action == ChangeActions.REMOVED
    assert manager.entries[2].key_path == "key3"


def test_add_entry_without_values():
    """
    Scenario:
        Add entry without specifying old_value or new_value.

    Expected:
        Entry is added with None values for unspecified parameters.
    """
    manager = ChangeLogManager()
    manager.add(ChangeActions.EDITED, "test.key")

    assert len(manager.entries) == 1
    entry = manager.entries[0]
    assert entry.old_value is None
    assert entry.new_value is None


def test_reset():
    """
    Scenario:
        Reset the changelog after adding entries.

    Expected:
        All entries are cleared.
    """
    manager = ChangeLogManager()
    manager.add(ChangeActions.ADDED, "test.key", new_value="value")
    assert len(manager.entries) == 1

    manager.reset()
    assert len(manager.entries) == 0
    assert manager.entries == []
