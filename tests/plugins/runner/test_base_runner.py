"""
TidyCode Plugins Runner Base Tests
"""

from pathlib import Path

import pytest

from tidycode.plugins.base import BasePlugin
from tidycode.plugins.runner.base_runner import BaseRunner
from tidycode.plugins.types import PluginMeta

# ---------------------------
# Unit tests
# ---------------------------


def test_base_runner_inheritance():
    """
    Scenario:
        Test that BaseRunner inherits from BasePlugin.

    Expected:
        BaseRunner is a subclass of BasePlugin.
    """
    # BasePlugin is a Protocol, so we can't use issubclass directly
    # Instead, we test that BaseRunner has the required attributes
    assert hasattr(BaseRunner, "__bases__")
    # Check that BasePlugin is in the MRO (Method Resolution Order)
    assert BasePlugin in BaseRunner.__mro__


def test_base_runner_is_abstract():
    """
    Scenario:
        Test that BaseRunner is an abstract class.

    Expected:
        BaseRunner cannot be instantiated directly.
    """
    with pytest.raises(TypeError):
        BaseRunner()


def test_base_runner_build_command_abstract():
    """
    Scenario:
        Test that build_command is an abstract method.

    Expected:
        Subclasses must implement build_command method.
    """

    class IncompleteRunner(BaseRunner):
        pass

    with pytest.raises(TypeError):
        IncompleteRunner()


def test_base_runner_build_command_implementation():
    """
    Scenario:
        Test a concrete implementation of BaseRunner.

    Expected:
        Concrete implementation can be instantiated and build_command works.
    """

    class ConcreteRunner(BaseRunner):
        def build_command(self, target, check_only, *args, **kwargs):
            return ["concrete", "command"]

    runner = ConcreteRunner()
    assert isinstance(runner, BaseRunner)
    # BasePlugin is a Protocol, so we can't use isinstance directly
    # Instead, we test that the runner has the required methods
    assert hasattr(runner, "build_command")
    assert hasattr(runner, "is_tool")

    command = runner.build_command(None, None)
    assert command == ["concrete", "command"]


def test_base_runner_build_command_with_parameters():
    """
    Scenario:
        Test build_command with various parameters.

    Expected:
        build_command receives and can use all parameters.
    """

    class ParameterRunner(BaseRunner):
        def build_command(self, target, check_only, *args, **kwargs):
            cmd = ["parameter", "command"]
            if target:
                cmd.append(str(target))
            if check_only:
                cmd.append("--check")
            if args:
                cmd.extend(args)
            if kwargs:
                cmd.extend([f"--{k}={v}" for k, v in kwargs.items()])
            return cmd

    runner = ParameterRunner()

    # Test with target
    target = Path("/test/path")
    command = runner.build_command(target, None)
    assert str(target) in command

    # Test with check_only
    command = runner.build_command(None, True)
    assert "--check" in command

    # Test with args
    command = runner.build_command(None, None, "arg1", "arg2")
    assert "arg1" in command
    assert "arg2" in command

    # Test with kwargs
    command = runner.build_command(None, None, verbose=True, debug=False)
    assert "--verbose=True" in command
    assert "--debug=False" in command


def test_base_runner_is_tool_default():
    """
    Scenario:
        Test the default is_tool method.

    Expected:
        is_tool returns True by default.
    """

    class DefaultRunner(BaseRunner):
        def build_command(self, target, check_only, *args, **kwargs):
            return ["default", "command"]

    runner = DefaultRunner()
    assert runner.is_tool() is True


def test_base_runner_is_tool_override():
    """
    Scenario:
        Test overriding the is_tool method.

    Expected:
        is_tool can be overridden in subclasses.
    """

    class NonToolRunner(BaseRunner):
        def build_command(self, target, check_only, *args, **kwargs):
            return ["non-tool", "command"]

        def is_tool(self):
            return False

    runner = NonToolRunner()
    assert runner.is_tool() is False


def test_base_runner_with_meta():
    """
    Scenario:
        Test BaseRunner with PluginMeta.

    Expected:
        BaseRunner can have meta attribute like BasePlugin.
    """

    class MetaRunner(BaseRunner):
        def __init__(self):
            self.meta = PluginMeta(
                name="meta_runner",
                description="A runner with meta",
                type="runner",
                category="quality",
            )

        def build_command(self, target, check_only, *args, **kwargs):
            return ["meta", "command"]

    runner = MetaRunner()
    assert hasattr(runner, "meta")
    assert runner.meta.name == "meta_runner"
    assert runner.meta.description == "A runner with meta"
    assert runner.meta.type == "runner"
    assert runner.meta.category == "quality"


def test_base_runner_build_command_return_type():
    """
    Scenario:
        Test that build_command returns a list of strings.

    Expected:
        build_command returns List[str] as specified in the signature.
    """

    class TypeRunner(BaseRunner):
        def build_command(self, target, check_only, *args, **kwargs):
            return ["type", "test", "command"]

    runner = TypeRunner()
    command = runner.build_command(None, None)

    assert isinstance(command, list)
    assert all(isinstance(item, str) for item in command)


