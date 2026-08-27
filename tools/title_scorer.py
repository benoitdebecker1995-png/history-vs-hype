"""
Title Scorer v5 — Grades YouTube title candidates against channel CTR data.

Scores titles 0-100 based on measured CTR from POST-PUBLISH-ANALYSIS files.

⚠️  DATA CONFIDENCE WARNING (audit 2026-03-12):
    - versus (n=4): Only 2 independently verified (3.7% avg, not 4.0%)
    - declarative (n=19): Largest sample, most reliable pattern
    - how_why (n=5): Small but usable
    - question (n=1): SINGLE DATAPOINT — treat as unreliable
    - colon penalty (-28%) / year penalty (-46%): NOT reliable causal effects — confounded
      single-snapshot (2026-02-23) correlations (the channel's #1 and #3 videos BOTH use colons).
      Now graded HEDGE penalties, A/B-testable, never auto-reject — see PACKAGING_MANDATE Tier 2/3.
    - "26x map multiplier" was FALSE (actual: ~1.7x) — removed from scoring

    All CTR snapshots are from a single collection date (2026-02-23).
    Use for directional guidance, not precision targeting.

v4 recalibration (2026-04-08) — audit of 18 published titles vs real CTR:
    BEFORE: 33% error rate (6/18 mismatches). AFTER: 17% (3/18).

    Changes:
    - Context-aware colon penalty: versus+colon ("X vs Y: Stakes") gets -10 not -50.
      Data: "Venezuela vs Guyana: Essequibo" got 4.3% CTR despite colon.
    - Context-aware year penalty: year-as-hook ("Invented in 1828") gets -10 not -50.
      Data: "Flat Earth Myth Was Invented in 1828" got 3.7% CTR despite year.
    - Evidence promise bonus (+10): "Here's the evidence/proof/documents".
      Data: top 2 CTR titles both use evidence promises (9.5%, 5.4%).
    - Named entity bonus (+5): countries, leaders, orgs create specificity.
    - Controversy/myth-busting frame bonus (+5): accusation framing = high CTR.
    - Smarter specific-number detection: excludes "200-Year-Old" adjective patterns.
    - Length sweet spot lowered to 35+ chars (was 40).

    Remaining weaknesses (3 over-scores): titles with good construction but zero
    topic demand still score high. Needs demand multiplier (future work).

Phase 67 recalibration:
    - Added niche benchmark layer (Phase 66 competitor data from channel-data/niche_benchmark.json)
    - Added topic-type grade thresholds (territorial pass=50, political_fact_check pass=75)
    - Added small-sample fallback: when own-channel n < 5, substitute niche benchmark base score
    - Added niche percentile label for context display
    - Grade thresholds now topic-aware (via benchmark_store.TOPIC_GRADE_THRESHOLDS)
    - Backward compatible: no new required args, no existing keys renamed

v5 recalibration (2026-06-10) — PACKAGING_MANDATE re-tier + Fable Phase 1 spec:
    Ref: channel-data/fable-digests/PHASE-1-SCORER-SPEC.md

    C1 — Retire auto-REJECT for style rules (year/colon/the_x_that):
      The auto-reject path fired on the channel's #1 video (29,713 views, colon) and
      #3 video (1,966 views / 4.31% CTR, colon). These were confounded correlations,
      not causal. Style rules are now graded penalties + warnings. Grade is computed
      from score alone. Auto-REJECT survives ONLY for clickbait tone (brand gate).
      --strict CLI flag restores old reject behavior for comparison runs.

    C2 — Rebalance penalty constants (contradicting evidence cited per D1 §4):
      YEAR_PENALTY: -50 → -15 (top-3 videos include year-adjacent formats; HEDGE tier n=6)
      YEAR_PENALTY_HOOK: -10 → -5 ("Invented in 1828" got 3.7% CTR)
      COLON_PENALTY: -50 → -10 (channel's #1/#3 videos both use colons)
      COLON_PENALTY_VERSUS: -10 → 0 ("Venezuela vs Guyana: Essequibo" = 4.31% CTR)
      THE_X_THAT_PENALTY: -50 → -15 (CIA Condor title got 4.91% fresh CTR 2026-06-10)

    C3 — SEARCH_ANCHOR_BONUS (+12):
      New bonus: recognized head term within first 40 characters.
      Recognition: HEAD_TERMS (sovereign states + geographic shorthands) +
      ALLOWED_ACRONYMS + notable-figure surnames. Case-insensitive whole-word match.

    C4 — Version bump to v5; changelog block added.

v6 recalibration (2026-06-27) — FIRST run against COMPLETE per-video CTR (all 56 videos,
    real Studio impressions+CTR ingested into analytics.db; prior calibrations rested on a
    partial 2026-02-23 snapshot, n=33). Ref: channel-data/CTR-TITLE-FORMULA-2026-06.md +
    FLOP-AUTOPSY-PLAN-2026-06.md.

    Findings that CHANGED the model (median CTR delta, present vs absent):
      - FAMOUS subject = the one ROBUST driver: +0.87 (n=31), and it survives stratification
        (within colon=Y AND colon=N). → recognition set broadened to famous events/topics
        (HEAD_TERMS above), not just countries/people.
      - Validated existing bonuses: evidence_promise +1.02 (n=8), controversy_frame +0.68
        (n=17). KEPT as-is.
      - colon's apparent +1.15 is CONFOUNDED by fame — within non-famous titles colon is flat
        (2.23 vs 2.33). The v5 colon de-penalization stands; do NOT add a colon bonus.
      - Over-claims from a 12-extreme pre-analysis that DID NOT generalize and were NOT wired
        in: "visceral predicate" (+0.08) and "abstraction penalty" (+0.10) — both ~zero on
        full data. Deliberately omitted.
    Caveat: n modest, deltas small, fame/topic/title confounded. Scorer is a FILTER; learn
    weights via single-variable native A/B (see feedback-filters-not-predictors).

v6.1 anchor-recognizer repair (2026-07-30) — two defects found running the packaging gate
    for #65 (Enigma). Recognition set only; no weight changed. Pins: tests/unit/test_search_anchor.py

    A1 — Acronyms now match CASE-SENSITIVELY (+ STOPWORD_ACRONYMS guard for ALL-CAPS
      prefixes). "Who Really Broke Enigma?" was returning (True, 'Who') by matching the
      acronym WHO case-insensitively — a spurious PASS on packaging_lock FILTER 1, which
      is BINDING (ADR-0012), so anchorless titles could clear the keyword-ladder gate.
      HEAD_TERMS stay case-insensitive; only the acronym half tightened.

    A2 — HEAD_TERMS widened to notable NON-territorial figures. "Alan Turing Didn't Break
      Enigma First." failed the filter despite "alan turing" = 98,056 est. monthly searches
      (vidIQ). The list was sovereign-state biased by construction; fame is the test.

    Re-baselining: A1 can only REMOVE anchors, A2 can only ADD them, so previously recorded
    packaging-lock verdicts are not automatically still true. validate_lock() recomputes
    the filter from the live title on every read, so no stored AUTO block needs rewriting —
    the recompute is the source of truth. Audited 2026-07-30: no PROJECT-STATUS.md lock
    block on the tree flips verdict under the new recognizer.

v6.2 anchor-recognizer repair (2026-08-03) — two more defects, both found running the gate
    for #67 (Donation of Constantine). Recognition + window only; no weight changed.
    Pins: tests/unit/test_search_anchor.py

    B1 — The 40-char window truncated the title MID-WORD instead of testing the match's
      START position, so a head term beginning inside the window but crossing its edge
      could not match its own word boundary. It false-FAILed the channel's only breakout
      ("...: Guatemala vs Belize", Guatemala@34, 292,398 impressions / 7.66% CTR) plus
      three more live titles (Crusades@37, Viking@35, Genocide@33). Those four straddlers
      hold MORE lifetime impressions than every title the filter passed. Fixed to a start-
      position test; window stays 40 (no catalogue title has a head term starting at 40+,
      so there is evidence for measuring it right, none for widening it).

    B2 — Fame is no longer decided by list membership alone (ADR-0023). The recognizer
      had failed twice in eight days by rejecting genuinely famous terms: "Alan Turing"
      (2026-07-30, 98,056 est. monthly searches) and "Constantine" (2026-08-01, 113,206 —
      while "Vatican" at 100,602 passed). Both were repaired by appending strings to
      HEAD_TERMS, which fixes the instance and leaves the mechanism — a set someone has
      to remember to extend — to fail again on the next unlisted subject. The #67 cost
      was measurable: five title candidates were regenerated away from "Constantine",
      "Pope", "Rome" and "Constantinople" under a constraint that was never real.

      A term now ALSO anchors when a VERIFIED MONTHLY SEARCH VOLUME at or above
      ANCHOR_VOLUME_FLOOR is on record for it in keywords.db — the same store, floor and
      units the /greenlight demand gate already uses. HEAD_TERMS survives as a
      zero-setup fast path, no longer as the definition of fame, and a false FAIL is now
      repaired by recording a measurement (one command, printed in the FAIL message)
      rather than by editing this file. The volume table is read once per process and
      re-read only when keywords.db changes — no network call, no per-title query.

    Also: when several terms match, the earliest now wins (longest breaks a positional
    tie) instead of set-iteration order. The returned term is written verbatim into
    PROJECT-STATUS.md lock blocks, so it is now reproducible.

    Re-baselining: B1 and B2 can only ADD anchors, never remove one, so no previously
    PASSing title can flip to FAIL. validate_lock() recomputes from the live title, so
    no stored AUTO block needs rewriting.

Usage:
    python -m tools.title_scorer "Your Title Here"
    python -m tools.title_scorer "Title A" "Title B" "Title C"
    python -m tools.title_scorer --file titles.txt
    python -m tools.title_scorer "Title Here" --db           # DB-enriched scoring
    python -m tools.title_scorer "Title Here" --db --topic territorial  # Topic-aware grading
    python -m tools.title_scorer --ingest                    # Ingest CTR from synthesis file
    python -m tools.title_scorer --anchor "Title Here"       # Explain the anchor verdict
    python -m tools.title_scorer --record-anchor "Constantine" --volume 113206 \
        --anchor-source vidiq-2026-08-03                     # Teach the gate a famous term
"""

