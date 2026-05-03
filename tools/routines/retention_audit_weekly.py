"""
Weekly retention audit.

Pulls the videos table from analytics.db, finds anything published in the last
30 days, fetches the retention curve for each, and flags new dropout cliffs
(any 30-second window with relative retention loss above DROP_THRESHOLD).

Compares against the previous week's snapshot so a steady cliff that was
already known doesn't keep firing alerts — only NEW cliffs are flagged.

CLI:
    python -m tools.routines.retention_audit_weekly
    python -m tools.routines.retention_audit_weekly --days 14 --threshold 0.04
"""

import argparse
import json
import sqlite3
import sys
from datetime import datetime, date, timedelta
from pathlib import Path

from tools.youtube_analytics.retention import get_retention_data

REPO_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = REPO_ROOT / "tools" / "youtube_analytics" / "analytics.db"
AUDIT_DIR = REPO_ROOT / "channel-data" / "retention-audits"
AUDIT_DIR.mkdir(parents=True, exist_ok=True)

DROP_THRESHOLD = 0.10
WINDOW_FRACTION = 0.03


def recent_videos(days: int) -> list[dict]:
    if not DB_PATH.exists():
        return []
    cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        """
        SELECT video_id, title, published_at, duration_seconds, views
        FROM videos
        WHERE published_at >= ?
        ORDER BY published_at DESC
        """,
        (cutoff,),
    ).fetchall()
    conn.close()
    return [
        {
            "video_id": r[0],
            "title": r[1],
            "published_at": r[2],
            "duration_seconds": r[3],
            "views": r[4],
        }
        for r in rows
    ]


def find_cliffs(data_points: list[dict], threshold: float) -> list[dict]:
    """Find windows where relative retention drops by `threshold` or more."""
    if not data_points or len(data_points) < 2:
        return []
    cliffs = []
    for i in range(1, len(data_points)):
        prev = data_points[i - 1]
        cur = data_points[i]
        prev_retention = prev.get("retention", prev.get("relative", 0))
        cur_retention = cur.get("retention", cur.get("relative", 0))
        if prev_retention <= 0:
            continue
        delta = (cur_retention - prev_retention) / prev_retention
        if delta <= -threshold:
            cliffs.append({
                "from_ratio": round(prev.get("position", 0), 3),
                "to_ratio": round(cur.get("position", 0), 3),
                "drop_pct": round(delta * 100, 1),
            })
    return cliffs


def previous_audit_cliffs(video_id: str) -> list[dict]:
    audits = sorted(AUDIT_DIR.glob("*.json"))
    if not audits:
        return []
    prev = json.loads(audits[-1].read_text(encoding="utf-8"))
    for v in prev.get("videos", []):
        if v["video_id"] == video_id:
            return v.get("cliffs", [])
    return []


def is_new_cliff(cliff: dict, prior: list[dict]) -> bool:
    for p in prior:
        if abs(p["from_ratio"] - cliff["from_ratio"]) < 0.02:
            return False
    return True


def render_report(today_str: str, audited: list[dict]) -> str:
    new_cliff_count = sum(
        len([c for c in v["cliffs"] if c.get("is_new")])
        for v in audited
    )
    lines = [
        f"# Retention Audit — {today_str}",
        "",
        f"**Videos audited:** {len(audited)}",
        f"**New dropout cliffs:** {new_cliff_count}",
        "",
    ]
    for v in audited:
        lines.append(f"## {v['title']}")
        lines.append(f"`{v['video_id']}` — published {v['published_at'][:10]} — {v['views']} views")
        lines.append("")
        if v.get("error"):
            lines.append(f"_Error fetching retention: {v['error']}_")
            lines.append("")
            continue
        if not v["cliffs"]:
            lines.append("No significant cliffs detected.")
            lines.append("")
            continue
        lines.append("| From % | To % | Drop | New? |")
        lines.append("|---|---|---|---|")
        for c in v["cliffs"]:
            new_marker = "**NEW**" if c.get("is_new") else "(known)"
            from_pct = int(c["from_ratio"] * 100)
            to_pct = int(c["to_ratio"] * 100)
            lines.append(
                f"| {from_pct}% | {to_pct}% | {c['drop_pct']:.1f}% | {new_marker} |"
            )
        lines.append("")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--threshold", type=float, default=DROP_THRESHOLD)
    args = parser.parse_args()

    videos = recent_videos(args.days)
    if not videos:
        print(f"No videos published in the last {args.days} days.", file=sys.stderr)
        return 0

    today = date.today().isoformat()
    audited = []
    for v in videos:
        print(f"Fetching {v['video_id']} — {v['title'][:50]}...")
        try:
            data = get_retention_data(v["video_id"])
            cliffs = find_cliffs(data.get("data_points", []), args.threshold)
            prior = previous_audit_cliffs(v["video_id"])
            for c in cliffs:
                c["is_new"] = is_new_cliff(c, prior)
            audited.append({**v, "cliffs": cliffs})
        except Exception as e:
            audited.append({**v, "cliffs": [], "error": f"{type(e).__name__}: {e}"})

    snapshot = {
        "date": today,
        "fetched_at": datetime.now().isoformat(),
        "threshold": args.threshold,
        "videos": audited,
    }
    (AUDIT_DIR / f"{today}.json").write_text(
        json.dumps(snapshot, indent=2), encoding="utf-8"
    )
    report = render_report(today, audited)
    report_path = AUDIT_DIR / f"{today}.md"
    report_path.write_text(report, encoding="utf-8")

    print(f"Report: {report_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
