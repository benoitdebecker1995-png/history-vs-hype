"""
Analytics Backfill Module

Populates the analytics database from all existing channel data and generates
a channel insights report.

This module is the primary backfill orchestrator for Phase 44. It imports data
from three sources (JSON pre-fetches, POST-PUBLISH-ANALYSIS markdown files),
fixes topic mis-classification, and writes channel-data/channel-insights.md.

Pipeline:
  Stage 1 — JSON import (primary, most complete data: views, retention, CTR)
  Stage 2 — Markdown import (adds lessons_learned, drop points, discovery notes)
  Stage 3 — Topic reclassification (fixes 'general' dominance with expanded vocabulary)
  Stage 4 — Channel insights report generation (channel-data/channel-insights.md)

Usage:
    python -m tools.youtube_analytics.backfill               # Full pipeline
    python -m tools.youtube_analytics.backfill --force       # Re-import all data
    python -m tools.youtube_analytics.backfill --json-only   # Skip markdown stage
    python -m tools.youtube_analytics.backfill --insights-only  # Skip all imports

Anti-patterns (from RESEARCH.md):
    - Do NOT use analytics.db (empty). Use keywords.db via KeywordDB exclusively.
    - Do NOT re-fetch from YouTube API. Use JSON pre-fetches as primary source.
    - Do NOT include competitor videos in insights (filter by own-channel IDs).
    - Do NOT make insights prescriptive — always advisory language.

Dependencies:
    - stdlib only: json, pathlib, datetime, sys, argparse, statistics
    - tools/discovery/database.py (KeywordDB)
    - tools/youtube_analytics/feedback_parser.py (backfill_all)
    - tools/youtube_analytics/performance.py (classify_topic_type, classify_own_video)
    - tools/youtube_analytics/topic_strategy.py (generate_topic_strategy)
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone
from statistics import mean
from typing import Dict, List, Any, Optional, Set

# Add discovery module to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'discovery'))

try:
    from database import KeywordDB
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False

# Add youtube_analytics to path for sibling imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from performance import classify_topic_type, classify_own_video
    PERFORMANCE_AVAILABLE = True
except ImportError:
    PERFORMANCE_AVAILABLE = False


# =========================================================================
# HELPER FUNCTIONS
# =========================================================================

def _safe_conversion(views: int, subscribers_gained: int) -> float:
    """Calculate subscriber conversion rate safely."""
    if not views or views <= 0:
        return 0.0
    return (subscribers_gained / views) * 100


def _load_own_channel_ids(project_root: Path) -> Set[str]:
    """
    Load the authoritative set of own-channel video IDs from JSON pre-fetches.

    Uses _longform_enriched.json first, then merges with _longform_metrics.json.
    These files are the ground truth for distinguishing own-channel vs competitors.

    Returns:
        Set of video ID strings
    """
    analytics_dir = project_root / 'tools' / 'youtube_analytics'
    own_ids = set()

    for json_name in ['_longform_enriched.json', '_longform_metrics.json']:
        json_path = analytics_dir / json_name
        if json_path.exists():
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    videos = json.load(f)
                for v in videos:
                    vid = v.get('video_id', '').strip()
                    if vid:
                        own_ids.add(vid)
            except (json.JSONDecodeError, OSError):
                pass

    return own_ids


def _ensure_avg_retention_column(db: 'KeywordDB') -> None:
    """
    Ensure avg_retention_pct column exists in video_performance table.

    This is a safe migration — adds the column if missing, no-ops otherwise.
    The column is needed by topic_strategy.py queries but may be absent in
    existing databases before Phase 44.
    """
    try:
        cursor = db._conn.cursor()
        cursor.execute("PRAGMA table_info(video_performance)")
        existing_cols = {row[1] for row in cursor.fetchall()}
        if 'avg_retention_pct' not in existing_cols:
            cursor.execute(
                "ALTER TABLE video_performance ADD COLUMN avg_retention_pct REAL"
            )
            db._conn.commit()
    except Exception:
        pass  # Non-fatal: topic_strategy will return 0 for missing retention


def _update_avg_retention(db: 'KeywordDB', video_id: str, avg_retention_pct: float) -> None:
    """
    Update avg_retention_pct for a video record.

    Called separately because add_video_performance() does not include this field
    (it was added in Phase 44 migration, not in the original schema).

    Only updates if avg_retention_pct is not already set (avoids overwriting
    good API data with lower-quality values).
    """
    try:
        cursor = db._conn.cursor()
        cursor.execute(
            """
            UPDATE video_performance
            SET avg_retention_pct = ?
            WHERE video_id = ?
              AND (avg_retention_pct IS NULL OR avg_retention_pct = 0)
            """,
            (avg_retention_pct, video_id)
        )
        db._conn.commit()
    except Exception:
        pass  # Non-fatal


# =========================================================================
# STAGE 1: JSON IMPORT
# =========================================================================

def import_from_json_prefetch(project_root: Path) -> Dict[str, Any]:
    """
    Import own-channel video metrics from JSON pre-fetched files.

    Prefers _longform_enriched.json (has CTR + avg_retention) over
    _longform_metrics.json (basic metrics only). Falls back gracefully.

    Per-video progress output format: "Importing {title_short} ({i}/{total})... done"

    Returns:
        {'imported': N, 'skipped': N, 'errors': [...]}
    """
    if not DB_AVAILABLE:
        return {'error': 'KeywordDB not available', 'imported': 0, 'skipped': 0, 'errors': []}

    analytics_dir = project_root / 'tools' / 'youtube_analytics'
    enriched_path = analytics_dir / '_longform_enriched.json'
    metrics_path = analytics_dir / '_longform_metrics.json'

    # Prefer enriched (has avg_retention from API)
    json_path = enriched_path if enriched_path.exists() else metrics_path
    if not json_path.exists():
        return {'error': 'No JSON pre-fetch found', 'imported': 0, 'skipped': 0, 'errors': []}

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            videos = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        return {'error': f'Failed to load {json_path.name}: {e}', 'imported': 0, 'skipped': 0, 'errors': []}

    total = len(videos)
    imported = 0
    skipped = 0
    errors = []

    print(f"  Found {total} videos in {json_path.name}")
    print()

    db = KeywordDB()
    _ensure_avg_retention_column(db)

    for i, video in enumerate(videos, 1):
        video_id = (video.get('video_id') or '').strip()
        title = video.get('title') or 'Unknown'
        title_short = title[:40]

        print(f"  Importing {title_short} ({i}/{total})...", end=' ', flush=True)

        if not video_id:
            errors.append({'index': i, 'error': 'Missing video_id'})
            print("ERROR (no video_id)")
            continue

        # Classify by title
        if PERFORMANCE_AVAILABLE:
            classification = classify_own_video(title)
            topic_type = classification['topic_type']
            angles = classification['angles']
        else:
            topic_type = classify_topic_type_simple(title)
            angles = []

        # Build metrics — use what's available
        views = video.get('views') or 0
        subs_gained = video.get('subscribers_gained') or 0
        subs_lost = video.get('subscribers_lost') or 0
        conversion_rate = _safe_conversion(views, subs_gained)

        result = db.add_video_performance(
            video_id=video_id,
            title=title,
            views=views,
            subscribers_gained=subs_gained,
            subscribers_lost=subs_lost,
            conversion_rate=conversion_rate,
            watch_time_minutes=video.get('watch_time_minutes'),
            avg_view_duration_seconds=video.get('avg_view_duration_seconds'),
            likes=video.get('likes'),
            comments=video.get('comments'),
            shares=video.get('shares'),
            topic_type=topic_type,
            angles=angles,
            published_at=video.get('published')
        )

        if 'error' in result:
            errors.append({'video_id': video_id, 'error': result['error']})
            print(f"ERROR: {result['error']}")
        else:
            # Store avg_retention_pct separately (not in add_video_performance signature)
            avg_retention_raw = video.get('avg_retention')
            if avg_retention_raw is not None:
                # JSON stores as decimal (0.363); convert to percent (36.3) for DB
                avg_retention_pct = float(avg_retention_raw) * 100
                _update_avg_retention(db, video_id, avg_retention_pct)

            imported += 1
            print("done")

    db.close()

    print()
    print(f"  JSON import: {imported} imported, {skipped} skipped, {len(errors)} errors")

    return {'imported': imported, 'skipped': skipped, 'errors': errors}


# =========================================================================
# STAGE 2: MARKDOWN PARSING
# =========================================================================

def import_from_analysis_files(project_root: Path, force: bool = False) -> Dict[str, Any]:
    """
    Parse all POST-PUBLISH-ANALYSIS markdown files and store in database.

    Delegates to feedback_parser.backfill_all() which handles all file scanning
    and storage via db.store_video_feedback().

    Critical (Pitfall 4): Analysis files with "Performance data unavailable"
    are low-quality. After backfill_all(), null values from sparse analysis files
    do NOT overwrite good API data already loaded in Stage 1. The feedback_parser
    uses store_video_feedback() which only updates feedback columns
    (lessons_learned, retention_drop_point, discovery_issues) — not metrics.

    Returns:
        Dict from backfill_all() with 'processed', 'skipped', 'errors' keys
    """
    try:
        from feedback_parser import backfill_all
    except ImportError:
        return {'error': 'feedback_parser not available', 'processed': 0, 'skipped': 0, 'errors': 0}

    return backfill_all(project_root, force=force)


# =========================================================================
# STAGE 3: TOPIC RECLASSIFICATION
# =========================================================================

# Expanded vocabulary beyond performance.py TAG_VOCABULARY
EXPANDED_TOPIC_RULES = {
    'legal': ['constitution', 'constitutional', 'democratic', 'statute', 'legislation',
              'referendum', 'loophole', 'provision', 'clause', 'article', 'mandate',
              'court', 'ruling', 'legal'],
    'ideological': ['myth', 'dark ages', 'flat earth', 'propaganda', 'narrative',
                    'debunk', 'fact-check', 'lie', 'misconception', 'rewriting',
                    'hero', 'erased', 'weaponized', 'kgb', 'nato promised',
                    'christmas', 'sol invictus', 'stalin', 'putin'],
    'factcheck': ['fact-check', 'fact check', 'claims', 'checking', 'verified'],
    'colonial': ['colonial', 'colony', 'empire', 'imperial', 'independence',
                 'decolonization', 'partition', 'somaliland', 'haiti', 'occupied',
                 'protectorate', 'french control', 'coups ended', 'stock exchange funded',
                 'leave or starve', 'emptied an island'],
    'territorial': ['dispute', 'border', 'territory', 'claim', 'annex', 'occupation',
                    'sovereignty', 'bir tawil', 'chagos', 'essequibo', 'bermeja',
                    'gibraltar', 'treaty', 'icj', 'disappear', 'disappeared',
                    'islands', 'island', 'wall', 'divided capital', 'cyprus',
                    'kashmir', 'ukraine', 'taiwan', 'china sea', 'south china',
                    'georgia', 'armenia', 'turkey', 'greece', 'morocco',
                    'map', 'cited this map', 'map error'],
}


def _classify_with_expanded_rules(title: str) -> Optional[str]:
    """
    Apply expanded classification rules to a video title.

    Returns topic type string, or None if no match found.
    Intended to be used as a fallback after the base classify_topic_type() returns 'general'.
    """
    if not title:
        return None

    title_lower = title.lower()

    for topic, keywords in EXPANDED_TOPIC_RULES.items():
        if any(kw in title_lower for kw in keywords):
            return topic

    return None


def reclassify_topics(project_root: Path) -> int:
    """
    Re-classify video_performance rows where topic_type is 'general' or NULL.

    Uses the base classify_topic_type() from performance.py first, then applies
    EXPANDED_TOPIC_RULES for titles that still return 'general'. This corrects
    the 'general' dominance problem identified in RESEARCH.md Pitfall 1.

    Only updates own-channel videos (IDs from JSON pre-fetches) to avoid
    corrupting competitor video classifications.

    Returns:
        Count of rows reclassified (0 if nothing needed reclassification)
    """
    if not DB_AVAILABLE:
        return 0

    own_channel_ids = _load_own_channel_ids(project_root)
    if not own_channel_ids:
        return 0

    db = KeywordDB()
    reclassified = 0

    try:
        cursor = db._conn.cursor()

        # Only look at own-channel videos that are mis-classified as general or NULL
        placeholders = ','.join('?' * len(own_channel_ids))
        cursor.execute(
            f"""
            SELECT video_id, title
            FROM video_performance
            WHERE (topic_type = 'general' OR topic_type IS NULL)
              AND video_id IN ({placeholders})
            """,
            list(own_channel_ids)
        )
        rows = cursor.fetchall()

        if not rows:
            db.close()
            return 0

        for row in rows:
            video_id = row['video_id']
            title = row['title'] or ''

            # Try base classification first
            if PERFORMANCE_AVAILABLE:
                new_type = classify_topic_type(title)
            else:
                new_type = 'general'

            # If still general, try expanded rules
            if new_type == 'general':
                expanded = _classify_with_expanded_rules(title)
                if expanded:
                    new_type = expanded

            # Only update if we found a non-general type
            if new_type and new_type != 'general':
                cursor.execute(
                    """
                    UPDATE video_performance
                    SET topic_type = ?, classified_at = ?
                    WHERE video_id = ?
                    """,
                    (new_type, datetime.now(timezone.utc).date().isoformat(), video_id)
                )
                reclassified += 1

        db._conn.commit()

    except Exception:
        pass

    db.close()
    return reclassified


# =========================================================================
# STAGE 4: CHANNEL INSIGHTS REPORT
# =========================================================================

def _signal_label(video_count: int) -> str:
    """Return confidence signal label based on video count."""
    if video_count >= 6:
        return 'strong signal'
    elif video_count >= 3:
        return 'moderate signal'
    else:
        return 'early signal'


def _composite_score(
    views: float,
    avg_retention: float,
    conversion_rate: float,
    max_views: float,
    max_conversion: float
) -> float:
    """
    Compute composite performance score.

    Weights: views 0.4, retention 0.35, conversion 0.25 (per user decision).
    Each metric normalized 0-1 against channel maximum.

    Args:
        views: Raw view count
        avg_retention: Retention as percentage (e.g. 36.3)
        conversion_rate: Conversion rate as percentage
        max_views: Channel maximum views (for normalization)
        max_conversion: Channel maximum conversion rate (for normalization)

    Returns:
        Composite score 0-1
    """
    weights = {'views': 0.4, 'retention': 0.35, 'conversion': 0.25}

    views_n = (views / max_views) if max_views > 0 else 0
    retention_n = (avg_retention / 100) if avg_retention else 0  # already 0-100
    conversion_n = (conversion_rate / max_conversion) if max_conversion > 0 else 0

    # Clamp to 0-1
    views_n = max(0.0, min(1.0, views_n))
    retention_n = max(0.0, min(1.0, retention_n))
    conversion_n = max(0.0, min(1.0, conversion_n))

    return (
        views_n * weights['views'] +
        retention_n * weights['retention'] +
        conversion_n * weights['conversion']
    )


def generate_channel_insights_report(project_root: Path) -> Dict[str, Any]:
    """
    Generate channel-data/channel-insights.md from own-channel performance data.

    CRITICAL: Filters to own-channel videos only (IDs from JSON pre-fetches).
    Competitor videos in the database are excluded. This prevents insights
    from being corrupted by competitor data (Pitfall 2 in RESEARCH.md).

    Report structure:
      - Header with timestamp and video count
      - "Auto-generated. Do not edit manually." notice
      - Performance by Topic Type table (topic, videos, avg views, avg retention,
        avg conversion, signal level)
      - Top Performers (3-5 by composite score with reasoning)
      - Channel Signals (advisory insights with confidence flagging)
      - Topic Recommendations (composite-scored, advisory language)
      - Footer

    Returns:
        {'saved_to': path, 'video_count': N} on success
        {'error': msg} on failure
    """
    if not DB_AVAILABLE:
        return {'error': 'KeywordDB not available'}

    own_channel_ids = _load_own_channel_ids(project_root)
    if not own_channel_ids:
        return {'error': 'No own-channel video IDs found in JSON pre-fetches'}

    db = KeywordDB()

    try:
        cursor = db._conn.cursor()

        # Query only own-channel videos
        placeholders = ','.join('?' * len(own_channel_ids))
        cursor.execute(
            f"""
            SELECT video_id, title, topic_type, views, subscribers_gained,
                   conversion_rate, avg_retention_pct, avg_view_duration_seconds
            FROM video_performance
            WHERE video_id IN ({placeholders})
              AND title IS NOT NULL
            ORDER BY views DESC NULLS LAST
            """,
            list(own_channel_ids)
        )
        rows = [dict(r) for r in cursor.fetchall()]
        db.close()

    except Exception as e:
        db.close()
        return {'error': f'Database query failed: {e}'}

    if not rows:
        return {'error': 'No own-channel videos found in database. Run backfill first.'}

    # Compute channel-wide maximums for normalization
    all_views = [r['views'] or 0 for r in rows]
    all_conversions = [r['conversion_rate'] or 0 for r in rows]
    max_views = max(all_views) if all_views else 1
    max_conversion = max(all_conversions) if all_conversions else 1

    # Score each video
    for row in rows:
        row['composite_score'] = _composite_score(
            views=row['views'] or 0,
            avg_retention=row['avg_retention_pct'] or 0,
            conversion_rate=row['conversion_rate'] or 0,
            max_views=max_views,
            max_conversion=max_conversion
        )

    # Group by topic type
    by_topic: Dict[str, List[Dict]] = {}
    for row in rows:
        topic = row.get('topic_type') or 'general'
        if topic not in by_topic:
            by_topic[topic] = []
        by_topic[topic].append(row)

    # Build topic stats rows
    topic_stats = []
    for topic, vids in by_topic.items():
        count = len(vids)
        avg_views = mean(v['views'] or 0 for v in vids)
        avg_ret = mean(v['avg_retention_pct'] or 0 for v in vids)
        avg_conv = mean(v['conversion_rate'] or 0 for v in vids)
        signal = _signal_label(count)
        topic_stats.append({
            'topic': topic,
            'count': count,
            'avg_views': avg_views,
            'avg_retention': avg_ret,
            'avg_conversion': avg_conv,
            'signal': signal,
            'videos': vids
        })

    # Sort by avg_views desc
    topic_stats.sort(key=lambda t: t['avg_views'], reverse=True)

    # Top performers by composite score
    top_performers = sorted(rows, key=lambda r: r['composite_score'], reverse=True)[:5]

    # Best-known benchmark (for reasoning strings)
    best_known = max(rows, key=lambda r: r['views'] or 0) if rows else None
    best_known_views = best_known['views'] if best_known else 0
    best_known_title_short = (best_known['title'] or '')[:35] if best_known else ''

    # Advisory insights
    channel_avg_conv = mean(all_conversions) if all_conversions else 0
    channel_avg_ret = mean(r['avg_retention_pct'] or 0 for r in rows)
    total_videos = len(rows)

    now_str = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')

    # Build recommendations
    recommendations = _build_recommendations(topic_stats, channel_avg_conv, channel_avg_ret)

    # Assemble report lines
    lines = [
        '# Channel Performance Insights',
        '',
        f'> Generated: {now_str} UTC',
        f'> Videos analyzed: {total_videos} own-channel videos',
        '> Auto-generated. Do not edit manually. Re-run: `python -m tools.youtube_analytics.backfill --insights-only`',
        '',
        '---',
        '',
        '## Performance by Topic Type',
        '',
        '| Topic | Videos | Avg Views | Avg Retention | Avg Conv% | Signal |',
        '|-------|--------|-----------|---------------|-----------|--------|',
    ]

    for t in topic_stats:
        retention_str = f"{t['avg_retention']:.1f}%" if t['avg_retention'] else 'N/A'
        lines.append(
            f"| {t['topic']} | {t['count']} | {t['avg_views']:,.0f} | "
            f"{retention_str} | {t['avg_conversion']:.2f}% | {t['signal']} ({t['count']} videos) |"
        )

    lines.extend([
        '',
        '---',
        '',
        '## Top Performers',
        '',
        f'Ranked by composite score (views 40%, retention 35%, conversion 25%).',
        '',
    ])

    for rank, vid in enumerate(top_performers, 1):
        title = vid['title'] or 'Unknown'
        views = vid['views'] or 0
        conv = vid['conversion_rate'] or 0
        ret = vid['avg_retention_pct']
        ret_str = f"{ret:.1f}% retention, " if ret else ''
        score = vid['composite_score']

        # Build reasoning with benchmark reference
        reasoning_parts = []
        if views >= 10000:
            reasoning_parts.append(f"{views:,} views")
        elif best_known and best_known['video_id'] != vid['video_id']:
            reasoning_parts.append(f"{views:,} views (channel leader: {best_known_views:,})")
        else:
            reasoning_parts.append(f"{views:,} views")

        if ret:
            reasoning_parts.append(f"{ret:.1f}% retention")
        if conv > 0:
            reasoning_parts.append(f"{conv:.2f}% conversion")

        lines.append(
            f"**{rank}. {title}** — {', '.join(reasoning_parts)} "
            f"(composite: {score:.2f})"
        )

    lines.extend([
        '',
        '---',
        '',
        '## Channel Signals',
        '',
        f'Based on {total_videos} own-channel long-form videos. All signals are early-to-moderate.',
        '',
    ])

    # Per-topic signals
    for t in topic_stats[:4]:  # Top 4 topics only
        signal = t['signal']
        avg_ret = t['avg_retention']
        ret_note = f", avg {avg_ret:.1f}% retention" if avg_ret else ''
        lines.append(
            f"- **{t['topic'].title()}** ({t['count']} videos): "
            f"avg {t['avg_views']:,.0f} views, {t['avg_conversion']:.2f}% conversion{ret_note} "
            f"— {signal}"
        )

    lines.extend([
        '',
        '---',
        '',
        '## Topic Recommendations',
        '',
        'Insights are advisory. Proven patterns are noted, but experimentation is encouraged.',
        '',
    ])

    for rec in recommendations:
        lines.append(f"- {rec}")

    lines.extend([
        '',
        '---',
        '',
        '> **Note:** These are patterns from ~15 videos — a small dataset. '
        'Treat as early signals, not prescriptions. '
        'Experiment freely — the channel is still finding its winning formula.',
        '',
    ])

    # Write file
    output_path = project_root / 'channel-data' / 'channel-insights.md'
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text('\n'.join(lines), encoding='utf-8')
    except OSError as e:
        return {'error': f'Failed to write {output_path}: {e}'}

    return {
        'saved_to': str(output_path),
        'video_count': total_videos
    }


def _build_recommendations(
    topic_stats: List[Dict],
    channel_avg_conv: float,
    channel_avg_ret: float
) -> List[str]:
    """
    Build advisory topic recommendations with composite scoring reasoning.

    Surfaces both proven patterns AND novel/underexplored opportunities.
    Always uses advisory language ("has worked well historically," not "always do").

    Returns:
        List of recommendation strings
    """
    recs = []

    if not topic_stats:
        return ['Insufficient data for recommendations. Run backfill to populate database.']

    # Sort by composite of views + conversion for recommendations
    sorted_by_perf = sorted(
        topic_stats,
        key=lambda t: t['avg_views'] * 0.4 + t['avg_conversion'] * 1000 * 0.35,
        reverse=True
    )

    # Recommendation 1: Best performing pattern
    if sorted_by_perf:
        best = sorted_by_perf[0]
        ret_note = f", {best['avg_retention']:.1f}% avg retention" if best['avg_retention'] else ''
        recs.append(
            f"**{best['topic'].title()} topics** have historically performed well for this channel "
            f"(avg {best['avg_views']:,.0f} views, {best['avg_conversion']:.2f}% conversion{ret_note}). "
            f"{best['signal']} from {best['count']} video(s). "
            f"Consider making another {best['topic']} video."
        )

    # Recommendation 2: Second pattern if significantly different
    if len(sorted_by_perf) >= 2:
        second = sorted_by_perf[1]
        if second['topic'] != sorted_by_perf[0]['topic']:
            recs.append(
                f"**{second['topic'].title()} topics** also show solid results "
                f"({second['avg_views']:,.0f} avg views). "
                f"{second['signal']}."
            )

    # Recommendation 3: Novel/underexplored opportunity
    underexplored = [t for t in topic_stats if t['count'] == 1]
    if underexplored:
        ue = underexplored[0]
        recs.append(
            f"**{ue['topic'].title()} topics** are underexplored — only {ue['count']} video(s) so far. "
            f"Early data shows {ue['avg_views']:,.0f} views and {ue['avg_conversion']:.2f}% conversion. "
            f"This could be a breakout area worth testing."
        )

    # Recommendation 4: Retention insight
    high_ret = [t for t in topic_stats if t['avg_retention'] and t['avg_retention'] > channel_avg_ret]
    if high_ret:
        best_ret = max(high_ret, key=lambda t: t['avg_retention'])
        recs.append(
            f"**Retention leader:** {best_ret['topic'].title()} videos average "
            f"{best_ret['avg_retention']:.1f}% retention "
            f"(channel avg: {channel_avg_ret:.1f}%). "
            f"This format keeps viewers watching — a positive signal for algorithm reach."
        )

    # Safety note if all signals are early
    if all(t['count'] < 3 for t in topic_stats):
        recs.append(
            "**Data caveat:** All topic insights are early-signal (fewer than 3 videos each). "
            "Continue publishing across topics to build a clearer pattern."
        )

    return recs


# =========================================================================
# SIMPLE TOPIC CLASSIFIER (fallback if performance.py unavailable)
# =========================================================================

def classify_topic_type_simple(title: str) -> str:
    """Minimal topic classification fallback."""
    if not title:
        return 'general'
    title_lower = title.lower()
    for topic, keywords in EXPANDED_TOPIC_RULES.items():
        if any(kw in title_lower for kw in keywords):
            return topic
    return 'general'


# =========================================================================
# ORCHESTRATOR
# =========================================================================

def run_backfill(project_root: Path, force: bool = False, skip_markdown: bool = False) -> Dict[str, Any]:
    """
    Full backfill pipeline: JSON import → markdown import → reclassification → insights.

    Args:
        project_root: Path to project root
        force: Re-import data even if already present (update mode)
        skip_markdown: Skip Stage 2 (markdown parsing), useful for --json-only

    Returns:
        Combined results dict with keys:
            json_import, markdown_import, reclassified, insights_path, errors
    """
    results: Dict[str, Any] = {
        'json_import': {},
        'markdown_import': {},
        'reclassified': 0,
        'insights_path': None,
        'errors': []
    }

    # Stage 1: JSON import
    print("=" * 60)
    print("Stage 1: Importing from JSON pre-fetches")
    print("=" * 60)
    json_result = import_from_json_prefetch(project_root)
    results['json_import'] = json_result
    if json_result.get('errors'):
        results['errors'].extend(json_result['errors'])
    print()

    # Stage 2: Markdown import (optional)
    if not skip_markdown:
        print("=" * 60)
        print("Stage 2: Parsing POST-PUBLISH-ANALYSIS files")
        print("=" * 60)
        md_result = import_from_analysis_files(project_root, force=force)
        results['markdown_import'] = md_result
        print()
    else:
        print("Stage 2: Skipped (--json-only)")
        print()

    # Stage 3: Reclassify topics
    print("=" * 60)
    print("Stage 3: Reclassifying topic types")
    print("=" * 60)
    reclassified = reclassify_topics(project_root)
    results['reclassified'] = reclassified
    print(f"  Reclassified {reclassified} videos from 'general' to specific topic types")
    print()

    # Stage 4: Generate insights report
    print("=" * 60)
    print("Stage 4: Generating channel insights report")
    print("=" * 60)
    insights_result = generate_channel_insights_report(project_root)
    if 'error' in insights_result:
        results['errors'].append({'stage': 4, 'error': insights_result['error']})
        print(f"  WARNING: Could not generate insights: {insights_result['error']}")
    else:
        results['insights_path'] = insights_result['saved_to']
        print(f"  Channel insights saved to: {insights_result['saved_to']}")
        print(f"  Videos analyzed: {insights_result['video_count']}")
    print()

    return results


# =========================================================================
# CLI
# =========================================================================

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Backfill analytics database from existing channel data.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m tools.youtube_analytics.backfill              Full pipeline
  python -m tools.youtube_analytics.backfill --force      Re-import all (update mode)
  python -m tools.youtube_analytics.backfill --json-only  JSON import only, skip markdown
  python -m tools.youtube_analytics.backfill --insights-only  Skip all imports, regenerate report

Data source priority:
  1. _longform_enriched.json (20 videos, has CTR + retention)
  2. _longform_metrics.json (40 videos, basic metrics only)
  3. POST-PUBLISH-ANALYSIS markdown files (adds lessons_learned)

Output: tools/discovery/keywords.db (video_performance table)
        channel-data/channel-insights.md
        """
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Re-import data even if already present (update mode)'
    )
    parser.add_argument(
        '--insights-only',
        action='store_true',
        help='Skip all imports. Only regenerate channel-insights.md from existing DB.'
    )
    parser.add_argument(
        '--json-only',
        action='store_true',
        help='Only run JSON import and reclassification. Skip markdown parsing.'
    )

    args = parser.parse_args()

    project_root = Path(__file__).parent.parent.parent

    print()
    print("Analytics Backfill")
    print(f"Project root: {project_root}")
    print(f"Database: {project_root / 'tools' / 'discovery' / 'keywords.db'}")
    print()

    if args.insights_only:
        print("=" * 60)
        print("Insights-only mode: regenerating channel-insights.md")
        print("=" * 60)
        result = generate_channel_insights_report(project_root)
        if 'error' in result:
            print(f"ERROR: {result['error']}")
            sys.exit(1)
        print(f"Channel insights saved to: {result['saved_to']}")
        print(f"Videos analyzed: {result['video_count']}")
        sys.exit(0)

    # Full pipeline (or json-only)
    result = run_backfill(
        project_root=project_root,
        force=args.force,
        skip_markdown=args.json_only
    )

    # Final summary
    print("=" * 60)
    print("Backfill Complete")
    print("=" * 60)

    json_import = result.get('json_import', {})
    md_import = result.get('markdown_import', {})

    print(f"  Stage 1 (JSON import):    {json_import.get('imported', 0)} imported, "
          f"{json_import.get('skipped', 0)} skipped, "
          f"{len(json_import.get('errors', []))} errors")

    if not args.json_only:
        print(f"  Stage 2 (Markdown):       {md_import.get('processed', 0)} processed, "
              f"{md_import.get('skipped', 0)} skipped, "
              f"{md_import.get('errors', 0)} errors")

    print(f"  Stage 3 (Reclassified):   {result.get('reclassified', 0)} topics updated")

    if result.get('insights_path'):
        print(f"  Stage 4 (Insights):       Saved to {result['insights_path']}")
    else:
        stage4_err = next((e for e in result.get('errors', []) if e.get('stage') == 4), None)
        if stage4_err:
            print(f"  Stage 4 (Insights):       FAILED — {stage4_err['error']}")

    total_errors = len(result.get('errors', []))
    if total_errors > 0:
        print(f"\n  {total_errors} total error(s) — see above for details")

    print()
    sys.exit(0 if total_errors == 0 else 1)
