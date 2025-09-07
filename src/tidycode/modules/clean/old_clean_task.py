"""
Clean task.
"""

from pathlib import Path
from typing import Dict, Iterable, List, Optional
import shutil

from tidycode.core.pyproject.utils.helpers import load_tidycode_config
from tidycode.runner.display import print_summary
from tidycode.runner.types import SubprocessDisplayMode, SubprocessResult
from tidycode.utils.printing import print_info, print_success, print_error


def _handle_removal(
    paths: Iterable[Path],
    excludes: List[str],
    dry_run: bool,
    label: str,
    counters: Dict[str, int],
    verbose: bool = False,
) -> List[SubprocessResult]:
    """
    Handle removal of files/directories with dry-run, logging and error handling.
    
    Args:
        paths: paths to clean
        excludes: paths to exclude
        dry_run: if True, only show what would be deleted without actually deleting
        label: label to use for the clean
    Returns:
        List of standardized results for summary display
    """
    results: List[SubprocessResult] = []

    for path in paths:
        if str(path) in excludes or not path.exists():
            continue

        display_name = f"Clean {label}: {path}"
        
        if path.is_dir():
            counters["directory"] += 1
        else:
            counters["file"] += 1

        if dry_run:
            if verbose:
                print_info(f"[Dry-run] Would remove {label}: {path}", newline_before=True)
            
            results.append(
                SubprocessResult(
                    display_name=display_name,
                    status="DRY_RUN",
                    summary=f"Would remove {label}: {path}",
                    stdout=str(path),
                )
            )
            continue

        try:
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()

            if verbose:
                print_success(f"Removed {label}: {path}", newline_before=True)
            results.append(
                SubprocessResult(
                    display_name=display_name,
                    status="SUCCESS",
                    summary=f"Removed {label}: {path}",
                    stdout=str(path),
                )
            )
        except Exception as e:
            if verbose:
                print_error(f"Error removing {label}: {path}")
            results.append(
                SubprocessResult(
                    display_name=display_name,
                    status="ERROR",
                    summary=f"Error removing {label}: {path}",
                    stdout=str(path),
                    stderr=str(e),
                )
            )

    return results



def run_clean_task(
    summary_mode: Optional[SubprocessDisplayMode] = SubprocessDisplayMode.TABLE_FULL,
    dry_run: bool = False,
    target: Optional[str] = None,
    excludes: Optional[List[str]] = None,
    verbose: bool = False,
):
    """
    Execute clean tasks defined in pyproject.toml under [tool.tidycode.clean].

    Args:
        summary_mode: display mode for summary
        dry_run: if True, only show what would be deleted without actually deleting
        target: target directory
        excludes: comma-separated list of files/directories to exclude
    Returns:
        List of standardized results for summary display
    """
    
    configs = load_tidycode_config()
    clean_conf = configs.get("clean", {})

    target_dir = Path(target or clean_conf.get("target", "."))

    cleanable_dirs = [target_dir / Path(d) for d in clean_conf.get("cleanable_dirs", [])]
    cleanable_files = [target_dir / Path(f) for f in clean_conf.get("cleanable_files", [])]
    patterns = clean_conf.get("patterns", [])
    excludes = [str(Path(e)) for e in (excludes or clean_conf.get("excludes", []))]
    
    results: List[SubprocessResult] = []
    counters: Dict[str, int] = {
        "directory": 0,
        "file": 0,
    }

    # Handle directories, files and patterns
    results.extend(_handle_removal(cleanable_dirs, excludes, dry_run, "directory", counters, verbose))
    results.extend(_handle_removal(cleanable_files, excludes, dry_run, "file", counters, verbose))

    for pattern in patterns:
        matched_paths = list(target_dir.rglob(pattern))
        results.extend(_handle_removal(matched_paths, excludes, dry_run, "pattern", counters, verbose))

    print_summary(results, summary_mode)
    
    print_info("\n--- Clean Task Summary ---")
    if dry_run:
        print_info(f"Would remove directories: {counters['directory']}")
        print_info(f"Would remove files: {counters['file']}")
    else:
        print_success(f"Removed directories: {counters['directory']}")
        print_success(f"Removed files: {counters['file']}")
        
    return results
        