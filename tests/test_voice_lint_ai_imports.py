"""Pins the Wikipedia "Signs of AI writing" import in voice_lint.

Two-sided contract, because a voice rule can fail in both directions: a rule
that never fires is dead weight, and a rule that fires on approved work
actively degrades the voice it is supposed to protect.

These imported catalogue rules retain their older profile provenance, but active
authority and conflict resolution now follow creator model v3 (ADR-0027).
"""
from pathlib import Path

import pytest

from tools.voice_lint import lint_file

REPO_ROOT = Path(__file__).resolve().parents[1]

# The four EVAL-GOLDEN-SET scripts (channel-data/calibration/EVAL-GOLDEN-SET.md).
GOLDEN = [
    "video-projects/_ARCHIVED/published/56-no-lassos-atlantic-slave-trade-origin-2026/02-SCRIPT-DRAFT.md",
    "video-projects/_ARCHIVED/published/57-piri-reis-map-ottoman-2026/SCRIPT.md",
    "video-projects/_READY_TO_FILM/58-kurdistan-statelessness-2026/SCRIPT.md",
    "video-projects/_ARCHIVED/published/59-israel-palestine-partition-offer-2026/SCRIPT.md",
]

IMPORTED_RULES = {
    "ai-vocab", "ai-shallow-verb", "negative-parallelism", "vague-attribution",
    "vague-some-scholars", "copula-serves-as", "copula-stands-as",
    "copula-functions-as", "puffery-nestled", "puffery-heart-of",
    "puffery-breathtaking", "puffery-diverse-array", "puffery-diverse-range",
    "sig-testament", "sig-setting-stage", "sig-indelible", "sig-deeply-rooted",
    "shallow-contributing-to", "shallow-valuable-insights", "vague-experts",
    "vague-experts-say", "vague-observers", "vague-industry-reports",
    "outline-despite-challenges", "outline-despite-its-challenges",
}

SLOP = """# Probe

Nestled in the heart of the Zagros mountains, the region boasts a rich cultural heritage.
The 1923 treaty serves as a testament to the intricate tapestry of imperial diplomacy.
Historians argue that this marked a pivotal moment, setting the stage for decades of conflict.
Some scholars believe the settlement was not just a border adjustment, but a deliberate erasure.
Several publications underscore its enduring significance, showcasing how the borders were drawn.
This was not merely administrative, but symbolizing a deeper shift contributing to instability.
Despite these challenges, the movement continues to foster a vibrant sense of identity.
Let us delve into the meticulous records that provide valuable insights.
"""


@pytest.mark.parametrize("rel", GOLDEN)
def test_imported_rules_are_silent_on_approved_scripts(rel):
    """Zero false positives on work he approved.

    All 54 imported tells were measured against these scripts before landing --
    they appear zero times in 8,885 spoken words. `legacy` was a candidate and
    was dropped for exactly this reason: #58 uses it as ordinary English
    ("obsessed with his legacy: Saddam Hussein"). If this test ever fails, the
    offending rule is wrong for his voice -- delete it, do not add an exception.
    """
    path = REPO_ROOT / rel
    if not path.exists():
        pytest.skip(f"golden-set script missing: {rel}")

    hits = [f for f in lint_file(str(path)) if f.rule in IMPORTED_RULES]

    assert not hits, (
        f"imported AI-tell rules fired on approved work: "
        f"{[(h.rule, h.line) for h in hits]}"
    )


def test_imported_rules_fire_on_actual_slop(tmp_path):
    """The other half: a rule that never fires is dead weight.

    Note this deliberately does NOT assert against the repo's AI control
    (REGEN-58-V18-DRAFT.md). Measured 2026-07-31: these rules score zero there,
    because that control drifts in HIS voice -- the existing fingerprint rules
    catch it with 5 HARD / 30 findings. The import guards a different failure
    mode: raw, unguided LLM prose reaching a script.
    """
    probe = tmp_path / "slop.md"
    probe.write_text(SLOP, encoding="utf-8")

    hits = [f for f in lint_file(str(probe)) if f.rule in IMPORTED_RULES]
    fired = {h.rule for h in hits}

    assert len(hits) >= 15, f"expected the import to catch this slop, got {len(hits)}"
    # every group represented, so a whole category cannot silently break
    for group in ("ai-vocab", "vague-attribution", "negative-parallelism",
                  "puffery-nestled", "sig-testament", "outline-despite-challenges"):
        assert group in fired, f"group {group!r} did not fire"


def test_imported_rules_never_ship_hard():
    """Imported provenance is not picks-validated, so it stays advisory.

    Same standing as the FINGERPRINT-UNSCRIPTED single-sample thresholds. A rule
    graduates to HARD only when his own picks confirm it, at which point it moves
    into the fingerprint proper.
    """
    from tools.voice_lint import HARD_LITERALS, HARD_REGEXES

    hard_ids = {r[0] for r in HARD_LITERALS} | {r[0] for r in HARD_REGEXES}

    assert not (hard_ids & IMPORTED_RULES), (
        f"imported tells must ship WARN, found as HARD: {hard_ids & IMPORTED_RULES}"
    )
