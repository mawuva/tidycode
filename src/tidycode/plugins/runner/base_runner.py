"""
Base class for runners.
"""

from abc import abstractmethod
from pathlib import Path
from typing import Any, List, Optional

from tidycode.plugins.base import BasePlugin
from tidycode.runner import CommandSpec, run_command, run_command_live


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

    def run(
        self,
        target: Optional[Path] = None,
        check_only: Optional[bool] = False,
        dry_run: bool = False,
        live: bool = False,
        verbose: bool = True,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Run the command.
        """
        cmd: List[str] = self.build_command(target, check_only, *args, **kwargs)

        if dry_run:
            print(f"[DRY RUN] {self.meta.name}: {' '.join(cmd)}")
            return

        if live:
            run_command_live(
                command=cmd,
                display_name=self.meta.name,
                cwd=target,
                is_tool=self.is_tool(),
            )
        else:
            run_command(
                command=cmd,
                display_name=self.meta.name,
                cwd=target,
                is_tool=self.is_tool(),
                verbose=verbose,
            )

    def get_command_spec(
        self,
        target: Optional[Path],
        check_only: Optional[bool],
        *args: Any,
        **kwargs: Any,
    ) -> CommandSpec:
        """
        Get the command spec.
        """
        return CommandSpec(
            command=self.build_command(target, check_only, *args, **kwargs),
            display_name=self.meta.name,
            cwd=target,
            is_tool=self.is_tool(),
        )
