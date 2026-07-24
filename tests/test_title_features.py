"""Tests for tools.title_features — the canonical title-structure logic.

This is the test surface the ~5 drifted classifier copies never had. Covers the
6-class pattern taxonomy (priority ordering is the subtle part) and the feature
predicates, especially the cases the naive copies got wrong
(has_specific_number excluding "200-Year-Old"; the_x_that before colon).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import title_features as tf  # noqa: E402


# --- pattern() taxonomy + priority ordering -------------------------------

def test_versus_beats_colon():
    # "X vs Y: Stakes" must read as versus, not colon
    assert tf.pattern("Venezuela vs Guyana: Who Owns Essequibo?") == "versus"


def test_versus_variants():
    assert tf.pattern("Nigeria versus Cameroon") == "versus"
    assert tf.pattern("Spain vs. Morocco") == "versus"


def test_the_x_that_beats_colon():
    # the_x_that is checked before colon — the drifted copies lacked this class
    assert tf.pattern("The Treaty That Redrew Africa") == "the_x_that"


def test_colon():
    assert tf.pattern("Dark Ages: What Americans Believe") == "colon"


def test_question_requires_trailing_qmark():
    # canonical taxonomy keys 'question' off a trailing '?', NOT interrogative
    # prefixes (that was the analytics copies' broader heuristic, now dropped)
    assert tf.pattern("Who Really Owns the Falklands?") == "question"
    assert tf.pattern("What Americans Get Wrong About Rome") == "declarative"


def test_how_why():
    assert tf.pattern("How the KGB Weaponized History") == "how_why"
    assert tf.pattern("Why Somaliland Isn't Recognized") == "how_why"


def test_declarative_default():
    assert tf.pattern("The Forgotten Border War") == "declarative"


def test_pipe_is_not_colon():
    # title_scorer's canonical logic does not treat '|' as a colon
    assert tf.pattern("Dark Ages | What Americans Believe") == "declarative"


# --- has_year -------------------------------------------------------------

def test_has_year():
    assert tf.has_year("The 1494 Line That Split a Continent")
    assert tf.has_year("Iran 1953")
    assert not tf.has_year("The Forgotten War")


# --- has_specific_number (the predicate the naive copies got wrong) -------

def test_specific_number_counts_real_numbers():
    assert tf.has_specific_number("5 Myths About the Dark Ages")
    assert tf.has_specific_number("122 Years of French Extraction")


def test_specific_number_excludes_year():
    assert not tf.has_specific_number("Iran 1953")


def test_specific_number_excludes_duration_adjective():
    # "200-Year-Old" is a vague scale marker, not a concrete data point
    assert not tf.has_specific_number("The 200-Year-Old Lie")
    assert not tf.has_specific_number("A 500-Year Mistake")


# --- other predicates -----------------------------------------------------

def test_active_verb():
    assert tf.has_active_verb("How Spain Erased a Civilization")
    assert not tf.has_active_verb("The Quiet Border")


def test_evidence_promise():
    assert tf.has_evidence_promise("Here's the Evidence")
    assert tf.has_evidence_promise("The Documents Prove It")
    assert not tf.has_evidence_promise("A History of Belize")


def test_named_entity():
    assert tf.has_named_entity("How France Lost Algeria")
    assert tf.has_named_entity("The KGB's Forgery Factory")
    assert not tf.has_named_entity("The Forgotten Treaty")


def test_controversy_frame():
    assert tf.has_controversy_frame("The Myth of the Flat Earth")
    assert tf.has_controversy_frame("Who Destroyed the Narrative")
    assert not tf.has_controversy_frame("A Quiet History of Trade")


# --- backward-compat: title_scorer re-exports the canonical names ---------

def test_title_scorer_reexports_match():
    from tools.title_scorer import detect_pattern, has_year, has_specific_number

    assert detect_pattern is tf.pattern
    assert has_year is tf.has_year
    assert has_specific_number is tf.has_specific_number
