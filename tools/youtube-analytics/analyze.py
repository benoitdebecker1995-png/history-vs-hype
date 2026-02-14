"""
YouTube Post-Publish Analysis Orchestrator

Combines all data sources into a complete post-publish analysis with automated lessons.
This is the engine that powers the /analyze command.

Usage:
    CLI:
        python analyze.py VIDEO_ID
        python analyze.py VIDEO_ID --markdown
        python analyze.py VIDEO_ID --save
        python analyze.py VIDEO_ID --save --output ./custom/path.md
        python analyze.py https://youtu.be/VIDEO_ID
        python analyze.py VIDEO_ID --ctr 4.5

    Python:
        from analyze import run_analysis, generate_lessons, find_project_folder, save_analysis

        analysis = run_analysis('VIDEO_ID')
        print(analysis['lessons'])

        # Save to project folder or fallback
        result = save_analysis(analysis)
        print(f"Saved to: {result['saved_to']}")

Output:
    JSON (default) or Markdown format with complete video analysis including:
    - Performance metrics vs channel benchmarks
    - Retention curve with drop-off points
    - Categorized comments
    - Automated lessons and actionable insights

Dependencies:
    - video_report.py (Phase 8) - engagement, retention, CTR data
    - comments.py (Plan 01) - comment fetching and categorization
    - channel_averages.py (Plan 01) - benchmark calculations
"""

import sys
import json
import re
import os
import glob
from datetime import datetime, timezone
from urllib.parse import urlparse, parse_qs
from pathlib import Path

from video_report import generate_video_report
from comments import fetch_and_categorize_comments
from channel_averages import get_channel_averages, compare_to_channel
from metrics import get_video_metrics

# Try to import discovery diagnostics (may not be available)
try:
    sys.path.insert(0, str(Path(__file__).parent.parent / 'discovery'))
    from diagnostics import diagnose_discovery, format_diagnosis_markdown
    DISCOVERY_AVAILABLE = True
except ImportError:
    DISCOVERY_AVAILABLE = False

# Try to import variant tracking (may not be available)
try:
    from database import KeywordDB
    VARIANTS_AVAILABLE = True
except ImportError:
    VARIANTS_AVAILABLE = False

# Try to import CTR analysis (Phase 30)
try:
    from benchmarks import compare_variants_for_video, get_benchmarks_report
    BENCHMARKS_AVAILABLE = True
except ImportError:
    BENCHMARKS_AVAILABLE = False

# Try to import feedback storage (Phase 31)
try:
    from feedback_parser import parse_analysis_file
    from feedback_queries import get_insights_preamble
    FEEDBACK_AVAILABLE = True
except ImportError:
    FEEDBACK_AVAILABLE = False

# Try to import diagnostics (Phase 35)
try:
    from retention_mapper import map_retention_to_sections, format_mapped_drops_table
    from section_diagnostics import diagnose_all_drops, format_diagnostics_markdown
    sys.path.insert(0, str(Path(__file__).parent.parent / 'production'))
    from parser import ScriptParser
    DIAGNOSTICS_AVAILABLE = True
except ImportError:
    DIAGNOSTICS_AVAILABLE = False

# Try to import playbook synthesizer (Phase 36)
try:
    from playbook_synthesizer import synthesize_part9, write_part9_to_style_guide
    PLAYBOOK_AVAILABLE = True
except ImportError:
    PLAYBOOK_AVAILABLE = False


# Determine project root (2 levels up from tools/youtube-analytics/)
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent


def find_project_folder(video_id: str = None, video_title: str = None) -> str:
    """
    Find project folder matching video ID or title.

    Search strategy (in order):
    1. Search for video ID string in any .md file within video-projects/_IN_PRODUCTION/*/
    2. Search for video ID in video-projects/_READY_TO_FILM/*/
    3. Search for video ID in video-projects/_ARCHIVED/*/
    4. If video_title provided, match title words against folder names
    5. Return None if no match found

    Args:
        video_id: YouTube video ID (11 characters)
        video_title: Video title for fuzzy matching

    Returns:
        Absolute path to project folder, or None if not found
    """
    search_paths = [
        PROJECT_ROOT / 'video-projects' / '_IN_PRODUCTION' / '*',
        PROJECT_ROOT / 'video-projects' / '_READY_TO_FILM' / '*',
        PROJECT_ROOT / 'video-projects' / '_ARCHIVED' / '*'
    ]

    # Strategy 1: Search for video ID in files
    if video_id:
        for pattern in search_paths:
            for folder in glob.glob(str(pattern)):
                if not os.path.isdir(folder):
                    continue
                # Search all .md files in the folder
                for filepath in glob.glob(os.path.join(folder, '*.md')):
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if video_id in content:
                                return folder
                    except (IOError, UnicodeDecodeError):
                        continue

    # Strategy 2: Match title slug to folder name
    if video_title:
        # Extract significant words (>3 chars) from title
        slug_words = re.sub(r'[^a-z0-9]+', ' ', video_title.lower()).split()
        significant_words = [w for w in slug_words if len(w) > 3]

        if significant_words:
            for pattern in search_paths:
                for folder in glob.glob(str(pattern)):
                    if not os.path.isdir(folder):
                        continue
                    folder_name = os.path.basename(folder).lower()
                    # Check if any significant word from title appears in folder name
                    if any(word in folder_name for word in significant_words):
                        return folder

    return None


