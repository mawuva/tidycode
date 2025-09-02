"""
Utils for the pyproject section.
"""

from typing import Any, Dict, Optional

from tidycode.changelog import ChangeLogManager
from tidycode.core.pyproject.types import Mode, OverwriteChoice, PyProjectHiddenSections
from tidycode.core.pyproject.utils.prompt import prompt_key_values
from tidycode.core.toml import TomlFileManager
from tidycode.plugins.config import ConfigProvider
from tidycode.settings import YesNo
from tidycode.utils import ask_action, ask_choice, ask_text, print_error

changelog = ChangeLogManager()


def collect_subsection_data(
    full_name: str,
    section_name: str,
) -> Dict[str, Any]:
    """
    Prompt the user to create a new subsection with keys/values.

    Args:
        full_name: Fully qualified section name (e.g., "tool.myplugin").
        section_name: Raw section name (e.g., "myplugin").

    Returns:
        A dictionary containing the subsection name and its data.
        Example: {"subsection": {"key": "value"}}
    """
    subsection_name = ask_text(
        f"Enter the subsection name under '{section_name}':"
    ).strip()

    if not subsection_name:
        return {}

    subsection_full = f"{full_name}.{subsection_name}"
    subsection_data: Dict[str, Any] = {}

    with changelog.capture(subsection_data, prefix=f"{subsection_full}."):
        subsection_data.update(prompt_key_values(existing={}, mode=Mode.ADD))

    return {subsection_name: subsection_data}


def collect_section_data(
    manager: TomlFileManager,
    *,
    full_name: str,
    section_name: str,
    display_label: str,
    existing: Dict[str, Any],
    overwrite_choice: Optional[OverwriteChoice | str],
    plugin: Optional[ConfigProvider],
    initial_data: Optional[Dict[str, Any]],
    interactive: bool,
) -> Optional[Dict[str, Any]]:
    """
    Collect configuration data for a section.

    Args:
        manager: PyProjectManager instance
        full_name: Fully qualified section name (with prefix if any).
        section_name: Raw section name.
        display_label: Label to display in prompts.
        existing: Existing data for this section.
        overwrite_choice: User's choice on handling conflicts.
        plugin: Optional plugin providing config.
        initial_data: Predefined data if interactive is False.
        interactive: Enable/disable prompts.

    Returns:
        A dictionary with new section data or None if cancelled.
    """

    new_data: Dict[str, Any] = {}

    with changelog.capture(new_data, prefix=f"{full_name}."):
        if plugin:
            new_data.update(plugin.get_data())
        elif initial_data:
            new_data.update(initial_data)
        elif interactive:
            if existing and overwrite_choice == OverwriteChoice.OVERWRITE:
                try:
                    manager.delete_section(full_name)
                except AttributeError:
                    manager.set_section(data={}, dot_key=full_name, overwrite=True)

                add_keys = ask_action(
                    f"Do you want to add keys to this {display_label}?", YesNo.to_list()
                )

                if add_keys == YesNo.YES:
                    new_data.update(prompt_key_values(existing={}, mode=Mode.ADD))

            elif overwrite_choice == OverwriteChoice.ADD_KEYS:
                new_data.update(prompt_key_values(existing={}, mode=Mode.ADD))

            elif overwrite_choice == OverwriteChoice.ADD_SUBSECTION:
                new_data.update(collect_subsection_data(full_name, section_name))
            else:
                new_data.update(prompt_key_values(existing={}, mode=Mode.ADD))
        else:
            print_error(
                f"No data provided for {display_label.capitalize()} '{section_name}'."
            )
            return None

    return new_data


def select_section(manager: TomlFileManager) -> Optional[str]:
    """Select a section from the pyproject.toml file.

    Args:
        manager (TomlFileManager): The manager of the pyproject.toml file.

    Returns:
        str: The name of the selected section.
    """
    editable_sections = [
        section
        for section in manager.document.keys()
        if section not in PyProjectHiddenSections.to_list()
    ]

    if not editable_sections:
        print_error("❌ No editable/removable sections found in pyproject.toml.")
        return None

    return ask_choice("Choose a section to modify/remove", editable_sections)
