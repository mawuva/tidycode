"""
Base class for runners.
"""

from abc import abstractmethod
from pathlib import Path
from typing import Any, List, Optional

from tidycode.plugins.base import BasePlugin


class BaseRunner(BasePlugin):
    """
    Base class for runners.
    """

    @abstractmethod
    def build_command(
        self,
        target: Optional[Path],
        check_only: Optional[bool],
        *args: Any,
        **kwargs: Any,
    ) -> List[str]:
        """
        Build the command to run.
        """
        pass

    def is_tool(self) -> bool:
        """Permet de dire si c’est un vrai outil externe ou juste une commande interne"""
        return True
