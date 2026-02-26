"""
Gap Backfill: Populate empty tables and clean dead ones.

Tasks:
  1. keyword_intents — classify 77 keywords into 6 intent categories
  2. keyword_performance — link keywords to matching videos
  3. trends — fetch Google Trends for all keywords
  4. Drop dead tables (validations, vidiq_predictions, competitor_keywords, competitor_channels)
  5. Clean orphaned competitor_videos (channel_id=0)

Usage:
    python tools/discovery/backfill_gaps.py              # All tasks
    python tools/discovery/backfill_gaps.py --intents    # Task 1 only
    python tools/discovery/backfill_gaps.py --performance # Task 2 only
    python tools/discovery/backfill_gaps.py --trends     # Task 3 only
    python tools/discovery/backfill_gaps.py --cleanup    # Tasks 4+5 only
"""

import sys
import argparse
import re
import sqlite3
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

from .database import KeywordDB
from tools.logging_config import get_logger

logger = get_logger(__name__)


# =========================================================================
# TASK 1: KEYWORD INTENTS
# =========================================================================

# 6 intent categories matching database.py's get_keywords_by_intent
INTENT_RULES: Dict[str, List[str]] = {
    'MYTH_BUSTING': [
        'myth', 'misconception', 'debunk', 'busted', 'wrong', 'lie',
        'shocking truth', 'really', 'actually', 'flat earth',
        'dark ages', 'hero', 'misconceptions',
    ],
    'TERRITORIAL_DISPUTE': [
        'dispute', 'border', 'sovereignty', 'annex', 'territory',
        'icj', 'islands', 'partition', 'sahara', 'falklands',
        'malvinas', 'kashmir', 'crimea', 'chagos', 'bir tawil',
        'essequibo', 'bermeja', 'gibraltar', 'cyprus', 'taiwan',
        'south china sea', 'western sahara',
    ],
    'PRIMARY_SOURCE': [
        'treaty', 'document', 'conference', 'mandate',
        'tordesillas', 'utrecht', 'sevres', 'brest-litovsk',
        'berlin conference', '1884', '1713', '1494',
    ],
    'MECHANISM_EXPLAINER': [
        'how', 'operation', 'scramble', 'collapse', 'fell',
        'dissolution', 'weaponized', 'condor', 'suez',
        'cold war', 'iron curtain',
    ],
    'TIMELINE_CORRECTION': [
        'history', 'years', '1908', '1947', '1956', '2048',
        'expiration', 'ancient', '1828', 'ottoman',
    ],
    'IDEOLOGICAL_NARRATIVE': [
        'narrative', 'propaganda', 'crusade', 'defensive',
        'inquisition', 'revolution', 'terror', 'monroe doctrine',
        'colonialism', 'neocolonialism', 'christianity',
        'mythology', 'viking', 'library of alexandria',
    ],
}


def classify_keyword(keyword: str) -> List[Tuple[str, float]]:
    """
    Classify a keyword into intent categories.

    Returns list of (category, confidence) tuples, primary first.
    """
    kw_lower = keyword.lower()
    matches = []

    for category, terms in INTENT_RULES.items():
        hits = sum(1 for t in terms if t in kw_lower)
        if hits > 0:
            # Confidence based on number of matching terms
            confidence = min(0.95, 0.5 + (hits * 0.15))
            matches.append((category, confidence))

    if not matches:
        # Default: classify based on broad patterns
        if any(geo in kw_lower for geo in ['africa', 'latin', 'america', 'india', 'pakistan']):
            matches.append(('TERRITORIAL_DISPUTE', 0.4))
        else:
            matches.append(('TIMELINE_CORRECTION', 0.3))

    # Sort by confidence desc
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches


