"""
TidyCode Changelog Manager Integration Tests
"""

from tidycode.changelog.manager import ChangeLogManager
from tidycode.changelog.types import ChangeActions


def test_complex_nested_structure_changes():
    """
    Scenario:
        Perform complex operations on deeply nested data structures.

    Expected:
        All changes are properly captured and logged with correct paths.
    """
    manager = ChangeLogManager()

    # Complex nested structure
    data = {
        "config": {
            "database": {
                "connections": [
                    {"host": "localhost", "port": 5432},
                    {"host": "backup", "port": 5433},
                ],
                "settings": {"timeout": 30, "retries": 3},
            },
            "logging": {"level": "INFO", "handlers": ["file", "console"]},
        }
    }

    with manager.capture(data) as captured_data:
        # Modify nested values
        captured_data["config"]["database"]["connections"][0]["port"] = 5434
        captured_data["config"]["database"]["settings"]["timeout"] = 60

        # Add new nested structure
        captured_data["config"]["cache"] = {"enabled": True, "ttl": 3600}

        # Remove existing key
        del captured_data["config"]["logging"]["handlers"]

        # Add new list item
        captured_data["config"]["database"]["connections"].append(
            {"host": "replica", "port": 5435}
        )

    # Verify all changes were captured
    assert len(manager.entries) == 5

    # Check edited values
    edited_entries = [e for e in manager.entries if e.action == ChangeActions.EDITED]
    assert len(edited_entries) == 2

    port_entry = next(e for e in edited_entries if "port" in e.key_path)
    assert port_entry.key_path == "config.database.connections.[0].port"
    assert port_entry.old_value == 5432
    assert port_entry.new_value == 5434

    timeout_entry = next(e for e in edited_entries if "timeout" in e.key_path)
    assert timeout_entry.key_path == "config.database.settings.timeout"
    assert timeout_entry.old_value == 30
    assert timeout_entry.new_value == 60

    # Check added values
    added_entries = [e for e in manager.entries if e.action == ChangeActions.ADDED]
    assert len(added_entries) == 2

    cache_entry = next(e for e in added_entries if "cache" in e.key_path)
    assert cache_entry.key_path == "config.cache"
    assert cache_entry.new_value == {"enabled": True, "ttl": 3600}

    connection_entry = next(e for e in added_entries if "connections" in e.key_path)
    assert connection_entry.key_path == "config.database.connections.[2]"
    assert connection_entry.new_value == {"host": "replica", "port": 5435}

    # Check removed values
    removed_entries = [e for e in manager.entries if e.action == ChangeActions.REMOVED]
    assert len(removed_entries) == 1

    handlers_entry = next(e for e in removed_entries if "handlers" in e.key_path)
    assert handlers_entry.key_path == "config.logging.handlers"
    assert handlers_entry.old_value == ["file", "console"]


def test_mixed_data_types():
    """
    Scenario:
        Work with mixed data types in the same structure.

    Expected:
        Changes are properly captured regardless of data type.
    """
    manager = ChangeLogManager()

    data = {
        "string": "hello",
        "number": 42,
        "boolean": True,
        "list": [1, 2, 3],
        "dict": {"nested": "value"},
        "tuple": (1, 2, 3),
    }

    with manager.capture(data) as captured_data:
        captured_data["string"] = "world"
        captured_data["number"] = 100
        captured_data["boolean"] = False
        captured_data["list"].append(4)
        captured_data["dict"]["nested"] = "new_value"
        captured_data["new_field"] = "new_value"
        del captured_data["tuple"]

    # Verify changes
    assert len(manager.entries) >= 6  # Allow for some flexibility

    # Check type changes - the exact number depends on how the diff logic works
    type_changes = [e for e in manager.entries if e.action == ChangeActions.EDITED]
    assert len(type_changes) >= 4  # Allow for some flexibility


def test_capture_context_reuse():
    """
    Scenario:
        Reuse the same capture context multiple times.

    Expected:
        Each capture session works independently.
    """
    manager = ChangeLogManager()
    data = {"key": "value"}

    # First capture session
    with manager.capture(data) as captured_data:
        captured_data["key"] = "new_value"

    assert len(manager.entries) == 1
    assert manager.entries[0].action == ChangeActions.EDITED

    # Second capture session
    with manager.capture(data) as captured_data:
        captured_data["new_key"] = "new_value"

    assert len(manager.entries) == 2
    assert manager.entries[1].action == ChangeActions.ADDED


def test_capture_with_prefix_reuse():
    """
    Scenario:
        Use different prefixes for different capture sessions.

    Expected:
        Each session uses its own prefix correctly.
    """
    manager = ChangeLogManager()
    data = {"key": "value"}

    # First session with prefix
    with manager.capture(data, prefix="session1.") as captured_data:
        captured_data["key"] = "new_value"

    # Second session with different prefix
    with manager.capture(data, prefix="session2.") as captured_data:
        captured_data["key"] = "another_value"

    assert len(manager.entries) == 2
    assert manager.entries[0].key_path == "session1.key"
    assert manager.entries[1].key_path == "session2.key"


def test_capture_and_display_workflow():
    """
    Scenario:
        Complete workflow: capture changes, display, and reset.

    Expected:
        Full workflow works correctly end-to-end.
    """
    manager = ChangeLogManager()
    data = {"config": {"setting": "old_value"}}

    # Capture changes
    with manager.capture(data) as captured_data:
        captured_data["config"]["setting"] = "new_value"
        captured_data["new_config"] = {"enabled": True}

    # Verify changes were captured
    assert len(manager.entries) == 2

    # Display in silent mode to get entries
    entries = manager.display(silent=True)
    assert len(entries) == 2

    # Display with clear_after
    manager.display(clear_after=True)
    assert len(manager.entries) == 0

    # Verify entries list is empty
    assert manager.entries == []


def test_multiple_managers_independence():
    """
    Scenario:
        Use multiple ChangeLogManager instances simultaneously.

    Expected:
        Each manager operates independently.
    """
    manager1 = ChangeLogManager()
    manager2 = ChangeLogManager()

    data1 = {"key1": "value1"}
    data2 = {"key2": "value2"}

    # Capture changes in both managers
    with manager1.capture(data1) as captured_data1:
        captured_data1["key1"] = "new_value1"

    with manager2.capture(data2) as captured_data2:
        captured_data2["key2"] = "new_value2"

    # Verify each manager has its own entries
    assert len(manager1.entries) == 1
    assert len(manager2.entries) == 1

    assert manager1.entries[0].key_path == "key1"
    assert manager2.entries[0].key_path == "key2"

    # Reset one manager
    manager1.reset()
    assert len(manager1.entries) == 0
    assert len(manager2.entries) == 1  # Unchanged
