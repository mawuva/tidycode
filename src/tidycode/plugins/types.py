"""
Types for plugins modules.
"""

from dataclasses import dataclass


@dataclass
class PluginMeta:
    name: str
    description: str = ""
    type: str = "generic"  # Ex: "quality", "audit", "extension"
    category: str = "default"  # Ex: "config_provider", "runner"
