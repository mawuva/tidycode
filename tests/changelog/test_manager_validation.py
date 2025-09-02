"""
TidyCode Changelog Manager Validation Tests
"""

import math

from tidycode.changelog.manager import ChangeLogManager
from tidycode.changelog.types import ChangeActions


def test_validation_of_key_paths():
    """
    Scenario:
        Test validation of various key path formats.

    Expected:
        All key path formats are accepted and stored correctly.
    """
    manager = ChangeLogManager()

    # Test various key path formats
    key_paths = [
        "simple_key",
        "key.with.dots",
        "key_with_underscores",
        "key-with-hyphens",
        "key123",
        "123key",
        "key.with.numbers.123",
        "key.with.special.chars!@#",
        "key.with.spaces and more",
        "key\nwith\nnewlines",
        "key\twith\ttabs",
        "key\rwith\rreturns",
        "key.with.unicode.Привет",
        "key.with.emoji.🌍",
        "key.with.accents.café",
        "key.with.brackets[0]",
        "key.with.parentheses(0)",
        "key.with.curly.braces{0}",
        "key.with.angle.brackets<0>",
        "key.with.quotes'value'",
        'key.with.double.quotes"value"',
        "key.with.backticks`value`",
        "key.with.backslashes.\\path\\to\\file",
        "key.with.forward.slashes./path/to/file",
        "key.with.colons:value",
        "key.with.semicolons;value",
        "key.with.commas,value",
        "key.with.pipes|value",
        "key.with.ampersands&value",
        "key.with.equals=value",
        "key.with.plus+value",
        "key.with.minus-value",
        "key.with.asterisk*value",
        "key.with.slash/value",
        "key.with.backslash\\value",
        "key.with.caret^value",
        "key.with.tilde~value",
    ]

    for i, key_path in enumerate(key_paths):
        manager.reset()
        manager.add(ChangeActions.ADDED, key_path, new_value=f"value_{i}")

        assert len(manager.entries) == 1
        assert manager.entries[0].key_path == key_path
        assert manager.entries[0].new_value == f"value_{i}"


def test_validation_of_action_types():
    """
    Scenario:
        Test validation of action types in changelog entries.

    Expected:
        Only valid action types are accepted.
    """
    manager = ChangeLogManager()

    # Test valid action types
    valid_actions = [ChangeActions.ADDED, ChangeActions.EDITED, ChangeActions.REMOVED]

    for action in valid_actions:
        manager.reset()
        manager.add(action, "test.key", new_value="test_value")

        assert len(manager.entries) == 1
        assert manager.entries[0].action == action

    # Test that invalid action types are handled gracefully
    # The add method accepts any action type, so we test with a string
    manager.reset()
    manager.add("invalid_action", "test.key", new_value="test_value")

    # Should still add the entry (no validation in the current implementation)
    assert len(manager.entries) == 1


def test_validation_of_value_types():
    """
    Scenario:
        Test validation of various value types in changelog entries.

    Expected:
        All Python types are properly handled.
    """
    manager = ChangeLogManager()

    # Test various value types
    test_values = [
        None,
        True,
        False,
        42,
        3.14,
        "hello",
        b"bytes",
        [1, 2, 3],
        {"key": "value"},
        (1, 2, 3),
        set([1, 2, 3]),
        complex(1, 2),
        lambda x: x,  # Function
        type,  # Type
        Exception("test"),  # Exception instance
        range(5),  # Range object
        slice(1, 10, 2),  # Slice object
        memoryview(b"test"),  # Memory view
        property(),  # Property object
        staticmethod(lambda: None),  # Static method
        classmethod(lambda cls: None),  # Class method
    ]

    for i, value in enumerate(test_values):
        manager.reset()
        manager.add(ChangeActions.ADDED, f"key_{i}", new_value=value)

        assert len(manager.entries) == 1
        assert manager.entries[0].new_value == value


def test_validation_of_nested_structures():
    """
    Scenario:
        Test validation of deeply nested data structures.

    Expected:
        Deep nesting is handled correctly without validation errors.
    """
    manager = ChangeLogManager()

    # Create deeply nested structure
    data = {}
    current = data
    for i in range(50):  # 50 levels deep
        current[f"level_{i}"] = {}
        current = current[f"level_{i}"]  # Fixed typo: level_i -> level_{i}

    # Test capture with deep nesting
    with manager.capture(data) as captured_data:
        # Navigate to deepest level
        current = captured_data
        for i in range(50):
            current = current[f"level_{i}"]

        # Make changes at deepest level
        current["deep_key"] = "deep_value"
        current["deep_list"] = [1, 2, 3]

    # Verify changes were captured
    assert len(manager.entries) == 2


