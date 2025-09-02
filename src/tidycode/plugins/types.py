"""
Types for plugins modules.
"""

from dataclasses import dataclass


@dataclass
class PluginMeta:
    name: str
    description: str = ""
