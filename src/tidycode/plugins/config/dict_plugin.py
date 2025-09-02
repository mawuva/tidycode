"""
Convert a dict to a ConfigProvider.
"""

from typing import Any, Dict

from .base_provider import ConfigProvider


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
