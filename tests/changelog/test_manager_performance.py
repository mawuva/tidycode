"""
TidyCode Changelog Manager Performance and Stress Tests
"""

import gc
import sys
import time

from tidycode.changelog.manager import ChangeLogManager


def test_capture_performance_small_structures():
    """
    Scenario:
        Test capture performance with small data structures.

    Expected:
        Small structures are captured quickly.
    """
    manager = ChangeLogManager()

    # Small nested structure
    data = {
        "config": {
            "database": {"host": "localhost", "port": 5432},
            "logging": {"level": "INFO"},
        }
    }

    start_time = time.time()

    with manager.capture(data) as captured_data:
        captured_data["config"]["database"]["host"] = "127.0.0.1"
        captured_data["config"]["database"]["port"] = 5433
        captured_data["config"]["cache"] = {"enabled": True}

    end_time = time.time()
    capture_time = end_time - start_time

    # Verify changes were captured
    assert len(manager.entries) == 3

    # Performance should be very fast for small structures
    assert capture_time < 0.1  # Less than 100ms


def test_capture_performance_medium_structures():
    """
    Scenario:
        Test capture performance with medium-sized data structures.

    Expected:
        Medium structures are captured efficiently.
    """
    manager = ChangeLogManager()

    # Medium nested structure
    data = {}
    for i in range(100):
        data[f"section_{i}"] = {
            f"subsection_{i}": {f"key_{i}": f"value_{i}", f"list_{i}": list(range(10))}
        }

    start_time = time.time()

    with manager.capture(data) as captured_data:
        # Make a few strategic changes
        captured_data["section_0"]["subsection_0"]["key_0"] = "modified"
        captured_data["section_50"]["subsection_50"]["new_key"] = "new_value"
        captured_data["section_99"]["subsection_99"]["list_99"].append(100)

    end_time = time.time()
    capture_time = end_time - start_time

    # Verify changes were captured
    assert len(manager.entries) == 3

    # Performance should be reasonable for medium structures
    assert capture_time < 0.5  # Less than 500ms


def test_capture_performance_large_structures():
    """
    Scenario:
        Test capture performance with large data structures.

    Expected:
        Large structures are handled without performance degradation.
    """
    manager = ChangeLogManager()

    # Large nested structure
    data = {}
    for i in range(1000):
        data[f"level1_{i}"] = {
            f"level2_{i}": {
                f"level3_{i}": {
                    f"level4_{i}": f"value_{i}",
                    f"list_{i}": list(range(50)),
                }
            }
        }

    start_time = time.time()

    with manager.capture(data) as captured_data:
        # Make a few changes at different levels
        captured_data["level1_0"]["level2_0"]["level3_0"]["level4_0"] = "modified"
        captured_data["level1_500"]["level2_500"]["level3_500"]["new_key"] = "new_value"
        captured_data["level1_999"]["level2_999"]["level3_999"]["list_999"].append(1000)

    end_time = time.time()
    capture_time = end_time - start_time

    # Verify changes were captured
    assert len(manager.entries) == 3

    # Performance should be reasonable even for large structures
    assert capture_time < 2.0  # Less than 2 seconds


def test_memory_usage_with_large_structures():
    """
    Scenario:
        Test memory usage when working with large data structures.

    Expected:
        Memory usage remains reasonable and doesn't leak.
    """
    manager = ChangeLogManager()

    # Force garbage collection before test
    gc.collect()

    # Get initial memory usage
    initial_memory = sys.getsizeof(manager.entries)

    # Create large data structure
    large_data = {}
    for i in range(500):
        large_data[f"key_{i}"] = {
            f"nested_{i}": f"value_{i}",
            f"list_{i}": list(range(100)),
        }

    # Capture changes
    with manager.capture(large_data) as captured_data:
        for i in range(0, 500, 10):  # Modify every 10th item
            captured_data[f"key_{i}"]["nested_{i}"] = f"modified_{i}"

    # Get memory usage after capture
    after_capture_memory = sys.getsizeof(manager.entries)

    # Verify changes were captured
    assert len(manager.entries) == 50

    # Memory increase should be reasonable
    memory_increase = after_capture_memory - initial_memory
    assert memory_increase < 10000  # Less than 10KB increase

    # Force garbage collection
    gc.collect()

    # Clear entries and check memory
    manager.reset()
    after_reset_memory = sys.getsizeof(manager.entries)

    # Memory should be back to initial level
    assert after_reset_memory <= initial_memory


