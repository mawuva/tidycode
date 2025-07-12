"""
Utils for Tidycode
"""

from .constants import CONFIG_FILE, PYPROJECT, DEPENDABOT
from .hook_definitions import HOOKS
from .tools_metadata import TOOLS_METADATA

from .hooks_helpers import (
    load_config,
    save_config,
    get_installed_hook_keys,
    add_hooks,
    remove_hooks,
    get_hooks_with_yaml,
    get_iter_hook_with_yaml,
)
from .helpers import (
    run_command,
    write_file_if_missing,
    ask_checkbox,
    ask_confirm,
    yaml_dump,
    yaml_load,
    print_msg,
    toml_dump,
    toml_load,
)

from .pyproject_helpers import (
    load_pyproject,
    save_pyproject,
    has_tool_section,
    get_tool_section,
    set_tool_section,
    remove_tool_section,
    remove_tool_section_and_return,
    inject_pyproject_config,
    diff_pyproject_config,
    format_pyproject_diff_plaintext,
)

__all__ = [
    "CONFIG_FILE",
    "PYPROJECT",
    "DEPENDABOT",
    "TOOLS_METADATA",
    "HOOKS",

    "load_config",
    "save_config",
    "get_installed_hook_keys",
    "add_hooks",
    "remove_hooks",
    "get_hooks_with_yaml",
    "get_iter_hook_with_yaml",

    "run_command",
    "write_file_if_missing",
    "ask_checkbox",
    "ask_confirm",
    "yaml_dump",
    "yaml_load",
    "print_msg",
    "toml_dump",
    "toml_load",

    "load_pyproject",
    "save_pyproject",
    "has_tool_section",
    "get_tool_section",
    "set_tool_section",
    "remove_tool_section",
    "remove_tool_section_and_return",
    "inject_pyproject_config",
    "diff_pyproject_config",
    "format_pyproject_diff_plaintext",
]