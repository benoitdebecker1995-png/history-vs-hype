"""
YouTube Cross-Video Pattern Analysis Module

Collects video data across all POST-PUBLISH-ANALYSIS files, auto-tags videos by topic,
and generates aggregated performance insights.

This module enables cross-video pattern recognition by:
1. Collecting POST-PUBLISH-ANALYSIS.md files from all project folders
2. Auto-tagging videos by topic based on title/description keywords
3. Aggregating metrics by topic type with minimum sample size enforcement
4. Generating insights-first reports with actionable recommendations
5. Extracting title structure and thumbnail metadata for CTR correlation

Usage:
    CLI:
        python patterns.py              # Show collected video data
        python patterns.py --tags       # Show videos with auto-tags
        python patterns.py --topic-report    # Generate TOPIC-ANALYSIS.md
        python patterns.py --title-report    # Generate TITLE-PATTERNS.md

    Python:
        from patterns import collect_video_data, auto_tag_video, aggregate_by_topic
        from patterns import identify_winners, generate_topic_report
        from patterns import extract_title_structure, extract_thumbnail_metadata
        from patterns import generate_title_patterns_report

        videos = collect_video_data()
        enriched = enrich_video_data(videos)
        topic_stats = aggregate_by_topic(enriched)
        generate_topic_report()
        generate_title_patterns_report()

Dependencies:
    - Standard library only (pathlib, re, glob, statistics, datetime)
    - No external packages required
"""

import re
import sys
import json
import glob as glob_module
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict
from statistics import mean


# Determine project root (2 levels up from tools/youtube-analytics/)
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent


# Fixed vocabulary for consistent topic tagging
TAG_VOCABULARY = {
    'territorial': ['dispute', 'border', 'territory', 'claim', 'annex', 'occupation', 'icj', 'sovereignty'],
    'ideological': ['myth', 'debunk', 'fact-check', 'propaganda', 'narrative', 'lie'],
    'colonial': ['colonial', 'empire', 'independence', 'decolonization', 'imperial'],
    'politician': ['vance', 'netanyahu', 'trump', 'fuentes', 'reagan', 'politician'],
    'archaeological': ['dna', 'excavation', 'artifact', 'manuscript', 'archaeology'],
    'medieval': ['medieval', 'dark ages', 'crusade', 'viking', 'middle ages'],
}


# Country names for title pattern detection (comprehensive list for history channel)
COUNTRY_NAMES = [
    'America', 'United States', 'USA', 'Britain', 'UK', 'England', 'France', 'Germany',
    'Russia', 'China', 'Israel', 'Palestine', 'Ukraine', 'Iran', 'Iraq', 'Syria',
    'Egypt', 'India', 'Japan', 'Spain', 'Portugal', 'Netherlands', 'Belgium', 'Italy',
    'Austria', 'Hungary', 'Poland', 'Turkey', 'Greece', 'Serbia', 'Croatia', 'Bosnia',
    'Kosovo', 'Cyprus', 'Lebanon', 'Jordan', 'Saudi', 'Yemen', 'Libya', 'Algeria',
    'Morocco', 'Tunisia', 'Ethiopia', 'Somalia', 'Somaliland', 'Kenya', 'Uganda',
    'Rwanda', 'Congo', 'Nigeria', 'Ghana', 'South Africa', 'Zimbabwe', 'Zambia',
    'Mozambique', 'Angola', 'Namibia', 'Botswana', 'Mexico', 'Brazil', 'Argentina',
    'Chile', 'Peru', 'Colombia', 'Venezuela', 'Cuba', 'Haiti', 'Jamaica', 'Canada',
    'Australia', 'New Zealand', 'Philippines', 'Vietnam', 'Thailand', 'Indonesia',
    'Malaysia', 'Singapore', 'Korea', 'Taiwan', 'Belize', 'Guatemala', 'Sudan',
    'Eritrea', 'Djibouti', 'Chagos', 'Mauritius',
]


def detect_title_pattern(title: str) -> str:
    """
    Identify which proven title pattern the title matches.

    Based on COMPETITOR-TITLE-DATABASE.md analysis of high-performing titles.
    Returns pattern name for aggregation, or 'other' if no pattern matches.

    Args:
        title: Video title to analyze

    Returns:
        str: Pattern name (e.g., "[X]'s [Noun] Problem", "Why [X] Is/Are [Verb]")
    """
    if not title:
        return 'other'

    patterns = [
        (r"^.+'s\s+\w+\s+Problem$", "[X]'s [Noun] Problem"),
        (r"^Why\s+.+\s+(Is|Are|Was|Were)\s+", "Why [X] Is/Are [Verb]"),
        (r"^How\s+.+\s+(Got|Became|Turned)\s+", "How [X] Got/Became [Adj]"),
        (r"^The\s+.+\s+That\s+", "The [X] That [Verb]"),
        (r"^What\s+.+\?$", "What [Question]"),
        (r"\?$", "[Question]"),
        (r":\s+.+$", "[Topic]: [Subtitle]"),
        (r"^Fact[- ]Check", "Fact-Check [Subject]"),
        (r"^The\s+(Real|True|Actual)\s+", "The Real/True [X]"),
    ]

    for regex, pattern_name in patterns:
        if re.search(regex, title, re.IGNORECASE):
            return pattern_name

    return 'other'