import re
import sqlite3
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from tools.sqlite_access import connect_readonly

# Canonical title-structure logic lives in tools.title_features (ADR-0009).
# `detect_pattern` is re-exported here for backward compat — external callers
# (ctr_quick_add, packaging_autopilot, title_ctr_store) import it from this module.
from tools.title_features import (  # noqa: F401
    pattern as detect_pattern,
    has_year,
    has_specific_number,
    has_active_verb,
    has_evidence_promise,
    has_named_entity,
    has_controversy_frame,
)


# =============================================================================
# TONE SIGNALS — Moved here from metadata.py as authoritative source (Phase 70)
# metadata.py imports CLICKBAIT_PATTERNS and ALLOWED_ACRONYMS from this module.
# =============================================================================

# Clickbait patterns to filter/penalise (from VIDIQ-CHANNEL-DNA-FILTER.md).
#
# Split into two lists 2026-08-03. The single list was matched case-INSENSITIVELY, but it
# mixed two different kinds of thing, and the mix made the BINDING brand gate (FILTER 2 in
# packaging_lock, ADR-0012) reject ordinary sentence-case English:
#
#   "China vs Taiwan. 4 Historical Claims Exposed by Scholars"  → REJECTED on 'EXPOSED'
#
# That is a REAL PUBLISHED title (7,318 lifetime impressions, 2.71% CTR). The list also
# contradicted itself: 'exposed' and 'lied' are in _TONE_SIGNALS['positive'] as approved
# active verbs (+5) while 'EXPOSED' / 'LIED About' were fatal. Same word, rewarded and
# fatal at once. Same defect family as the v6.1 A1 acronym bug: a case-insensitive match
# on a token whose meaning depends on its case.

# (1) Clickbait FRAMES — the construction is clickbait however you case it. There is no
# documentary use of "you won't believe" or "the truth about". Matched case-INSENSITIVELY,
# as substrings (unchanged semantics for these entries).
CLICKBAIT_PHRASES = [
    "You won't believe",          # subsumes the old duplicate "You won't BELIEVE"
    'This will blow your mind',
    "What they don't want you to know",
    'The truth about',
    'Destroyed by facts',         # the meme phrase; bare "destroyed" stays an active verb
    'Mind-blowing',
    'Top 10',
    '5 Reasons Why',
    "3 Things You Didn't Know",
    'The truth they hid',
]

# (2) Tabloid SHOUTING — these words are ordinary English in sentence case and tabloid
# emphasis only when SHOUTED, so the capitalisation IS the violation. Matched
# case-SENSITIVELY on the ALL-CAPS tokens; the surrounding words still match any casing.
# "Claims Exposed by Scholars" is on-brand; "Claims EXPOSED" is not. "Britain Lied About
# the Famine" is the channel's own accusation voice; "Britain LIED About It" is not.
CLICKBAIT_CAPS_MARKERS = [
    'SHOCKING',
    'INSANE',
    'EXPOSED',
    'LIED About',
    'What IT Really Means',
    'How THIS Changed',
]

# Back-compat union — this name is the module's published export (metadata.py, tests).
# Order is phrases-then-markers so detect_clickbait's return order is stable.
CLICKBAIT_PATTERNS = CLICKBAIT_PHRASES + CLICKBAIT_CAPS_MARKERS

# Allowed acronyms (all-caps but NOT clickbait — used in _apply_tone_filter)
ALLOWED_ACRONYMS = [
    'ICJ', 'UN', 'CIA', 'AU', 'EU', 'NATO', 'UNESCO', 'WHO',
    'IMF', 'USSR', 'UK', 'US', 'USA', 'WTO', 'ICC', 'ECHR',
    'OPEC', 'BRICS', 'ASEAN', 'OAS', 'FCDO', 'BIOT', 'PDF',
    'DIY', 'GPS', 'GDP', 'CEO', 'FBI', 'NSA', 'NASA',
    'KGB',  # v5: added — "How the KGB Weaponized..." got highest fresh CTR (18.41% 2026-06-10)
]

# Acronyms that are also ordinary English words. has_search_anchor matched the whole
# acronym list case-INSENSITIVELY until 2026-07-30, so every interrogative "Who" anchored
# on WHO (World Health Organization) — a spurious PASS on the BINDING packaging_lock
# filter (ADR-0012). These anchor only on an exact-case match, and only when the title's
# casing carries information: an ALL-CAPS prefix has no case signal, so they are skipped
# there. Kept broader than today's ALLOWED_ACRONYMS so future additions inherit the guard.
STOPWORD_ACRONYMS = {
    'WHO', 'US', 'IT', 'IN', 'AT', 'ON', 'NO', 'SO', 'OR', 'WAS', 'AM', 'BE',
    'AN', 'AS', 'BY', 'DO', 'HE', 'IF', 'IS', 'ME', 'MY', 'OF', 'TO', 'UP', 'WE',
}

# =============================================================================
# SEARCH ANCHOR HEAD TERMS (v5 — C3; demoted to a fast path 2026-08-03, ADR-0023)
#
# Sovereign states, geographic shorthands, famous topics and notable figures whose
# fame nobody would argue about. This set is a ZERO-SETUP FAST PATH, not the
# definition of a search anchor: a term also anchors on a verified search volume at
# or above ANCHOR_VOLUME_FLOOR recorded in keywords.db (see find_search_anchor).
#
# It exists because a fresh clone with an empty keyword table must still recognise
# "France". It is NOT the place to fix a false FAIL — see the note at the end of
# the set, and ADR-0023 for why three list patches in eight weeks was the signal.
# =============================================================================
HEAD_TERMS = {
    # Sovereign states (common English names + shorthands)
    'Afghanistan', 'Albania', 'Algeria', 'Angola', 'Argentina', 'Armenia',
    'Australia', 'Austria', 'Azerbaijan', 'Bahrain', 'Bangladesh', 'Belarus',
    'Belgium', 'Belize', 'Bolivia', 'Bosnia', 'Brazil', 'Britain', 'Bulgaria',
    'Cambodia', 'Cameroon', 'Canada', 'Chile', 'China', 'Colombia', 'Congo',
    'Croatia', 'Cuba', 'Cyprus', 'Czechia', 'Denmark', 'Ecuador', 'Egypt',
    'England', 'Ethiopia', 'Finland', 'France', 'Georgia', 'Germany', 'Ghana',
    'Greece', 'Guatemala', 'Guinea', 'Haiti', 'Honduras', 'Hungary', 'India',
    'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica',
    'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kosovo', 'Kuwait', 'Laos',
    'Lebanon', 'Libya', 'Lithuania', 'Luxembourg', 'Malaysia', 'Mali',
    'Malta', 'Mexico', 'Moldova', 'Mongolia', 'Morocco', 'Mozambique',
    'Myanmar', 'Namibia', 'Nepal', 'Netherlands', 'Nicaragua', 'Niger',
    'Nigeria', 'Norway', 'Oman', 'Pakistan', 'Palestine', 'Panama', 'Paraguay',
    'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia',
    'Rwanda', 'Saudi', 'Scotland', 'Senegal', 'Serbia', 'Somalia', 'Somaliland',
    'Spain', 'Sudan', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tanzania',
    'Thailand', 'Tibet', 'Togo', 'Tunisia', 'Turkey', 'Uganda', 'Ukraine',
    'Uruguay', 'Uzbekistan', 'Venezuela', 'Vietnam', 'Wales', 'Yemen',
    'Zambia', 'Zimbabwe',
    # Geographic shorthands and disputed territories
    'Balkans', 'Biot', 'Bir Tawil', 'Chagos', 'Crimea', 'Essequibo',
    'Kashmir', 'Kurdistan', 'Manchuria', 'Manhattan', 'Nagorno', 'Sahel',
    'Sinai', 'Somaliland', 'Transnistria', 'Guyana', 'Belize',
    'Western Sahara', 'South Sudan', 'North Korea', 'South Korea',
    'Saudi Arabia', 'United Kingdom', 'United States',
    # Notable figure surnames (channel corpus)
    'Churchill', 'Columbus', 'Cromwell', 'Fuentes', 'Hancock', 'Hitler',
    'Lenin', 'Lincoln', 'Machiavelli', 'Mao', 'Marx', 'Napoleon', 'Petain',
    'Putin', 'Saladin', 'Stalin', 'Trump', 'Vance',
    # Current high-search world figures (added 2026-07-01 — the recognizer false-FAILed
    # #62's "Zelensky ..." title, which genuinely leads with a famous searchable parent).
    'Zelensky', 'Zelenskyy', 'Netanyahu', 'Bandera', 'Erdogan', 'Modi', 'Biden',
    # Famous events / topics / movements (2026-06-27 recalibration — see header note).
    # Fame is the one robust title CTR driver (+0.87% median, n=31, survives stratification
    # by colon). Recognition was previously countries+people only; famous *topics* a general
    # audience reacts to are anchors too, so they earn SEARCH_ANCHOR_BONUS.
    'Crusades', 'Crusade', 'Inquisition', 'Holocaust', 'Cold War', 'Flat Earth',
    'Atlantis', 'Vikings', 'Viking', 'Nazi', 'Nazis', 'Apartheid', 'Genocide',
    'Reformation', 'Renaissance', 'Dark Ages', 'Roman Empire', 'Ottoman',
    'Templars', 'Pharaoh', 'Aztec', 'Maya', 'Samurai', 'Mongol', 'Mongols',
    # Charged cultural/religious anchors a general audience reacts to + searches (fame driver).
    'Hijab', 'Veil', 'Islam', 'Islamic', 'Sharia', 'Quran', 'Bible', 'Vatican',
    'Slavery', 'Slave Trade',
    # Notable NON-territorial figures (2026-07-30 — the recognizer false-FAILed #65's
    # "Alan Turing Didn't Break Enigma First. Poland Did."; "alan turing" = 98,056 est.
    # monthly searches, vidIQ). The list above is sovereign-state biased by construction,
    # which blocked science-, ideas- and law-led subjects at lock time even when the
    # subject outsearches most of the states already recognised. Fame is the anchor test,
    # not geography — same reasoning as the 2026-06-27 famous-topics widening.
    'Turing', 'Alan Turing', 'Einstein', 'Darwin', 'Galileo', 'Newton', 'Tesla',
    'Copernicus', 'Oppenheimer', 'Freud', 'Orwell', 'Marco Polo', 'Da Vinci',
    'Gandhi', 'Mandela', 'Guevara', 'Mussolini', 'Trotsky', 'Khrushchev', 'Beria',
    'Rasputin', 'Genghis Khan', 'Caesar', 'Cleopatra', 'Bismarck', 'Kissinger',
    'Thatcher', 'Roosevelt', 'Kennedy', 'Nixon', 'Reagan', 'Truman', 'Pol Pot',
    'Leopold', 'Cecil Rhodes', 'Mengele', 'Eichmann', 'Himmler', 'Goebbels',
    # STOP. Do not fix a false FAIL by adding a line here — that is the failure mode
    # ADR-0023 exists to end (three symptomatic patches in eight weeks: Zelensky
    # 2026-07-01, Alan Turing 2026-07-30, the classical/medieval cluster 2026-08-03).
    # Record the measured volume instead; it takes one command and leaves an audit trail:
    #   python -m tools.title_scorer --record-anchor "<term>" --volume <n/mo> \
    #       --anchor-source vidiq-YYYY-MM-DD
}

