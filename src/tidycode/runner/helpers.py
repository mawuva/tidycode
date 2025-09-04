"""
Helpers for the runner.
"""

from tidycode.runner.types import SubprocessResult
from tidycode.utils.printing import print_warning


def status_color(status: str) -> str:
    """Map status to color (Rich/typer compatible)."""
    if "✅" in status:
        return "green"
    if "⚠️" in status:
        return "yellow"
    return "red"


def status_from_returncode(
    display_name: str, 
    return_code: int, 
    stdout: str, 
    is_tool: bool,
) -> str:
    """
    Get the status from the return code.
    
    Args:
        display_name: name of the command
        return_code: return code of the command
        stdout: stdout of the command
        is_tool: if the command is a tool
    Returns:
        str: status
    """
    if not is_tool:
        return f"Exit {return_code}"

    # Ruff can return 1 even if everything is "All done"
    if display_name.lower() == "ruff" and return_code == 1 and "All done" in stdout:
        return "✅ Passed"

    return "✅ Passed" if return_code == 0 else "❌ Failed"


def build_result(
    display_name: str,
    return_code: int,
    stdout: str = "",
    stderr: str = "",
    is_tool: bool = True,
) -> SubprocessResult:
    """
    Standardize the result dict and compute status string.

    Args:
        display_name: name of the tool
        return_code: return code of the command
        stdout: stdout of the command
        stderr: stderr of the command
        is_tool: if the command is a tool
    Returns:
        SubprocessResult: standardized result
    """
    stdout_clean = stdout.encode("utf-8", errors="replace").decode("utf-8")
    stderr_clean = stderr.encode("utf-8", errors="replace").decode("utf-8")

    status = status_from_returncode(display_name, return_code, stdout, is_tool)
    
    return SubprocessResult(
        display_name=display_name,
        status=status,
        return_code=return_code,
        stdout=stdout_clean.strip(),
        stderr=stderr_clean.strip(),
    )
    
    
def handle_exception(
    e: Exception, 
    display_name: str, 
    is_tool: bool = True, 
    verbose: bool = False
) -> SubprocessResult:
    """
    Return standardized result on exception.

    Args:
        e: exception
        display_name: name of the command
        is_tool: if the command is a tool
        verbose: display the outputs
    Returns:
        SubprocessResult: standardized result
    """
    
    msg = (
        str(e)
        if not isinstance(e, FileNotFoundError)
        else f"Command not found: {display_name}"
    )
    
    if verbose:
        print_warning(msg)

    return_code = 127 if isinstance(e, FileNotFoundError) else 1
    
    return build_result(
        display_name,
        return_code=return_code,
        stdout="",
        stderr=msg,
        is_tool=is_tool,
    )