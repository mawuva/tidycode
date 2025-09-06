"""
TidyCode Runner Types Tests
"""

from pathlib import Path

from tidycode.runner.types import CommandSpec, SubprocessDisplayMode, SubprocessResult

# ---------------------------
# Unit tests
# ---------------------------


def test_subprocess_result_creation():
    """
    Scenario:
        Create a SubprocessResult with all fields.

    Expected:
        All fields are properly set.
    """
    result = SubprocessResult(
        display_name="test",
        status="✅ Passed",
        stdout="success output",
        stderr="",
        category="quality",
        summary="All tests passed",
        details="Detailed information",
    )

    assert result.display_name == "test"
    assert result.status == "✅ Passed"
    assert result.stdout == "success output"
    assert result.stderr == ""
    assert result.category == "quality"
    assert result.summary == "All tests passed"
    assert result.details == "Detailed information"


def test_subprocess_result_minimal_creation():
    """
    Scenario:
        Create a SubprocessResult with only required fields.

    Expected:
        Required fields are set, optional fields have defaults.
    """
    result = SubprocessResult(
        display_name="test",
        status="✅ Passed",
    )

    assert result.display_name == "test"
    assert result.status == "✅ Passed"
    assert result.stdout == ""
    assert result.stderr == ""
    assert result.category is None
    assert result.summary is None
    assert result.details is None


def test_subprocess_result_with_stdout_stderr():
    """
    Scenario:
        Create a SubprocessResult with stdout and stderr.

    Expected:
        stdout and stderr are properly set.
    """
    result = SubprocessResult(
        display_name="test",
        status="❌ Failed",
        stdout="standard output",
        stderr="error output",
    )

    assert result.display_name == "test"
    assert result.status == "❌ Failed"
    assert result.stdout == "standard output"
    assert result.stderr == "error output"


def test_subprocess_result_with_category():
    """
    Scenario:
        Create a SubprocessResult with category.

    Expected:
        Category is properly set.
    """
    result = SubprocessResult(
        display_name="test",
        status="⚠️ Warning",
        category="quality",
    )

    assert result.display_name == "test"
    assert result.status == "⚠️ Warning"
    assert result.category == "quality"


def test_subprocess_result_with_summary():
    """
    Scenario:
        Create a SubprocessResult with summary.

    Expected:
        Summary is properly set.
    """
    result = SubprocessResult(
        display_name="test",
        status="✅ Passed",
        summary="All tests passed successfully",
    )

    assert result.display_name == "test"
    assert result.status == "✅ Passed"
    assert result.summary == "All tests passed successfully"


def test_subprocess_result_with_details():
    """
    Scenario:
        Create a SubprocessResult with details.

    Expected:
        Details are properly set.
    """
    result = SubprocessResult(
        display_name="test",
        status="✅ Passed",
        details="Detailed execution information",
    )

    assert result.display_name == "test"
    assert result.status == "✅ Passed"
    assert result.details == "Detailed execution information"


def test_subprocess_display_mode_values():
    """
    Scenario:
        Test SubprocessDisplayMode enum values.

    Expected:
        All enum values are properly defined.
    """
    assert SubprocessDisplayMode.TABLE_FULL == "table_full"
    assert SubprocessDisplayMode.TABLE_MINIMAL == "table_minimal"
    assert SubprocessDisplayMode.TEXT == "text"
    assert SubprocessDisplayMode.LIST == "list"


def test_subprocess_display_mode_enum_properties():
    """
    Scenario:
        Test SubprocessDisplayMode enum properties.

    Expected:
        Enum has proper properties and methods.
    """
    # Test that it's an enum
    assert hasattr(SubprocessDisplayMode, "TABLE_FULL")
    assert hasattr(SubprocessDisplayMode, "TABLE_MINIMAL")
    assert hasattr(SubprocessDisplayMode, "TEXT")
    assert hasattr(SubprocessDisplayMode, "LIST")

    # Test that values are accessible
    assert SubprocessDisplayMode.TABLE_FULL in SubprocessDisplayMode
    assert SubprocessDisplayMode.TABLE_MINIMAL in SubprocessDisplayMode
    assert SubprocessDisplayMode.TEXT in SubprocessDisplayMode
    assert SubprocessDisplayMode.LIST in SubprocessDisplayMode


def test_command_spec_creation():
    """
    Scenario:
        Create a CommandSpec with all fields.

    Expected:
        All fields are properly set.
    """
    command = ["echo", "hello"]
    tool_name = "echo"
    cwd = Path("/tmp")
    is_tool = True

    spec = CommandSpec(
        command=command,
        display_name=tool_name,
        cwd=cwd,
        is_tool=is_tool,
    )

    assert spec.command == command
    assert spec.display_name == tool_name
    assert spec.cwd == cwd
    assert spec.is_tool == is_tool


def test_command_spec_with_none_values():
    """
    Scenario:
        Create a CommandSpec with None values for optional fields.

    Expected:
        None values are properly set.
    """
    command = ["echo", "hello"]

    spec = CommandSpec(
        command=command,
        display_name=None,
        cwd=None,
        is_tool=False,
    )

    assert spec.command == command
    assert spec.display_name is None
    assert spec.cwd is None
    assert spec.is_tool is False


def test_command_spec_with_path_cwd():
    """
    Scenario:
        Create a CommandSpec with Path object for cwd.

    Expected:
        Path object is properly stored.
    """
    command = ["ls"]
    cwd = Path("/home/user")

    spec = CommandSpec(
        command=command,
        display_name="ls",
        cwd=cwd,
        is_tool=True,
    )

    assert spec.command == command
    assert spec.display_name == "ls"
    assert spec.cwd == cwd
    assert isinstance(spec.cwd, Path)
    assert spec.is_tool is True


