"""
Feedback Parser Module

Parses POST-PUBLISH-ANALYSIS markdown files into structured data for database storage.
Uses best-effort regex extraction for known markdown structure.

Usage:
    from feedback_parser import parse_analysis_file, backfill_all

    # Parse single file
    result = parse_analysis_file('path/to/POST-PUBLISH-ANALYSIS.md')
    print(result['video_id'], result['avg_retention'])

    # Backfill all analysis files
    from pathlib import Path
    results = backfill_all(Path('../..'))
    print(f"Processed: {results['processed']}, Errors: {results['errors']}")

Dependencies:
    - stdlib only: re, pathlib, datetime, json, sys
    - KeywordDB for backfill (graceful import)
"""

import re
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any


def extract_video_id(content: str, filepath: str = '') -> Optional[str]:
    """
    Extract video ID from markdown content or filename.

    Args:
        content: Markdown file content
        filepath: Path to file (for fallback extraction from filename)

    Returns:
        11-character video ID or None
    """
    # Try to extract from header: **Video ID:** XXXX
    video_id_match = re.search(r'\*\*Video ID:\*\*\s*(\w+)', content)
    if video_id_match:
        return video_id_match.group(1)

    # Fallback: extract from filename pattern POST-PUBLISH-ANALYSIS-{VIDEO_ID}.md
    if filepath:
        filename_match = re.search(r'POST-PUBLISH-ANALYSIS-(\w+)\.md', filepath)
        if filename_match:
            return filename_match.group(1)

    return None


def extract_metrics(content: str) -> Dict[str, Any]:
    """
    Extract numeric performance metrics from markdown.

    Args:
        content: Markdown file content

    Returns:
        Dict with extracted metrics (None for missing values)
    """
    metrics = {}

    # Extract retention percentages
    avg_ret_match = re.search(r'\*\*Average retention:\*\*\s*([\d.]+)%', content)
    metrics['avg_retention'] = float(avg_ret_match.group(1)) if avg_ret_match else None

    final_ret_match = re.search(r'\*\*Final retention:\*\*\s*([\d.]+)%', content)
    metrics['final_retention'] = float(final_ret_match.group(1)) if final_ret_match else None

    # Extract CTR (skip if "Not available via API")
    ctr_match = re.search(r'\*\*CTR:\*\*\s*([\d.]+)%', content)
    metrics['ctr'] = float(ctr_match.group(1)) if ctr_match else None

    # Extract impressions (with comma handling)
    impressions_match = re.search(r'\*\*Impressions:\*\*\s*([\d,]+)', content)
    if impressions_match:
        impressions_str = impressions_match.group(1).replace(',', '')
        metrics['impressions'] = int(impressions_str)
    else:
        metrics['impressions'] = None

    # Extract from Performance table
    # | Views | 5,088 | 628 | +710% |  -> extract "This Video" column (second column)
    views_match = re.search(r'\|\s*Views\s*\|\s*([\d,]+)\s*\|', content)
    if views_match:
        views_str = views_match.group(1).replace(',', '')
        metrics['views'] = int(views_str)
    else:
        metrics['views'] = None

    # | Subscribers | +51 | +1 | +5000% |  -> extract and strip +
    subs_match = re.search(r'\|\s*Subscribers\s*\|\s*\+?([\d,]+)\s*\|', content)
    if subs_match:
        subs_str = subs_match.group(1).replace(',', '')
        metrics['subscribers_gained'] = int(subs_str)
    else:
        metrics['subscribers_gained'] = None

    return metrics


def extract_lessons(content: str) -> Dict[str, List[str]]:
    """
    Extract qualitative insights from Lessons section.

    Args:
        content: Markdown file content

    Returns:
        Dict with 'observations' and 'actionable' lists
    """
    lessons = {
        'observations': [],
        'actionable': []
    }

    # Extract Observations (### Observations followed by bullet list)
    obs_section_match = re.search(
        r'### Observations\s*\n\n(.*?)(?:\n\n###|\n\n\*\*|\Z)',
        content,
        re.DOTALL
    )
    if obs_section_match:
        obs_text = obs_section_match.group(1)
        obs_lines = [line.strip() for line in obs_text.split('\n') if line.strip().startswith('-')]
        lessons['observations'] = [line.lstrip('- ').strip() for line in obs_lines if line]

    # Extract Actionable Items (### Actionable Items followed by checkbox bullets)
    action_section_match = re.search(
        r'### Actionable Items\s*\n\n(.*?)(?:\n\n##|\Z)',
        content,
        re.DOTALL
    )
    if action_section_match:
        action_text = action_section_match.group(1)
        action_lines = [line.strip() for line in action_text.split('\n') if line.strip().startswith('-')]
        # Strip checkbox "- [ ] " or "- [x] "
        lessons['actionable'] = [
            re.sub(r'^-\s*\[[ x]\]\s*', '', line).strip()
            for line in action_lines if line
        ]

    return lessons