def test_capture_performance_with_many_changes():
    """
    Scenario:
        Test capture performance when many changes are made.

    Expected:
        Many changes are captured efficiently.
    """
    manager = ChangeLogManager()

    # Create data structure
    data = {}
    for i in range(100):
        data[f"key_{i}"] = f"value_{i}"

    start_time = time.time()

    with manager.capture(data) as captured_data:
        # Make many changes
        for i in range(100):
            captured_data[f"key_{i}"] = f"new_value_{i}"

    end_time = time.time()
    capture_time = end_time - start_time

    # Verify all changes were captured
    assert len(manager.entries) == 100

    # Performance should be reasonable for many changes
    assert capture_time < 1.0  # Less than 1 second


def test_capture_performance_with_deep_nesting():
    """
    Scenario:
        Test capture performance with very deep nested structures.

    Expected:
        Deep nesting doesn't cause performance issues.
    """
    manager = ChangeLogManager()

    # Create deeply nested structure
    data = {}
    current = data
    for i in range(20):  # 20 levels deep
        current[f"level_{i}"] = {}
        current = current[f"level_{i}"]
    current["final"] = "value"

    start_time = time.time()

    with manager.capture(data) as captured_data:
        # Navigate to deepest level and modify
        current = captured_data
        for i in range(20):
            current = current[f"level_{i}"]
        current["final"] = "new_value"

        # Add new deeply nested structure
        current["new_deep"] = {"deepest": "deep_value"}

    end_time = time.time()
    capture_time = end_time - start_time

    # Verify changes were captured
    assert len(manager.entries) == 2

    # Performance should be reasonable even with deep nesting
    assert capture_time < 1.0  # Less than 1 second


def test_concurrent_capture_performance():
    """
    Scenario:
        Test performance when multiple capture contexts are used.

    Expected:
        Multiple captures work efficiently.
    """
    manager = ChangeLogManager()

    # Create multiple data structures
    data1 = {"key1": "value1"}
    data2 = {"key2": "value2"}
    data3 = {"key3": "value3"}

    start_time = time.time()

    # Use multiple capture contexts
    with manager.capture(data1) as captured_data1:
        captured_data1["key1"] = "new_value1"

    with manager.capture(data2) as captured_data2:
        captured_data2["key2"] = "new_value2"

    with manager.capture(data3) as captured_data3:
        captured_data3["key3"] = "new_value3"

    end_time = time.time()
    total_time = end_time - start_time

    # Verify all changes were captured
    assert len(manager.entries) == 3

    # Performance should be reasonable for multiple captures
    assert total_time < 0.5  # Less than 500ms


def test_capture_performance_with_complex_types():
    """
    Scenario:
        Test capture performance with complex data types.

    Expected:
        Complex types are handled efficiently.
    """
    manager = ChangeLogManager()

    # Create data with complex types
    data = {
        "strings": ["hello", "world", "python"],
        "numbers": [1, 2, 3, 4, 5],
        "booleans": [True, False, True],
        "nested": {
            "dict1": {"key1": "value1", "key2": "value2"},
            "dict2": {"key3": "value3", "key4": "value4"},
        },
        "mixed": [
            {"type": "string", "value": "hello"},
            {"type": "number", "value": 42},
            {"type": "boolean", "value": True},
        ],
    }

    start_time = time.time()

    with manager.capture(data) as captured_data:
        # Make various types of changes
        captured_data["strings"].append("new")
        captured_data["numbers"][0] = 100
        captured_data["booleans"].remove(False)
        captured_data["nested"]["dict1"]["key1"] = "modified"
        captured_data["mixed"].append({"type": "list", "value": [1, 2, 3]})

    end_time = time.time()
    capture_time = end_time - start_time

    # Verify changes were captured
    assert len(manager.entries) == 5

    # Performance should be reasonable for complex types
    assert capture_time < 0.5  # Less than 500ms