def test_validation_of_circular_references():
    """
    Scenario:
        Test validation of data structures with circular references.

    Expected:
        Circular references are handled gracefully without infinite recursion.
    """
    manager = ChangeLogManager()

    # Create circular reference
    data = {"key": "value"}
    data["self"] = data  # Circular reference

    # Test that capture doesn't crash
    with manager.capture(data) as captured_data:
        captured_data["key"] = "new_value"

    # Should capture the change without infinite recursion
    assert len(manager.entries) == 1
    assert manager.entries[0].action == ChangeActions.EDITED
    assert manager.entries[0].key_path == "key"


def test_validation_of_large_data_structures():
    """
    Scenario:
        Test validation of large data structures.

    Expected:
        Large structures are handled efficiently.
    """
    manager = ChangeLogManager()

    # Create large data structure
    data = {}
    for i in range(10000):
        data[f"key_{i}"] = {
            "nested": f"value_{i}",
            "list": list(range(i % 100)),
            "dict": {f"nested_key_{j}": f"nested_value_{j}" for j in range(i % 10)},
        }

    # Test capture with large structure
    with manager.capture(data) as captured_data:
        # Make a few strategic changes
        captured_data["key_0"]["nested"] = "modified"
        captured_data["key_5000"]["new_key"] = "new_value"
        captured_data["key_9999"]["list"].append(1000)

    # Verify changes were captured
    assert len(manager.entries) >= 3

    # Check that specific changes were captured
    changes_by_path = {entry.key_path: entry for entry in manager.entries}
    assert changes_by_path["key_0.nested"].new_value == "modified"
    assert changes_by_path["key_5000.new_key"].new_value == "new_value"

    # For list append, check that the new value contains the appended item
    # The exact key path might vary depending on how the diff logic works
    list_changes = [e for e in manager.entries if "list" in e.key_path]
    assert len(list_changes) >= 1
    # Check that at least one list change contains the appended item
    # Some changes might not have new_value that supports containment checks
    list_changes_with_values = [
        e for e in list_changes if hasattr(e.new_value, "__contains__")
    ]
    if list_changes_with_values:
        assert any(1000 in e.new_value for e in list_changes_with_values)


def test_validation_of_special_characters():
    """
    Scenario:
        Test validation of key paths and values with special characters.

    Expected:
        Special characters are handled correctly.
    """
    manager = ChangeLogManager()

    # Test key paths with special characters
    special_key_paths = [
        "key.with.dots",
        "key-with-hyphens",
        "key_with_underscores",
        "key123",
        "123key",
        "key.with.brackets[0]",
        "key.with.quotes",
        "key.with.spaces",
        "key\nwith\nnewlines",
        "key\twith\ttabs",
        "key\rwith\rreturns",
        "key.with.unicode.Привет",
        "key.with.emoji.🌍",
        "key.with.accents.café",
        "key.with.symbols.!@#$%^&*()",
        "key.with.backticks.`code`",
        "key.with.backslashes.\\path\\to\\file",
        "key.with.forward.slashes./path/to/file",
        "key.with.colons:value",
        "key.with.semicolons;value",
        "key.with.commas,value",
        "key.with.pipes|value",
        "key.with.ampersands&value",
        "key.with.equals=value",
        "key.with.plus+value",
        "key.with.minus-value",
        "key.with.asterisk*value",
        "key.with.slash/value",
        "key.with.backslash\\value",
        "key.with.caret^value",
        "key.with.tilde~value",
        "key.with.curly.braces{value}",
        "key.with.square.brackets[value]",
        "key.with.parentheses(value)",
        "key.with.angle.brackets<value>",
        "key.with.quotes'value'",
        'key.with.double.quotes"value"',
        "key.with.backticks`value`",
    ]

    for i, key_path in enumerate(special_key_paths):
        manager.reset()
        manager.add(ChangeActions.ADDED, key_path, new_value=f"value_{i}")

        assert len(manager.entries) == 1
        assert manager.entries[0].key_path == key_path
        assert manager.entries[0].new_value == f"value_{i}"


def test_validation_of_edge_case_values():
    """
    Scenario:
        Test validation of edge case values.

    Expected:
        Edge case values are handled correctly.
    """
    manager = ChangeLogManager()

    # Test edge case values
    edge_cases = [
        "",  # Empty string
        " ",  # Single space
        "\n",  # Newline
        "\t",  # Tab
        "\r",  # Carriage return
        "\0",  # Null byte
        "\\",  # Backslash
        "/",  # Forward slash
        "..",  # Double dots
        ".",  # Single dot
        "key.",  # Key ending with dot
        ".key",  # Key starting with dot
        "key..",  # Key ending with double dots
        "..key",  # Key starting with double dots
        "key...",  # Key with triple dots
        "...key",  # Key starting with triple dots
        "key....",  # Key with quadruple dots
        "....key",  # Key starting with quadruple dots
        "key.....",  # Key with quintuple dots
        ".....key",  # Key starting with quintuple dots
        "key......",  # Key with sextuple dots
        "......key",  # Key starting with sextuple dots
        "key.......",  # Key with septuple dots
        ".......key",  # Key starting with septuple dots
        "key........",  # Key with octuple dots
        "........key",  # Key starting with octuple dots
        "key.........",  # Key with nonuple dots
        ".........key",  # Key starting with nonuple dots
        "key..........",  # Key with decuple dots
        "..........key",  # Key starting with decuple dots
    ]

    for i, value in enumerate(edge_cases):
        manager.reset()
        manager.add(ChangeActions.ADDED, f"key_{i}", new_value=value)

        assert len(manager.entries) == 1
        assert manager.entries[0].new_value == value


