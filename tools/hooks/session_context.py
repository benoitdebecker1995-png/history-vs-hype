"""
SessionStart hook — surfaces the active production state at session start so the
first turn already knows what's in flight, without the user typing /status.

Plain-text stdout is added to Claude's context by Claude Code. Fast, repo-only
reads, fails open (never hangs or errors a session). Wired into
.claude/settings.json SessionStart (matcher: startup).
"""

import glob
import sys
from pathlib import Path


def _lead_num(name: str) -> int:
    head = name.split("-", 1)[0]
    return int(head) if head.isdigit() else -1


def _names(pattern: str, limit: int = 6):
    names = [Path(p.rstrip("/\\")).name for p in glob.glob(pattern)]
    # newest-first by leading project number (so the active ones lead)
    names.sort(key=_lead_num, reverse=True)
    return names[:limit]


def main() -> None:
    try:
        lines = []
        inprod = _names("video-projects/_IN_PRODUCTION/*/")
        ready = _names("video-projects/_READY_TO_FILM/*/")
        if inprod:
            lines.append(f"In production ({len(inprod)} shown): " + ", ".join(inprod))
        if ready:
            lines.append(f"Ready to film: " + ", ".join(ready))

        if lines:
            print("Active video projects (auto-surfaced at session start):")
            for ln in lines:
                print("  - " + ln)
            print("Run /status for the ranked next action; /next for topic ideas.")
    except Exception:
        pass
    sys.exit(0)


if __name__ == "__main__":
    main()
