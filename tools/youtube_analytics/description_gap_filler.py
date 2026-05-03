"""
Description Keyword Gap Filler

Cross-references actual YouTube search terms (from Analytics API) against
video descriptions to find high-value keywords that are missing.
Generates actionable recommendations for description edits.

Data sources:
  - _search_terms.json (cached search queries per video)
  - YOUTUBE-METADATA.md files (current descriptions)
  - analytics.db (video metadata)

Usage:
    python -m tools.youtube_analytics.description_gap_filler --report
    python -m tools.youtube_analytics.description_gap_filler --video VIDEO_ID
    python -m tools.youtube_analytics.description_gap_filler --project PROJECT_SLUG
    python -m tools.youtube_analytics.description_gap_filler --top 10
"""

import argparse
import json
import re
import sqlite3
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from tools.logging_config import get_logger, setup_logging

logger = get_logger(__name__)

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PROJECTS_DIR = PROJECT_ROOT / "video-projects" / "_IN_PRODUCTION"
DB_PATH = PROJECT_ROOT / "tools" / "youtube_analytics" / "analytics.db"
SEARCH_TERMS_PATH = Path(__file__).parent / "_search_terms.json"
GAPS_CACHE = Path(__file__).parent / "_description_gaps.json"
REPORT_PATH = PROJECT_ROOT / "channel-data" / "DESCRIPTION-KEYWORD-GAPS.md"

# Common stop words to ignore in keyword matching
STOP_WORDS = {
    'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'can', 'shall', 'to', 'of', 'in', 'for',
    'on', 'with', 'at', 'by', 'from', 'as', 'into', 'through', 'during',
    'before', 'after', 'above', 'below', 'between', 'under', 'again',
    'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
    'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most', 'other',
    'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
    'than', 'too', 'very', 'just', 'and', 'but', 'or', 'if', 'this',
    'that', 'these', 'those', 'what', 'which', 'who', 'whom', 'its',
    'it', 'he', 'she', 'they', 'we', 'you', 'i', 'me', 'my', 'your',
    'his', 'her', 'our', 'their', 'about', 'up', 'out', 'off', 'over',
    'vs', 'video', 'youtube', 'subscribe', 'channel',
}


def load_search_terms() -> dict:
    """Load cached search term data. Returns {video_id: [terms]}."""
    if not SEARCH_TERMS_PATH.exists():
        logger.warning("No search term cache at %s. Run search_term_analysis.py first.", SEARCH_TERMS_PATH)
        return {}

    with open(SEARCH_TERMS_PATH, encoding='utf-8') as f:
        return json.load(f)


def load_video_metadata() -> dict:
    """Load video metadata from DB. Returns {video_id: {title, topic_type, views}}."""
    if not DB_PATH.exists():
        return {}

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT video_id, title, topic_type, views FROM videos")
    result = {row['video_id']: dict(row) for row in cur.fetchall()}
    conn.close()
    return result


def find_description_for_video(video_id: str, title: str) -> Optional[str]:
    """Find the description text from YOUTUBE-METADATA.md for a video."""
    # Search all project folders for matching YOUTUBE-METADATA.md
    for project_dir in PROJECTS_DIR.iterdir():
        if not project_dir.is_dir():
            continue

        # Check for metadata files
        for name in ['YOUTUBE-METADATA.md', '06-YOUTUBE-METADATA.md']:
            meta_path = project_dir / name
            if not meta_path.exists():
                continue

            try:
                text = meta_path.read_text(encoding='utf-8')
            except Exception:
                continue

            # Check if this metadata file matches the video (by title substring)
            title_words = title.lower().split()[:4]
            text_lower = text.lower()
            if sum(1 for w in title_words if w in text_lower) >= 3:
                # Extract description block (between ``` markers after ## Description)
                desc_match = re.search(
                    r'##\s*Description\s*\n+```\s*\n(.*?)\n```',
                    text, re.DOTALL
                )
                if desc_match:
                    return desc_match.group(1).strip()

    return None


def normalize_keyword(kw: str) -> str:
    """Normalize a keyword for comparison."""
    kw = kw.lower().strip()
    kw = re.sub(r'[^\w\s]', '', kw)
    return ' '.join(kw.split())