def save_analysis(analysis: dict, output_path: str = None) -> dict:
    """
    Save analysis to file.

    Behavior:
    1. If output_path provided, save there
    2. If not, try find_project_folder(video_id, title)
    3. If project folder found, save as `{folder}/POST-PUBLISH-ANALYSIS.md`
    4. If not found, save to `channel-data/analyses/POST-PUBLISH-ANALYSIS-{video_id}.md`
    5. Create directory if needed

    Args:
        analysis: Complete analysis dict from run_analysis()
        output_path: Optional explicit path. If None, auto-discover project folder.

    Returns:
        dict with:
            'saved_to': path where file was saved
            'project_folder_found': bool indicating if project folder was matched
    """
    video_id = analysis.get('video_id', 'unknown')
    title = analysis.get('title')
    fetched_at = analysis.get('fetched_at', datetime.now(timezone.utc).isoformat())

    project_folder_found = False

    if output_path:
        # Use explicit path
        save_path = Path(output_path)
    else:
        # Try to find project folder
        project_folder = find_project_folder(video_id=video_id, video_title=title)

        if project_folder:
            save_path = Path(project_folder) / 'POST-PUBLISH-ANALYSIS.md'
            project_folder_found = True
        else:
            # Fallback to central location
            fallback_dir = PROJECT_ROOT / 'channel-data' / 'analyses'
            fallback_dir.mkdir(parents=True, exist_ok=True)
            save_path = fallback_dir / f'POST-PUBLISH-ANALYSIS-{video_id}.md'

    # Ensure parent directory exists
    save_path.parent.mkdir(parents=True, exist_ok=True)

    # Format content with header
    display_title = title or video_id
    header_lines = [
        f"# Post-Publish Analysis: {display_title}",
        "",
        f"**Video ID:** {video_id}",
        f"**Analyzed:** {fetched_at}",
        f"**Saved to:** {save_path}",
        "",
        "---",
        ""
    ]

    # Get full markdown content (skip the first header since we have our own)
    full_markdown = format_analysis_markdown(analysis)
    # Remove the duplicate header section from format_analysis_markdown
    lines = full_markdown.split('\n')
    # Skip lines until we hit "## Quick Summary" (the first real section)
    content_start = 0
    for i, line in enumerate(lines):
        if line.startswith('## Quick Summary'):
            content_start = i
            break
    content = '\n'.join(lines[content_start:])

    # Combine header and content
    final_content = '\n'.join(header_lines) + content

    # Write to file
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

    # Auto-store feedback in database (Phase 31)
    feedback_stored = False
    if FEEDBACK_AVAILABLE:
        try:
            parsed = parse_analysis_file(str(save_path))
            if 'error' not in parsed:
                # Import KeywordDB for storage
                from database import KeywordDB
                db = KeywordDB()
                store_result = db.store_video_feedback(
                    parsed.get('video_id', video_id),
                    {
                        'biggest_drop_position': parsed.get('drop_points', [{}])[0].get('position_pct') if parsed.get('drop_points') else None,
                        'observations': parsed.get('observations', []),
                        'actionable': parsed.get('actionable', []),
                        'discovery': parsed.get('discovery')
                    }
                )
                db.close()
                if 'status' in store_result and store_result['status'] in ('inserted', 'updated'):
                    feedback_stored = True
        except Exception:
            pass  # Non-blocking: feedback storage failure should not affect save

    return {
        'saved_to': str(save_path),
        'project_folder_found': project_folder_found,
        'feedback_stored': feedback_stored
    }


def generate_section_diagnostics(video_id: str, script_path: str) -> dict:
    """
    Generate section-level retention diagnostics for a video.

    Maps retention drop points to specific script sections and generates
    actionable recommendations based on anti-pattern detection.

    Args:
        video_id: YouTube video ID
        script_path: Path to script markdown file

    Returns:
        dict with:
            'status': 'success' or 'error'
            'mapped_drops': [...] - List of mapped drop dicts (if success)
            'diagnostics': [...] - List of diagnosis dicts (if success)
            'summary_table': str - Formatted markdown table (if success)
            'error': str - Error message (if error)
    """
    if not DIAGNOSTICS_AVAILABLE:
        return {'error': 'Diagnostics modules not available (retention_mapper or section_diagnostics not imported)'}

    try:
        # Check script file exists
        script_file = Path(script_path)
        if not script_file.exists():
            return {'error': f'Script file not found: {script_path}'}

        # Get retention data
        from retention import get_retention_data, find_drop_off_points
        retention_data = get_retention_data(video_id)

        if 'error' in retention_data:
            return {'error': f'Could not fetch retention data: {retention_data["error"]}'}

        # Find drop-off points
        data_points = retention_data.get('data_points', [])
        drops = find_drop_off_points(data_points)

        if not drops:
            return {'error': 'No retention drops detected'}

        # Parse script
        parser = ScriptParser()
        sections = parser.parse_file(str(script_file))

        if not sections:
            return {'error': 'Could not parse script sections'}

        # Map drops to sections
        mapped_drops = map_retention_to_sections(drops, sections)

        if not mapped_drops:
            return {'error': 'Could not map drops to sections'}

        # Generate diagnostics
        diagnostics = diagnose_all_drops(mapped_drops, sections)

        # Format summary table
        summary_table = format_mapped_drops_table(mapped_drops)

        return {
            'status': 'success',
            'mapped_drops': mapped_drops,
            'diagnostics': diagnostics,
            'summary_table': summary_table
        }

    except Exception as e:
        return {'error': f'Section diagnostics failed: {str(e)}'}


def extract_video_id(url_or_id: str) -> str:
    """
    Extract YouTube video ID from URL or return as-is if already an ID.

    Supports:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://youtube.com/shorts/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    - Raw VIDEO_ID (11 characters)

    Args:
        url_or_id: YouTube URL or video ID

    Returns:
        11-character video ID

    Raises:
        ValueError: If video ID cannot be extracted
    """
    # Clean input
    url_or_id = url_or_id.strip()

    # If already looks like a video ID (11 alphanumeric + hyphens/underscores)
    if re.match(r'^[\w-]{11}$', url_or_id):
        return url_or_id

    # Parse URL
    parsed = urlparse(url_or_id)

    # youtu.be/VIDEO_ID
    if parsed.netloc in ('youtu.be', 'www.youtu.be'):
        video_id = parsed.path.lstrip('/')
        if len(video_id) >= 11:
            return video_id[:11]

    # youtube.com variants
    if 'youtube.com' in parsed.netloc or 'youtube.com' in url_or_id:
        # /watch?v=VIDEO_ID
        if parsed.path == '/watch' or '/watch' in url_or_id:
            query = parse_qs(parsed.query)
            if 'v' in query:
                return query['v'][0][:11]

        # /shorts/VIDEO_ID, /embed/VIDEO_ID, /v/VIDEO_ID
        for prefix in ('/shorts/', '/embed/', '/v/'):
            if prefix in parsed.path:
                remainder = parsed.path.split(prefix)[-1]
                if len(remainder) >= 11:
                    return remainder[:11]

    raise ValueError(f"Could not extract video ID from: {url_or_id}")