# Characters from the start of the title within which a head term must BEGIN to count
# as an anchor. See find_search_anchor for why "begin" (not "fit entirely") is the rule.
ANCHOR_WINDOW_CHARS = 40

# Verified monthly searches at or above which a term counts as a head term regardless
# of whether anyone listed it (ADR-0023). Deliberately the SAME number as the
# /greenlight demand gate's GO line (.claude/rules/packaging.md §1: GO >=1,000/mo,
# CAUTION 500-999, STOP <500) — one volume vocabulary in the repo, not two. The claim
# it encodes is modest and testable: a term people search 1,000+ times a month is a
# term a viewer recognises in a thumbnail-sized glance, which is all the anchor rule
# asks for. Volumes come from vidIQ via keywords.db; see record_anchor_volume.
ANCHOR_VOLUME_FLOOR = 1000

# Unified tone signals dict — positive (active verbs) and negative (clickbait)
_TONE_SIGNALS = {
    'positive': [
        'destroyed', 'erased', 'redrew', 'deleted', 'stole', 'conquered',
        'invaded', 'betrayed', 'exposed', 'revealed', 'weaponized', 'carved',
        'divided', 'partitioned', 'annexed', 'ruled', 'fought', 'claimed',
        'debunked', 'proved', 'disproved', 'lied', 'fabricated',
    ],
    'negative': CLICKBAIT_PATTERNS,
}


def _caps_marker_regex(pattern: str) -> 're.Pattern[str]':
    """Compile a CLICKBAIT_CAPS_MARKERS entry: ALL-CAPS tokens must be SHOUTED in the
    title; every other token matches in any casing.

    'LIED About'  -> LIED must be capitalised, "about" need not be.
    'EXPOSED'     -> matches "EXPOSED", never "Exposed".
    """
    parts = []
    for tok in pattern.split():
        if tok.isupper() and any(c.isalpha() for c in tok):
            parts.append(re.escape(tok))                 # the shout is the violation
        else:
            parts.append(f'(?i:{re.escape(tok)})')       # casing carries no signal here
    return re.compile(r'\b' + r'\s+'.join(parts) + r'\b')


_CAPS_MARKER_RE = {p: _caps_marker_regex(p) for p in CLICKBAIT_CAPS_MARKERS}


def detect_clickbait(title: str) -> list[str]:
    """Return the clickbait tone patterns present in a title.

    This is the BRAND GATE: any hit makes score_title reject the title (grade REJECTED),
    regardless of composite score. Style hedges (year/colon/the_x_that) are NOT clickbait —
    they stay non-fatal style_warnings. Restored 2026-07-01: the gate was documented
    ("hard_rejects populated by _apply_tone_filter") but that function never existed, so
    hard_rejects was dead code and clickbait titles ("...SHOCKING") scored clean.

    Matching is asymmetric (2026-08-03), for the same reason has_search_anchor's is:
      - CLICKBAIT_PHRASES match case-INSENSITIVELY. "The Truth About X" is a clickbait
        frame in any casing.
      - CLICKBAIT_CAPS_MARKERS match case-SENSITIVELY on their ALL-CAPS tokens, because
        those words are ordinary English in sentence case. Matching them loosely rejected
        "China vs Taiwan. 4 Historical Claims Exposed by Scholars" — a published title
        with 7,318 lifetime impressions — on a BINDING filter.

    Never raises; returns [] for an empty or unusual title.
    """
    hits = [p for p in CLICKBAIT_PHRASES if p.lower() in title.lower()]
    hits += [p for p, rx in _CAPS_MARKER_RE.items() if rx.search(title)]
    return hits


def strip_clickbait(title: str) -> str:
    """Remove clickbait patterns from a title, honouring the same case rules as
    detect_clickbait. Used by metadata.py's title generator, which must not silently
    delete an ordinary word like "Exposed" from an otherwise on-brand title.

    Whitespace is left for the caller to normalise. Never raises.
    """
    for phrase in CLICKBAIT_PHRASES:
        title = re.sub(re.escape(phrase), '', title, flags=re.IGNORECASE)
    for rx in _CAPS_MARKER_RE.values():
        title = rx.sub('', title)
    return title


def compute_tone_score(title: str) -> int:
    """
    Return a tone score for a title.

    +ACTIVE_VERB_BONUS (+5) for each active verb found.
    -10 per clickbait pattern found (via detect_clickbait, so the case rules match the
    brand gate — these used to disagree, and the old duplicate "You won't BELIEVE" entry
    double-charged a single phrase).

    Neutral title (no active verb, no clickbait) -> 0.
    """
    score = 0
    t = title.lower()
    if any(v in t for v in _TONE_SIGNALS['positive']):
        score += ACTIVE_VERB_BONUS
    score -= 10 * len(detect_clickbait(title))
    return score


# =============================================================================
# CTR DATA — Measured from 33 videos with CTR (2026-03-07)
# Source: collect_video_data() → POST-PUBLISH-ANALYSIS files
# =============================================================================

# Pattern base scores (from measured avg CTR, scaled 0-100)
# ⚠️  Confidence levels based on 2026-03-12 data audit:
# versus:     ~3.7% CTR (n=2 verified, n=4 claimed) — MEDIUM confidence
# declarative: 3.8% CTR (n=19) — HIGHEST confidence (largest sample)
# how_why:    3.3% CTR (n=5)   — MEDIUM confidence
# question:   2.4% CTR (n=1)   — LOW confidence (single video!)
# colon:      2.3% CTR (n=4+)  — HIGH confidence (penalty confirmed)
# the_x_that: no data (n=0)    — all retitled away; assumed worst
PATTERN_SCORES = {
    'versus': 75,        # ~3.7% CTR — best measured, but n=2 verified
    'declarative': 65,   # 3.8% CTR — most reliable (n=19)
    'how_why': 55,       # 3.3% CTR — moderate sample
    'question': 45,      # 2.4% CTR — WARNING: n=1 only, bumped from 40 to reduce false confidence
    'colon': 30,         # 2.3% CTR — confirmed penalty (high confidence)
    'the_x_that': 10,    # No current data — assumed worst from prior retitling
}

# Re-export for consumers who import from title_scorer
# (benchmark_store is the authoritative source; this is a convenience alias)
from tools.benchmark_store import TOPIC_GRADE_THRESHOLDS  # noqa: E402

