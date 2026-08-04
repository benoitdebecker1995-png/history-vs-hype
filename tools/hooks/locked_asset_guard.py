"""
PreToolUse guard — surfaces a warning before an agent edits a protected asset, so a published
record or a deliberately-locked script can't be silently rewritten mid-task.

Dual-harness. The two hosts disagree on both the payload and what a hook may return:

* **Claude Code** — matcher `Edit|Write|NotebookEdit`, payload carries `tool_input.file_path`.
  Returns permissionDecision "ask" (NOT "deny"): protected files DO get legitimate edits
  (e.g. /reconcile rewriting a published project's AUTO block), so this warns + requires
  confirmation rather than hard-blocking. Wired in `.claude/settings.json`.
* **Codex** — matcher `apply_patch`, payload carries `tool_input.command` (the patch envelope;
  there is no `file_path`). Codex parses `permissionDecision: "ask"` but does not support it — it
  marks the hook run failed and proceeds — so there the guard returns `additionalContext`, an
  advisory the model sees without a false block. Wired in `.codex/hooks.json`.

`paths_from_payload` and `evaluate` are pure — the tests drive them directly.
Fails open (exit 0, no output) on any error: a guard must never break a session.
"""

import json
import re
import sys
from pathlib import Path

LOCK_MARKERS = (
    "DRAFT-LOCKED", "STATUS: LOCKED", "<!-- LOCKED", "[LOCKED]",
    "SCRIPT LOCKED", "LOCKED - DO NOT EDIT", "LOCKED — DO NOT EDIT",
)

# Codex apply_patch envelope: `*** Add File: path`, `*** Update File: path`, `*** Delete File: path`
_PATCH_TARGET = re.compile(r"^\*\*\*\s+(?:Add|Update|Delete)\s+File:\s*(.+?)\s*$", re.M)


def paths_from_payload(data: dict) -> list:
    """Every file path this tool call would touch, whichever host sent it."""
    tool_input = data.get("tool_input") or {}

    fp = tool_input.get("file_path")
    if fp:
        return [str(fp)]

    # Codex: apply_patch (and its Edit/Write matcher aliases) send the patch text as `command`.
    command = tool_input.get("command")
    if isinstance(command, str) and command:
        return [m.group(1) for m in _PATCH_TARGET.finditer(command)]

    return []


def reasons_for(path: str) -> list:
    """Why `path` is protected. Empty list = not protected."""
    norm = str(path).replace("\\", "/")
    reasons = []

    # 1. Published archive — the immutable record of a shipped video.
    if "_ARCHIVED/published/" in norm:
        reasons.append("under _ARCHIVED/published/ (the record of a shipped video)")

    # 2. Final teleprompter export — frozen for filming.
    if "FINAL-SCRIPT-TELEPROMPTER" in norm.upper():
        reasons.append("the FINAL teleprompter export (frozen for filming)")

    # 3. Explicit LOCKED marker in the file head (text files only).
    try:
        f = Path(path)
        if f.exists() and f.suffix.lower() in (".md", ".txt"):
            head = f.read_text(encoding="utf-8", errors="ignore")[:2000].upper()
            if any(m in head for m in LOCK_MARKERS):
                reasons.append("carries a LOCKED marker (deliberately frozen)")
    except OSError:
        pass

    # dedupe, preserve order
    seen, ordered = set(), []
    for r in reasons:
        if r not in seen:
            seen.add(r)
            ordered.append(r)
    return ordered


def evaluate(data: dict):
    """The hook response for `data`, or None when nothing is protected."""
    paths = paths_from_payload(data)
    findings = []
    for path in paths:
        found = reasons_for(path)
        if found:
            findings.append((path, found))

    if not findings:
        return None

    # A single-target call can say "this file"; a multi-target patch has to name which one.
    if len(paths) == 1:
        body = "this file is " + "; ".join(findings[0][1])
    else:
        body = "; ".join(f"{p} is {', '.join(f)}" for p, f in findings)

    reason = (
        "Protected asset: " + body + ". "
        "Confirm the edit is intentional (e.g. a /reconcile AUTO-block update, "
        "a postmortem, or an explicit re-open) — not an accidental rewrite."
    )

    # Codex reports the canonical tool name `apply_patch` even under the Edit/Write matcher
    # aliases, and rejects permissionDecision "ask". Advise there; ask on Claude Code.
    if data.get("tool_name") == "apply_patch":
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "additionalContext": reason,
            }
        }

    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": reason,
        }
    }


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    try:
        out = evaluate(data)
    except Exception:
        sys.exit(0)

    if out:
        print(json.dumps(out))
    sys.exit(0)


if __name__ == "__main__":
    main()
