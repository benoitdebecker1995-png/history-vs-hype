"""
High-Impact Discovery DB Backfill

Populates 4 empty tables + expands keyword coverage + fixes keyword_performance linkage.

Tasks:
  1. title_variants — backfill from retitle recommendations + current titles
  2. thumbnail_variants — backfill from project folders (find .png/.psd files)
  3. section_feedback — extract from post-publish analyses (retention data)
  4. keyword_performance — link keywords to videos via title/tag matching
  5. keyword expansion — add keywords for in-production topics
  6. script_choices — extract hook type, structure from published scripts

Usage:
    python -m tools.discovery.backfill_high_impact [--all] [--titles] [--thumbnails]
        [--sections] [--kw-perf] [--kw-expand] [--scripts] [--dry-run]
"""

import sqlite3
import re
import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

DB_PATH = Path(__file__).parent / 'keywords.db'
PROJECT_ROOT = Path(__file__).parent.parent.parent
TODAY = datetime.now().strftime('%Y-%m-%d')


def get_conn():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


# =========================================================================
# TASK 1: TITLE VARIANTS
# =========================================================================

def backfill_title_variants(conn, dry_run=False):
    """Populate title_variants from video_performance + retitle recommendations."""
    c = conn.cursor()

    # Get all long-form videos with titles
    videos = c.execute(
        "SELECT video_id, title FROM video_performance "
        "WHERE topic_type != 'short' AND title IS NOT NULL"
    ).fetchall()

    # Check existing
    existing = set(r[0] for r in c.execute(
        "SELECT video_id FROM title_variants"
    ).fetchall())

    inserted = 0
    for v in videos:
        vid = v['video_id']
        if vid in existing:
            continue
        title = v['title']
        if not title:
            continue

        # Classify the title formula
        tags = classify_title_formula(title)

        if dry_run:
            print(f"  [DRY] {vid}: '{title[:50]}' -> {tags}")
            continue

        c.execute(
            "INSERT INTO title_variants (video_id, variant_letter, title_text, character_count, formula_tags, created_at) "
            "VALUES (?, 'A', ?, ?, ?, ?)",
            (vid, title, len(title), json.dumps(tags), TODAY)
        )
        inserted += 1

    # Now add known title swaps from retitle data
    known_swaps = get_known_title_swaps()
    for vid, swaps in known_swaps.items():
        for letter, (title, swap_date) in swaps.items():
            exists = c.execute(
                "SELECT 1 FROM title_variants WHERE video_id = ? AND variant_letter = ?",
                (vid, letter)
            ).fetchone()
            if exists:
                continue
            tags = classify_title_formula(title)
            if dry_run:
                print(f"  [DRY] SWAP {vid} variant {letter}: '{title[:50]}' -> {tags}")
                continue
            c.execute(
                "INSERT INTO title_variants (video_id, variant_letter, title_text, character_count, formula_tags, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (vid, letter, title, len(title), json.dumps(tags), swap_date or TODAY)
            )
            inserted += 1

    if not dry_run:
        conn.commit()
    print(f"Title variants: {inserted} inserted")
    return inserted


def classify_title_formula(title: str) -> List[str]:
    """Classify a title into formula tags based on proven patterns."""
    tags = []

    # Versus pattern
    if ' vs ' in title.lower() or ' vs. ' in title.lower():
        tags.append('versus')

    # Colon pattern
    if ':' in title:
        tags.append('colon')

    # Question
    if '?' in title:
        tags.append('question')

    # "The [X] That [Verb]" pattern
    if re.search(r'\bThe\s+\w+\s+That\s+\w+', title):
        tags.append('the_x_that')

    # "Here's" / evidence promise
    if "here's" in title.lower() or 'evidence' in title.lower() or 'proof' in title.lower() or 'prove' in title.lower():
        tags.append('evidence_promise')

    # How pattern
    if title.lower().startswith('how '):
        tags.append('how')

    # Why pattern
    if title.lower().startswith('why '):
        tags.append('why')

    # Declarative (no question, no colon, makes a statement)
    if not tags or (len(tags) == 1 and tags[0] in ('evidence_promise',)):
        if '?' not in title and ':' not in title:
            tags.append('declarative')

    # ALL CAPS words (clickbait signal)
    caps_words = re.findall(r'\b[A-Z]{3,}\b', title)
    if len(caps_words) >= 2:
        tags.append('caps_clickbait')

    # Number in title
    if re.search(r'\d', title):
        tags.append('has_number')

    # Year in title
    if re.search(r'\b(1[0-9]{3}|20[0-2][0-9])\b', title):
        tags.append('has_year')

    return tags


