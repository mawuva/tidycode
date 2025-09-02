"""
Plugins for configuring the pyproject.toml file and more.
"""


from .dict_plugin import DictPlugin
from .base_provider import ConfigProvider

__all__ = ["DictPlugin", "ConfigProvider"]

