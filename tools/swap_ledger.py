"""
Swap Ledger — instruments the single-variable before/after swap loop.

The channel's low-traffic learning strategy is: on a video that still draws
impressions, change EXACTLY ONE packaging variable (thumbnail OR title, never
both) and measure CTR before vs after. Changing both re-blends the number and
you learn nothing about which lever moved it (see
memory/feedback-filters-not-predictors.md, ADR 0007).

Until now that loop lived in prose (experiment #1 baseline was a paragraph in a
memory file). This tool records each swap, auto-computes the before/after delta
from keywords.db ctr_snapshots, flags experiments due to read, and — on a
confirmed lift — emits a paste-ready line for the recipe's proven-recipes
appendix so wins compound into the operation priors.

Source of truth = the `swap_experiments` table in keywords.db (created on first
use). A human-readable view is regenerated at channel-data/SWAP-LEDGER.md on
every write — the same dual-write pattern tools/ctr_quick_add.py uses.

Usage:
    # Record a swap + its baseline (single variable only):
    python -m tools.swap_ledger open --video aSfZtrgGjwA --variable thumbnail \
        --baseline-ctr 1.91 --baseline-impr 2672 --surface Suggested \
        --read-in 21d --old "DEPOPULATED" --new "THE RECEIPTS" --note "real materials"

    # Read the result once impressions have accrued (computes delta + verdict):
    python -m tools.swap_ledger read 1

    # Status board (PENDING past its planned read date is flagged DUE TO READ):
    python -m tools.swap_ledger list
"""

import argparse
import sqlite3
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from tools.logging_config import get_logger

logger = get_logger(__name__)

_PROJECT_ROOT = Path(__file__).parent.parent
_KEYWORDS_DB = _PROJECT_ROOT / "tools" / "discovery" / "keywords.db"
_LEDGER_MD = _PROJECT_ROOT / "channel-data" / "SWAP-LEDGER.md"

VALID_VARIABLES = ("title", "thumbnail")
VALID_SURFACES = ("Suggested", "Search", "Browse", "Mixed", "")

# A delta this size (percentage points) or larger is a real signal; smaller is FLAT.
LIFT_THRESHOLD_PP = 0.5


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------
def _connect(db_path: Optional[str] = None) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path or str(_KEYWORDS_DB))
    conn.row_factory = sqlite3.Row
    _ensure_table(conn)
    return conn


