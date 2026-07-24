"""Preflight fallback title classifier — taxonomy parity with title_features.

The fallback (`_classify_title_pattern_fallback`) only runs when the
title_scorer path errors out. It was the last hand-synced copy of the
structural taxonomy (ADR-0009 deferred item, closed 2026-07-01); it now
delegates to tools.title_features.pattern, so its labels can never drift
from the primary path again. The base-score/penalty policy stays preflight's
own and is pinned here.

Run:
    pytest tools/tests/test_preflight_title_fallback.py -v
"""

import sys
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from tools.preflight.scorer import _classify_title_pattern_fallback  # noqa: E402
from tools.title_features import pattern as canonical_pattern  # noqa: E402

SAMPLE_TITLES = [
    "France vs Britain. Who Drew the Border",
    "The Treaty That Never Existed",
    "France Lost Its Largest Colony Twice",
    "How France Lost the Treaty",
    "Why the Border Moved",
    "Did France Fake the Map?",
    "Sykes-Picot: The Line That Broke the Middle East",
]


@pytest.mark.parametrize("title", SAMPLE_TITLES)
def test_fallback_taxonomy_matches_canonical(title):
    """The fallback's pattern label must be exactly title_features.pattern's."""
    pattern, _, _ = _classify_title_pattern_fallback(title)
    assert pattern == canonical_pattern(title)


def test_base_scores_follow_preflight_policy():
    assert _classify_title_pattern_fallback("France Lost Its Largest Colony Twice")[1] == 75
    assert _classify_title_pattern_fallback("How France Lost the Treaty")[1] == 70
    assert _classify_title_pattern_fallback("The Treaty That Never Existed")[1] == 20


def test_year_penalty_applies_and_flags():
    pattern, score, issues = _classify_title_pattern_fallback(
        "France Lost the Treaty of 1919")
    assert score == 45  # declarative 75 - 30 year penalty
    assert any('YEAR' in i for i in issues)


def test_question_mark_flagged():
    _, _, issues = _classify_title_pattern_fallback("Did France Fake the Map?")
    assert any('Question mark' in i for i in issues)


def test_the_x_that_flagged_never_use():
    _, _, issues = _classify_title_pattern_fallback("The Treaty That Never Existed")
    assert any('NEVER USE' in i for i in issues)