def extract_drop_points(content: str) -> List[Dict[str, Any]]:
    """
    Extract drop-off points from retention table.

    Args:
        content: Markdown file content

    Returns:
        List of dicts with position_pct, viewers_lost_pct, location
    """
    drop_points = []

    # Find Drop-off Points section table
    # | 3% | 7.0% dropped | intro |
    drop_matches = re.finditer(
        r'\|\s*(\d+)%\s*\|\s*([\d.]+)%\s*dropped\s*\|\s*([^|]+)\s*\|',
        content
    )

    for match in drop_matches:
        drop_points.append({
            'position_pct': int(match.group(1)),
            'viewers_lost_pct': float(match.group(2)),
            'location': match.group(3).strip()
        })

    return drop_points


def extract_discovery_diagnosis(content: str) -> Optional[Dict[str, str]]:
    """
    Extract discovery diagnostics from Discovery Diagnostics section.

    Args:
        content: Markdown file content

    Returns:
        Dict with primary_issue, severity, summary or None
    """
    # Find Discovery Diagnostics section
    discovery_section = re.search(
        r'## Discovery Diagnostics\s*\n\n(.*?)(?:\n\n##|\Z)',
        content,
        re.DOTALL
    )

    if not discovery_section:
        return None

    section_text = discovery_section.group(1)

    diagnosis = {}

    # Extract **Diagnosis:** line
    diag_match = re.search(r'\*\*Diagnosis:\*\*\s*([^\n]+)', section_text)
    diagnosis['summary'] = diag_match.group(1).strip() if diag_match else None

    # Extract **Primary Issue:** and (Severity: XXX)
    issue_match = re.search(
        r'\*\*Primary Issue:\*\*\s*([^(]+)(?:\(Severity:\s*(\w+)\))?',
        section_text
    )
    if issue_match:
        diagnosis['primary_issue'] = issue_match.group(1).strip()
        diagnosis['severity'] = issue_match.group(2).strip() if issue_match.group(2) else 'UNKNOWN'
    else:
        diagnosis['primary_issue'] = None
        diagnosis['severity'] = None

    return diagnosis if any(diagnosis.values()) else None


def parse_analysis_file(filepath: str) -> Dict[str, Any]:
    """
    Parse POST-PUBLISH-ANALYSIS markdown file into structured data.

    Main entry point. Calls all extractor functions and returns complete dict.

    Args:
        filepath: Path to POST-PUBLISH-ANALYSIS.md file

    Returns:
        Dict with all extracted data, or {'error': msg} on failure
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract all components
        video_id = extract_video_id(content, filepath)
        if not video_id:
            return {'error': 'Could not extract video_id', 'filepath': filepath}

        metrics = extract_metrics(content)
        lessons = extract_lessons(content)
        drop_points = extract_drop_points(content)
        discovery = extract_discovery_diagnosis(content)

        # Find biggest drop point (for retention_drop_point column)
        biggest_drop = None
        if drop_points:
            biggest = max(drop_points, key=lambda d: d['viewers_lost_pct'])
            biggest_drop = biggest['position_pct']

        # Combine into complete result
        result = {
            'video_id': video_id,
            'parsed_at': datetime.utcnow().isoformat(),
            'filepath': filepath,
            **metrics,  # avg_retention, final_retention, ctr, impressions, views, subscribers_gained
            'observations': lessons['observations'],
            'actionable': lessons['actionable'],
            'drop_points': drop_points,
            'biggest_drop_position': biggest_drop,
            'discovery': discovery
        }

        return result

    except FileNotFoundError:
        return {'error': 'File not found', 'filepath': filepath}
    except Exception as e:
        return {'error': f'Parse failed: {str(e)}', 'filepath': filepath}


def find_analysis_files(project_root: Path) -> List[Path]:
    """
    Scan for all POST-PUBLISH-ANALYSIS files in project.

    Searches:
    - video-projects/_IN_PRODUCTION/*/POST-PUBLISH-ANALYSIS.md
    - video-projects/_READY_TO_FILM/*/POST-PUBLISH-ANALYSIS.md
    - video-projects/_ARCHIVED/*/POST-PUBLISH-ANALYSIS.md
    - channel-data/analyses/POST-PUBLISH-ANALYSIS-*.md

    Args:
        project_root: Path to project root directory

    Returns:
        List of Path objects for found analysis files
    """
    files = []

    # Search video-projects lifecycle folders
    for lifecycle_folder in ['_IN_PRODUCTION', '_READY_TO_FILM', '_ARCHIVED']:
        pattern = project_root / 'video-projects' / lifecycle_folder / '*' / 'POST-PUBLISH-ANALYSIS.md'
        files.extend(project_root.glob(f'video-projects/{lifecycle_folder}/*/POST-PUBLISH-ANALYSIS.md'))

    # Search channel-data/analyses folder
    analyses_pattern = project_root / 'channel-data' / 'analyses' / 'POST-PUBLISH-ANALYSIS-*.md'
    files.extend(project_root.glob('channel-data/analyses/POST-PUBLISH-ANALYSIS-*.md'))

    return sorted(files)