def get_known_title_swaps() -> Dict[str, Dict[str, Tuple[str, str]]]:
    """Return known title swaps from project status and retitle recommendations."""
    return {
        # Bermeja - swapped 2026-03-05
        'P6yalauLDic': {
            'A': ("The Phantom Island That Was on Maps for 400 Years", '2026-02-19'),
            'B': ("Mexico's Missing Island: The Map Error That Cost $22 Billion", '2026-03-05'),
        },
        # Dark Ages - candidate swaps from retitle recs
        'UxsXdUj0EhU': {
            'A': ("The Dark Ages Myth: Why Europe Didn't Go Dark after Rome", '2025-08-06'),
        },
        # Tariff
        'ejkC0ecYyxk': {
            'A': ("The 200-Year-Old Lie That Drains Your Bank Account", '2025-11-16'),
        },
        # Stalin
        '7fpBz6uo504': {
            'A': ("Was Stalin Really a Hero? The Evidence Says Otherwise", '2025-09-09'),
        },
        # Taiwan
        'BXyT8OTGBBo': {
            'A': ("The SHOCKING Truth About China's TAIWAN History", '2025-07-13'),
        },
    }


# =========================================================================
# TASK 2: THUMBNAIL VARIANTS
# =========================================================================

def backfill_thumbnail_variants(conn, dry_run=False):
    """Find thumbnail files in project folders and register them."""
    c = conn.cursor()

    existing = set(r[0] for r in c.execute(
        "SELECT video_id FROM thumbnail_variants"
    ).fetchall())

    # Scan project folders for thumbnail files
    production_dir = PROJECT_ROOT / 'video-projects' / '_IN_PRODUCTION'
    inserted = 0

    for project_dir in sorted(production_dir.iterdir()):
        if not project_dir.is_dir():
            continue

        # Find thumbnail files (PSD and PNG)
        thumb_files = []
        for ext in ('*.png', '*.psd', '*.jpg'):
            for f in project_dir.glob(ext):
                name_lower = f.name.lower()
                if 'thumbnail' in name_lower or 'thum' in name_lower:
                    thumb_files.append(f)
            # Also check _research subfolder
            for f in project_dir.glob(f'_research/{ext}'):
                name_lower = f.name.lower()
                if 'thumbnail' in name_lower or 'thum' in name_lower:
                    thumb_files.append(f)

        if not thumb_files:
            continue

        # Try to find video_id from POST-PUBLISH-ANALYSIS or PROJECT-STATUS
        video_id = find_video_id_for_project(project_dir)
        if not video_id:
            continue
        if video_id in existing:
            continue

        # Classify thumbnails by letter (A, B, C) or sequential
        for i, tf in enumerate(sorted(thumb_files)):
            # Try to extract variant letter from filename
            letter = extract_variant_letter(tf.name) or chr(65 + i)  # A, B, C...

            # Only register PNGs (final renders), skip PSDs
            if tf.suffix.lower() != '.png':
                continue

            # Extract visual pattern tags
            vis_tags = classify_thumbnail(tf.name)

            rel_path = str(tf.relative_to(PROJECT_ROOT))

            if dry_run:
                print(f"  [DRY] {video_id} variant {letter}: {rel_path} -> {vis_tags}")
                continue

            c.execute(
                "INSERT INTO thumbnail_variants (video_id, variant_letter, file_path, visual_pattern_tags, created_at) "
                "VALUES (?, ?, ?, ?, ?)",
                (video_id, letter, rel_path, json.dumps(vis_tags), TODAY)
            )
            inserted += 1

    if not dry_run:
        conn.commit()
    print(f"Thumbnail variants: {inserted} inserted")
    return inserted


