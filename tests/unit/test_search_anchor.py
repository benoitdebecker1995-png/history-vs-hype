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

Two more found 2026-08-03 while running the gate for #67 (Donation of Constantine):

  FALSE NEGATIVE (window) — the 40-char rule truncated the title MID-WORD instead of
  testing where the match STARTS, so a head term beginning inside the window but
  crossing its edge could not match its own \\b boundary. It failed the channel's only
  breakout and three other live titles. See the straddle tests below.

  FALSE NEGATIVE (mechanism) — "Constantine" (113,206 est. monthly searches) failed the
  gate while "Vatican" (100,602) passed, because recognition was membership in a
  hand-maintained set. That is the SAME defect as the Alan Turing one eight days
  earlier, and appending more strings would have been the third symptomatic fix. Fame
  is now ALSO decided by measured search volume (ADR-0023), so the tests below split
  in two: the curated fast path, and the volume mechanism that makes the gate
  self-repairing. The volume tests build their own keywords.db in tmp_path — they must
  pass on a machine whose keyword store is empty.

Contract note: has_search_anchor returns a TUPLE (found, term). A bare truthiness test
on the return value is always True — the tuple-read is pinned here too.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.title_scorer import (  # noqa: E402
    ALLOWED_ACRONYMS,
    ANCHOR_VOLUME_FLOOR,
    ANCHOR_WINDOW_CHARS,
    HEAD_TERMS,
    find_search_anchor,
    has_search_anchor,
    load_anchor_volumes,
    normalize_anchor_term,
    record_anchor_volume,
)


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
    """Poland STARTS past the window here, so it cannot carry the title."""
    title = "A Cartographer Drew a Very Strange Map of Poland"
    assert title.index('Poland') >= ANCHOR_WINDOW_CHARS  # guards the fixture's premise
    assert has_search_anchor(title) == (False, '')


# --- THE WINDOW IS A START POSITION, NOT A SUBSTRING (2026-08-03) ----------
# Fixed defect: the check ran against `title[:40]`, which truncates MID-WORD, so a head
# term that begins inside the window but crosses its edge failed its own \b boundary.

def test_channel_breakout_title_passes_the_gate():
    """The single best-performing title in the catalogue must not fail the binding gate.

    292,398 lifetime impressions at 7.66% CTR (analytics.db studio_ctr_rows) — the
    channel's only breakout. "Guatemala" begins at char 34, inside the window, but
    `title[:40]` left only "Guatem" and the gate returned FAIL.
    """
    title = "The Country That Might Disappear: Guatemala vs Belize"
    found, term = has_search_anchor(title)
    assert found, 'the channel breakout title failed the binding search-anchor filter'
    assert term == 'Guatemala'


@pytest.mark.parametrize('title,term,start', [
    ("The Country That Might Disappear: Guatemala vs Belize", 'Guatemala', 34),
    ("Primary Sources Destroy the 'Awesome Crusades' Narrative", 'Crusades', 37),
    ("Was Lagertha Real? DNA Says Female Viking Warriors Existed", 'Viking', 35),
    ("London's Stock Exchange Funded a Genocide", 'Genocide', 33),
])
def test_head_term_straddling_the_window_edge_still_anchors(title, term, start):
    """All four live titles whose head term begins inside the window but crosses it.

    Together they hold more lifetime impressions than every title the filter passed.
    """
    assert title.index(term) == start  # guards the fixture against title drift
    assert start < ANCHOR_WINDOW_CHARS <= start + len(term)  # genuinely straddles
    assert has_search_anchor(title) == (True, term)


def test_window_boundary_is_exact():
    """A term starting at char 39 anchors; the same term starting at 40 does not."""
    # Pad so 'France' begins at exactly ANCHOR_WINDOW_CHARS - 1, then at exactly
    # ANCHOR_WINDOW_CHARS (the trailing space is part of the padding).
    inside = 'x' * (ANCHOR_WINDOW_CHARS - 2) + ' France Lost It'
    outside = 'x' * (ANCHOR_WINDOW_CHARS - 1) + ' France Lost It'
    assert inside.index('France') == ANCHOR_WINDOW_CHARS - 1
    assert outside.index('France') == ANCHOR_WINDOW_CHARS
    assert has_search_anchor(inside) == (True, 'France')
    assert has_search_anchor(outside) == (False, '')


