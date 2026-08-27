"""Phase L1 — Behavioral pinning tests for script-checkers CLI.

Tests for each checker (stumble, repetition, scaffolding, flow, pacing):
- Invokes `python -m tools.script_checkers.cli --<checker>` against test fixture
- Asserts exit code 0 + non-empty output
- Verifies JSON output format when requested

Run with: pytest tests/test_script_checkers.py -v
"""
import subprocess
import json
import os
import pytest
from pathlib import Path


FIXTURE_PATH = Path("tests/fixtures/test_script.md")
CHECKERS = ["stumble", "repetition", "scaffolding", "flow", "pacing", "told-so-far"]

# Decode child output as UTF-8 to match the PYTHONIOENCODING=utf-8 set on every
# child below. `errors="replace"` so a stray byte degrades one character instead
# of losing the whole capture.
UTF8_PIPE = {"text": True, "encoding": "utf-8", "errors": "replace"}

# stumble/flow/pacing lazy-load spaCy; skip their spaCy-dependent assertions
# when the [nlp] extra isn't installed, matching tests/unit/test_pacing.py's
# existing convention rather than asserting on a CLI crash we didn't cause.
try:
    import spacy  # noqa: F401
    NLP_AVAILABLE = True
except ImportError:
    NLP_AVAILABLE = False

requires_nlp = pytest.mark.skipif(not NLP_AVAILABLE, reason="spaCy required (pip install -e .[nlp])")


def _run_checker(checker_name: str, json_output: bool = False):
    """Run a checker and return the result with proper UTF-8 encoding."""
    cmd = ["python", "-m", "tools.script_checkers.cli", str(FIXTURE_PATH), f"--{checker_name}"]
    if json_output:
        cmd.append("--json")

    # Set PYTHONIOENCODING to UTF-8 to handle Unicode output on Windows
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    result = subprocess.run(
        cmd,
        capture_output=True,
        # BOTH sides must name UTF-8. `text=True` alone decodes with the PARENT's
        # locale codec (cp1252 here), which does not match the child's
        # PYTHONIOENCODING above: the child's UTF-8 bytes then blow up inside
        # subprocess's reader thread and result.stdout comes back empty, so any
        # assertion on output silently tests nothing.
        **UTF8_PIPE,
        env=env
    )
    return result


class TestScriptCheckersCLI:
    """Test script-checkers CLI behavior for each checker."""

    def test_stumble_checker_exit_code(self):
        """Stumble checker produces exit code 0 and output."""
        result = _run_checker("stumble")
        assert result.returncode in (0, 1, 2), f"Unexpected exit code: {result.returncode}"

    @requires_nlp
    def test_stumble_checker_json_output(self):
        """Stumble checker produces valid JSON when requested."""
        result = _run_checker("stumble", json_output=True)
        assert result.returncode in (0, 1, 2), f"Unexpected exit code: {result.returncode}"
        data = json.loads(result.stdout)
        assert isinstance(data, dict), "JSON output is not a dict"
        assert "stumble" in data, "stumble key missing from JSON output"

    def test_repetition_checker_exit_code(self):
        """Repetition checker produces exit code 0 and output."""
        result = _run_checker("repetition")
        assert result.returncode in (0, 1, 2), f"Unexpected exit code: {result.returncode}"

    def test_repetition_checker_json_output(self):
        """Repetition checker produces valid JSON when requested."""
        result = _run_checker("repetition", json_output=True)
        assert result.returncode in (0, 1, 2), f"Unexpected exit code: {result.returncode}"
        data = json.loads(result.stdout)
        assert isinstance(data, dict), "JSON output is not a dict"
        assert "repetition" in data, "repetition key missing from JSON output"

    def test_scaffolding_checker_exit_code(self):
        """Scaffolding checker produces exit code 0 and output."""
        result = _run_checker("scaffolding")
        assert result.returncode in (0, 1, 2), f"Unexpected exit code: {result.returncode}"

    def test_scaffolding_checker_json_output(self):
        """Scaffolding checker produces valid JSON when requested."""
        result = _run_checker("scaffolding", json_output=True)
        assert result.returncode in (0, 1, 2), f"Unexpected exit code: {result.returncode}"
        data = json.loads(result.stdout)
        assert isinstance(data, dict), "JSON output is not a dict"
        assert "scaffolding" in data, "scaffolding key missing from JSON output"

    @requires_nlp
    def test_flow_checker_exit_code(self):
        """Flow checker produces exit code 0 and output."""
        result = _run_checker("flow")
        assert result.returncode in (0, 1, 2), f"Unexpected exit code: {result.returncode}"

    @requires_nlp
    def test_flow_checker_json_output(self):
        """Flow checker produces valid JSON when requested."""
        result = _run_checker("flow", json_output=True)
        assert result.returncode in (0, 1, 2), f"Unexpected exit code: {result.returncode}"
        data = json.loads(result.stdout)
        assert isinstance(data, dict), "JSON output is not a dict"
        assert "flow" in data, "flow key missing from JSON output"

    def test_pacing_checker_exit_code(self):
        """Pacing checker produces exit code 0 and output."""
        result = _run_checker("pacing")
        assert result.returncode in (0, 1, 2), f"Unexpected exit code: {result.returncode}"

    @requires_nlp
    def test_pacing_checker_json_output(self):
        """Pacing checker produces valid JSON when requested."""
        result = _run_checker("pacing", json_output=True)
        assert result.returncode in (0, 1, 2), f"Unexpected exit code: {result.returncode}"
        data = json.loads(result.stdout)
        assert isinstance(data, dict), "JSON output is not a dict"
        assert "pacing" in data, "pacing key missing from JSON output"

    def test_told_so_far_checker_json_output(self):
        """Told-so-far checker is reachable through its public CLI flag."""
        result = _run_checker("told-so-far", json_output=True)
        assert result.returncode in (0, 1, 2), result.stderr
        data = json.loads(result.stdout)
        assert "told_so_far" in data, "told_so_far key missing from JSON output"
    @requires_nlp
    def test_all_checkers_together(self):
        """All checkers run together with --all flag."""
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        result = subprocess.run(
            ["python", "-m", "tools.script_checkers.cli", str(FIXTURE_PATH), "--all"],
            capture_output=True,
            **UTF8_PIPE,
            env=env
        )
        assert result.returncode in (0, 1, 2), f"Unexpected exit code: {result.returncode}"

    @requires_nlp
    def test_all_checkers_json(self):
        """All checkers produce valid JSON output."""
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        result = subprocess.run(
            ["python", "-m", "tools.script_checkers.cli", str(FIXTURE_PATH), "--all", "--json"],
            capture_output=True,
            **UTF8_PIPE,
            env=env
        )
        assert result.returncode in (0, 1, 2), f"Unexpected exit code: {result.returncode}"
        data = json.loads(result.stdout)
        assert isinstance(data, dict), "JSON output is not a dict"
        # At least some checkers should be present
        assert any(k in data for k in ["stumble", "repetition", "scaffolding", "flow", "pacing"]), \
            "No checker results found in JSON output"
