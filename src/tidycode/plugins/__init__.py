"""
Plugins module.
"""

from .base import BasePlugin
from .loader import load_plugins_from
from .registry import register_plugin, registry

__all__ = ["registry", "register_plugin", "load_plugins_from", "BasePlugin"]