def _ensure_table(conn: sqlite3.Connection) -> None:
    with conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS swap_experiments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id TEXT NOT NULL,
                title TEXT,
                variable TEXT NOT NULL,          -- 'title' | 'thumbnail'
                old_asset TEXT,
                new_asset TEXT,
                swap_date DATE NOT NULL,
                baseline_ctr REAL,
                baseline_impr INTEGER,
                baseline_date DATE,
                surface TEXT,                    -- Suggested | Search | Browse | Mixed
                planned_read_date DATE,
                post_ctr REAL,
                post_impr INTEGER,
                post_date DATE,
                delta_pp REAL,
                verdict TEXT NOT NULL DEFAULT 'PENDING',  -- PENDING|LIFT|FLAT|DROP
                notes TEXT
            )
            """
        )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _today() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def _parse_read_in(spec: str) -> int:
    """'21d' / '21' / '0d' -> int days. Raises ValueError on garbage."""
    s = spec.strip().lower().rstrip("d").strip()
    return int(s)


def _verdict_for(delta_pp: float) -> str:
    if delta_pp >= LIFT_THRESHOLD_PP:
        return "LIFT"
    if delta_pp <= -LIFT_THRESHOLD_PP:
        return "DROP"
    return "FLAT"


def _latest_snapshot(conn: sqlite3.Connection, video_id: str,
                     after_date: Optional[str] = None) -> Optional[sqlite3.Row]:
    """Latest non-zero ctr_snapshots row for a video, optionally after a date."""
    sql = (
        "SELECT ctr_percent, impression_count, view_count, snapshot_date "
        "FROM ctr_snapshots WHERE video_id = ? AND ctr_percent > 0"
    )
    params: List[Any] = [video_id]
    if after_date:
        sql += " AND snapshot_date >= ?"
        params.append(after_date)
    sql += " ORDER BY snapshot_date DESC LIMIT 1"
    try:
        return conn.execute(sql, params).fetchone()
    except sqlite3.Error as e:
        logger.warning("snapshot lookup failed: %s", e)
        return None


# ---------------------------------------------------------------------------
# Core operations
# ---------------------------------------------------------------------------
def open_experiment(
    video_id: str,
    variable: str,
    baseline_ctr: Optional[float] = None,
    baseline_impr: Optional[int] = None,
    surface: str = "",
    read_in_days: int = 21,
    old_asset: str = "",
    new_asset: str = "",
    title: str = "",
    note: str = "",
    also_changed: Optional[str] = None,
    db_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Record a single-variable swap with its baseline.

    Single-variable guard: `variable` is the ONE lever under test. If
    `also_changed` names the *other* lever, the swap is rejected — changing
    both re-blends CTR and the experiment teaches nothing.
    """
    variable = variable.strip().lower()
    if variable not in VALID_VARIABLES:
        return {"error": f"variable must be one of {VALID_VARIABLES}, got '{variable}'"}

    if also_changed:
        other = also_changed.strip().lower()
        if other in VALID_VARIABLES and other != variable:
            return {
                "error": (
                    f"TWO-VARIABLE SWAP REJECTED: you set --variable {variable} but also "
                    f"changed the {other}. Change ONE lever per experiment (single-variable "
                    f"doctrine) — otherwise the CTR delta can't be attributed. "
                    f"Split into two experiments run sequentially."
                )
            }

    if surface and surface not in VALID_SURFACES:
        return {"error": f"surface must be one of {VALID_SURFACES}, got '{surface}'"}

    swap_date = _today()
    planned = (datetime.now(timezone.utc).date()
               + timedelta(days=read_in_days)).isoformat()

    conn = _connect(db_path)
    try:
        with conn:
            cur = conn.execute(
                """
                INSERT INTO swap_experiments
                (video_id, title, variable, old_asset, new_asset, swap_date,
                 baseline_ctr, baseline_impr, baseline_date, surface,
                 planned_read_date, verdict, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'PENDING', ?)
                """,
                (video_id, title, variable, old_asset, new_asset, swap_date,
                 baseline_ctr, baseline_impr, swap_date, surface,
                 planned, note),
            )
        exp_id = cur.lastrowid
        _regenerate_md(conn)
        return {"status": "opened", "id": exp_id, "planned_read_date": planned}
    finally:
        conn.close()


def read_experiment(exp_id: int, db_path: Optional[str] = None) -> Dict[str, Any]:
    """Pull the latest ctr_snapshot for the experiment's video, compute delta + verdict."""
    conn = _connect(db_path)
    try:
        row = conn.execute(
            "SELECT * FROM swap_experiments WHERE id = ?", (exp_id,)
        ).fetchone()
        if row is None:
            return {"error": f"No experiment #{exp_id}"}

        snap = _latest_snapshot(conn, row["video_id"], after_date=row["swap_date"])
        if snap is None:
            return {
                "error": (
                    f"No post-swap ctr_snapshot for {row['video_id']} on/after "
                    f"{row['swap_date']}. Ingest the Studio read first: "
                    f"python -m tools.ctr_quick_add \"<title>\" --ctr X --views Y "
                    f"--impressions Z --swap-read {exp_id}"
                )
            }

        post_ctr = snap["ctr_percent"]
        post_impr = snap["impression_count"]
        baseline = row["baseline_ctr"]
        if baseline is None:
            return {"error": f"Experiment #{exp_id} has no baseline_ctr — cannot compute delta"}

        delta = round(post_ctr - baseline, 2)
        verdict = _verdict_for(delta)

        with conn:
            conn.execute(
                "UPDATE swap_experiments SET post_ctr=?, post_impr=?, post_date=?, "
                "delta_pp=?, verdict=? WHERE id=?",
                (post_ctr, post_impr, snap["snapshot_date"], delta, verdict, exp_id),
            )
        _regenerate_md(conn)

        result = {
            "status": "read",
            "id": exp_id,
            "video_id": row["video_id"],
            "variable": row["variable"],
            "baseline_ctr": baseline,
            "post_ctr": post_ctr,
            "delta_pp": delta,
            "verdict": verdict,
        }
        if verdict == "LIFT":
            result["recipe_line"] = _recipe_appendix_line(row, post_ctr, delta)
        return result
    finally:
        conn.close()


