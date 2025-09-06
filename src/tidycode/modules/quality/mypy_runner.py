"""
Mypy runner.
"""

from pathlib import Path
from typing import Any, List, Optional

from tidycode.plugins import register_plugin
from tidycode.plugins.runner import BaseRunner


@register_plugin(
    name="mypy",
    description="Mypy runner.",
    type="runner",
    category="quality",
    scope="type",
)
class MypyRunner(BaseRunner):
    """
    Mypy runner.
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
        cmd = ["mypy"]
        if target is not None:
            cmd.append(str(target))
        return cmd
