"""
Tests for BlackRunner.
"""

from pathlib import Path

from tidycode.modules.quality.black_runner import BlackRunner


class TestBlackRunner:
    """Test cases for BlackRunner."""

    def test_black_runner_initialization(self):
        """
        Scenario:
            Initialize BlackRunner.

        Expected:
            BlackRunner is properly initialized.
        """
        runner = BlackRunner()
        assert runner is not None
        assert hasattr(runner, "meta")
        assert runner.meta.name == "black"
        assert runner.meta.description == "Black runner."
        assert runner.meta.type == "runner"
        assert runner.meta.category == "quality"

    def test_black_runner_build_command_with_target(self):
        """
        Scenario:
            Build command with target path.

        Expected:
            Command includes target path.
        """
        runner = BlackRunner()
        target = Path("/path/to/file.py")

        command = runner.build_command(target, None)

        assert command == ["black", str(target)]

    def test_black_runner_build_command_without_target(self):
        """
        Scenario:
            Build command without target path.

        Expected:
            Command does not include target path.
        """
        runner = BlackRunner()

        command = runner.build_command(None, None)

        assert command == ["black"]

    def test_black_runner_build_command_with_check_only(self):
        """
        Scenario:
            Build command with check_only=True.

        Expected:
            Command includes --check flag.
        """
        runner = BlackRunner()
        target = Path("/path/to/file.py")

        command = runner.build_command(target, True)

        assert command == ["black", str(target), "--check"]

    def test_black_runner_build_command_with_check_only_false(self):
        """
        Scenario:
            Build command with check_only=False.

        Expected:
            Command does not include --check flag.
        """
        runner = BlackRunner()
        target = Path("/path/to/file.py")

        command = runner.build_command(target, False)

        assert command == ["black", str(target)]

    def test_black_runner_build_command_with_check_only_none(self):
        """
        Scenario:
            Build command with check_only=None.

        Expected:
            Command does not include --check flag.
        """
        runner = BlackRunner()
        target = Path("/path/to/file.py")

        command = runner.build_command(target, None)

        assert command == ["black", str(target)]

    def test_black_runner_build_command_with_args_and_kwargs(self):
        """
        Scenario:
            Build command with additional args and kwargs.

        Expected:
            Command ignores additional args and kwargs.
        """
        runner = BlackRunner()
        target = Path("/path/to/file.py")

        command = runner.build_command(
            target, True, "extra_arg1", "extra_arg2", verbose=True, debug=False
        )

        assert command == ["black", str(target), "--check"]

    def test_black_runner_build_command_empty_target(self):
        """
        Scenario:
            Build command with empty target.

        Expected:
            Command handles empty target correctly.
        """
        runner = BlackRunner()
        target = Path("")

        command = runner.build_command(target, None)

        assert command == ["black", "."]

    def test_black_runner_build_command_unicode_target(self):
        """
        Scenario:
            Build command with unicode target path.

        Expected:
            Command handles unicode target correctly.
        """
        runner = BlackRunner()
        target = Path("/path/à/fichier.py")

        command = runner.build_command(target, None)

        assert command == ["black", str(target)]

    def test_black_runner_build_command_return_type(self):
        """
        Scenario:
            Build command returns correct type.

        Expected:
            Command returns List[str].
        """
        runner = BlackRunner()
        target = Path("/path/to/file.py")

        command = runner.build_command(target, None)

        assert isinstance(command, list)
        assert all(isinstance(item, str) for item in command)

    def test_black_runner_build_command_empty_list(self):
        """
        Scenario:
            Build command with minimal parameters.

        Expected:
            Command returns minimal list.
        """
        runner = BlackRunner()

        command = runner.build_command(None, None)

        assert command == ["black"]
        assert len(command) == 1

    def test_black_runner_build_command_with_unicode(self):
        """
        Scenario:
            Build command with unicode characters.

        Expected:
            Command handles unicode correctly.
        """
        runner = BlackRunner()
        target = Path("/path/测试/文件.py")

        command = runner.build_command(target, True)

        assert command == ["black", str(target), "--check"]

    def test_black_runner_with_register_plugin(self):
        """
        Scenario:
            Test that BlackRunner is properly registered as a plugin.

        Expected:
            BlackRunner is registered with correct metadata.
        """
        runner = BlackRunner()

        # Verify the plugin is registered
        assert runner.meta.name == "black"
        assert runner.meta.description == "Black runner."
        assert runner.meta.type == "runner"
        assert runner.meta.category == "quality"

    def test_black_runner_multiple_implementations(self):
        """
        Scenario:
            Create multiple BlackRunner instances.

        Expected:
            Each instance is independent.
        """
        runner1 = BlackRunner()
        runner2 = BlackRunner()

        target = Path("/path/to/file.py")
        command1 = runner1.build_command(target, True)
        command2 = runner2.build_command(target, False)

        assert command1 == ["black", str(target), "--check"]
        assert command2 == ["black", str(target)]
        assert command1 != command2

    def test_black_runner_import_consistency(self):
        """
        Scenario:
            Test that BlackRunner can be imported consistently.

        Expected:
            BlackRunner is properly importable from different paths.
        """
        # Test direct import
        # Test import from module
        from tidycode.modules.quality import black_runner
        from tidycode.modules.quality.black_runner import (
            BlackRunner as DirectBlackRunner,
        )

        # Verify both imports work
        assert DirectBlackRunner is not None
        assert black_runner.BlackRunner is not None
        assert DirectBlackRunner is black_runner.BlackRunner
