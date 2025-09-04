"""
Convert a dict to a ConfigProvider.
"""

from typing import Any, Dict

from tidycode.plugins import register_plugin
from .base_provider import ConfigProvider


@register_plugin(
    name="dict",
    description="Convert a dict to a ConfigProvider.",
    type="config",
    category="config_provider",
)
class DictPlugin(ConfigProvider):
    """
    Convert a dict to a ConfigProvider.
    """

    def __init__(self, name: str, data: Dict[str, Any]):
        self._name = name
        self._data = data

    def get_name(self) -> str:
        return self._name

    def get_data(self) -> Dict[str, Any]:
        return self._data