def find_video_id_for_project(project_dir: Path) -> Optional[str]:
    """Extract video ID from project files."""
    # Check POST-PUBLISH-ANALYSIS.md
    for fname in ('POST-PUBLISH-ANALYSIS.md', 'PROJECT-STATUS.md', 'YOUTUBE-METADATA.md'):
        fpath = project_dir / fname
        if fpath.exists():
            try:
                text = fpath.read_text(encoding='utf-8', errors='replace')
                # Look for YouTube video ID patterns
                m = re.search(r'(?:Video ID|video_id|youtu\.be/|watch\?v=)[:\s]*([a-zA-Z0-9_-]{11})', text)
                if m:
                    return m.group(1)
            except Exception:
                pass
    return None


def extract_variant_letter(filename: str) -> Optional[str]:
    """Extract A/B/C variant letter from thumbnail filename."""
    m = re.search(r'[Tt]humbnail\s*([A-Ca-c])', filename)
    if m:
        return m.group(1).upper()
    m = re.search(r'(?:redo|new)\s*(\d)', filename, re.IGNORECASE)
    if m:
        # redo 1 = B, redo 2 = C
        num = int(m.group(1))
        return chr(64 + num + 1)  # 1->B, 2->C
    return None


def classify_thumbnail(filename: str) -> List[str]:
    """Classify thumbnail type from filename patterns."""
    tags = []
    lower = filename.lower()
    if 'redo' in lower or 'new' in lower:
        tags.append('revision')
    if re.search(r'[a-c]\.', lower):
        tags.append('ab_test')
    return tags


# =========================================================================
# TASK 3: SECTION FEEDBACK
# =========================================================================

def backfill_section_feedback(conn, dry_run=False):
    """Extract section-level retention data from post-publish analyses."""
    c = conn.cursor()

    existing_videos = set(r[0] for r in c.execute(
        "SELECT DISTINCT video_id FROM section_feedback"
    ).fetchall())

    analyses_dir = PROJECT_ROOT / 'channel-data' / 'analyses'
    inserted = 0

    for analysis_file in sorted(analyses_dir.glob('POST-PUBLISH-ANALYSIS-*.md')):
        # Extract video ID from filename
        video_id = analysis_file.stem.replace('POST-PUBLISH-ANALYSIS-', '')
        if video_id in existing_videos:
            continue

        try:
            text = analysis_file.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue

        # Extract section-level retention data
        sections = extract_retention_sections(text, video_id)

        for section in sections:
            if dry_run:
                print(f"  [DRY] {video_id}: {section['name']} -> {section['retention']}%")
                continue

            c.execute(
                "INSERT INTO section_feedback (video_id, section_name, retention_percent, notes, created_at) "
                "VALUES (?, ?, ?, ?, ?)",
                (video_id, section['name'], section['retention'], section.get('notes'), TODAY)
            )
            inserted += 1

    # Also check project-level POST-PUBLISH-ANALYSIS.md files
    production_dir = PROJECT_ROOT / 'video-projects' / '_IN_PRODUCTION'
    for project_dir in sorted(production_dir.iterdir()):
        if not project_dir.is_dir():
            continue
        analysis_file = project_dir / 'POST-PUBLISH-ANALYSIS.md'
        if not analysis_file.exists():
            continue

        video_id = find_video_id_for_project(project_dir)
        if not video_id or video_id in existing_videos:
            continue

        try:
            text = analysis_file.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue

        sections = extract_retention_sections(text, video_id)
        for section in sections:
            if dry_run:
                print(f"  [DRY] {video_id}: {section['name']} -> {section['retention']}%")
                continue
            c.execute(
                "INSERT INTO section_feedback (video_id, section_name, retention_percent, notes, created_at) "
                "VALUES (?, ?, ?, ?, ?)",
                (video_id, section['name'], section['retention'], section.get('notes'), TODAY)
            )
            inserted += 1
        existing_videos.add(video_id)

    if not dry_run:
        conn.commit()
    print(f"Section feedback: {inserted} inserted")
    return inserted


