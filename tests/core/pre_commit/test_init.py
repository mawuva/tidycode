"""
TidyCode Pre-commit Module Initialization Tests
"""

from tidycode.core.pre_commit import PreCommitManager, normalize_pre_commit_file


def test_pre_commit_module_imports():
    """
    Scenario:
        Import the pre-commit module and check that all expected functions and classes are available.

    Expected:
        All expected functions and classes are imported correctly.
    """
    # Test that function is callable
    assert callable(normalize_pre_commit_file)

    # Test that class is available
    assert PreCommitManager is not None

    # Test that class can be instantiated (with proper file)
    # This is a basic import test, actual functionality is tested in other test files


def test_pre_commit_module_all_exports():
    """
    Scenario:
        Check that the module's __all__ list contains all expected exports.

    Expected:
        All expected items are in __all__.
    """
    from tidycode.core.pre_commit import __all__

    expected_exports = ["normalize_pre_commit_file", "PreCommitManager"]

    for export in expected_exports:
        assert export in __all__

    # Ensure no unexpected exports
    assert len(__all__) == len(expected_exports)