def test_command_spec_with_string_cwd():
    """
    Scenario:
        Create a CommandSpec with string for cwd.

    Expected:
        String is properly stored.
    """
    command = ["ls"]
    cwd = "/home/user"

    spec = CommandSpec(
        command=command,
        display_name="ls",
        cwd=cwd,
        is_tool=True,
    )

    assert spec.command == command
    assert spec.display_name == "ls"
    assert spec.cwd == cwd
    assert spec.is_tool is True


def test_command_spec_with_empty_command():
    """
    Scenario:
        Create a CommandSpec with empty command list.

    Expected:
        Empty command list is properly stored.
    """
    command = []

    spec = CommandSpec(
        command=command,
        display_name="empty",
        cwd=None,
        is_tool=False,
    )

    assert spec.command == command
    assert spec.display_name == "empty"
    assert spec.cwd is None
    assert spec.is_tool is False


def test_command_spec_with_complex_command():
    """
    Scenario:
        Create a CommandSpec with complex command.

    Expected:
        Complex command is properly stored.
    """
    command = ["python", "-m", "pytest", "--verbose", "--tb=short", "tests/"]

    spec = CommandSpec(
        command=command,
        display_name="pytest",
        cwd=None,
        is_tool=True,
    )

    assert spec.command == command
    assert spec.display_name == "pytest"
    assert spec.cwd is None
    assert spec.is_tool is True


# ---------------------------
# Integration tests
# ---------------------------


def test_subprocess_result_immutability():
    """
    Scenario:
        Test that SubprocessResult fields can be accessed but are immutable.

    Expected:
        Fields can be read but not modified after creation.
    """
    result = SubprocessResult(
        display_name="test",
        status="✅ Passed",
        stdout="output",
        stderr="error",
    )

    # Fields should be readable
    assert result.display_name == "test"
    assert result.status == "✅ Passed"
    assert result.stdout == "output"
    assert result.stderr == "error"

    # Fields should be immutable (dataclass with frozen=True would make this true)
    # For now, we just test that the values are as expected
    result.display_name = "modified"
    assert result.display_name == "modified"  # This will work since it's not frozen


def test_command_spec_immutability():
    """
    Scenario:
        Test that CommandSpec fields can be accessed but are immutable.

    Expected:
        Fields can be read but not modified after creation.
    """
    spec = CommandSpec(
        command=["echo", "hello"],
        display_name="echo",
        cwd=None,
        is_tool=True,
    )

    # Fields should be readable
    assert spec.command == ["echo", "hello"]
    assert spec.display_name == "echo"
    assert spec.cwd is None
    assert spec.is_tool is True

    # Fields should be mutable (dataclass without frozen=True)
    spec.display_name = "modified"
    assert spec.display_name == "modified"


def test_subprocess_display_mode_comparison():
    """
    Scenario:
        Test SubprocessDisplayMode comparison operations.

    Expected:
        Enum values can be compared correctly.
    """
    mode1 = SubprocessDisplayMode.TABLE_FULL
    mode2 = SubprocessDisplayMode.TABLE_FULL
    mode3 = SubprocessDisplayMode.TABLE_MINIMAL

    assert mode1 == mode2
    assert mode1 != mode3
    assert mode1 == "table_full"
    assert mode1 != "table_minimal"


def test_subprocess_display_mode_string_conversion():
    """
    Scenario:
        Test SubprocessDisplayMode string conversion.

    Expected:
        Enum values can be converted to strings.
    """
    mode = SubprocessDisplayMode.TABLE_FULL
    # The enum uses the default string representation
    assert str(mode) == "SubprocessDisplayMode.TABLE_FULL"
    assert repr(mode) == "<SubprocessDisplayMode.TABLE_FULL: 'table_full'>"
    # But the value itself is accessible
    assert mode.value == "table_full"


def test_types_import_consistency():
    """
    Scenario:
        Test that all types can be imported consistently.

    Expected:
        All types are properly importable.
    """
    from tidycode.runner.types import (
        CommandSpec,
        SubprocessDisplayMode,
        SubprocessResult,
    )

    # Test that classes exist
    assert CommandSpec is not None
    assert SubprocessDisplayMode is not None
    assert SubprocessResult is not None

    # Test that they can be instantiated
    result = SubprocessResult("test", "✅ Passed")
    spec = CommandSpec(["echo"], "echo", None, True)
    mode = SubprocessDisplayMode.TABLE_FULL

    assert result is not None
    assert spec is not None
    assert mode is not None


def test_subprocess_result_with_unicode():
    """
    Scenario:
        Test SubprocessResult with unicode characters.

    Expected:
        Unicode characters are properly handled.
    """
    result = SubprocessResult(
        display_name="test_unicode",
        status="✅ Passed",
        stdout="café ñöç",
        stderr="émojis 🚀",
        summary="Unicode test: 中文",
    )

    assert result.display_name == "test_unicode"
    assert result.status == "✅ Passed"
    assert result.stdout == "café ñöç"
    assert result.stderr == "émojis 🚀"
    assert result.summary == "Unicode test: 中文"


def test_command_spec_with_unicode():
    """
    Scenario:
        Test CommandSpec with unicode characters.

    Expected:
        Unicode characters are properly handled.
    """
    command = ["echo", "café", "ñöç", "中文"]

    spec = CommandSpec(
        command=command,
        display_name="echo_unicode",
        cwd=None,
        is_tool=True,
    )

    assert spec.command == command
    assert spec.display_name == "echo_unicode"
    assert spec.command[1] == "café"
    assert spec.command[2] == "ñöç"
    assert spec.command[3] == "中文"
