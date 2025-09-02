"""
TidyCode Core PyProject List Sections Tests
"""

from unittest.mock import Mock, patch

from tidycode.core.pyproject.sections.list_sections import list_config_sections


def test_list_config_sections_with_sections():
    """
    Scenario:
        List config sections when sections exist.

    Expected:
        Section summary is printed with display_content=True.
    """
    mock_manager = Mock()
    mock_manager.document = {"tool": {"black": {}}, "project": {"name": "test"}}
    mock_manager.path = "pyproject.toml"

    with patch(
        "tidycode.core.pyproject.sections.list_sections.print_section_summary"
    ) as mock_print_summary:
        result = list_config_sections(manager=mock_manager, interactive=False)

    # Verify section summary was printed
    mock_print_summary.assert_called_once()
    call_args = mock_print_summary.call_args
    assert call_args[1]["section_name"] == "pyproject.toml"
    assert call_args[1]["data"] == {"tool": {"black": {}}, "project": {"name": "test"}}
    assert call_args[1]["display_content"] is True

    # Function should return None
    assert result is None


def test_list_config_sections_with_prefix():
    """
    Scenario:
        List config sections with a prefix.

    Expected:
        Section summary is printed with correct data.
    """
    mock_manager = Mock()
    mock_manager.document = {"tool": {"black": {}}, "project": {"name": "test"}}
    mock_manager.path = "pyproject.toml"

    with patch(
        "tidycode.core.pyproject.sections.list_sections.print_section_summary"
    ) as mock_print_summary:
        list_config_sections(manager=mock_manager, prefix="tool.", interactive=False)

    # Verify section summary was printed
    mock_print_summary.assert_called_once()


def test_list_config_sections_no_sections():
    """
    Scenario:
        List config sections when no sections exist.

    Expected:
        Error message is printed and function returns None.
    """
    mock_manager = Mock()
    mock_manager.document = {}
    mock_manager.path = "pyproject.toml"

    with patch(
        "tidycode.core.pyproject.sections.list_sections.print_error"
    ) as mock_print_error:
        result = list_config_sections(manager=mock_manager, interactive=False)

    # Verify error was printed
    mock_print_error.assert_called_once_with(
        "No sections found in the pyproject.toml file."
    )

    # Function should return None
    assert result is None


def test_list_config_sections_none_document():
    """
    Scenario:
        List config sections when document is None.

    Expected:
        Error message is printed and function returns None.
    """
    mock_manager = Mock()
    mock_manager.document = None
    mock_manager.path = "pyproject.toml"

    with patch(
        "tidycode.core.pyproject.sections.list_sections.print_error"
    ) as mock_print_error:
        result = list_config_sections(manager=mock_manager, interactive=False)

    # Verify error was printed
    mock_print_error.assert_called_once_with(
        "No sections found in the pyproject.toml file."
    )

    # Function should return None
    assert result is None


def test_list_config_sections_complex_structure():
    """
    Scenario:
        List config sections with complex nested structure.

    Expected:
        Section summary is printed with complex data.
    """
    complex_data = {
        "project": {
            "name": "test-project",
            "version": "1.0.0",
            "authors": [{"name": "Test Author"}],
        },
        "tool": {
            "poetry": {
                "dependencies": {"requests": "^2.28.0"},
                "dev-dependencies": {"pytest": "^7.0.0"},
            },
            "black": {"line-length": 88},
            "ruff": {"target-version": "py39"},
        },
        "build-system": {"requires": ["poetry-core"]},
    }

    mock_manager = Mock()
    mock_manager.document = complex_data
    mock_manager.path = "pyproject.toml"

    with patch(
        "tidycode.core.pyproject.sections.list_sections.print_section_summary"
    ) as mock_print_summary:
        list_config_sections(manager=mock_manager, interactive=False)

    # Verify section summary was printed with complex data
    mock_print_summary.assert_called_once()
    call_args = mock_print_summary.call_args
    assert call_args[1]["data"] == complex_data


def test_list_config_sections_manager_integration():
    """
    Scenario:
        Test integration with TomlFileManager.

    Expected:
        Manager document and path are accessed correctly.
    """
    mock_manager = Mock()
    mock_manager.document = {"section": "data"}
    mock_manager.path = "pyproject.toml"

    with patch("tidycode.core.pyproject.sections.list_sections.print_section_summary"):
        list_config_sections(manager=mock_manager, interactive=False)

    # Verify manager properties were accessed
    assert mock_manager.document == {"section": "data"}
    assert str(mock_manager.path) == "pyproject.toml"


def test_list_config_sections_interactive_mode():
    """
    Scenario:
        List config sections in interactive mode.

    Expected:
        Function works the same regardless of interactive mode.
    """
    mock_manager = Mock()
    mock_manager.document = {"section": "data"}
    mock_manager.path = "pyproject.toml"

    with patch(
        "tidycode.core.pyproject.sections.list_sections.print_section_summary"
    ) as mock_print_summary:
        result = list_config_sections(manager=mock_manager, interactive=True)

    # Verify section summary was printed
    mock_print_summary.assert_called_once()

    # Function should return None
    assert result is None
