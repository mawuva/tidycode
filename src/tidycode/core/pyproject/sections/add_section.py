"""
Add a new section in the pyproject.toml file through the CLI.
"""

from typing import Any, Dict, Optional

from tomlkit.items import Table

from tidycode.changelog import ChangeLogManager
from tidycode.core.pyproject.types import OverwriteChoice
from tidycode.core.pyproject.utils.display import print_section_summary
from tidycode.core.pyproject.utils.helpers import has_subsections, list_subsections
from tidycode.core.pyproject.utils.section_utils import collect_section_data
from tidycode.core.toml import TomlFileManager
from tidycode.plugins.config import ConfigProvider
from tidycode.utils import (
    ask_action,
    ask_text,
    print_error,
    print_success,
    print_warning,
)

changelog = ChangeLogManager()


def add_config_section(
    manager: TomlFileManager,
    section_name: Optional[str],
    *,
    prefix: str = "",
    display_label: str = "section",
    plugin: Optional[ConfigProvider] = None,
    initial_data: Optional[Dict[str, Any]] = None,
    interactive: bool = True,
) -> None:
    """
    Create or update a config block in pyproject.toml, either interactively
    or via a plugin / predefined data.

    Args:
        manager: PyProjectManager instance
        section_name: Name of the section/tool
        prefix: Optional prefix like "tool."
        display_label: Display label for prompts
        plugin: Optional ConfigProvider plugin
        initial_data: Predefined dict to insert (used when interactive=False)
        interactive: If False, disables all prompts
    """

    # 1. Get the section name
    if plugin:
        section_name = plugin.get_name()
    elif not section_name:
        section_name = ask_text(f"Enter the new {display_label} name:").strip()

    if not section_name:
        print_error(f"{display_label.capitalize()} name cannot be empty.")
        return None

    full_name = f"{prefix}{section_name}" if prefix else section_name

    # 2. Check if the section already exists
    existing = manager.get_section(full_name) or {}
    overwrite_choice = None

    if existing and interactive and not plugin:
        print_warning(f"{display_label.capitalize()} '{section_name}' already exists.")

        if has_subsections(existing):
            subsections = list_subsections(existing)
            print_warning(
                f"This {display_label} contains subsections: {', '.join(subsections)}"
            )

        overwrite_choice = ask_action(
            f"What do you want to do with the existing {display_label}?",
            OverwriteChoice.to_list(),
        )

        if overwrite_choice == OverwriteChoice.CANCEL:
            print_warning(
                f"{display_label.capitalize()} '{section_name}' not modified."
            )
            return None

    # 3. Collect new data interactively
    new_data = collect_section_data(
        manager=manager,
        full_name=full_name,
        section_name=section_name,
        display_label=display_label,
        existing=existing,
        overwrite_choice=overwrite_choice,
        plugin=plugin,
        initial_data=initial_data,
        interactive=interactive,
    )

    if not new_data:
        print_warning(f"{display_label.capitalize()} '{section_name}' not modified.")
        return None

    # 4. Build the final data/config
    if existing and overwrite_choice == OverwriteChoice.OVERWRITE:
        final_data = new_data
    else:
        final_data = {**existing, **new_data}

    # 5. Persist
    manager.set_section(data=final_data, dot_key=full_name, overwrite=True)

    # 6. Ensure line break after the section (works for nested tables too)
    section_obj = manager.get_section(full_name)
    if isinstance(section_obj, Table):
        section_obj.trivia.trail = "\n"

    manager.save()

    action = (
        "overwritten"
        if overwrite_choice == OverwriteChoice.OVERWRITE
        else "created/updated"
    )
    print_success(
        f"{display_label.capitalize()} '{section_name}' {action}.\n",
        newline_before=True,
    )

    if interactive:
        print_section_summary(section_name=full_name, data=final_data)
        changelog.display()
    else:
        changelog.display(silent=False, show_values=False)
