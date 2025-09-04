"""
Tests for RuffRunner.
"""

from pathlib import Path

from tidycode.modules.quality.ruff_runner import RuffRunner


class TestRuffRunner:
    """Test cases for RuffRunner."""

    def test_ruff_runner_initialization(self):
        """
        Scenario:
            Initialize RuffRunner.

        Expected:
            RuffRunner is properly initialized.
        """
        runner = RuffRunner()
        assert runner is not None
        assert hasattr(runner, "meta")
        assert runner.meta.name == "ruff"
        assert runner.meta.description == "Ruff runner."
        assert runner.meta.type == "runner"
        assert runner.meta.category == "quality"

    def test_ruff_runner_build_command_with_target(self):
        """
        Scenario:
            Build command with target path.

        Expected:
            Command includes ruff check command (target is ignored).
        """
        runner = RuffRunner()
        target = Path("/path/to/file.py")

        command = runner.build_command(target, None)

        assert command == ["ruff", "check", "--fix"]

    def test_ruff_runner_build_command_without_target(self):
        """
        Scenario:
            Build command without target path.

        Expected:
            Command includes ruff check command.
        """
        runner = RuffRunner()

        command = runner.build_command(None, None)

        assert command == ["ruff", "check", "--fix"]

    def test_ruff_runner_build_command_with_check_only_true(self):
        """
        Scenario:
            Build command with check_only=True.

        Expected:
            Command includes ruff check without --fix flag.
        """
        runner = RuffRunner()
        target = Path("/path/to/file.py")

        command = runner.build_command(target, True)

        assert command == ["ruff", "check"]

    def test_ruff_runner_build_command_with_check_only_false(self):
        """
        Scenario:
            Build command with check_only=False.

        Expected:
            Command includes ruff check with --fix flag.
        """
        runner = RuffRunner()
        target = Path("/path/to/file.py")

        command = runner.build_command(target, False)

        assert command == ["ruff", "check", "--fix"]

    def test_ruff_runner_build_command_with_check_only_none(self):
        """
        Scenario:
            Build command with check_only=None.

        Expected:
            Command includes ruff check with --fix flag.
        """
        runner = RuffRunner()
        target = Path("/path/to/file.py")

        command = runner.build_command(target, None)

        assert command == ["ruff", "check", "--fix"]

    def test_ruff_runner_build_command_with_args_and_kwargs(self):
        """
        Scenario:
            Build command with additional args and kwargs.

        Expected:
            Command ignores additional args and kwargs.
        """
        runner = RuffRunner()
        target = Path("/path/to/file.py")

        command = runner.build_command(
            target, True, "extra_arg1", "extra_arg2", verbose=True, debug=False
        )

        assert command == ["ruff", "check"]

    def test_ruff_runner_build_command_empty_target(self):
        """
        Scenario:
            Build command with empty target.

        Expected:
            Command handles empty target correctly (target is ignored).
        """
        runner = RuffRunner()
        target = Path("")

        command = runner.build_command(target, None)

        assert command == ["ruff", "check", "--fix"]

    def test_ruff_runner_build_command_unicode_target(self):
        """
        Scenario:
            Build command with unicode target path.

        Expected:
            Command handles unicode target correctly (target is ignored).
        """
        runner = RuffRunner()
        target = Path("/path/à/fichier.py")

        command = runner.build_command(target, None)

        assert command == ["ruff", "check", "--fix"]

    def test_ruff_runner_build_command_return_type(self):
        """
        Scenario:
            Build command returns correct type.

        Expected:
            Command returns List[str].
        """
        runner = RuffRunner()
        target = Path("/path/to/file.py")

        command = runner.build_command(target, None)

        assert isinstance(command, list)
        assert all(isinstance(item, str) for item in command)

    def test_ruff_runner_build_command_empty_list(self):
        """
        Scenario:
            Build command with minimal parameters.

        Expected:
            Command returns ruff check command.
        """
        runner = RuffRunner()

        command = runner.build_command(None, None)

        assert command == ["ruff", "check", "--fix"]
        assert len(command) == 3

    def test_ruff_runner_build_command_with_unicode(self):
        """
        Scenario:
            Build command with unicode characters.

        Expected:
            Command handles unicode correctly (target is ignored).
        """
        runner = RuffRunner()
        target = Path("/path/测试/文件.py")

        command = runner.build_command(target, True)

        assert command == ["ruff", "check"]

    def test_ruff_runner_with_register_plugin(self):
        """
        Scenario:
            Test that RuffRunner is properly registered as a plugin.

        Expected:
            RuffRunner is registered with correct metadata.
        """
        runner = RuffRunner()

        # Verify the plugin is registered
        assert runner.meta.name == "ruff"
        assert runner.meta.description == "Ruff runner."
        assert runner.meta.type == "runner"
        assert runner.meta.category == "quality"

    def test_ruff_runner_multiple_implementations(self):
        """
        Scenario:
            Create multiple RuffRunner instances.

        Expected:
            Each instance is independent.
        """
        runner1 = RuffRunner()
        runner2 = RuffRunner()

        target = Path("/path/to/file.py")
        command1 = runner1.build_command(target, True)
        command2 = runner2.build_command(target, False)

        assert command1 == ["ruff", "check"]
        assert command2 == ["ruff", "check", "--fix"]
        assert command1 != command2

    def test_ruff_runner_import_consistency(self):
        """
        Scenario:
            Test that RuffRunner can be imported consistently.

        Expected:
            RuffRunner is properly importable from different paths.
        """
        # Test direct import
        # Test import from module
        from tidycode.modules.quality import ruff_runner
        from tidycode.modules.quality.ruff_runner import RuffRunner as DirectRuffRunner

        # Verify both imports work
        assert DirectRuffRunner is not None
        assert ruff_runner.RuffRunner is not None
        assert DirectRuffRunner is ruff_runner.RuffRunner
