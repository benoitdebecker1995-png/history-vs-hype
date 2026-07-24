"""Phase L3 — Programmatic registry API tests demonstrating the CheckerRegistry seam.

Tests:
- test_register_custom_checker: defines a minimal custom checker, registers it,
  verifies it appears in list_all() and can be run via registry.
- test_run_by_name: invokes registry.run("stumble", text) directly,
  asserts result dict contains expected keys.

Run with: pytest tests/test_checker_registry.py -v
"""
from typing import Dict, Any

import pytest

from tools.script_checkers.registry import CheckerRegistry, build_default_registry

# stumble lazy-loads spaCy; skip when the [nlp] extra isn't installed,
# matching tests/unit/test_pacing.py's existing convention.
try:
    import spacy  # noqa: F401
    NLP_AVAILABLE = True
except ImportError:
    NLP_AVAILABLE = False

requires_nlp = pytest.mark.skipif(not NLP_AVAILABLE, reason="spaCy required (pip install -e .[nlp])")


class _EchoChecker:
    """Minimal custom checker for registry registration testing."""

    @property
    def name(self) -> str:
        return "echo"

    @property
    def description(self) -> str:
        return "Returns word count — used for registry tests only."

    def run(self, text: str) -> Dict[str, Any]:
        return {
            "issues": [],
            "stats": {"word_count": len(text.split()), "severity": "ok"},
        }


class TestCheckerRegistry:
    def test_register_custom_checker(self):
        """Custom checker registers, appears in list_all(), and runs via registry."""
        registry = CheckerRegistry()
        checker = _EchoChecker()
        registry.register(checker)

        assert "echo" in registry.list_all()

        result = registry.run("echo", "dark ages myth colonial history")
        assert isinstance(result, dict)
        assert "issues" in result
        assert result["stats"]["word_count"] == 5

    @requires_nlp
    def test_run_by_name(self):
        """registry.run('stumble', text) returns dict with issues and stats keys."""
        registry = build_default_registry()
        text = "The dark ages were not actually dark. Historians have long argued this point."

        result = registry.run("stumble", text)

        assert isinstance(result, dict), "Result must be a dict"
        assert "issues" in result, "Result must contain 'issues' key"
        assert "stats" in result, "Result must contain 'stats' key"
        assert isinstance(result["issues"], list), "'issues' must be a list"

    def test_list_all_returns_all_defaults(self):
        """Default registry lists all 6 built-in checkers."""
        registry = build_default_registry()
        names = registry.list_all()

        assert names == ["flow", "pacing", "repetition", "scaffolding", "stumble", "told_so_far"]

    def test_get_returns_checker(self):
        """registry.get() returns a checker that can be called directly."""
        registry = build_default_registry()
        checker = registry.get("repetition")

        assert checker.name == "repetition"
        result = checker.run("The treaty. The treaty. The treaty.")
        assert "issues" in result