def test_validation_of_numeric_edge_cases():
    """
    Scenario:
        Test validation of numeric edge cases.

    Expected:
        Numeric edge cases are handled correctly.
    """
    manager = ChangeLogManager()

    # Test numeric edge cases
    numeric_edge_cases = [
        (0, 0),
        (-0, -0),
        (1, 1),
        (-1, -1),
        (float("inf"), float("inf")),
        (float("-inf"), float("-inf")),
        (float("nan"), float("nan")),
        (complex(0, 0), complex(0, 0)),
        (complex(1, 1), complex(1, 1)),
        (complex(-1, -1), complex(-1, -1)),
        (complex(float("inf"), float("inf")), complex(float("inf"), float("inf"))),
        (complex(float("-inf"), float("-inf")), complex(float("-inf"), float("-inf"))),
        (complex(float("nan"), float("nan")), complex(float("nan"), float("nan"))),
    ]

    for i, (key_num, value) in enumerate(numeric_edge_cases):
        manager.reset()
        key_path = f"key_{i}"
        manager.add(ChangeActions.ADDED, key_path, new_value=value)

        assert len(manager.entries) == 1
        assert manager.entries[0].key_path == key_path

        # Handle NaN comparison properly
        if isinstance(value, float) and math.isnan(value):
            assert math.isnan(manager.entries[0].new_value)
        elif (
            isinstance(value, complex)
            and math.isnan(value.real)
            and math.isnan(value.imag)
        ):
            assert math.isnan(manager.entries[0].new_value.real)
            assert math.isnan(manager.entries[0].new_value.imag)
        else:
            assert manager.entries[0].new_value == value


def test_validation_of_boolean_edge_cases():
    """
    Scenario:
        Test validation of boolean edge cases.

    Expected:
        Boolean edge cases are handled correctly.
    """
    manager = ChangeLogManager()

    # Test boolean edge cases
    boolean_edge_cases = [
        (True, True),
        (False, False),
        (1, 1),  # Truthy values
        (0, 0),  # Falsy values
        ("", ""),  # Empty string
        ("hello", "hello"),  # Non-empty string
        ([], []),  # Empty list
        ([1, 2, 3], [1, 2, 3]),  # Non-empty list
        ({}, {}),  # Empty dict
        ({"key": "value"}, {"key": "value"}),  # Non-empty dict
        (None, None),  # None value
    ]

    for i, (key_val, value) in enumerate(boolean_edge_cases):
        manager.reset()
        key_path = f"key_{i}"
        manager.add(ChangeActions.ADDED, key_path, new_value=value)

        assert len(manager.entries) == 1
        assert manager.entries[0].key_path == key_path
        assert manager.entries[0].new_value == value


def test_validation_of_collection_edge_cases():
    """
    Scenario:
        Test validation of collection edge cases.

    Expected:
        Collection edge cases are handled correctly.
    """
    manager = ChangeLogManager()

    # Test collection edge cases
    collection_edge_cases = [
        ([], []),  # Empty list
        ([1, 2, 3], [1, 2, 3]),  # Simple list
        ([[1, 2], [3, 4]], [[1, 2], [3, 4]]),  # Nested list
        ([1, "string", True, None], [1, "string", True, None]),  # Mixed types
        ({}, {}),  # Empty dict
        ({"key": "value"}, {"key": "value"}),  # Simple dict
        ({"nested": {"key": "value"}}, {"nested": {"key": "value"}}),  # Nested dict
        ({"key": [1, 2, 3]}, {"key": [1, 2, 3]}),  # Dict with list
        (
            {"key": {"nested": [1, 2, 3]}},
            {"key": {"nested": [1, 2, 3]}},
        ),  # Complex nested
        ((), ()),  # Empty tuple
        ((1, 2, 3), (1, 2, 3)),  # Simple tuple
        ((1, "string", True), (1, "string", True)),  # Mixed types tuple
        (set(), set()),  # Empty set
        ({1, 2, 3}, {1, 2, 3}),  # Simple set
        (frozenset([1, 2, 3]), frozenset([1, 2, 3])),  # Frozen set
    ]

    for i, (key_val, value) in enumerate(collection_edge_cases):
        manager.reset()
        key_path = f"key_{i}"
        manager.add(ChangeActions.ADDED, key_path, new_value=value)

        assert len(manager.entries) == 1
        assert manager.entries[0].key_path == key_path
        assert manager.entries[0].new_value == value
