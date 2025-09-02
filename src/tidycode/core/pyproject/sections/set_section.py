"""
Set a section in the pyproject.toml file.
"""

from typing import Any, Dict, Optional

from tomlkit.items import Table

from tidycode.changelog.manager import ChangeLogManager
from tidycode.core.pyproject.types import GlobalActions, Mode
from tidycode.core.pyproject.utils.display import print_section_summary
from tidycode.core.pyproject.utils.key_actions import select_and_handle_section_keys
from tidycode.core.pyproject.utils.prompt import prompt_global_action, prompt_key_values
from tidycode.core.pyproject.utils.section_utils import (
    collect_subsection_data,
    select_section,
)
from tidycode.core.toml.manager import TomlFileManager
from tidycode.utils import print_error, print_success

changelog = ChangeLogManager()


def set_config_section(
    manager: TomlFileManager,
    section_name: Optional[str] = None,
    *,
    prefix: str = "",
    display_label: str = "section",
    initial_data: Optional[Dict[str, Any]] = None,
    interactive: bool = True,
) -> None:
    """Set a section in the pyproject.toml file.

    Args:
        manager (TomlFileManager): The manager of the pyproject.toml file.
        section_name (Optional[str]): The name of the section to set.
        prefix (str): The prefix of the section.
        display_label (str): The label of the section.
        initial_data (Optional[Dict[str, Any]]): The initial data of the section.
        interactive (bool): Whether the user wants to interact with the section.
    """

    if not interactive and not section_name:
        raise ValueError("❌ 'section_name' must be provided when interactive=False.")

    # 1) Select section/tool if not provided
    if not section_name:
        section_name = select_section(manager)

    if not section_name:
        print_error(f"No {display_label} selected, exiting.")
        return None

    full_name = f"{prefix}{section_name}" if prefix else section_name

    # 2) Get section data
    section_current_data = (
        initial_data.copy()
        if initial_data is not None
        else manager.get_section(section_name)
    )

    if not section_current_data:
        print_error(f"Section '{section_name}' not found in {str(manager.path)}.")
        return None

    print_section_summary(
        section_name=full_name, data=section_current_data, display_content=False
    )

    with changelog.capture(section_current_data, prefix=f"{full_name}."):
        if interactive:
            while True:
                action = prompt_global_action()

                if action == GlobalActions.EXIT:
                    break

                elif action == GlobalActions.ADD_KEYS:
                    added_data = prompt_key_values(
                        existing=section_current_data, mode=Mode.ADD
                    )
                    section_current_data.update(added_data)

                elif action == GlobalActions.ADD_SUBSECTION:
                    section_current_data.update(
                        collect_subsection_data(full_name, section_name)
                    )

                elif action == GlobalActions.EDIT:
                    select_and_handle_section_keys(section_current_data, mode=Mode.EDIT)

                elif action == GlobalActions.REMOVE:
                    select_and_handle_section_keys(
                        section_current_data, mode=Mode.REMOVE
                    )

    manager.set_section(data=section_current_data, dot_key=full_name, overwrite=True)

    section_obj = manager.get_section(full_name)
    if isinstance(section_obj, Table):
        section_obj.trivia.trail = "\n"

    manager.save()

    print_success(
        f"Section '{section_name}' updated in {str(manager.path)}.", newline_after=True
    )

    if interactive:
        print_section_summary(
            section_name=full_name, data=section_current_data, display_content=True
        )
        changelog.display()
    else:
        changelog.display(silent=False, show_values=False)