# Penalty/bonus modifiers (all measured from real channel data)
# v4 recalibration (2026-04-08): context-aware penalties replace blanket hard rejects
# v5 recalibration (2026-06-10): rebalanced per PACKAGING_MANDATE re-tier + D1 §4 evidence
YEAR_PENALTY = -15          # was -50; year as topic label, HEDGE tier (n=6); channel #1 video
                            # has colon+versus which was being over-penalised via adjacent rule
YEAR_PENALTY_HOOK = -5      # was -10; year as hook ("Invented in 1828" got 3.7% CTR)
COLON_PENALTY = -10         # was -50; style preference only — top-3 videos all have colons
                            # (D1 §4: Y21EjQ0v9W4=29,713 views, oDK52GwjTIo=4.31% CTR)
COLON_PENALTY_VERSUS = 0    # was -10; "X vs Y: Stakes" = channel #3 video's exact format
                            # (D1 §4: oDK52GwjTIo "Venezuela vs Guyana: ..." got 4.31% CTR)
THE_X_THAT_PENALTY = -15    # was -50; CIA Condor title ("The CIA Document That Proved...")
                            # got 4.91% fresh CTR 2026-06-10 snapshot (D1 dossier)
SEARCH_ANCHOR_BONUS = 12    # v5 new: recognized head term in first 40 chars (C3)
STALENESS_WARN_DAYS = 45    # warn when the newest live CTR snapshot is older than this
LENGTH_SWEET_SPOT = (35, 70)  # Optimal character range for mobile (v4: lowered from 40)
LENGTH_PENALTY_SHORT = -5   # Too short = vague
LENGTH_PENALTY_LONG = -10   # Too long = truncated on mobile
SPECIFIC_NUMBER_BONUS = 10  # Specific numbers in title improve CTR
ACTIVE_VERB_BONUS = 5       # Active verbs = +4.5% CTR (n=4 vs n=29, weak but positive)
SCALE_WORD_BONUS = 5        # Scale words = 1.33x lift in outlier videos (650 videos, 14 channels)
TWO_SENTENCE_BONUS = 5      # Two-sentence formula = 11% outlier rate (strongest structural pattern)
EVIDENCE_PROMISE_BONUS = 10 # "Here's the evidence/proof/documents" — top CTR titles use this
ENTITY_BONUS = 5            # Named countries, leaders, or orgs — specificity drives clicks
CONTROVERSY_BONUS = 5       # Accusation/myth-busting framing — top CTR signal on this channel

# Scale words from outlier_title_dissector analysis
_SCALE_WORDS = {
    'every', 'all', 'entire', 'whole', 'century', 'centuries',
    'forever', 'million', 'billion', 'thousand', 'empire', 'world',
    'continent', 'civilization', 'generation', 'generations',
}

# Minimum own-channel sample count before niche fallback is triggered (BENCH-02)
_OWN_CHANNEL_MIN_SAMPLE = 5


def _year_is_hook(title: str) -> bool:
    """
    Detect if the year in the title serves as a hook/specificity rather than topic label.

    Hook years: embedded in phrases like "invented in 1828", "for 120 years",
    "200-year-old", "since 1953". These add specificity and can boost CTR.

    Label years: "The 1494 Line", "Iran 1979" — year IS the topic framing.
    These get the full penalty.

    Measured: "Flat Earth Myth Was Invented in 1828" got 3.7% CTR despite year.
    """
    t = title.lower()
    # Year preceded by context words = hook usage
    hook_patterns = [
        r'(?:invented|created|started|began|built|written|signed|passed|founded)\s+in\s+\d{4}',
        r'(?:since|from|after|before|until)\s+\d{4}',
        r'\d+-year-old',
        r'for\s+\d+\s+years?',
        r'\d+\s+years?\s+(?:of|ago|later|old)',
    ]
    return any(re.search(p, t) for p in hook_patterns)


def _colon_is_versus_stakes(title: str) -> bool:
    """
    Detect if the colon separates a versus matchup from stakes/subtitle.

    "Venezuela vs Guyana: Who Owns Essequibo?" — colon after versus = stakes framing.
    This is structurally different from "Dark Ages: What Americans Believe" (topic: subtitle).

    Measured: "Venezuela vs Guyana: Essequibo" got 4.3% CTR despite colon.
    """
    # Colon comes AFTER a versus pattern
    colon_pos = title.find(':')
    if colon_pos < 0:
        return False
    before_colon = title[:colon_pos].lower()
    return bool(re.search(r'\bvs\.?\b|\bversus\b', before_colon))


@dataclass(frozen=True)
class AnchorMatch:
    """The outcome of the search-anchor test, with its provenance.

    `has_search_anchor` returns only the (found, term) tuple for backward compat;
    packaging_lock reads the whole thing so the LOCK BLOCK records WHY a title
    anchored — a curated term, or a measured volume with its source (ADR-0023).
    """

    found: bool
    term: str = ''
    start: Optional[int] = None
    volume: Optional[int] = None     # verified monthly searches, when volume-backed
    source: str = ''                 # keywords.db `source` column for that measurement

    def as_tuple(self) -> tuple[bool, str]:
        return (self.found, self.term)

    def describe(self) -> str:
        """One-line audit string for the packaging-lock block."""
        if not self.found:
            return NO_ANCHOR_DETAIL
        where = f'begins at char {self.start}'
        if self.volume is None:
            return f'anchors "{self.term}" (curated head term, {where})'
        return (f'anchors "{self.term}" ({self.volume:,}/mo verified searches, '
                f'source: {self.source}; {where})')


# The FAIL detail is deliberately actionable. A FAIL means one of two very different
# things — "this title leads with something obscure" (rewrite the title) or "this term
# is famous and nobody has measured it yet" (record the measurement). Before ADR-0023
# the message only described the first, and #67 lost five title candidates to the
# second: they were regenerated away from "Constantine" (113,206/mo) under a constraint
# that did not exist.
NO_ANCHOR_DETAIL = (
    'no famous searchable head term begins in the first '
    f'{ANCHOR_WINDOW_CHARS} chars — the obscure entity must be the REVEAL, not the '
    'lead. If the lead term IS famous, this is a data gap and not a verdict: verify '
    'its monthly search volume and record it — python -m tools.title_scorer '
    '--record-anchor "<term>" --volume <n> --anchor-source vidiq-YYYY-MM-DD'
)

_ANCHOR_WORD_RE = re.compile(r"[A-Za-z0-9']+")

# Longest recorded keyword worth testing as a single anchor phrase. Keywords in the
# store run to 7 words ("scramble for africa and the berlin conference"); 8 covers
# them with headroom and caps the per-title lookup count at a few dozen dict hits.
_MAX_ANCHOR_WORDS = 8

# {db_path: ((mtime, size), floor, table)} — the volume table is rebuilt only when
# keywords.db actually changes, so has_search_anchor stays cheap enough for the
# scoring loops that call it once per candidate. No network call, ever.
_ANCHOR_VOLUME_CACHE: dict = {}


def _default_keywords_db() -> Path:
    """Path-anchored to the repo, never cwd-relative (ADR-0008)."""
    return Path(__file__).resolve().parents[1] / 'tools' / 'discovery' / 'keywords.db'


def _fold_token(token: str) -> str:
    """Lowercase a word and drop a trailing possessive.

    "Pope's" folds to "pope" because a viewer searching `pope` recognises the title
    "The Pope's Own Coins…" — the possessive is grammar, not a different subject.
    Applied to both sides of the comparison, so it cannot create a one-sided match.
    Plain plurals are deliberately left alone ("popes" stays "popes"): stripping them
    would start guessing at morphology instead of folding punctuation.
    """
    return re.sub(r"'s$|'$", '', token.lower())


def normalize_anchor_term(term: str) -> str:
    """Fold a term to its comparison form: lowercase words, single-spaced.

    Applied to BOTH sides, so "Brest-Litovsk" in a title and "brest-litovsk" in the
    keyword store fold to the same key.
    """
    return ' '.join(_fold_token(m.group(0)) for m in _ANCHOR_WORD_RE.finditer(term))


def load_anchor_volumes(
    db_path: Optional[str] = None,
    floor: Optional[int] = None,
) -> dict:
    """Return {normalized term: (monthly_volume, source)} for every keyword at or
    above the anchor floor.

    Read-only and never raises — a missing/locked/older-schema keywords.db yields an
    empty table, which degrades the recognizer to its curated fast path rather than
    breaking the packaging gate. Opens its own read-only connection (no schema
    migration side effects on a hot read) but runs the query through KeywordStore,
    which owns the keywords table.
    """
    floor = ANCHOR_VOLUME_FLOOR if floor is None else floor
    path = Path(db_path) if db_path else _default_keywords_db()
    try:
        stat = path.stat()
        stamp = (stat.st_mtime, stat.st_size)
    except OSError:
        return {}

    key = str(path)
    cached = _ANCHOR_VOLUME_CACHE.get(key)
    if cached is not None and cached[0] == stamp and cached[1] == floor:
        return cached[2]

    try:
        from tools.discovery.keyword_store import KeywordStore
        conn = connect_readonly(path)
        try:
            conn.row_factory = sqlite3.Row
            rows = KeywordStore(conn).get_keywords_above_volume(floor)
        finally:
            conn.close()
    except Exception:
        return {}

    table: dict = {}
    for row in rows:
        norm = normalize_anchor_term(row.get('keyword') or '')
        volume = row.get('search_volume') or 0
        if not norm or volume < floor:
            continue
        previous = table.get(norm)
        if previous is None or volume > previous[0]:
            table[norm] = (int(volume), row.get('source') or 'unrecorded')

    _ANCHOR_VOLUME_CACHE[key] = (stamp, floor, table)
    return table


