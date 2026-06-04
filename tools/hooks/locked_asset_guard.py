"""
PreToolUse guard — surfaces a confirmation prompt before Claude edits a
protected asset, so a published record or a deliberately-locked script can't be
silently rewritten mid-task.

Uses permissionDecision "ask" (NOT "deny"): protected files DO get legitimate
edits (e.g. /reconcile rewriting a published project's AUTO block), so this
warns + requires confirmation rather than hard-blocking. Wired into
.claude/settings.json PreToolUse for Edit|Write|NotebookEdit.

Reads the hook JSON on stdin; emits a hookSpecificOutput JSON on a match.
Fails open (exit 0, no output) on any error — a guard must never break a session.
"""

import json
import sys
from pathlib import Path

LOCK_MARKERS = (
    "DRAFT-LOCKED", "STATUS: LOCKED", "<!-- LOCKED", "[LOCKED]",
    "SCRIPT LOCKED", "LOCKED - DO NOT EDIT", "LOCKED — DO NOT EDIT",
)


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    fp = (data.get("tool_input") or {}).get("file_path")
    if not fp:
        sys.exit(0)

    norm = str(fp).replace("\\", "/")
    reasons = []

    # 1. Published archive — the immutable record of a shipped video.
    if "_ARCHIVED/published/" in norm:
        reasons.append("under _ARCHIVED/published/ (the record of a shipped video)")

    # 2. Final teleprompter export — frozen for filming.
    if "FINAL-SCRIPT-TELEPROMPTER" in norm.upper():
        reasons.append("the FINAL teleprompter export (frozen for filming)")

    # 3. Explicit LOCKED marker in the file head (text files only).
    try:
        f = Path(fp)
        if f.exists() and f.suffix.lower() in (".md", ".txt"):
            head = f.read_text(encoding="utf-8", errors="ignore")[:2000].upper()
            if any(m in head for m in LOCK_MARKERS):
                reasons.append("carries a LOCKED marker (deliberately frozen)")
    except Exception:
        pass

    if not reasons:
        sys.exit(0)

    # dedupe, preserve order
    seen, ordered = set(), []
    for r in reasons:
        if r not in seen:
            seen.add(r)
            ordered.append(r)

    reason = (
        "Protected asset: this file is " + "; ".join(ordered) + ". "
        "Confirm the edit is intentional (e.g. a /reconcile AUTO-block update, "
        "a postmortem, or an explicit re-open) — not an accidental rewrite."
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


if __name__ == "__main__":
    main()
