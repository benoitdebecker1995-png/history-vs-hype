"""Unit tests for tools.title_scorer.detect_clickbait — the BRAND GATE.

`detect_clickbait` is FILTER 2 in `tools/preflight/packaging_lock.py` (ADR-0012) and the
sole surviving auto-REJECT in `score_title` (style hedges are graded, non-fatal). A hit
forces grade='REJECTED' regardless of composite score, so its false POSITIVES are as
expensive as an anchor filter's false negatives — they kill a good title outright.

Defect fixed 2026-08-03: the pattern list was matched case-INSENSITIVELY, but it mixed
two different kinds of entry. Several are ALL-CAPS emphasis markers whose clickbaitness
IS the capitalisation ('EXPOSED', 'INSANE', 'SHOCKING', 'LIED About'), and lowercasing
the title made ordinary sentence-case English fatal:

    "China vs Taiwan. 4 Historical Claims Exposed by Scholars"  -> REJECTED on 'EXPOSED'

That is a REAL PUBLISHED title (7,318 lifetime impressions, 2.71% CTR per
analytics.db studio_ctr_rows). The list also contradicted itself: 'exposed' and 'lied'
sit in _TONE_SIGNALS['positive'] as approved active verbs earning ACTIVE_VERB_BONUS,
while 'EXPOSED' and 'LIED About' were hard rejects — the same word both rewarded and
fatal. Same defect family as the v6.1 A1 acronym bug (a case-insensitive match on a
token whose meaning depends on case), and fixed the same way: split the matching.

tests/unit/test_search_anchor.py is the sibling file, pinning the other binding filter.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.title_scorer import (  # noqa: E402
    CLICKBAIT_CAPS_MARKERS,
    CLICKBAIT_PATTERNS,
    CLICKBAIT_PHRASES,
    compute_tone_score,
    detect_clickbait,
    score_title,
    strip_clickbait,
)


# --- THE REGRESSION: sentence case is ordinary English --------------------

def test_published_title_is_not_clickbait():
    """The title that exposed the defect. Published, 7,318 impressions, 2.71% CTR."""
    title = "China vs Taiwan. 4 Historical Claims Exposed by Scholars"
    assert detect_clickbait(title) == []


def test_published_title_is_not_brand_gate_rejected():
    """The gate is binding, so pin the end-to-end verdict, not just the matcher."""
    result = score_title("China vs Taiwan. 4 Historical Claims Exposed by Scholars")
    assert result['hard_rejects'] == []
    assert result['grade'] != 'REJECTED'


@pytest.mark.parametrize('title', [
    "China vs Taiwan. 4 Historical Claims Exposed by Scholars",
    "How a Coin Exposed the Donation of Constantine",   # blocked #67 on 2026-08-03
    "An Insane Amount of Paperwork Preceded the Border",
    "Britain Lied About the Bengal Famine",             # the channel's own accusation voice
    "What the Treaty Really Means",
    "How This Changed the Border",
    "The Shocking Document Was Filed in 1953",
])
def test_sentence_case_markers_do_not_trip_the_gate(title):
    assert detect_clickbait(title) == [], f'false positive on {title!r}'


# --- ...but SHOUTING still is -------------------------------------------

@pytest.mark.parametrize('title,expected', [
    ("Claims EXPOSED by Scholars", 'EXPOSED'),
    ("SHOCKING: The Treaty Nobody Read", 'SHOCKING'),
    ("This Border Dispute Is INSANE", 'INSANE'),
    ("Britain LIED About the Bengal Famine", 'LIED About'),
    ("What IT Really Means for the Border", 'What IT Really Means'),
    ("How THIS Changed Europe Forever", 'How THIS Changed'),
])
def test_all_caps_markers_still_trip_the_gate(title, expected):
    assert detect_clickbait(title) == [expected]


def test_shouted_title_is_still_brand_gate_rejected():
    result = score_title("France Hid a SHOCKING Map Secret")
    assert result['hard_rejects'], 'the brand gate stopped rejecting shouted titles'
    assert result['grade'] == 'REJECTED'


def test_only_the_capitalised_token_must_be_shouted():
    """'LIED About' pins LIED; the trailing word's casing carries no signal."""
    assert detect_clickbait("Britain LIED about the Famine") == ['LIED About']
    assert detect_clickbait("Britain LIED ABOUT the Famine") == ['LIED About']
    assert detect_clickbait("Britain Lied About the Famine") == []


