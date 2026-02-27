#!/usr/bin/env python3
"""
Metadata Consistency Checker - Pre-publish validation

Validates title, description, and tags for keyword consistency,
detects keyword stuffing, checks metadata quality.

Part of Phase 13-03 (Discovery Tools - Metadata Integration)
"""

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import Counter

from tools.logging_config import get_logger

logger = get_logger(__name__)


def infer_primary_keyword(title: str) -> str:
    """
    Extract likely primary keyword from title.

    Heuristics:
    - Remove common stop words
    - Find longest meaningful phrase (2-4 words)
    - Prioritize earlier words in title

    Args:
        title: Video title

    Returns:
        Inferred primary keyword
    """
    # Stop words to filter out
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
        'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
        'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this',
        'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
        'what', 'which', 'who', 'when', 'where', 'why', 'how'
    }

    # Clean and tokenize
    title_lower = title.lower()
    title_lower = re.sub(r'[^\w\s-]', ' ', title_lower)
    words = [w for w in title_lower.split() if w and w not in stop_words]

    if not words:
        return title.lower().strip()

    # Try to find meaningful 2-4 word phrases from start
    for length in [3, 2, 4]:
        if len(words) >= length:
            phrase = ' '.join(words[:length])
            return phrase

    # Fallback: first word
    return words[0]


def calculate_keyword_density(text: str, keyword: str) -> float:
    """
    Calculate keyword density as percentage.

    Args:
        text: Text to analyze
        keyword: Keyword phrase to count

    Returns:
        Density as decimal (0.02 = 2%)
    """
    text_lower = text.lower()
    keyword_lower = keyword.lower()

    # Count keyword occurrences
    count = text_lower.count(keyword_lower)

    # Count total words
    words = re.findall(r'\w+', text_lower)
    total_words = len(words)

    if total_words == 0:
        return 0.0

    # Keyword phrase word count
    keyword_words = len(keyword_lower.split())

    # Density = (keyword_count * keyword_words) / total_words
    density = (count * keyword_words) / total_words

    return density


def calculate_title_tag_overlap(title: str, tags: List[str]) -> Tuple[int, List[str]]:
    """
    Calculate word overlap between title and tags.

    Args:
        title: Video title
        tags: List of tags

    Returns:
        (overlap_count, overlapping_words)
    """
    # Extract meaningful words from title
    title_words = set(re.findall(r'\w+', title.lower()))
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    title_words = title_words - stop_words

    # Extract words from tags
    tag_words = set()
    for tag in tags:
        tag_words.update(re.findall(r'\w+', tag.lower()))

    # Find overlap
    overlap = title_words & tag_words

    return len(overlap), sorted(overlap)