def run_analysis(video_id_or_url: str, manual_ctr: float = None) -> dict:
    """
    Run complete post-publish analysis for a video.

    Orchestrates data from video_report, comments, and channel_averages,
    then generates automated lessons based on the data.

    Args:
        video_id_or_url: YouTube video ID or URL
        manual_ctr: Optional manual CTR override (0-100)

    Returns:
        Complete analysis dict:
        {
            'video_id': '...',
            'title': '...',
            'fetched_at': 'ISO timestamp',
            'engagement': {...},
            'ctr': {...},
            'retention': {...},
            'benchmarks': {
                'channel_averages': {...},
                'comparison': {...}
            },
            'comments': {
                'total': N,
                'questions': [...],
                'objections': [...],
                'requests': [...]
            },
            'lessons': {
                'observations': [...],
                'actionable': [...]
            },
            'errors': [...]
        }
    """
    errors = []
    fetched_at = datetime.now(timezone.utc).isoformat()

    # Extract video ID from URL if needed
    try:
        video_id = extract_video_id(video_id_or_url)
    except ValueError as e:
        return {
            'video_id': video_id_or_url,
            'title': None,
            'fetched_at': fetched_at,
            'errors': [{'source': 'input', 'message': str(e)}]
        }

    # 1. Get video report (engagement, retention, CTR)
    video_report = generate_video_report(video_id)

    # Extract components from video report
    title = video_report.get('title')
    engagement = video_report.get('engagement')
    retention = video_report.get('retention')
    ctr = video_report.get('ctr')

    # Collect errors from video report
    if video_report.get('errors'):
        errors.extend(video_report['errors'])

    # 2. Handle manual CTR override
    if manual_ctr is not None:
        ctr = {
            'impressions': ctr.get('impressions') if ctr else None,
            'ctr_percent': manual_ctr,
            'available': True,
            'source': 'manual'
        }

    # 3. Fetch and categorize comments
    comments_result = fetch_and_categorize_comments(video_id)

    if 'error' in comments_result:
        errors.append({
            'source': 'comments',
            'message': comments_result['error']
        })
        comments = {
            'total': 0,
            'questions': [],
            'objections': [],
            'requests': [],
            'other': []
        }
    else:
        comments = {
            'total': comments_result.get('total_fetched', 0),
            'questions': comments_result.get('categories', {}).get('questions', []),
            'objections': comments_result.get('categories', {}).get('objections', []),
            'requests': comments_result.get('categories', {}).get('requests', []),
            'other': comments_result.get('categories', {}).get('other', [])
        }

    # 4. Get channel averages and comparison
    channel_avgs = get_channel_averages()

    if 'error' in channel_avgs:
        errors.append({
            'source': 'channel_averages',
            'message': channel_avgs['error']
        })
        benchmarks = {
            'channel_averages': None,
            'comparison': None
        }
    else:
        # Get video metrics for comparison
        video_metrics = get_video_metrics(video_id)

        if 'error' in video_metrics:
            comparison = None
        else:
            comparison = compare_to_channel(video_metrics, channel_avgs)
            if 'error' in comparison:
                errors.append({
                    'source': 'comparison',
                    'message': comparison['error']
                })
                comparison = None

        benchmarks = {
            'channel_averages': channel_avgs,
            'comparison': comparison
        }

    # 5. Generate lessons based on all data
    analysis_data = {
        'engagement': engagement,
        'retention': retention,
        'ctr': ctr,
        'benchmarks': benchmarks,
        'comments': comments
    }
    lessons = generate_lessons(analysis_data)

    # 6. Run discovery diagnostics if available
    discovery_diagnosis = None
    if DISCOVERY_AVAILABLE:
        try:
            discovery_diagnosis = diagnose_discovery(
                video_metrics=engagement if engagement else {},
                channel_averages=channel_avgs if channel_avgs and 'error' not in channel_avgs else {},
                ctr=ctr.get('ctr_percent') if ctr and ctr.get('available') else None
            )
        except Exception as e:
            errors.append({
                'source': 'discovery',
                'message': f'Discovery diagnostics failed: {str(e)}'
            })

    # 7. Fetch variant tracking data if available
    variant_data = None
    if VARIANTS_AVAILABLE:
        try:
            db = KeywordDB()
            summary = db.get_variant_summary(video_id)
            if summary['thumbnails'] > 0 or summary['titles'] > 0 or summary['snapshots'] > 0:
                variant_data = {
                    'summary': summary,
                    'thumbnails': db.get_thumbnail_variants(video_id),
                    'titles': db.get_title_variants(video_id),
                    'snapshots': db.get_ctr_snapshots(video_id)
                }
            db.close()
        except Exception as e:
            errors.append({
                'source': 'variants',
                'message': f'Variant tracking query failed: {str(e)}'
            })

    # 8. Run CTR analysis if available
    ctr_analysis = None
    if BENCHMARKS_AVAILABLE and variant_data:
        try:
            benchmarks_data = get_benchmarks_report()
            thumb_verdict = compare_variants_for_video(video_id, 'thumbnail', benchmarks_data.get('overall', {}))
            title_verdict = compare_variants_for_video(video_id, 'title', benchmarks_data.get('overall', {}))
            ctr_analysis = {
                'thumbnail_verdict': thumb_verdict,
                'title_verdict': title_verdict,
                'benchmarks': benchmarks_data
            }
        except Exception as e:
            errors.append({
                'source': 'ctr_analysis',
                'message': f'CTR analysis failed: {str(e)}'
            })

    return {
        'video_id': video_id,
        'title': title,
        'fetched_at': fetched_at,
        'engagement': engagement,
        'ctr': ctr,
        'retention': retention,
        'benchmarks': benchmarks,
        'comments': comments,
        'lessons': lessons,
        'discovery': discovery_diagnosis,
        'variants': variant_data,
        'ctr_analysis': ctr_analysis,
        'errors': errors
    }


