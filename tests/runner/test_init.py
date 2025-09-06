"""
TidyCode Runner Module Initialization Tests
"""

from tidycode.runner import (
    CommandSpec,
    SubprocessDisplayMode,
    SubprocessResult,
    print_summary
)

from tidycode.runner.subprocess import run_multiple_commands, run_plugins


def test_runner_module_imports():
    """
    Scenario:
        Import the runner module and check that all expected functions and classes are available.

    Expected:
        All expected functions and classes are imported correctly.
    """
    # Test that functions are callable
    assert callable(run_multiple_commands)
    assert callable(run_plugins)
    assert callable(print_summary)

    # Test that classes are available
    assert CommandSpec is not None
    assert SubprocessResult is not None
    assert SubprocessDisplayMode is not None

    # Test that classes can be instantiated (with proper parameters)
    # This is a basic import test, actual functionality is tested in other test files
    result = SubprocessResult("test", "✅ Passed")
    spec = CommandSpec(["echo"], "echo", None, True)
    mode = SubprocessDisplayMode.TABLE_FULL

    assert result is not None
    assert spec is not None
    assert mode is not None


def test_runner_module_all_exports():
    """
    Scenario:
        Check that the module's __all__ list contains all expected exports.

    Expected:
        All expected items are in __all__.
    """
    from tidycode.runner import __all__

    expected_exports = [
        "CommandSpec",
        "SubprocessResult",
        "SubprocessDisplayMode",
        "print_summary",
        "run_command",
        "run_command_live",
    ]

    for export in expected_exports:
        assert export in __all__

    # Ensure no unexpected exports
    assert len(__all__) == len(expected_exports)


def test_runner_module_import_consistency():
    """
    Scenario:
        Test that imports work consistently from different paths.

    Expected:
        All imports work correctly.
    """
    # Test direct imports
    from tidycode.runner import (
        CommandSpec,
        SubprocessDisplayMode,
        SubprocessResult,
        print_summary,
    )
    from tidycode.runner.subprocess import run_multiple_commands, run_plugins

    assert run_multiple_commands is not None
    assert run_plugins is not None
    assert CommandSpec is not None
    assert SubprocessResult is not None
    assert SubprocessDisplayMode is not None
    assert print_summary is not None

    # Test that they are the same objects
    from tidycode.runner.display import print_summary as display_print_summary
    from tidycode.runner.subprocess import (
        run_multiple_commands as subprocess_run_multiple_commands,
        run_plugins as subprocess_run_plugins,
    )
    from tidycode.runner.types import CommandSpec as types_CommandSpec
    from tidycode.runner.types import (
        SubprocessDisplayMode as types_SubprocessDisplayMode,
    )
    from tidycode.runner.types import SubprocessResult as types_SubprocessResult

    assert run_multiple_commands is subprocess_run_multiple_commands
    assert run_plugins is subprocess_run_plugins
    assert CommandSpec is types_CommandSpec
    assert SubprocessResult is types_SubprocessResult
    assert SubprocessDisplayMode is types_SubprocessDisplayMode
    assert print_summary is display_print_summary


def test_runner_module_function_signatures():
    """
    Scenario:
        Test that imported functions have expected signatures.

    Expected:
        Functions have the expected signatures.
    """
    import inspect

    # Test run_multiple_commands signature
    run_multiple_commands_sig = inspect.signature(run_multiple_commands)
    expected_params = ["commands", "live", "verbose", "summary_display_mode"]
    for param in expected_params:
        assert param in run_multiple_commands_sig.parameters

    # Test print_summary signature
    print_summary_sig = inspect.signature(print_summary)
    expected_params = ["results", "mode"]
    for param in expected_params:
        assert param in print_summary_sig.parameters


def test_runner_module_class_attributes():
    """
    Scenario:
        Test that imported classes have expected attributes.

    Expected:
        Classes have the expected attributes.
    """
    # Test SubprocessResult attributes
    result = SubprocessResult("test", "✅ Passed")
    expected_attrs = [
        "display_name",
        "status",
        "stdout",
        "stderr",
        "category",
        "summary",
        "details",
    ]
    for attr in expected_attrs:
        assert hasattr(result, attr)

    # Test CommandSpec attributes
    spec = CommandSpec(["echo"], "echo", None, True)
    expected_attrs = ["command", "display_name", "cwd", "is_tool"]
    for attr in expected_attrs:
        assert hasattr(spec, attr)

    # Test SubprocessDisplayMode attributes
    expected_modes = ["TABLE_FULL", "TABLE_MINIMAL", "TEXT", "LIST"]
    for mode in expected_modes:
        assert hasattr(SubprocessDisplayMode, mode)


def test_runner_module_enum_values():
    """
    Scenario:
        Test that SubprocessDisplayMode enum has correct values.

    Expected:
        Enum values are correct.
    """
    assert SubprocessDisplayMode.TABLE_FULL == "table_full"
    assert SubprocessDisplayMode.TABLE_MINIMAL == "table_minimal"
    assert SubprocessDisplayMode.TEXT == "text"
    assert SubprocessDisplayMode.LIST == "list"
