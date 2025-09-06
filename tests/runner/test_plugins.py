"""
TidyCode Runner Plugins Tests
"""

from pathlib import Path
from unittest import mock

from tidycode.runner.subprocess import run_plugins
from tidycode.runner.types import CommandSpec
from tidycode.plugins.runner.base_runner import BaseRunner


# ---------------------------
# Plugin runner tests
# ---------------------------


def create_mock_runner(name: str, category: str = "quality") -> mock.MagicMock:
    """Create a mock BaseRunner instance."""
    mock_runner = mock.MagicMock(spec=BaseRunner)
    # Create a mock meta object
    mock_meta = mock.MagicMock()
    mock_meta.name = name
    mock_meta.category = category
    mock_runner.meta = mock_meta
    mock_runner.get_command_spec.return_value = CommandSpec(
        command=[name, "--check", "."],
        display_name=name,
        cwd=Path("."),
        is_tool=True
    )
    # Make sure the run method is callable
    mock_runner.run = mock.MagicMock()
    return mock_runner


def test_run_plugins_with_quality_tools():
    """
    Scenario:
        Run plugins with quality tools.

    Expected:
        Quality tools are executed.
    """
    with mock.patch("tidycode.core.pyproject.utils.helpers.load_tidycode_config") as mock_config, mock.patch(
            "tidycode.runner.subprocess.load_plugins_from"
        ) as mock_load, mock.patch(
            "tidycode.plugins.registry.registry.filter"
        ) as mock_filter, mock.patch(
            "tidycode.runner.subprocess.run_multiple_commands"
        ) as mock_run_multiple:
            # Mock configuration
            mock_config.return_value = {
                "target": ".",
                "check_only": False,
                "tools": ["black", "isort"]
            }
            
            # Mock load_plugins_from to avoid importing non-existent modules
            mock_load.return_value = None
            
            # Mock plugin registry
            mock_plugin1 = create_mock_runner("black")
            mock_plugin1.get_command_spec.return_value = CommandSpec(
                command=["black", "--check", "."],
                display_name="black",
                cwd=Path("."),
                is_tool=True
            )
            
            mock_plugin2 = create_mock_runner("isort")
            mock_plugin2.get_command_spec.return_value = CommandSpec(
                command=["isort", "--check-only", "."],
                display_name="isort",
                cwd=Path("."),
                is_tool=True
            )
            
            mock_filter.return_value = [mock_plugin1, mock_plugin2]
            
            # Run plugins
            run_plugins(
                category="quality",
                tools=["black", "isort"],
                dry_run=False,
                live=False,
                verbose=False
            )
            
            # Verify calls
            mock_load.assert_called_once_with("tidycode.modules.quality")
            mock_filter.assert_called_once()
            mock_run_multiple.assert_called_once()


def test_run_plugins_dry_run():
    """
    Scenario:
        Run plugins in dry run mode.

    Expected:
        Tools are executed in dry run mode.
    """
    with mock.patch("tidycode.core.pyproject.utils.helpers.load_tidycode_config") as mock_config, mock.patch(
            "tidycode.runner.subprocess.load_plugins_from"
    ) as mock_load, mock.patch(
        "tidycode.plugins.registry.registry.filter"
    ) as mock_filter, mock.patch(
        "tidycode.plugins.runner.base_runner.BaseRunner.run"
    ) as mock_run:
        # Mock configuration
        mock_config.return_value = {
            "target": ".",
            "check_only": False,
            "tools": ["black"]
        }
        
        # Mock load_plugins_from to avoid importing non-existent modules
        mock_load.return_value = None
        
        # Mock plugin registry
        mock_plugin = create_mock_runner("black")
        mock_filter.return_value = [mock_plugin]
        
        # Run plugins in dry run mode
        run_plugins(
            category="quality",
            tools=["black"],
            dry_run=True,
            live=False,
            verbose=False
        )
        
        # Verify dry run was called
        mock_plugin.run.assert_called_once_with(
            target=Path("."),
            check_only=False,
            dry_run=True,
            live=False,
            verbose=False
        )


def test_run_plugins_tool_not_found():
    """
    Scenario:
        Run plugins with a tool that doesn't exist.

    Expected:
        Warning is printed and tool is skipped.
    """
    with mock.patch("tidycode.core.pyproject.utils.helpers.load_tidycode_config") as mock_config, mock.patch(
            "tidycode.runner.subprocess.load_plugins_from"
    ) as mock_load, mock.patch(
        "tidycode.plugins.registry.registry.filter"
    ) as mock_filter, mock.patch(
        "tidycode.runner.subprocess.print_warning"
    ) as mock_warning:
        # Mock configuration
        mock_config.return_value = {
            "target": ".",
            "check_only": False,
            "tools": ["nonexistent"]
        }
        
        # Mock empty plugin registry
        mock_filter.return_value = []
        
        # Run plugins
        run_plugins(
            category="quality",
            tools=["nonexistent"],
            dry_run=False,
            live=False,
            verbose=False
        )
        
        # Verify warning was printed
        mock_warning.assert_called_once_with("Tool nonexistent not found")