# --- THE MECHANISM: fame is measured, not remembered (2026-08-03, ADR-0023) ---
# These build their own keyword store in tmp_path, so they pin the MECHANISM and pass
# on a machine whose keywords.db is empty. The live-data pins come after them.

def _store(tmp_path, *rows):
    """Create a tmp keywords.db holding (term, volume) rows. Returns its path as str."""
    db = str(tmp_path / 'keywords.db')
    for term, volume in rows:
        outcome = record_anchor_volume(term, volume, 'vidiq-test-2026-08-03', db_path=db)
        assert 'error' not in outcome, outcome
    return db


def test_an_unlisted_term_anchors_once_its_volume_is_measured(tmp_path):
    """The whole point: no code change, no list edit — a measurement is enough.

    "Sassanid" is deliberately absent from HEAD_TERMS and always will be; the gate
    must not need anyone to have thought of it in advance.
    """
    title = "The Sassanid Archive Contradicts Every Retelling"
    assert 'Sassanid' not in HEAD_TERMS
    assert has_search_anchor(title) == (False, '')  # curated path alone: no anchor

    db = _store(tmp_path, ('Sassanid', 40_000))
    match = find_search_anchor(title, db_path=db)
    assert match.found
    assert match.term == 'Sassanid'
    assert match.volume == 40_000
    assert match.source == 'vidiq-test-2026-08-03'


def test_a_term_below_the_floor_is_not_an_anchor(tmp_path):
    """The gate still means something — measurement widens it, it does not dissolve it."""
    db = _store(tmp_path, ('Sassanid', ANCHOR_VOLUME_FLOOR))          # exactly at floor
    assert find_search_anchor("Sassanid Records Disagree", db_path=db).found

    below = str(tmp_path / 'below' / 'keywords.db')
    (tmp_path / 'below').mkdir()
    record_anchor_volume('Sassanid', ANCHOR_VOLUME_FLOOR, 'vidiq-test', db_path=below)
    # Overwrite the volume with a sub-floor number the recording API would refuse.
    import sqlite3
    conn = sqlite3.connect(below)
    conn.execute("UPDATE keywords SET search_volume = ? WHERE keyword = 'Sassanid'",
                 (ANCHOR_VOLUME_FLOOR - 1,))
    conn.commit()
    conn.close()
    assert find_search_anchor("Sassanid Records Disagree", db_path=below).found is False


def test_record_anchor_volume_refuses_a_sub_floor_number(tmp_path):
    """An unsearched term cannot be talked into being a head term."""
    outcome = record_anchor_volume(
        'Sassanid', ANCHOR_VOLUME_FLOOR - 1, 'vidiq-test',
        db_path=str(tmp_path / 'keywords.db'))
    assert 'error' in outcome
    assert str(ANCHOR_VOLUME_FLOOR) in outcome['error']


@pytest.mark.parametrize('term,volume,title', [
    # The two documented regressions, as measured volumes rather than list entries.
    ('Alan Turing', 87_786, "Alan Turing Didn't Break Enigma First. Poland Did."),
    ('Constantine', 113_206, "How a Coin Exposed the Donation of Constantine"),
])
def test_the_two_documented_regressions_pass_on_measurement_alone(
        term, volume, title, tmp_path):
    """Both false FAILs, reproduced against a store that knows only the one term.

    Constantine is NOT in HEAD_TERMS and must not be added — that was the third
    symptomatic fix this change exists to prevent. It anchors because 113,206 people
    a month search for it.
    """
    match = find_search_anchor(title, db_path=_store(tmp_path, (term, volume)))
    assert match.found, f'{term!r} still fails the binding filter'
    assert match.volume == volume
    assert term.split()[-1].lower() in match.term.lower()


def test_a_measured_phrase_beats_its_own_substring(tmp_path):
    """The most specific term at the earliest position is what gets recorded."""
    db = _store(tmp_path, ('Constantine', 113_206), ('Donation of Constantine', 3_412))
    match = find_search_anchor("How a Coin Exposed the Donation of Constantine", db_path=db)
    assert match.term == 'Donation of Constantine'
    assert match.volume == 3_412


