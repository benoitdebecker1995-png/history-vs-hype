"""
Graphify snapshot retention.

The post-commit hook writes a fresh dated snapshot into graphify-out/ on every
commit and never removes the old one. By 2026-07-30 that had accumulated 65
dated directories at ~82 MB each — 4.2 GB, of which nothing in the repo reads a
single byte. The live artifacts are graphify-out/graph.json, the .bak restore
copy, the cache, and the tracked research/ subtree; the dated dirs are pure
history.

Keeps the N most recent dated snapshots (default 3) and deletes the rest.
Refuses to touch anything that is not a dated snapshot directory.

Dry-run by default — pass --apply to actually delete.

CLI:
    python -m tools.routines.prune_graphify_snapshots
    python -m tools.routines.prune_graphify_snapshots --keep 5
    python -m tools.routines.prune_graphify_snapshots --apply
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
GRAPHIFY_DIR = REPO_ROOT / "graphify-out"

# A snapshot dir is YYYY-MM-DD, optionally _N for repeat runs on the same day.
# Anything else under graphify-out/ (research/, cache/, *.json, *.bak) is live
# and must never be a deletion candidate.
SNAPSHOT_RE = re.compile(r"^\d{4}-\d{2}-\d{2}(_\d+)?$")

KEEP_DEFAULT = 3


def _sort_key(path: Path):
    """Order snapshots chronologically: date first, then the _N suffix.

    String sort is wrong here — '2026-06-12_2' sorts before '2026-06-12_10'
    lexically but is older, so the suffix has to compare as an integer.
    """
    name = path.name
    date_part, _, suffix = name.partition("_")
    return (date_part, int(suffix) if suffix.isdigit() else 0)


def find_snapshots(graphify_dir: Path = GRAPHIFY_DIR) -> list[Path]:
    """Return dated snapshot dirs, oldest first. Empty list if dir is absent."""
    if not graphify_dir.is_dir():
        return []
    return sorted(
        (p for p in graphify_dir.iterdir() if p.is_dir() and SNAPSHOT_RE.match(p.name)),
        key=_sort_key,
    )


def _dir_size(path: Path) -> int:
    total = 0
    for p in path.rglob("*"):
        try:
            if p.is_file():
                total += p.stat().st_size
        except OSError:
            continue
    return total


def prune(keep: int = KEEP_DEFAULT, apply: bool = False,
          graphify_dir: Path = GRAPHIFY_DIR) -> dict:
    """Delete all but the `keep` most recent snapshots.

    Returns {'kept': [...], 'deleted': [...], 'bytes_freed': int, 'errors': [...]}.
    Never raises — read-side error contract.
    """
    if keep < 1:
        return {"error": "--keep must be at least 1 (never delete every snapshot)"}

    snapshots = find_snapshots(graphify_dir)
    if not snapshots:
        return {"kept": [], "deleted": [], "bytes_freed": 0, "errors": [],
                "note": f"no dated snapshots under {graphify_dir}"}

    doomed = snapshots[:-keep] if keep < len(snapshots) else []
    kept = snapshots[len(doomed):]

    freed = 0
    deleted, errors = [], []
    for path in doomed:
        size = _dir_size(path)
        if apply:
            try:
                shutil.rmtree(path)
            except OSError as exc:
                errors.append(f"{path.name}: {exc}")
                continue
        freed += size
        deleted.append(path.name)

    return {"kept": [p.name for p in kept], "deleted": deleted,
            "bytes_freed": freed, "errors": errors}


def _human(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.1f} {unit}" if unit != "B" else f"{n} B"
        n /= 1024
    return f"{n:.1f} GB"


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Prune old graphify-out dated snapshots.",
        epilog=(
            "Examples:\n"
            "  python -m tools.routines.prune_graphify_snapshots\n"
            "  python -m tools.routines.prune_graphify_snapshots --keep 5 --apply\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--keep", type=int, default=KEEP_DEFAULT,
                    help=f"snapshots to retain, newest first (default {KEEP_DEFAULT})")
    ap.add_argument("--apply", action="store_true",
                    help="actually delete (default is a dry run)")
    args = ap.parse_args()

    result = prune(keep=args.keep, apply=args.apply)
    if "error" in result:
        print(f"ERROR: {result['error']}")
        return 1

    mode = "DELETED" if args.apply else "would delete (dry run)"
    print(f"graphify-out snapshots: {len(result['kept'])} kept, "
          f"{len(result['deleted'])} {mode}, {_human(result['bytes_freed'])} freed")
    if result["kept"]:
        print(f"  kept:    {', '.join(result['kept'])}")
    if result["deleted"]:
        shown = result["deleted"][:5]
        more = f" … +{len(result['deleted']) - 5} more" if len(result["deleted"]) > 5 else ""
        print(f"  removed: {', '.join(shown)}{more}")
    for err in result["errors"]:
        print(f"  ERROR: {err}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
