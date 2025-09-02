"""
TidyCode Changelog Manager Initialization Tests
"""

from tidycode.changelog.manager import ChangeLogManager


def test_changelog_manager_init():
    """
    Scenario:
        Initialize ChangeLogManager.

    Expected:
        Manager is created with empty entries list.
    """
    manager = ChangeLogManager()
    assert manager.entries == []
    assert len(manager.entries) == 0


def test_changelog_manager_init_multiple_instances():
    """
    Scenario:
        Create multiple ChangeLogManager instances.

    Expected:
        Each instance has its own independent entries list.
    """
    manager1 = ChangeLogManager()
    manager2 = ChangeLogManager()

    assert manager1.entries is not manager2.entries
    assert len(manager1.entries) == 0
    assert len(manager2.entries) == 0