def generate_lessons(analysis_data: dict) -> dict:
    """
    Generate automated lessons and actionable insights from analysis data.

    Applies pattern-based rules to generate observations and recommendations.

    Args:
        analysis_data: dict with engagement, retention, ctr, benchmarks, comments

    Returns:
        dict with:
            'observations': [...] - What the data shows
            'actionable': [...] - What to do next time
    """
    observations = []
    actionable = []

    engagement = analysis_data.get('engagement') or {}
    retention = analysis_data.get('retention') or {}
    ctr = analysis_data.get('ctr') or {}
    benchmarks = analysis_data.get('benchmarks') or {}
    comments = analysis_data.get('comments') or {}

    # --- Retention Observations ---
    avg_retention = retention.get('avg_retention')
    if avg_retention is not None:
        retention_percent = avg_retention * 100

        if retention_percent >= 35:
            observations.append(f"Strong retention ({retention_percent:.1f}%) - hook and pacing working well")
        elif retention_percent >= 25:
            observations.append(f"Average retention ({retention_percent:.1f}%) - room for improvement")
            actionable.append("Consider stronger opening hook in first 30 seconds")
        else:
            observations.append(f"Retention needs work ({retention_percent:.1f}%) - review first 30 seconds")
            actionable.append("Review and tighten intro - front-load the most compelling content")

    drop_offs = retention.get('drop_off_points', [])
    if drop_offs:
        # Find biggest drop
        biggest_drop = max(drop_offs, key=lambda d: d.get('drop', 0))
        drop_percent = biggest_drop.get('drop', 0) * 100
        drop_position = biggest_drop.get('position', 0) * 100
        drop_location = biggest_drop.get('timestamp_hint', 'unknown')

        if drop_percent > 10:
            observations.append(
                f"Major drop-off at {drop_position:.0f}% ({drop_location}) - {drop_percent:.1f}% viewers lost"
            )
            actionable.append(f"Review content at {drop_location} section - consider adding pattern interrupt")

        if len(drop_offs) > 5:
            observations.append(f"Multiple drop-off points ({len(drop_offs)}) - consider tightening overall pacing")
            actionable.append("Trim tangents and maintain narrative momentum throughout")

    # --- Engagement Observations ---
    views = engagement.get('views', 0) or 0
    subs_gained = engagement.get('subscribers_gained', 0) or 0
    likes = engagement.get('likes', 0) or 0
    comment_count = engagement.get('comments', 0) or 0

    if views > 0:
        # Subscriber conversion rate
        subs_per_100 = (subs_gained / views) * 100
        if subs_per_100 >= 1:
            observations.append(f"Strong subscriber conversion ({subs_per_100:.2f} per 100 views)")
        elif subs_per_100 < 0.3 and views > 1000:
            observations.append(f"Low subscriber conversion ({subs_per_100:.2f} per 100 views)")
            actionable.append("Consider adding stronger subscribe CTA at high-engagement moment")

        # Engagement rate
        engagement_rate = ((likes + comment_count) / views) * 100
        if engagement_rate >= 5:
            observations.append(f"Excellent engagement ({engagement_rate:.1f}%)")
        elif engagement_rate >= 2:
            observations.append(f"Good engagement ({engagement_rate:.1f}%)")
        elif engagement_rate < 1:
            observations.append(f"Low engagement ({engagement_rate:.1f}%)")
            actionable.append("Consider adding engagement prompts (questions, polls, discussion topics)")

    # --- Benchmark Observations ---
    comparison = benchmarks.get('comparison')
    if comparison and 'comparisons' in comparison:
        views_comp = comparison['comparisons'].get('views', {})
        delta = views_comp.get('delta_percent', 0)

        if delta > 50:
            observations.append(f"Outperforming channel average by {delta:.0f}%")
            actionable.append("This topic type works well - consider similar content")
        elif delta < -50:
            observations.append(f"Underperforming vs channel average by {abs(delta):.0f}%")
            actionable.append("Analyze what's different about this video vs better performers")

    # --- CTR Observations ---
    if ctr.get('available') and ctr.get('ctr_percent') is not None:
        ctr_val = ctr['ctr_percent']
        if ctr_val >= 6:
            observations.append(f"Excellent CTR ({ctr_val}%) - thumbnail/title working well")
        elif ctr_val >= 4:
            observations.append(f"Good CTR ({ctr_val}%)")
        elif ctr_val < 2:
            observations.append(f"Low CTR ({ctr_val}%) - consider thumbnail/title optimization")
            actionable.append("A/B test alternative thumbnails or titles")

    # --- Comment Observations ---
    question_count = len(comments.get('questions', []))
    objection_count = len(comments.get('objections', []))
    request_count = len(comments.get('requests', []))

    if question_count > 5:
        observations.append(f"{question_count} questions detected - audience seeking clarification")
        actionable.append("Address top questions in pinned comment or follow-up content")

    if objection_count > 3:
        observations.append(f"{objection_count} objections raised - review for accuracy")
        actionable.append("Review objections for potential corrections or clarifications")

    if request_count > 3:
        observations.append(f"{request_count} content requests - note for future topics")
        actionable.append("Log requested topics for future video pipeline")

    # Provide at least one observation even if data is sparse
    if not observations:
        observations.append("Insufficient data for automated insights - check individual metrics")

    return {
        'observations': observations,
        'actionable': actionable
    }


