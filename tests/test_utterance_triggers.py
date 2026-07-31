"""Tests for the UserPromptSubmit utterance-trigger hook.

Two properties matter more than coverage here:
  1. It never blocks a prompt. A false positive must cost a sentence of context,
     never the user's turn.
  2. Patterns stay narrow. A reminder that fires on ordinary conversation trains
     the user to ignore all of them, which is worse than having no hook.
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

from tools.hooks.utterance_triggers import check, main

REPO_ROOT = Path(__file__).resolve().parents[1]
HOOK = REPO_ROOT / "tools" / "hooks" / "utterance_triggers.py"


# --------------------------------------------------------------- publish ---

@pytest.mark.parametrize("prompt", [
    "I uploaded volhynia",
    "i just published the enigma video",
    "Bir Tawil is live",
    "the kurdistan one went up this morning",
    "I released it yesterday",
    # Real phrasing from 2026-07-30 ("i already made nato one inch video") --
    # the first pattern only allowed "just" in the adverb slot and missed it.
    "I already uploaded volhynia",
    "I finally published the bengal one",
])
def test_publish_utterances_fire_reconcile(prompt):
    hits = check(prompt)
    assert any("/reconcile" in h for h in hits), f"no reconcile reminder for {prompt!r}"


@pytest.mark.parametrize("prompt", [
    "can you look up when volhynia was published",
    "what did we upload last month",
    "the upload schedule is Monday to Thursday",
    # Negated forms must not fire — this is why the adverb slot is an allowlist
    # rather than \w+, which would have matched all three of these.
    "I never uploaded that one",
    "I haven't published it yet",
    "I should have released it sooner",
])
def test_talking_about_publishing_does_not_fire(prompt):
    """Discussing a publish is not declaring one. The trigger is the utterance,
    so it must not fire on questions about past uploads."""
    assert not any("/reconcile" in h for h in check(prompt)), f"false positive on {prompt!r}"


# ------------------------------------------------------------ script lock ---

@pytest.mark.parametrize("prompt", [
    "script locked",
    "lock it",
    "T1 passed",
    "read-aloud passed top to bottom",
])
def test_lock_utterances_fire_delta_mine(prompt):
    hits = check(prompt)
    assert any("CALIBRATION-CORPUS" in h for h in hits), f"no delta-mine reminder for {prompt!r}"


def test_lock_reminder_names_all_three_targets():
    """The mine is three writes; a reminder naming one would half-do it."""
    hit = next(h for h in check("script locked") if "CALIBRATION-CORPUS" in h)
    for target in ("CALIBRATION-CORPUS", "INTERVIEW-AGENDA", "EVAL-BASELINE"):
        assert target in hit


# -------------------------------------------------------------- correction ---

@pytest.mark.parametrize("prompt", [
    "no, that's not what I meant",
    "wrong. the penalty is graded",
    "don't use em dashes there",
    "Actually, the turn should come earlier",
])
def test_correction_shapes_fire_capture(prompt):
    assert any("_CORRECTIONS-LOG" in h for h in check(prompt))


@pytest.mark.parametrize("prompt", [
    "there is no data for that video",
    "I know nothing about the 1923 treaty",
    "the stopword list needs updating",
    "we don't have the source yet",
])
def test_correction_pattern_is_anchored_not_substring(prompt):
    """Anchored to sentence start so 'no'/'don't'/'stop' inside ordinary prose
    do not fire. These are the cases that would make the hook noise."""
    assert not any("_CORRECTIONS-LOG" in h for h in check(prompt)), f"false positive on {prompt!r}"


# ------------------------------------------------------------------ shape ---

def test_ordinary_prompt_produces_nothing():
    assert check("run the test suite and show me the slowest tests") == []


def test_empty_and_none_are_safe():
    assert check("") == []
    assert check(None) == []


def test_multiple_triggers_can_fire_together():
    hits = check("no, I already uploaded volhynia")
    assert len(hits) == 2


# ------------------------------------------------------------- never block ---

def test_main_exits_zero_on_malformed_stdin(monkeypatch, capsys):
    """Fail open AND silent: a hook that cannot read its input must not
    editorialise into the user's context."""
    monkeypatch.setattr(sys, "stdin", type("S", (), {"read": staticmethod(lambda: "not json")})())

    assert main() == 0
    assert capsys.readouterr().out == ""


def test_hook_runs_as_a_subprocess_and_exits_zero():
    """End-to-end through the real CLI path Claude Code uses."""
    proc = subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps({"prompt": "I uploaded volhynia"}),
        capture_output=True, text=True, cwd=str(REPO_ROOT), timeout=60,
    )

    assert proc.returncode == 0, proc.stderr
    assert "/reconcile" in proc.stdout


def test_hook_exits_zero_even_with_empty_stdin():
    proc = subprocess.run(
        [sys.executable, str(HOOK)],
        input="", capture_output=True, text=True, cwd=str(REPO_ROOT), timeout=60,
    )

    assert proc.returncode == 0
    assert proc.stdout.strip() == ""