def extract_title_structure(title: str) -> dict:
    """
    Extract structural attributes from video title.

    Parses title structure for correlation with CTR data.
    Used for pattern analysis in TITLE-PATTERNS.md report.

    Args:
        title: Video title to analyze

    Returns:
        dict with title attributes:
            - length: Character count
            - word_count: Word count
            - has_colon: Contains ':'
            - has_question: Contains '?'
            - has_number: Contains any digit
            - has_year: Contains 4-digit year (19xx or 20xx)
            - has_country: Contains country name from COUNTRY_NAMES
            - pattern: Detected title pattern (from detect_title_pattern)
            - first_word: First word of title
    """
    if not title:
        return {
            'length': 0,
            'word_count': 0,
            'has_colon': False,
            'has_question': False,
            'has_number': False,
            'has_year': False,
            'has_country': False,
            'pattern': 'other',
            'first_word': '',
        }

    # Build regex pattern for country names
    country_pattern = r'\b(' + '|'.join(re.escape(c) for c in COUNTRY_NAMES) + r')\b'

    return {
        'length': len(title),
        'word_count': len(title.split()),
        'has_colon': ':' in title,
        'has_question': '?' in title,
        'has_number': bool(re.search(r'\d+', title)),
        'has_year': bool(re.search(r'\b(19|20)\d{2}\b', title)),
        'has_country': bool(re.search(country_pattern, title, re.IGNORECASE)),
        'pattern': detect_title_pattern(title),
        'first_word': title.split()[0] if title.split() else '',
    }


def collect_video_data() -> list[dict]:
    """
    Collect all analyzed video data from POST-PUBLISH-ANALYSIS files.

    Search locations (in order):
    1. channel-data/analyses/POST-PUBLISH-ANALYSIS-*.md
    2. video-projects/_IN_PRODUCTION/*/POST-PUBLISH-ANALYSIS.md
    3. video-projects/_READY_TO_FILM/*/POST-PUBLISH-ANALYSIS.md
    4. video-projects/_ARCHIVED/*/POST-PUBLISH-ANALYSIS.md

    Returns:
        list[dict] where each dict has:
            - video_id: str
            - title: str
            - views: int or None
            - watch_time_minutes: float or None
            - avg_retention: float (decimal, e.g., 0.32) or None
            - ctr_percent: float or None
            - analyzed_date: str or None
            - source_file: str (path to analysis file)
    """
    videos = []

    # Search patterns in order
    search_patterns = [
        PROJECT_ROOT / 'channel-data' / 'analyses' / 'POST-PUBLISH-ANALYSIS*.md',
        PROJECT_ROOT / 'video-projects' / '_IN_PRODUCTION' / '*' / 'POST-PUBLISH-ANALYSIS.md',
        PROJECT_ROOT / 'video-projects' / '_READY_TO_FILM' / '*' / 'POST-PUBLISH-ANALYSIS.md',
        PROJECT_ROOT / 'video-projects' / '_ARCHIVED' / '*' / 'POST-PUBLISH-ANALYSIS.md',
    ]

    seen_files = set()

    for pattern in search_patterns:
        for filepath in glob_module.glob(str(pattern)):
            if filepath in seen_files:
                continue
            seen_files.add(filepath)

            parsed = parse_analysis_file(filepath)
            if parsed:
                videos.append(parsed)

    return videos


