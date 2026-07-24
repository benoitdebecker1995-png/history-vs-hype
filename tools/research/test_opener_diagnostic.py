"""
Unit tests for tools.research.opener_diagnostic.

The load-bearing test is the natural-experiment validation: the three own openers
(same voice, same channel, same format) must reproduce their measured retention
ordering on the SUCCES scorecard:

    Tripoli (61% retention, BEST)  ->  SUCCES 6
    No-Lassos (58%, STRONG)        ->  SUCCES 5
    Bakassi (~31%, WORST)          ->  SUCCES 3

Verbatim opener texts are quoted from
.claude/REFERENCE/OPENER-CRAFT-BRIEF.md §3 (Own-Opener Contrast Verdict).
"""

import pytest

from tools.research.opener_diagnostic import diagnose_opener


# --- Verbatim first-30s openers (OPENER-CRAFT-BRIEF.md §3) -------------------

TRIPOLI_TEXT = (
    "In 1930, a Dutch scholar named Snouck Hurgronje examined the Arabic original "
    "of an American treaty. The next year, the United States government printing "
    "office published what he found, what he found the State Department couldn't "
    "explain. And, almost 100 years later, neither can anyone else."
)
TRIPOLI_TITLE = "The Treaty That Proves America Wasn't Founded a Christian Nation"

NO_LASSOS_TEXT = (
    "There's a claim about the Atlantic slave trade you've probably seen online. "
    "It goes something like this. Europeans and Americans didn't go over to Africa "
    "with a lasso and start wrangling up random black people. We didn't do that. We "
    "went over there and other black people sold them to us. They were already "
    "slaves to begin with. They were slaves before they even made it to America. On "
    "the surface, this sounds like an even-handed correction of the historical "
    "record. The problem is, we have the historical record. And it was written by "
    "the men who ran the operation. August 8th, 1444. Prince Henry the Navigator "
    "sits on horseback in Lagos, Portugal, watching 235 captured Africans being "
    "divided into lots, while captives cling to each other so close they can hardly "
    "be separated."
)
NO_LASSOS_TITLE = "The Atlantic Slave Trade Myth, Corrected by the Record"

BAKASSI_TEXT = (
    "Most border disputes are about who got to the land first. They are about who "
    "bled for the perimeter or who tilled the soil. The story of the Bakassi "
    "Peninsula is different. It is a study of what happens when lines drawn by men "
    "in London, men who had never seen the sun set over the Gulf of Guinea, collide "
    "with the lived reality of the people standing on the shore."
)
BAKASSI_TITLE = "The Bakassi Peninsula Border Dispute"


@pytest.fixture(scope="module")
def diagnoses():
    return {
        "tripoli": diagnose_opener(TRIPOLI_TEXT, TRIPOLI_TITLE,
                                   topic_type="political_fact_check"),
        "no_lassos": diagnose_opener(NO_LASSOS_TEXT, NO_LASSOS_TITLE,
                                     topic_type="ideological"),
        "bakassi": diagnose_opener(BAKASSI_TEXT, BAKASSI_TITLE,
                                   topic_type="territorial"),
    }


# --- Load-bearing: SUCCES reproduces the measured retention ordering ---------

def test_succes_exact_scores(diagnoses):
    assert diagnoses["tripoli"]["succes"]["score"] == 6
    assert diagnoses["no_lassos"]["succes"]["score"] == 5
    assert diagnoses["bakassi"]["succes"]["score"] == 3


def test_succes_strict_ordering(diagnoses):
    t = diagnoses["tripoli"]["succes"]["score"]
    n = diagnoses["no_lassos"]["succes"]["score"]
    b = diagnoses["bakassi"]["succes"]["score"]
    assert t > n > b


def test_succes_roughly_six_five_three(diagnoses):
    # "roughly 6 / 5 / 3" — within +/-1 of target, ordering preserved.
    assert abs(diagnoses["tripoli"]["succes"]["score"] - 6) <= 1
    assert abs(diagnoses["no_lassos"]["succes"]["score"] - 5) <= 1
    assert abs(diagnoses["bakassi"]["succes"]["score"] - 3) <= 1


# --- Principle-level diagnosis matches the brief's narrative -----------------

def test_tripoli_passes_all_principles(diagnoses):
    principles = diagnoses["tripoli"]["succes"]["principles"]
    assert all(principles.values()), principles


def test_no_lassos_fails_only_concrete(diagnoses):
    # Brief: "Concrete weak in first 10 words" is the single No-Lassos miss.
    principles = diagnoses["no_lassos"]["succes"]["principles"]
    assert principles["concrete"] is False
    assert sum(1 for v in principles.values() if not v) == 1


def test_bakassi_gap_does_not_fire(diagnoses):
    # Brief: the gap never cleanly opens — schema-break absent.
    principles = diagnoses["bakassi"]["succes"]["principles"]
    assert principles["unexpected"] is False
    assert principles["concrete"] is False


# --- Verdict -----------------------------------------------------------------

def test_verdicts(diagnoses):
    assert diagnoses["tripoli"]["verdict"] == "retains"
    assert diagnoses["no_lassos"]["verdict"] == "retains"
    assert diagnoses["bakassi"]["verdict"] == "bleeds"


# --- Eves pattern tests ------------------------------------------------------

def test_bakassi_predicted_to_bleed_on_eves(diagnoses):
    # No macro-gap -> slow-burn risk flagged.
    assert diagnoses["bakassi"]["eves"]["slow_burn_risk"] is True
    assert diagnoses["bakassi"]["eves"]["macro_gap_present"] is False


def test_strong_openers_have_macro_gap(diagnoses):
    assert diagnoses["tripoli"]["eves"]["macro_gap_present"] is True
    assert diagnoses["no_lassos"]["eves"]["macro_gap_present"] is True


# --- top_fix follows the gap -> anchor -> timing hierarchy -------------------

def test_bakassi_top_fix_is_gap(diagnoses):
    assert diagnoses["bakassi"]["top_fix"]["axis"] == "GAP"


def test_top_fix_axis_is_valid(diagnoses):
    valid = {"GAP", "ANCHOR", "TIMING", "FULFILLMENT", "EASE", "POLISH"}
    for d in diagnoses.values():
        assert d["top_fix"]["axis"] in valid


# --- Contract / robustness ---------------------------------------------------

def test_heuristic_checks_are_labelled(diagnoses):
    q = diagnoses["tripoli"]["diagnostic_questions"]
    assert q["gap_feels_painful"]["heuristic"] is True
    assert q["prerequisite_knowledge"]["heuristic"] is True
    assert "emotional" in diagnoses["tripoli"]["succes"]["heuristic_principles"]


def test_is_filter_not_predictor_flag(diagnoses):
    assert diagnoses["tripoli"]["meta"]["is_filter_not_predictor"] is True


def test_short_opener_returns_error_gracefully():
    out = diagnose_opener("Too short.", "Some Title")
    assert "error" in out
    assert out["verdict"] == "bleeds"


def test_topic_type_inferred_when_omitted():
    out = diagnose_opener(TRIPOLI_TEXT, TRIPOLI_TITLE)
    assert out["topic_type"] in {
        "territorial", "ideological", "political_fact_check", "general",
    }


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-v"]))