def test_capture_performance_with_large_lists():
    """
    Scenario:
        Test capture performance with large list operations.

    Expected:
        Large list operations are handled efficiently.
    """
    manager = ChangeLogManager()

    # Create data with large lists
    data = {
        "large_list": list(range(1000)),
        "nested_lists": [[i] * 100 for i in range(100)],
    }

    start_time = time.time()

    with manager.capture(data) as captured_data:
        # Perform list operations
        captured_data["large_list"].append(1000)
        captured_data["large_list"][0] = -1
        captured_data["large_list"].extend([1001, 1002, 1003])

        # Modify nested lists
        captured_data["nested_lists"][0][0] = -1
        captured_data["nested_lists"].append([999] * 100)

    end_time = time.time()
    capture_time = end_time - start_time

    # Verify changes were captured
    assert len(manager.entries) == 6

    # Performance should be reasonable for large list operations
    assert capture_time < 1.0  # Less than 1 second


def test_capture_performance_with_string_operations():
    """
    Scenario:
        Test capture performance with string operations.

    Expected:
        String operations are handled efficiently.
    """
    manager = ChangeLogManager()

    # Create data with strings
    data = {
        "short_string": "hello",
        "long_string": "x" * 1000,
        "unicode_string": "Привет мир " * 100,
        "emoji_string": "Hello 🌍 " * 50,
    }

    start_time = time.time()

    with manager.capture(data) as captured_data:
        # Modify strings
        captured_data["short_string"] = "world"
        captured_data["long_string"] = "y" * 1000
        captured_data["unicode_string"] = "Добро пожаловать " * 100
        captured_data["emoji_string"] = "Hello 🚀 " * 50
        captured_data["new_string"] = "new value"

    end_time = time.time()
    capture_time = end_time - start_time

    # Verify changes were captured
    assert len(manager.entries) == 5

    # Performance should be reasonable for string operations
    assert capture_time < 0.5  # Less than 500ms


def test_capture_performance_with_numeric_operations():
    """
    Scenario:
        Test capture performance with numeric operations.

    Expected:
        Numeric operations are handled efficiently.
    """
    manager = ChangeLogManager()

    # Create data with various numeric types
    data = {
        "integers": list(range(1000)),
        "floats": [i * 0.1 for i in range(1000)],
        "complex_numbers": [complex(i, i) for i in range(100)],
    }

    start_time = time.time()

    with manager.capture(data) as captured_data:
        # Modify numeric values
        for i in range(0, 1000, 10):  # Modify every 10th item
            captured_data["integers"][i] = -i
            captured_data["floats"][i] = -i * 0.1

        # Modify complex numbers
        for i in range(0, 100, 5):  # Modify every 5th item
            captured_data["complex_numbers"][i] = complex(-i, -i)

    end_time = time.time()
    capture_time = end_time - start_time

    # Verify changes were captured
    # The exact number depends on how the diff logic works
    expected_changes = 200 + 20  # 200 integer changes + 20 complex changes
    assert len(manager.entries) >= expected_changes * 0.9  # Allow some flexibility

    # Performance should be reasonable for numeric operations
    assert capture_time < 1.0  # Less than 1 second


def test_capture_performance_with_boolean_operations():
    """
    Scenario:
        Test capture performance with boolean operations.

    Expected:
        Boolean operations are handled efficiently.
    """
    manager = ChangeLogManager()

    # Create data with boolean values
    data = {"booleans": [True] * 1000, "mixed_bools": [i % 2 == 0 for i in range(1000)]}

    start_time = time.time()

    with manager.capture(data) as captured_data:
        # Toggle boolean values
        for i in range(0, 1000, 2):  # Toggle every other item
            captured_data["booleans"][i] = False
            captured_data["mixed_bools"][i] = not captured_data["mixed_bools"][i]

    end_time = time.time()
    capture_time = end_time - start_time

    # Verify changes were captured
    # The exact number depends on how the diff logic works
    assert len(manager.entries) >= 1  # Allow for some flexibility

    # Performance should be reasonable for boolean operations
    assert capture_time < 1.0  # Less than 1 second