def test_a_measured_term_is_still_bound_by_the_window(tmp_path):
    """Volume widens WHAT counts as a head term, never WHERE it may sit."""
    db = _store(tmp_path, ('Sassanid', 40_000))
    late = 'x' * ANCHOR_WINDOW_CHARS + ' Sassanid Records Disagree'
    assert late.index('Sassanid') > ANCHOR_WINDOW_CHARS
    assert find_search_anchor(late, db_path=db).found is False


def test_a_missing_keyword_store_degrades_to_the_curated_path(tmp_path):
    """A gate that hard-fails when a DB is absent would be worse than the bug."""
    missing = str(tmp_path / 'does-not-exist.db')
    assert load_anchor_volumes(missing) == {}
    assert find_search_anchor("France Lost the Treaty", db_path=missing).found


def test_normalization_folds_case_and_punctuation():
    """Both sides fold the same way, so "Brest-Litovsk" matches "brest-litovsk"."""
    assert normalize_anchor_term('Treaty of Brest-Litovsk') == 'treaty of brest litovsk'
    assert normalize_anchor_term('  THE  Vatican, ') == 'the vatican'
    # Possessive is grammar, not a different subject. Plain plurals are left alone.
    assert normalize_anchor_term("The Pope's Coins") == 'the pope coins'
    assert normalize_anchor_term('Popes') == 'popes'


def test_a_possessive_lead_anchors_on_the_measured_term(tmp_path):
    """Found running #67's real candidates: "The Pope's Own Coins…" FAILed while
    "A Coin Proved the Pope…" passed — the same subject, one apostrophe apart."""
    db = _store(tmp_path, ('Pope', 69_409))
    match = find_search_anchor("The Pope's Own Coins Proved He Never Ruled Rome", db_path=db)
    assert match.found
    assert match.term == "Pope's"
    assert match.volume == 69_409


# --- the live keyword store must actually carry the repaired terms ---------
# These read the repo's committed keywords.db. That is deliberate and it is the point
# of item 6 in the defect report: if the volumes behind the two documented regressions
# ever go missing, CI says so — a creator should not rediscover it mid-greenlight.

@pytest.mark.parametrize('title', [
    "Alan Turing Didn't Break Enigma First. Poland Did.",
    "How a Coin Exposed the Donation of Constantine",
    "The Pope Claimed Rome. A Forgery Said So.",
])
def test_live_store_carries_the_documented_regressions(title):
    match = find_search_anchor(title)
    assert match.found, (
        f'{title!r} fails the binding anchor filter against the live keyword store. '
        'Do NOT fix this by editing HEAD_TERMS — record the measured volume (ADR-0023).')


@pytest.mark.parametrize('title', [
    # The classical/medieval cluster the original defect report named "at minimum".
    # Constantine/Rome/Pope were recorded first and are covered above; these six were
    # still failing afterwards, and NOTHING WAS RED — no test asserted them, so a green
    # suite hid an open gap in a binding gate. That is what this parametrize exists for.
    "The Papacy Forged Its Own Land Deed",
    "Byzantine Scribes Knew the Donation Was Fake",
    "The Byzantine Empire Never Accepted the Claim",
    "Charlemagne Was Crowned on a Forgery",
    "Martin Luther Cited a Document He Knew Was Fake",
    "Aquinas Built an Argument on a Forged Grant",
    "Thomas Aquinas Never Questioned the Provenance",
    "Augustine of Hippo Set the Rule They Later Broke",
])
def test_live_store_carries_the_classical_medieval_cluster(title):
    """Measured on vidIQ 2026-08-03; all eight clear ANCHOR_VOLUME_FLOOR.

    Volumes at recording: Charlemagne 55,887 · Byzantine Empire 66,734 · Martin Luther
    33,669 · Thomas Aquinas 21,656 · Byzantine 14,734 · Augustine of Hippo 10,247 ·
    Aquinas 3,707 · Papacy 3,265.
    """
    match = find_search_anchor(title)
    assert match.found, (
        f'{title!r} fails the binding anchor filter against the live keyword store. '
        'Re-measure the term and `--record-anchor` it (ADR-0023); do not edit HEAD_TERMS.')