def extract_description_keywords(description: str) -> set:
    """Extract meaningful keywords/phrases from a description."""
    text = description.lower()
    text = re.sub(r'https?://\S+', '', text)  # Remove URLs
    text = re.sub(r'#\w+', '', text)  # Remove hashtags
    text = re.sub(r'[^\w\s]', ' ', text)
    text = ' '.join(text.split())

    words = set()
    tokens = text.split()

    # Single words (non-stop)
    for t in tokens:
        if t not in STOP_WORDS and len(t) > 2:
            words.add(t)

    # Bigrams
    for i in range(len(tokens) - 1):
        bigram = f"{tokens[i]} {tokens[i+1]}"
        words.add(bigram)

    # Trigrams
    for i in range(len(tokens) - 2):
        trigram = f"{tokens[i]} {tokens[i+1]} {tokens[i+2]}"
        words.add(trigram)

    return words


def check_keyword_in_description(search_term: str, desc_keywords: set, description: str) -> bool:
    """Check if a search term (or close variant) appears in the description."""
    normalized = normalize_keyword(search_term)
    desc_lower = description.lower()

    # Exact substring check
    if normalized in desc_lower:
        return True

    # Check individual words of multi-word terms
    term_words = [w for w in normalized.split() if w not in STOP_WORDS and len(w) > 2]
    if not term_words:
        return True  # All stop words = irrelevant

    # If all meaningful words appear in description, consider it present
    if all(w in desc_lower for w in term_words):
        return True

    return False


def analyze_video(video_id: str, search_terms: list, description: str,
                  meta: dict) -> dict:
    """Analyze keyword gaps for a single video."""
    desc_keywords = extract_description_keywords(description)

    gaps = []
    present = []

    for term_data in search_terms:
        term = term_data['term']
        views = term_data.get('views', 0)
        watch_time = term_data.get('watch_time_minutes', 0)

        if check_keyword_in_description(term, desc_keywords, description):
            present.append({
                'term': term,
                'views': views,
                'watch_time': watch_time,
                'status': 'present',
            })
        else:
            # Calculate impact score: views × avg watch time per view
            avg_wt = watch_time / max(views, 1)
            impact = views * (1 + avg_wt / 10)  # Weight by engagement quality

            gaps.append({
                'term': term,
                'views': views,
                'watch_time': watch_time,
                'avg_watch_time': avg_wt,
                'impact_score': impact,
                'status': 'missing',
            })

    # Sort gaps by impact
    gaps.sort(key=lambda x: x['impact_score'], reverse=True)

    total_search_views = sum(t.get('views', 0) for t in search_terms)
    gap_views = sum(g['views'] for g in gaps)

    return {
        'video_id': video_id,
        'title': meta.get('title', ''),
        'topic_type': meta.get('topic_type', ''),
        'total_views': meta.get('views', 0),
        'total_search_views': total_search_views,
        'gaps': gaps,
        'present': present,
        'gap_count': len(gaps),
        'present_count': len(present),
        'gap_view_share': gap_views / max(total_search_views, 1),
    }


def analyze_all(search_data: dict, metadata: dict,
                top_n: int = 0) -> list:
    """Analyze all videos with search data."""
    results = []

    for video_id, terms in search_data.items():
        if not terms:
            continue

        meta = metadata.get(video_id, {})
        title = meta.get('title', video_id)

        description = find_description_for_video(video_id, title)
        if not description:
            logger.debug("No description found for %s (%s)", video_id, title[:40])
            continue

        result = analyze_video(video_id, terms, description, meta)
        if result['gaps']:
            results.append(result)

    # Sort by total gap impact
    results.sort(key=lambda x: sum(g['impact_score'] for g in x['gaps']), reverse=True)

    if top_n > 0:
        results = results[:top_n]

    return results


