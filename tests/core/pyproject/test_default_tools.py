"""
TidyCode Core PyProject Default Tools Tests
"""

from unittest.mock import Mock, patch

from tidycode.core.pyproject.default_tools import (
    DEFAULT_TOOLS_CONFIG,
    load_default_tools,
)
from tidycode.plugins.config import DictPlugin


def test_default_tools_config_structure():
    """
    Scenario:
        Test the structure of DEFAULT_TOOLS_CONFIG.

    Expected:
        DEFAULT_TOOLS_CONFIG contains the expected tools with correct structure.
    """
    # Check that expected tools exist
    assert "tidycode" in DEFAULT_TOOLS_CONFIG
    assert "black" in DEFAULT_TOOLS_CONFIG
    assert "ruff" in DEFAULT_TOOLS_CONFIG
    assert "isort" in DEFAULT_TOOLS_CONFIG

    # Check tidycode tool structure
    tidycode_tool = DEFAULT_TOOLS_CONFIG["tidycode"]
    assert "name" in tidycode_tool
    assert "description" in tidycode_tool
    assert "config" in tidycode_tool
    assert tidycode_tool["name"] == "TidyCode"
    assert (
        tidycode_tool["description"]
        == "A tool to keep your Python projects clean and secure (format, lint, test, etc.)"
    )

    # Check black tool structure
    black_tool = DEFAULT_TOOLS_CONFIG["black"]
    assert "name" in black_tool
    assert "description" in black_tool
    assert "config" in black_tool
    assert black_tool["name"] == "Black"
    assert black_tool["description"] == "The uncompromising Python code formatter"

    # Check ruff tool structure
    ruff_tool = DEFAULT_TOOLS_CONFIG["ruff"]
    assert "name" in ruff_tool
    assert "description" in ruff_tool
    assert "config" in ruff_tool
    assert ruff_tool["name"] == "Ruff"
    assert (
        ruff_tool["description"] == "A fast Python linter, compatible with Flake8 rules"
    )

    # Check isort tool structure
    isort_tool = DEFAULT_TOOLS_CONFIG["isort"]
    assert "name" in isort_tool
    assert "description" in isort_tool
    assert "config" in isort_tool
    assert isort_tool["name"] == "isort"
    assert isort_tool["description"] == "Python utility for sorting imports"


def test_tidycode_tool_config():
    """
    Scenario:
        Test the tidycode tool configuration.

    Expected:
        TidyCode tool has the expected configuration values.
    """
    tidycode_config = DEFAULT_TOOLS_CONFIG["tidycode"]["config"]

    assert tidycode_config["target"] == "."
    assert tidycode_config["check-only"] is False
    assert tidycode_config["verbose"] is False
    assert "tools" in tidycode_config


def test_black_tool_config():
    """
    Scenario:
        Test the black tool configuration.

    Expected:
        Black tool has the expected configuration values.
    """
    black_config = DEFAULT_TOOLS_CONFIG["black"]["config"]

    assert black_config["line-length"] == 88
    assert black_config["target-version"] == ["py310"]
    assert black_config["skip-string-normalization"] is False
    assert black_config["preview"] is True


def test_ruff_tool_config():
    """
    Scenario:
        Test the ruff tool configuration.

    Expected:
        Ruff tool has the expected configuration values.
    """
    ruff_config = DEFAULT_TOOLS_CONFIG["ruff"]["config"]

    assert ruff_config["line-length"] == 88
    assert ruff_config["target-version"] == "py310"

    # Check exclude list
    assert "migrations" in ruff_config["exclude"]
    assert ".venv" in ruff_config["exclude"]
    assert ".git" in ruff_config["exclude"]
    assert "build" in ruff_config["exclude"]

    # Check lint configuration
    assert ruff_config["lint"]["select"] == ["E", "F", "W", "I"]
    assert ruff_config["lint"]["ignore"] == ["E501"]
    assert ruff_config["lint"]["fixable"] == ["ALL"]

    # Check format configuration
    assert ruff_config["format"]["quote-style"] == "double"
    assert ruff_config["format"]["skip-magic-trailing-comma"] is False
    assert ruff_config["format"]["line-ending"] == "auto"


def test_isort_tool_config():
    """
    Scenario:
        Test the isort tool configuration.

    Expected:
        Isort tool has the expected configuration values.
    """
    isort_config = DEFAULT_TOOLS_CONFIG["isort"]["config"]

    assert isort_config["profile"] == "black"
    assert isort_config["line_length"] == 88


