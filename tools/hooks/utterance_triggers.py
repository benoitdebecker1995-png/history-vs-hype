"""Prompt-time reminders for conversational state changes that must be recorded."""

import json
import re
import sys


_TRIGGERS = [
    (
        re.compile(
            r"\b(i\s+(?:just\s+|already\s+|finally\s+|now\s+)?"
            r"(?:uploaded|released|published|posted)|(?:is|went)\s+live|went\s+up)\b",
            re.I,
        ),
        "Publication was declared. Infer the current project, reconcile publication state using "
        "the existing deterministic reconciler, record the effective package version, and create "
        "a published milestone snapshot. Do not ask the creator for a command.",
    ),
    (
        re.compile(r"\b(script\s+lock(?:ed)?|lock\s+it|t1\s+passed|read[-\s]?aloud\s+passed)\b", re.I),
        "Script lock was declared. Create a non-Git active-state snapshot now. Treat spontaneous "
        "read-through corrections as voice evidence, but do not expand a default voice doctrine.",
    ),
    (
        re.compile(
            r"\b(use|choose|lock|publish|go with|switch to|change to)\b.{0,40}"
            r"\b(title|thumbnail|package)\b|\b(title|thumbnail)\b.{0,30}\b(is final|is locked)\b",
            re.I,
        ),
        "A package choice may have been made. If so, record the exact title or hashed thumbnail "
        "with its effective time through package history; do not merely update prose.",
    ),
    (
        re.compile(
            r"\b(?:accept|accepted|go with|let'?s do|use)\b.{0,60}"
            r"\b(?:recommendation|approach|plan|strategy)\b|"
            r"\b(?:recommendation|approach|plan|strategy)\b.{0,40}\b(?:is final|is accepted)\b",
            re.I,
        ),
        "A material recommendation may have been accepted. If it changes topic, package, workflow, "
        "research or business direction, record its rationale, predicted mechanism, expected "
        "observation and evidence limitations before an outcome is known. Ignore ordinary micro-edits.",
    ),
]


def check(prompt: str) -> list[str]:
    return [message for pattern, message in _TRIGGERS if pattern.search(prompt or "")]


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    try:
        raw = sys.stdin.read()
        prompt = json.loads(raw).get("prompt", "") if raw.strip() else ""
    except (ValueError, OSError):
        return 0
    for message in check(prompt):
        print(message)
    return 0


if __name__ == "__main__":
    sys.exit(main())
