"""
News Hook Scanner — checks pipeline topics for fresh news relevance.

Scans all _IN_PRODUCTION projects that aren't published yet, WebSearches
each topic for recent developments, and ranks them by urgency.

This helps decide filming order: "Berlin Conference or Tordesillas first?"

Usage:
    python tools/discovery/news_scanner.py              # scan all pipeline topics
    python tools/discovery/news_scanner.py --top 5      # show top 5 most timely
    python tools/discovery/news_scanner.py --json       # machine-readable output

Called by: /next --timely
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional


# ---------------------------------------------------------------------------
# Topic extraction from project folders
# ---------------------------------------------------------------------------

# Map folder slug patterns to search-friendly topic strings
SLUG_OVERRIDES = {
    'fuentes-fact-check': 'Nick Fuentes fact check',
    'vance-part-2-review': 'JD Vance history claims',
    'netanyahu-map': 'Netanyahu map Greater Israel',
    'vichy-statut-juifs': 'Vichy France anti-Jewish law Statut des Juifs',
    'adwa-wuchale': 'Battle of Adwa Treaty of Wuchale Ethiopia',
    'belavezha-accords': 'Belavezha Accords dissolution Soviet Union',
    'guadalupe-hidalgo': 'Treaty of Guadalupe Hidalgo Mexico',
    'bir-tawil': 'Bir Tawil unclaimed territory Egypt Sudan',
    'panama-canal-deconcini': 'Panama Canal Treaty DeConcini reservation',
    'belize-icj-endgame': 'Belize Guatemala ICJ case',
    'bermeja-island': 'Bermeja Island Mexico missing island',
    'gibraltar-treaty-utrecht': 'Gibraltar Treaty of Utrecht Spain UK',
    'spanish-colonial-law-untranslated': 'Spanish colonial law Latin America',
    'greenland-independence': 'Greenland independence Denmark',
}

# Projects that are already published or not real video topics
SKIP_SLUGS = {
    'format-research', 'README', 'Taiwan', 'Tariffs',
}

# Status keywords indicating a project is still filmable (not published)
FILMABLE_STATUSES = {
    'RESEARCHING', 'SCRIPT', 'APPROVED', 'READY', 'EDITING',
    'DRAFT', 'VERIFIED', 'IN PROGRESS',
}


def _slug_to_topic(slug: str) -> str:
    """Convert a project folder slug to a search-friendly topic string."""
    # Strip leading number and year suffix
    clean = re.sub(r'^\d+-', '', slug)
    clean = re.sub(r'-\d{4}$', '', clean)

    # Check overrides
    if clean in SLUG_OVERRIDES:
        return SLUG_OVERRIDES[clean]

    # Default: replace hyphens with spaces, title case
    return clean.replace('-', ' ').title()


def get_pipeline_topics(production_dir: str = 'video-projects/_IN_PRODUCTION') -> List[Dict[str, str]]:
    """Get all pipeline topics that aren't published yet.

    Returns list of dicts with: slug, topic, folder_path, status
    """
    prod_path = Path(production_dir)
    if not prod_path.is_dir():
        return []

    topics = []
    for folder in sorted(prod_path.iterdir()):
        if not folder.is_dir():
            continue

        slug = folder.name
        # Skip non-project items
        clean_slug = re.sub(r'^\d+-', '', slug).rstrip('-0123456789')
        if clean_slug in SKIP_SLUGS or slug in SKIP_SLUGS:
            continue

        # Check project status
        status = 'UNKNOWN'
        status_file = folder / 'PROJECT-STATUS.md'
        if status_file.exists():
            try:
                text = status_file.read_text(encoding='utf-8')[:500]
                # Look for status line
                m = re.search(r'Status[:\s]*\*?\*?([A-Z ]+)', text)
                if m:
                    status = m.group(1).strip()
            except Exception:
                pass

        # Check for published indicators
        post_pub = folder / 'POST-PUBLISH-ANALYSIS.md'
        has_srt = any(folder.glob('*.srt'))
        has_mp4 = any(folder.glob('*.mp4'))

        if post_pub.exists():
            status = 'PUBLISHED'

        # Only include filmable projects
        if status == 'PUBLISHED':
            continue

        topic = _slug_to_topic(slug)
        topics.append({
            'slug': slug,
            'topic': topic,
            'folder_path': str(folder),
            'status': status,
            'has_script': (folder / 'SCRIPT.md').exists()
                          or (folder / '02-SCRIPT-DRAFT.md').exists()
                          or (folder / 'FINAL-SCRIPT.md').exists(),
        })

    return topics


def format_search_queries(topic: str) -> List[str]:
    """Generate search queries for a topic's news relevance."""
    return [
        f'"{topic}" 2026',
        f'"{topic}" 2025 OR 2026 news',
    ]


# ---------------------------------------------------------------------------
# Results formatting
# ---------------------------------------------------------------------------

def format_report(results: List[Dict[str, Any]]) -> str:
    """Format scan results as a markdown report."""
    lines = [
        '# News Hook Scanner — Pipeline Timeliness Report',
        '',
        f'**Scanned:** {len(results)} pipeline topics',
        f'**Date:** Check timestamps in results for freshness',
        '',
        '---',
        '',
    ]

    if not results:
        lines.append('No pipeline topics found to scan.')
        return '\n'.join(lines)

    # Sort by hook count descending
    results.sort(key=lambda r: r.get('hook_count', 0), reverse=True)

    # Urgent section
    urgent = [r for r in results if r.get('hook_count', 0) >= 2]
    if urgent:
        lines.append('## URGENT — Multiple Fresh News Hooks')
        lines.append('')
        for r in urgent:
            lines.append(f"### {r['topic']} ({r['slug']})")
            lines.append(f"**Status:** {r['status']} | **Hooks found:** {r['hook_count']}")
            lines.append('')
            for hook in r.get('hooks', []):
                lines.append(f"- **{hook.get('date', '?')}:** {hook.get('headline', '?')}")
                if hook.get('source'):
                    lines.append(f"  Source: {hook['source']}")
            lines.append('')
            lines.append(f"**Filming priority boost:** This topic has active news. Consider prioritizing.")
            lines.append('')
        lines.append('---')
        lines.append('')

    # Some hooks
    some = [r for r in results if r.get('hook_count', 0) == 1]
    if some:
        lines.append('## TIMELY — One Recent Hook')
        lines.append('')
        for r in some:
            lines.append(f"**{r['topic']}** ({r['slug']}) — {r['status']}")
            for hook in r.get('hooks', []):
                lines.append(f"  - {hook.get('headline', '?')} ({hook.get('date', '?')})")
            lines.append('')
        lines.append('---')
        lines.append('')

    # No hooks
    none_found = [r for r in results if r.get('hook_count', 0) == 0]
    if none_found:
        lines.append('## EVERGREEN — No Recent News (film anytime)')
        lines.append('')
        for r in none_found:
            lines.append(f"- {r['topic']} ({r['slug']}) — {r['status']}")
        lines.append('')

    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# CLI entry point (for manual testing; actual scanning uses WebSearch via agent)
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    root = Path(__file__).resolve().parent.parent.parent
    topics = get_pipeline_topics(str(root / 'video-projects' / '_IN_PRODUCTION'))

    if '--json' in sys.argv:
        print(json.dumps(topics, indent=2))
    else:
        print(f"Pipeline topics to scan ({len(topics)}):\n")
        for t in topics:
            status_icon = 'S' if t['has_script'] else 'R'
            print(f"  [{status_icon}] {t['topic']:<50} ({t['slug']})")
        print(f"\nTo scan for news: /next --timely")