def extract_retention_sections(text: str, video_id: str) -> List[Dict]:
    """Parse retention/section data from a post-publish analysis markdown."""
    sections = []

    # Extract overall retention: "**Average retention:** 35.6%"
    avg_ret_m = re.search(r'\*\*Average retention:\*\*\s*(\d+(?:\.\d+)?)\s*%', text)
    if avg_ret_m:
        sections.append({
            'name': 'overall',
            'retention': float(avg_ret_m.group(1)),
            'notes': 'Average retention',
        })

    # Extract final retention: "**Final retention:** 20.4%"
    final_ret_m = re.search(r'\*\*Final retention:\*\*\s*(\d+(?:\.\d+)?)\s*%', text)
    if final_ret_m:
        sections.append({
            'name': 'final',
            'retention': float(final_ret_m.group(1)),
            'notes': 'Final retention',
        })

    # Pattern 1: Drop-off table "| Position | Viewers Lost | Location |"
    # "| 3% | 8.0% dropped | intro |"
    drop_table_pattern = re.compile(
        r'\|\s*(\d+)%\s*\|\s*(\d+(?:\.\d+)?)%\s*dropped\s*\|\s*(\w+)\s*\|'
    )
    for m in drop_table_pattern.finditer(text):
        sections.append({
            'name': f'drop_{m.group(3)}_{m.group(1)}pct',
            'retention': 100.0 - float(m.group(2)),  # Convert "dropped" to retention
            'notes': f'{m.group(2)}% dropped at {m.group(1)}% ({m.group(3)})',
        })

    # Pattern 2: Table rows like "| 0:00-1:30 | Hook | 45% | Good opening |"
    time_table_pattern = re.compile(
        r'\|\s*(\d+:\d+(?:-\d+:\d+)?)\s*\|\s*([^|]+?)\s*\|\s*(\d+(?:\.\d+)?)\s*%?\s*\|([^|]*)\|'
    )
    for m in time_table_pattern.finditer(text):
        sections.append({
            'name': m.group(2).strip(),
            'retention': float(m.group(3)),
            'notes': m.group(4).strip() or None,
        })

    # Pattern 3: Bullet points "- Hook (0:00-0:45): 52% retention"
    bullet_pattern = re.compile(
        r'-\s*\*?\*?([^(]+?)\*?\*?\s*\((\d+:\d+[^)]*)\)\s*:?\s*(\d+(?:\.\d+)?)\s*%'
    )
    for m in bullet_pattern.finditer(text):
        sections.append({
            'name': m.group(1).strip(),
            'retention': float(m.group(3)),
            'notes': None,
        })

    # Pattern 4: "Major drop-off at 2% (intro) - 20.0% viewers lost"
    lesson_drop_pattern = re.compile(
        r'drop-off at (\d+)%\s*\((\w+)\)\s*-\s*(\d+(?:\.\d+)?)%\s*viewers lost'
    )
    for m in lesson_drop_pattern.finditer(text):
        sections.append({
            'name': f'lesson_drop_{m.group(2)}_{m.group(1)}pct',
            'retention': 100.0 - float(m.group(3)),
            'notes': f'Lesson: {m.group(3)}% lost at {m.group(1)}% ({m.group(2)})',
        })

    return sections


