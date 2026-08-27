"""
SessionStart hook — surfaces the active production state at session start so the
first turn already knows what's in flight, without the user typing /status.

Plain-text stdout is added to the model's context by both Claude Code and Codex,
so one script serves both. Fast, repo-only reads, fails open (never hangs or
errors a session). Wired into `.claude/settings.json` (matcher: startup) and
`.codex/hooks.json` (matcher: startup|resume|clear|compact — Codex adds
`compact`, which fires after a context compaction).
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.video_projects import Stage, VideoProjectRepo

_REPO_ROOT = Path(__file__).resolve().parents[2]

# Manual-export staleness nudges (2026-07-03): these CSV families are pulled BY HAND
# from web UIs — no API/tool can refresh them — and deep analyses (flop autopsy,
# CHANNEL-PERFORMANCE docs) silently degrade when they age. Surface a pull reminder
# at session start once the newest file in a family crosses its threshold.
_CSV_FAMILIES = [
    {
        "label": "YouTube Studio CSV export",
        "max_age_days": 30,
        "matches": lambda p: "vidiq" not in p.name.lower(),
        "pull": "YouTube Studio > Analytics > Advanced mode > Export CSV -> save into channel-data/analytics-exports/",
    },
    {
        "label": "VidIQ CSV export",
        "max_age_days": 45,
        "matches": lambda p: "vidiq" in p.name.lower(),
        "pull": "vidiq.com > Channel Analytics > Export CSV -> save into channel-data/analytics-exports/",
    },
]


def _csv_pull_nudges():
    """One reminder line per CSV family whose newest export is past its threshold."""
    candidates = list((_REPO_ROOT / "channel-data").glob("*.csv")) + list(
        (_REPO_ROOT / "channel-data" / "analytics-exports").glob("*.csv")
    )
    nudges = []
    now = datetime.now()
    for fam in _CSV_FAMILIES:
        fam_files = [p for p in candidates if fam["matches"](p)]
        if not fam_files:
            newest_str, overdue = "never pulled", True
        else:
            newest = max(datetime.fromtimestamp(p.stat().st_mtime) for p in fam_files)
            overdue = now - newest > timedelta(days=fam["max_age_days"])
            newest_str = f"last {newest:%Y-%m-%d}"
        if overdue:
            nudges.append(
                f"{fam['label']} is stale ({newest_str}; threshold {fam['max_age_days']}d). "
                f"Pull: {fam['pull']}"
            )
    return nudges


def _lead_num(name: str) -> int:
    head = name.split("-", 1)[0]
    return int(head) if head.isdigit() else -1


def _names(projects, limit: int = 6):
    names = [p.slug for p in projects]
    # newest-first by leading project number (so the active ones lead)
    names.sort(key=_lead_num, reverse=True)
    return names[:limit]


def main() -> None:
    try:
        repo = VideoProjectRepo()
        lines = []
        inprod = _names(repo.in_stage(Stage.IN_PRODUCTION))
        ready = _names(repo.in_stage(Stage.READY_TO_FILM))
        if inprod:
            lines.append(f"In production ({len(inprod)} shown): " + ", ".join(inprod))
        if ready:
            lines.append(f"Ready to film: " + ", ".join(ready))

        if lines:
            print("Active video projects (auto-surfaced at session start):")
            for ln in lines:
                print("  - " + ln)
            print("Run /status for the ranked next action; /next for topic ideas.")

        try:
            nudges = _csv_pull_nudges()
        except Exception:
            nudges = []
        if nudges:
            print("Manual data pulls due (tell the user — these can NOT be fetched via API):")
            for n in nudges:
                print("  - " + n)
    except Exception:
        pass
    sys.exit(0)


if __name__ == "__main__":
    main()
