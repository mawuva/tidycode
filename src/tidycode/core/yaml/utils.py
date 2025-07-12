"""
Utils for YAML.
"""

from typing import Union, Dict, Any, Optional
from pathlib import Path
from .adapters.base import YAMLAdapter
from .manager import YAMLManager
from .adapters.ruamel_adapter import RuamelYAMLAdapter
from .adapters.pyyaml_adapter import PyYAMLAdapter
from tidycode.utils import CONFIG_FILE_PATH


def get_manager(adapter: Union[str, YAMLAdapter, None] = None) -> YAMLManager:
    """
    Return a YAMLManager with the specified adapter.

    - If `adapter` is a string, it must be one of: "pyyaml", "ruamel".
    - If `adapter` is None, defaults to PyYAMLAdapter.
    - If `adapter` is an instance of YAMLAdapter, use it directly.
    """
    if isinstance(adapter, YAMLAdapter):
        selected_adapter = adapter
    elif adapter == "pyyaml":
        selected_adapter = PyYAMLAdapter()
    elif adapter in (None, "ruamel"):
        selected_adapter = RuamelYAMLAdapter()
    else:
        raise ValueError(f"Unsupported YAML adapter: {adapter}")

    return YAMLManager(adapter=selected_adapter)


def yaml_load(
    path: Optional[Path] = None, adapter: Optional[YAMLAdapter] = None
) -> Dict[str, Any]:
    """
    Load a YAML file.
    """
    path = path or CONFIG_FILE_PATH
    manager = get_manager(adapter) if adapter else get_manager()
    return manager.load_file(path)


def yaml_save(
    data: Dict[str, Any], path: Path, adapter: Optional[YAMLAdapter] = None
) -> None:
    """
    Save a YAML file.
    """
    path = path or CONFIG_FILE_PATH
    manager = get_manager(adapter) if adapter else get_manager()
    manager.save_file(data, path)
