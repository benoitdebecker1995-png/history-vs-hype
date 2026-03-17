"""
Title Scorer — Grades YouTube title candidates against channel CTR data.

Scores titles 0-100 based on measured CTR from POST-PUBLISH-ANALYSIS files.

⚠️  DATA CONFIDENCE WARNING (audit 2026-03-12):
    - versus (n=4): Only 2 independently verified (3.7% avg, not 4.0%)
    - declarative (n=19): Largest sample, most reliable pattern
    - how_why (n=5): Small but usable
    - question (n=1): SINGLE DATAPOINT — treat as unreliable
    - colon penalty (-28%): RELIABLE — measured across multiple videos
    - year penalty (-46%): RELIABLE — 5 with years vs 30 without
    - "26x map multiplier" was FALSE (actual: ~1.7x) — removed from scoring

    All CTR snapshots are from a single collection date (2026-02-23).
    Use for directional guidance, not precision targeting.

Phase 67 recalibration:
    - Added niche benchmark layer (Phase 66 competitor data from channel-data/niche_benchmark.json)
    - Added topic-type grade thresholds (territorial pass=50, political_fact_check pass=75)
    - Added small-sample fallback: when own-channel n < 5, substitute niche benchmark base score
    - Added niche percentile label for context display
    - Grade thresholds now topic-aware (via benchmark_store.TOPIC_GRADE_THRESHOLDS)
    - Backward compatible: no new required args, no existing keys renamed

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
YEAR_PENALTY = -50          # HARD REJECT: Year in title = -45.6% CTR (n=6 vs n=27)
COLON_PENALTY = -50         # HARD REJECT: Colon structure = -28.1% CTR (n=9 vs n=26)
THE_X_THAT_PENALTY = -50    # HARD REJECT: Worst-performing pattern (1.2% CTR historically)
LENGTH_SWEET_SPOT = (40, 70)  # Optimal character range for mobile
LENGTH_PENALTY_SHORT = -5   # Too short = vague
LENGTH_PENALTY_LONG = -10   # Too long = truncated on mobile
SPECIFIC_NUMBER_BONUS = 10  # Specific numbers in title improve CTR
ACTIVE_VERB_BONUS = 5       # Active verbs = +4.5% CTR (n=4 vs n=29, weak but positive)

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
    """Check for specific numbers (not years) that create specificity."""
    # Remove years first
    no_years = re.sub(r'\b(1[0-9]{3}|20[0-2][0-9])\b', '', title)
    return bool(re.search(r'\b\d+\b', no_years))


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


def score_title(title: str, db_path: str = None, topic_type: str = None) -> dict:
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
    # 5. Penalties, bonuses, hard rejects
    # ------------------------------------------------------------------
    penalties = []
    bonuses = []
    hard_rejects = []

    # HARD REJECT: Year in title
    if has_year(title):
        hard_rejects.append('YEAR detected — -45.6% CTR. Move year to description.')
        penalties.append(('HARD REJECT: Year in title', YEAR_PENALTY))

    # HARD REJECT: Colon in title
    # NOTE: Do NOT use niche colon data (0.776 VPS) to soften this penalty.
    # That figure is inflated by pipe-style titles (Knowing Better/Kraut).
    # Own-channel measurement = -28.1% CTR penalty (HIGH confidence, n=9).
    if ':' in title:
        hard_rejects.append('COLON detected — -28.1% CTR. Use period or em-dash.')
        penalties.append(('HARD REJECT: Colon in title', COLON_PENALTY if pattern == 'colon' else COLON_PENALTY // 2))

    # HARD REJECT: "The X That Y" pattern
    if pattern == 'the_x_that':
        hard_rejects.append('"THE X THAT Y" detected — worst pattern (1.2% CTR). Rewrite completely.')
        penalties.append(('HARD REJECT: The X That Y pattern', THE_X_THAT_PENALTY))

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
        suggestions.append('Remove the year — 43.7% CTR penalty')
    if ':' in title:
        suggestions.append('Replace colon with em-dash or period — colons cost 37% CTR')
    if pattern == 'the_x_that':
        suggestions.append('Rewrite — "The X That Y" is the worst-performing pattern (1.2% CTR)')
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
        'hard_rejects': hard_rejects,
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
        lines.append("  *** REJECTED — DO NOT PUBLISH ***")
        lines.append("  " + "!" * 50)
        for reason in result['hard_rejects']:
            lines.append(f"  REASON: {reason}")
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

    results = [score_title(t, db_path=db_path, topic_type=args.topic) for t in titles]
    results.sort(key=lambda x: -x['score'])

    db_label = " (DB-enriched)" if db_path else " (static scores)"
    topic_label = f", topic: {args.topic}" if args.topic else ""
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
