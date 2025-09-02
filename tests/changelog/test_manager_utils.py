"""
TidyCode Changelog Manager Utilities and Advanced Features Tests
"""

from tidycode.changelog.manager import ChangeLogManager
from tidycode.changelog.types import ChangeActions


def test_capture_context_manager_enter_exit():
    """
    Scenario:
        Test the context manager behavior of capture method.

    Expected:
        Context manager properly enters and exits.
    """
    manager = ChangeLogManager()
    data = {"key": "value"}

    # Test context manager behavior
    context = manager.capture(data)

    # Enter context
    captured_data = context.__enter__()
    assert captured_data == data

    # Exit context (should trigger diff)
    context.__exit__(None, None, None)

    # No changes were made, so no entries
    assert len(manager.entries) == 0


def test_capture_with_prefix_handling():
    """
    Scenario:
        Test prefix handling in capture method.

    Expected:
        Prefixes are properly applied to key paths.
    """
    manager = ChangeLogManager()
    data = {"key": "value"}

    # Test with different prefixes
    with manager.capture(data, prefix="config.") as captured_data:
        captured_data["key"] = "new_value"

    assert len(manager.entries) == 1
    assert manager.entries[0].key_path == "config.key"

    # Test with empty prefix
    manager.reset()
    with manager.capture(data, prefix="") as captured_data:
        captured_data["key"] = "another_value"

    assert len(manager.entries) == 1
    assert manager.entries[0].key_path == "key"


def test_capture_nested_prefix_handling():
    """
    Scenario:
        Test prefix handling with nested structures.

    Expected:
        Nested prefixes are properly constructed.
    """
    manager = ChangeLogManager()
    data = {"level1": {"level2": {"key": "value"}}}

    with manager.capture(data, prefix="root.") as captured_data:
        captured_data["level1"]["level2"]["key"] = "new_value"
        captured_data["level1"]["new_key"] = "new_value"

    assert len(manager.entries) == 2

    # Check nested path with prefix
    edited_entry = next(e for e in manager.entries if e.action == ChangeActions.EDITED)
    assert edited_entry.key_path == "root.level1.level2.key"

    # Check new key with prefix
    added_entry = next(e for e in manager.entries if e.action == ChangeActions.ADDED)
    assert added_entry.key_path == "root.level1.new_key"


def test_capture_list_index_handling():
    """
    Scenario:
        Test list index handling in key paths.

    Expected:
        List indices are properly formatted in key paths.
    """
    manager = ChangeLogManager()
    data = [{"key": "value1"}, {"key": "value2"}]

    with manager.capture(data) as captured_data:
        captured_data[0]["key"] = "new_value1"
        captured_data.append({"key": "value3"})
        captured_data[1]["new_key"] = "new_value"

    assert len(manager.entries) == 3

    # Check edited list item
    edited_entry = next(e for e in manager.entries if e.action == ChangeActions.EDITED)
    assert edited_entry.key_path == "[0].key"

    # Check added list item
    added_list_entry = next(
        e
        for e in manager.entries
        if e.action == ChangeActions.ADDED and "[2]" in e.key_path
    )
    assert added_list_entry.key_path == "[2]"

    # Check added key in list item
    added_key_entry = next(
        e
        for e in manager.entries
        if e.action == ChangeActions.ADDED and "new_key" in e.key_path
    )
    assert added_key_entry.key_path == "[1].new_key"


def test_capture_mixed_structure_types():
    """
    Scenario:
        Test capture with mixed structure types in the same data.

    Expected:
        Mixed types are handled correctly.
    """
    manager = ChangeLogManager()
    data = {
        "dict_key": {"nested": "value"},
        "list_key": [1, 2, 3],
        "string_key": "hello",
        "number_key": 42,
    }

    with manager.capture(data) as captured_data:
        captured_data["dict_key"]["nested"] = "new_value"
        captured_data["list_key"].append(4)
        captured_data["string_key"] = "world"
        captured_data["number_key"] = 100

    assert len(manager.entries) == 4

    # Verify all changes were captured
    paths = [e.key_path for e in manager.entries]
    assert "dict_key.nested" in paths
    # Check that list append was captured (the exact path format may vary)
    list_changes = [e for e in manager.entries if "list_key" in e.key_path]
    assert len(list_changes) >= 1
    assert "string_key" in paths
    assert "number_key" in paths


def test_capture_object_attribute_changes():
    """
    Scenario:
        Test capture of object attribute changes.

    Expected:
        Object attribute changes are properly tracked.
    """

    class TestObject:
        def __init__(self):
            self.attr1 = "value1"
            self.attr2 = "value2"

    manager = ChangeLogManager()
    data = TestObject()

    with manager.capture(data) as captured_data:
        captured_data.attr1 = "new_value1"
        captured_data.attr3 = "new_attr"
        delattr(captured_data, "attr2")

    assert len(manager.entries) == 3

    # Check edited attribute
    edited_entry = next(
        e
        for e in manager.entries
        if e.action == ChangeActions.EDITED and "attr1" in e.key_path
    )
    assert edited_entry.old_value == "value1"
    assert edited_entry.new_value == "new_value1"

    # Check added attribute
    added_entry = next(
        e
        for e in manager.entries
        if e.action == ChangeActions.ADDED and "attr3" in e.key_path
    )
    assert added_entry.new_value == "new_attr"

    # Check removed attribute
    removed_entry = next(
        e
        for e in manager.entries
        if e.action == ChangeActions.REMOVED and "attr2" in e.key_path
    )
    assert removed_entry.old_value == "value2"


