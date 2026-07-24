"""
vidiq_competitor_sync.py — reconcile VidIQ's tracked competitor list with the
repo's curated `competitor_channels.json` (the source of truth).

Why this exists (ADR-0013 / grill 2026-07-01): VidIQ auto-populated its tracked
competitor list with off-brand channels (finance, video games, gen-ed, conspiracy)
and NONE of the channel's documented style-peers. `vidiq_outliers(channelIds=tracked)`
therefore mined garbage as the channel's "demand signal." The repo already holds the
correct, category-tagged set. This utility computes the target set + the diff against
whatever VidIQ currently tracks, so the agent can call `vidiq_update_competitors`.

Design constraint: MCP tools (vidiq_*) CANNOT be called from Python. So this tool is
"offline": it takes VidIQ's current tracked IDs as input (--current, gathered by the
agent via vidiq_list_competitors) and EMITS the target ID list + a readable diff. The
agent then performs the single write via vidiq_update_competitors.

Locked policy (grill 2026-07-01):
  - Tracked set = repo tiers {style-match, broad-history}. The `geopolitics` tier
    (stakes-first anti-voice lane) is EXCLUDED from the standing default.
  - Full replace, not prune. Repo is canonical; VidIQ mirrors it.

Usage:
    # Show the target set (what VidIQ should track):
    python -m tools.intel.vidiq_competitor_sync

    # Diff against VidIQ's current tracked IDs (agent pastes them from vidiq_list_competitors):
    python -m tools.intel.vidiq_competitor_sync --current "UCxxxx,UCyyyy,..."

    # Machine-readable (target ids + diff) for the agent to feed vidiq_update_competitors:
    python -m tools.intel.vidiq_competitor_sync --current "..." --json
"""

import argparse
import json
import sys
from typing import Dict, List, Optional

from tools.logging_config import get_logger, setup_logging
from tools.intel.competitor_tracker import load_channel_config

logger = get_logger(__name__)

# Tiers that belong in VidIQ's standing default outlier lens (grill-locked).
DEFAULT_TIERS = ("style-match", "broad-history")


def build_target_set(
    config_path: Optional[str] = None,
    tiers: tuple = DEFAULT_TIERS,
) -> Dict:
    """Load competitor_channels.json and select the channels for VidIQ's tracked set.

    Returns {'channels': [{'id','name','category'}...], 'ids': [...]} on success,
    or {'error': str} if the config can't be loaded.
    """
    channels = load_channel_config(config_path)
    if isinstance(channels, dict) and "error" in channels:
        return channels  # propagate the error dict

    selected = [
        {"id": c.get("id"), "name": c.get("name", c.get("id")), "category": c.get("category", "")}
        for c in channels
        if c.get("category") in tiers and c.get("id")
    ]
    return {"channels": selected, "ids": [c["id"] for c in selected]}


def diff_tracked(target_ids: List[str], current_ids: List[str]) -> Dict[str, List[str]]:
    """Compute the add/remove/keep diff to move VidIQ from current → target.

    Order-preserving, duplicate-safe.
    """
    target = list(dict.fromkeys(target_ids))
    current = list(dict.fromkeys(current_ids))
    target_set, current_set = set(target), set(current)
    return {
        "to_add": [i for i in target if i not in current_set],
        "to_remove": [i for i in current if i not in target_set],
        "unchanged": [i for i in target if i in current_set],
    }


def _parse_ids(raw: Optional[str]) -> List[str]:
    if not raw:
        return []
    return [tok.strip() for tok in raw.replace("\n", ",").split(",") if tok.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Reconcile VidIQ tracked competitors with the repo's curated set (repo = canonical).",
    )
    parser.add_argument(
        "--current",
        help="VidIQ's currently-tracked channel IDs (comma/newline separated) — from vidiq_list_competitors. "
             "Omit to just print the target set.",
    )
    parser.add_argument(
        "--tiers",
        default=",".join(DEFAULT_TIERS),
        help=f"Repo categories to include (comma-separated). Default: {','.join(DEFAULT_TIERS)}",
    )
    parser.add_argument("--config", help="Path to competitor_channels.json (default: repo copy)")
    parser.add_argument("--json", action="store_true", help="Machine-readable output")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-q", "--quiet", action="store_true")
    args = parser.parse_args()
    setup_logging(args.verbose, args.quiet)

    tiers = tuple(t.strip() for t in args.tiers.split(",") if t.strip())
    target = build_target_set(args.config, tiers)
    if "error" in target:
        print(f"ERROR: {target['error']}", file=sys.stderr)
        sys.exit(2)

    current_ids = _parse_ids(args.current)
    diff = diff_tracked(target["ids"], current_ids) if current_ids else None

    if args.json:
        print(json.dumps(
            {"tiers": list(tiers), "target": target, "current_ids": current_ids, "diff": diff},
            indent=2,
        ))
        return

    print(f"\n{'=' * 68}")
    print("  VidIQ COMPETITOR SYNC  (repo = source of truth)")
    print(f"{'=' * 68}")
    print(f"  Tiers included: {', '.join(tiers)}")
    print(f"  Target set: {len(target['ids'])} channels\n")
    for c in target["channels"]:
        print(f"    {c['id']}  [{c['category']:>13}]  {c['name']}")

    if diff is not None:
        print(f"\n  {'-' * 64}")
        print(f"  DIFF vs VidIQ current ({len(current_ids)} tracked):")
        print(f"    + add    ({len(diff['to_add'])}): {', '.join(diff['to_add']) or '(none)'}")
        print(f"    - remove ({len(diff['to_remove'])}): {', '.join(diff['to_remove']) or '(none)'}")
        print(f"    = keep   ({len(diff['unchanged'])}): {', '.join(diff['unchanged']) or '(none)'}")
        print(f"\n  → Call vidiq_update_competitors with the {len(target['ids'])} target IDs above.")
    print()


if __name__ == "__main__":
    main()
