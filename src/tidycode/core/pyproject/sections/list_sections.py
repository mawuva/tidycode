"""
List all sections from the pyproject.toml file.
"""

from tidycode.core.pyproject.utils.display import print_section_summary
from tidycode.core.toml import TomlFileManager
from tidycode.utils import print_error


def list_config_sections(
    manager: TomlFileManager,
    prefix: str = "",
    interactive: bool = True,
):
    """List all sections from the pyproject.toml file."""

    sections = manager.document

    if not sections:
        print_error("No sections found in the pyproject.toml file.")
        return None

    print_section_summary(
        section_name=str(manager.path), data=sections, display_content=True
    )
