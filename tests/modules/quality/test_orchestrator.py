"""
Tests for orchestrator.
"""

import pytest
from pathlib import Path
from unittest import mock

from tidycode.modules.quality.orchestrator import run_quality_tools
from tidycode.runner import SubprocessDisplayMode


class TestRunQualityTools:
    """Test cases for run_quality_tools function."""

    @mock.patch("tidycode.modules.quality.orchestrator.run_multiple_commands")
    @mock.patch("tidycode.modules.quality.orchestrator.registry")
    @mock.patch("tidycode.modules.quality.orchestrator.load_plugins_from")
    @mock.patch("tidycode.modules.quality.orchestrator.load_tidycode_config")
    def test_run_quality_tools_with_default_parameters(
        self,
        mock_load_config,
        mock_load_plugins,
        mock_registry,
        mock_run_commands,
    ):
        """
        Scenario:
            Run quality tools with default parameters.

        Expected:
            Tools are loaded and executed with default settings.
        """
        # Setup mocks
        mock_config = {
            "target": Path("/project"),
            "check_only": False,
            "tools": ["black", "isort"],
        }
        mock_load_config.return_value = mock_config

        # Mock plugin registry
        mock_plugin1 = mock.MagicMock()
        mock_plugin1.meta.name = "black"
        mock_plugin1.build_command.return_value = ["black", "--check"]
        mock_plugin1.is_tool.return_value = True

        mock_plugin2 = mock.MagicMock()
        mock_plugin2.meta.name = "isort"
        mock_plugin2.build_command.return_value = ["isort", "--check-only"]
        mock_plugin2.is_tool.return_value = True

        mock_registry.by_category.return_value = [mock_plugin1, mock_plugin2]

        # Call function
        run_quality_tools()

        # Verify calls
        mock_load_config.assert_called_once()
        mock_load_plugins.assert_called_once_with("tidycode.modules.quality")
        mock_registry.by_category.assert_called_once_with("quality")
        mock_run_commands.assert_called_once()

    @mock.patch("tidycode.modules.quality.orchestrator.run_multiple_commands")
    @mock.patch("tidycode.modules.quality.orchestrator.registry")
    @mock.patch("tidycode.modules.quality.orchestrator.load_plugins_from")
    @mock.patch("tidycode.modules.quality.orchestrator.load_tidycode_config")
    def test_run_quality_tools_with_specific_tools(
        self,
        mock_load_config,
        mock_load_plugins,
        mock_registry,
        mock_run_commands,
    ):
        """
        Scenario:
            Run quality tools with specific tools list.

        Expected:
            Only specified tools are executed.
        """
        # Setup mocks
        mock_config = {
            "target": Path("/project"),
            "check_only": False,
            "tools": ["black", "isort", "mypy"],
        }
        mock_load_config.return_value = mock_config

        # Mock plugin registry
        mock_plugin1 = mock.MagicMock()
        mock_plugin1.meta.name = "black"
        mock_plugin1.build_command.return_value = ["black", "--check"]
        mock_plugin1.is_tool.return_value = True

        mock_plugin2 = mock.MagicMock()
        mock_plugin2.meta.name = "isort"
        mock_plugin2.build_command.return_value = ["isort", "--check-only"]
        mock_plugin2.is_tool.return_value = True

        mock_plugin3 = mock.MagicMock()
        mock_plugin3.meta.name = "mypy"
        mock_plugin3.build_command.return_value = ["mypy"]
        mock_plugin3.is_tool.return_value = True

        mock_registry.by_category.return_value = [mock_plugin1, mock_plugin2, mock_plugin3]

        # Call function with specific tools
        run_quality_tools(tools=["black", "mypy"])

        # Verify calls
        mock_load_config.assert_called_once()
        mock_load_plugins.assert_called_once_with("tidycode.modules.quality")
        mock_registry.by_category.assert_called_once_with("quality")
        mock_run_commands.assert_called_once()

    @mock.patch("tidycode.modules.quality.orchestrator.run_multiple_commands")
    @mock.patch("tidycode.modules.quality.orchestrator.registry")
    @mock.patch("tidycode.modules.quality.orchestrator.load_plugins_from")
    @mock.patch("tidycode.modules.quality.orchestrator.load_tidycode_config")
    def test_run_quality_tools_with_check_only(
        self,
        mock_load_config,
        mock_load_plugins,
        mock_registry,
        mock_run_commands,
    ):
        """
        Scenario:
            Run quality tools with check_only=True.

        Expected:
            Tools are executed with check_only flag.
        """
        # Setup mocks
        mock_config = {
            "target": Path("/project"),
            "check_only": False,
            "tools": ["black"],
        }
        mock_load_config.return_value = mock_config

        # Mock plugin registry
        mock_plugin = mock.MagicMock()
        mock_plugin.meta.name = "black"
        mock_plugin.build_command.return_value = ["black", "--check"]
        mock_plugin.is_tool.return_value = True

        mock_registry.by_category.return_value = [mock_plugin]

        # Call function with check_only=True
        run_quality_tools(check_only=True)

        # Verify that build_command was called with check_only from config (False)
        mock_plugin.build_command.assert_called_with(Path("/project"), False)

    @mock.patch("tidycode.modules.quality.orchestrator.run_multiple_commands")
    @mock.patch("tidycode.modules.quality.orchestrator.registry")
    @mock.patch("tidycode.modules.quality.orchestrator.load_plugins_from")
    @mock.patch("tidycode.modules.quality.orchestrator.load_tidycode_config")
    def test_run_quality_tools_with_live_mode(
        self,
        mock_load_config,
        mock_load_plugins,
        mock_registry,
        mock_run_commands,
    ):
        """
        Scenario:
            Run quality tools with live mode.

        Expected:
            Tools are executed in live mode.
        """
        # Setup mocks
        mock_config = {
            "target": Path("/project"),
            "check_only": False,
            "tools": ["black"],
        }
        mock_load_config.return_value = mock_config

        # Mock plugin registry
        mock_plugin = mock.MagicMock()
        mock_plugin.meta.name = "black"
        mock_plugin.build_command.return_value = ["black"]
        mock_plugin.is_tool.return_value = True

        mock_registry.by_category.return_value = [mock_plugin]

        # Call function with live=True
        run_quality_tools(live=True)

        # Verify run_multiple_commands was called with live=True
        call_args = mock_run_commands.call_args
        assert call_args[1]["live"] is True
        assert call_args[1]["summary_display_mode"] == SubprocessDisplayMode.TABLE_MINIMAL

    @mock.patch("tidycode.modules.quality.orchestrator.run_multiple_commands")
    @mock.patch("tidycode.modules.quality.orchestrator.registry")
    @mock.patch("tidycode.modules.quality.orchestrator.load_plugins_from")
    @mock.patch("tidycode.modules.quality.orchestrator.load_tidycode_config")
    def test_run_quality_tools_with_verbose_mode(
        self,
        mock_load_config,
        mock_load_plugins,
        mock_registry,
        mock_run_commands,
    ):
        """
        Scenario:
            Run quality tools with verbose mode.

        Expected:
            Tools are executed with verbose output.
        """
        # Setup mocks
        mock_config = {
            "target": Path("/project"),
            "check_only": False,
            "tools": ["black"],
        }
        mock_load_config.return_value = mock_config

        # Mock plugin registry
        mock_plugin = mock.MagicMock()
        mock_plugin.meta.name = "black"
        mock_plugin.build_command.return_value = ["black"]
        mock_plugin.is_tool.return_value = True

        mock_registry.by_category.return_value = [mock_plugin]

        # Call function with verbose=True
        run_quality_tools(verbose=True)

        # Verify run_multiple_commands was called with verbose=True
        call_args = mock_run_commands.call_args
        assert call_args[1]["verbose"] is True

    @mock.patch("tidycode.modules.quality.orchestrator.run_multiple_commands")
    @mock.patch("tidycode.modules.quality.orchestrator.registry")
    @mock.patch("tidycode.modules.quality.orchestrator.load_plugins_from")
    @mock.patch("tidycode.modules.quality.orchestrator.load_tidycode_config")
    def test_run_quality_tools_with_custom_summary_display_mode(
        self,
        mock_load_config,
        mock_load_plugins,
        mock_registry,
        mock_run_commands,
    ):
        """
        Scenario:
            Run quality tools with custom summary display mode.

        Expected:
            Tools are executed with custom display mode.
        """
        # Setup mocks
        mock_config = {
            "target": Path("/project"),
            "check_only": False,
            "tools": ["black"],
        }
        mock_load_config.return_value = mock_config

        # Mock plugin registry
        mock_plugin = mock.MagicMock()
        mock_plugin.meta.name = "black"
        mock_plugin.build_command.return_value = ["black"]
        mock_plugin.is_tool.return_value = True

        mock_registry.by_category.return_value = [mock_plugin]

        # Call function with custom summary_display_mode
        run_quality_tools(summary_display_mode=SubprocessDisplayMode.TABLE_FULL)

        # Verify run_multiple_commands was called with custom display mode
        call_args = mock_run_commands.call_args
        assert call_args[1]["summary_display_mode"] == SubprocessDisplayMode.TABLE_FULL

    @mock.patch("tidycode.modules.quality.orchestrator.print_warning")
    @mock.patch("tidycode.modules.quality.orchestrator.run_multiple_commands")
    @mock.patch("tidycode.modules.quality.orchestrator.registry")
    @mock.patch("tidycode.modules.quality.orchestrator.load_plugins_from")
    @mock.patch("tidycode.modules.quality.orchestrator.load_tidycode_config")
    def test_run_quality_tools_with_unknown_tool(
        self,
        mock_load_config,
        mock_load_plugins,
        mock_registry,
        mock_run_commands,
        mock_print_warning,
    ):
        """
        Scenario:
            Run quality tools with unknown tool name.

        Expected:
            Warning is printed and unknown tool is skipped.
        """
        # Setup mocks
        mock_config = {
            "target": Path("/project"),
            "check_only": False,
            "tools": ["black", "unknown_tool"],
        }
        mock_load_config.return_value = mock_config

        # Mock plugin registry
        mock_plugin = mock.MagicMock()
        mock_plugin.meta.name = "black"
        mock_plugin.build_command.return_value = ["black"]
        mock_plugin.is_tool.return_value = True

        mock_registry.by_category.return_value = [mock_plugin]

        # Call function
        run_quality_tools()

        # Verify warning was printed
        mock_print_warning.assert_called_once_with("Tool unknown_tool not found")

        # Verify only known tool was executed
        call_args = mock_run_commands.call_args
        commands = call_args[1]["commands"]
        assert len(commands) == 1
        assert commands[0].tool_name == "black"

    @mock.patch("tidycode.modules.quality.orchestrator.run_multiple_commands")
    @mock.patch("tidycode.modules.quality.orchestrator.registry")
    @mock.patch("tidycode.modules.quality.orchestrator.load_plugins_from")
    @mock.patch("tidycode.modules.quality.orchestrator.load_tidycode_config")
    def test_run_quality_tools_with_plugin_without_build_command(
        self,
        mock_load_config,
        mock_load_plugins,
        mock_registry,
        mock_run_commands,
    ):
        """
        Scenario:
            Run quality tools with plugin that doesn't have build_command method.

        Expected:
            Plugin is skipped.
        """
        # Setup mocks
        mock_config = {
            "target": Path("/project"),
            "check_only": False,
            "tools": ["black"],
        }
        mock_load_config.return_value = mock_config

        # Mock plugin registry with plugin without build_command
        mock_plugin = mock.MagicMock()
        mock_plugin.meta.name = "black"
        # Remove build_command attribute
        del mock_plugin.build_command
        mock_plugin.is_tool.return_value = True

        mock_registry.by_category.return_value = [mock_plugin]

        # Call function
        run_quality_tools()

        # Verify no commands were executed
        call_args = mock_run_commands.call_args
        commands = call_args[1]["commands"]
        assert len(commands) == 0

    @mock.patch("tidycode.modules.quality.orchestrator.run_multiple_commands")
    @mock.patch("tidycode.modules.quality.orchestrator.registry")
    @mock.patch("tidycode.modules.quality.orchestrator.load_plugins_from")
    @mock.patch("tidycode.modules.quality.orchestrator.load_tidycode_config")
    def test_run_quality_tools_with_plugin_without_is_tool(
        self,
        mock_load_config,
        mock_load_plugins,
        mock_registry,
        mock_run_commands,
    ):
        """
        Scenario:
            Run quality tools with plugin that doesn't have is_tool method.

        Expected:
            Plugin is skipped.
        """
        # Setup mocks
        mock_config = {
            "target": Path("/project"),
            "check_only": False,
            "tools": ["black"],
        }
        mock_load_config.return_value = mock_config

        # Mock plugin registry with plugin without is_tool
        mock_plugin = mock.MagicMock()
        mock_plugin.meta.name = "black"
        mock_plugin.build_command.return_value = ["black"]
        # Remove is_tool attribute
        del mock_plugin.is_tool

        mock_registry.by_category.return_value = [mock_plugin]

        # Call function
        run_quality_tools()

        # Verify no commands were executed
        call_args = mock_run_commands.call_args
        commands = call_args[1]["commands"]
        assert len(commands) == 0

    @mock.patch("tidycode.modules.quality.orchestrator.run_multiple_commands")
    @mock.patch("tidycode.modules.quality.orchestrator.registry")
    @mock.patch("tidycode.modules.quality.orchestrator.load_plugins_from")
    @mock.patch("tidycode.modules.quality.orchestrator.load_tidycode_config")
    def test_run_quality_tools_with_empty_tools_list(
        self,
        mock_load_config,
        mock_load_plugins,
        mock_registry,
        mock_run_commands,
    ):
        """
        Scenario:
            Run quality tools with empty tools list.

        Expected:
            No commands are executed.
        """
        # Setup mocks
        mock_config = {
            "target": Path("/project"),
            "check_only": False,
            "tools": [],
        }
        mock_load_config.return_value = mock_config

        # Mock plugin registry
        mock_registry.by_category.return_value = []

        # Call function
        run_quality_tools()

        # Verify no commands were executed
        call_args = mock_run_commands.call_args
        commands = call_args[1]["commands"]
        assert len(commands) == 0

    @mock.patch("tidycode.modules.quality.orchestrator.run_multiple_commands")
    @mock.patch("tidycode.modules.quality.orchestrator.registry")
    @mock.patch("tidycode.modules.quality.orchestrator.load_plugins_from")
    @mock.patch("tidycode.modules.quality.orchestrator.load_tidycode_config")
    def test_run_quality_tools_with_config_override(
        self,
        mock_load_config,
        mock_load_plugins,
        mock_registry,
        mock_run_commands,
    ):
        """
        Scenario:
            Run quality tools with config values overriding function parameters.

        Expected:
            Config values take precedence over function parameters.
        """
        # Setup mocks
        mock_config = {
            "target": Path("/config/project"),
            "check_only": True,
            "tools": ["black", "isort"],
        }
        mock_load_config.return_value = mock_config

        # Mock plugin registry
        mock_plugin1 = mock.MagicMock()
        mock_plugin1.meta.name = "black"
        mock_plugin1.build_command.return_value = ["black", "--check"]
        mock_plugin1.is_tool.return_value = True

        mock_plugin2 = mock.MagicMock()
        mock_plugin2.meta.name = "isort"
        mock_plugin2.build_command.return_value = ["isort", "--check-only"]
        mock_plugin2.is_tool.return_value = True

        mock_registry.by_category.return_value = [mock_plugin1, mock_plugin2]

        # Call function with different parameters
        run_quality_tools(
            tools=None,  # This should use config tools
            check_only=False,  # This should be overridden by config
        )

        # Verify that config values were used
        # Note: tools=None uses config tools=["black", "isort"]
        # So only black and isort should be called
        mock_plugin1.build_command.assert_called_with(Path("/config/project"), True)
        mock_plugin2.build_command.assert_called_with(Path("/config/project"), True)

    @mock.patch("tidycode.modules.quality.orchestrator.run_multiple_commands")
    @mock.patch("tidycode.modules.quality.orchestrator.registry")
    @mock.patch("tidycode.modules.quality.orchestrator.load_plugins_from")
    @mock.patch("tidycode.modules.quality.orchestrator.load_tidycode_config")
    def test_run_quality_tools_integration(
        self,
        mock_load_config,
        mock_load_plugins,
        mock_registry,
        mock_run_commands,
    ):
        """
        Scenario:
            Run quality tools with full integration test.

        Expected:
            All components work together correctly.
        """
        # Setup mocks
        mock_config = {
            "target": Path("/project"),
            "check_only": False,
            "tools": ["black", "isort", "mypy", "ruff"],
        }
        mock_load_config.return_value = mock_config

        # Mock plugin registry
        mock_plugins = []
        for tool_name in ["black", "isort", "mypy", "ruff"]:
            mock_plugin = mock.MagicMock()
            mock_plugin.meta.name = tool_name
            mock_plugin.build_command.return_value = [tool_name]
            mock_plugin.is_tool.return_value = True
            mock_plugins.append(mock_plugin)

        mock_registry.by_category.return_value = mock_plugins

        # Call function
        run_quality_tools(
            live=True,
            verbose=False,
            summary_display_mode=SubprocessDisplayMode.TABLE_FULL,
        )

        # Verify all components were called correctly
        mock_load_config.assert_called_once()
        mock_load_plugins.assert_called_once_with("tidycode.modules.quality")
        mock_registry.by_category.assert_called_once_with("quality")

        # Verify run_multiple_commands was called with correct parameters
        call_args = mock_run_commands.call_args
        assert call_args[1]["live"] is True
        assert call_args[1]["verbose"] is False
        assert call_args[1]["summary_display_mode"] == SubprocessDisplayMode.TABLE_FULL

        # Verify all tools were included in commands
        commands = call_args[1]["commands"]
        assert len(commands) == 4
        tool_names = [cmd.tool_name for cmd in commands]
        assert set(tool_names) == {"black", "isort", "mypy", "ruff"}
