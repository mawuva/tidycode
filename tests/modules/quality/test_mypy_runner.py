"""
Tests for MypyRunner.
"""

import pytest
from pathlib import Path
from unittest import mock

from tidycode.modules.quality.mypy_runner import MypyRunner


class TestMypyRunner:
    """Test cases for MypyRunner."""

    def test_mypy_runner_initialization(self):
        """
        Scenario:
            Initialize MypyRunner.

        Expected:
            MypyRunner is properly initialized.
        """
        runner = MypyRunner()
        assert runner is not None
        assert hasattr(runner, "meta")
        assert runner.meta.name == "mypy"
        assert runner.meta.description == "Mypy runner."
        assert runner.meta.type == "runner"
        assert runner.meta.category == "quality"

    def test_mypy_runner_build_command_with_target(self):
        """
        Scenario:
            Build command with target path.

        Expected:
            Command includes target path.
        """
        runner = MypyRunner()
        target = Path("/path/to/file.py")
        
        command = runner.build_command(target, None)
        
        assert command == ["mypy", str(target)]

    def test_mypy_runner_build_command_without_target(self):
        """
        Scenario:
            Build command without target path.

        Expected:
            Command does not include target path.
        """
        runner = MypyRunner()
        
        command = runner.build_command(None, None)
        
        assert command == ["mypy"]

    def test_mypy_runner_build_command_with_check_only(self):
        """
        Scenario:
            Build command with check_only=True.

        Expected:
            Command does not include check_only flag (mypy doesn't support it).
        """
        runner = MypyRunner()
        target = Path("/path/to/file.py")
        
        command = runner.build_command(target, True)
        
        assert command == ["mypy", str(target)]

    def test_mypy_runner_build_command_with_check_only_false(self):
        """
        Scenario:
            Build command with check_only=False.

        Expected:
            Command does not include check_only flag.
        """
        runner = MypyRunner()
        target = Path("/path/to/file.py")
        
        command = runner.build_command(target, False)
        
        assert command == ["mypy", str(target)]

    def test_mypy_runner_build_command_with_check_only_none(self):
        """
        Scenario:
            Build command with check_only=None.

        Expected:
            Command does not include check_only flag.
        """
        runner = MypyRunner()
        target = Path("/path/to/file.py")
        
        command = runner.build_command(target, None)
        
        assert command == ["mypy", str(target)]

    def test_mypy_runner_build_command_with_args_and_kwargs(self):
        """
        Scenario:
            Build command with additional args and kwargs.

        Expected:
            Command ignores additional args and kwargs.
        """
        runner = MypyRunner()
        target = Path("/path/to/file.py")
        
        command = runner.build_command(
            target, 
            True, 
            "extra_arg1", 
            "extra_arg2",
            verbose=True,
            debug=False
        )
        
        assert command == ["mypy", str(target)]

    def test_mypy_runner_build_command_empty_target(self):
        """
        Scenario:
            Build command with empty target.

        Expected:
            Command handles empty target correctly.
        """
        runner = MypyRunner()
        target = Path("")
        
        command = runner.build_command(target, None)
        
        assert command == ["mypy", "."]

    def test_mypy_runner_build_command_unicode_target(self):
        """
        Scenario:
            Build command with unicode target path.

        Expected:
            Command handles unicode target correctly.
        """
        runner = MypyRunner()
        target = Path("/path/à/fichier.py")
        
        command = runner.build_command(target, None)
        
        assert command == ["mypy", str(target)]

    def test_mypy_runner_build_command_return_type(self):
        """
        Scenario:
            Build command returns correct type.

        Expected:
            Command returns List[str].
        """
        runner = MypyRunner()
        target = Path("/path/to/file.py")
        
        command = runner.build_command(target, None)
        
        assert isinstance(command, list)
        assert all(isinstance(item, str) for item in command)

    def test_mypy_runner_build_command_empty_list(self):
        """
        Scenario:
            Build command with minimal parameters.

        Expected:
            Command returns minimal list.
        """
        runner = MypyRunner()
        
        command = runner.build_command(None, None)
        
        assert command == ["mypy"]
        assert len(command) == 1

    def test_mypy_runner_build_command_with_unicode(self):
        """
        Scenario:
            Build command with unicode characters.

        Expected:
            Command handles unicode correctly.
        """
        runner = MypyRunner()
        target = Path("/path/测试/文件.py")
        
        command = runner.build_command(target, True)
        
        assert command == ["mypy", str(target)]

    def test_mypy_runner_with_register_plugin(self):
        """
        Scenario:
            Test that MypyRunner is properly registered as a plugin.

        Expected:
            MypyRunner is registered with correct metadata.
        """
        runner = MypyRunner()
        
        # Verify the plugin is registered
        assert runner.meta.name == "mypy"
        assert runner.meta.description == "Mypy runner."
        assert runner.meta.type == "runner"
        assert runner.meta.category == "quality"

    def test_mypy_runner_multiple_implementations(self):
        """
        Scenario:
            Create multiple MypyRunner instances.

        Expected:
            Each instance is independent.
        """
        runner1 = MypyRunner()
        runner2 = MypyRunner()
        
        target = Path("/path/to/file.py")
        command1 = runner1.build_command(target, True)
        command2 = runner2.build_command(target, False)
        
        # Both commands should be the same since mypy doesn't support check_only
        assert command1 == ["mypy", str(target)]
        assert command2 == ["mypy", str(target)]
        assert command1 == command2

    def test_mypy_runner_import_consistency(self):
        """
        Scenario:
            Test that MypyRunner can be imported consistently.

        Expected:
            MypyRunner is properly importable from different paths.
        """
        # Test direct import
        from tidycode.modules.quality.mypy_runner import MypyRunner as DirectMypyRunner
        
        # Test import from module
        from tidycode.modules.quality import mypy_runner
        
        # Verify both imports work
        assert DirectMypyRunner is not None
        assert mypy_runner.MypyRunner is not None
        assert DirectMypyRunner is mypy_runner.MypyRunner