def backfill_all(project_root: Path, force: bool = False) -> Dict[str, Any]:
    """
    Process all POST-PUBLISH-ANALYSIS files and store in database.

    Args:
        project_root: Path to project root directory
        force: If True, re-parse files that already have feedback stored

    Returns:
        Dict with processed/skipped/errors counts and details list
    """
    # Try to import KeywordDB for storage
    try:
        sys.path.insert(0, str(project_root / 'tools' / 'discovery'))
        from database import KeywordDB
        db = KeywordDB()
    except ImportError:
        return {
            'error': 'KeywordDB not available',
            'processed': 0,
            'skipped': 0,
            'errors': 1
        }

    results = {
        'processed': 0,
        'skipped': 0,
        'errors': 0,
        'details': []
    }

    files = find_analysis_files(project_root)
    total = len(files)

    print(f"Found {total} analysis files to process")
    print()

    for i, filepath in enumerate(files, 1):
        filename = filepath.name
        print(f"[{i}/{total}] Parsing: {filename}...", end=' ')

        # Parse file
        parsed = parse_analysis_file(str(filepath))

        if 'error' in parsed:
            print(f"ERROR: {parsed['error']}")
            results['errors'] += 1
            results['details'].append({
                'file': filename,
                'status': 'error',
                'message': parsed['error']
            })
            continue

        video_id = parsed['video_id']

        # Check if already has feedback (unless force=True)
        if not force and db.has_feedback(video_id):
            print("SKIP (already has feedback)")
            results['skipped'] += 1
            results['details'].append({
                'file': filename,
                'video_id': video_id,
                'status': 'skipped'
            })
            continue

        # Store in database
        feedback_data = {
            'biggest_drop_position': parsed['biggest_drop_position'],
            'observations': parsed['observations'],
            'actionable': parsed['actionable'],
            'discovery': parsed.get('discovery', {})
        }

        store_result = db.store_video_feedback(video_id, feedback_data)

        if 'error' in store_result:
            print(f"ERROR: {store_result['error']}")
            results['errors'] += 1
            results['details'].append({
                'file': filename,
                'video_id': video_id,
                'status': 'error',
                'message': store_result['error']
            })
        elif store_result.get('status') == 'no_match':
            print("SKIP (video not in performance table)")
            results['skipped'] += 1
            results['details'].append({
                'file': filename,
                'video_id': video_id,
                'status': 'no_match'
            })
        else:
            print("OK")
            results['processed'] += 1
            results['details'].append({
                'file': filename,
                'video_id': video_id,
                'status': 'success'
            })

    db.close()

    print()
    print(f"Complete: {results['processed']} processed, {results['skipped']} skipped, {results['errors']} errors")

    return results


if __name__ == '__main__':
    # CLI usage for testing
    if len(sys.argv) > 1:
        if sys.argv[1] == 'backfill':
            project_root = Path(__file__).parent.parent.parent
            force = '--force' in sys.argv
            result = backfill_all(project_root, force=force)
            sys.exit(0 if result['errors'] == 0 else 1)
        else:
            # Parse single file
            result = parse_analysis_file(sys.argv[1])
            print(json.dumps(result, indent=2))
    else:
        print("Usage:")
        print("  python feedback_parser.py <path-to-analysis-file>")
        print("  python feedback_parser.py backfill [--force]")
