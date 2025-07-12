"""
Utils for Tidycode
"""

from .constants import (
    CONFIG_FILE_PATH,
    PYPROJECT_PATH,
    DEPENDABOT_PATH,
    EXCLUDE_DIRS,
    TARGETS,
)

from .hooks.hooks_definitions import HOOKS
from .tools_metadata import TOOLS_METADATA

from .hooks.hooks_helpers import (
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

from .toml.toml_helpers import (
    load_toml_file,
    save_toml_file,
    has_tool_section,
    get_tool_section,
    set_tool_section,
    remove_tool_section,
    remove_tool_section_and_return,
)

from .toml.toml_config_editor import (
    inject_toml_config,
    inject_tool_config,
    inject_tool_config_in_file,
)

from .toml.toml_config_diff import (
    diff_configs,
    format_config_diff,
)


__all__ = [
    "CONFIG_FILE_PATH",
    "PYPROJECT_PATH",
    "DEPENDABOT_PATH",
    "TOOLS_METADATA",
    "HOOKS",
    "EXCLUDE_DIRS",
    "TARGETS",

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

    "load_toml_file",
    "save_toml_file",
    "has_tool_section",
    "get_tool_section",
    "set_tool_section",
    "remove_tool_section",
    "remove_tool_section_and_return",

    "inject_toml_config",
    "inject_tool_config",
    "inject_tool_config_in_file",

    "diff_configs",
    "format_config_diff",
]