def ascii_retention_curve(data_points: list, width: int = 60, height: int = 10) -> str:
    """
    Generate ASCII retention curve visualization.

    Custom implementation without external dependencies.

    Args:
        data_points: List of {'position': float, 'retention': float} dicts
        width: Chart width in characters (default 60)
        height: Chart height in rows (default 10)

    Returns:
        ASCII art string representing retention curve
    """
    if not data_points:
        return "No retention data available for visualization"

    # Extract retention values
    values = [dp.get('retention', 0) for dp in data_points]

    if not values:
        return "No retention data available for visualization"

    # Sample values to fit width
    step = max(1, len(values) // width)
    sampled = values[::step][:width]

    if not sampled:
        return "Insufficient data points for visualization"

    # Build chart
    lines = []

    for row in range(height, -1, -1):
        threshold = row / height
        pct_label = int(threshold * 100)
        line = f"{pct_label:3d}% |"

        for val in sampled:
            if val >= threshold:
                line += "*"
            else:
                line += " "

        lines.append(line)

    # X-axis
    lines.append("     +" + "-" * len(sampled))
    lines.append("     0%       Video Progress       100%")

    return "\n".join(lines)


def format_analysis_markdown(analysis: dict) -> str:
    """
    Format complete analysis as human-readable Markdown.

    Includes:
    - Quick summary with benchmark comparisons
    - Performance table with channel average comparison
    - Retention section with ASCII curve
    - All drop-off points with timestamps
    - Full comment lists under each category
    - Lessons section

    Args:
        analysis: Complete analysis dict from run_analysis()

    Returns:
        Markdown-formatted string
    """
    lines = []

    # --- Header ---
    title = analysis.get('title') or analysis.get('video_id')
    lines.append(f"# Post-Publish Analysis: {title}")
    lines.append("")
    lines.append(f"**Video ID:** {analysis.get('video_id')}")
    lines.append(f"**Analysis generated:** {analysis.get('fetched_at', 'Unknown')}")
    lines.append("")

    # --- Quick Summary ---
    lines.append("## Quick Summary")
    lines.append("")

    benchmarks = analysis.get('benchmarks', {})
    comparison = benchmarks.get('comparison', {})

    if comparison and 'summary' in comparison:
        above = comparison['summary'].get('above_average', [])
        below = comparison['summary'].get('below_average', [])

        if above:
            lines.append(f"**Above average:** {', '.join(above)}")
        if below:
            lines.append(f"**Below average:** {', '.join(below)}")
        if not above and not below:
            lines.append("**Performance:** At channel average")
    else:
        lines.append("*Channel benchmark comparison unavailable*")

    lines.append("")

    # --- Performance vs Benchmarks Table ---
    lines.append("## Performance vs Benchmarks")
    lines.append("")

    engagement = analysis.get('engagement')
    channel_avgs = benchmarks.get('channel_averages')

    if engagement and channel_avgs and 'error' not in channel_avgs:
        lines.append("| Metric | This Video | Channel Avg | vs Avg |")
        lines.append("|--------|-----------|-------------|--------|")

        comparisons = comparison.get('comparisons', {}) if comparison else {}

        # Views
        views = engagement.get('views', 0)
        avg_views = channel_avgs.get('avg_views', 0)
        views_comp = comparisons.get('views', {})
        delta = views_comp.get('delta_percent', 0)
        delta_str = f"+{delta:.0f}%" if delta > 0 else f"{delta:.0f}%"
        lines.append(f"| Views | {views:,} | {avg_views:,.0f} | {delta_str} |")

        # Watch time
        watch_time = engagement.get('watch_time_minutes', 0)
        avg_watch = channel_avgs.get('avg_watch_time_minutes', 0)
        wt_comp = comparisons.get('watch_time_minutes', {})
        wt_delta = wt_comp.get('delta_percent', 0)
        wt_delta_str = f"+{wt_delta:.0f}%" if wt_delta > 0 else f"{wt_delta:.0f}%"
        lines.append(f"| Watch Time (min) | {watch_time:,.0f} | {avg_watch:,.0f} | {wt_delta_str} |")

        # Likes
        likes = engagement.get('likes', 0)
        avg_likes = channel_avgs.get('avg_likes', 0)
        likes_comp = comparisons.get('likes', {})
        likes_delta = likes_comp.get('delta_percent', 0)
        likes_delta_str = f"+{likes_delta:.0f}%" if likes_delta > 0 else f"{likes_delta:.0f}%"
        lines.append(f"| Likes | {likes:,} | {avg_likes:,.0f} | {likes_delta_str} |")

        # Comments
        comments_count = engagement.get('comments', 0)
        avg_comments = channel_avgs.get('avg_comments', 0)
        comments_comp = comparisons.get('comments', {})
        comments_delta = comments_comp.get('delta_percent', 0)
        comments_delta_str = f"+{comments_delta:.0f}%" if comments_delta > 0 else f"{comments_delta:.0f}%"
        lines.append(f"| Comments | {comments_count:,} | {avg_comments:,.0f} | {comments_delta_str} |")

        # Subscribers gained
        subs = engagement.get('subscribers_gained', 0)
        avg_subs = channel_avgs.get('avg_subscribers_gained', 0)
        subs_comp = comparisons.get('subscribers_gained', {})
        subs_delta = subs_comp.get('delta_percent', 0)
        subs_delta_str = f"+{subs_delta:.0f}%" if subs_delta > 0 else f"{subs_delta:.0f}%"
        lines.append(f"| Subscribers | +{subs} | +{avg_subs:.0f} | {subs_delta_str} |")

        sample_size = channel_avgs.get('sample_size', 0)
        lines.append("")
        lines.append(f"*Channel averages based on last {sample_size} videos*")
    elif engagement:
        # No benchmark, just show raw metrics
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        lines.append(f"| Views | {engagement.get('views', 0):,} |")
        lines.append(f"| Watch Time | {engagement.get('watch_time_minutes', 0):,.0f} min |")
        lines.append(f"| Likes | {engagement.get('likes', 0):,} |")
        lines.append(f"| Comments | {engagement.get('comments', 0):,} |")
        lines.append(f"| Subscribers | +{engagement.get('subscribers_gained', 0)} |")
        lines.append("")
        lines.append("*Channel benchmark unavailable - need 3+ videos for comparison*")
    else:
        lines.append("*Performance data unavailable*")

    lines.append("")

    # --- CTR Section ---
    lines.append("## Click-Through Rate")
    lines.append("")

    ctr = analysis.get('ctr')
    if ctr:
        if ctr.get('available') and ctr.get('ctr_percent') is not None:
            source = ctr.get('source', 'api')
            source_note = " (manual entry)" if source == 'manual' else ""
            lines.append(f"**CTR:** {ctr['ctr_percent']}%{source_note}")
            if ctr.get('impressions'):
                lines.append(f"**Impressions:** {ctr['impressions']:,}")
        else:
            lines.append("**CTR:** Not available via API")
            lines.append("")
            lines.append("*Check YouTube Studio > Analytics > Reach tab for CTR data*")
    else:
        lines.append("*CTR data unavailable*")

    lines.append("")

    # --- Retention Section ---
    lines.append("## Retention Analysis")
    lines.append("")

    retention = analysis.get('retention')
    if retention:
        avg_ret = retention.get('avg_retention')
        final_ret = retention.get('final_retention')

        if avg_ret is not None:
            lines.append(f"**Average retention:** {avg_ret * 100:.1f}%")
        if final_ret is not None:
            lines.append(f"**Final retention:** {final_ret * 100:.1f}%")

        lines.append("")

        # ASCII curve - we need to fetch full data points for this
        # The video_report only includes summary, not full curve
        # For now, note that full curve requires retention.py directly
        lines.append("### Retention Curve")
        lines.append("")
        lines.append("*Run `python retention.py VIDEO_ID` for full curve visualization*")
        lines.append("")

        # Drop-offs
        drop_offs = retention.get('drop_off_points', [])
        if drop_offs:
            lines.append("### Drop-off Points")
            lines.append("")
            lines.append("*Sorted by impact (biggest drops first)*")
            lines.append("")
            lines.append("| Position | Viewers Lost | Location |")
            lines.append("|----------|--------------|----------|")

            sorted_drops = sorted(drop_offs, key=lambda d: d.get('drop', 0), reverse=True)

            for drop in sorted_drops[:10]:
                pos = drop.get('position', 0) * 100
                lost = drop.get('drop', 0) * 100
                hint = drop.get('timestamp_hint', 'unknown')
                lines.append(f"| {pos:.0f}% | {lost:.1f}% dropped | {hint} |")

            if len(drop_offs) > 10:
                lines.append(f"| ... | ({len(drop_offs) - 10} more) | ... |")
        else:
            lines.append("*No significant drop-offs detected*")
    else:
        lines.append("*Retention data unavailable*")

    lines.append("")

    # --- Comments Section ---
    lines.append("## Comments Analysis")
    lines.append("")

    comments = analysis.get('comments', {})
    total = comments.get('total', 0)
    lines.append(f"**Total fetched:** {total}")
    lines.append("")

    # Questions
    questions = comments.get('questions', [])
    lines.append(f"### Questions ({len(questions)})")
    lines.append("")
    if questions:
        for q in questions[:10]:
            author = q.get('author', 'Unknown')
            text = q.get('text', '')[:200]
            likes = q.get('likes', 0)
            lines.append(f"- **{author}** ({likes} likes): {text}")
        if len(questions) > 10:
            lines.append(f"- *...and {len(questions) - 10} more questions*")
    else:
        lines.append("*No questions detected*")
    lines.append("")

    # Objections
    objections = comments.get('objections', [])
    lines.append(f"### Objections ({len(objections)})")
    lines.append("")
    if objections:
        for obj in objections[:10]:
            author = obj.get('author', 'Unknown')
            text = obj.get('text', '')[:200]
            likes = obj.get('likes', 0)
            lines.append(f"- **{author}** ({likes} likes): {text}")
        if len(objections) > 10:
            lines.append(f"- *...and {len(objections) - 10} more objections*")
    else:
        lines.append("*No objections detected*")
    lines.append("")

    # Requests
    requests = comments.get('requests', [])
    lines.append(f"### Content Requests ({len(requests)})")
    lines.append("")
    if requests:
        for req in requests[:10]:
            author = req.get('author', 'Unknown')
            text = req.get('text', '')[:200]
            likes = req.get('likes', 0)
            lines.append(f"- **{author}** ({likes} likes): {text}")
        if len(requests) > 10:
            lines.append(f"- *...and {len(requests) - 10} more requests*")
    else:
        lines.append("*No content requests detected*")
    lines.append("")

    # --- Lessons Section ---
    lines.append("## Lessons")
    lines.append("")

    lessons = analysis.get('lessons', {})
    observations = lessons.get('observations', [])
    actionable_items = lessons.get('actionable', [])

    lines.append("### Observations")
    lines.append("")
    if observations:
        for obs in observations:
            lines.append(f"- {obs}")
    else:
        lines.append("*No automated observations generated*")
    lines.append("")

    lines.append("### Actionable Items")
    lines.append("")
    if actionable_items:
        for item in actionable_items:
            lines.append(f"- [ ] {item}")
    else:
        lines.append("*No action items identified*")
    lines.append("")

    # --- Discovery Diagnostics Section ---
    if analysis.get('discovery'):
        discovery = analysis['discovery']
        diagnosis = discovery.get('diagnosis', {})

        lines.append("## Discovery Diagnostics")
        lines.append("")

        # Summary
        primary_issue = diagnosis.get('primary_issue', 'UNKNOWN')
        severity = diagnosis.get('severity', 'UNKNOWN')
        summary = diagnosis.get('summary', 'No diagnosis available')

        lines.append(f"**Diagnosis:** {summary}")
        lines.append(f"**Primary Issue:** {primary_issue} (Severity: {severity})")
        lines.append("")

        # Issues detail
        issues = discovery.get('issues', [])
        if issues:
            lines.append("### Issues Detected")
            lines.append("")
            for issue in issues:
                issue_type = issue.get('type', 'UNKNOWN')
                issue_severity = issue.get('severity', 'UNKNOWN')
                description = issue.get('description', '')
                lines.append(f"- **{issue_type}** ({issue_severity}): {description}")
            lines.append("")

        # Fixes
        fixes = discovery.get('fixes', [])
        if fixes:
            lines.append("### Recommended Fixes")
            lines.append("")
            for fix in fixes:
                priority = fix.get('priority', 'NORMAL')
                action = fix.get('action', '')
                rationale = fix.get('rationale', '')
                lines.append(f"- [{priority}] {action}")
                lines.append(f"  - *Why:* {rationale}")
            lines.append("")

        # Learnings
        learnings = discovery.get('learnings', [])
        if learnings:
            lines.append("### Learnings for Future Videos")
            lines.append("")
            for learn in learnings:
                insight = learn.get('insight', '')
                apply_to = learn.get('apply_to', '')
                lines.append(f"- {insight}")
                lines.append(f"  - *Apply to:* {apply_to}")
            lines.append("")

    # --- Variant Tracking Section ---
    variant_data = analysis.get('variants')
    if variant_data:
        lines.append("## Variant Tracking")
        lines.append("")

        summary = variant_data.get('summary', {})
        lines.append(f"**Thumbnails:** {summary.get('thumbnails', 0)} registered")
        lines.append(f"**Titles:** {summary.get('titles', 0)} registered")
        lines.append(f"**CTR Snapshots:** {summary.get('snapshots', 0)} recorded")
        lines.append("")

        # Thumbnail variants table
        thumbnails = variant_data.get('thumbnails', [])
        if thumbnails:
            lines.append("### Thumbnail Variants")
            lines.append("")
            lines.append("| Variant | Tags | Hash | Registered |")
            lines.append("|---------|------|------|------------|")
            for thumb in thumbnails:
                letter = thumb.get('variant_letter', '?')
                tags = thumb.get('visual_pattern_tags', [])
                tags_str = ', '.join(tags) if isinstance(tags, list) else str(tags)
                hash_val = thumb.get('perceptual_hash', 'N/A')
                hash_short = hash_val[:8] + '...' if hash_val and len(hash_val) > 8 else (hash_val or 'N/A')
                created = thumb.get('created_at', 'Unknown')
                lines.append(f"| {letter} | {tags_str} | {hash_short} | {created} |")
            lines.append("")

        # Title variants table
        titles = variant_data.get('titles', [])
        if titles:
            lines.append("### Title Variants")
            lines.append("")
            lines.append("| Variant | Title | Chars | Tags |")
            lines.append("|---------|-------|-------|------|")
            for title_var in titles:
                letter = title_var.get('variant_letter', '?')
                title_text = title_var.get('title_text', '')
                title_display = title_text[:50] + '...' if len(title_text) > 50 else title_text
                chars = title_var.get('character_count', 0)
                tags = title_var.get('formula_tags', [])
                tags_str = ', '.join(tags) if isinstance(tags, list) else str(tags)
                lines.append(f"| {letter} | {title_display} | {chars} | {tags_str} |")
            lines.append("")

        # CTR snapshots table
        snapshots = variant_data.get('snapshots', [])
        if snapshots:
            lines.append("### CTR History")
            lines.append("")
            lines.append("| Date | CTR | Impressions | Views |")
            lines.append("|------|-----|-------------|-------|")
            for snap in snapshots:
                snap_date = snap.get('snapshot_date', 'Unknown')
                ctr_val = snap.get('ctr_percent', 0)
                impressions = snap.get('impression_count', 0)
                views = snap.get('view_count', 0)
                lines.append(f"| {snap_date} | {ctr_val}% | {impressions:,} | {views:,} |")
            lines.append("")

            # CTR trend (if multiple snapshots)
            if len(snapshots) >= 2:
                first_ctr = snapshots[0].get('ctr_percent', 0)
                last_ctr = snapshots[-1].get('ctr_percent', 0)
                delta = last_ctr - first_ctr
                direction = "up" if delta > 0 else "down" if delta < 0 else "flat"
                lines.append(f"**CTR Trend:** {direction} ({first_ctr}% -> {last_ctr}%, delta: {delta:+.1f}%)")
                lines.append("")

        if not thumbnails and not titles and not snapshots:
            lines.append("*No variant details available*")
            lines.append("")

    # --- CTR Analysis Section (Phase 30) ---
    ctr_analysis = analysis.get('ctr_analysis')
    if ctr_analysis:
        lines.append("### CTR Analysis")
        lines.append("")

        # Status badges for verdicts
        status_badges = {
            'winner_found': 'WINNER',
            'edge': 'EDGE',
            'no_clear_winner': 'TIE',
            'insufficient_data': 'WAIT',
            'single_variant': 'NOTE',
            'no_data': 'NO DATA'
        }

        # Thumbnail verdict
        thumb = ctr_analysis.get('thumbnail_verdict', {})
        thumb_verdict = thumb.get('verdict', {})
        thumb_status = thumb_verdict.get('status', 'no_data')
        thumb_badge = status_badges.get(thumb_status, thumb_status.upper())
        thumb_rec = thumb_verdict.get('recommendation', 'No data')
        lines.append(f"**Thumbnail:** [{thumb_badge}] {thumb_rec}")

        # Title verdict
        title = ctr_analysis.get('title_verdict', {})
        title_verdict = title.get('verdict', {})
        title_status = title_verdict.get('status', 'no_data')
        title_badge = status_badges.get(title_status, title_status.upper())
        title_rec = title_verdict.get('recommendation', 'No data')
        lines.append(f"**Title:** [{title_badge}] {title_rec}")

        lines.append("")

        # Benchmark context
        benchmarks_data = ctr_analysis.get('benchmarks', {})
        overall = benchmarks_data.get('overall', {})
        by_category = benchmarks_data.get('by_category', {})
        category = thumb.get('category') or title.get('category')

        if overall.get('video_count', 0) > 0:
            lines.append(f"**Channel avg CTR:** {overall.get('avg_ctr', 0):.2f}%")
        if category and category in by_category:
            cat_data = by_category[category]
            sample_note = " *(low sample)*" if cat_data.get('low_sample') else ""
            lines.append(f"**Category ({category}) avg CTR:** {cat_data.get('avg_ctr', 0):.2f}% (n={cat_data.get('video_count', 0)} videos){sample_note}")

        lines.append("")

        # Attribution rate (from thumbnail verdict metadata)
        if thumb.get('attribution_rate'):
            lines.append(f"_Data: {thumb['attribution_rate']}_")
            lines.append("")

        # Freshness warning
        if thumb.get('freshness_warning'):
            lines.append(f"> **Warning:** {thumb['freshness_warning']}")
            lines.append("")

    # --- Section-Level Retention Diagnostics (Phase 35) ---
    section_diagnostics = analysis.get('section_diagnostics')
    if section_diagnostics and section_diagnostics.get('status') == 'success':
        lines.append("## Section-Level Retention Analysis")
        lines.append("")

        # Retention Drop Map
        lines.append("### Retention Drop Map")
        lines.append("")
        summary_table = section_diagnostics.get('summary_table', '')
        if summary_table:
            lines.append(summary_table)
        lines.append("")

        # Diagnostics
        diagnostics_list = section_diagnostics.get('diagnostics', [])
        if diagnostics_list:
            lines.append("### Diagnostics")
            lines.append("")
            diagnostics_md = format_diagnostics_markdown(diagnostics_list)
            lines.append(diagnostics_md)
        lines.append("")

    # --- Feedback Insights Section (Phase 31) ---
    if FEEDBACK_AVAILABLE:
        try:
            # Determine topic type from video performance data
            topic_type = None
            if VARIANTS_AVAILABLE:
                try:
                    from database import KeywordDB
                    db = KeywordDB()
                    cursor = db._conn.cursor()
                    cursor.execute(
                        "SELECT topic_type FROM video_performance WHERE video_id = ?",
                        (analysis.get('video_id'),)
                    )
                    row = cursor.fetchone()
                    if row and row[0]:
                        topic_type = row[0]
                    db.close()
                except Exception:
                    pass

            if topic_type:
                preamble = get_insights_preamble(topic_type, 'script')
                if preamble:
                    lines.append("## Past Performance Insights")
                    lines.append("")
                    lines.append(preamble)
                    lines.append("")
        except Exception:
            pass  # Non-blocking

    # --- Errors Section ---
    errors = analysis.get('errors', [])
    if errors:
        lines.append("## Errors")
        lines.append("")
        for err in errors:
            lines.append(f"- **{err.get('source')}:** {err.get('message')}")
        lines.append("")

    return "\n".join(lines)


if __name__ == '__main__':
    # CLI interface
    if len(sys.argv) < 2:
        print("Usage: python analyze.py VIDEO_ID_OR_URL [OPTIONS]")
        print("")
        print("Complete post-publish analysis with benchmarks and lessons.")
        print("")
        print("Options:")
        print("  --markdown      Output as human-readable Markdown (default: JSON)")
        print("  --ctr VALUE     Provide manual CTR (e.g., --ctr 4.5)")
        print("  --save          Save analysis to file (project folder or fallback)")
        print("  --output PATH   Save to specific path (implies --save)")
        print("  --script PATH   Add section-level retention diagnostics with script mapping")
        print("")
        print("Examples:")
        print("  python analyze.py wCFReiCGiks")
        print("  python analyze.py wCFReiCGiks --markdown")
        print("  python analyze.py wCFReiCGiks --save")
        print("  python analyze.py wCFReiCGiks --save --output ./custom/analysis.md")
        print("  python analyze.py https://youtu.be/wCFReiCGiks")
        print("  python analyze.py wCFReiCGiks --ctr 4.5 --markdown --save")
        print("  python analyze.py wCFReiCGiks --script path/to/script.md --save")
        sys.exit(1)

    # Parse arguments
    video_input = sys.argv[1]
    output_markdown = '--markdown' in sys.argv
    do_save = '--save' in sys.argv
    manual_ctr = None
    output_path = None
    script_path = None

    # Parse --ctr, --output, and --script arguments
    args = sys.argv[2:]
    for i, arg in enumerate(args):
        if arg == '--ctr' and i + 1 < len(args):
            try:
                ctr_value = float(args[i + 1])
                if 0 <= ctr_value <= 100:
                    manual_ctr = ctr_value
                else:
                    print(f"Error: --ctr must be between 0 and 100, got {ctr_value}")
                    sys.exit(1)
            except ValueError:
                print(f"Error: --ctr must be a number, got '{args[i + 1]}'")
                sys.exit(1)
        elif arg == '--output' and i + 1 < len(args):
            output_path = args[i + 1]
            do_save = True  # --output implies --save
        elif arg == '--script' and i + 1 < len(args):
            script_path = args[i + 1]

    # Run analysis
    analysis = run_analysis(video_input, manual_ctr=manual_ctr)

    # Run section diagnostics if --script provided
    section_diagnostics_result = None
    if script_path:
        try:
            video_id = extract_video_id(video_input)
            section_diagnostics_result = generate_section_diagnostics(video_id, script_path)

            if 'error' in section_diagnostics_result:
                print(f"\nWarning: Section diagnostics failed: {section_diagnostics_result['error']}")
                section_diagnostics_result = None
            else:
                # Add to analysis for markdown formatting
                analysis['section_diagnostics'] = section_diagnostics_result

                # Auto-update retention playbook (Part 9) after section diagnostics
                if PLAYBOOK_AVAILABLE:
                    try:
                        print("\nUpdating retention playbook (STYLE-GUIDE.md Part 9)...")
                        result = write_part9_to_style_guide(synthesize_part9())
                        if 'error' in result:
                            print(f"Warning: Playbook update failed: {result['error']}")
                        else:
                            print("Part 9 updated.")
                    except Exception as e:
                        print(f"Warning: Playbook update error: {str(e)}")
        except Exception as e:
            print(f"\nWarning: Section diagnostics error: {str(e)}")

    # Output to stdout
    if output_markdown or do_save:
        print(format_analysis_markdown(analysis))
    else:
        print(json.dumps(analysis, indent=2))

    # Save to file if requested
    if do_save:
        save_result = save_analysis(analysis, output_path=output_path)
        print("")
        print("---")
        print(f"Analysis saved to: {save_result['saved_to']}")
        if save_result['project_folder_found']:
            print("(Matched to video project folder)")
        else:
            print("(Saved to fallback location - no matching project folder found)")