def check_metadata_consistency(metadata: Dict) -> Dict:
    """
    Check metadata consistency and quality.

    Args:
        metadata: Dict with keys:
            - title (str): Video title
            - description (str): Video description
            - tags (List[str]): List of tags
            - primary_keyword (str, optional): Primary keyword to check for

    Returns:
        Dict with keys:
            - passed (bool): Overall pass/fail
            - issues (List[Dict]): List of issues found
            - stats (Dict): Statistics about metadata
            - summary (str): Human-readable summary
    """
    title = metadata.get('title', '').strip()
    description = metadata.get('description', '').strip()
    tags = metadata.get('tags', [])
    primary_keyword = metadata.get('primary_keyword')

    # Infer primary keyword if not provided
    if not primary_keyword:
        primary_keyword = infer_primary_keyword(title)

    issues = []

    # Check 1: Primary keyword in title
    if primary_keyword.lower() not in title.lower():
        issues.append({
            'severity': 'HIGH',
            'check': 'Primary keyword in title',
            'message': f'Primary keyword "{primary_keyword}" not found in title',
            'suggestion': f'Add "{primary_keyword}" to title for better discoverability'
        })

    # Check 2: Primary keyword in description first 200 chars
    desc_start = description[:200].lower() if len(description) >= 200 else description.lower()
    if primary_keyword.lower() not in desc_start:
        issues.append({
            'severity': 'HIGH',
            'check': 'Primary keyword in description opening',
            'message': f'Primary keyword "{primary_keyword}" not in first 200 characters',
            'suggestion': 'Add primary keyword early in description for SEO'
        })

    # Check 3: Primary keyword in tags
    tags_lower = [t.lower() for t in tags]
    if not any(primary_keyword.lower() in tag for tag in tags_lower):
        issues.append({
            'severity': 'MEDIUM',
            'check': 'Primary keyword in tags',
            'message': f'Primary keyword "{primary_keyword}" not found in any tag',
            'suggestion': f'Add tag: "{primary_keyword}"'
        })

    # Check 4: Keyword stuffing
    title_density = calculate_keyword_density(title, primary_keyword)
    desc_density = calculate_keyword_density(description, primary_keyword)

    if title_density > 0.3:  # 30% of title is keyword
        issues.append({
            'severity': 'HIGH',
            'check': 'Keyword stuffing in title',
            'message': f'Primary keyword density in title: {title_density*100:.1f}% (threshold: 30%)',
            'suggestion': 'Reduce keyword repetition in title'
        })

    if desc_density > 0.02:  # 2% of description is keyword
        issues.append({
            'severity': 'HIGH',
            'check': 'Keyword stuffing in description',
            'message': f'Primary keyword density in description: {desc_density*100:.1f}% (threshold: 2%)',
            'suggestion': 'Reduce keyword repetition in description'
        })

    # Check 5: Title-tag overlap
    overlap_count, overlap_words = calculate_title_tag_overlap(title, tags)
    if overlap_count < 3:
        issues.append({
            'severity': 'MEDIUM',
            'check': 'Title-tag overlap',
            'message': f'Only {overlap_count} words overlap between title and tags',
            'suggestion': 'Add more title words as tags for consistency'
        })

    # Check 6: Description length
    word_count = len(description.split())
    if word_count < 200:
        issues.append({
            'severity': 'WARNING',
            'check': 'Description length',
            'message': f'Description has {word_count} words (recommended: 200+)',
            'suggestion': 'Expand description for better context and SEO'
        })

    # Check 7: Tag count
    tag_count = len(tags)
    if tag_count < 5:
        issues.append({
            'severity': 'WARNING',
            'check': 'Tag count',
            'message': f'Only {tag_count} tags (recommended: 5-30)',
            'suggestion': 'Add more relevant tags'
        })
    elif tag_count > 30:
        issues.append({
            'severity': 'WARNING',
            'check': 'Tag count',
            'message': f'{tag_count} tags (recommended: 5-30)',
            'suggestion': 'Focus on most relevant tags'
        })

    # Calculate stats
    stats = {
        'primary_keyword': primary_keyword,
        'title_length': len(title),
        'description_length': word_count,
        'tag_count': tag_count,
        'title_keyword_density': f'{title_density*100:.1f}%',
        'description_keyword_density': f'{desc_density*100:.1f}%',
        'title_tag_overlap': overlap_count,
        'overlapping_words': overlap_words
    }

    # Determine pass/fail
    high_severity_issues = [i for i in issues if i['severity'] == 'HIGH']
    passed = len(high_severity_issues) == 0

    # Generate summary
    if passed:
        summary = f"[PASS] Metadata is consistent ({len(issues)} warnings)"
    else:
        summary = f"[FAIL] {len(high_severity_issues)} HIGH severity issues, {len(issues) - len(high_severity_issues)} other issues"

    return {
        'passed': passed,
        'issues': issues,
        'stats': stats,
        'summary': summary
    }


def format_metadata_report(result: Dict, format: str = 'markdown') -> str:
    """
    Format check results as markdown or JSON.

    Args:
        result: Result from check_metadata_consistency()
        format: 'markdown' or 'json'

    Returns:
        Formatted report string
    """
    if format == 'json':
        return json.dumps(result, indent=2)

    # Markdown format
    lines = []
    lines.append("# Metadata Consistency Check")
    lines.append("")
    lines.append(f"**Status:** {result['summary']}")
    lines.append("")

    # Stats
    lines.append("## Statistics")
    lines.append("")
    stats = result['stats']
    lines.append(f"- **Primary keyword:** {stats['primary_keyword']}")
    lines.append(f"- **Title length:** {stats['title_length']} characters")
    lines.append(f"- **Description length:** {stats['description_length']} words")
    lines.append(f"- **Tag count:** {stats['tag_count']}")
    lines.append(f"- **Title keyword density:** {stats['title_keyword_density']}")
    lines.append(f"- **Description keyword density:** {stats['description_keyword_density']}")
    lines.append(f"- **Title-tag overlap:** {stats['title_tag_overlap']} words ({', '.join(stats['overlapping_words'])})")
    lines.append("")

    # Issues
    if result['issues']:
        lines.append("## Issues Found")
        lines.append("")

        # Group by severity
        by_severity = {}
        for issue in result['issues']:
            severity = issue['severity']
            if severity not in by_severity:
                by_severity[severity] = []
            by_severity[severity].append(issue)

        for severity in ['HIGH', 'MEDIUM', 'WARNING']:
            if severity in by_severity:
                lines.append(f"### {severity} Priority")
                lines.append("")
                for issue in by_severity[severity]:
                    lines.append(f"**{issue['check']}**")
                    lines.append(f"- Problem: {issue['message']}")
                    lines.append(f"- Fix: {issue['suggestion']}")
                    lines.append("")
    else:
        lines.append("## No Issues Found")
        lines.append("")
        lines.append("Metadata meets all consistency requirements.")
        lines.append("")

    return '\n'.join(lines)


