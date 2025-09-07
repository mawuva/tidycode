"""
Clean task module with counters, JSON summary and relative paths.
"""

from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple
import shutil
import json

from tidycode.core.pyproject.utils.helpers import load_tidycode_config
from tidycode.runner.display import print_summary
from tidycode.runner.types import SubprocessDisplayMode, SubprocessResult
from tidycode.utils.printing import print_info, print_success, print_error


def _relative(path: Path, base: Path) -> str:
    """Return path relative to base directory (fallback: absolute)."""
    try:
        return str(path.relative_to(base))
    except ValueError:
        return str(path)


def _handle_removal(
    paths: Iterable[Path],
    excludes: List[str],
    dry_run: bool,
    label: str,
    counters: Dict[str, int],
    verbose: bool,
    target_dir: Path,
)  -> Tuple[List[SubprocessResult], List[str]]:
    """
    Handle removal of files/directories with dry-run, logging and error handling.
    Paths are normalized relative to target_dir for display and JSON output.
    """
    results: List[SubprocessResult] = []
    skipped: List[str] = []

    for path in paths:
        rel_path = _relative(path, target_dir)

        # Exclude check (use relative path for matching)
        if rel_path in excludes or not path.exists():
            skipped.append(rel_path)
            continue

        display_name = f"Clean {label}: {rel_path}"

        # Count (always increment, even in dry-run)
        # Count the number of directories and files
        if path.is_dir():
            counters["directory"] += 1
        else:
            counters["file"] += 1

        if dry_run:
            if verbose:
                print_info(f"[Dry-run] Would remove {label}: {rel_path}", newline_before=True)

            results.append(
                SubprocessResult(
                    display_name=display_name,
                    status="DRY_RUN",
                    summary=f"Would remove {label}: {rel_path}",
                    stdout=rel_path,
                )
            )
            continue

        try:
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()

            if verbose:
                print_success(f"Removed {label}: {rel_path}", newline_before=True)
            results.append(
                SubprocessResult(
                    display_name=display_name,
                    status="SUCCESS",
                    summary=f"Removed {label}: {rel_path}",
                    stdout=rel_path,
                )
            )
        except Exception as e:
            counters["error"] += 1
            if verbose:
                print_error(f"Error removing {label}: {rel_path}")
            results.append(
                SubprocessResult(
                    display_name=display_name,
                    status="ERROR",
                    summary=f"Error removing {label}: {rel_path}",
                    stdout=rel_path,
                    stderr=str(e),
                )
            )

    return results, skipped


def run_clean_task(
    summary_mode: Optional[SubprocessDisplayMode] = SubprocessDisplayMode.TABLE_FULL,
    dry_run: bool = False,
    target: Optional[str] = None,
    excludes: Optional[List[str]] = None,
    verbose: bool = False,
    all: bool = False,
):
    """
    Execute clean tasks defined in pyproject.toml under [tool.tidycode.clean].
    """

    configs = load_tidycode_config()
    clean_conf = configs.get("clean", {})

    target_dir = Path(target or clean_conf.get("target", ".")).resolve()

    cleanable_dirs = [target_dir / Path(d) for d in clean_conf.get("cleanable_dirs", [])]
    cleanable_files = [target_dir / Path(f) for f in clean_conf.get("cleanable_files", [])]
    patterns = clean_conf.get("patterns", [])

    # Normalize excludes as relative strings
    excludes = [str(Path(e)) for e in (excludes or clean_conf.get("excludes", []))]

    if all:
        cleanable_dirs += [
            target_dir / "__pycache__",
            target_dir / ".pytest_cache",
            target_dir / ".mypy_cache",
            target_dir / ".ruff_cache",
            target_dir / ".tox",
            target_dir / "build",
            target_dir / "dist",
        ]
        cleanable_files += [
            target_dir / ".coverage",
            target_dir / "coverage.xml",
        ]

    results: List[SubprocessResult] = []
    counters: Dict[str, int] = {"directory": 0, "file": 0, "error": 0}
    skipped_summary: Dict[str, List[str]] = {"directories": [], "files": [], "patterns": []}

    # Handle configured dirs
    rslt, skipped = _handle_removal(cleanable_dirs, excludes, dry_run, "directory", counters, verbose, target_dir)
    results.extend(rslt)
    skipped_summary["directories"].extend(skipped)

    # Handle configured files
    rslt, skipped = _handle_removal(cleanable_files, excludes, dry_run, "file", counters, verbose, target_dir)
    results.extend(rslt)
    skipped_summary["files"].extend(skipped)

    # Handle glob patterns (skip if parent is already scheduled for removal/excluded)
    for pattern in patterns:
        matched_paths: List[Path] = []
        local_skipped: List[str] = []
        for p in target_dir.rglob(pattern):
            skip = False
            for parent in p.parents:
                rel_parent = _relative(parent, target_dir)
                if rel_parent in excludes:
                    local_skipped.append(_relative(p, target_dir))
                    skip = True
                    break
            if not skip:
                matched_paths.append(p)

        r, skipped = _handle_removal(matched_paths, excludes, dry_run, "pattern", counters, verbose, target_dir)
        results.extend(r)
        skipped_summary["patterns"].extend(local_skipped + skipped)

    # Count skipped
    skipped_counts = {
        "directories": len(skipped_summary["directories"]),
        "files": len(skipped_summary["files"]),
        "patterns": len(skipped_summary["patterns"]),
    }
    skipped_total = sum(skipped_counts.values())
    
    # Totals (processed = removed + skipped + errors)
    total_removed = counters["directory"] + counters["file"]
    totals = {
        "processed": total_removed + skipped_total + counters["error"],
        "removed": total_removed,
        "skipped": skipped_total,
        "errors": counters["error"],
    }
    
    # Print classic summary table
    print_summary(results, summary_mode)

    # JSON summary
    summary_json = {
        "totals": totals,
        "removed_directories": counters["directory"],
        "removed_files": counters["file"],
        "errors": counters["error"],
        "dry_run": dry_run,
        "excludes": excludes,
        "target": str(target_dir),
        "items": [r.stdout for r in results],
        "skipped": {
            "count": skipped_total,
            "by_type": skipped_counts,
            "items": skipped_summary,
        },
    }
    print_info("\n--- JSON Summary ---")
    print(json.dumps(summary_json, indent=2))

    return results