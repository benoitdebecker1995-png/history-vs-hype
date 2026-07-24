"""
Opener Diagnostic — the expert 60-second opener lens, as code.

Implements the self-diagnosis protocol from `.claude/REFERENCE/OPENER-MASTERY-BRIEF.md`
(§2 hierarchy, §3 the 6-question diagnostic + SUCCES scorecard + Eves pattern tests)
and the sentence-1 checklist from `.claude/REFERENCE/OPENER-CRAFT-BRIEF-2.md` (§4).

WHAT THIS IS — AND IS NOT
-------------------------
This is a **FILTER, not a predictor**. It checks *necessary conditions* an opener
must clear (does a gap fire, is there an anchor, does the title↔opener promise hold),
exactly the way the title/hook scorers are filters not predictors
(see memory/feedback-filters-not-predictors.md). A 6/6 SUCCES does NOT predict
retention; a 3/6 reliably flags where an opener will bleed. Use it to catch missing
necessary conditions before filming, never to rank openers by a single score.

HEURISTIC FLAGS
---------------
Several checks can only be *approximated* from text — chiefly "does the gap feel
painful?" (Q4) and "does the viewer already hold the prerequisite belief?" (Q1 /
the Emotional principle). A scorer cannot know what an audience believes. Those
checks are LABELLED `heuristic=True` in the returned dict and in their docstrings.
They look for the textual *signatures* of the real thing (belief-priming framing,
authority-failure language, unresolved-mystery markers), which is a proxy, not a
measurement.

REUSE (no rebuilding)
---------------------
- tools.production.parser.strip_for_teleprompter   → markdown/B-roll cleaning
- tools.newsletter.article_scorer._split_sentences  → plain-text sentence splitting
- tools.research.hook_scorer._check_fulfillment     → title↔opener (Eves hockey-stick)
- tools.research.hook_scorer._detect_framework      → anomaly/stakes/inciting signals
- tools.research.hook_scorer._extract_title_entities→ title entity extraction
- tools.research.hook_scorer._detect_hook_style     → archetype detection
- tools.research.hook_scorer.detect_topic_from_script→ topic inference when unset

Usage:
    from tools.research.opener_diagnostic import diagnose_opener
    d = diagnose_opener(opener_text, title="Why Brazil Speaks Portuguese",
                        topic_type="territorial")
    print(d["succes"]["score"], d["top_fix"]["axis"])

Called by: /opener and /script (wiring is done separately, after validation).
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

from tools.production.parser import strip_for_teleprompter
from tools.newsletter.article_scorer import _split_sentences
from tools.research.hook_scorer import (
    _check_fulfillment,
    _detect_framework,
    _extract_title_entities,
    _detect_hook_style,
    _load_pattern_library,
    detect_topic_from_script,
)


# ---------------------------------------------------------------------------
# Marker libraries (textual signatures the diagnostic looks for)
# ---------------------------------------------------------------------------

# Schema-break / contradiction signals (Made to Stick "Unexpected"; the gap firing).
# Deliberately specific phrases — bare "not"/"never" are excluded so emotive prose
# ("had never seen the sun set") does not read as a schema-break.
_SCHEMA_BREAK = [
    r"could ?n[o']?t",
    r"can'?t explain",
    r"cannot explain",
    r"the problem is",
    r"neither can",
    r"no one can",
    r"nobody can",
    r"\bdidn'?t\b",
    r"\bdid not\b",
    r"\bwasn'?t\b",
    r"\bweren'?t\b",
    r"\bdoesn'?t\b",
    r"contradict",
    r"\bin fact\b",
    r"\bactually\b",
    r"turns out",
    r"the catch",
    r"the twist",
    r"\bexcept\b",
    r"but the (?:problem|truth|record|catch)",
]

# Unresolved / authority-failure signals — proxy for "does the gap feel painful?"
# HEURISTIC. Real painfulness depends on the viewer; this matches its signature.
_GAP_PAINFUL = [
    r"could ?n[o']?t explain",
    r"can'?t explain",
    r"cannot explain",
    r"neither can",
    r"no one (?:can|knows|has|could)",
    r"still (?:can'?t|cannot|unsolved|unexplained|a mystery)",
    r"\bunsolved\b",
    r"\bunexplained\b",
    r"the problem is",
    r"\b\d{1,4} years? (?:later|on|after)",
    r"to this day",
    r"remains? (?:a mystery|unsolved|unexplained|unanswered)",
]

# Belief-priming framing — proxy for "viewer already holds the prerequisite belief"
# (Loewenstein prerequisite-knowledge). HEURISTIC.
_BELIEF_PRIMING = [
    r"you'?ve (?:probably )?(?:seen|heard|read)",
    r"you'?ve been (?:told|taught)",
    r"most people",
    r"the (?:standard|popular|textbook|common|official) (?:answer|version|story|view|line)",
    r"there'?s a (?:claim|story|version)",
    r"the (?:claim|story) (?:is|goes)",
    r"\bthe myth\b",
    r"everyone (?:knows|thinks|learns|believes)",
    r"we'?ve (?:all )?been (?:told|taught)",
    r"you'?d think",
    r"the story goes",
    r"it'?s (?:often|widely|commonly) (?:said|believed|claimed)",
    r"\bsupposedly\b",
]

# Pathos / emotive imagery — secondary route to the Emotional principle.
_PATHOS = [
    r"\bbled\b",
    r"\bblood\b",
    r"\bdied\b",
    r"\bkilled\b",
    r"\bsuffer",
    r"\bcling(?:ing)?\b",
    r"\btorn\b",
    r"lived reality",
    r"standing on the (?:shore|edge)",
    r"\bfate\b",
    r"\bstruggle\b",
    r"hardly be separated",
    r"\bbleed\b",
]

# Concrete scene verbs — actors doing things (Story / transportation).
_SCENE_VERBS = {
    "examined", "examines", "sits", "sit", "sat", "watching", "watched", "watches",
    "drawn", "draw", "drew", "collide", "collides", "collided", "standing", "stood",
    "divided", "dividing", "clinging", "sailed", "sailing", "signed", "signs", "rode",
    "presided", "walked", "walks", "hammered", "captured", "wrangling", "tilled",
    "negotiated", "published", "ran", "hired", "sold", "knelt", "marched",
}

# Hedging openings — disqualify cognitive-ease pass on sentence 1.
_HEDGE_STARTS = [
    "some people argue", "it could be said", "there is a view", "there's a view",
    "arguably", "perhaps", "it has been argued", "it could be argued",
    "many believe", "some say", "one might say", "it might be said",
]

# State-of-being sentence openings (McKee: weakest way into a sentence) — advisory.
_STATE_OF_BEING_STARTS = [
    "there is", "there's", "there are", "it is", "it's", "they are", "they're",
    "this is", "that is", "he is", "she is", "he was", "she was", "it was",
]

_MONTHS = (
    r"(?:january|february|march|april|may|june|july|august|september|october|"
    r"november|december)"
)
_DATE_RE = re.compile(rf"\b{_MONTHS}\s+\d{{1,2}}", re.IGNORECASE)
_YEAR_RE = re.compile(r"\b\d{3,4}\b")
_PROPER_PAIR_RE = re.compile(r"[A-Z][a-z]+\s+[A-Z][a-z]+")


# ---------------------------------------------------------------------------
# Small text helpers
# ---------------------------------------------------------------------------

def _clean(text: str) -> str:
    """Strip markdown / B-roll markers; passes plain prose through unchanged."""
    if not text:
        return ""
    return strip_for_teleprompter(text)


def _first_words(text: str, n: int) -> str:
    return " ".join(text.split()[:n])


def _any(patterns: List[str], text: str) -> bool:
    low = text.lower()
    return any(re.search(p, low) for p in patterns)


def _count(patterns: List[str], text: str) -> int:
    low = text.lower()
    return sum(1 for p in patterns if re.search(p, low))


def _has_named_specificity(segment: str) -> bool:
    """Named person / specific date / year inside `segment`.

    A year or month-day counts directly. A capitalized proper-noun *pair*
    counts as a named person/place — but the first token is dropped first so a
    sentence-initial common word ('Most', "There's") cannot pair with the next
    word and produce a false positive.
    """
    if not segment:
        return False
    if _YEAR_RE.search(segment) or _DATE_RE.search(segment):
        return True
    tokens = segment.split()
    remainder = " ".join(tokens[1:]) if tokens else ""
    return bool(_PROPER_PAIR_RE.search(remainder))


# ---------------------------------------------------------------------------
# SUCCES scorecard (Made to Stick — 6 principles, OPENER-MASTERY-BRIEF §3 Step 3)
# ---------------------------------------------------------------------------

def _score_succes(
    cleaned: str,
    sentences: List[str],
    title_entities: List[str],
) -> Dict[str, Any]:
    """Score the opener 0-6 against the SUCCES principles.

    Each principle is a necessary-condition check, not a weighted predictor.
    `emotional` and the prerequisite-belief facet are HEURISTIC (see module
    docstring) — they match the *signature* of audience belief, not the belief.
    """
    s1 = sentences[0] if sentences else ""
    first_112 = _first_words(cleaned, 112)

    belief_priming = _any(_BELIEF_PRIMING, cleaned)
    gap_painful = _any(_GAP_PAINFUL, cleaned)
    pathos = _any(_PATHOS, cleaned)
    schema_break = _any(_SCHEMA_BREAK, first_112)

    # Simple — one core gap, not a pile of competing claims.
    enumeration = bool(re.search(r"\bfirst(?:ly)?\b.*\bsecond(?:ly)?\b", cleaned.lower()))
    overloaded = _count(_SCHEMA_BREAK, first_112) >= 4 or enumeration
    simple = not overloaded

    # Unexpected — violates a schema the viewer holds.
    unexpected = schema_break

    # Concrete — named person/date/place in sentence 1.
    concrete = _has_named_specificity(s1)

    # Credible — claim is falsifiable: a named, checkable anchor exists.
    credible = bool(
        _YEAR_RE.search(cleaned)
        or _DATE_RE.search(cleaned)
        or re.search(
            r"\b(treaty|document|record|charter|decree|statute|census|archive|"
            r"court|ledger|letter|telegram|\bmap\b|report|transcript|minutes|\bact\b|"
            r"department|ministry|government|parliament|congress|commission|tribunal|"
            r"printing office)\b",
            cleaned.lower(),
        )
    )

    # Emotional — connects to a belief/concern the viewer already holds. HEURISTIC.
    # Routes: belief-priming framing, authority-failure awe, or emotive pathos.
    emotional = belief_priming or gap_painful or pathos

    # Story — a scene with an actor, an action, and a consequence.
    scene_verb_hits = sum(1 for w in re.findall(r"[a-z]+", cleaned.lower()) if w in _SCENE_VERBS)
    tokens = cleaned.split()
    named_actor = bool(_PROPER_PAIR_RE.search(" ".join(tokens[1:]))) if tokens else False
    story = (named_actor and scene_verb_hits >= 1) or scene_verb_hits >= 2

    principles = {
        "simple": simple,
        "unexpected": unexpected,
        "concrete": concrete,
        "credible": credible,
        "emotional": emotional,
        "story": story,
    }
    score = sum(1 for v in principles.values() if v)
    return {
        "score": score,
        "max": 6,
        "principles": principles,
        "heuristic_principles": ["emotional"],
        "note": (
            "'emotional' is a heuristic proxy for the prerequisite-belief the "
            "viewer holds; it matches belief-priming / pathos / authority-failure "
            "signatures, not actual audience belief."
        ),
    }


# ---------------------------------------------------------------------------
# The 6-question 60-second diagnostic (OPENER-MASTERY-BRIEF §3 Step 1)
# ---------------------------------------------------------------------------

def _diagnostic_questions(
    cleaned: str,
    sentences: List[str],
    title_entities: List[str],
    fulfillment: Dict[str, Any],
) -> Dict[str, Any]:
    """The six yes/no questions an expert asks in the first 60 seconds.

    Q1 (prerequisite belief) and Q4 (gap painful) are HEURISTIC approximations.
    """
    s1 = sentences[0] if sentences else ""
    first_10 = _first_words(cleaned, 10)
    first_30_words = _first_words(cleaned, 30)
    first_3_sentences = " ".join(sentences[:3])
    cleaned_low = cleaned.lower()

    entity_echo = fulfillment.get("entity_echo", {}).get("passed", False)

    # Q1 — prerequisite knowledge the opener can assume. HEURISTIC.
    q1 = bool(
        _any(_BELIEF_PRIMING, first_30_words)
        or entity_echo
        or re.search(r"\b(department|government|court|treaty|empire|king|president)\b", cleaned_low)
    )

    # Q2 — named person/date/place in the first 10 words.
    q2 = _has_named_specificity(first_10)

    # Q3 — has a specific unknown / contradiction been named by sentence 3.
    q3 = _any(_SCHEMA_BREAK, first_3_sentences) or _any(_GAP_PAINFUL, first_3_sentences)

    # Q4 — does the gap feel painful (unresolved, authority failed). HEURISTIC.
    q4 = _any(_GAP_PAINFUL, cleaned)

    # Q5 — surprise relates to the core argument (post-dictable). HEURISTIC:
    # title↔opener entity overlap is the proxy that the surprise is on-thesis.
    q5 = entity_echo

    # Q6 — sentence 1 parses cleanly in one listening (cognitive ease of form).
    s1_words = len(s1.split())
    starts_hedge = any(s1.lower().startswith(h) for h in _HEDGE_STARTS)
    q6 = (s1_words <= 18) and not starts_hedge

    return {
        "prerequisite_knowledge": {"passed": q1, "heuristic": True},
        "named_specificity_first_10_words": {"passed": q2, "heuristic": False},
        "gap_named_by_sentence_3": {"passed": q3, "heuristic": False},
        "gap_feels_painful": {"passed": q4, "heuristic": True},
        "surprise_relates_to_argument": {"passed": q5, "heuristic": True},
        "sentence_1_parses_cleanly": {"passed": q6, "heuristic": False},
    }


# ---------------------------------------------------------------------------
# Sentence-1 checklist (OPENER-CRAFT-BRIEF-2 §4) — advisory detail
# ---------------------------------------------------------------------------

def _sentence1_checklist(s1: str) -> Dict[str, Any]:
    """Per-item sentence-1 mechanics from OPENER-CRAFT-BRIEF-2 §4 (advisory)."""
    low = s1.lower().strip()
    words = s1.split()
    return {
        "length_le_13": len(words) <= 13,
        "word_count": len(words),
        "no_state_of_being_lead": not any(low.startswith(s) for s in _STATE_OF_BEING_STARTS),
        "no_hedge": not any(low.startswith(h) for h in _HEDGE_STARTS),
        "has_specificity": _has_named_specificity(s1),
        "no_subordinate_pileup": s1.count(",") <= 2,
    }


# ---------------------------------------------------------------------------
# Eves retention-pattern tests (OPENER-MASTERY-BRIEF §3 Step 2)
# ---------------------------------------------------------------------------

def _eves_tests(
    cleaned: str,
    fulfillment: Dict[str, Any],
    macro_gap_present: bool,
    thumbnail: Optional[str],
) -> Dict[str, Any]:
    """The two Eves failure-pattern predictions.

    Hockey stick = title/thumbnail promise not honored in the first 15s (reuses
    hook_scorer._check_fulfillment, which inspects the first ~50 words ≈ 20s — a
    slightly wider window than 15s, documented here as a conservative proxy).

    Slow burn = no macro-gap established that the video will take its length to
    resolve (the opener delivers everything up front).
    """
    entity_echo = fulfillment.get("entity_echo", {}).get("passed", False)
    promise_ok = fulfillment.get("promise_type", {}).get("passed", False)

    thumbnail_echo = False
    if thumbnail:
        first_50 = _first_words(cleaned, 50).lower()
        thumb_words = [w for w in re.findall(r"[A-Za-z]{4,}", thumbnail)]
        thumbnail_echo = any(w.lower() in first_50 for w in thumb_words)

    aligned = (entity_echo or thumbnail_echo) and promise_ok
    return {
        "hockey_stick_risk": not aligned,
        "title_opener_aligned": aligned,
        "thumbnail_echo": thumbnail_echo if thumbnail else None,
        "slow_burn_risk": not macro_gap_present,
        "macro_gap_present": macro_gap_present,
        "note": (
            "hockey_stick uses hook_scorer._check_fulfillment (first ~50 words / "
            "~20s) as a proxy for the first-15s promise window."
        ),
    }


# ---------------------------------------------------------------------------
# Top fix — gap -> anchor -> timing hierarchy (OPENER-MASTERY-BRIEF §2)
# ---------------------------------------------------------------------------

def _choose_top_fix(
    succes: Dict[str, Any],
    questions: Dict[str, Any],
    eves: Dict[str, Any],
) -> Dict[str, str]:
    """Pick the single highest-leverage fix.

    Strict hierarchy from §2: 'Fix the gap first. Then fix the anchor. Then fix
    the timing. Everything else is polish.' Gap (Tier 1.1) > Anchor (Tier 1.2) >
    Timing (Tier 1.3) > Fulfillment (Tier 2.7) > Ease (Tier 2.4) > Polish.
    """
    p = succes["principles"]
    q = questions
    gap_ok = p["unexpected"] and q["gap_feels_painful"]["passed"]
    anchor_ok = p["concrete"] or q["named_specificity_first_10_words"]["passed"]
    timing_ok = q["gap_named_by_sentence_3"]["passed"]

    if not gap_ok:
        return {
            "axis": "GAP",
            "tier": "Tier 1 (load-bearing)",
            "fix": (
                "The gap does not fire. Name a specific unknown the viewer wants "
                "closed — a schema-break tied to the thesis (an authority that "
                "can't explain, a claim the record contradicts). Move it to "
                "sentence 1. Nothing downstream matters until this lands."
            ),
        }
    if not anchor_ok:
        return {
            "axis": "ANCHOR",
            "tier": "Tier 1 (load-bearing)",
            "fix": (
                "The gap fires but has no anchor. Put a named person, specific "
                "date, or named place in the first 10 words so the gap becomes a "
                "scene that transports, not an abstraction."
            ),
        }
    if not timing_ok:
        return {
            "axis": "TIMING",
            "tier": "Tier 1 (load-bearing)",
            "fix": (
                "Gap and anchor are present but the gap opens too late. Compress "
                "the primer so a specific unknown is named by sentence 3."
            ),
        }
    if eves["hockey_stick_risk"]:
        return {
            "axis": "FULFILLMENT",
            "tier": "Tier 2 (multiplier)",
            "fix": (
                "Title/thumbnail promise is not honored in the opener's first "
                "seconds. Name the promised entity and deliver the promised "
                "promise-type (document / conflict / myth-bust) up front."
            ),
        }
    if not q["sentence_1_parses_cleanly"]["passed"]:
        return {
            "axis": "EASE",
            "tier": "Tier 2 (multiplier)",
            "fix": (
                "Sentence 1 strains the ear. Shorten to <=13 words, drop hedging "
                "and subordinate clauses; read it aloud without stumbling."
            ),
        }
    return {
        "axis": "POLISH",
        "tier": "Tier 3 (marginal)",
        "fix": (
            "Tier 1 and Tier 2 conditions pass. Remaining work is polish: "
            "stikomythia rhythm, shot change <12s, suspense-sentence structure."
        ),
    }


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def diagnose_opener(
    text: str,
    title: str,
    topic_type: Optional[str] = None,
    thumbnail: Optional[str] = None,
) -> Dict[str, Any]:
    """Run the expert 60-second opener lens over an opener's first ~30 seconds.

    This is a FILTER (necessary conditions), not a predictor — see module
    docstring. Heuristic checks are flagged `heuristic=True` in their results.

    Args:
        text:       The opener narration (first ~30s). Markdown/B-roll markers ok.
        title:      The video title — drives the Eves hockey-stick / fulfillment test.
        topic_type: Optional ('territorial' | 'ideological' | 'political_fact_check'
                    | 'general'). Inferred from `text` when omitted.
        thumbnail:  Optional thumbnail text — folded into the promise-alignment check.

    Returns a dict with:
        succes:               {score 0-6, principles{...}, heuristic_principles, note}
        diagnostic_questions: the six yes/no questions (each {passed, heuristic})
        eves:                 {hockey_stick_risk, slow_burn_risk, macro_gap_present, ...}
        sentence_1:           {text, checklist{...}}
        top_fix:              {axis, tier, fix}  (gap->anchor->timing hierarchy)
        verdict:              'retains' (>=5) | 'borderline' (4) | 'bleeds' (<=3)
        topic_type, hook_archetype, fulfillment, meta
    """
    cleaned = _clean(text)
    sentences = _split_sentences(cleaned)
    s1 = sentences[0] if sentences else ""

    if not cleaned or len(cleaned.split()) < 8:
        return {
            "error": "Opener too short to evaluate (need >= ~8 words of narration).",
            "succes": {"score": 0, "max": 6, "principles": {}},
            "diagnostic_questions": {},
            "eves": {},
            "sentence_1": {"text": s1, "checklist": {}},
            "top_fix": {"axis": "GAP", "tier": "Tier 1 (load-bearing)",
                        "fix": "Write an opener first."},
            "verdict": "bleeds",
        }

    if topic_type is None:
        topic_type = detect_topic_from_script(cleaned)

    title_entities = _extract_title_entities(title) if title else []
    fulfillment = _check_fulfillment(cleaned, title) if title else {
        "entity_echo": {"passed": False, "matched_entities": [], "title_entities": []},
        "promise_type": {"passed": True, "type": None},
        "fix_suggestion": "",
    }

    succes = _score_succes(cleaned, sentences, title_entities)
    questions = _diagnostic_questions(cleaned, sentences, title_entities, fulfillment)

    macro_gap_present = (
        questions["gap_named_by_sentence_3"]["passed"]
        or questions["gap_feels_painful"]["passed"]
    )
    eves = _eves_tests(cleaned, fulfillment, macro_gap_present, thumbnail)
    top_fix = _choose_top_fix(succes, questions, eves)

    score = succes["score"]
    verdict = "retains" if score >= 5 else ("borderline" if score == 4 else "bleeds")

    # Reuse hook_scorer's archetype + framework signals for context (not gating).
    try:
        hook_archetype = _detect_hook_style(cleaned, _load_pattern_library())
    except Exception:
        hook_archetype = "unknown"

    return {
        "succes": succes,
        "diagnostic_questions": questions,
        "eves": eves,
        "sentence_1": {"text": s1, "checklist": _sentence1_checklist(s1)},
        "top_fix": top_fix,
        "verdict": verdict,
        "topic_type": topic_type,
        "hook_archetype": hook_archetype,
        "fulfillment": fulfillment,
        "framework_signals": _detect_framework(cleaned),
        "meta": {
            "is_filter_not_predictor": True,
            "heuristic_checks": ["diagnostic_questions.prerequisite_knowledge",
                                 "diagnostic_questions.gap_feels_painful",
                                 "diagnostic_questions.surprise_relates_to_argument",
                                 "succes.emotional"],
            "sentence_count_first_30s": len(sentences),
            "word_count": len(cleaned.split()),
        },
    }


# ---------------------------------------------------------------------------
# CLI smoke test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import json

    tripoli = (
        "In 1930, a Dutch scholar named Snouck Hurgronje examined the Arabic "
        "original of an American treaty. The next year, the United States "
        "government printing office published what he found, what he found the "
        "State Department couldn't explain. And, almost 100 years later, neither "
        "can anyone else."
    )
    out = diagnose_opener(
        tripoli,
        title="The Treaty That Proves America Wasn't Founded a Christian Nation",
        topic_type="political_fact_check",
    )
    print(json.dumps(out, indent=2))
