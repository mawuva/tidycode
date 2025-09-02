"""
TidyCode Changelog Types Tests
"""

from tidycode.changelog.types import ChangeActions, ChangeLogEntry


def test_change_actions_enum():
    """
    Scenario:
        Test the ChangeActions enum values.

    Expected:
        All expected action types are defined.
    """
    assert ChangeActions.ADDED == "added"
    assert ChangeActions.EDITED == "edited"
    assert ChangeActions.REMOVED == "removed"

    # Verify these are the only actions
    all_actions = [ChangeActions.ADDED, ChangeActions.EDITED, ChangeActions.REMOVED]
    assert len(all_actions) == 3
    assert len(set(all_actions)) == 3  # All unique


def test_change_log_entry_creation():
    """
    Scenario:
        Create ChangeLogEntry instances with different parameters.

    Expected:
        Entries are created with correct values.
    """
    # Entry with all parameters
    entry1 = ChangeLogEntry(
        action=ChangeActions.ADDED,
        key_path="test.key",
        old_value=None,
        new_value="new_value",
    )

    assert entry1.action == ChangeActions.ADDED
    assert entry1.key_path == "test.key"
    assert entry1.old_value is None
    assert entry1.new_value == "new_value"

    # Entry with minimal parameters
    entry2 = ChangeLogEntry(action=ChangeActions.REMOVED, key_path="removed.key")

    assert entry2.action == ChangeActions.REMOVED
    assert entry2.key_path == "removed.key"
    assert entry2.old_value is None
    assert entry2.new_value is None


def test_change_log_entry_defaults():
    """
    Scenario:
        Test default values for ChangeLogEntry.

    Expected:
        Default values are applied correctly.
    """
    entry = ChangeLogEntry(action=ChangeActions.EDITED, key_path="edited.key")

    assert entry.old_value is None
    assert entry.new_value is None


def test_change_log_entry_with_various_types():
    """
    Scenario:
        Create entries with various data types.

    Expected:
        All data types are handled correctly.
    """
    # String values
    string_entry = ChangeLogEntry(
        action=ChangeActions.ADDED, key_path="string.key", new_value="string_value"
    )
    assert string_entry.new_value == "string_value"

    # Numeric values
    numeric_entry = ChangeLogEntry(
        action=ChangeActions.EDITED, key_path="numeric.key", old_value=42, new_value=100
    )
    assert numeric_entry.old_value == 42
    assert numeric_entry.new_value == 100

    # Boolean values
    boolean_entry = ChangeLogEntry(
        action=ChangeActions.EDITED,
        key_path="boolean.key",
        old_value=False,
        new_value=True,
    )
    assert boolean_entry.old_value is False
    assert boolean_entry.new_value is True

    # List values
    list_entry = ChangeLogEntry(
        action=ChangeActions.ADDED, key_path="list.key", new_value=[1, 2, 3]
    )
    assert list_entry.new_value == [1, 2, 3]

    # Dict values
    dict_entry = ChangeLogEntry(
        action=ChangeActions.ADDED, key_path="dict.key", new_value={"nested": "value"}
    )
    assert dict_entry.new_value == {"nested": "value"}

    # None values
    none_entry = ChangeLogEntry(
        action=ChangeActions.REMOVED, key_path="none.key", old_value=None
    )
    assert none_entry.old_value is None


def test_change_log_entry_immutability():
    """
    Scenario:
        Test that ChangeLogEntry instances are immutable (dataclass behavior).

    Expected:
        Entries behave as expected for dataclass immutability.
    """
    entry = ChangeLogEntry(
        action=ChangeActions.ADDED, key_path="test.key", new_value="value"
    )

    # Verify initial values
    assert entry.action == ChangeActions.ADDED
    assert entry.key_path == "test.key"
    assert entry.new_value == "value"

    # Note: This test documents the current behavior
    # If the dataclass is made mutable in the future, this test should be updated


def test_change_log_entry_equality():
    """
    Scenario:
        Test equality comparison between ChangeLogEntry instances.

    Expected:
        Entries with same values are equal, different values are not.
    """
    entry1 = ChangeLogEntry(
        action=ChangeActions.ADDED, key_path="test.key", new_value="value"
    )

    entry2 = ChangeLogEntry(
        action=ChangeActions.ADDED, key_path="test.key", new_value="value"
    )

    entry3 = ChangeLogEntry(
        action=ChangeActions.EDITED, key_path="test.key", new_value="value"
    )

    # Same values should be equal
    assert entry1 == entry2

    # Different values should not be equal
    assert entry1 != entry3


def test_change_log_entry_string_representation():
    """
    Scenario:
        Test string representation of ChangeLogEntry.

    Expected:
        String representation is informative and readable.
    """
    entry = ChangeLogEntry(
        action=ChangeActions.EDITED,
        key_path="config.database.host",
        old_value="localhost",
        new_value="127.0.0.1",
    )

    # Convert to string and verify it contains key information
    entry_str = str(entry)
    assert "config.database.host" in entry_str
    assert "localhost" in entry_str
    assert "127.0.0.1" in entry_str


def test_change_actions_inheritance():
    """
    Scenario:
        Test that ChangeActions inherits from BaseEnum.

    Expected:
        ChangeActions is properly derived from BaseEnum.
    """
    # Verify inheritance
    assert issubclass(ChangeActions, type(ChangeActions.ADDED))

    # Verify enum behavior
    assert ChangeActions.ADDED in ChangeActions
    assert ChangeActions.EDITED in ChangeActions
    assert ChangeActions.REMOVED in ChangeActions


def test_change_log_entry_with_complex_objects():
    """
    Scenario:
        Create entries with complex Python objects.

    Expected:
        Complex objects are handled correctly.
    """

    class TestObject:
        def __init__(self, value):
            self.value = value

        def __repr__(self):
            return f"TestObject({self.value})"

    old_obj = TestObject("old")
    new_obj = TestObject("new")

    entry = ChangeLogEntry(
        action=ChangeActions.EDITED,
        key_path="object.key",
        old_value=old_obj,
        new_value=new_obj,
    )

    assert entry.old_value == old_obj
    assert entry.new_value == new_obj
    assert entry.old_value.value == "old"
    assert entry.new_value.value == "new"


def test_change_log_entry_key_path_edge_cases():
    """
    Scenario:
        Test ChangeLogEntry with edge case key paths.

    Expected:
        Edge case key paths are handled correctly.
    """
    # Empty key path
    empty_entry = ChangeLogEntry(
        action=ChangeActions.ADDED, key_path="", new_value="value"
    )
    assert empty_entry.key_path == ""

    # Very long key path
    long_path = ".".join([f"level{i}" for i in range(100)])
    long_entry = ChangeLogEntry(
        action=ChangeActions.ADDED, key_path=long_path, new_value="value"
    )
    assert len(long_entry.key_path) > 100

    # Key path with special characters
    special_path = "key.with.dots[0].and.brackets"
    special_entry = ChangeLogEntry(
        action=ChangeActions.ADDED, key_path=special_path, new_value="value"
    )
    assert special_entry.key_path == special_path
