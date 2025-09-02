"""
Base class for plugins.
"""

from typing import Protocol

from .types import PluginMeta


class BasePlugin(Protocol):
    meta: PluginMeta
