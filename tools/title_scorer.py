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

Usage:
    python -m tools.title_scorer "Your Title Here"
    python -m tools.title_scorer "Title A" "Title B" "Title C"
    python -m tools.title_scorer --file titles.txt
    python -m tools.title_scorer "Title Here" --db           # DB-enriched scoring
    python -m tools.title_scorer "Title Here" --db --topic territorial  # Topic-aware grading
    python -m tools.title_scorer --ingest                    # Ingest CTR from synthesis file
"""

import re
import sys
from pathlib import Path
from typing import Optional


# =============================================================================
# TONE SIGNALS — Moved here from metadata.py as authoritative source (Phase 70)
# metadata.py imports CLICKBAIT_PATTERNS and ALLOWED_ACRONYMS from this module.
# =============================================================================

# Clickbait patterns to filter/penalise (from VIDIQ-CHANNEL-DNA-FILTER.md)
CLICKBAIT_PATTERNS = [
    'SHOCKING', "You won't believe", "You won't BELIEVE",
    'This will BLOW your mind', "What THEY don't want you to know",
    'INSANE', 'MIND-BLOWING', 'EXPOSED', 'The TRUTH About',
    'DESTROYED by Facts', 'What IT Really Means', 'How THIS Changed',
    'Top 10', '5 Reasons Why', "3 Things You Didn't Know",
    'LIED About', 'The Truth They HID',
]

# Allowed acronyms (all-caps but NOT clickbait — used in _apply_tone_filter)
ALLOWED_ACRONYMS = [
    'ICJ', 'UN', 'CIA', 'AU', 'EU', 'NATO', 'UNESCO', 'WHO',
    'IMF', 'USSR', 'UK', 'US', 'USA', 'WTO', 'ICC', 'ECHR',
    'OPEC', 'BRICS', 'ASEAN', 'OAS', 'FCDO', 'BIOT', 'PDF',
    'DIY', 'GPS', 'GDP', 'CEO', 'FBI', 'NSA', 'NASA',
    'KGB',  # v5: added — "How the KGB Weaponized..." got highest fresh CTR (18.41% 2026-06-10)
]

# =============================================================================
# SEARCH ANCHOR HEAD TERMS (v5 — C3)
# Sovereign states, geographic shorthands, and notable figure surnames.
# A recognized head term within the first 40 chars earns SEARCH_ANCHOR_BONUS.
# Static list — a miss on obscure-but-valid term is fine; scorer is a floor.
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
}

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


def compute_tone_score(title: str) -> int:
    """
    Return a tone score for a title.

    +ACTIVE_VERB_BONUS (+5) for each active verb found.
    -10 per clickbait pattern found.

    Neutral title (no active verb, no clickbait) -> 0.
    """
    score = 0
    t = title.lower()
    if any(v in t for v in _TONE_SIGNALS['positive']):
        score += ACTIVE_VERB_BONUS
    for pattern in _TONE_SIGNALS['negative']:
        if pattern.lower() in t:
            score -= 10
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


def detect_pattern(title: str) -> str:
    """Detect which title pattern this matches."""
    t = title.lower()

    # versus pattern: "X vs Y", "X versus Y"
    if re.search(r'\bvs\.?\b|\bversus\b', t):
        return 'versus'

    # the_x_that pattern: "The [1-3 words] That [Verb]"
    if re.search(r'^the\s+(?:\w+\s+){0,2}\w+\s+that\s+', t):
        return 'the_x_that'

    # colon pattern
    if ':' in title:
        return 'colon'

    # question pattern
    if title.strip().endswith('?'):
        return 'question'

    # how/why pattern
    if re.search(r'^(how|why)\b', t):
        return 'how_why'

    return 'declarative'


def has_year(title: str) -> bool:
    """Check if title contains a 4-digit year."""
    return bool(re.search(r'\b(1[0-9]{3}|20[0-2][0-9])\b', title))


def has_specific_number(title: str) -> bool:
    """Check for specific numbers (not years) that create real specificity.

    v4: Exclude duration-as-adjective patterns like "200-Year-Old" or "500-Year"
    which don't create the same specificity as "5 Myths" or "122 Years of French Extraction".
    Duration adjectives are vague scale markers, not concrete data points.
    """
    # Remove years first
    no_years = re.sub(r'\b(1[0-9]{3}|20[0-2][0-9])\b', '', title)
    # Remove duration-as-adjective patterns (e.g., "200-Year-Old", "500-Year Lie")
    no_duration_adj = re.sub(r'\b\d+-[Yy]ear-?\w*', '', no_years)
    return bool(re.search(r'\b\d+\b', no_duration_adj))


def has_active_verb(title: str) -> bool:
    """Check for strong active verbs."""
    active_verbs = [
        'destroyed', 'erased', 'redrew', 'deleted', 'stole', 'conquered',
        'invaded', 'betrayed', 'exposed', 'revealed', 'weaponized', 'carved',
        'divided', 'partitioned', 'annexed', 'ruled', 'fought', 'claimed',
        'debunked', 'proved', 'disproved', 'lied', 'fabricated',
    ]
    t = title.lower()
    return any(v in t for v in active_verbs)


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


def has_evidence_promise(title: str) -> bool:
    """
    Detect evidence/proof promise language — strongest CTR signal on this channel.

    Top CTR titles: "Here's the Evidence" (9.5%), "Here's Who Did It" (3.7%),
    "The Documents Prove It", "Primary Sources Destroy".

    The channel's competitive advantage is evidence. Titles that promise it click better.
    """
    t = title.lower()
    evidence_phrases = [
        "here's", "the evidence", "the proof", "the documents",
        "documents prove", "documents show", "primary source",
        "the receipt", "every receipt", "we found", "we read",
        "the original", "the actual", "word for word",
    ]
    return any(p in t for p in evidence_phrases)


def has_named_entity(title: str) -> bool:
    """
    Detect named countries, leaders, or orgs that create specificity.

    Titles with named entities get more impressions (YouTube knows who to show them to).
    Top performers all name specific countries or political figures.
    """
    # Check for country/entity patterns (capitalized proper nouns typical of geo/political titles)
    # Rather than maintain a huge list, detect patterns: "X vs Y" with caps, possessives, etc.
    entity_signals = [
        # Two+ capitalized words that aren't common English
        r"\b(?:France|Spain|Portugal|Turkey|Greece|Iran|Venezuela|Guyana|"
        r"Israel|Palestine|Russia|China|Morocco|Cyprus|Kashmir|Peru|"
        r"Georgia|Haiti|Armenia|Kosovo|NATO|USSR|CIA|KGB|UN|EU|"
        r"Trump|Vance|Stalin|Petain|Lagertha|Sykes|Picot)\b",
    ]
    return any(re.search(p, title) for p in entity_signals)


def has_controversy_frame(title: str) -> bool:
    """
    Detect accusation/myth-busting framing that signals conflict/tension.

    Top CTR: "Claims Christians Found Child Sacrifice" (9.5%), "Started With a Lie" (5.1%),
    "Destroy the Narrative" (5.4%), "Weaponized Palestine" (5.5%).
    """
    t = title.lower()
    controversy_words = [
        'myth', 'lie', 'fake', 'hoax', 'claims', 'claim',
        'debunk', 'destroy', 'narrative', 'propaganda',
        'secret', 'hidden', 'nobody', 'sacrifice',
        'walked back', 'phantom', 'illegal',
    ]
    return any(w in t for w in controversy_words)


def has_search_anchor(title: str) -> tuple[bool, str]:
    """
    Detect if a recognized head term appears within the first 40 characters (v5 C3).

    Returns (found: bool, matched_term: str).  matched_term is '' when not found.

    Recognition list: HEAD_TERMS (sovereign states + geographic shorthands) +
    ALLOWED_ACRONYMS + notable-figure surnames already in the corpus.
    Case-insensitive whole-word match.

    A miss on an obscure-but-valid term is acceptable — scorer is a floor, not an oracle.
    Keep it cheap and static: no API calls.
    """
    prefix = title[:40]
    # Build lookup set: HEAD_TERMS + ALLOWED_ACRONYMS (case-insensitive keys)
    candidates = list(HEAD_TERMS) + list(ALLOWED_ACRONYMS)
    for term in candidates:
        pattern = re.compile(r'\b' + re.escape(term) + r'\b', re.IGNORECASE)
        if pattern.search(prefix):
            # Return the matched surface form from the title
            m = pattern.search(prefix)
            return (True, m.group(0))
    return (False, '')


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
        import sqlite3
        conn = sqlite3.connect(db_path)
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
    args = parser.parse_args()

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
