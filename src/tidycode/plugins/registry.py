"""
Plugin registry.
"""

from typing import Callable, Dict, List, Optional, Type

from tidycode.plugins.base import BasePlugin
from tidycode.plugins.types import PluginMeta


class PluginRegistry:
    """
    Plugin registry.
    """

    def __init__(self) -> None:
        self._plugins: Dict[str, BasePlugin] = {}

    def register(self, plugin: BasePlugin) -> None:
        self._plugins[plugin.meta.name] = plugin

    def get(self, name: str) -> Optional[BasePlugin]:
        return self._plugins[name]

    def all(self) -> List[BasePlugin]:
        return list(self._plugins.values())

    def by_category(self, category: str) -> List[BasePlugin]:
        return [p for p in self._plugins.values() if p.meta.category == category]

    def by_type(self, type: str) -> List[BasePlugin]:
        return [p for p in self._plugins.values() if p.meta.type == type]

    def by_scope(self, scope: str) -> List[BasePlugin]:
        return [p for p in self._plugins.values() if p.meta.scope == scope]

    def filter(self, **criteria: str) -> List[BasePlugin]:
        """
        Filter plugins by the given criteria.
        """
        return [
            p
            for p in self._plugins.values()
            if all(getattr(p.meta, key) == value for key, value in criteria.items())
        ]


registry = PluginRegistry()


def register_plugin(
    name: str,
    description: str = "",
    type: str = "generic",
    category: str = "default",
    scope: str = "default",
) -> Callable[[Type[BasePlugin]], Type[BasePlugin]]:
    """
    Decorator to register a plugin.
    """

    def decorator(cls: Type[BasePlugin]):
        cls.meta = PluginMeta(
            name=name,
            description=description,
            type=type,
            category=category,
            scope=scope,
        )
        instance = cls()
        registry.register(instance)
        return cls

    return decorator