# --- phrase frames are clickbait in ANY casing ---------------------------

@pytest.mark.parametrize('title,expected', [
    ("the truth about spain", 'The truth about'),
    ("The TRUTH About Spain", 'The truth about'),
    ("You Won't Believe What the Map Shows", "You won't believe"),
    ("you won't BELIEVE what the map shows", "You won't believe"),
    ("TOP 10 TREATIES THAT FAILED", 'Top 10'),
    ("5 reasons why the border moved", '5 Reasons Why'),
    ("3 things you didn't know about Belize", "3 Things You Didn't Know"),
    ("Shapiro Destroyed by Facts", 'Destroyed by facts'),
    ("this will blow your mind", 'This will blow your mind'),
    ("What They Don't Want You to Know", "What they don't want you to know"),
    ("The Truth They Hid for 40 Years", 'The truth they hid'),
    ("A mind-blowing discovery", 'Mind-blowing'),
])
def test_phrase_frames_match_in_any_casing(title, expected):
    assert expected in detect_clickbait(title), f'phrase frame missed on {title!r}'


# --- the list no longer contradicts itself -------------------------------

@pytest.mark.parametrize('verb', ['exposed', 'lied', 'destroyed'])
def test_approved_active_verbs_are_not_fatal_in_sentence_case(verb):
    """These are in _TONE_SIGNALS['positive'] and earn ACTIVE_VERB_BONUS.

    A word cannot be both a rewarded active verb and a hard reject.
    """
    title = f"Britain {verb.capitalize()} the Record"
    assert detect_clickbait(title) == []
    assert compute_tone_score(title) > 0


def test_a_phrase_is_charged_once():
    """The old list held both "You won't believe" and "You won't BELIEVE", so a single
    shouted phrase was matched twice and charged -20."""
    assert detect_clickbait("You won't BELIEVE This") == ["You won't believe"]
    assert compute_tone_score("You won't BELIEVE This") == -10


# --- strip_clickbait honours the same rules ------------------------------

def test_strip_removes_only_shouted_markers():
    assert strip_clickbait("Claims EXPOSED by Scholars") == "Claims  by Scholars"
    # A generator must not silently delete an ordinary word from an on-brand title.
    assert strip_clickbait("Claims Exposed by Scholars") == "Claims Exposed by Scholars"


def test_strip_removes_phrase_frames_in_any_casing():
    assert 'truth' not in strip_clickbait("The Truth About Spain").lower()
    assert 'truth' not in strip_clickbait("the TRUTH about Spain").lower()


# --- back-compat: the published export -----------------------------------

def test_clickbait_patterns_is_the_union_of_both_lists():
    """metadata.py and tests/unit/test_metadata_bundle.py import this name."""
    assert CLICKBAIT_PATTERNS == CLICKBAIT_PHRASES + CLICKBAIT_CAPS_MARKERS
    assert isinstance(CLICKBAIT_PATTERNS, list)
    assert len(CLICKBAIT_PATTERNS) >= 5


def test_every_caps_marker_has_a_shouted_token():
    """A marker with no ALL-CAPS token would silently match case-insensitively —
    it belongs in CLICKBAIT_PHRASES instead."""
    for marker in CLICKBAIT_CAPS_MARKERS:
        assert any(tok.isupper() and tok.isalpha() for tok in marker.split()), (
            f'{marker!r} has no shouted token; move it to CLICKBAIT_PHRASES'
        )


def test_detect_clickbait_returns_a_list_and_never_raises():
    for title in ('', '   ', 'A', 'EXPOSED', "Spain vs Portugal"):
        assert isinstance(detect_clickbait(title), list)
