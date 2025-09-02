"""
Remove a section from the pyproject.toml file.
"""

from typing import Optional

from tidycode.changelog import ChangeLogManager
from tidycode.settings import YesNo
from tidycode.core.pyproject.types import RemoveSectionChoices
from tidycode.core.pyproject.utils.helpers import get_keys
from tidycode.core.pyproject.utils.key_actions import handle_key_deletion
from tidycode.core.pyproject.utils.section_utils import select_section
from tidycode.core.toml import TomlFileManager
from tidycode.utils import ask_action, ask_choice, print_error, print_success

changelog = ChangeLogManager()


def remove_config_section(
    manager: TomlFileManager,
    section_name: Optional[str] = None,
    *,
    prefix: str = "",
    display_label: str = "section",
    interactive: bool = True,
) -> None:
    """Remove a section from the pyproject.toml file.

    Args:
        manager (TomlFileManager): The manager of the pyproject.toml file.
        section_name (str): The name of the section to remove.
        prefix (str): The prefix of the section.
        display_label (str): The label of the section.
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
    section_current_data = manager.get_section(full_name)

    if not section_current_data:
        print_error(f"Section '{section_name}' not found in {str(manager.path)}.")
        return None

    # 2) Ask if deleting entire block or individual keys
    delete_choice = ask_action(
        f"Do you want to delete the entire {display_label} '{section_name}' or specific keys?",
        RemoveSectionChoices.to_list(),
    )

    with changelog.capture(section_current_data, prefix=f"{full_name}."):
        if delete_choice == RemoveSectionChoices.ENTIRE_SECTION:
            confirm = ask_action(
                f"Are you sure you want to delete {display_label} '{section_name}'?",
                YesNo.to_list(),
            )
            if confirm == YesNo.YES:
                section_current_data.clear()
                manager.delete_section(full_name)
                manager.save()

        elif delete_choice == RemoveSectionChoices.KEYS_ONLY:
            while section_current_data:
                choices = get_keys(section_current_data, hide_sensitive=True) + ["exit"]
                if not choices:
                    print_error(
                        f"No keys available to remove in {display_label} '{section_name}'."
                    )
                    return None

                key_to_remove = ask_choice(
                    f"Select a key to remove from {display_label} '{section_name}':",
                    choices,
                )
                if key_to_remove == "exit":
                    break

                handle_key_deletion(key_to_remove, section_current_data)

                manager.set_section(
                    data=section_current_data, dot_key=full_name, overwrite=True
                )

    manager.save()

    print_success(
        f"{display_label.capitalize()} '{section_name}' removed from {str(manager.path)}."
    )
    changelog.display()

    return None
