"""Tests for the CTA placement checker.

Pins the two necessary conditions it enforces — an ask exists, and it lands
early enough to be heard — plus the non-spoken-scaffolding rule that stops an
end-screen heading counting as an ask.

Measured basis (analytics.db, 58 videos): 22.4% of viewers remain at 80%
elapsed vs 31.2% at 30%, and the curve is flat between them.
"""
import pytest

from tools.script_checkers.checkers.cta_placement import CTAPlacementChecker
from tools.script_checkers.config import Config
from tools.script_checkers.registry import build_default_registry


@pytest.fixture
def checker():
    return CTAPlacementChecker(Config())


def _script(cta_at: float, length: int = 4000) -> str:
    """Build a script with the subscribe ask at a given fraction of the body."""
    filler = "The document says something specific and we read it closely. "
    body = (filler * (length // len(filler) + 1))[:length]
    idx = int(length * cta_at)
    return body[:idx] + " If this is useful, please subscribe. " + body[idx:]


def test_missing_cta_is_flagged(checker):
    result = checker.check("The treaty says one thing. " * 60)
    assert [i["type"] for i in result["issues"]] == ["cta_missing"]
    assert result["stats"]["cta_count"] == 0


def test_late_cta_is_noted_but_does_not_bind(checker):
    """Placement is CONTESTED (OPENER-RETENTION-DIAGNOSIS recommends the final 5%),
    so it must surface as information, never as a binding failure."""
    result = checker.check(_script(0.80))
    late = [i for i in result["issues"] if i["type"] == "cta_too_late"]
    assert late and late[0]["severity"] == "info"
    assert result["stats"]["first_cta_position"] > 0.35


def test_missing_cta_binds_but_placement_does_not(checker):
    """The two rules carry deliberately unequal force."""
    missing = checker.check("The treaty says one thing. " * 60)["issues"][0]
    late = [i for i in checker.check(_script(0.80))["issues"] if i["type"] == "cta_too_late"][0]
    assert missing["severity"] == "high"
    assert late["severity"] == "info"


def test_early_cta_passes(checker):
    result = checker.check(_script(0.22))
    assert result["issues"] == []
    assert result["stats"]["in_ideal_window"] is True


def test_boundary_just_inside_threshold_passes(checker):
    assert checker.check(_script(0.30))["issues"] == []


def test_end_screen_heading_does_not_count_as_an_ask(checker):
    """A CTA that exists only as production scaffolding is never spoken."""
    script = ("The document says something specific. " * 80
              + "\n## END SCREEN / CTA\n"
              + "**[VISUAL: end screen with subscribe button]**\n")
    types = [i["type"] for i in checker.check(script)["issues"]]
    assert "cta_missing" in types


def test_empty_script_does_not_crash(checker):
    result = checker.check("")
    assert result["issues"] == []
    assert result["stats"]["empty"] is True


def test_reported_position_is_accurate(checker):
    result = checker.check(_script(0.50))
    assert result["stats"]["first_cta_position"] == pytest.approx(0.50, abs=0.03)


def test_checker_is_registered_and_runnable():
    registry = build_default_registry()
    assert "cta" in registry.list_all()
    result = registry.run("cta", "The treaty says one thing. " * 60)
    assert [i["type"] for i in result["issues"]] == ["cta_missing"]