# =========================================================================
# TASK 4: KEYWORD-PERFORMANCE LINKAGE
# =========================================================================

def backfill_keyword_performance(conn, dry_run=False):
    """Link keywords to videos that target them via title/topic matching."""
    c = conn.cursor()

    # Get all keywords
    keywords = c.execute("SELECT id, keyword FROM keywords").fetchall()

    # Get all long-form videos with metrics
    videos = c.execute(
        "SELECT video_id, title, views, topic_type FROM video_performance "
        "WHERE topic_type != 'short' AND title IS NOT NULL"
    ).fetchall()

    # Get existing linkages
    existing = set()
    for r in c.execute("SELECT keyword_id, video_id FROM keyword_performance"):
        existing.add((r[0], r[1]))

    # Get CTR data for videos
    ctr_data = {}
    for r in c.execute(
        "SELECT video_id, ctr_percent, impression_count, view_count "
        "FROM ctr_snapshots ORDER BY snapshot_date DESC"
    ):
        if r['video_id'] not in ctr_data:
            ctr_data[r['video_id']] = r

    inserted = 0
    for kw in keywords:
        kw_id = kw['id']
        kw_text = kw['keyword'].lower()
        kw_words = set(kw_text.split())

        for v in videos:
            if (kw_id, v['video_id']) in existing:
                continue

            title_lower = v['title'].lower()

            # Match if keyword words appear in title (allow partial)
            title_words = set(re.findall(r'\w+', title_lower))
            overlap = kw_words & title_words

            # Require at least 60% of keyword words to match
            if len(overlap) < max(1, len(kw_words) * 0.6):
                continue

            ctr = ctr_data.get(v['video_id'])

            if dry_run:
                print(f"  [DRY] kw='{kw['keyword']}' -> vid={v['video_id']} ({v['title'][:40]})")
                continue

            c.execute(
                "INSERT INTO keyword_performance (keyword_id, video_id, impressions, ctr, views, measured_date) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (
                    kw_id,
                    v['video_id'],
                    int(ctr['impression_count']) if ctr else None,
                    float(ctr['ctr_percent']) if ctr else None,
                    v['views'],
                    TODAY,
                )
            )
            inserted += 1

    if not dry_run:
        conn.commit()
    print(f"Keyword-performance links: {inserted} inserted")
    return inserted


# =========================================================================
# TASK 5: KEYWORD EXPANSION
# =========================================================================