def parse_analysis_file(filepath: str) -> dict | None:
    """
    Parse a POST-PUBLISH-ANALYSIS.md file and extract structured data.

    Args:
        filepath: Path to the analysis file

    Returns:
        dict with extracted fields, or None if parsing fails
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except (IOError, UnicodeDecodeError):
        return None

    data = {
        'video_id': None,
        'title': None,
        'views': None,
        'watch_time_minutes': None,
        'avg_retention': None,
        'ctr_percent': None,
        'analyzed_date': None,
        'source_file': filepath,
    }

    # Extract video_id from "**Video ID:**" line
    video_id_match = re.search(r'\*\*Video ID:\*\*\s*(\S+)', content)
    if video_id_match:
        data['video_id'] = video_id_match.group(1)

    # Extract title from h1 header or "# Post-Publish Analysis: {title}"
    title_match = re.search(r'^#\s+Post-Publish Analysis:\s*(.+)$', content, re.MULTILINE)
    if title_match:
        data['title'] = title_match.group(1).strip()
    else:
        # Try generic h1
        h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if h1_match:
            data['title'] = h1_match.group(1).strip()

    # Extract views from Performance table (| Views | X |)
    views_match = re.search(r'\|\s*Views\s*\|\s*([\d,]+)', content, re.IGNORECASE)
    if views_match:
        data['views'] = int(views_match.group(1).replace(',', ''))

    # Extract watch_time_minutes from Performance table
    watch_time_match = re.search(r'\|\s*Watch Time.*?\|\s*([\d,]+)', content, re.IGNORECASE)
    if watch_time_match:
        data['watch_time_minutes'] = float(watch_time_match.group(1).replace(',', ''))

    # Extract avg_retention from "**Average retention:**" line
    retention_match = re.search(r'\*\*Average retention:\*\*\s*([\d.]+)%', content)
    if retention_match:
        # Convert percentage to decimal
        data['avg_retention'] = float(retention_match.group(1)) / 100

    # Extract CTR from "**CTR:**" line if available
    ctr_match = re.search(r'\*\*CTR:\*\*\s*([\d.]+)%', content)
    if ctr_match:
        data['ctr_percent'] = float(ctr_match.group(1))
    else:
        # Check for "Not available" indication
        if re.search(r'\*\*CTR:\*\*\s*Not available', content, re.IGNORECASE):
            data['ctr_percent'] = None

    # Extract analyzed_date from "**Analyzed:**" line
    analyzed_match = re.search(r'\*\*Analyzed:\*\*\s*(\S+)', content)
    if analyzed_match:
        data['analyzed_date'] = analyzed_match.group(1)

    # Only return if we got at least video_id or title
    if data['video_id'] or data['title']:
        return data

    return None


def auto_tag_video(title: str, description: str = '') -> list[str]:
    """
    Auto-detect topic tags from video metadata.

    Uses TAG_VOCABULARY to match keywords in title and description.
    A video can have multiple tags (e.g., ['territorial', 'colonial']).

    Args:
        title: Video title
        description: Optional video description

    Returns:
        list[str] of matching tags, or ['uncategorized'] if no matches
    """
    text = f"{title} {description}".lower()
    tags = []

    for tag, keywords in TAG_VOCABULARY.items():
        if any(kw in text for kw in keywords):
            tags.append(tag)

    return tags or ['uncategorized']


def find_project_folder_for_video(title: str) -> str | None:
    """
    Find project folder matching video title.

    Search strategy:
    1. Extract significant words (>3 chars) from title
    2. Search video-projects lifecycle folders for matching folder names
    3. Return folder path if found, None otherwise

    Args:
        title: Video title to match

    Returns:
        Path to project folder if found, None otherwise
    """
    if not title:
        return None

    # Extract significant words (>3 chars) from title
    slug_words = re.sub(r'[^a-z0-9]+', ' ', title.lower()).split()
    significant_words = [w for w in slug_words if len(w) > 3]

    if not significant_words:
        return None

    search_paths = [
        PROJECT_ROOT / 'video-projects' / '_IN_PRODUCTION' / '*',
        PROJECT_ROOT / 'video-projects' / '_READY_TO_FILM' / '*',
        PROJECT_ROOT / 'video-projects' / '_ARCHIVED' / '*',
    ]

    for pattern in search_paths:
        for folder in glob_module.glob(str(pattern)):
            if not Path(folder).is_dir():
                continue
            folder_name = Path(folder).name.lower()
            if any(word in folder_name for word in significant_words):
                return folder

    return None


def extract_thumbnail_metadata(project_folder: str | None) -> dict:
    """
    Extract thumbnail attributes from project YOUTUBE-METADATA.md file.

    Parses thumbnail characteristics for correlation with CTR data.

    Args:
        project_folder: Path to project folder (may be None)

    Returns:
        dict with thumbnail attributes:
            - type: 'map', 'face', 'document', 'mixed', or 'unknown'
            - has_text: Whether thumbnail has text overlay
            - has_person: Whether thumbnail includes a person/face
            - has_map: Whether thumbnail includes a map
            - description: Extracted thumbnail description if available
    """
    metadata = {
        'type': 'unknown',
        'has_text': False,
        'has_person': False,
        'has_map': False,
        'description': None,
    }

    if not project_folder:
        return metadata

    metadata_path = Path(project_folder) / 'YOUTUBE-METADATA.md'
    if not metadata_path.exists():
        return metadata

    try:
        content = metadata_path.read_text(encoding='utf-8').lower()

        # Parse thumbnail section - detect thumbnail type
        if 'map-focused' in content or 'map thumbnail' in content or 'map:' in content:
            metadata['type'] = 'map'
            metadata['has_map'] = True
        if 'face' in content or 'person' in content or 'talking head' in content:
            metadata['has_person'] = True
            if metadata['type'] == 'unknown':
                metadata['type'] = 'face'
        if 'text overlay' in content or 'text:' in content or 'text options' in content:
            metadata['has_text'] = True
        if 'document' in content or 'primary source' in content or 'manuscript' in content:
            if metadata['type'] == 'unknown':
                metadata['type'] = 'document'

        # Detect mixed type (e.g., map with text)
        detected_features = sum([metadata['has_map'], metadata['has_person'], metadata['has_text']])
        if detected_features >= 2 and metadata['type'] != 'unknown':
            metadata['type'] = 'mixed'

        # Try to extract thumbnail description
        thumb_match = re.search(r'thumbnail[:\s]+([^\n]+)', content)
        if thumb_match:
            desc = thumb_match.group(1).strip()
            # Clean up common patterns
            if desc and not desc.startswith('option') and not desc.startswith('#'):
                metadata['description'] = desc[:100]  # Truncate for display

    except (IOError, UnicodeDecodeError):
        pass

    return metadata


def aggregate_by_thumbnail(videos: list[dict], min_count: int = 2) -> dict:
    """
    Aggregate performance by thumbnail characteristics.

    Groups videos by thumbnail type and attributes.

    Args:
        videos: List of video data dicts with 'thumbnail' and metrics
        min_count: Minimum videos per group to include (default 2)

    Returns:
        dict with two sections:
        {
            'by_type': {
                'map': {'count': 4, 'avg_views': 2100, 'avg_ctr': 5.2, 'avg_retention': 0.34},
                'face': {...},
                ...
            },
            'by_attribute': {
                'has_text': {
                    'with': {'count': 5, 'avg_views': 1400, 'avg_ctr': 4.2},
                    'without': {'count': 3, 'avg_views': 1200, 'avg_ctr': 3.8},
                    'delta_views': 16.7,
                    'delta_ctr': 10.5,
                },
                ...
            },
        }
    """
    # Aggregate by type
    by_type_groups = defaultdict(list)
    for v in videos:
        thumb = v.get('thumbnail', {})
        thumb_type = thumb.get('type', 'unknown')
        if v.get('views') is not None:
            by_type_groups[thumb_type].append(v)

    by_type_result = {}
    for thumb_type, vids in by_type_groups.items():
        if len(vids) >= min_count:
            views_list = [v['views'] for v in vids]
            ctr_list = [v['ctr_percent'] for v in vids if v.get('ctr_percent') is not None]
            ret_list = [v['avg_retention'] for v in vids if v.get('avg_retention') is not None]

            by_type_result[thumb_type] = {
                'count': len(vids),
                'avg_views': mean(views_list) if views_list else 0,
                'avg_ctr': mean(ctr_list) if ctr_list else None,
                'avg_retention': mean(ret_list) if ret_list else None,
            }

    # Aggregate by boolean attributes
    bool_attributes = ['has_text', 'has_person', 'has_map']
    by_attr_result = {}

    for attr in bool_attributes:
        with_attr = []
        without_attr = []

        for v in videos:
            thumb = v.get('thumbnail', {})
            if v.get('views') is None:
                continue

            if thumb.get(attr, False):
                with_attr.append(v)
            else:
                without_attr.append(v)

        if len(with_attr) >= min_count and len(without_attr) >= min_count:
            # Calculate metrics for "with" group
            with_views = [v['views'] for v in with_attr]
            with_ctr = [v['ctr_percent'] for v in with_attr if v.get('ctr_percent') is not None]

            with_stats = {
                'count': len(with_attr),
                'avg_views': mean(with_views) if with_views else 0,
                'avg_ctr': mean(with_ctr) if with_ctr else None,
            }

            # Calculate metrics for "without" group
            without_views = [v['views'] for v in without_attr]
            without_ctr = [v['ctr_percent'] for v in without_attr if v.get('ctr_percent') is not None]

            without_stats = {
                'count': len(without_attr),
                'avg_views': mean(without_views) if without_views else 0,
                'avg_ctr': mean(without_ctr) if without_ctr else None,
            }

            # Calculate deltas
            def calc_delta(with_val, without_val):
                if with_val is None or without_val is None:
                    return None
                if without_val == 0:
                    return None
                return ((with_val - without_val) / without_val) * 100

            by_attr_result[attr] = {
                'with': with_stats,
                'without': without_stats,
                'delta_views': calc_delta(with_stats['avg_views'], without_stats['avg_views']),
                'delta_ctr': calc_delta(with_stats['avg_ctr'], without_stats['avg_ctr']),
            }

    return {
        'by_type': by_type_result,
        'by_attribute': by_attr_result,
    }


def enrich_video_data(videos: list[dict]) -> list[dict]:
    """
    Add tags, title structure, thumbnail metadata, and computed fields to video data.

    For each video:
    1. Calls auto_tag_video(title) to get topic tags
    2. Calls extract_title_structure(title) to get title attributes
    3. Finds project folder and extracts thumbnail metadata
    4. Computes 'days_since_publish' if analyzed_date available

    Args:
        videos: List of video data dicts from collect_video_data()

    Returns:
        list[dict] with enriched data (same dicts, modified in place)
    """
    for video in videos:
        # Add tags based on title
        title = video.get('title') or ''
        video['tags'] = auto_tag_video(title)

        # Add title structure analysis
        video['title_structure'] = extract_title_structure(title)

        # Find project folder and extract thumbnail metadata
        project_folder = find_project_folder_for_video(title)
        video['project_folder'] = project_folder
        video['thumbnail'] = extract_thumbnail_metadata(project_folder)

        # Compute days_since_publish if we have analyzed_date
        analyzed_date = video.get('analyzed_date')
        if analyzed_date:
            try:
                # Parse ISO format date
                if 'T' in analyzed_date:
                    parsed = datetime.fromisoformat(analyzed_date.replace('Z', '+00:00'))
                else:
                    parsed = datetime.strptime(analyzed_date[:10], '%Y-%m-%d')
                    parsed = parsed.replace(tzinfo=timezone.utc)

                now = datetime.now(timezone.utc)
                video['days_since_analysis'] = (now - parsed).days
            except (ValueError, TypeError):
                video['days_since_analysis'] = None
        else:
            video['days_since_analysis'] = None

    return videos


def get_youtube_metadata(video_title: str) -> str | None:
    """
    Try to find YOUTUBE-METADATA.md for a video based on title matching.

    Search strategy:
    1. Extract significant words from title (>3 chars)
    2. Search video-projects/*/* for folders containing those words
    3. Look for YOUTUBE-METADATA.md in matched folder
    4. Return file path if found, None otherwise

    Args:
        video_title: Video title to match

    Returns:
        Path to YOUTUBE-METADATA.md if found, None otherwise
    """
    if not video_title:
        return None

    # Extract significant words (>3 chars) from title
    words = re.sub(r'[^a-z0-9]+', ' ', video_title.lower()).split()
    significant_words = [w for w in words if len(w) > 3]

    if not significant_words:
        return None

    # Search project folders
    search_paths = [
        PROJECT_ROOT / 'video-projects' / '_IN_PRODUCTION' / '*',
        PROJECT_ROOT / 'video-projects' / '_READY_TO_FILM' / '*',
        PROJECT_ROOT / 'video-projects' / '_ARCHIVED' / '*',
    ]

    for pattern in search_paths:
        for folder in glob_module.glob(str(pattern)):
            if not Path(folder).is_dir():
                continue

            folder_name = Path(folder).name.lower()

            # Check if any significant word from title appears in folder name
            if any(word in folder_name for word in significant_words):
                metadata_path = Path(folder) / 'YOUTUBE-METADATA.md'
                if metadata_path.exists():
                    return str(metadata_path)

    return None


def aggregate_by_topic(videos: list[dict], min_count: int = 3) -> dict:
    """
    Aggregate metrics by topic tag with minimum sample size enforcement.

    Args:
        videos: List of video data dicts with 'tags' and metrics
        min_count: Minimum videos to include topic (default 3)

    Returns:
        dict with topic -> stats mapping (only topics with enough data)
        Each topic has:
            - count: number of videos
            - avg_views: mean views
            - avg_retention: mean retention (decimal)
            - avg_ctr: mean CTR (percentage)
            - videos: list of video titles
    """
    by_topic = defaultdict(list)

    for v in videos:
        for tag in v.get('tags', ['uncategorized']):
            by_topic[tag].append(v)

    result = {}

    for topic, vids in by_topic.items():
        # Filter to videos with valid views data
        valid_vids = [v for v in vids if v.get('views') is not None]

        if len(valid_vids) >= min_count:
            # Calculate averages, handling None values
            views_list = [v['views'] for v in valid_vids]
            retention_list = [v['avg_retention'] for v in valid_vids if v.get('avg_retention') is not None]
            ctr_list = [v['ctr_percent'] for v in valid_vids if v.get('ctr_percent') is not None]

            result[topic] = {
                'count': len(valid_vids),
                'avg_views': mean(views_list) if views_list else 0,
                'avg_retention': mean(retention_list) if retention_list else None,
                'avg_ctr': mean(ctr_list) if ctr_list else None,
                'videos': [v.get('title', v.get('video_id', 'Unknown')) for v in valid_vids],
            }

    return result


def identify_winners(videos: list[dict], channel_avg: dict = None) -> list[dict]:
    """
    Identify videos that beat channel average on BOTH CTR and retention.

    "Winners" = above average on both metrics (per 10-CONTEXT.md decision).

    Args:
        videos: List of video data dicts with ctr_percent and avg_retention
        channel_avg: Optional dict with 'avg_ctr' and 'avg_retention'.
                     If not provided, calculates from videos themselves.

    Returns:
        list[dict] of winning videos, sorted by views (highest first),
        each enriched with ctr_delta and retention_delta
    """
    # Calculate averages if not provided
    if channel_avg is None:
        valid_ctr = [v['ctr_percent'] for v in videos if v.get('ctr_percent') is not None]
        valid_ret = [v['avg_retention'] for v in videos if v.get('avg_retention') is not None]

        avg_ctr = sum(valid_ctr) / len(valid_ctr) if valid_ctr else 0
        avg_retention = sum(valid_ret) / len(valid_ret) if valid_ret else 0
    else:
        avg_ctr = channel_avg.get('avg_ctr', 0)
        avg_retention = channel_avg.get('avg_retention', 0)

    winners = []

    for v in videos:
        ctr = v.get('ctr_percent')
        retention = v.get('avg_retention')

        if ctr is not None and retention is not None:
            if ctr > avg_ctr and retention > avg_retention:
                winners.append({
                    **v,
                    'ctr_delta': ctr - avg_ctr,
                    'retention_delta': retention - avg_retention,
                })

    return sorted(winners, key=lambda x: x.get('views', 0) or 0, reverse=True)


def identify_anti_patterns(videos: list[dict], channel_avg: dict = None) -> list[dict]:
    """
    Identify videos that are BELOW average on BOTH CTR and retention.

    "Anti-patterns" = below average on both metrics.

    Args:
        videos: List of video data dicts with ctr_percent and avg_retention
        channel_avg: Optional dict with 'avg_ctr' and 'avg_retention'.

    Returns:
        list[dict] of underperforming videos, sorted by views (lowest first)
    """
    # Calculate averages if not provided
    if channel_avg is None:
        valid_ctr = [v['ctr_percent'] for v in videos if v.get('ctr_percent') is not None]
        valid_ret = [v['avg_retention'] for v in videos if v.get('avg_retention') is not None]

        avg_ctr = sum(valid_ctr) / len(valid_ctr) if valid_ctr else 0
        avg_retention = sum(valid_ret) / len(valid_ret) if valid_ret else 0
    else:
        avg_ctr = channel_avg.get('avg_ctr', 0)
        avg_retention = channel_avg.get('avg_retention', 0)

    anti_patterns = []

    for v in videos:
        ctr = v.get('ctr_percent')
        retention = v.get('avg_retention')

        if ctr is not None and retention is not None:
            if ctr < avg_ctr and retention < avg_retention:
                anti_patterns.append({
                    **v,
                    'ctr_delta': ctr - avg_ctr,
                    'retention_delta': retention - avg_retention,
                })

    return sorted(anti_patterns, key=lambda x: x.get('views', 0) or 0)


def aggregate_by_title_structure(videos: list[dict], min_count: int = 2) -> dict:
    """
    Aggregate performance by title structure attributes.

    For each boolean attribute (has_colon, has_question, etc.):
    1. Split videos into "with attribute" and "without attribute"
    2. Calculate avg_views, avg_ctr, avg_retention for each group
    3. Calculate percentage delta between groups

    Args:
        videos: List of video data dicts with 'title_structure' and metrics
        min_count: Minimum videos per group to include (default 2)

    Returns:
        dict with attribute -> comparison mapping:
        {
            'has_colon': {
                'with': {'count': 5, 'avg_views': 1500, 'avg_ctr': 4.2, 'avg_retention': 0.32},
                'without': {'count': 8, 'avg_views': 1200, 'avg_ctr': 3.8, 'avg_retention': 0.28},
                'delta_views': 25.0,  # percentage difference
                'delta_ctr': 10.5,
                'delta_retention': 14.3,
            },
            ...
        }
    """
    # Boolean attributes to analyze
    bool_attributes = ['has_colon', 'has_question', 'has_number', 'has_year', 'has_country']

    result = {}

    for attr in bool_attributes:
        with_attr = []
        without_attr = []

        for v in videos:
            title_struct = v.get('title_structure', {})
            views = v.get('views')

            # Skip videos without views data
            if views is None:
                continue

            if title_struct.get(attr, False):
                with_attr.append(v)
            else:
                without_attr.append(v)

        # Only include if both groups have enough data
        if len(with_attr) >= min_count and len(without_attr) >= min_count:
            # Calculate metrics for "with" group
            with_views = [v['views'] for v in with_attr]
            with_ctr = [v['ctr_percent'] for v in with_attr if v.get('ctr_percent') is not None]
            with_ret = [v['avg_retention'] for v in with_attr if v.get('avg_retention') is not None]

            with_stats = {
                'count': len(with_attr),
                'avg_views': mean(with_views) if with_views else 0,
                'avg_ctr': mean(with_ctr) if with_ctr else None,
                'avg_retention': mean(with_ret) if with_ret else None,
            }

            # Calculate metrics for "without" group
            without_views = [v['views'] for v in without_attr]
            without_ctr = [v['ctr_percent'] for v in without_attr if v.get('ctr_percent') is not None]
            without_ret = [v['avg_retention'] for v in without_attr if v.get('avg_retention') is not None]

            without_stats = {
                'count': len(without_attr),
                'avg_views': mean(without_views) if without_views else 0,
                'avg_ctr': mean(without_ctr) if without_ctr else None,
                'avg_retention': mean(without_ret) if without_ret else None,
            }

            # Calculate deltas (percentage difference)
            def calc_delta(with_val, without_val):
                if with_val is None or without_val is None:
                    return None
                if without_val == 0:
                    return None
                return ((with_val - without_val) / without_val) * 100

            result[attr] = {
                'with': with_stats,
                'without': without_stats,
                'delta_views': calc_delta(with_stats['avg_views'], without_stats['avg_views']),
                'delta_ctr': calc_delta(with_stats['avg_ctr'], without_stats['avg_ctr']),
                'delta_retention': calc_delta(
                    with_stats['avg_retention'] * 100 if with_stats['avg_retention'] else None,
                    without_stats['avg_retention'] * 100 if without_stats['avg_retention'] else None
                ),
            }

    return result


def aggregate_by_pattern(videos: list[dict], min_count: int = 2) -> dict:
    """
    Aggregate performance by detected title pattern type.

    Groups videos by their 'pattern' field from title_structure.

    Args:
        videos: List of video data dicts with 'title_structure' and metrics
        min_count: Minimum videos per pattern to include (default 2)

    Returns:
        dict with pattern -> stats mapping:
        {
            '[Topic]: [Subtitle]': {
                'count': 5,
                'avg_views': 1500,
                'avg_ctr': 4.5,
                'avg_retention': 0.32,
                'videos': ['Video Title 1', 'Video Title 2', ...],
            },
            ...
        }
    """
    by_pattern = defaultdict(list)

    for v in videos:
        title_struct = v.get('title_structure', {})
        pattern = title_struct.get('pattern', 'other')

        # Skip videos without views data
        if v.get('views') is None:
            continue

        by_pattern[pattern].append(v)

    result = {}

    for pattern, vids in by_pattern.items():
        if len(vids) >= min_count:
            views_list = [v['views'] for v in vids]
            ctr_list = [v['ctr_percent'] for v in vids if v.get('ctr_percent') is not None]
            ret_list = [v['avg_retention'] for v in vids if v.get('avg_retention') is not None]

            result[pattern] = {
                'count': len(vids),
                'avg_views': mean(views_list) if views_list else 0,
                'avg_ctr': mean(ctr_list) if ctr_list else None,
                'avg_retention': mean(ret_list) if ret_list else None,
                'videos': [v.get('title', v.get('video_id', 'Unknown')) for v in vids],
            }

    return result


def generate_insights(topic_stats: dict, winners: list[dict], anti_patterns: list[dict], total_videos: int) -> list[str]:
    """
    Generate actionable insights from topic statistics.

    Insight types:
    1. Best performing topic comparison
    2. Topic retention comparison
    3. Winners analysis
    4. Sample size warnings

    Args:
        topic_stats: dict from aggregate_by_topic()
        winners: list from identify_winners()
        anti_patterns: list from identify_anti_patterns()
        total_videos: total number of videos analyzed

    Returns:
        list[str] of insight statements
    """
    insights = []

    if not topic_stats:
        insights.append(f"Insufficient data for topic patterns - need 3+ videos per topic (currently {total_videos} total videos)")
        return insights

    # Find best performing topic by views
    topics_by_views = sorted(topic_stats.items(), key=lambda x: x[1]['avg_views'], reverse=True)

    if topics_by_views:
        best_topic, best_stats = topics_by_views[0]
        insights.append(
            f"**{best_topic.capitalize()}** topics average {best_stats['avg_views']:,.0f} views "
            f"({best_stats['count']} videos analyzed)"
        )

        # Compare to second-best if available
        if len(topics_by_views) > 1:
            second_topic, second_stats = topics_by_views[1]
            if second_stats['avg_views'] > 0:
                ratio = best_stats['avg_views'] / second_stats['avg_views']
                if ratio > 1.5:
                    insights.append(
                        f"{best_topic.capitalize()} videos get {ratio:.1f}x more views than {second_topic}"
                    )

    # Retention comparison by topic
    topics_with_retention = [
        (t, s) for t, s in topic_stats.items()
        if s.get('avg_retention') is not None
    ]

    if len(topics_with_retention) >= 2:
        topics_by_retention = sorted(topics_with_retention, key=lambda x: x[1]['avg_retention'], reverse=True)
        best_ret_topic, best_ret_stats = topics_by_retention[0]
        worst_ret_topic, worst_ret_stats = topics_by_retention[-1]

        diff = (best_ret_stats['avg_retention'] - worst_ret_stats['avg_retention']) * 100
        if diff > 5:
            insights.append(
                f"{best_ret_topic.capitalize()} videos have {diff:.1f}% higher retention than {worst_ret_topic}"
            )

    # Winners analysis
    if winners:
        insights.append(f"{len(winners)} video(s) beat channel average on BOTH CTR AND retention")
    else:
        insights.append("No videos currently beat channel average on both CTR and retention")

    # Anti-patterns analysis
    if anti_patterns:
        insights.append(f"{len(anti_patterns)} video(s) underperform on both CTR and retention - review for lessons")

    # Sample size warnings
    small_topics = [t for t, s in topic_stats.items() if s['count'] < 5]
    if small_topics:
        insights.append(
            f"Sample size warning: {', '.join(small_topics)} have fewer than 5 videos - patterns may shift"
        )

    return insights


def generate_recommendations(topic_stats: dict, winners: list[dict], anti_patterns: list[dict]) -> list[str]:
    """
    Generate actionable recommendations from pattern analysis.

    Args:
        topic_stats: dict from aggregate_by_topic()
        winners: list from identify_winners()
        anti_patterns: list from identify_anti_patterns()

    Returns:
        list[str] of recommended actions
    """
    recommendations = []

    if not topic_stats:
        recommendations.append("Run /analyze on more videos to build pattern data (need 3+ per topic)")
        return recommendations

    # Find best performing topic
    topics_by_views = sorted(topic_stats.items(), key=lambda x: x[1]['avg_views'], reverse=True)

    if topics_by_views:
        best_topic, _ = topics_by_views[0]
        recommendations.append(f"Consider prioritizing {best_topic} topics - highest view average")

    # Winners recommendation
    if winners:
        winner_tags = set()
        for w in winners:
            winner_tags.update(w.get('tags', []))

        if winner_tags:
            recommendations.append(f"Study winning patterns in: {', '.join(winner_tags)} videos")

    # Anti-pattern recommendation
    if anti_patterns:
        recommendations.append("Review underperforming videos for common mistakes to avoid")

    # Data collection recommendation
    if len(topic_stats) < 3:
        recommendations.append("Analyze more videos to enable cross-topic comparison")

    return recommendations


def generate_topic_report() -> str:
    """
    Generate complete TOPIC-ANALYSIS.md report with insights-first format.

    Collects video data, enriches with tags, aggregates by topic,
    and generates a Markdown report saved to channel-data/patterns/.

    Returns:
        str: Path to saved report file
    """
    # Collect and enrich data
    videos = collect_video_data()
    videos = enrich_video_data(videos)

    # Generate statistics
    topic_stats = aggregate_by_topic(videos)
    winners = identify_winners(videos)
    anti_patterns = identify_anti_patterns(videos)

    # Generate insights and recommendations
    insights = generate_insights(topic_stats, winners, anti_patterns, len(videos))
    recommendations = generate_recommendations(topic_stats, winners, anti_patterns)

    # Build report
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')

    lines = [
        "# Topic Performance Analysis",
        "",
        f"**Generated:** {timestamp}",
        f"**Videos analyzed:** {len(videos)}",
        "",
        "## Key Insights",
        "",
    ]

    # Add insights
    if insights:
        for insight in insights:
            lines.append(f"- {insight}")
    else:
        lines.append("- Insufficient data for insights - analyze more videos")

    lines.extend([
        "",
        "## Recommended Next Actions",
        "",
    ])

    # Add recommendations
    if recommendations:
        for rec in recommendations:
            lines.append(f"- [ ] {rec}")
    else:
        lines.append("- [ ] Run /analyze on published videos to build pattern data")

    lines.extend([
        "",
        "## Performance by Topic Type",
        "",
    ])

    if topic_stats:
        lines.append(f"*Based on {len(videos)} videos with 3+ videos per category*")
        lines.append("")
        lines.append("| Topic | Videos | Avg Views | Avg CTR | Avg Retention |")
        lines.append("|-------|--------|-----------|---------|---------------|")

        # Sort by views for display
        for topic, stats in sorted(topic_stats.items(), key=lambda x: x[1]['avg_views'], reverse=True):
            ctr_str = f"{stats['avg_ctr']:.1f}%" if stats['avg_ctr'] is not None else "N/A"
            ret_str = f"{stats['avg_retention']*100:.1f}%" if stats['avg_retention'] is not None else "N/A"

            lines.append(
                f"| {topic} | {stats['count']} | {stats['avg_views']:,.0f} | {ctr_str} | {ret_str} |"
            )
    else:
        lines.append("*No topics have 3+ videos yet - need more data*")

    lines.extend([
        "",
        "## Winners (Above Average on Both CTR AND Retention)",
        "",
    ])

    if winners:
        lines.append("| Title | Views | CTR | Retention |")
        lines.append("|-------|-------|-----|-----------|")

        for w in winners[:10]:
            title = w.get('title', w.get('video_id', 'Unknown'))[:50]
            views = w.get('views', 0) or 0
            ctr = w.get('ctr_percent', 0) or 0
            retention = (w.get('avg_retention', 0) or 0) * 100

            lines.append(f"| {title} | {views:,} | {ctr:.1f}% | {retention:.1f}% |")

        if len(winners) > 10:
            lines.append(f"| *...and {len(winners) - 10} more* | | | |")
    else:
        lines.append("*No videos currently beat average on both metrics*")

    lines.extend([
        "",
        "## Anti-Patterns (Below Average on Both)",
        "",
    ])

    if anti_patterns:
        lines.append("| Title | Views | CTR | Retention |")
        lines.append("|-------|-------|-----|-----------|")

        for ap in anti_patterns[:10]:
            title = ap.get('title', ap.get('video_id', 'Unknown'))[:50]
            views = ap.get('views', 0) or 0
            ctr = ap.get('ctr_percent', 0) or 0
            retention = (ap.get('avg_retention', 0) or 0) * 100

            lines.append(f"| {title} | {views:,} | {ctr:.1f}% | {retention:.1f}% |")

        if len(anti_patterns) > 10:
            lines.append(f"| *...and {len(anti_patterns) - 10} more* | | | |")
    else:
        lines.append("*No videos are below average on both metrics*")

    lines.extend([
        "",
        "## Videos by Topic",
        "",
    ])

    if topic_stats:
        for topic, stats in sorted(topic_stats.items()):
            lines.append(f"### {topic.capitalize()} ({stats['count']} videos)")
            lines.append("")
            for video_title in stats['videos']:
                lines.append(f"- {video_title}")
            lines.append("")
    else:
        lines.append("*No topics have enough videos for grouping*")
        lines.append("")

    lines.extend([
        "---",
        "*Sample sizes below 3 videos are excluded from analysis*",
        ""
    ])

    # Save report
    output_dir = PROJECT_ROOT / 'channel-data' / 'patterns'
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / 'TOPIC-ANALYSIS.md'
    report_content = '\n'.join(lines)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_content)

    return str(output_path)


if __name__ == '__main__':
    # CLI interface
    if len(sys.argv) == 1:
        # No args: show collected video data
        print("Collecting video data from POST-PUBLISH-ANALYSIS files...")
        print()

        videos = collect_video_data()

        if not videos:
            print("No POST-PUBLISH-ANALYSIS files found.")
            print()
            print("To generate analysis files, run:")
            print("  python analyze.py VIDEO_ID --save")
            print()
            print("Search locations:")
            print("  - channel-data/analyses/POST-PUBLISH-ANALYSIS-*.md")
            print("  - video-projects/_IN_PRODUCTION/*/POST-PUBLISH-ANALYSIS.md")
            print("  - video-projects/_READY_TO_FILM/*/POST-PUBLISH-ANALYSIS.md")
            print("  - video-projects/_ARCHIVED/*/POST-PUBLISH-ANALYSIS.md")
        else:
            print(f"Found {len(videos)} analyzed videos:")
            print()
            for v in videos:
                title = v.get('title', v.get('video_id', 'Unknown'))
                views = v.get('views', 'N/A')
                views_str = f"{views:,}" if isinstance(views, int) else views
                print(f"  - {title}: {views_str} views")

            print()
            print("Run with --tags to see topic classifications")
            print("Run with --topic-report to generate TOPIC-ANALYSIS.md")

    elif sys.argv[1] == '--tags':
        # Show videos with auto-tags
        print("Collecting and tagging video data...")
        print()

        videos = collect_video_data()
        videos = enrich_video_data(videos)

        if not videos:
            print("No POST-PUBLISH-ANALYSIS files found.")
        else:
            print(f"Found {len(videos)} videos with tags:")
            print()
            for v in videos:
                title = v.get('title', v.get('video_id', 'Unknown'))
                tags = ', '.join(v.get('tags', ['uncategorized']))
                print(f"  - {title}")
                print(f"    Tags: {tags}")
                print()

    elif sys.argv[1] == '--topic-report':
        # Generate TOPIC-ANALYSIS.md
        print("Generating topic performance report...")
        print()

        output_path = generate_topic_report()

        # Also print report to stdout
        with open(output_path, 'r', encoding='utf-8') as f:
            print(f.read())

        print()
        print(f"Report saved to: {output_path}")

    elif sys.argv[1] in ('--help', '-h'):
        print("Usage: python patterns.py [OPTIONS]")
        print()
        print("Cross-video pattern analysis for YouTube channel performance.")
        print()
        print("Options:")
        print("  (no args)         Show collected video data from analysis files")
        print("  --tags            Show videos with auto-detected topic tags")
        print("  --topic-report    Generate TOPIC-ANALYSIS.md report")
        print("  --help, -h        Show this help message")
        print()
        print("Examples:")
        print("  python patterns.py              # List analyzed videos")
        print("  python patterns.py --tags       # Show videos with topic tags")
        print("  python patterns.py --topic-report   # Generate report")
        print()
        print("Data sources:")
        print("  POST-PUBLISH-ANALYSIS files are searched in:")
        print("  - channel-data/analyses/")
        print("  - video-projects/_IN_PRODUCTION/*/")
        print("  - video-projects/_READY_TO_FILM/*/")
        print("  - video-projects/_ARCHIVED/*/")

    else:
        print(f"Unknown option: {sys.argv[1]}")
        print("Run 'python patterns.py --help' for usage information")
        sys.exit(1)
