"""
Tests for IsortRunner.
"""

from pathlib import Path

from tidycode.modules.quality.isort_runner import IsortRunner


class TestIsortRunner:
    """Test cases for IsortRunner."""

    def test_isort_runner_initialization(self):
        """
        Scenario:
            Initialize IsortRunner.

        Expected:
            IsortRunner is properly initialized.
        """
        runner = IsortRunner()
        assert runner is not None
        assert hasattr(runner, "meta")
        assert runner.meta.name == "isort"
        assert runner.meta.description == "Isort runner."
        assert runner.meta.type == "runner"
        assert runner.meta.category == "quality"

    def test_isort_runner_build_command_with_target(self):
        """
        Scenario:
            Build command with target path.

        Expected:
            Command includes target path.
        """
        runner = IsortRunner()
        target = Path("/path/to/file.py")

        command = runner.build_command(target, None)

        assert command == ["isort", str(target)]

    def test_isort_runner_build_command_without_target(self):
        """
        Scenario:
            Build command without target path.

        Expected:
            Command does not include target path.
        """
        runner = IsortRunner()

        command = runner.build_command(None, None)

        assert command == ["isort"]

    def test_isort_runner_build_command_with_check_only(self):
        """
        Scenario:
            Build command with check_only=True.

        Expected:
            Command includes --check-only flag.
        """
        runner = IsortRunner()
        target = Path("/path/to/file.py")

        command = runner.build_command(target, True)

        assert command == ["isort", str(target), "--check-only"]

    def test_isort_runner_build_command_with_check_only_false(self):
        """
        Scenario:
            Build command with check_only=False.

        Expected:
            Command does not include --check-only flag.
        """
        runner = IsortRunner()
        target = Path("/path/to/file.py")

        command = runner.build_command(target, False)

        assert command == ["isort", str(target)]

    def test_isort_runner_build_command_with_check_only_none(self):
        """
        Scenario:
            Build command with check_only=None.

        Expected:
            Command does not include --check-only flag.
        """
        runner = IsortRunner()
        target = Path("/path/to/file.py")

        command = runner.build_command(target, None)

        assert command == ["isort", str(target)]

    def test_isort_runner_build_command_with_args_and_kwargs(self):
        """
        Scenario:
            Build command with additional args and kwargs.

        Expected:
            Command ignores additional args and kwargs.
        """
        runner = IsortRunner()
        target = Path("/path/to/file.py")

        command = runner.build_command(
            target, True, "extra_arg1", "extra_arg2", verbose=True, debug=False
        )

        assert command == ["isort", str(target), "--check-only"]

    def test_isort_runner_build_command_empty_target(self):
        """
        Scenario:
            Build command with empty target.

        Expected:
            Command handles empty target correctly.
        """
        runner = IsortRunner()
        target = Path("")

        command = runner.build_command(target, None)

        assert command == ["isort", "."]

    def test_isort_runner_build_command_unicode_target(self):
        """
        Scenario:
            Build command with unicode target path.

        Expected:
            Command handles unicode target correctly.
        """
        runner = IsortRunner()
        target = Path("/path/à/fichier.py")

        command = runner.build_command(target, None)

        assert command == ["isort", str(target)]

    def test_isort_runner_build_command_return_type(self):
        """
        Scenario:
            Build command returns correct type.

        Expected:
            Command returns List[str].
        """
        runner = IsortRunner()
        target = Path("/path/to/file.py")

        command = runner.build_command(target, None)

        assert isinstance(command, list)
        assert all(isinstance(item, str) for item in command)

    def test_isort_runner_build_command_empty_list(self):
        """
        Scenario:
            Build command with minimal parameters.

        Expected:
            Command returns minimal list.
        """
        runner = IsortRunner()

        command = runner.build_command(None, None)

        assert command == ["isort"]
        assert len(command) == 1

    def test_isort_runner_build_command_with_unicode(self):
        """
        Scenario:
            Build command with unicode characters.

        Expected:
            Command handles unicode correctly.
        """
        runner = IsortRunner()
        target = Path("/path/测试/文件.py")

        command = runner.build_command(target, True)

        assert command == ["isort", str(target), "--check-only"]

    def test_isort_runner_with_register_plugin(self):
        """
        Scenario:
            Test that IsortRunner is properly registered as a plugin.

        Expected:
            IsortRunner is registered with correct metadata.
        """
        runner = IsortRunner()

        # Verify the plugin is registered
        assert runner.meta.name == "isort"
        assert runner.meta.description == "Isort runner."
        assert runner.meta.type == "runner"
        assert runner.meta.category == "quality"

    def test_isort_runner_multiple_implementations(self):
        """
        Scenario:
            Create multiple IsortRunner instances.

        Expected:
            Each instance is independent.
        """
        runner1 = IsortRunner()
        runner2 = IsortRunner()

        target = Path("/path/to/file.py")
        command1 = runner1.build_command(target, True)
        command2 = runner2.build_command(target, False)

        assert command1 == ["isort", str(target), "--check-only"]
        assert command2 == ["isort", str(target)]
        assert command1 != command2

    def test_isort_runner_import_consistency(self):
        """
        Scenario:
            Test that IsortRunner can be imported consistently.

        Expected:
            IsortRunner is properly importable from different paths.
        """
        # Test direct import
        # Test import from module
        from tidycode.modules.quality import isort_runner
        from tidycode.modules.quality.isort_runner import (
            IsortRunner as DirectIsortRunner,
        )

        # Verify both imports work
        assert DirectIsortRunner is not None
        assert isort_runner.IsortRunner is not None
        assert DirectIsortRunner is isort_runner.IsortRunner
