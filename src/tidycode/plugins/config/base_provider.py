"""
Base class for config providers.
"""

from typing import Any, Dict
from abc import abstractmethod

from tidycode.plugins.base import BasePlugin

class ConfigProvider(BasePlugin):
    """Interface for plugins that provide config data for the pyproject.toml file."""

    @abstractmethod
    def get_name(self) -> str:
        """Return the unique name of the configuration block."""
        pass

    @abstractmethod
    def get_data(self) -> Dict[str, Any]:
        """Return the configuration data as a dict."""
        pass