def test_run_plugins_with_custom_path():
    """
    Scenario:
        Run plugins with a custom target path.

    Expected:
        Tools are executed with the custom path.
    """
    with mock.patch("tidycode.core.pyproject.utils.helpers.load_tidycode_config") as mock_config, mock.patch(
            "tidycode.runner.subprocess.load_plugins_from"
    ) as mock_load, mock.patch(
        "tidycode.plugins.registry.registry.filter"
    ) as mock_filter, mock.patch(
        "tidycode.runner.subprocess.run_multiple_commands"
    ) as mock_run_multiple:
        # Mock configuration
        mock_config.return_value = {
            "target": ".",
            "check_only": False,
            "tools": ["black"]
        }
        
        # Mock plugin registry
        mock_plugin = create_mock_runner("black")
        mock_plugin.get_command_spec.return_value = CommandSpec(
            command=["black", "--check", "/custom/path"],
            display_name="black",
            cwd=Path("/custom/path"),
            is_tool=True
        )
        mock_filter.return_value = [mock_plugin]
        
        # Run plugins with custom path
        run_plugins(
            category="quality",
            tools=["black"],
            path=Path("/custom/path"),
            dry_run=False,
            live=False,
            verbose=False
        )
        
        # Verify the plugin was called with custom path
        mock_plugin.get_command_spec.assert_called_once_with(
            target=Path("/custom/path"),
            check_only=False
        )


def test_run_plugins_with_scope_filter():
    """
    Scenario:
        Run plugins with scope filtering.

    Expected:
        Only plugins matching the scope are executed.
    """
    with mock.patch("tidycode.core.pyproject.utils.helpers.load_tidycode_config") as mock_config, mock.patch(
            "tidycode.runner.subprocess.load_plugins_from"
    ) as mock_load, mock.patch(
        "tidycode.plugins.registry.registry.filter"
    ) as mock_filter, mock.patch(
        "tidycode.runner.subprocess.run_multiple_commands"
    ) as mock_run_multiple:
        # Mock configuration
        mock_config.return_value = {
            "target": ".",
            "check_only": False,
            "tools": ["black"]
        }
        
        # Mock plugin registry
        mock_plugin = mock.MagicMock()
        mock_plugin.meta.name = "black"
        mock_plugin.meta.category = "quality"
        mock_plugin.meta.scope = "formatting"
        mock_plugin.get_command_spec.return_value = CommandSpec(
            command=["black", "--check", "."],
            display_name="black",
            cwd=Path("."),
            is_tool=True
        )
        mock_filter.return_value = [mock_plugin]
        
        # Run plugins with scope filter
        run_plugins(
            category="quality",
            scope="formatting",
            tools=["black"],
            dry_run=False,
            live=False,
            verbose=False
        )
        
        # Verify filter was called with scope
        mock_filter.assert_called_once()
        call_args = mock_filter.call_args[1]
        assert call_args["type"] == "runner"
        assert call_args["category"] == "quality"
        assert call_args["scope"] == "formatting"


def test_run_plugins_no_tools_specified():
    """
    Scenario:
        Run plugins without specifying tools.

    Expected:
        Uses tools from configuration.
    """
    with mock.patch("tidycode.core.pyproject.utils.helpers.load_tidycode_config") as mock_config, mock.patch(
            "tidycode.runner.subprocess.load_plugins_from"
    ) as mock_load, mock.patch(
        "tidycode.plugins.registry.registry.filter"
    ) as mock_filter, mock.patch(
        "tidycode.runner.subprocess.run_multiple_commands"
    ) as mock_run_multiple:
        # Mock configuration with tools
        mock_config.return_value = {
            "target": ".",
            "check_only": False,
            "tools": ["black", "isort"]
        }
        
        # Mock plugin registry
        mock_plugin = create_mock_runner("black")
        mock_plugin.get_command_spec.return_value = CommandSpec(
            command=["black", "--check", "."],
            display_name="black",
            cwd=Path("."),
            is_tool=True
        )
        mock_filter.return_value = [mock_plugin]
        
        # Run plugins without specifying tools
        run_plugins(
            category="quality",
            dry_run=False,
            live=False,
            verbose=False
        )
        
        # Verify the plugin was called
        mock_plugin.get_command_spec.assert_called_once()


def test_run_plugins_check_only_mode():
    """
    Scenario:
        Run plugins in check-only mode.

    Expected:
        Tools are executed in check-only mode.
    """
    with mock.patch("tidycode.core.pyproject.utils.helpers.load_tidycode_config") as mock_config, mock.patch(
            "tidycode.runner.subprocess.load_plugins_from"
    ) as mock_load, mock.patch(
        "tidycode.plugins.registry.registry.filter"
    ) as mock_filter, mock.patch(
        "tidycode.runner.subprocess.run_multiple_commands"
    ) as mock_run_multiple:
        # Mock configuration
        mock_config.return_value = {
            "target": ".",
            "check_only": True,
            "tools": ["black"]
        }
        
        # Mock plugin registry
        mock_plugin = create_mock_runner("black")
        mock_plugin.get_command_spec.return_value = CommandSpec(
            command=["black", "--check", "."],
            display_name="black",
            cwd=Path("."),
            is_tool=True
        )
        mock_filter.return_value = [mock_plugin]
        
        # Run plugins in check-only mode
        run_plugins(
            category="quality",
            tools=["black"],
            check_only=True,
            dry_run=False,
            live=False,
            verbose=False
        )
        
        # Verify the plugin was called with check_only=True
        mock_plugin.get_command_spec.assert_called_once_with(
            target=Path("."),
            check_only=True
        )