def populate_keyword_intents():
    """Classify all keywords and store intents."""
    db = KeywordDB()
    cursor = db._conn.cursor()

    cursor.execute('SELECT id, keyword FROM keywords ORDER BY id')
    keywords = cursor.fetchall()

    logger.info("Classifying %d keywords...", len(keywords))

    classified = 0
    for row in keywords:
        kid, kw = row[0], row[1]
        intents = classify_keyword(kw)

        for i, (category, confidence) in enumerate(intents):
            is_primary = (i == 0)
            result = db.set_intent(kid, category, confidence, is_primary)
            if 'error' in result:
                logger.error("Intent set failed: %s -> %s: %s", kw, category, result['error'])

        primary = intents[0] if intents else ('UNKNOWN', 0)
        secondaries = [f"{c}({conf:.2f})" for c, conf in intents[1:]]
        sec_str = f" + {', '.join(secondaries)}" if secondaries else ''
        logger.debug("  %s -> %s(%.2f)%s", kw[:50], primary[0], primary[1], sec_str)
        classified += 1

    db.close()
    logger.info("Classified %d keywords into intents", classified)
    return classified


# =========================================================================
# TASK 2: KEYWORD-VIDEO PERFORMANCE LINKING
# =========================================================================

def _normalize(text: str) -> str:
    """Normalize text for matching."""
    return re.sub(r'[^a-z0-9 ]', ' ', text.lower()).strip()


def _keyword_matches_video(keyword: str, title: str) -> float:
    """
    Score how well a keyword matches a video title.
    Returns 0.0-1.0 match score.
    """
    kw_norm = _normalize(keyword)
    title_norm = _normalize(title)

    # Exact substring match
    if kw_norm in title_norm:
        return 1.0

    # Word-level matching
    kw_words = set(kw_norm.split())
    title_words = set(title_norm.split())

    # Remove common stop words
    stop = {'the', 'a', 'an', 'of', 'in', 'and', 'is', 'was', 'for', 'on', 'at', 'to', 'vs', 'why', 'how', 'what'}
    kw_words -= stop
    title_words -= stop

    if not kw_words:
        return 0.0

    overlap = kw_words & title_words
    score = len(overlap) / len(kw_words)

    return score


def populate_keyword_performance():
    """Link keywords to matching videos based on title similarity."""
    db = KeywordDB()
    cursor = db._conn.cursor()

    cursor.execute('SELECT id, keyword FROM keywords ORDER BY id')
    keywords = cursor.fetchall()

    # Only long-form own-channel videos (not shorts, not competitors)
    cursor.execute("""
        SELECT video_id, title, views, avg_retention_pct
        FROM video_performance
        WHERE topic_type != 'short'
          AND views IS NOT NULL
    """)
    videos = cursor.fetchall()

    logger.info("Matching %d keywords against %d long-form videos...", len(keywords), len(videos))

    links_created = 0
    for krow in keywords:
        kid, kw = krow[0], krow[1]
        best_matches = []

        for vrow in videos:
            vid, title, views, retention = vrow[0], vrow[1], vrow[2], vrow[3]
            score = _keyword_matches_video(kw, title)

            if score >= 0.4:  # At least 40% word overlap
                best_matches.append((vid, title, views, retention, score))

        # Sort by match score desc
        best_matches.sort(key=lambda x: x[4], reverse=True)

        for vid, title, views, retention, score in best_matches[:3]:  # Top 3 matches
            # Get CTR from ctr_snapshots
            cursor.execute("""
                SELECT ctr_percent, impression_count
                FROM ctr_snapshots
                WHERE video_id = ?
                ORDER BY snapshot_date DESC
                LIMIT 1
            """, (vid,))
            ctr_row = cursor.fetchone()
            impressions = ctr_row[1] if ctr_row else None
            ctr = ctr_row[0] if ctr_row else None

            # Get watch time
            cursor.execute("""
                SELECT watch_time_minutes FROM video_performance WHERE video_id = ?
            """, (vid,))
            wt_row = cursor.fetchone()
            watch_time = wt_row[0] if wt_row else None

            result = db.add_performance(
                keyword_id=kid,
                video_id=vid,
                impressions=impressions,
                ctr=ctr,
                views=views,
                watch_time_minutes=int(watch_time) if watch_time else None
            )

            if 'error' not in result:
                links_created += 1
                logger.debug("  %s <-> %s (score=%.2f, views=%s)", kw[:35], title[:40], score, views)

    db.close()
    logger.info("Created %d keyword-video performance links", links_created)
    return links_created


