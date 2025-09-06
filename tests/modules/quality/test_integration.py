"""
Integration tests for quality module.
"""

from pathlib import Path
from unittest import mock

from tidycode.modules.quality.black_runner import BlackRunner
from tidycode.modules.quality.isort_runner import IsortRunner
from tidycode.modules.quality.mypy_runner import MypyRunner
from tidycode.modules.quality.ruff_runner import RuffRunner


class TestQualityModuleIntegration:
    """Integration test cases for quality module."""

    def test_all_runners_initialization(self):
        """
        Scenario:
            Initialize all quality runners.

        Expected:
            All runners are properly initialized with correct metadata.
        """
        runners = [
            BlackRunner(),
            IsortRunner(),
            MypyRunner(),
            RuffRunner(),
        ]

        expected_names = ["black", "isort", "mypy", "ruff"]
        expected_categories = ["quality"] * 4
        expected_types = ["runner"] * 4

        for runner, name, category, type_ in zip(
            runners, expected_names, expected_categories, expected_types
        ):
            assert runner.meta.name == name
            assert runner.meta.category == category
            assert runner.meta.type == type_

    def test_all_runners_build_command_consistency(self):
        """
        Scenario:
            Test that all runners build commands consistently.

        Expected:
            All runners return List[str] and handle parameters consistently.
        """
        runners = [
            BlackRunner(),
            IsortRunner(),
            MypyRunner(),
            RuffRunner(),
        ]

        target = Path("/path/to/file.py")

        for runner in runners:
            # Test with target
            command = runner.build_command(target, None)
            assert isinstance(command, list)
            assert all(isinstance(item, str) for item in command)
            assert len(command) > 0

            # Test without target
            command_no_target = runner.build_command(None, None)
            assert isinstance(command_no_target, list)
            assert all(isinstance(item, str) for item in command_no_target)
            assert len(command_no_target) > 0

            # Test with check_only=True
            command_check = runner.build_command(target, True)
            assert isinstance(command_check, list)
            assert all(isinstance(item, str) for item in command_check)

    def test_runners_specific_behavior(self):
        """
        Scenario:
            Test specific behavior of each runner.

        Expected:
            Each runner behaves according to its specific implementation.
        """
        target = Path("/path/to/file.py")

        # Test BlackRunner
        black_runner = BlackRunner()
        black_command = black_runner.build_command(target, True)
        assert black_command == ["black", str(target), "--check"]

        # Test IsortRunner
        isort_runner = IsortRunner()
        isort_command = isort_runner.build_command(target, True)
        assert isort_command == ["isort", str(target), "--check-only"]

        # Test MypyRunner (doesn't support check_only)
        mypy_runner = MypyRunner()
        mypy_command = mypy_runner.build_command(target, True)
        assert mypy_command == ["mypy", str(target)]

        # Test RuffRunner
        ruff_runner = RuffRunner()
        ruff_command = ruff_runner.build_command(target, True)
        assert ruff_command == ["ruff", "check"]
        ruff_command_fix = ruff_runner.build_command(target, False)
        assert ruff_command_fix == ["ruff", "check", "--fix"]

    def test_runners_with_unicode_paths(self):
        """
        Scenario:
            Test all runners with unicode paths.

        Expected:
            All runners handle unicode paths correctly.
        """
        runners = [
            BlackRunner(),
            IsortRunner(),
            MypyRunner(),
            RuffRunner(),
        ]

        unicode_target = Path("/path/测试/文件.py")

        for runner in runners:
            command = runner.build_command(unicode_target, None)
            assert isinstance(command, list)
            assert all(isinstance(item, str) for item in command)
            # Verify that the unicode path is properly converted to string
            # Note: RuffRunner doesn't include the target in its command
            if runner.meta.name != "ruff" and len(command) > 1:
                assert str(unicode_target) in command

    def test_runners_with_empty_paths(self):
        """
        Scenario:
            Test all runners with empty paths.

        Expected:
            All runners handle empty paths correctly.
        """
        runners = [
            BlackRunner(),
            IsortRunner(),
            MypyRunner(),
            RuffRunner(),
        ]

        empty_target = Path("")

        for runner in runners:
            command = runner.build_command(empty_target, None)
            assert isinstance(command, list)
            assert all(isinstance(item, str) for item in command)

    def test_runners_with_args_and_kwargs(self):
        """
        Scenario:
            Test all runners with additional args and kwargs.

        Expected:
            All runners ignore additional args and kwargs.
        """
        runners = [
            BlackRunner(),
            IsortRunner(),
            MypyRunner(),
            RuffRunner(),
        ]

        target = Path("/path/to/file.py")

        for runner in runners:
            # Test with args and kwargs
            command_with_extras = runner.build_command(
                target,
                True,
                "extra_arg1",
                "extra_arg2",
                verbose=True,
                debug=False,
                output="/output/path",
            )

            # Test without extras
            command_simple = runner.build_command(target, True)

            # Commands should be the same (extras are ignored)
            assert command_with_extras == command_simple

    def test_runners_plugin_registration(self):
        """
        Scenario:
            Test that all runners are properly registered as plugins.

        Expected:
            All runners have correct plugin metadata.
        """
        runners = [
            BlackRunner(),
            IsortRunner(),
            MypyRunner(),
            RuffRunner(),
        ]

        for runner in runners:
            # Verify plugin metadata
            assert hasattr(runner, "meta")
            assert runner.meta.name is not None
            assert runner.meta.description is not None
            assert runner.meta.type == "runner"
            assert runner.meta.category == "quality"

    def test_runners_import_consistency(self):
        """
        Scenario:
            Test that all runners can be imported consistently.

        Expected:
            All runners are importable from their respective modules.
        """
        # Test direct imports
        # Test module imports
        from tidycode.modules.quality import (
            black_runner,
            isort_runner,
            mypy_runner,
            ruff_runner,
        )
        from tidycode.modules.quality.black_runner import BlackRunner
        from tidycode.modules.quality.isort_runner import IsortRunner
        from tidycode.modules.quality.mypy_runner import MypyRunner
        from tidycode.modules.quality.ruff_runner import RuffRunner

        # Verify consistency
        assert BlackRunner is black_runner.BlackRunner
        assert IsortRunner is isort_runner.IsortRunner
        assert MypyRunner is mypy_runner.MypyRunner
        assert RuffRunner is ruff_runner.RuffRunner

    def test_runners_command_building_edge_cases(self):
        """
        Scenario:
            Test command building with edge cases.

        Expected:
            All runners handle edge cases gracefully.
        """
        runners = [
            BlackRunner(),
            IsortRunner(),
            MypyRunner(),
            RuffRunner(),
        ]

        # Test with None target
        for runner in runners:
            command = runner.build_command(None, None)
            assert isinstance(command, list)
            assert len(command) > 0

        # Test with None check_only
        target = Path("/path/to/file.py")
        for runner in runners:
            command = runner.build_command(target, None)
            assert isinstance(command, list)
            assert len(command) > 0

        # Test with False check_only
        for runner in runners:
            command = runner.build_command(target, False)
            assert isinstance(command, list)
            assert len(command) > 0

    def test_runners_performance_consistency(self):
        """
        Scenario:
            Test that all runners perform consistently.

        Expected:
            All runners return results in reasonable time.
        """
        import time

        runners = [
            BlackRunner(),
            IsortRunner(),
            MypyRunner(),
            RuffRunner(),
        ]

        target = Path("/path/to/file.py")

        for runner in runners:
            start_time = time.time()
            command = runner.build_command(target, True)
            end_time = time.time()

            # Command building should be fast (less than 1 second)
            assert end_time - start_time < 1.0
            assert isinstance(command, list)
