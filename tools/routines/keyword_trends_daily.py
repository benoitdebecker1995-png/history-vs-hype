"""
Daily Google Trends sweep for tracked keywords.

Reads channel-data/tracked-keywords.txt, queries Google Trends for each,
compares against the previous run's snapshot, and writes a daily report
flagging any keyword that moved more than ALERT_THRESHOLD percent.

CLI:
    python -m tools.routines.keyword_trends_daily
    python -m tools.routines.keyword_trends_daily --threshold 30
"""

import argparse
import json
import sys
from datetime import datetime, date
from pathlib import Path

from tools.discovery.trends import TrendsClient

REPO_ROOT = Path(__file__).resolve().parents[2]
KEYWORDS_FILE = REPO_ROOT / "channel-data" / "tracked-keywords.txt"
SNAPSHOT_DIR = REPO_ROOT / "channel-data" / "keyword-tracking"
SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

ALERT_THRESHOLD = 20.0


def load_keywords(path: Path) -> list[str]:
    if not path.exists():
        return []
    keywords = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            keywords.append(line)
    return keywords


def latest_snapshot() -> dict | None:
    snapshots = sorted(SNAPSHOT_DIR.glob("*.json"))
    if not snapshots:
        return None
    return json.loads(snapshots[-1].read_text(encoding="utf-8"))


def fetch_all(keywords: list[str], region: str = "US") -> dict:
    client = TrendsClient(region=region)
    results = {}
    for kw in keywords:
        result = client.get_interest_over_time(kw, hours=168)
        results[kw] = result
    return results


def diff_against_previous(today: dict, previous: dict | None, threshold: float) -> list[dict]:
    if not previous:
        return []
    alerts = []
    prev_map = previous.get("keywords", {})
    for kw, current in today.items():
        if "error" in current:
            continue
        prev = prev_map.get(kw)
        if not prev or "error" in prev:
            continue
        cur_interest = current.get("interest", 0)
        prev_interest = prev.get("interest", 0)
        if prev_interest == 0:
            continue
        delta = ((cur_interest - prev_interest) / prev_interest) * 100
        if abs(delta) >= threshold:
            alerts.append({
                "keyword": kw,
                "previous": prev_interest,
                "current": cur_interest,
                "delta_pct": round(delta, 1),
                "direction": "up" if delta > 0 else "down",
            })
    return alerts


def render_report(today_str: str, results: dict, alerts: list[dict]) -> str:
    lines = [
        f"# Keyword Trends — {today_str}",
        "",
        f"**Tracked keywords:** {len(results)}",
        f"**Alerts (≥{int(ALERT_THRESHOLD)}% move):** {len(alerts)}",
        "",
    ]
    if alerts:
        lines.append("## Alerts")
        lines.append("")
        lines.append("| Keyword | Previous | Current | Δ % | Direction |")
        lines.append("|---|---|---|---|---|")
        for a in alerts:
            arrow = "↑" if a["direction"] == "up" else "↓"
            lines.append(
                f"| {a['keyword']} | {a['previous']} | {a['current']} | "
                f"{a['delta_pct']:+.1f}% | {arrow} |"
            )
        lines.append("")
    else:
        lines.append("## No alerts today")
        lines.append("")

    lines.append("## Full snapshot")
    lines.append("")
    lines.append("| Keyword | Interest | Δ vs last 7d | Direction |")
    lines.append("|---|---|---|---|")
    for kw, r in results.items():
        if "error" in r:
            lines.append(f"| {kw} | — | — | error: {r['error']} |")
        else:
            lines.append(
                f"| {kw} | {r.get('interest', 0)} | "
                f"{r.get('percent_change', 0):+.1f}% | {r.get('direction', '?')} |"
            )
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--threshold", type=float, default=ALERT_THRESHOLD)
    parser.add_argument("--region", default="US")
    args = parser.parse_args()

    keywords = load_keywords(KEYWORDS_FILE)
    if not keywords:
        print(f"No keywords found in {KEYWORDS_FILE}", file=sys.stderr)
        return 1

    today = date.today().isoformat()
    print(f"Querying {len(keywords)} keywords...")
    results = fetch_all(keywords, region=args.region)

    previous = latest_snapshot()
    alerts = diff_against_previous(results, previous, args.threshold)

    snapshot = {
        "date": today,
        "fetched_at": datetime.now().isoformat(),
        "region": args.region,
        "keywords": results,
    }
    (SNAPSHOT_DIR / f"{today}.json").write_text(
        json.dumps(snapshot, indent=2), encoding="utf-8"
    )

    report = render_report(today, results, alerts)
    report_path = SNAPSHOT_DIR / f"{today}.md"
    report_path.write_text(report, encoding="utf-8")

    print(f"Report: {report_path}")
    print(f"Alerts: {len(alerts)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
