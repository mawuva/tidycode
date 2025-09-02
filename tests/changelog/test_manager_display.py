"""
TidyCode Changelog Manager Display Tests
"""

from tidycode.changelog.manager import ChangeLogManager
from tidycode.changelog.types import ChangeActions


def test_display_no_entries():
    """
    Scenario:
        Display changelog with no entries.

    Expected:
        "No changes made" message is displayed.
    """
    manager = ChangeLogManager()

    # Test that display doesn't crash with no entries
    # The actual output will go to stdout, which is hard to test
    result = manager.display()
    assert result is None


def test_display_silent_mode():
    """
    Scenario:
        Display changelog in silent mode.

    Expected:
        Returns entries list instead of printing.
    """
    manager = ChangeLogManager()
    manager.add(ChangeActions.ADDED, "test.key", new_value="value")

    result = manager.display(silent=True)

    assert result == manager.entries
    assert len(result) == 1
    assert result[0].action == ChangeActions.ADDED


def test_display_silent_mode_clear_after():
    """
    Scenario:
        Display changelog in silent mode with clear_after=True.

    Expected:
        Returns entries and clears the changelog.
    """
    manager = ChangeLogManager()
    manager.add(ChangeActions.ADDED, "test.key", new_value="value")

    result = manager.display(silent=True, clear_after=True)

    assert len(result) == 1
    assert len(manager.entries) == 0  # Should be cleared


def test_display_with_values():
    """
    Scenario:
        Display changelog with show_values=True (default).

    Expected:
        Display works without crashing.
    """
    manager = ChangeLogManager()
    manager.add(ChangeActions.EDITED, "test.key", old_value="old", new_value="new")

    # Test that display works without crashing
    result = manager.display()
    assert result is None


def test_display_without_values():
    """
    Scenario:
        Display changelog with show_values=False.

    Expected:
        Display works without crashing.
    """
    manager = ChangeLogManager()
    manager.add(ChangeActions.EDITED, "test.key", old_value="old", new_value="new")

    # Test that display works without crashing
    result = manager.display(show_values=False)
    assert result is None


def test_display_action_icons():
    """
    Scenario:
        Display changelog with different action types.

    Expected:
        Display works without crashing.
    """
    manager = ChangeLogManager()
    manager.add(ChangeActions.ADDED, "added.key", new_value="value")
    manager.add(ChangeActions.EDITED, "edited.key", old_value="old", new_value="new")
    manager.add(ChangeActions.REMOVED, "removed.key", old_value="removed")

    # Test that display works without crashing
    result = manager.display()
    assert result is None


def test_display_clear_after():
    """
    Scenario:
        Display changelog with clear_after=True.

    Expected:
        Changelog is cleared after display.
    """
    manager = ChangeLogManager()
    manager.add(ChangeActions.ADDED, "test.key", new_value="value")

    manager.display(clear_after=True)

    # Check that changelog was cleared
    assert len(manager.entries) == 0


def test_display_complex_changes():
    """
    Scenario:
        Display changelog with complex nested changes.

    Expected:
        Display works without crashing.
    """
    manager = ChangeLogManager()
    manager.add(ChangeActions.ADDED, "config.database.host", new_value="localhost")
    manager.add(
        ChangeActions.EDITED, "config.database.port", old_value=5432, new_value=5433
    )
    manager.add(ChangeActions.REMOVED, "config.database.legacy_option", old_value=True)

    # Test that display works without crashing
    result = manager.display()
    assert result is None


def test_display_none_values():
    """
    Scenario:
        Display changelog with None values.

    Expected:
        Display works without crashing.
    """
    manager = ChangeLogManager()
    manager.add(ChangeActions.ADDED, "test.key")  # No values specified
    manager.add(ChangeActions.REMOVED, "removed.key", old_value=None)

    # Test that display works without crashing
    result = manager.display()
    assert result is None