NEW_KEYWORDS = {
    # Berlin Conference (project 40 - in editing)
    'berlin conference 1884': {'volume': 11648, 'source': 'manual'},
    'scramble for africa history': {'volume': 8000, 'source': 'manual'},
    'partition of africa': {'volume': 3200, 'source': 'manual'},
    'africa colonization history': {'volume': 5400, 'source': 'manual'},
    'berlin conference africa map': {'volume': 2400, 'source': 'manual'},

    # Treaty of Tordesillas (project 41)
    'treaty of tordesillas': {'volume': 2703, 'source': 'manual'},
    'tordesillas line': {'volume': 800, 'source': 'manual'},
    'pope divided the world': {'volume': 600, 'source': 'manual'},
    'spain portugal divided world': {'volume': 500, 'source': 'manual'},

    # Adwa/Wuchale Treaty (project 39)
    'battle of adwa': {'volume': 2900, 'source': 'manual'},
    'treaty of wuchale': {'volume': 1200, 'source': 'manual'},
    'ethiopia colonization': {'volume': 2000, 'source': 'manual'},
    'menelik ii italy': {'volume': 800, 'source': 'manual'},
    'ethiopia never colonized': {'volume': 3600, 'source': 'manual'},

    # Panama Canal (project 36)
    'panama canal history': {'volume': 6600, 'source': 'manual'},
    'panama canal treaty': {'volume': 1900, 'source': 'manual'},
    'torrijos carter treaty': {'volume': 800, 'source': 'manual'},
    'deconcini reservation panama': {'volume': 200, 'source': 'manual'},

    # Vichy Statut des Juifs (project 37 - just published)
    'vichy france jewish laws': {'volume': 900, 'source': 'manual'},
    'statut des juifs 1940': {'volume': 400, 'source': 'manual'},
    'petain anti jewish law': {'volume': 300, 'source': 'manual'},
    'vichy france holocaust': {'volume': 2400, 'source': 'manual'},

    # Gibraltar (project 35 - published)
    'treaty of utrecht gibraltar': {'volume': 800, 'source': 'manual'},
    'gibraltar sovereignty dispute': {'volume': 600, 'source': 'manual'},
    'spain gibraltar border': {'volume': 500, 'source': 'manual'},

    # Greenland (project 33)
    'greenland independence': {'volume': 2900, 'source': 'manual'},
    'greenland denmark history': {'volume': 1200, 'source': 'manual'},
    'trump buy greenland': {'volume': 8100, 'source': 'manual'},

    # High-value pipeline topics (from TOPIC-PIPELINE.md)
    'crimea annexation history': {'volume': 1528, 'source': 'manual'},
    'crimea russia ukraine': {'volume': 4400, 'source': 'manual'},
    'viking misconceptions': {'volume': 923, 'source': 'manual'},
    'viking mythology debunked': {'volume': 600, 'source': 'manual'},
    'monroe doctrine history': {'volume': 1245, 'source': 'manual'},
    'kashmir partition history': {'volume': 2000, 'source': 'manual'},
    'falklands malvinas dispute': {'volume': 1400, 'source': 'manual'},
    'antarctic treaty 2048': {'volume': 800, 'source': 'manual'},
}


def backfill_keywords(conn, dry_run=False):
    """Add keywords for in-production and pipeline topics."""
    c = conn.cursor()

    existing = set(r[0] for r in c.execute("SELECT keyword FROM keywords"))

    inserted = 0
    for kw, meta in NEW_KEYWORDS.items():
        if kw in existing:
            continue

        if dry_run:
            print(f"  [DRY] ADD keyword: '{kw}' (vol={meta['volume']})")
            continue

        c.execute(
            "INSERT INTO keywords (keyword, search_volume, first_discovered, last_updated, source) "
            "VALUES (?, ?, ?, ?, ?)",
            (kw, meta['volume'], TODAY, TODAY, meta['source'])
        )
        inserted += 1

    if not dry_run:
        conn.commit()
    print(f"Keywords expanded: {inserted} new keywords added (was {len(existing)}, now {len(existing) + inserted})")
    return inserted


# =========================================================================
# TASK 6: SCRIPT CHOICES
# =========================================================================

