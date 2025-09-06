"""
Black runner.
"""

from pathlib import Path
from typing import Any, List, Optional

from tidycode.plugins import register_plugin
from tidycode.plugins.runner import BaseRunner


@register_plugin(
    name="black",
    description="Black runner.",
    type="runner",
    category="quality",
    scope="style",
)
class BlackRunner(BaseRunner):
    """
    Black runner.
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
        cmd = ["black"]
        if target is not None:
            cmd.append(str(target))
        if check_only:
            cmd.append("--check")
        return cmd
