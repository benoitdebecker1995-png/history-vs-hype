"""
UserPromptSubmit hook — makes CLAUDE.md's MANDATORY utterance triggers deterministic.

CLAUDE.md marks two behaviours MANDATORY ("the utterance IS the write trigger"),
and `extending-safely` makes a third a standing hard rule. All three depended on
the model noticing the phrasing mid-conversation. This matches them at prompt
time instead, so the reminder is in context before the turn starts.

It replaces a backstop that never existed: `automation-ops` described a
user-global Stop hook `extract-learnings.js` feeding `~/.claude/wiki/_queue/`,
and `extending-safely` told every session "the Stop hook is only the backstop".
Verified absent 2026-07-31 — no script, no wiki, no /wiki-ingest. Matching
correction language at prompt time is both cheaper than a Stop hook (which fires
every turn) and earlier (before the work happens, not after).

Contract, same as session_context.py: read stdin, print plain text to stdout for
Claude's context, ALWAYS exit 0. This hook must never block a prompt — a false
positive should cost a sentence of context, never the user's turn.

Wired into .claude/settings.json UserPromptSubmit.
"""

import json
import re
import sys

# Each: (compiled pattern, reminder). Patterns stay narrow — a false positive
# spends context and, worse, trains the user to ignore the reminders.
_TRIGGERS = [
    (
        re.compile(
            # The adverb slot is an allowlist, not \w+, so negated forms
            # ("I never uploaded", "I haven't published") do not fire.
            r"\b(i\s+(just\s+|already\s+|finally\s+|now\s+)?"
            r"(uploaded|released|published|posted)"
            r"|(is|went)\s+live"
            r"|went\s+up)\b",
            re.IGNORECASE,
        ),
        "TRIGGER — publish declared. CLAUDE.md: run `/reconcile <slug>` NOW. Do not just look the "
        "video up, and do not assume project files are current — the utterance IS the write "
        "trigger. If the slug is ambiguous across folders, ask once, then proceed.",
    ),
    (
        re.compile(
            r"\b(script\s+lock(ed)?|lock\s+it|t1\s+passed"
            r"|read[-\s]?aloud\s+passed)\b",
            re.IGNORECASE,
        ),
        "TRIGGER — script lock declared. CLAUDE.md: run the post-lock delta-mine NOW, while the "
        "deltas are fresh: (1) consolidate read-aloud notes, version diffs and session corrections "
        "into channel-data/calibration/CALIBRATION-CORPUS.md (axis-tagged, tiered); (2) append new "
        "contradictions to INTERVIEW-AGENDA.md; (3) record passes-to-lock in EVAL-BASELINE.md.",
    ),
    (
        re.compile(
            r"(^|[.!?]\s+)(no[,.\s]|nope\b|wrong\b|that'?s not\b|don'?t\b|stop\b"
            r"|never\b|actually,?\s)",
            re.IGNORECASE,
        ),
        "POSSIBLE CORRECTION — if the user is correcting you, capture the rule immediately in "
        "video-projects/_CORRECTIONS-LOG.md (and the user-memory store if it is a standing "
        "preference). `extending-safely`: live capture is a standing hard rule, not 'noted'. "
        "Ignore this line if the message was not a correction.",
    ),
]


def check(prompt: str) -> list:
    """Reminders triggered by `prompt`. Pure — the tests drive this directly."""
    return [msg for pattern, msg in _TRIGGERS if pattern.search(prompt or "")]


def main() -> int:
    try:
        raw = sys.stdin.read()
        prompt = json.loads(raw).get("prompt", "") if raw.strip() else ""
    except (ValueError, OSError):
        # Fail open and silent. A hook that cannot read its input must not
        # editorialise into the user's context.
        return 0

    hits = check(prompt)
    if hits:
        print("Utterance triggers matched (tools/hooks/utterance_triggers.py):")
        for msg in hits:
            print("  - " + msg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