def backfill_script_choices(conn, dry_run=False):
    """Populate script_choices with hook/structure data for published long-form videos.

    Uses existing schema: choice_type, project_path, topic_type, selected_variant,
    selected_technique, rejected_variants, recommended_technique, choice_date
    """
    c = conn.cursor()

    existing = set()
    for r in c.execute("SELECT project_path, choice_type FROM script_choices"):
        existing.add((r[0], r[1]))

    # Known script patterns from analyses
    choices = [
        ('hook', 'oDK52GwjTIo', 'territorial', 'specific_number', 'modern_consequence_first'),
        ('structure', 'oDK52GwjTIo', 'territorial', 'chronological', 'ongoing_stakes_close'),
        ('hook', 'UxsXdUj0EhU', 'ideological', 'myth_statement', 'popular_myth_challenge'),
        ('structure', 'UxsXdUj0EhU', 'ideological', 'myth_then_evidence', 'modern_belief_connection_close'),
        ('hook', 'Yx5oywZs-rk', 'ideological', 'myth_vs_evidence', 'modern_debate_hook'),
        ('structure', 'Yx5oywZs-rk', 'ideological', 'claim_by_claim', 'nuance_synthesis_close'),
        ('hook', 'n-CUSE4bDvg', 'territorial', 'geographic_mystery', 'map_anomaly'),
        ('structure', 'n-CUSE4bDvg', 'territorial', 'narrative_discovery', 'ironic_twist_close'),
        ('hook', 'P6yalauLDic', 'territorial', 'mystery', 'disappearance_hook'),
        ('structure', 'P6yalauLDic', 'territorial', 'investigation', 'unresolved_mystery_close'),
        ('hook', 'Q5Pfv_dPubU', 'colonial', 'document_reveal', 'classified_document'),
        ('structure', 'Q5Pfv_dPubU', 'colonial', 'chronological', 'ongoing_justice_close'),
        ('hook', 'WZnCxVPNF7A', 'territorial', 'treaty_clause', 'document_close_read'),
        ('structure', 'WZnCxVPNF7A', 'territorial', 'legal_analysis', 'modern_negotiation_close'),
        ('hook', 'ejkC0ecYyxk', 'ideological', 'provocative_claim', 'personal_impact'),
        ('structure', 'ejkC0ecYyxk', 'ideological', 'evidence_stack', 'ongoing_stakes_close'),
    ]

    inserted = 0
    for choice_type, path, topic, variant, technique in choices:
        if (path, choice_type) in existing:
            continue

        if dry_run:
            print(f"  [DRY] {path}: {choice_type}={variant}")
            continue

        c.execute(
            "INSERT INTO script_choices (choice_type, project_path, topic_type, "
            "selected_variant, selected_technique, choice_date) VALUES (?, ?, ?, ?, ?, ?)",
            (choice_type, path, topic, variant, technique, TODAY)
        )
        inserted += 1

    if not dry_run:
        conn.commit()
    print(f"Script choices: {inserted} inserted")
    return inserted


# =========================================================================
# MAIN
# =========================================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description='High-impact discovery DB backfill')
    parser.add_argument('--all', action='store_true', help='Run all tasks')
    parser.add_argument('--titles', action='store_true', help='Backfill title_variants')
    parser.add_argument('--thumbnails', action='store_true', help='Backfill thumbnail_variants')
    parser.add_argument('--sections', action='store_true', help='Backfill section_feedback')
    parser.add_argument('--kw-perf', action='store_true', help='Fix keyword_performance linkage')
    parser.add_argument('--kw-expand', action='store_true', help='Add new keywords')
    parser.add_argument('--scripts', action='store_true', help='Backfill script_choices')
    parser.add_argument('--dry-run', action='store_true', help='Preview without writing')
    args = parser.parse_args()

    if not any([args.all, args.titles, args.thumbnails, args.sections, args.kw_perf, args.kw_expand, args.scripts]):
        args.all = True

    conn = get_conn()

    try:
        if args.all or args.kw_expand:
            print("\n=== KEYWORD EXPANSION ===")
            backfill_keywords(conn, args.dry_run)

        if args.all or args.titles:
            print("\n=== TITLE VARIANTS ===")
            backfill_title_variants(conn, args.dry_run)

        if args.all or args.thumbnails:
            print("\n=== THUMBNAIL VARIANTS ===")
            backfill_thumbnail_variants(conn, args.dry_run)

        if args.all or args.sections:
            print("\n=== SECTION FEEDBACK ===")
            backfill_section_feedback(conn, args.dry_run)

        if args.all or args.kw_perf:
            print("\n=== KEYWORD-PERFORMANCE LINKAGE ===")
            backfill_keyword_performance(conn, args.dry_run)

        if args.all or args.scripts:
            print("\n=== SCRIPT CHOICES ===")
            backfill_script_choices(conn, args.dry_run)

    finally:
        conn.close()

    print("\nDone.")


if __name__ == '__main__':
    main()
