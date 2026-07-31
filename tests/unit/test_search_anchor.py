"""Unit tests for tools.title_scorer.has_search_anchor — the BINDING anchor filter.

`has_search_anchor` is not just the SEARCH_ANCHOR_BONUS input. It is FILTER 1 in
`tools/preflight/packaging_lock.py` (ADR-0012), recomputed at `validate_lock()` time,
so a spurious PASS advances a title through the packaging gate with no real head term.
That makes its false positives/negatives worth pinning, not just its happy path.

Two defects found 2026-07-30 while running the gate for #65 (Enigma) are pinned below:

  FALSE POSITIVE — the acronym list was matched case-INSENSITIVELY, so the ordinary
  English interrogative "Who" matched the acronym 'WHO' (World Health Organization).
  Every question-form title anchored on nothing at all.

  FALSE NEGATIVE — the head-term list is documented as territorially biased (sovereign
  states + geographic shorthands), so non-geographic subjects failed at lock time even
  when the subject massively outsearches most states ("alan turing" = 98,056 est.
  monthly searches per vidIQ).

Contract note: has_search_anchor returns a TUPLE (found, term). A bare truthiness test
on the return value is always True — the tuple-read is pinned here too.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.title_scorer import ALLOWED_ACRONYMS, has_search_anchor  # noqa: E402


# --- FALSE POSITIVE: stopwords that collide with acronyms ------------------

@pytest.mark.parametrize('title', [
    # Both were generated for #65 and both spuriously returned (True, 'Who').
    "Who Really Broke Enigma? Not Bletchley Park.",
    "The Imitation Game Erased the Men Who Broke Enigma.",
])
def test_interrogative_who_is_not_an_anchor(title):
    """Ordinary "Who" must not match the acronym WHO. No head term = FAIL the gate."""
    found, term = has_search_anchor(title)
    assert not found, f'spurious anchor {term!r} on a title with no head term'
    assert term == ''


def test_ordinary_words_colliding_with_acronyms_are_not_anchors():
    """"Us"/"It"/"Was" are English words here, not United States / acronyms."""
    found, term = has_search_anchor("It Was Not What They Told Us")
    assert not found, f'spurious anchor {term!r}'


def test_real_acronyms_still_anchor_in_their_own_casing():
    """The fix must not cost the acronyms their anchoring power."""
    # Single-match titles only — when several terms match, which one is returned is
    # set-iteration order and deliberately not part of the contract.
    assert has_search_anchor("The US Ended Birthright Citizenship") == (True, 'US')
    assert has_search_anchor("The ICJ Ruled Against the Claim") == (True, 'ICJ')
    assert has_search_anchor("How the KGB Weaponized a Forgery") == (True, 'KGB')
    assert has_search_anchor("WHO Rewrote Its Own Pandemic Record") == (True, 'WHO')


# --- FALSE NEGATIVE: famous non-territorial subjects -----------------------

def test_famous_surname_anchors_even_without_a_country():
    """"Alan Turing" outsearches most sovereign states; it must clear the filter."""
    found, term = has_search_anchor("Alan Turing Didn't Break Enigma First. Poland Did.")
    assert found, 'famous non-territorial subject failed the binding anchor filter'
    assert 'Turing' in term


def test_surname_alone_anchors():
    found, term = has_search_anchor("Turing Got the Credit. Three Poles Got There First.")
    assert found
    assert 'Turing' in term


# --- unchanged behaviour: the cases the filter already got right -----------

def test_country_still_anchors_case_insensitively():
    assert has_search_anchor("France Lost the Treaty That Drew Its Borders") == (True, 'France')
    # Head terms (unlike acronyms) stay case-insensitive — a country is a country.
    assert has_search_anchor("france lost the treaty")[0] is True


def test_anchorless_title_still_fails():
    assert has_search_anchor("An Obscure Cartographer Made a Strange Map") == (False, '')


def test_anchor_must_fall_inside_the_first_40_chars():
    """Poland sits at char 38+ here — past the window, so it cannot carry the title."""
    assert has_search_anchor("A Cartographer Drew a Very Strange Map of Poland") == (False, '')


# --- contract: the return value is a TUPLE, never a bare bool -------------

def test_returns_two_tuple_of_bool_and_str():
    for title in ("France Lost the Treaty", "An Obscure Cartographer"):
        result = has_search_anchor(title)
        assert isinstance(result, tuple) and len(result) == 2
        found, term = result
        assert isinstance(found, bool) and isinstance(term, str)
        # The trap: `if has_search_anchor(t):` is True for a NOT-FOUND result.
        assert bool(result) is True


def test_who_is_still_an_allowed_acronym_for_the_clickbait_gate():
    """The fix is scoped to anchoring. 'WHO' must stay all-caps-legal in titles."""
    assert 'WHO' in ALLOWED_ACRONYMS
