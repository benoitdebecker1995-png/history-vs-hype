"""Hedge counter: classifier `kind of` and numeric `at least` are not hedges.

Regression test for the T6-T7 defect where the raw pattern reported noise as signal
(CALIBRATION-CORPUS 62-21). The three classifier false positives below are the exact
strings that were miscounted across #62's VO.
"""

import pytest

from tools.voice_lint import _hedges_in


@pytest.mark.parametrize(
    "sentence",
    [
        # the three real #62 false positives
        "It tells you what kind of record we're reading.",
        "This kind of collaboration existed across occupied Europe.",
        "If that's the kind of history you want, please subscribe.",
        # other classifier determiners
        "Some kind of order must have existed.",
        "There was no kind of paper trail left.",
        "Every sort of claim gets checked.",
        # numeric floor, not a verdict hedge
        "At least one OUN-B member was in every police unit.",
        "At least four thousand died that day.",
    ],
)
def test_classifier_and_quantifier_are_not_hedges(sentence):
    assert _hedges_in(sentence) == []


@pytest.mark.parametrize(
    "sentence,expected",
    [
        ("That's kind of how I speak.", ["kind of"]),
        ("It was sort of the point.", ["sort of"]),
        ("These are claims I cannot answer, I think.", ["I think"]),
        ("I guess that's the whole fight.", ["I guess"]),
        ("They basically rewrote the document.", ["basically"]),
        ("He probably carried the order out.", ["probably"]),
        ("At least, that's how the record reads.", ["At least"]),
    ],
)
def test_real_hedges_still_counted(sentence, expected):
    assert _hedges_in(sentence) == expected


def test_mixed_sentence_counts_only_the_hedge():
    s = "That kind of record is basically all we have."
    assert _hedges_in(s) == ["basically"]
