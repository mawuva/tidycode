"""
TidyCode Core PyProject Add Section Tests
"""

from unittest.mock import Mock, patch

from tidycode.core.pyproject.sections.add_section import add_config_section


class MockConfigProvider:
    """Mock config provider for testing."""

    def __init__(self, name: str, data: dict):
        self.name = name
        self.data = data

    def get_name(self) -> str:
        return self.name

    def get_data(self) -> dict:
        return self.data


def test_add_config_section_with_plugin_non_interactive():
    """
    Scenario:
        Add a config section using a plugin in non-interactive mode.

    Expected:
        Section is created with plugin data, no prompts shown.
    """
    mock_manager = Mock()
    mock_manager.get_section.return_value = None
    mock_manager.set_section = Mock()
    mock_manager.save = Mock()

    plugin = MockConfigProvider("test-tool", {"version": "1.0.0"})

    with patch(
        "tidycode.core.pyproject.sections.add_section.print_success"
    ) as mock_print_success:
        add_config_section(
            manager=mock_manager, section_name=None, plugin=plugin, interactive=False
        )

    # Verify plugin name was used
    mock_manager.set_section.assert_called_once()
    call_args = mock_manager.set_section.call_args
    assert call_args[1]["dot_key"] == "test-tool"

    # Verify success message was printed
    mock_print_success.assert_called_once()
    mock_manager.save.assert_called_once()


def test_add_config_section_with_initial_data_non_interactive():
    """
    Scenario:
        Add a config section with predefined data in non-interactive mode.

    Expected:
        Section is created with initial data, no prompts shown.
    """
    mock_manager = Mock()
    mock_manager.get_section.return_value = None
    mock_manager.set_section = Mock()
    mock_manager.save = Mock()

    initial_data = {"name": "test-project", "version": "1.0.0"}

    with patch(
        "tidycode.core.pyproject.sections.add_section.print_success"
    ) as mock_print_success:
        add_config_section(
            manager=mock_manager,
            section_name="test-section",
            initial_data=initial_data,
            interactive=False,
        )

    # Verify section was created with initial data
    mock_manager.set_section.assert_called_once()
    call_args = mock_manager.set_section.call_args
    assert call_args[1]["dot_key"] == "test-section"

    # Verify success message was printed
    mock_print_success.assert_called_once()
    mock_manager.save.assert_called_once()


def test_add_config_section_with_prefix():
    """
    Scenario:
        Add a config section with a prefix.

    Expected:
        Section is created with the correct full name including prefix.
    """
    mock_manager = Mock()
    mock_manager.get_section.return_value = None
    mock_manager.set_section = Mock()
    mock_manager.save = Mock()

    initial_data = {"line-length": 88, "target-version": ["py37"]}

    with patch("tidycode.core.pyproject.sections.add_section.print_success"):
        add_config_section(
            manager=mock_manager,
            section_name="black",
            prefix="tool.",
            initial_data=initial_data,
            interactive=False,
        )

    # Verify section was created with prefix
    mock_manager.set_section.assert_called_once()
    call_args = mock_manager.set_section.call_args
    assert call_args[1]["dot_key"] == "tool.black"


def test_add_config_section_existing_section_overwrite():
    """
    Scenario:
        Add a config section that already exists, with overwrite choice.

    Expected:
        Existing section is overwritten with new data.
    """
    existing_data = {"old_key": "old_value"}
    mock_manager = Mock()
    mock_manager.get_section.return_value = existing_data
    mock_manager.set_section = Mock()
    mock_manager.save = Mock()

    initial_data = {"new_key": "new_value"}

    with patch("tidycode.core.pyproject.sections.add_section.print_success"):
        add_config_section(
            manager=mock_manager,
            section_name="test-section",
            initial_data=initial_data,
            interactive=False,
        )

    # Verify section was updated (merged existing + new)
    mock_manager.set_section.assert_called_once()
    call_args = mock_manager.set_section.call_args
    assert call_args[1]["dot_key"] == "test-section"

    # Check that set_section was called with correct parameters
    assert "data" in call_args[1]

    # Verify data was merged (check that it's a dict)
    data_arg = call_args[1]["data"]  # Named argument
    assert isinstance(data_arg, dict)
    assert "new_key" in data_arg


def test_add_config_section_existing_section_with_subsections():
    """
    Scenario:
        Add a config section that already exists and has subsections.

    Expected:
        Section is handled appropriately even with subsections.
    """
    existing_data = {"main_key": "main_value", "subsection": {"nested": "value"}}
    mock_manager = Mock()
    mock_manager.get_section.return_value = existing_data
    mock_manager.set_section = Mock()
    mock_manager.save = Mock()

    initial_data = {"new_key": "new_value"}

    with patch("tidycode.core.pyproject.sections.add_section.print_success"):
        add_config_section(
            manager=mock_manager,
            section_name="test-section",
            initial_data=initial_data,
            interactive=False,
        )

    # Verify section was updated
    mock_manager.set_section.assert_called_once()
    mock_manager.save.assert_called_once()


