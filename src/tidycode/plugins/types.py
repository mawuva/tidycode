"""
Types for plugins modules.
"""

from dataclasses import dataclass


@dataclass
class PluginMeta:
    name: str
    description: str = ""
    category: str = "default"  # Ex: "config_provider", "runner"
    type: str = "generic"  # Ex: "quality", "audit", "extension"
    scope: str = "default"  # Ex: "style", "type", "security", "complexity"