def test_base_runner_build_command_empty_list():
    """
    Scenario:
        Test build_command returning an empty list.

    Expected:
        build_command can return an empty list.
    """

    class EmptyRunner(BaseRunner):
        def build_command(self, target, check_only, *args, **kwargs):
            return []

    runner = EmptyRunner()
    command = runner.build_command(None, None)
    assert command == []


def test_base_runner_build_command_with_unicode():
    """
    Scenario:
        Test build_command with unicode characters.

    Expected:
        build_command can handle unicode characters in command.
    """

    class UnicodeRunner(BaseRunner):
        def build_command(self, target, check_only, *args, **kwargs):
            return ["unicode", "café", "ñöç", "中文"]

    runner = UnicodeRunner()
    command = runner.build_command(None, None)
    assert "café" in command
    assert "ñöç" in command
    assert "中文" in command


# ---------------------------
# Integration tests
# ---------------------------


def test_base_runner_with_register_plugin():
    """
    Scenario:
        Test BaseRunner with register_plugin decorator.

    Expected:
        BaseRunner can be registered as a plugin.
    """
    from tidycode.plugins.registry import registry

    # Clear the registry first
    registry._plugins.clear()

    from tidycode.plugins.registry import register_plugin

    @register_plugin(
        name="registered_runner",
        description="A registered runner",
        type="runner",
        category="quality",
    )
    class RegisteredRunner(BaseRunner):
        def build_command(self, target, check_only, *args, **kwargs):
            return ["registered", "runner"]

    # Check that the runner was registered
    assert "registered_runner" in registry._plugins
    registered_runner = registry._plugins["registered_runner"]
    assert isinstance(registered_runner, RegisteredRunner)

    # Check that it works as a runner
    command = registered_runner.build_command(None, None)
    assert command == ["registered", "runner"]

    # Check that it works as a plugin
    assert registered_runner.meta.name == "registered_runner"
    assert registered_runner.meta.type == "runner"
    assert registered_runner.meta.category == "quality"


def test_base_runner_multiple_implementations():
    """
    Scenario:
        Test multiple BaseRunner implementations.

    Expected:
        Multiple runners can coexist and work independently.
    """

    class QualityRunner(BaseRunner):
        def build_command(self, target, check_only, *args, **kwargs):
            return ["quality", "runner"]

    class AuditRunner(BaseRunner):
        def build_command(self, target, check_only, *args, **kwargs):
            return ["audit", "runner"]

    class ConfigRunner(BaseRunner):
        def build_command(self, target, check_only, *args, **kwargs):
            return ["config", "runner"]

    # Test that all runners work independently
    quality_runner = QualityRunner()
    audit_runner = AuditRunner()
    config_runner = ConfigRunner()

    assert quality_runner.build_command(None, None) == ["quality", "runner"]
    assert audit_runner.build_command(None, None) == ["audit", "runner"]
    assert config_runner.build_command(None, None) == ["config", "runner"]

    # Test that they all return True for is_tool by default
    assert quality_runner.is_tool() is True
    assert audit_runner.is_tool() is True
    assert config_runner.is_tool() is True


def test_base_runner_with_complex_logic():
    """
    Scenario:
        Test BaseRunner with complex build_command logic.

    Expected:
        build_command can implement complex logic based on parameters.
    """

    class ComplexRunner(BaseRunner):
        def build_command(self, target, check_only, *args, **kwargs):
            cmd = ["complex", "runner"]

            # Add target if provided
            if target:
                cmd.extend(["--target", str(target)])

            # Add check flag if check_only is True
            if check_only:
                cmd.append("--check")

            # Add additional arguments
            if args:
                cmd.extend(args)

            # Add keyword arguments
            for key, value in kwargs.items():
                if isinstance(value, bool):
                    if value:
                        cmd.append(f"--{key}")
                else:
                    cmd.extend([f"--{key}", str(value)])

            return cmd

    runner = ComplexRunner()

    # Test with all parameters
    target = Path("/test/path")
    command = runner.build_command(
        target,
        True,
        "extra_arg1",
        "extra_arg2",
        verbose=True,
        debug=False,
        output="/output/path",
    )

    expected = [
        "complex",
        "runner",
        "--target",
        str(target),
        "--check",
        "extra_arg1",
        "extra_arg2",
        "--verbose",
        "--output",
        "/output/path",
    ]

    # The order of kwargs processing might vary, so we check that all expected items are present
    # Note: The actual command might have different length due to kwargs processing order
    for item in expected:
        assert item in command


def test_base_runner_import_consistency():
    """
    Scenario:
        Test that BaseRunner can be imported consistently.

    Expected:
        BaseRunner is properly importable from different paths.
    """
    # Test direct import
    # Test import from runner module
    from tidycode.plugins.runner import BaseRunner as ModuleBaseRunner
    from tidycode.plugins.runner.base_runner import BaseRunner as DirectBaseRunner

    # Test that they are the same
    assert DirectBaseRunner is ModuleBaseRunner
    assert DirectBaseRunner is BaseRunner

    # Test that it's a class
    assert isinstance(BaseRunner, type)
    # BasePlugin is a Protocol, so we can't use issubclass directly
    # Instead, we test that BasePlugin is in the MRO
    assert BasePlugin in BaseRunner.__mro__