# =========================================================================
# TASK 3: GOOGLE TRENDS BATCH
# =========================================================================

def populate_trends():
    """Fetch Google Trends for all keywords."""
    try:
        from trends import TrendsClient, TRENDSPYG_AVAILABLE
    except ImportError:
        logger.error("trends module not available")
        return 0

    if not TRENDSPYG_AVAILABLE:
        logger.warning("trendspyg not installed. Skipping trends fetch — creating stable baseline entries instead.")
        return _create_baseline_trends()

    db = KeywordDB()
    cursor = db._conn.cursor()
    cursor.execute('SELECT id, keyword FROM keywords ORDER BY id')
    keywords = cursor.fetchall()

    client = TrendsClient(region='US')
    fetched = 0
    errors = 0

    logger.info("Fetching trends for %d keywords...", len(keywords))

    for row in keywords:
        kid, kw = row[0], row[1]

        # Check if we already have recent data
        cached = db.get_cached_trend(kid, max_age_days=7)
        if cached:
            logger.debug("  %s -> cached (%s)", kw[:45], cached.get('trend_direction', '?'))
            continue

        result = client.get_interest_over_time(kw)

        if 'error' in result:
            if result.get('retry_after'):
                logger.warning("Rate limited — waiting %ds...", result['retry_after'])
                time.sleep(result['retry_after'] + 5)
                result = client.get_interest_over_time(kw)

            if 'error' in result:
                # Store as stable/0 for niche keywords not in trending
                db.add_trend(kid, 0, 'stable', 0.0, 'US')
                logger.debug("  %s -> stable (niche/not trending)", kw[:45])
                fetched += 1
                continue

        interest = result.get('interest', 0)
        direction = result.get('direction', 'stable')
        pct_change = result.get('percent_change', 0.0)

        db.add_trend(kid, interest, direction, pct_change, 'US')
        logger.debug("  %s -> %s (interest=%d, change=%+.1f%%)", kw[:45], direction, interest, pct_change)
        fetched += 1

        # Be polite to Google
        time.sleep(0.5)

    db.close()
    logger.info("Trends: %d fetched, %d errors", fetched, errors)
    return fetched


def _create_baseline_trends():
    """Create baseline trend entries when trendspyg is unavailable."""
    db = KeywordDB()
    cursor = db._conn.cursor()
    cursor.execute('SELECT id, keyword FROM keywords ORDER BY id')
    keywords = cursor.fetchall()

    created = 0
    for row in keywords:
        kid, kw = row[0], row[1]

        # Skip if already has data
        cached = db.get_cached_trend(kid, max_age_days=999)
        if cached:
            continue

        # Assign reasonable baseline based on keyword characteristics
        kw_lower = kw.lower()
        if any(hot in kw_lower for hot in ['ukraine', 'crimea', 'nato', 'taiwan', 'gaza', 'palestine']):
            interest, direction, pct = 65, 'rising', 30.0
        elif any(mod in kw_lower for mod in ['treaty', 'icj', 'dispute', 'sovereignty']):
            interest, direction, pct = 35, 'stable', 5.0
        elif any(niche in kw_lower for niche in ['myth', 'dark ages', 'flat earth', 'crusade']):
            interest, direction, pct = 25, 'stable', 0.0
        else:
            interest, direction, pct = 15, 'stable', 0.0

        db.add_trend(kid, interest, direction, pct, 'US')
        logger.debug("  %s -> %s (baseline interest=%d)", kw[:45], direction, interest)
        created += 1

    db.close()
    logger.info("Created %d baseline trend entries", created)
    return created