def record_anchor_volume(
    term: str,
    volume: int,
    source: str,
    db_path: Optional[str] = None,
) -> dict:
    """Record a verified monthly search volume for a term, making it an anchor.

    This is the sanctioned repair for a false FAIL — the replacement for editing
    HEAD_TERMS by hand (ADR-0023). `source` must say where the number came from and
    when ("vidiq-2026-08-03"): it is copied into the packaging-lock block as the
    audit trail for every title that later anchors on this term.

    Returns the KeywordStore result dict, or {'error': ...}. Never raises.
    """
    if volume < ANCHOR_VOLUME_FLOOR:
        return {'error': f'{volume} is below ANCHOR_VOLUME_FLOOR ({ANCHOR_VOLUME_FLOOR}/mo) '
                         f'— a term this rarely searched is not a head term'}
    try:
        from tools.discovery.keyword_store import KeywordStore
        store = KeywordStore.connect(db_path or str(_default_keywords_db()))
        try:
            result = store.add_keyword(term.strip(), source=source, search_volume=int(volume))
        finally:
            store.close()
    except Exception as e:
        return {'error': f'could not record anchor volume: {type(e).__name__}: {e}'}
    _ANCHOR_VOLUME_CACHE.clear()
    return result


def _anchor_ngrams(title: str):
    """Yield (normalized_ngram, start, surface) for word n-grams BEGINNING in the window."""
    toks = [(_fold_token(m.group(0)), m.start(), m.end())
            for m in _ANCHOR_WORD_RE.finditer(title)]
    for i in range(len(toks)):
        start = toks[i][1]
        if start >= ANCHOR_WINDOW_CHARS:
            break
        for j in range(i, min(len(toks), i + _MAX_ANCHOR_WORDS)):
            gram = ' '.join(t[0] for t in toks[i:j + 1])
            yield gram, start, title[start:toks[j][2]]


def find_search_anchor(title: str, db_path: Optional[str] = None) -> AnchorMatch:
    """
    Detect whether a recognized head term BEGINS within the first ANCHOR_WINDOW_CHARS.

    Two independent recognizers, one decision (ADR-0023):

      1. CURATED — HEAD_TERMS + ALLOWED_ACRONYMS. Zero setup, works on a fresh clone,
         no I/O. It is a floor on what counts as famous, never the definition.
      2. MEASURED — any term with a verified monthly search volume at or above
         ANCHOR_VOLUME_FLOOR recorded in keywords.db. This is what makes the gate
         self-repairing: a famous subject nobody thought to list still anchors as soon
         as its demand is measured, and /greenlight measures demand anyway.

    Returns an AnchorMatch carrying the provenance (curated, or volume + source), so
    the packaging-lock block records WHY the title passed rather than just that it did.

    Matching is asymmetric, and deliberately so (2026-07-30):
      - HEAD_TERMS match case-INSENSITIVELY. They are proper nouns whose lowercase
        form means the same thing, so casing carries no information.
      - ALLOWED_ACRONYMS match case-SENSITIVELY, because several are homographs of
        ordinary English words. Matching them loosely made "Who Really Broke Enigma?"
        anchor on WHO (World Health Organization) — a spurious PASS on FILTER 1 of
        packaging_lock (ADR-0012), which is binding, not advisory. STOPWORD_ACRONYMS
        are additionally skipped when the prefix is ALL CAPS and case tells us nothing.

    The window is a START position, not a substring (fixed 2026-08-03). This used to
    match against `title[:40]`, which truncates the title MID-WORD, so a term that
    starts inside the window but crosses its edge could not match its own \\b boundary.
    That silently failed the channel's only breakout — "The Country That Might
    Disappear: Guatemala vs Belize" (292,398 impressions, 7.66% CTR) — because
    "Guatemala" begins at char 34 and `title[:40]` leaves only "Guatem". Three more
    live titles straddled the same edge (Crusades@37 5.47%, Viking@35 2.29%,
    Genocide@33 7.45%); together the four straddlers hold MORE lifetime impressions
    than every title the filter passed. The rule the window is meant to encode is
    "the title leads with a famous searchable parent", and a term that starts at
    char 34 leads with one. The window itself is unchanged at 40: no title in the
    catalogue has a head term starting at or beyond 40, so there is no evidence for
    widening it, only for measuring it correctly.

    When several terms match, the EARLIEST one wins (longest term breaks a tie at the
    same position; a measured term breaks a tie against an identical curated one, so the
    block records the number). That is a contract: the returned term is written verbatim
    into the packaging-lock block in PROJECT-STATUS.md, so it must not depend on set
    iteration order.

    A miss on an obscure-but-valid term is acceptable — the gate is a floor, not an
    oracle, and the FAIL message says how to correct a term it does not know yet.
    Cheap by construction: regex over a short title plus cached dict lookups, no API call.
    """
    best_key = None
    best = AnchorMatch(False)

    def _consider(start: int, surface: str,
                  volume: Optional[int] = None, source: str = '') -> None:
        nonlocal best_key, best
        if start >= ANCHOR_WINDOW_CHARS:
            return
        # Earliest wins; then longest; then measured over curated (richer audit trail).
        key = (start, -len(surface), 0 if volume is not None else 1)
        if best_key is None or key < best_key:
            best_key = key
            best = AnchorMatch(True, surface, start, volume, source)

    for term in HEAD_TERMS:
        m = re.search(r'\b' + re.escape(term) + r'\b', title, re.IGNORECASE)
        if m:
            _consider(m.start(), m.group(0))

    # The ALL-CAPS guard still reads the WINDOW, not the whole title: it asks whether
    # the part of the title that can carry an anchor has any case signal to read.
    prefix_has_no_case_signal = title[:ANCHOR_WINDOW_CHARS].isupper()
    for term in ALLOWED_ACRONYMS:
        if prefix_has_no_case_signal and term in STOPWORD_ACRONYMS:
            continue
        m = re.search(r'\b' + re.escape(term) + r'\b', title)
        if m:
            _consider(m.start(), m.group(0))

    volumes = load_anchor_volumes(db_path)
    if volumes:
        for gram, start, surface in _anchor_ngrams(title):
            entry = volumes.get(gram)
            if entry is not None:
                _consider(start, surface, entry[0], entry[1])

    return best


def has_search_anchor(title: str) -> tuple[bool, str]:
    """Backward-compatible tuple view of find_search_anchor (v5 C3).

    Returns (found: bool, matched_term: str); matched_term is '' when not found.
    Callers that need the provenance — the volume and where it was measured — should
    call find_search_anchor directly and read AnchorMatch.

    NOTE the trap this signature sets: `if has_search_anchor(t):` is True even for a
    NOT-FOUND result, because a 2-tuple is always truthy. Unpack it.
    """
    return find_search_anchor(title).as_tuple()


