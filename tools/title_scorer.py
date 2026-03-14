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

Usage:
    python -m tools.title_scorer "Your Title Here"
    python -m tools.title_scorer "Title A" "Title B" "Title C"
    python -m tools.title_scorer --file titles.txt
    python -m tools.title_scorer "Title Here" --db           # DB-enriched scoring
    python -m tools.title_scorer --ingest                    # Ingest CTR from synthesis file
"""

import re
import sys
from pathlib import Path


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

# Penalty/bonus modifiers (all measured from real channel data)
YEAR_PENALTY = -50          # HARD REJECT: Year in title = -45.6% CTR (n=6 vs n=27)
COLON_PENALTY = -50         # HARD REJECT: Colon structure = -28.1% CTR (n=9 vs n=26)
THE_X_THAT_PENALTY = -50    # HARD REJECT: Worst-performing pattern (1.2% CTR historically)
LENGTH_SWEET_SPOT = (40, 70)  # Optimal character range for mobile
LENGTH_PENALTY_SHORT = -5   # Too short = vague
LENGTH_PENALTY_LONG = -10   # Too long = truncated on mobile
SPECIFIC_NUMBER_BONUS = 10  # Specific numbers in title improve CTR
ACTIVE_VERB_BONUS = 5       # Active verbs = +4.5% CTR (n=4 vs n=29, weak but positive)


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


def score_title(title: str, db_path: str = None) -> dict:
    """
    Score a title candidate 0-100.

    Args:
        title: YouTube title candidate string.
        db_path: Optional path to keywords.db. When provided, pattern base scores
                 are sourced from real CTR data (if sufficient samples exist).
                 Falls back silently to static PATTERN_SCORES when DB is unavailable
                 or the pattern has insufficient data. Pass None (default) for
                 fully static scoring — backward-compatible behavior.

    Returns:
        Dict with score, breakdown, and suggestions. Includes two additional keys
        vs the static-only version:
        - db_enriched (bool): True if a DB-derived base score was used.
        - db_base_score (int|None): The DB-derived score, or None if not used.
    """
    title = title.strip()
    pattern = detect_pattern(title)

    # Attempt to load DB overrides when db_path is provided
    db_overrides = {}
    if db_path is not None:
        try:
            from tools.title_ctr_store import get_pattern_ctr_from_db
            db_overrides = get_pattern_ctr_from_db(db_path)
        except Exception:
            pass  # Silent fallback — never crash due to DB issues

    db_base_score = db_overrides.get(pattern)  # None if not in DB
    db_enriched = db_base_score is not None
    base = db_base_score if db_enriched else PATTERN_SCORES.get(pattern, 50)

    penalties = []
    bonuses = []
    hard_rejects = []

    # HARD REJECT: Year in title
    if has_year(title):
        hard_rejects.append('YEAR detected — -45.6% CTR. Move year to description.')
        penalties.append(('HARD REJECT: Year in title', YEAR_PENALTY))

    # HARD REJECT: Colon in title
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

    # Calculate final score
    total_penalties = sum(p[1] for p in penalties)
    total_bonuses = sum(b[1] for b in bonuses)
    final = max(0, min(100, base + total_penalties + total_bonuses))

    # Grade — hard rejects override everything
    if hard_rejects:
        grade = 'REJECTED'
    elif final >= 80:
        grade = 'A'
    elif final >= 65:
        grade = 'B'
    elif final >= 50:
        grade = 'C'
    elif final >= 35:
        grade = 'D'
    else:
        grade = 'F'

    # Suggestions
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
    }


def format_result(result: dict) -> str:
    """Format a single title score as readable output."""
    lines = []

    if result['hard_rejects']:
        lines.append("  " + "!" * 50)
        lines.append("  *** REJECTED — DO NOT PUBLISH ***")
        lines.append("  " + "!" * 50)
        for reason in result['hard_rejects']:
            lines.append(f"  REASON: {reason}")
        lines.append("")

    # DB enrichment status line
    if result.get('db_enriched'):
        source_line = f"  Source:  DB-enriched (base score from live CTR data)"
    else:
        source_line = "  Source:  static scores (run python -m tools.ctr_ingest first)"

    lines.extend([
        f"  Title:   {result['title']}",
        f"  Score:   {result['score']}/100 ({result['grade']})",
        f"  Pattern: {result['pattern']} (base: {result['base_score']})",
        f"  Length:  {result['length']} chars",
        source_line,
    ])

    if result['penalties']:
        for desc, val in result['penalties']:
            lines.append(f"  Penalty: {desc} ({val:+d})")

    if result['bonuses']:
        for desc, val in result['bonuses']:
            lines.append(f"  Bonus:   {desc} ({val:+d})")

    if result['suggestions']:
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

    results = [score_title(t, db_path=db_path) for t in titles]
    results.sort(key=lambda x: -x['score'])

    db_label = " (DB-enriched)" if db_path else " (static scores)"
    print("\n" + "=" * 60)
    print(f"  TITLE SCORER — History vs Hype{db_label}")
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