def test_load_default_tools():
    """
    Scenario:
        Test loading default tools into a pyproject.toml file.

    Expected:
        All default tools are loaded using add_config_section.
    """
    mock_manager = Mock()

    with patch(
        "tidycode.core.pyproject.default_tools.add_config_section"
    ) as mock_add_section:
        with patch("tidycode.core.pyproject.default_tools.print_info"):
            load_default_tools(mock_manager)

    # Verify that add_config_section was called for each tool
    assert mock_add_section.call_count == 4

    # Verify calls for each tool
    calls = mock_add_section.call_args_list

    # Check tidycode tool call
    tidycode_call = calls[0]
    assert tidycode_call[1]["section_name"] == "tidycode"
    assert tidycode_call[1]["prefix"] == "tool."
    assert tidycode_call[1]["display_label"] == "tool"
    assert tidycode_call[1]["interactive"] is False
    assert isinstance(tidycode_call[1]["plugin"], DictPlugin)
    assert tidycode_call[1]["plugin"].get_name() == "tidycode"

    # Check black tool call
    black_call = calls[1]
    assert black_call[1]["section_name"] == "black"
    assert black_call[1]["prefix"] == "tool."
    assert black_call[1]["display_label"] == "tool"
    assert black_call[1]["interactive"] is False
    assert isinstance(black_call[1]["plugin"], DictPlugin)
    assert black_call[1]["plugin"].get_name() == "black"

    # Check ruff tool call
    ruff_call = calls[2]
    assert ruff_call[1]["section_name"] == "ruff"
    assert ruff_call[1]["prefix"] == "tool."
    assert ruff_call[1]["display_label"] == "tool"
    assert ruff_call[1]["interactive"] is False
    assert isinstance(ruff_call[1]["plugin"], DictPlugin)
    assert ruff_call[1]["plugin"].get_name() == "ruff"

    # Check isort tool call
    isort_call = calls[3]
    assert isort_call[1]["section_name"] == "isort"
    assert isort_call[1]["prefix"] == "tool."
    assert isort_call[1]["display_label"] == "tool"
    assert isort_call[1]["interactive"] is False
    assert isinstance(isort_call[1]["plugin"], DictPlugin)
    assert isort_call[1]["plugin"].get_name() == "isort"


def test_load_default_tools_info_messages():
    """
    Scenario:
        Test that info messages are printed for each tool.

    Expected:
        Info messages are printed for each tool being loaded.
    """
    mock_manager = Mock()

    with patch("tidycode.core.pyproject.default_tools.add_config_section"):
        with patch(
            "tidycode.core.pyproject.default_tools.print_info"
        ) as mock_print_info:
            load_default_tools(mock_manager)

    # Verify that print_info was called for each tool
    assert mock_print_info.call_count == 4

    # Check the messages
    calls = mock_print_info.call_args_list
    assert "Loading default tool: tidycode" in calls[0][0][0]
    assert "Loading default tool: black" in calls[1][0][0]
    assert "Loading default tool: ruff" in calls[2][0][0]
    assert "Loading default tool: isort" in calls[3][0][0]


def test_load_default_tools_plugin_creation():
    """
    Scenario:
        Test that DictPlugin instances are created correctly.

    Expected:
        DictPlugin instances are created with correct names and configs.
    """
    mock_manager = Mock()

    with patch(
        "tidycode.core.pyproject.default_tools.add_config_section"
    ) as mock_add_section:
        load_default_tools(mock_manager)

    # Verify that plugins were created with correct data
    calls = mock_add_section.call_args_list

    # Check tidycode plugin
    tidycode_plugin = calls[0][1]["plugin"]
    assert tidycode_plugin.get_name() == "tidycode"
    tidycode_config = tidycode_plugin.get_data()
    assert tidycode_config["target"] == "."
    assert tidycode_config["check-only"] is False
    assert tidycode_config["verbose"] is False

    # Check black plugin
    black_plugin = calls[1][1]["plugin"]
    assert black_plugin.get_name() == "black"
    black_config = black_plugin.get_data()
    assert black_config["line-length"] == 88
    assert black_config["target-version"] == ["py310"]

    # Check ruff plugin
    ruff_plugin = calls[2][1]["plugin"]
    assert ruff_plugin.get_name() == "ruff"
    ruff_config = ruff_plugin.get_data()
    assert ruff_config["line-length"] == 88
    assert ruff_config["target-version"] == "py310"

    # Check isort plugin
    isort_plugin = calls[3][1]["plugin"]
    assert isort_plugin.get_name() == "isort"
    isort_config = isort_plugin.get_data()
    assert isort_config["profile"] == "black"
    assert isort_config["line_length"] == 88


def test_default_tools_config_immutability():
    """
    Scenario:
        Test that DEFAULT_TOOLS_CONFIG is not modified during loading.

    Expected:
        DEFAULT_TOOLS_CONFIG remains unchanged after loading tools.
    """
    mock_manager = Mock()

    # Store original config
    original_tidycode_config = DEFAULT_TOOLS_CONFIG["tidycode"]["config"].copy()
    original_black_config = DEFAULT_TOOLS_CONFIG["black"]["config"].copy()
    original_ruff_config = DEFAULT_TOOLS_CONFIG["ruff"]["config"].copy()
    original_isort_config = DEFAULT_TOOLS_CONFIG["isort"]["config"].copy()

    with patch("tidycode.core.pyproject.default_tools.add_config_section"):
        load_default_tools(mock_manager)

    # Verify configs were not modified
    assert DEFAULT_TOOLS_CONFIG["tidycode"]["config"] == original_tidycode_config
    assert DEFAULT_TOOLS_CONFIG["black"]["config"] == original_black_config
    assert DEFAULT_TOOLS_CONFIG["ruff"]["config"] == original_ruff_config
    assert DEFAULT_TOOLS_CONFIG["isort"]["config"] == original_isort_config


def test_default_tools_manager_integration():
    """
    Scenario:
        Test integration with TomlFileManager.

    Expected:
        Manager is passed correctly to add_config_section.
    """
    mock_manager = Mock()

    with patch(
        "tidycode.core.pyproject.default_tools.add_config_section"
    ) as mock_add_section:
        load_default_tools(mock_manager)

    # Verify that manager was passed to all calls
    calls = mock_add_section.call_args_list
    for call in calls:
        assert call[1]["manager"] == mock_manager