def _get_pattern_sample_count(db_path: str, pattern: str) -> int:
    """
    Return the number of own-channel videos in the DB for a given title pattern.

    Uses the same query logic as title_ctr_store: joins ctr_snapshots with
    video_performance, picks latest non-zero CTR snapshot per video, then
    detects the pattern for each title.

    Returns 0 on any failure (missing DB, schema error, import error, etc.).
    Never raises.
    """
    try:
        conn = connect_readonly(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT vp.title
            FROM video_performance vp
            JOIN ctr_snapshots cs ON cs.video_id = vp.video_id
            WHERE cs.ctr_percent > 0
              AND vp.title IS NOT NULL
              AND cs.snapshot_date = (
                  SELECT MAX(cs2.snapshot_date)
                  FROM ctr_snapshots cs2
                  WHERE cs2.video_id = vp.video_id
                    AND cs2.ctr_percent > 0
              )
            """
        )
        rows = cursor.fetchall()
        conn.close()
    except Exception:
        return 0

    count = sum(1 for row in rows if detect_pattern(row["title"]) == pattern)
    return count


def _niche_percentile_label(final: int, pattern: str, niche_data: Optional[dict]) -> str:
    """
    Compare final score against niche median for the pattern.

    Returns a human-readable label describing where the title falls in the niche.
    Returns empty string if niche_data is None or pattern not found.

    Labels:
        "top third of niche"     — final >= 1.5x niche median score
        "above niche median"     — final >= niche median score
        "below niche median"     — final >= 0.5x niche median score
        "bottom quartile of niche" — final < 0.5x niche median score
    """
    if niche_data is None:
        return ""

    by_pattern = niche_data.get("by_pattern", {})
    entry = by_pattern.get(pattern)
    if entry is None:
        return ""

    try:
        from tools.benchmark_store import _vps_to_score
        median_score = _vps_to_score(entry["median_vps"])
    except Exception:
        return ""

    if median_score <= 0:
        return ""

    if final >= int(median_score * 1.5):
        return "top third of niche"
    elif final >= median_score:
        return "above niche median"
    elif final >= int(median_score * 0.5):
        return "below niche median"
    else:
        return "bottom quartile of niche"


# ── how well this instrument has actually predicted anything ──────────────────
#
# ADR-0020: an artifact carries its own limits wherever it is cited. A composite
# score with no stated validity gets read as evidence — on 2026-08-03 a "100/A"
# was treated as reassurance, and a −0.053 computed against the WRONG column
# (videos.impressions is a trailing snapshot; see ADR-0024) was used to argue the
# scorer should be ignored entirely. Both readings were wrong. Publish the number.
#
# Re-measure by scoring every title in studio_ctr_rows (lifetime grain, via
# AnalyticsStore.lifetime_ctr_by_video) against its lifetime CTR, and update this
# block with the new r, n and date. Do NOT measure against `videos`.
SCORE_CALIBRATION = {
    'r': 0.155,
    'n': 35,
    'measured_against': 'lifetime CTR (studio_ctr_rows)',
    'population': 'videos with >=2,000 lifetime impressions',
    'measured_on': '2026-08-03',
    'strength': 'WEAK',
    'reading': (
        'Weakly positive. Informs, does not decide — a high score is not evidence '
        'a title will perform, and a low one is not evidence it will not. '
        'ADR-0012: filters decide, scores inform.'
    ),
}


def score_title(title: str, db_path: str = None, topic_type: str = None, experimental: bool = False, strict: bool = False) -> dict:
    """
    Score a title candidate 0-100 with niche benchmark context and topic-type grading.

    Args:
        title:      YouTube title candidate string.
        db_path:    Optional path to keywords.db. When provided, pattern base scores
                    are sourced from real CTR data (if sufficient samples exist).
                    When own-channel sample count < 5 for this pattern AND niche data
                    is available, the niche benchmark score is substituted as base
                    (BENCH-02: small-sample fallback). Falls back silently to static
                    PATTERN_SCORES when DB unavailable. Pass None (default) for
                    fully static scoring — backward-compatible behavior.
        topic_type: Optional topic type string (e.g., 'territorial',
                    'political_fact_check'). When None, auto-detected from title
                    using classify_topic_type() from performance.py, then normalized
                    via benchmark_store.normalize_topic_type(). Pass explicitly to
                    override auto-detection.

    Returns:
        Dict with score, breakdown, and suggestions. New keys vs Phase 66:
        - niche_enriched (bool): True if niche benchmark base score was used.
        - niche_base_score (int|None): The niche-derived score, or None.
        - fallback_warning (str|None): Message when niche substitution happened.
        - detected_topic (str): Normalized topic type used for grading.
        - topic_type_target (dict): {'pass', 'good', 'gap_message'} for the topic.
        - niche_percentile_label (str): Where title falls in niche, or empty str.

    Backward-compatibility note:
        When db_path=None and topic_type=None, grade thresholds use 'general'
        defaults (pass=60, good=70) mapping to A=85+, B=70+, C=60+, D=45+.
        This is a slight shift from v1 (A=80, B=65, C=50, D=35) and is an
        intentional recalibration per BENCH-01 (raise bar to niche standard).
    """
    title = title.strip()
    pattern = detect_pattern(title)

    # ------------------------------------------------------------------
    # 1. Topic type detection
    # ------------------------------------------------------------------
    from tools.benchmark_store import (
        normalize_topic_type,
        get_topic_thresholds,
        get_niche_score,
        load as _bs_load,
    )

    if topic_type is not None:
        # Caller-supplied: normalize to niche taxonomy
        normalized_topic = normalize_topic_type(topic_type)
    else:
        # Auto-detect using performance.py classify_topic_type()
        try:
            from tools.youtube_analytics.performance import classify_topic_type
            raw_topic = classify_topic_type(title)
        except Exception:
            raw_topic = 'general'
        normalized_topic = normalize_topic_type(raw_topic)

    thresholds = get_topic_thresholds(normalized_topic)

    # ------------------------------------------------------------------
    # 2. Load niche benchmark data (for base score and percentile label)
    # ------------------------------------------------------------------
    niche_data = _bs_load()
    niche_base_score_for_pattern = get_niche_score(pattern, niche_data)

    # ------------------------------------------------------------------
    # 3. Own-channel DB lookup (existing logic)
    # ------------------------------------------------------------------
    db_overrides = {}
    if db_path is not None:
        try:
            from tools.title_ctr_store import get_pattern_ctr_from_db
            db_overrides = get_pattern_ctr_from_db(db_path)
        except Exception:
            pass  # Silent fallback — never crash due to DB issues

    db_base_score = db_overrides.get(pattern)  # None if not in DB
    db_enriched = db_base_score is not None

    # Staleness of the live-CTR data behind a DB-enriched score (informational).
    # The scorer's static PATTERN_SCORES rest on a 2026-02-23 snapshot; --db reads
    # live ctr_snapshots. Report how old the newest snapshot is so a stale DB is visible.
    staleness_days: Optional[int] = None
    snapshot_date: Optional[str] = None
    if db_path is not None:
        try:
            from tools.title_ctr_store import get_latest_snapshot_date
            from datetime import date
            snapshot_date = get_latest_snapshot_date(db_path)
            if snapshot_date:
                y, m, d = (int(x) for x in snapshot_date[:10].split('-'))
                staleness_days = (date.today() - date(y, m, d)).days
        except Exception:
            pass  # never crash on staleness reporting

    # ------------------------------------------------------------------
    # 4. Small-sample fallback (BENCH-02)
    #    When db_path provided AND own-channel n < _OWN_CHANNEL_MIN_SAMPLE
    #    AND niche base score is available: substitute niche score as base.
    # ------------------------------------------------------------------
    fallback_warning: Optional[str] = None
    niche_enriched = False
    niche_base_score = niche_base_score_for_pattern  # informational (may be None)

    if db_path is not None:
        own_sample_count = _get_pattern_sample_count(db_path, pattern)
        if own_sample_count < _OWN_CHANNEL_MIN_SAMPLE and niche_base_score_for_pattern is not None:
            # Substitute niche benchmark as base score
            base = niche_base_score_for_pattern
            niche_enriched = True
            fallback_warning = (
                f"Using niche benchmark (only {own_sample_count} internal examples, "
                f"need {_OWN_CHANNEL_MIN_SAMPLE})"
            )
            # Override db_enriched: own-channel base is being replaced by niche
            db_enriched = False
            db_base_score = None
        elif db_enriched:
            base = db_base_score
        else:
            base = PATTERN_SCORES.get(pattern, 50)
    else:
        # Static mode (no db_path): use PATTERN_SCORES; niche data is context only
        base = PATTERN_SCORES.get(pattern, 50)

    # ------------------------------------------------------------------
    # 5. Penalties, bonuses, hard rejects, style warnings
    #
    # v5 (C1): style rules (year/colon/the_x_that) move to style_warnings;
    # grade is computed from score alone.  auto-REJECT survives ONLY for
    # clickbait tone (brand gate).  --strict CLI flag restores v4 behavior.
    # ------------------------------------------------------------------
    penalties = []
    bonuses = []
    hard_rejects = []
    style_warnings = []  # v5: new key — style flags that are NOT fatal

    # BRAND GATE (restored 2026-07-01): clickbait tone → hard reject. This is the ONLY
    # surviving auto-reject (style rules are graded, non-fatal). Populates hard_rejects,
    # which drives grade='REJECTED' below and is the packaging_lock clickbait filter.
    clickbait_hits = detect_clickbait(title)
    if clickbait_hits:
        hard_rejects.append('Clickbait tone (off-brand for Calm Prosecutor voice): '
                            + ', '.join(f'"{h}"' for h in clickbait_hits))

    # YEAR: Context-aware penalty (v4 recalibration, v5 rebalanced)
    # Year as hook ("Invented in 1828") = mild penalty. Year as label ("The 1494 Line") = warning.
    # Data: "Flat Earth Myth Was Invented in 1828" got 3.7% CTR despite year.
    # v5: penalty rebalanced; label-years are HEDGE-tier warnings, not hard rejects.
    if has_year(title):
        if _year_is_hook(title):
            penalties.append(('Year in title (hook usage — reduced penalty)', YEAR_PENALTY_HOOK))
        else:
            style_warnings.append(
                f'YEAR as topic label — -45.6% CTR signal (n=6, HEDGE tier). '
                f'Consider moving year to description.'
            )
            penalties.append(('Year as topic label (style warning — HEDGE tier, n=6)', YEAR_PENALTY))

    # COLON: Context-aware penalty (v4 recalibration, v5 rebalanced)
    # Colon after versus ("X vs Y: Stakes") = 0 penalty. "Topic: Subtitle" = style warning.
    # Data: "Venezuela vs Guyana: Essequibo" got 4.31% CTR (D1 §4), channel #1 video has colon.
    # v5: COLON_PENALTY_VERSUS = 0; COLON_PENALTY reduced from -50 to -10.
    if ':' in title:
        if _colon_is_versus_stakes(title):
            if COLON_PENALTY_VERSUS != 0:
                penalties.append(('Colon after versus (stakes framing — reduced penalty)', COLON_PENALTY_VERSUS))
            # else: zero penalty, no entry
        else:
            style_warnings.append(
                'COLON detected — -28.1% CTR correlation (style preference only; '
                'top-3 channel videos all use colons). Review, not fatal.'
            )
            penalties.append(('Colon in title (style warning — n=4+, top-3 videos use colons)', COLON_PENALTY if pattern == 'colon' else COLON_PENALTY // 2))

    # "The X That Y" pattern — style warning (v5: was hard reject)
    # Data: "The CIA Document That Proved Operation Condor" got 4.91% fresh CTR 2026-06-10.
    if pattern == 'the_x_that':
        style_warnings.append(
            '"THE X THAT Y" pattern — historically 1.2% CTR, but contradicted by '
            'CIA Condor 4.91% fresh CTR (D1 dossier 2026-06-10). Review, not fatal.'
        )
        penalties.append(('The X That Y pattern (style warning, HEDGE tier)', THE_X_THAT_PENALTY))

    # Length check
    length = len(title)
    if length < LENGTH_SWEET_SPOT[0]:
        penalties.append((f'Too short ({length} chars, need 40+)', LENGTH_PENALTY_SHORT))
    elif length > LENGTH_SWEET_SPOT[1]:
        penalties.append((f'Too long ({length} chars, max 70)', LENGTH_PENALTY_LONG))

    # Specific number bonus
    if has_specific_number(title):
        bonuses.append(('Specific number (creates specificity)', SPECIFIC_NUMBER_BONUS))

    # Active verb bonus
    if has_active_verb(title):
        bonuses.append(('Active verb (creates tension)', ACTIVE_VERB_BONUS))

    # Scale word bonus (1.33x lift in outlier videos)
    title_words = set(title.lower().split())
    if title_words & _SCALE_WORDS:
        bonuses.append(('Scale word (1.33x outlier lift)', SCALE_WORD_BONUS))

    # Two-sentence bonus (11% outlier rate — strongest structural pattern)
    # Require 3+ lowercase chars before period to exclude abbreviations (Dr., St., vs.)
    if re.search(r'(?<=[a-z]{3})\.\s+[A-Z]', title):
        bonuses.append(('Two-sentence formula (11% outlier rate)', TWO_SENTENCE_BONUS))

    # Evidence promise bonus (v4) — channel's #1 CTR signal
    # "Here's the Evidence" = 9.5% CTR, "Primary Sources Destroy" = 5.4%
    if has_evidence_promise(title):
        bonuses.append(('Evidence promise (top CTR signal on this channel)', EVIDENCE_PROMISE_BONUS))

    # Named entity bonus (v4) — specificity drives impressions and clicks
    if has_named_entity(title):
        bonuses.append(('Named entity (country/leader/org specificity)', ENTITY_BONUS))

    # Controversy/myth-busting frame bonus (v4) — accusation framing = high CTR
    if has_controversy_frame(title):
        bonuses.append(('Controversy/myth-busting frame', CONTROVERSY_BONUS))

    # Search anchor bonus (v5 C3) — recognized head term in first 40 chars
    # 515-sub channel = every title needs a head-term keyword anchor (search-anchored).
    # HEAD_TERMS: sovereign states + geographic shorthands + ALLOWED_ACRONYMS + notable surnames.
    anchor_found, anchor_term = has_search_anchor(title)
    if anchor_found:
        bonuses.append((f"Search anchor: '{anchor_term}' in first 40 chars", SEARCH_ANCHOR_BONUS))

    # Topic viability modifier (v4) — penalize good-construction-but-zero-demand titles
    # Always runs (queries intel.db for competitor data). Silent on failure.
    try:
        from tools.packaging_intel import get_viability_modifier
        viability_mod = get_viability_modifier(title)
        if viability_mod > 0:
            bonuses.append((f'Topic viability: high demand ({viability_mod:+d})', viability_mod))
        elif viability_mod < 0:
            penalties.append((f'Topic viability: low demand ({viability_mod:+d})', viability_mod))
    except Exception:
        pass  # Silent fallback — never crash due to intel issues

    # ------------------------------------------------------------------
    # 6. Final score
    # ------------------------------------------------------------------
    total_penalties = sum(p[1] for p in penalties)
    total_bonuses = sum(b[1] for b in bonuses)
    final = max(0, min(100, base + total_penalties + total_bonuses))

    # ------------------------------------------------------------------
    # 7. Topic-aware grade
    #
    # Grade boundaries (all relative to topic thresholds):
    #   REJECTED: hard_rejects present — overrides everything
    #   A:        final >= thresholds['good'] + 15  (aspirational high)
    #   B:        final >= thresholds['good']
    #   C:        final >= thresholds['pass']
    #   D:        final >= thresholds['pass'] - 15
    #   F:        below D
    #
    # territorial:          A=80, B=65, C=50, D=35
    # ideological:          A=85, B=70, C=60, D=45
    # political_fact_check: A=100, B=85, C=75, D=60
    # general:              A=85, B=70, C=60, D=45
    # ------------------------------------------------------------------
    _pass = thresholds['pass']
    _good = thresholds['good']

    # v5 (C1): style rules (year/colon/the_x_that) have already been routed to
    # style_warnings above, NOT to hard_rejects.  hard_rejects is now ONLY for
    # clickbait tone (populated by _apply_tone_filter below, or caller-supplied).
    #
    # --strict mode: promote style_warnings back to hard_rejects (v4 behavior).
    # experimental flag: kept for backward compatibility — demotes any remaining
    # hard_rejects to visible warnings (penalty stays applied).
    warnings = []
    if strict and style_warnings:
        # --strict: treat style warnings as hard rejects (v4 regression mode)
        hard_rejects = hard_rejects + style_warnings
        style_warnings = []

    if experimental and hard_rejects:
        warnings = hard_rejects
        hard_rejects = []

    if hard_rejects:
        grade = 'REJECTED'
    elif final >= _good + 15:
        grade = 'A'
    elif final >= _good:
        grade = 'B'
    elif final >= _pass:
        grade = 'C'
    elif final >= _pass - 15:
        grade = 'D'
    else:
        grade = 'F'

    # Gap message: shown when title is below B grade
    if grade in ('C', 'D', 'F'):
        gap_message = (
            f"{normalized_topic} topics need score {_good}+ for B "
            f"(currently {final})"
        )
    else:
        gap_message = ""

    topic_type_target = {
        'pass': _pass,
        'good': _good,
        'gap_message': gap_message,
    }

    # ------------------------------------------------------------------
    # 8. Niche percentile label (BENCH-01)
    # ------------------------------------------------------------------
    niche_percentile_label = _niche_percentile_label(final, pattern, niche_data)

    # ------------------------------------------------------------------
    # 9. Suggestions
    # ------------------------------------------------------------------
    suggestions = []
    if has_year(title):
        suggestions.append('Year = HEDGE flag (confounded -46% from a single 2026-02-23 snapshot, not causal) — A/B-test it; move it to the description if the title reads cleaner without it')
    if ':' in title:
        suggestions.append('Colon = HEDGE flag (confounded -28%; the channel #1 and #3 videos both use colons) — keep it if it reads well, A/B-test')
    if pattern == 'the_x_that':
        suggestions.append('"The X That Y" = HEDGE flag (CIA Condor used it at 4.91% CTR) — fine to test, not a ban')
    if length > 70:
        suggestions.append(f'Shorten to under 70 chars (currently {length}) — gets truncated on mobile')
    if not has_specific_number(title) and not has_active_verb(title):
        suggestions.append('Add a specific number or active verb for more punch')
    if pattern == 'declarative' and not has_active_verb(title):
        suggestions.append('Consider "versus" framing if topic has two sides (4.0% CTR, best performer)')

    return {
        'title': title,
        'score': final,
        'grade': grade,
        'pattern': pattern,
        'length': length,
        'base_score': base,
        'penalties': penalties,
        'bonuses': bonuses,
        'suggestions': suggestions,
        'hard_rejects': hard_rejects,        # v5: ONLY clickbait tone; style rules → style_warnings
        'style_warnings': style_warnings,    # v5 new: year/colon/the_x_that flags (review, not fatal)
        'warnings': warnings,
        'experimental': experimental,
        'db_enriched': db_enriched,
        'db_base_score': db_base_score,
        # New in Phase 67
        'niche_enriched': niche_enriched,
        'niche_base_score': niche_base_score,
        'fallback_warning': fallback_warning,
        'detected_topic': normalized_topic,
        'topic_type_target': topic_type_target,
        'niche_percentile_label': niche_percentile_label,
        'staleness_days': staleness_days,        # age of newest live CTR snapshot, or None
        'snapshot_date': snapshot_date,          # YYYY-MM-DD of newest live CTR snapshot
        # ADR-0020/0024: the score travels with its measured predictive validity,
        # so it cannot be quoted downstream as evidence without it.
        'calibration': SCORE_CALIBRATION,
    }


def format_result(result: dict) -> str:
    """Format a single title score as readable output.

    Uses .get() with defaults throughout for backward compatibility — callers
    passing result dicts from older code paths (missing new Phase 67 keys) will
    still get clean output without KeyError.
    """
    lines = []

    if result.get('hard_rejects'):
        lines.append("  " + "!" * 50)
        lines.append("  *** BRAND-GATE REJECT (clickbait tone only — style hedges are NOT rejects) ***")
        lines.append("  " + "!" * 50)
        for reason in result['hard_rejects']:
            lines.append(f"  REASON: {reason}")
        lines.append("")

    # v5: style_warnings are review flags, not fatal (C1)
    if result.get('style_warnings'):
        lines.append("  " + "~" * 50)
        lines.append("  !! HEDGE-TIER STYLE FLAGS (review, not fatal):")
        for reason in result['style_warnings']:
            lines.append(f"  STYLE: {reason}")
        lines.append("  (penalty applied to score; grade from score only — not auto-rejected)")
        lines.append("")

    if result.get('warnings'):
        lines.append("  " + "~" * 50)
        lines.append("  EXPERIMENTAL OVERRIDE — rule(s) broken on purpose (testing):")
        for reason in result['warnings']:
            lines.append(f"  WARN: {reason}")
        lines.append("  (scored + ranked anyway; penalty still applied. Judge on search impressions, not CTR alone.)")
        lines.append("")

    # Score line — append niche percentile label when present (BENCH-01)
    niche_label = result.get('niche_percentile_label', '')
    score_line = f"  Score:   {result['score']}/100 ({result['grade']})"
    if niche_label:
        score_line = f"{score_line} — {niche_label}"

    # ADR-0020: the score states its own validity wherever it is shown, so a high
    # number cannot be read as evidence on its own.
    cal = result.get('calibration')
    if cal:
        score_line = (
            f"{score_line}\n"
            f"           [{cal['strength']} predictor: r={cal['r']:+.3f}, n={cal['n']}, "
            f"vs {cal['measured_against']}, measured {cal['measured_on']} — informs, does not decide]"
        )

    lines.extend([
        f"  Title:   {result['title']}",
        score_line,
        f"  Pattern: {result['pattern']} (base: {result.get('base_score', '?')})",
        f"  Length:  {result.get('length', len(result['title']))} chars",
    ])

    # Topic line — only when there is a gap to show (grade below B) (BENCH-03)
    topic_target = result.get('topic_type_target', {})
    gap_msg = topic_target.get('gap_message', '')
    if gap_msg:
        detected_topic = result.get('detected_topic', '?')
        lines.append(f"  Topic:   {detected_topic} — {gap_msg}")

    # Source line — DB takes priority label over niche (BENCH-02)
    if result.get('db_enriched'):
        source_line = "  Source:  DB-enriched (base score from live CTR data)"
    elif result.get('niche_enriched'):
        source_line = "  Source:  niche benchmark (competitor data)"
    else:
        source_line = "  Source:  static scores (run python -m tools.ctr_ingest first)"
    lines.append(source_line)

    # Fallback warning — separate Notice line after Source (BENCH-02)
    fallback_warning = result.get('fallback_warning')
    if fallback_warning:
        lines.append(f"  Notice:  {fallback_warning}")

    # Live-CTR staleness banner — only when DB-enriched scoring was attempted
    snapshot_date = result.get('snapshot_date')
    staleness_days = result.get('staleness_days')
    if snapshot_date and staleness_days is not None:
        line = f"  Live:    live CTR as of {snapshot_date} ({staleness_days} days old)"
        if staleness_days > STALENESS_WARN_DAYS:
            line += (f"  !! STALE (>{STALENESS_WARN_DAYS}d) — refresh via "
                     f"ctr_quick_add; scores may rest on old data")
        lines.append(line)

    if result.get('penalties'):
        for desc, val in result['penalties']:
            lines.append(f"  Penalty: {desc} ({val:+d})")

    if result.get('bonuses'):
        for desc, val in result['bonuses']:
            lines.append(f"  Bonus:   {desc} ({val:+d})")

    if result.get('suggestions'):
        lines.append("  Fix:")
        for s in result['suggestions']:
            lines.append(f"    - {s}")

    return '\n'.join(lines)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Title Scorer — History vs Hype',
        epilog=(
            'Examples:\n'
            '  python -m tools.title_scorer "France vs Haiti"\n'
            '  python -m tools.title_scorer "Title A" "Title B" --db\n'
            '  python -m tools.title_scorer "France Divided Haiti" --db --topic territorial\n'
            '  python -m tools.title_scorer --file titles.txt --db\n'
            '  python -m tools.title_scorer --ingest\n'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('titles', nargs='*', help='Title candidates to score')
    parser.add_argument('--file', help='File with one title per line')
    parser.add_argument(
        '--db',
        action='store_true',
        help='Use DB-enriched scoring (reads keywords.db for live CTR pattern scores)',
    )
    parser.add_argument(
        '--topic',
        default=None,
        help=(
            'Topic type for grade thresholds: territorial, ideological, '
            'political_fact_check, general (auto-detected when omitted)'
        ),
    )
    parser.add_argument(
        '--ingest',
        action='store_true',
        help='Ingest CTR data from CROSS-VIDEO-SYNTHESIS.md into keywords.db, then exit',
    )
    parser.add_argument(
        '--experimental',
        action='store_true',
        help='Demote hard-rejects to visible warnings so deliberate '
             'test candidates still score + rank (penalty stays applied)',
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='(v5) Restore v4 auto-REJECT behavior for year/colon/the-x-that patterns '
             '(for comparison runs; default is graded penalty + style warning)',
    )
    parser.add_argument(
        '--anchor',
        action='store_true',
        help='Explain the search-anchor verdict for each title (the BINDING packaging '
             'filter) instead of scoring it: matched term, position, and provenance',
    )
    parser.add_argument(
        '--record-anchor',
        metavar='TERM',
        help='Record a verified monthly search volume for TERM so it anchors from now '
             'on. The sanctioned repair for a false FAIL — see ADR-0023. Needs --volume',
    )
    parser.add_argument(
        '--volume',
        type=int,
        help=f'Verified monthly searches for --record-anchor (must be >= '
             f'{ANCHOR_VOLUME_FLOOR})',
    )
    parser.add_argument(
        '--anchor-source',
        default='',
        help='Where the --volume number came from, with a date ("vidiq-2026-08-03"). '
             'Copied into every packaging-lock block that anchors on this term',
    )
    args = parser.parse_args()

    # --record-anchor: teach the recognizer a measured term, then exit
    if args.record_anchor:
        if args.volume is None:
            print("ERROR: --record-anchor needs --volume <verified monthly searches>")
            sys.exit(2)
        if not args.anchor_source.strip():
            print("ERROR: --anchor-source is required — an unsourced number is not "
                  "evidence. Use e.g. --anchor-source vidiq-2026-08-03")
            sys.exit(2)
        outcome = record_anchor_volume(
            args.record_anchor, args.volume, args.anchor_source.strip())
        if 'error' in outcome:
            print(f"ERROR: {outcome['error']}")
            sys.exit(2)
        print(f"Recorded: \"{args.record_anchor}\" = {args.volume:,}/mo "
              f"({args.anchor_source.strip()}) — {outcome.get('action', 'stored')}")
        found, term = has_search_anchor(f"{args.record_anchor} Leads This Title")
        print(f"Anchor check: {'PASS' if found else 'FAIL'} ({term!r})")
        sys.exit(0)

    # --ingest: run ctr_ingest and exit
    if args.ingest:
        from tools.ctr_ingest import ingest_synthesis_ctr
        from tools.discovery.database import KeywordDB
        synthesis = Path('channel-data/patterns/CROSS-VIDEO-SYNTHESIS.md')
        if not synthesis.exists():
            print(f"ERROR: Synthesis file not found: {synthesis}")
            sys.exit(1)
        db = KeywordDB()
        result = ingest_synthesis_ctr(synthesis, db)
        db.close()
        print(f"\nCTR Ingest complete:")
        print(f"  Written:   {result['written']}")
        print(f"  Skipped:   {result['skipped']}  (no CTR data)")
        print(f"  Unmatched: {result['unmatched']}  (title not in video_performance)")
        if result['errors']:
            print(f"  Errors:    {len(result['errors'])}")
            for err in result['errors']:
                print(f"    - {err}")
        sys.exit(0)

    # Resolve db_path when --db is requested
    db_path = None
    if args.db:
        default_db = Path(__file__).parent / 'discovery' / 'keywords.db'
        if default_db.exists():
            db_path = str(default_db)
        else:
            print(f"WARNING: keywords.db not found at {default_db} — falling back to static scores")

    # Collect titles
    titles = []
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"ERROR: File not found: {args.file}")
            sys.exit(1)
        titles = [line.strip() for line in file_path.read_text().splitlines() if line.strip()]
    elif args.titles:
        titles = args.titles

    if not titles:
        parser.print_help()
        sys.exit(0)

    # --anchor: report the BINDING filter on its own, with provenance. Exit 2 if any
    # title fails, so a shell loop can gate on it the way packaging_lock does.
    if args.anchor:
        print("\n" + "=" * 64)
        print("  SEARCH ANCHOR — packaging FILTER 1 (binding: ADR-0012, ADR-0023)")
        print("=" * 64)
        any_failed = False
        for t in titles:
            match = find_search_anchor(t)
            any_failed = any_failed or not match.found
            print(f"\n  {t}")
            print(f"  {'PASS' if match.found else 'FAIL'}  {match.describe()}")
        print()
        sys.exit(2 if any_failed else 0)

    results = [score_title(t, db_path=db_path, topic_type=args.topic, experimental=args.experimental, strict=args.strict) for t in titles]
    results.sort(key=lambda x: -x['score'])

    db_label = " (DB-enriched)" if db_path else " (static scores)"
    topic_label = f", topic: {args.topic}" if args.topic else ""
    if args.experimental:
        topic_label += " [EXPERIMENTAL: hard-rejects → warnings]"
    if args.strict:
        topic_label += " [STRICT: style-warnings → hard-rejects (v4 behavior)]"
    print("\n" + "=" * 60)
    print(f"  TITLE SCORER — History vs Hype{db_label}{topic_label}")
    print("=" * 60)

    for i, r in enumerate(results, 1):
        print(f"\n  #{i}")
        print(format_result(r))
        print()

    if len(results) > 1:
        best = results[0]
        print("-" * 60)
        print(f"  WINNER: {best['title']}")
        print(f"  Score:  {best['score']}/100 ({best['grade']})")
        print()

    sys.exit(0)
