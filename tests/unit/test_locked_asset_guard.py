"""Behavioral pins for the dual-harness PreToolUse guard (tools/hooks/locked_asset_guard.py).

The guard runs under two hosts that disagree on both the payload and the allowed response:

* Claude Code sends `tool_input.file_path` and accepts `permissionDecision: "ask"`.
* Codex sends `tool_input.command` (the apply_patch envelope) and *rejects* "ask" — it parses the
  value, marks the hook run failed, and proceeds with the call. There the guard must return
  `additionalContext` instead.

Origin: 2026-08-04 Codex port. Read against `tool_input.file_path` only, the guard was a silent
no-op on Codex — it never fired and never errored. These pins lock both payload shapes.
"""

import json
import subprocess
import sys
from pathlib import Path

from tools.hooks.locked_asset_guard import evaluate, paths_from_payload, reasons_for

REPO_ROOT = Path(__file__).resolve().parents[2]
GUARD = REPO_ROOT / "tools" / "hooks" / "locked_asset_guard.py"

PUBLISHED = "video-projects/_ARCHIVED/published/1-somaliland-2025/PROJECT-STATUS.md"


def _claude(file_path, tool_name="Edit"):
    return {"tool_name": tool_name, "tool_input": {"file_path": file_path}}


def _codex(*targets, verb="Update"):
    body = "\n".join(f"*** {verb} File: {t}" for t in targets)
    command = f"*** Begin Patch\n{body}\n@@\n-old\n+new\n*** End Patch"
    return {"tool_name": "apply_patch", "tool_input": {"command": command}}


class TestPathExtraction:
    def test_claude_file_path(self):
        assert paths_from_payload(_claude("a/b.md")) == ["a/b.md"]

    def test_codex_patch_envelope(self):
        assert paths_from_payload(_codex("a/b.md")) == ["a/b.md"]

    def test_codex_multi_file_patch(self):
        payload = _codex("a/b.md", "c/d.md")
        assert paths_from_payload(payload) == ["a/b.md", "c/d.md"]

    def test_codex_add_and_delete_verbs(self):
        assert paths_from_payload(_codex("new.md", verb="Add")) == ["new.md"]
        assert paths_from_payload(_codex("gone.md", verb="Delete")) == ["gone.md"]

    def test_empty_payload_yields_no_paths(self):
        assert paths_from_payload({}) == []
        assert paths_from_payload({"tool_input": {}}) == []
        assert paths_from_payload({"tool_input": {"command": ""}}) == []

    def test_bash_command_without_patch_envelope_yields_no_paths(self):
        payload = {"tool_name": "Bash", "tool_input": {"command": "python -m pytest"}}
        assert paths_from_payload(payload) == []


class TestProtection:
    def test_published_archive_is_protected(self):
        assert reasons_for(PUBLISHED)

    def test_windows_separators_still_match(self):
        assert reasons_for(PUBLISHED.replace("/", "\\"))

    def test_teleprompter_export_is_protected(self):
        assert reasons_for("video-projects/_IN_PRODUCTION/x/FINAL-SCRIPT-TELEPROMPTER.md")

    def test_ordinary_file_is_not_protected(self):
        assert reasons_for("tools/title_scorer.py") == []

    def test_lock_marker_in_file_head(self, tmp_path):
        f = tmp_path / "SCRIPT.md"
        f.write_text("# Draft\n<!-- LOCKED -->\nbody\n", encoding="utf-8")
        assert any("LOCKED marker" in r for r in reasons_for(str(f)))

    def test_lock_marker_ignored_in_non_text_file(self, tmp_path):
        f = tmp_path / "notes.bin"
        f.write_text("STATUS: LOCKED", encoding="utf-8")
        assert reasons_for(str(f)) == []

    def test_missing_file_does_not_raise(self, tmp_path):
        assert reasons_for(str(tmp_path / "does-not-exist.md")) == []


class TestResponseShape:
    def test_claude_gets_ask(self):
        out = evaluate(_claude(PUBLISHED))
        hook = out["hookSpecificOutput"]
        assert hook["permissionDecision"] == "ask"
        assert "_ARCHIVED/published/" in hook["permissionDecisionReason"]

    def test_codex_gets_additional_context_not_ask(self):
        out = evaluate(_codex(PUBLISHED))
        hook = out["hookSpecificOutput"]
        # "ask" is parsed-but-unsupported on Codex; returning it fails the hook run.
        assert "permissionDecision" not in hook
        assert "_ARCHIVED/published/" in hook["additionalContext"]

    def test_both_hosts_name_the_event(self):
        for payload in (_claude(PUBLISHED), _codex(PUBLISHED)):
            assert evaluate(payload)["hookSpecificOutput"]["hookEventName"] == "PreToolUse"

    def test_unprotected_edit_returns_none(self):
        assert evaluate(_claude("tools/title_scorer.py")) is None
        assert evaluate(_codex("tools/title_scorer.py")) is None

    def test_multi_file_patch_reports_every_protected_target(self):
        out = evaluate(_codex(PUBLISHED, "tools/title_scorer.py"))
        context = out["hookSpecificOutput"]["additionalContext"]
        assert PUBLISHED in context
        assert "title_scorer" not in context


class TestProcessContract:
    """The hook is run as a subprocess by both hosts; it must never break a session."""

    def _run(self, payload):
        return subprocess.run(
            [sys.executable, str(GUARD)],
            input=payload,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env={"PYTHONIOENCODING": "utf-8", "PATH": ""},
            cwd=str(REPO_ROOT),
        )

    def test_protected_edit_emits_json_and_exits_zero(self):
        r = self._run(json.dumps(_claude(PUBLISHED)))
        assert r.returncode == 0
        assert json.loads(r.stdout)["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_unprotected_edit_is_silent(self):
        r = self._run(json.dumps(_claude("tools/title_scorer.py")))
        assert r.returncode == 0
        assert r.stdout.strip() == ""

    def test_malformed_stdin_fails_open(self):
        r = self._run("not json at all")
        assert r.returncode == 0
        assert r.stdout.strip() == ""