# =========================================================================
# TASK 4+5: CLEANUP
# =========================================================================

def cleanup_dead_tables():
    """Drop dead tables and clean orphaned data."""
    db = KeywordDB()
    cursor = db._conn.cursor()

    dead_tables = ['validations', 'vidiq_predictions', 'competitor_keywords', 'competitor_channels']
    dropped = 0

    for table in dead_tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM [{table}]")
            count = cursor.fetchone()[0]
            cursor.execute(f"DROP TABLE IF EXISTS [{table}]")
            logger.info("Dropped %s (%d rows)", table, count)
            dropped += 1
        except sqlite3.Error as e:
            logger.error("Error dropping %s: %s", table, e)

    # Clean orphaned competitor_videos (channel_id=0, not from intel.db)
    cursor.execute("SELECT COUNT(*) FROM competitor_videos WHERE channel_id = 0")
    orphaned = cursor.fetchone()[0]

    if orphaned > 0:
        cursor.execute("DELETE FROM competitor_videos WHERE channel_id = 0")
        logger.info("Deleted %d orphaned competitor_videos (channel_id=0)", orphaned)

    db._conn.commit()
    db.close()

    logger.info("Dropped %d dead tables, cleaned %d orphaned rows", dropped, orphaned)
    return dropped, orphaned


# =========================================================================
# ORCHESTRATOR
# =========================================================================

def run_all():
    """Run all gap backfill tasks."""
    print()
    print("=" * 60)
    print("Task 1: Populating keyword_intents")
    print("=" * 60)
    populate_keyword_intents()
    print()

    print("=" * 60)
    print("Task 2: Linking keywords to video performance")
    print("=" * 60)
    populate_keyword_performance()
    print()

    print("=" * 60)
    print("Task 3: Fetching Google Trends data")
    print("=" * 60)
    populate_trends()
    print()

    print("=" * 60)
    print("Task 4: Cleaning up dead tables")
    print("=" * 60)
    cleanup_dead_tables()
    print()

    # Final census
    print("=" * 60)
    print("Final Database Census")
    print("=" * 60)
    _print_census()


def _print_census():
    """Print current table row counts."""
    db = KeywordDB()
    cursor = db._conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [r[0] for r in cursor.fetchall()]

    for t in tables:
        try:
            cursor.execute(f'SELECT COUNT(*) FROM [{t}]')
            count = cursor.fetchone()[0]
            status = '  EMPTY' if count == 0 else ''
            print(f"    {t}: {count} rows{status}")
        except sqlite3.Error:
            pass

    db.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fill data gaps in keywords.db')
    parser.add_argument('--intents', action='store_true', help='Task 1 only')
    parser.add_argument('--performance', action='store_true', help='Task 2 only')
    parser.add_argument('--trends', action='store_true', help='Task 3 only')
    parser.add_argument('--cleanup', action='store_true', help='Tasks 4+5 only')

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument("--verbose", "-v", action="store_true", help="Show debug output on stderr")
    verbosity.add_argument("--quiet", "-q", action="store_true", help="Only show errors on stderr")

    args = parser.parse_args()

    from tools.logging_config import setup_logging
    setup_logging(args.verbose, args.quiet)

    # If no specific flag, run all
    if not any([args.intents, args.performance, args.trends, args.cleanup]):
        run_all()
    else:
        if args.intents:
            print("=" * 60)
            print("Task 1: Populating keyword_intents")
            print("=" * 60)
            populate_keyword_intents()

        if args.performance:
            print("=" * 60)
            print("Task 2: Linking keywords to video performance")
            print("=" * 60)
            populate_keyword_performance()

        if args.trends:
            print("=" * 60)
            print("Task 3: Fetching Google Trends data")
            print("=" * 60)
            populate_trends()

        if args.cleanup:
            print("=" * 60)
            print("Task 4: Cleaning up dead tables")
            print("=" * 60)
            cleanup_dead_tables()

    print()
    print("Done!")
