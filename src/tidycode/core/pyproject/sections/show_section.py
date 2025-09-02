"""
Show a section from the pyproject.toml file.
"""

from typing import Optional

from tidycode.core.pyproject.utils.display import print_section_summary
from tidycode.core.pyproject.utils.section_utils import select_section
from tidycode.core.toml import TomlFileManager
from tidycode.utils import print_error


def show_config_section(
    manager: TomlFileManager,
    section_name: Optional[str] = None,
    *,
    prefix: str = "",
    display_label: str = "section",
    interactive: bool = True,
    display_list: bool = False,
):
    """Show a section from the pyproject.toml file."""

    if not interactive and not section_name and not display_list:
        raise ValueError("❌ 'section_name' must be provided when interactive=False.")

    # 1) Select section/tool if not provided
    if not interactive and display_list:
        section_name = None

    if not section_name:
        section_name = select_section(manager)

    if not section_name:
        print_error(f"No {display_label} selected, exiting.")
        return None

    full_name = f"{prefix}{section_name}" if prefix else section_name

    section_current_data = manager.get_section(full_name)

    if not section_current_data:
        print_error(f"Section '{section_name}' not found in {str(manager.path)}.")
        return None

    print_section_summary(
        section_name=full_name, data=section_current_data, display_content=True
    )