def parse_metadata_file(filepath: Path) -> Dict:
    """
    Parse YOUTUBE-METADATA.md file.

    Expected format:
        # Title
        [title text]

        ## Description
        [description text]

        ## Tags
        tag1, tag2, tag3

    Args:
        filepath: Path to YOUTUBE-METADATA.md

    Returns:
        Dict with title, description, tags
    """
    content = filepath.read_text(encoding='utf-8')

    metadata = {
        'title': '',
        'description': '',
        'tags': []
    }

    # Extract title (first # heading or text before ##)
    title_match = re.search(r'^#\s+(.+?)$', content, re.MULTILINE)
    if title_match:
        metadata['title'] = title_match.group(1).strip()

    # Extract description (text between ## Description and next ##)
    desc_match = re.search(r'##\s+Description\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
    if desc_match:
        metadata['description'] = desc_match.group(1).strip()

    # Extract tags (after ## Tags)
    tags_match = re.search(r'##\s+Tags\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
    if tags_match:
        tags_text = tags_match.group(1).strip()
        # Split by comma and clean
        metadata['tags'] = [t.strip() for t in tags_text.split(',') if t.strip()]

    return metadata


def main():
    parser = argparse.ArgumentParser(
        description='Check metadata consistency for YouTube videos',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check metadata from command line
  python metadata_checker.py --title "The Dark Ages Myth" --description "..." --tags "history,medieval"

  # Check metadata from file
  python metadata_checker.py --file YOUTUBE-METADATA.md

  # Get JSON output
  python metadata_checker.py --file YOUTUBE-METADATA.md --json

  # Specify primary keyword
  python metadata_checker.py --file YOUTUBE-METADATA.md --keyword "dark ages myth"
        """
    )

    parser.add_argument('--title', help='Video title')
    parser.add_argument('--description', help='Video description')
    parser.add_argument('--tags', help='Comma-separated tags')
    parser.add_argument('--keyword', '--primary-keyword', dest='primary_keyword',
                        help='Primary keyword (auto-inferred if not provided)')
    parser.add_argument('--file', type=Path, help='Path to YOUTUBE-METADATA.md file')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument("--verbose", "-v", action="store_true", help="Show debug output on stderr")
    verbosity.add_argument("--quiet", "-q", action="store_true", help="Only show errors on stderr")

    args = parser.parse_args()

    from tools.logging_config import setup_logging
    setup_logging(args.verbose, args.quiet)

    # Get metadata from file or command line
    if args.file:
        if not args.file.exists():
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            return 1
        metadata = parse_metadata_file(args.file)
    elif args.title and args.description:
        metadata = {
            'title': args.title,
            'description': args.description,
            'tags': [t.strip() for t in args.tags.split(',') if t.strip()] if args.tags else []
        }
    else:
        parser.print_help()
        return 1

    # Add primary keyword if specified
    if args.primary_keyword:
        metadata['primary_keyword'] = args.primary_keyword

    # Run check
    result = check_metadata_consistency(metadata)

    # Format output
    output = format_metadata_report(result, format='json' if args.json else 'markdown')

    # Handle Unicode output for Windows console
    try:
        print(output)
    except UnicodeEncodeError:
        # Fallback for Windows console without UTF-8 support
        print(output.encode('utf-8', errors='replace').decode('utf-8', errors='replace'))

    # Exit with appropriate code
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    exit(main())