def find_channel_wide_gaps(results: list) -> list:
    """Find keywords that are gaps across multiple videos."""
    term_videos = defaultdict(list)

    for r in results:
        for gap in r['gaps']:
            term_videos[gap['term']].append({
                'video_id': r['video_id'],
                'title': r['title'],
                'views': gap['views'],
                'impact': gap['impact_score'],
            })

    # Multi-video gaps
    channel_gaps = []
    for term, videos in term_videos.items():
        if len(videos) >= 2:
            total_views = sum(v['views'] for v in videos)
            channel_gaps.append({
                'term': term,
                'video_count': len(videos),
                'total_views': total_views,
                'videos': videos,
            })

    channel_gaps.sort(key=lambda x: x['total_views'], reverse=True)
    return channel_gaps


def generate_report(results: list) -> str:
    """Generate the keyword gap analysis report."""
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d')

    lines = []
    lines.append("# Description Keyword Gap Analysis")
    lines.append("")
    lines.append(f"**Generated:** {now}")
    lines.append(f"**Videos analyzed:** {len(results)}")
    lines.append("")

    # Summary stats
    total_gaps = sum(r['gap_count'] for r in results)
    total_gap_views = sum(
        sum(g['views'] for g in r['gaps'])
        for r in results
    )
    lines.append(f"**Total keyword gaps found:** {total_gaps}")
    lines.append(f"**Total search views in gaps:** {total_gap_views}")
    lines.append("")

    # ---- Section 1: Per-Video Gaps ----
    lines.append("## 1. Per-Video Keyword Gaps")
    lines.append("")

    for r in results:
        if not r['gaps']:
            continue

        lines.append(f"### {r['title'][:70]}")
        lines.append(f"**Video ID:** `{r['video_id']}` | **Topic:** {r['topic_type']} | **Views:** {r['total_views']:,}")
        lines.append(f"**Search terms in description:** {r['present_count']} | **Missing:** {r['gap_count']}")
        lines.append("")

        # Show present terms
        if r['present']:
            present_str = ", ".join(
                f"`{p['term']}` ({p['views']}v)"
                for p in sorted(r['present'], key=lambda x: x['views'], reverse=True)[:5]
            )
            lines.append(f"**Already in description:** {present_str}")
            lines.append("")

        # Show gaps
        lines.append("| # | Missing Keyword | Search Views | Watch Time | Impact | Recommendation |")
        lines.append("|---|----------------|------------:|----------:|---------:|----------------|")

        for i, gap in enumerate(r['gaps'][:10], 1):
            wt_str = f"{gap['watch_time']:.1f}m"
            impact = "HIGH" if gap['impact_score'] > 5 else "MED" if gap['impact_score'] > 1 else "LOW"

            # Generate recommendation
            term_words = [w for w in gap['term'].split() if w.lower() not in STOP_WORDS]
            if len(term_words) >= 2:
                rec = f"Add \"{gap['term']}\" to description body"
            else:
                rec = f"Weave \"{gap['term']}\" into existing text"

            lines.append(
                f"| {i} | `{gap['term']}` | {gap['views']} | {wt_str} | {impact} | {rec} |"
            )

        lines.append("")

    # ---- Section 2: Channel-Wide Gaps ----
    channel_gaps = find_channel_wide_gaps(results)
    if channel_gaps:
        lines.append("## 2. Channel-Wide Keyword Gaps")
        lines.append("")
        lines.append("Keywords missing from multiple video descriptions.")
        lines.append("")
        lines.append("| # | Keyword | Videos Missing It | Total Search Views | Priority |")
        lines.append("|---|---------|------------------:|------------------:|----------|")

        for i, cg in enumerate(channel_gaps[:15], 1):
            video_names = ", ".join(v['title'][:30] for v in cg['videos'][:3])
            priority = "HIGH" if cg['total_views'] > 10 else "MED" if cg['total_views'] > 3 else "LOW"
            lines.append(
                f"| {i} | `{cg['term']}` | {cg['video_count']} | {cg['total_views']} | {priority} |"
            )

        lines.append("")

    # ---- Section 3: Best-Optimized Videos ----
    lines.append("## 3. Best-Optimized Videos (Fewest Gaps)")
    lines.append("")

    optimized = sorted(results, key=lambda x: x['gap_count'])
    lines.append("| Video | Present | Missing | Coverage |")
    lines.append("|-------|--------:|--------:|---------:|")
    for r in optimized[:10]:
        total = r['present_count'] + r['gap_count']
        coverage = r['present_count'] / max(total, 1) * 100
        lines.append(
            f"| {r['title'][:50]} | {r['present_count']} | {r['gap_count']} | {coverage:.0f}% |"
        )
    lines.append("")

    # ---- Interpreted Findings ----
    lines.append("## Interpreted Findings")
    lines.append("")

    if results:
        worst = results[0]
        lines.append(f"- **Biggest gap opportunity:** \"{worst['title'][:50]}\" — "
                     f"{worst['gap_count']} missing keywords generating "
                     f"{sum(g['views'] for g in worst['gaps'])} search views.")

    if channel_gaps:
        top_gap = channel_gaps[0]
        lines.append(f"- **Most common channel-wide gap:** `{top_gap['term']}` — "
                     f"missing from {top_gap['video_count']} videos, "
                     f"{top_gap['total_views']} total search views.")

    avg_coverage = sum(
        r['present_count'] / max(r['present_count'] + r['gap_count'], 1)
        for r in results
    ) / max(len(results), 1) * 100
    lines.append(f"- **Average keyword coverage:** {avg_coverage:.0f}% of search terms appear in descriptions.")
    lines.append(f"- **Actionable gaps:** Fix the HIGH-priority gaps first — "
                 f"these are real search queries that bring viewers but aren't in your description.")
    lines.append("")
    lines.append("---")
    lines.append(f"*Generated by `description_gap_filler.py` on {now}.*")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Description keyword gap filler — find missing high-value keywords"
    )
    parser.add_argument('--report', action='store_true',
                        help='Generate full channel analysis')
    parser.add_argument('--video', type=str,
                        help='Analyze a single video by ID')
    parser.add_argument('--project', type=str,
                        help='Analyze by project slug')
    parser.add_argument('--top', type=int, default=0,
                        help='Show only top N videos by gap impact')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-q', '--quiet', action='store_true')
    args = parser.parse_args()

    setup_logging(args.verbose, args.quiet)

    # Load data
    search_data = load_search_terms()
    if not search_data:
        print("No search term data. Run: python -m tools.youtube_analytics.search_term_analysis --report")
        sys.exit(1)

    metadata = load_video_metadata()

    if args.video:
        if args.video not in search_data:
            print(f"No search data for video {args.video}")
            sys.exit(1)
        meta = metadata.get(args.video, {'title': args.video})
        desc = find_description_for_video(args.video, meta.get('title', ''))
        if not desc:
            print(f"No description found for {args.video}")
            sys.exit(1)
        result = analyze_video(args.video, search_data[args.video], desc, meta)
        results = [result] if result['gaps'] else []
    elif args.project:
        # Find video ID for project
        from tools.youtube_analytics.script_srt_deviation import get_video_id_for_project
        vid = get_video_id_for_project(args.project)
        if not vid or vid not in search_data:
            print(f"No search data for project {args.project}")
            sys.exit(1)
        meta = metadata.get(vid, {'title': vid})
        desc = find_description_for_video(vid, meta.get('title', ''))
        if not desc:
            print(f"No description found for {vid}")
            sys.exit(1)
        result = analyze_video(vid, search_data[vid], desc, meta)
        results = [result] if result['gaps'] else []
    else:
        results = analyze_all(search_data, metadata, top_n=args.top)

    if not results:
        print("No keyword gaps found.")
        sys.exit(0)

    # Generate report
    report = generate_report(results)

    if args.report or not (args.video or args.project):
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_text(report, encoding='utf-8')
        print(f"Report saved to {REPORT_PATH}")

    # Cache results
    cache_data = []
    for r in results:
        cache_data.append({
            'video_id': r['video_id'],
            'title': r['title'],
            'gap_count': r['gap_count'],
            'gaps': [{'term': g['term'], 'views': g['views'], 'impact': g['impact_score']}
                     for g in r['gaps'][:10]],
        })
    with open(GAPS_CACHE, 'w', encoding='utf-8') as f:
        json.dump(cache_data, f, indent=2)

    # Print summary
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    print(report)


if __name__ == '__main__':
    main()