def test_capture_deep_nesting():
    """
    Scenario:
        Test capture with very deep nested structures.

    Expected:
        Deep nesting is handled correctly.
    """
    manager = ChangeLogManager()

    # Create deeply nested structure
    data = {}
    current = data
    for i in range(10):
        current[f"level{i}"] = {}
        current = current[f"level{i}"]
    current["final"] = "value"

    with manager.capture(data) as captured_data:
        # Navigate to deepest level and modify
        current = captured_data
        for i in range(10):
            current = current[f"level{i}"]
        current["final"] = "new_value"

        # Add new deeply nested structure
        current["new_deep"] = {"deepest": "deep_value"}

    assert len(manager.entries) == 2

    # Check edited deep value
    edited_entry = next(e for e in manager.entries if e.action == ChangeActions.EDITED)
    assert (
        "level0.level1.level2.level3.level4.level5.level6.level7.level8.level9.final"
        in edited_entry.key_path
    )

    # Check added deep structure
    added_entry = next(e for e in manager.entries if e.action == ChangeActions.ADDED)
    assert (
        "level0.level1.level2.level3.level4.level5.level6.level7.level8.level9.new_deep"
        in added_entry.key_path
    )


def test_capture_with_custom_objects():
    """
    Scenario:
        Test capture with custom objects that have special methods.

    Expected:
        Custom objects are handled correctly.
    """

    class CustomDict(dict):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.custom_attr = "custom_value"

    class CustomList(list):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.custom_attr = "custom_value"

    manager = ChangeLogManager()

    # Test custom dict
    custom_dict = CustomDict({"key": "value"})
    with manager.capture(custom_dict) as captured_data:
        captured_data["key"] = "new_value"
        captured_data["new_key"] = "new_value"

    assert len(manager.entries) == 2

    # Test custom list
    manager.reset()
    custom_list = CustomList([1, 2, 3])
    with manager.capture(custom_list) as captured_data:
        captured_data.append(4)
        captured_data[0] = 100

    assert len(manager.entries) == 2


def test_capture_performance_with_large_data():
    """
    Scenario:
        Test capture performance with large data structures.

    Expected:
        Large data structures are handled efficiently.
    """
    manager = ChangeLogManager()

    # Create large data structure
    large_data = {}
    for i in range(1000):
        large_data[f"key_{i}"] = {
            f"nested_{i}": f"value_{i}",
            f"list_{i}": list(range(100)),
        }

    # Measure capture performance
    import time

    start_time = time.time()

    with manager.capture(large_data) as captured_data:
        # Make a few changes
        captured_data["key_0"]["nested_0"] = "modified"
        captured_data["key_500"]["new_key"] = "new_value"
        captured_data["key_999"]["list_999"].append(1000)

    end_time = time.time()
    capture_time = end_time - start_time

    # Verify changes were captured
    assert len(manager.entries) == 3

    # Performance should be reasonable (less than 1 second for 1000 items)
    assert capture_time < 1.0


def test_capture_error_handling():
    """
    Scenario:
        Test capture error handling and recovery.

    Expected:
        Errors don't break the capture mechanism.
    """
    manager = ChangeLogManager()
    data = {"key": "value"}

    # Test with various error conditions
    try:
        with manager.capture(data) as captured_data:
            captured_data["key"] = "new_value"
            # Simulate an error
            raise RuntimeError("Test error")
    except RuntimeError:
        pass

    # Changes should still be captured even if error occurs
    assert len(manager.entries) == 1
    assert manager.entries[0].action == ChangeActions.EDITED


def test_capture_with_unicode_and_special_chars():
    """
    Scenario:
        Test capture with unicode and special characters.

    Expected:
        Unicode and special characters are handled correctly.
    """
    manager = ChangeLogManager()
    data = {
        "unicode_key": "Привет мир",
        "emoji_key": "Hello 🌍",
        "special_chars": "Line\nBreak\tTab",
        "accents": "café résumé naïve",
    }

    with manager.capture(data) as captured_data:
        captured_data["unicode_key"] = "Добро пожаловать"
        captured_data["emoji_key"] = "Hello 🚀"
        captured_data["new_unicode"] = "नमस्ते दुनिया"

    assert len(manager.entries) == 3

    # Verify unicode changes were captured correctly
    unicode_entry = next(e for e in manager.entries if "unicode_key" in e.key_path)
    assert unicode_entry.old_value == "Привет мир"
    assert unicode_entry.new_value == "Добро пожаловать"

    emoji_entry = next(e for e in manager.entries if "emoji_key" in e.key_path)
    assert emoji_entry.old_value == "Hello 🌍"
    assert emoji_entry.new_value == "Hello 🚀"

    new_unicode_entry = next(e for e in manager.entries if "new_unicode" in e.key_path)
    assert new_unicode_entry.new_value == "नमस्ते दुनिया"