def test_add_config_section_empty_section_name():
    """
    Scenario:
        Try to add a config section with empty name.

    Expected:
        Function returns early with error message.
    """
    mock_manager = Mock()

    with patch(
        "tidycode.core.pyproject.sections.add_section.ask_text"
    ) as mock_ask_text:
        with patch(
            "tidycode.core.pyproject.sections.add_section.print_error"
        ) as mock_print_error:
            # Mock empty section name
            mock_ask_text.return_value = ""

            result = add_config_section(
                manager=mock_manager, section_name="", interactive=True
            )

    # Verify error message was printed
    mock_print_error.assert_called_once()
    # Verify function returned None
    assert result is None


def test_add_config_section_no_data_collected():
    """
    Scenario:
        Add a config section but no data is collected.

    Expected:
        Function returns early with warning message.
    """
    mock_manager = Mock()
    mock_manager.get_section.return_value = None

    # Mock collect_section_data to return None
    with patch(
        "tidycode.core.pyproject.sections.add_section.collect_section_data"
    ) as mock_collect:
        mock_collect.return_value = None

        with patch(
            "tidycode.core.pyproject.sections.add_section.print_warning"
        ) as mock_warning:
            result = add_config_section(
                manager=mock_manager, section_name="test-section", interactive=False
            )

    # Verify warning was printed and function returned early
    mock_warning.assert_called_once()
    assert result is None


def test_add_config_section_with_table_trivia():
    """
    Scenario:
        Add a config section and ensure proper line breaks.

    Expected:
        Table trivia is set for proper formatting.
    """
    mock_manager = Mock()
    mock_manager.set_section = Mock()
    mock_manager.save = Mock()

    # Mock the section object to be a Table
    mock_table = Mock()
    mock_table.trivia = Mock()
    mock_table.trivia.trail = ""
    # Mock the keys method to return an empty list
    mock_table.keys.return_value = []
    # Mock the table to behave like a dict for unpacking
    mock_table.__iter__ = lambda self: iter([])

    # Configure get_section to return None first (for existing check) and mock_table second (for trivia setting)
    get_section_call_count = 0

    def mock_get_section_side_effect(full_name):
        nonlocal get_section_call_count
        get_section_call_count += 1
        if get_section_call_count == 1:
            # First call: check if section exists
            return None
        else:
            # Second call: get section for trivia setting
            return mock_table

    mock_manager.get_section.side_effect = mock_get_section_side_effect

    initial_data = {"key": "value"}

    with patch("tidycode.core.pyproject.sections.add_section.print_success"):
        with patch(
            "tidycode.core.pyproject.sections.add_section.isinstance"
        ) as mock_isinstance:
            # Mock isinstance to return True for Table check
            mock_isinstance.return_value = True

            add_config_section(
                manager=mock_manager,
                section_name="test-section",
                initial_data=initial_data,
                interactive=False,
            )

    # Verify set_section was called
    mock_manager.set_section.assert_called_once()

    # Verify table trivia was set
    assert mock_table.trivia.trail == "\n"
    mock_manager.save.assert_called_once()


def test_add_config_section_changelog_display():
    """
    Scenario:
        Add a config section and verify changelog display.

    Expected:
        Changelog is displayed appropriately based on interactive mode.
    """
    mock_manager = Mock()
    mock_manager.get_section.return_value = None
    mock_manager.set_section = Mock()
    mock_manager.save = Mock()

    initial_data = {"key": "value"}

    # Test non-interactive mode
    with patch(
        "tidycode.core.pyproject.sections.add_section.changelog"
    ) as mock_changelog:
        with patch("tidycode.core.pyproject.sections.add_section.print_success"):
            add_config_section(
                manager=mock_manager,
                section_name="test-section",
                initial_data=initial_data,
                interactive=False,
            )

    # Verify changelog was displayed in non-interactive mode
    mock_changelog.display.assert_called_once_with(silent=False, show_values=False)


def test_add_config_section_display_label():
    """
    Scenario:
        Add a config section with custom display label.

    Expected:
        Display label is used in messages and prompts.
    """
    mock_manager = Mock()
    mock_manager.get_section.return_value = None
    mock_manager.set_section = Mock()
    mock_manager.save = Mock()

    initial_data = {"key": "value"}

    with patch(
        "tidycode.core.pyproject.sections.add_section.print_success"
    ) as mock_print_success:
        add_config_section(
            manager=mock_manager,
            section_name="test-section",
            display_label="configuration block",
            initial_data=initial_data,
            interactive=False,
        )

    # Verify success message was printed
    mock_print_success.assert_called_once()


def test_add_config_section_manager_integration():
    """
    Scenario:
        Test integration with TomlFileManager methods.

    Expected:
        All manager methods are called correctly.
    """
    mock_manager = Mock()
    mock_manager.get_section.return_value = None
    mock_manager.set_section = Mock()
    mock_manager.save = Mock()

    initial_data = {"key": "value"}

    with patch("tidycode.core.pyproject.sections.add_section.print_success"):
        add_config_section(
            manager=mock_manager,
            section_name="test-section",
            initial_data=initial_data,
            interactive=False,
        )

    # Verify all manager methods were called
    mock_manager.set_section.assert_called_once()
    mock_manager.save.assert_called_once()

    # Verify set_section was called with correct parameters
    set_section_call = mock_manager.set_section.call_args
    assert set_section_call[1]["overwrite"] is True
    assert set_section_call[1]["dot_key"] == "test-section"