def list_experiments(db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = _connect(db_path)
    try:
        rows = conn.execute(
            "SELECT * FROM swap_experiments ORDER BY id"
        ).fetchall()
        today = _today()
        out = []
        for r in rows:
            d = dict(r)
            d["due"] = (
                r["verdict"] == "PENDING"
                and r["planned_read_date"] is not None
                and r["planned_read_date"] <= today
            )
            out.append(d)
        return out
    finally:
        conn.close()


def experiments_due(db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """PENDING experiments whose planned_read_date has passed — for autopilot."""
    return [e for e in list_experiments(db_path) if e["due"]]


def _recipe_appendix_line(row: sqlite3.Row, post_ctr: float, delta: float) -> str:
    """Paste-ready proven-recipes line for THUMBNAIL-CRAFT-RECIPE.md."""
    return (
        f"| {row['swap_date']} | {row['video_id']} | {row['variable']} | "
        f"{row['old_asset']} → {row['new_asset']} | "
        f"{row['baseline_ctr']:.2f}% → {post_ctr:.2f}% (+{delta:.2f}pp) | "
        f"{row['surface'] or '?'} | {row['notes'] or ''} |"
    )


# ---------------------------------------------------------------------------
# Markdown view (regenerated on every write)
# ---------------------------------------------------------------------------
def _regenerate_md(conn: sqlite3.Connection) -> None:
    rows = conn.execute("SELECT * FROM swap_experiments ORDER BY id DESC").fetchall()
    today = _today()
    lines = [
        "# Swap Ledger",
        "",
        "<!-- AUTO-GENERATED by tools/swap_ledger.py on every write. Do not hand-edit; "
        "edits are overwritten. Source of truth = swap_experiments in keywords.db. -->",
        "",
        f"_Last regenerated: {today}_",
        "",
        "Single-variable before/after swap experiments. One lever per row (thumbnail OR "
        "title, never both) so the CTR delta is attributable. Verdict: LIFT ≥ +0.5pp / "
        "FLAT / DROP ≤ -0.5pp. See `tools/swap_ledger.py`, `tools/SWAP-PROTOCOL.md`.",
        "",
        "| # | Video | Var | Change | Baseline | Post | Δpp | Verdict | Surface | Read by | Notes |",
        "|---|-------|-----|--------|----------|------|------|---------|---------|---------|-------|",
    ]
    for r in rows:
        base = f"{r['baseline_ctr']:.2f}% / {r['baseline_impr'] or '?'}imp" if r["baseline_ctr"] is not None else "?"
        post = f"{r['post_ctr']:.2f}% / {r['post_impr'] or '?'}imp" if r["post_ctr"] is not None else "—"
        delta = f"{r['delta_pp']:+.2f}" if r["delta_pp"] is not None else "—"
        change = f"{r['old_asset'] or '?'} → {r['new_asset'] or '?'}"
        verdict = r["verdict"]
        if verdict == "PENDING" and r["planned_read_date"] and r["planned_read_date"] <= today:
            verdict = "PENDING ⏰ DUE"
        read_by = r["planned_read_date"] or "—"
        lines.append(
            f"| {r['id']} | `{r['video_id']}` | {r['variable']} | {change} | {base} | "
            f"{post} | {delta} | {verdict} | {r['surface'] or '—'} | {read_by} | "
            f"{(r['notes'] or '').replace('|', '/')} |"
        )
    lines.append("")
    _LEDGER_MD.parent.mkdir(parents=True, exist_ok=True)
    _LEDGER_MD.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def _print_list(experiments: List[Dict[str, Any]]) -> None:
    print(f"\n{'=' * 70}")
    print("  SWAP LEDGER")
    print(f"{'=' * 70}")
    if not experiments:
        print("\n  (no experiments yet — open one with `swap_ledger open ...`)\n")
        return
    for e in experiments:
        flag = "  [DUE TO READ]" if e["due"] else ""
        post = (f"{e['post_ctr']:.2f}%" if e["post_ctr"] is not None else "pending")
        base = (f"{e['baseline_ctr']:.2f}%" if e["baseline_ctr"] is not None else "?")
        print(f"\n  #{e['id']} [{e['verdict']}]{flag}  {e['video_id']}  ({e['variable']})")
        print(f"     {base} -> {post}"
              + (f"  (delta {e['delta_pp']:+.2f}pp)" if e["delta_pp"] is not None else "")
              + f"  | surface={e['surface'] or '?'} | read by {e['planned_read_date'] or '?'}")
        if e.get("old_asset") or e.get("new_asset"):
            print(f"     change: {e.get('old_asset','?')} -> {e.get('new_asset','?')}")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Swap Ledger — track single-variable packaging swaps",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd")

    p_open = sub.add_parser("open", help="Record a swap + its baseline")
    p_open.add_argument("--video", required=True, help="YouTube video ID")
    p_open.add_argument("--variable", required=True, choices=VALID_VARIABLES,
                        help="The ONE lever under test")
    p_open.add_argument("--baseline-ctr", type=float, help="Pre-swap CTR %% (e.g. 1.91)")
    p_open.add_argument("--baseline-impr", type=int, help="Pre-swap impressions")
    p_open.add_argument("--surface", default="", choices=VALID_SURFACES,
                        help="Dominant traffic surface (Suggested/Search/Browse)")
    p_open.add_argument("--read-in", default="21d", help="When to read (e.g. 21d, default 21d)")
    p_open.add_argument("--old", default="", help="Old asset description")
    p_open.add_argument("--new", default="", help="New asset description")
    p_open.add_argument("--title", default="", help="Video title (for the ledger view)")
    p_open.add_argument("--note", default="", help="Free-text note")
    p_open.add_argument("--thumbnail-changed", action="store_true",
                        help="Declare the thumbnail ALSO changed (rejected if variable=title)")
    p_open.add_argument("--title-changed", action="store_true",
                        help="Declare the title ALSO changed (rejected if variable=thumbnail)")

    p_read = sub.add_parser("read", help="Read result, compute delta + verdict")
    p_read.add_argument("id", type=int)

    sub.add_parser("list", help="Status board")

    args = parser.parse_args()

    if args.cmd == "open":
        try:
            read_in_days = _parse_read_in(args.read_in)
        except ValueError:
            print(f"ERROR: --read-in must be like '21d' or '21', got '{args.read_in}'")
            sys.exit(1)
        also = "thumbnail" if args.thumbnail_changed else ("title" if args.title_changed else None)
        res = open_experiment(
            video_id=args.video, variable=args.variable,
            baseline_ctr=args.baseline_ctr, baseline_impr=args.baseline_impr,
            surface=args.surface, read_in_days=read_in_days,
            old_asset=args.old, new_asset=args.new, title=args.title,
            note=args.note, also_changed=also,
        )
        if "error" in res:
            print(f"\n  REJECTED: {res['error']}\n")
            sys.exit(1)
        print(f"\n  Opened experiment #{res['id']} — read by {res['planned_read_date']}")
        print(f"  Ledger: {_LEDGER_MD}\n")
        return

    if args.cmd == "read":
        res = read_experiment(args.id)
        if "error" in res:
            print(f"\n  {res['error']}\n")
            sys.exit(1)
        print(f"\n{'=' * 60}")
        print(f"  EXPERIMENT #{res['id']} — {res['verdict']}")
        print(f"{'=' * 60}")
        print(f"  Variable: {res['variable']}")
        print(f"  CTR:      {res['baseline_ctr']:.2f}% -> {res['post_ctr']:.2f}% "
              f"({res['delta_pp']:+.2f}pp)")
        if res.get("recipe_line"):
            print("\n  LIFT confirmed — paste into THUMBNAIL-CRAFT-RECIPE.md proven-recipes:")
            print(f"  {res['recipe_line']}")
        print()
        return

    if args.cmd == "list":
        _print_list(list_experiments())
        return

    parser.print_help()


if __name__ == "__main__":
    main()