@pytest.mark.parametrize('term,title,collision', [
    ('Luther', "Luther Nailed Nothing to That Door",
     'the TV series — 62% of the 504,753/mo volume is Turkey, 2.9% US'),
    ('Augustine', "Augustine Never Wrote That Sentence",
     'the Florida city, which carries most of the tourism-driven volume'),
])
def test_ambiguous_bare_surnames_were_deliberately_left_unmeasured(term, title, collision):
    """These two FAIL on purpose, and that is the honest outcome (2026-08-03).

    Both bare surnames measure well above the floor, but the volume belongs to a
    DIFFERENT SUBJECT: {collision}. Recording it would put a real number behind a false
    claim in a binding gate — the reverse of the defect this filter keeps hitting.
    The disambiguated forms ("Martin Luther", "Augustine of Hippo") are recorded instead.

    If this test starts failing, someone recorded the bare surname. That may be correct
    — but only with a measurement that actually isolates the historical subject. Redo
    the reasoning; do not just delete the case.
    """
    assert find_search_anchor(title).found is False, (
        f'{term!r} now anchors. If that came from recording the bare surname, check the '
        f'volume is not {collision}.')


def test_the_project_67_title_that_exposed_the_gap():
    """#67's real candidate. It failed the gate while a strictly vaguer variant passed."""
    assert has_search_anchor("How a Coin Exposed the Donation of Constantine")[0] is True
    # The variant that used to be the only passing option — still fine, no longer forced.
    assert has_search_anchor("How a Coin Exposed a Vatican Forgery")[0] is True


# --- DETERMINISM: earliest match wins, longest breaks a positional tie ------
# The returned term is written verbatim into PROJECT-STATUS.md packaging-lock blocks,
# so it must not depend on set-iteration order.

def test_earliest_matching_term_is_returned():
    found, term = has_search_anchor("France Fought Spain. Napoleon Rewrote It.")
    assert (found, term) == (True, 'France')


def test_longest_term_wins_a_positional_tie():
    """"Saudi Arabia" and "Saudi" both start at 0 — the specific one is reported."""
    assert has_search_anchor("Saudi Arabia Redrew a Border It Never Held") == (
        True, 'Saudi Arabia')


def test_measured_provenance_wins_a_tie_against_an_identical_curated_term(tmp_path):
    """Same term, same position: report the number, because the block records it."""
    db = _store(tmp_path, ('France', 250_000))
    match = find_search_anchor("France Lost the Treaty", db_path=db)
    assert (match.term, match.volume) == ('France', 250_000)
    assert 'France' in HEAD_TERMS  # the curated path would also have matched


def test_returned_term_is_stable_across_calls():
    title = "The Vatican, Rome, and the Pope All Claim the Same Document"
    assert len({has_search_anchor(title) for _ in range(25)}) == 1


# --- the audit trail written into the packaging-lock block ------------------

def test_describe_records_the_measurement_and_its_source(tmp_path):
    match = find_search_anchor("Sassanid Records Disagree",
                               db_path=_store(tmp_path, ('Sassanid', 40_000)))
    described = match.describe()
    assert '40,000/mo' in described
    assert 'vidiq-test-2026-08-03' in described


def test_describe_on_a_fail_says_how_to_repair_a_famous_but_unmeasured_term():
    """A FAIL means one of two things; the block must not leave the reader guessing."""
    described = find_search_anchor("An Obscure Cartographer Made a Strange Map").describe()
    assert '--record-anchor' in described


# --- the repair can only ADD anchors, never remove one ---------------------

def test_no_previously_passing_shape_starts_failing():
    """B1 (window) and B2 (measurement) are both additive; nothing that passed may fail."""
    for title in (
        "France Lost the Treaty That Drew Its Borders",
        "The US Ended Birthright Citizenship",
        "The ICJ Ruled Against the Claim",
        "How the KGB Weaponized a Forgery",
        "Alan Turing Didn't Break Enigma First. Poland Did.",
    ):
        assert has_search_anchor(title)[0] is True, title


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
