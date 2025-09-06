"""
Ruff runner.
"""

from pathlib import Path
from typing import Any, List, Optional

from tidycode.plugins import register_plugin
from tidycode.plugins.runner import BaseRunner


@register_plugin(
    name="ruff",
    description="Ruff runner.",
    type="runner",
    category="quality",
    scope="style",
)
class RuffRunner(BaseRunner):
    """
    Ruff runner.
    """

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
        cmd = ["ruff", "check"]
        if not check_only:
            cmd.append("--fix")
        return cmd
