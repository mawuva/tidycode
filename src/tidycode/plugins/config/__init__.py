"""
Plugins for configuring the pyproject.toml file and more.
"""

from .base_provider import ConfigProvider
from .dict_plugin import DictPlugin

__all__ = ["DictPlugin", "ConfigProvider"]
