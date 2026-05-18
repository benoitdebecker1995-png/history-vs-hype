"""
Cross-Video Comment Engagement Analysis Tool

Fetches top comments for all long-form videos and performs aggregate analysis:
engagement rates, topic requests, questions, sentiment, recurring commenters,
and engagement by topic type.

Data sources:
  - analytics.db (videos table for metadata)
  - YouTube Data API v3 (commentThreads endpoint)
  - _comment_data.json (cached comment data)

Usage:
    python -m tools.youtube_analytics.comment_analysis --report      # Full report
    python -m tools.youtube_analytics.comment_analysis --fetch       # Fetch fresh data
    python -m tools.youtube_analytics.comment_analysis --cached      # Report from cache only
    python -m tools.youtube_analytics.comment_analysis --video ID    # Single video
    python -m tools.youtube_analytics.comment_analysis --verbose     # Debug logging

Output:
    channel-data/patterns/COMMENT-ENGAGEMENT-ANALYSIS.md
"""

import sys
import json
import re
import sqlite3
import argparse
import time
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict
from typing import Dict, List, Any, Optional

from tools.logging_config import get_logger, setup_logging

logger = get_logger(__name__)

try:
    from googleapiclient.errors import HttpError
except ImportError:
    HttpError = Exception

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ANALYTICS_DB = Path(__file__).parent / 'analytics.db'
COMMENT_JSON = Path(__file__).parent / '_comment_data.json'
REPORT_PATH = PROJECT_ROOT / 'channel-data' / 'patterns' / 'COMMENT-ENGAGEMENT-ANALYSIS.md'

# Sentiment keywords
POSITIVE_KEYWORDS = [
    'great', 'amazing', 'excellent', 'love', 'best', 'fantastic',
    'learned', 'subscribed', 'wonderful', 'brilliant', 'awesome',
    'informative', 'well researched', 'well-researched', 'thank you',
    'thanks', 'incredible', 'fascinating', 'underrated', 'quality',
]

NEGATIVE_KEYWORDS = [
    'wrong', 'incorrect', 'disagree', 'bad', 'terrible', 'misleading',
    'biased', 'propaganda', 'disappointed', 'inaccurate', 'boring',
    'waste', 'clickbait', 'misinformation',
]

# Topic request patterns
REQUEST_PATTERNS = [
    r'\b(?:you should|can you|could you|please do|would love to see)\b',
    r'\b(?:video (?:about|on)|make a video|do a video|cover(?:ing)?)\b',
    r'\b(?:next (?:video|topic|time)|suggestion|recommend)\b',
    r'\b(?:would be (?:great|cool|interesting) (?:to|if))\b',
]

# Question patterns
QUESTION_STARTS = [
    'what', 'why', 'how', 'when', 'where', 'who', 'which',
    'can', 'could', 'would', 'is', 'are', 'do', 'does', 'did',
    'will', 'should', 'have', 'has', 'was', 'were',
]


# =========================================================================
# DATA LOADING
# =========================================================================

def load_video_metadata() -> Dict[str, dict]:
    """Load video metadata from analytics.db (long-form only)."""
    if not ANALYTICS_DB.exists():
        logger.warning("analytics.db not found at %s", ANALYTICS_DB)
        return {}

    from tools.youtube_analytics.store import AnalyticsStore
    with AnalyticsStore.open(ANALYTICS_DB) as store:
        rows = store.videos(min_duration_seconds=61)  # preserve old `> 60`

    keep = ('video_id', 'title', 'published_at', 'duration_seconds',
            'views', 'topic_type', 'comments', 'likes')
    result = {r['video_id']: {k: r[k] for k in keep} for r in rows}

    logger.info("Loaded metadata for %d long-form videos", len(result))
    return result


def load_comments_from_json() -> Dict[str, List[dict]]:
    """Load cached comment data from JSON file."""
    if not COMMENT_JSON.exists():
        logger.warning("No comment cache found at %s", COMMENT_JSON)
        return {}

    with open(COMMENT_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total = sum(len(v) for v in data.values())
    logger.info("Loaded %d comments for %d videos from cache", total, len(data))
    return data


def save_comments_json(data: Dict[str, List[dict]]) -> None:
    """Save comment data to JSON cache."""
    with open(COMMENT_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    total = sum(len(v) for v in data.values())
    logger.info("Saved %d comments for %d videos to %s", total, len(data), COMMENT_JSON)


# =========================================================================
# API FETCH
# =========================================================================

def fetch_comments_for_video(youtube, video_id: str, max_results: int = 100) -> Optional[List[dict]]:
    """
    Fetch top comments for a single video via Data API v3.

    Returns list of comment dicts on success, None on error (e.g., disabled comments).
    """
    try:
        response = youtube.commentThreads().list(
            videoId=video_id,
            part='snippet',
            maxResults=min(max_results, 100),
            order='relevance',
            textFormat='plainText',
        ).execute()

        comments = []
        for item in response.get('items', []):
            snippet = item['snippet']['topLevelComment']['snippet']
            comments.append({
                'text': snippet.get('textDisplay', ''),
                'likes': snippet.get('likeCount', 0),
                'published_at': snippet.get('publishedAt', ''),
                'author': snippet.get('authorDisplayName', ''),
            })

        return comments

    except HttpError as e:
        status_code = e.resp.status if hasattr(e, 'resp') else None
        error_str = str(e)

        if status_code == 403 and 'commentsDisabled' in error_str:
            logger.info("  Comments disabled for %s — skipping", video_id)
            return None
        elif status_code == 403:
            logger.warning("  403 for %s (quota or permission): %s", video_id, error_str[:120])
            return None
        elif status_code == 404:
            logger.warning("  404 for %s — video not found", video_id)
            return None
        else:
            logger.warning("  API error for %s (HTTP %s): %s", video_id, status_code, error_str[:120])
            return None

    except Exception as e:
        logger.warning("  Unexpected error for %s: %s", video_id, e)
        return None


def fetch_all_comments(video_ids: Optional[List[str]] = None) -> Dict[str, List[dict]]:
    """
    Fetch comments for all (or specified) videos.

    Rate-limits with 0.2s sleep between API calls to respect Data API quotas.
    """
    from tools.youtube_analytics.auth import get_authenticated_service

    youtube = get_authenticated_service('youtube', 'v3')

    if video_ids is None:
        metadata = load_video_metadata()
        video_ids = list(metadata.keys())

    logger.info("Fetching comments for %d videos from API...", len(video_ids))
    result = {}
    skipped = 0

    for i, vid_id in enumerate(video_ids):
        comments = fetch_comments_for_video(youtube, vid_id)

        if comments is not None:
            result[vid_id] = comments
            logger.debug("  %s: %d comments", vid_id, len(comments))
        else:
            skipped += 1

        if (i + 1) % 10 == 0:
            logger.info("  Fetched %d/%d videos (%d skipped)", i + 1, len(video_ids), skipped)

        # Rate limit: Data API v3 has stricter quotas than Analytics API
        time.sleep(0.2)

    logger.info("Fetched comments for %d videos (%d skipped)", len(result), skipped)
    return result


# =========================================================================
# ANALYSIS FUNCTIONS
# =========================================================================

def compute_engagement_rates(
    comment_data: Dict[str, List[dict]],
    metadata: Dict[str, dict],
) -> List[dict]:
    """
    Compute comments per 1000 views for each video, sorted descending.

    Returns list of dicts with video_id, title, comments, views,
    engagement_rate, topic_type.
    """
    rates = []

    for vid_id, comments in comment_data.items():
        meta = metadata.get(vid_id)
        if not meta:
            continue

        views = meta.get('views', 0) or 0
        if views == 0:
            continue

        rate = len(comments) / views * 1000

        rates.append({
            'video_id': vid_id,
            'title': meta.get('title', vid_id),
            'comment_count': len(comments),
            'views': views,
            'engagement_rate': rate,
            'topic_type': meta.get('topic_type', 'general'),
        })

    rates.sort(key=lambda x: x['engagement_rate'], reverse=True)
    return rates


def extract_topic_requests(comment_data: Dict[str, List[dict]]) -> List[dict]:
    """
    Scan comments for topic requests (viewers asking for specific videos).

    Returns list of dicts with text, likes, video_id, author.
    Sorted by likes descending (highest-demand requests first).
    """
    requests = []
    compiled = [re.compile(p, re.IGNORECASE) for p in REQUEST_PATTERNS]

    for vid_id, comments in comment_data.items():
        for comment in comments:
            text = comment.get('text', '')
            text_lower = text.lower()

            for pattern in compiled:
                if pattern.search(text_lower):
                    requests.append({
                        'text': text[:300],  # Truncate long comments
                        'likes': comment.get('likes', 0),
                        'video_id': vid_id,
                        'author': comment.get('author', ''),
                    })
                    break  # Don't double-count

    requests.sort(key=lambda x: x['likes'], reverse=True)
    return requests


def extract_questions(comment_data: Dict[str, List[dict]]) -> List[dict]:
    """
    Find comments that are questions.

    Detects: ends with ?, or starts with question words.
    Returns sorted by likes descending.
    """
    questions = []

    for vid_id, comments in comment_data.items():
        for comment in comments:
            text = comment.get('text', '').strip()
            if not text:
                continue

            is_question = False

            # Ends with question mark
            if '?' in text:
                is_question = True
            else:
                # Starts with question word
                first_word = text.split()[0].lower() if text.split() else ''
                if first_word in QUESTION_STARTS:
                    is_question = True

            if is_question:
                questions.append({
                    'text': text[:300],
                    'likes': comment.get('likes', 0),
                    'video_id': vid_id,
                    'author': comment.get('author', ''),
                })

    questions.sort(key=lambda x: x['likes'], reverse=True)
    return questions


def analyze_sentiment_simple(comment_data: Dict[str, List[dict]], metadata: Dict[str, dict]) -> List[dict]:
    """
    Simple keyword-based sentiment for each video.

    Returns list of dicts with video_id, title, positive_pct, negative_pct,
    neutral_pct, total_comments.
    """
    results = []

    for vid_id, comments in comment_data.items():
        meta = metadata.get(vid_id)
        if not meta or not comments:
            continue

        positive = 0
        negative = 0
        neutral = 0

        for comment in comments:
            text = comment.get('text', '').lower()

            has_positive = any(kw in text for kw in POSITIVE_KEYWORDS)
            has_negative = any(kw in text for kw in NEGATIVE_KEYWORDS)

            if has_positive and not has_negative:
                positive += 1
            elif has_negative and not has_positive:
                negative += 1
            elif has_positive and has_negative:
                # Mixed — count as neutral
                neutral += 1
            else:
                neutral += 1

        total = positive + negative + neutral
        if total == 0:
            continue

        results.append({
            'video_id': vid_id,
            'title': meta.get('title', vid_id),
            'positive_pct': positive / total * 100,
            'negative_pct': negative / total * 100,
            'neutral_pct': neutral / total * 100,
            'positive': positive,
            'negative': negative,
            'neutral': neutral,
            'total': total,
        })

    results.sort(key=lambda x: x['positive_pct'], reverse=True)
    return results


def find_recurring_commenters(comment_data: Dict[str, List[dict]]) -> List[dict]:
    """
    Find authors who comment on multiple videos (loyal audience).

    Returns list of dicts with author, video_count, total_likes, video_ids.
    Sorted by video_count descending.
    """
    author_map: Dict[str, dict] = defaultdict(lambda: {
        'video_ids': set(),
        'total_likes': 0,
        'comment_count': 0,
    })

    for vid_id, comments in comment_data.items():
        for comment in comments:
            author = comment.get('author', '').strip()
            if not author:
                continue

            author_map[author]['video_ids'].add(vid_id)
            author_map[author]['total_likes'] += comment.get('likes', 0)
            author_map[author]['comment_count'] += 1

    # Filter to 2+ videos and convert sets to lists for JSON compatibility
    recurring = []
    for author, data in author_map.items():
        if len(data['video_ids']) >= 2:
            recurring.append({
                'author': author,
                'video_count': len(data['video_ids']),
                'comment_count': data['comment_count'],
                'total_likes': data['total_likes'],
                'video_ids': sorted(data['video_ids']),
            })

    recurring.sort(key=lambda x: x['video_count'], reverse=True)
    return recurring


def engagement_by_topic_type(
    comment_data: Dict[str, List[dict]],
    metadata: Dict[str, dict],
) -> List[dict]:
    """
    Average comments per 1000 views by topic type.

    Returns list of dicts with topic_type, n, avg_engagement, total_comments.
    Sorted by avg_engagement descending.
    """
    topic_groups: Dict[str, dict] = defaultdict(lambda: {
        'rates': [],
        'total_comments': 0,
    })

    for vid_id, comments in comment_data.items():
        meta = metadata.get(vid_id)
        if not meta:
            continue

        views = meta.get('views', 0) or 0
        if views == 0:
            continue

        topic = meta.get('topic_type', 'general') or 'general'
        rate = len(comments) / views * 1000

        topic_groups[topic]['rates'].append(rate)
        topic_groups[topic]['total_comments'] += len(comments)

    results = []
    for topic, data in topic_groups.items():
        if not data['rates']:
            continue

        results.append({
            'topic_type': topic,
            'n': len(data['rates']),
            'avg_engagement': sum(data['rates']) / len(data['rates']),
            'total_comments': data['total_comments'],
        })

    results.sort(key=lambda x: x['avg_engagement'], reverse=True)
    return results


# =========================================================================
# REPORT GENERATION
# =========================================================================

def generate_report(
    comment_data: Dict[str, List[dict]],
    metadata: Dict[str, dict],
) -> str:
    """Generate the full comment engagement analysis report."""

    # Filter to videos with both comment data and metadata
    common_ids = set(comment_data.keys()) & set(metadata.keys())
    filtered = {k: v for k, v in comment_data.items() if k in common_ids}

    if not filtered:
        return ("# Comment Engagement Analysis\n\n"
                "No data available. Run with --fetch to pull comments from API.")

    now = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    total_comments = sum(len(v) for v in filtered.values())

    lines = []
    lines.append("# Comment Engagement Analysis")
    lines.append("")
    lines.append(f"**Generated:** {now}")
    lines.append(f"**Videos analyzed:** {len(filtered)} | **Total comments fetched:** {total_comments:,}")
    lines.append("")

    # ---- Section 1: Engagement Rate Ranking ----
    lines.append("## 1. Engagement Rate Ranking")
    lines.append("")
    lines.append("Comments per 1,000 views — measures how much a video provokes discussion.")
    lines.append("")

    rates = compute_engagement_rates(filtered, metadata)
    lines.append("| # | Title | Comments | Views | Comments/1K Views | Topic |")
    lines.append("|---|-------|--------:|------:|------------------:|-------|")

    for i, r in enumerate(rates, 1):
        title_short = r['title'][:50] + ('...' if len(r['title']) > 50 else '')
        lines.append(
            f"| {i} | {title_short} | {r['comment_count']} "
            f"| {r['views']:,} | {r['engagement_rate']:.2f} | {r['topic_type']} |"
        )
    lines.append("")

    if rates:
        avg_rate = sum(r['engagement_rate'] for r in rates) / len(rates)
        lines.append(f"**Channel average:** {avg_rate:.2f} comments/1K views")
        lines.append("")

    # ---- Section 2: Engagement by Topic Type ----
    lines.append("## 2. Engagement by Topic Type")
    lines.append("")

    topic_data = engagement_by_topic_type(filtered, metadata)
    lines.append("| Topic Type | n | Avg Comments/1K Views | Total Comments |")
    lines.append("|------------|---|---------------------:|---------------:|")

    for t in topic_data:
        lines.append(
            f"| {t['topic_type']} | {t['n']} "
            f"| {t['avg_engagement']:.2f} | {t['total_comments']:,} |"
        )
    lines.append("")

    # ---- Section 3: Viewer-Requested Topics ----
    lines.append("## 3. Viewer-Requested Topics")
    lines.append("")
    lines.append("Topics viewers are asking for (demand signal from comments).")
    lines.append("")

    requests = extract_topic_requests(filtered)
    if requests:
        # Show top 20
        for i, req in enumerate(requests[:20], 1):
            likes_str = f" ({req['likes']} likes)" if req['likes'] > 0 else ""
            lines.append(f"{i}. \"{req['text']}\"{likes_str}")
        lines.append("")
        lines.append(f"*{len(requests)} total topic requests found across all videos.*")
    else:
        lines.append("No topic requests detected.")
    lines.append("")

    # ---- Section 4: Common Questions ----
    lines.append("## 4. Common Questions")
    lines.append("")
    lines.append("Questions viewers ask (FAQ material for future videos or pinned comments).")
    lines.append("")

    questions = extract_questions(filtered)
    if questions:
        # Show top 20 by likes
        for i, q in enumerate(questions[:20], 1):
            likes_str = f" ({q['likes']} likes)" if q['likes'] > 0 else ""
            text_short = q['text'][:200] + ('...' if len(q['text']) > 200 else '')
            lines.append(f"{i}. \"{text_short}\"{likes_str}")
        lines.append("")
        lines.append(f"*{len(questions)} total questions found across all videos.*")
    else:
        lines.append("No questions detected.")
    lines.append("")

    # ---- Section 5: Sentiment Overview ----
    lines.append("## 5. Sentiment Overview")
    lines.append("")
    lines.append("Simple keyword-based sentiment (positive/negative/neutral).")
    lines.append("")

    sentiment = analyze_sentiment_simple(filtered, metadata)
    lines.append("| Video | Positive % | Negative % | Neutral % | Comments |")
    lines.append("|-------|----------:|----------:|---------:|--------:|")

    for s in sentiment:
        title_short = s['title'][:45] + ('...' if len(s['title']) > 45 else '')
        lines.append(
            f"| {title_short} | {s['positive_pct']:.0f}% "
            f"| {s['negative_pct']:.0f}% | {s['neutral_pct']:.0f}% | {s['total']} |"
        )
    lines.append("")

    if sentiment:
        avg_pos = sum(s['positive_pct'] for s in sentiment) / len(sentiment)
        avg_neg = sum(s['negative_pct'] for s in sentiment) / len(sentiment)
        lines.append(f"**Channel average:** {avg_pos:.0f}% positive, {avg_neg:.0f}% negative")
        lines.append("")

    # ---- Section 6: Recurring Commenters ----
    lines.append("## 6. Recurring Commenters (Loyal Audience)")
    lines.append("")

    recurring = find_recurring_commenters(filtered)
    loyal = [r for r in recurring if r['video_count'] >= 3]
    regular = [r for r in recurring if r['video_count'] == 2]

    if loyal:
        lines.append(f"**Loyal commenters (3+ videos):** {len(loyal)}")
        lines.append("")
        lines.append("| Author | Videos | Comments | Total Likes |")
        lines.append("|--------|-------:|--------:|------------:|")
        for r in loyal[:25]:
            lines.append(
                f"| {r['author']} | {r['video_count']} "
                f"| {r['comment_count']} | {r['total_likes']} |"
            )
        lines.append("")

    lines.append(f"**Regular commenters (2 videos):** {len(regular)}")
    lines.append(f"**Total unique recurring commenters:** {len(recurring)}")
    lines.append("")

    # ---- Section 7: Interpreted Findings ----
    lines.append("## Interpreted Findings")
    lines.append("")

    findings = _generate_findings(rates, topic_data, requests, questions, sentiment, recurring)
    for finding in findings:
        lines.append(f"- {finding}")
    lines.append("")

    # Footer
    lines.append("---")
    lines.append(f"*Generated by `comment_analysis.py` on {now}. "
                 f"Data covers {len(filtered)} long-form videos, {total_comments:,} comments.*")

    return "\n".join(lines)


def _generate_findings(
    rates: List[dict],
    topic_data: List[dict],
    requests: List[dict],
    questions: List[dict],
    sentiment: List[dict],
    recurring: List[dict],
) -> List[str]:
    """Generate actionable findings from the analysis."""
    findings = []

    # Engagement insight
    if rates:
        avg_rate = sum(r['engagement_rate'] for r in rates) / len(rates)
        top = rates[0]
        findings.append(
            f"**Highest engagement:** \"{top['title'][:50]}\" at "
            f"{top['engagement_rate']:.2f} comments/1K views "
            f"(channel avg: {avg_rate:.2f})."
        )

    # Topic type insight
    if len(topic_data) >= 2:
        best = topic_data[0]
        worst = topic_data[-1]
        findings.append(
            f"**Most discussed topic type:** {best['topic_type']} "
            f"({best['avg_engagement']:.2f} comments/1K views, n={best['n']}). "
            f"Least: {worst['topic_type']} ({worst['avg_engagement']:.2f})."
        )

    # Topic requests insight
    if requests:
        high_demand = [r for r in requests if r['likes'] >= 3]
        findings.append(
            f"**{len(requests)} topic requests found** in comments "
            f"({len(high_demand)} with 3+ likes = strong demand signals)."
        )

    # Questions insight
    if questions:
        findings.append(
            f"**{len(questions)} viewer questions found.** "
            f"Top questions by likes could inform FAQ pinned comments or follow-up videos."
        )

    # Sentiment insight
    if sentiment:
        avg_pos = sum(s['positive_pct'] for s in sentiment) / len(sentiment)
        avg_neg = sum(s['negative_pct'] for s in sentiment) / len(sentiment)
        findings.append(
            f"**Sentiment ratio:** {avg_pos:.0f}% positive vs {avg_neg:.0f}% negative. "
            + ("Healthy ratio — audience is receptive." if avg_pos > avg_neg * 3
               else "Monitor negative feedback for content adjustments.")
        )

    # Loyal audience insight
    loyal = [r for r in recurring if r['video_count'] >= 3]
    if loyal:
        findings.append(
            f"**{len(loyal)} loyal commenters** (3+ videos). "
            f"These are community advocates — consider engaging directly."
        )

    return findings


def generate_db_only_report(metadata: Dict[str, dict]) -> str:
    """Generate a comment engagement report using only DB comment counts (no API text)."""
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d')

    lines = []
    lines.append("# Comment Engagement Analysis (DB-Only Mode)")
    lines.append("")
    lines.append(f"**Generated:** {now}")
    lines.append(f"**Videos analyzed:** {len(metadata)}")
    lines.append("**Mode:** DB-only (comment text not available -- YouTube Data API commentThreads scope not enabled)")
    lines.append("")
    lines.append("> To get full comment text analysis, enable the YouTube Data API v3 in your Google Cloud project")
    lines.append("> and add `https://www.googleapis.com/auth/youtube.force-ssl` to the OAuth scopes in `auth.py`.")
    lines.append("")

    # 1. Engagement rate ranking
    lines.append("## 1. Engagement Rate Ranking")
    lines.append("")
    lines.append("| # | Title | Comments | Views | Comments/1K Views | Topic |")
    lines.append("|---|-------|--------:|------:|------------------:|-------|")

    ranked = []
    for vid_id, meta in metadata.items():
        views = meta.get('views', 0) or 0
        comments = meta.get('comments', 0) or 0
        if views > 0:
            rate = comments / views * 1000
            ranked.append({
                'video_id': vid_id,
                'title': meta.get('title', vid_id),
                'comments': comments,
                'views': views,
                'rate': rate,
                'topic_type': meta.get('topic_type', 'general'),
            })

    ranked.sort(key=lambda x: x['rate'], reverse=True)
    for i, v in enumerate(ranked[:25], 1):
        title_short = v['title'][:55] + ('...' if len(v['title']) > 55 else '')
        lines.append(
            f"| {i} | {title_short} | {v['comments']} | {v['views']:,} "
            f"| {v['rate']:.2f} | {v['topic_type']} |"
        )
    lines.append("")

    # 2. Engagement by topic type
    lines.append("## 2. Engagement by Topic Type")
    lines.append("")
    lines.append("| Topic Type | n | Total Comments | Total Views | Avg Comments/1K Views |")
    lines.append("|-----------|--:|-------------:|----------:|--------------------:|")

    from collections import defaultdict
    topic_stats = defaultdict(lambda: {'count': 0, 'comments': 0, 'views': 0})
    for v in ranked:
        t = topic_stats[v['topic_type']]
        t['count'] += 1
        t['comments'] += v['comments']
        t['views'] += v['views']

    for topic, s in sorted(topic_stats.items(), key=lambda x: x[1]['views'], reverse=True):
        avg_rate = s['comments'] / s['views'] * 1000 if s['views'] > 0 else 0
        lines.append(
            f"| {topic} | {s['count']} | {s['comments']} | {s['views']:,} | {avg_rate:.2f} |"
        )
    lines.append("")

    # 3. Correlation: comments vs subscribers
    lines.append("## 3. Comments vs Subscriber Conversion")
    lines.append("")
    high_eng = [v for v in ranked if v['rate'] >= 3.0]
    low_eng = [v for v in ranked if v['rate'] < 3.0]

    if high_eng and low_eng:
        from statistics import mean
        avg_views_high = mean(v['views'] for v in high_eng)
        avg_views_low = mean(v['views'] for v in low_eng)
        lines.append(f"- **High engagement** (>=3 comments/1K views): {len(high_eng)} videos, avg {avg_views_high:,.0f} views")
        lines.append(f"- **Low engagement** (<3 comments/1K views): {len(low_eng)} videos, avg {avg_views_low:,.0f} views")
    lines.append("")

    # Interpreted findings
    lines.append("## Interpreted Findings")
    lines.append("")

    if ranked:
        best = ranked[0]
        lines.append(f"- **Highest engagement:** \"{best['title'][:50]}\" at {best['rate']:.1f} comments/1K views ({best['topic_type']})")

    # Topic comparison
    topic_rates = {t: s['comments']/s['views']*1000 for t, s in topic_stats.items() if s['views'] > 0}
    if topic_rates:
        best_topic = max(topic_rates, key=topic_rates.get)
        worst_topic = min(topic_rates, key=topic_rates.get)
        lines.append(f"- **{best_topic}** generates the most discussion ({topic_rates[best_topic]:.1f} comments/1K views)")
        lines.append(f"- **{worst_topic}** generates the least ({topic_rates[worst_topic]:.1f} comments/1K views)")

    avg_rate = sum(v['rate'] for v in ranked) / len(ranked) if ranked else 0
    lines.append(f"- **Channel average:** {avg_rate:.1f} comments/1K views")
    lines.append("")
    lines.append("## Limitations")
    lines.append("")
    lines.append("- Comment TEXT not available (API scope not enabled) -- cannot extract topic requests, questions, or sentiment")
    lines.append("- To unlock full analysis: enable YouTube Data API v3 and add `youtube.force-ssl` scope to `auth.py` SCOPES")

    return "\n".join(lines)


def single_video_report(
    video_id: str,
    comment_data: Dict[str, List[dict]],
    metadata: Dict[str, dict],
) -> str:
    """Generate a comment analysis for a single video."""
    comments = comment_data.get(video_id)
    meta = metadata.get(video_id)

    if not comments:
        return f"No comment data found for {video_id}. Run with --fetch."

    title = meta.get('title', video_id) if meta else video_id
    views = meta.get('views', 0) if meta else 0

    lines = []
    lines.append(f"# Comment Analysis: {title}")
    lines.append("")
    lines.append(f"- **Comments fetched:** {len(comments)}")
    if views:
        rate = len(comments) / views * 1000
        lines.append(f"- **Views:** {views:,}")
        lines.append(f"- **Engagement rate:** {rate:.2f} comments/1K views")
    lines.append("")

    # Top comments by likes
    sorted_comments = sorted(comments, key=lambda c: c.get('likes', 0), reverse=True)
    lines.append("## Top Comments (by likes)")
    lines.append("")
    for i, c in enumerate(sorted_comments[:10], 1):
        text_short = c['text'][:150].replace('\n', ' ')
        lines.append(f"{i}. ({c['likes']} likes) \"{text_short}\"")
    lines.append("")

    # Questions from this video
    vid_questions = []
    for c in comments:
        if '?' in c.get('text', ''):
            vid_questions.append(c)

    if vid_questions:
        lines.append(f"## Questions ({len(vid_questions)})")
        lines.append("")
        for q in sorted(vid_questions, key=lambda x: x.get('likes', 0), reverse=True)[:10]:
            text_short = q['text'][:150].replace('\n', ' ')
            lines.append(f"- ({q['likes']} likes) \"{text_short}\"")
        lines.append("")

    # Sentiment
    positive = sum(1 for c in comments if any(kw in c.get('text', '').lower() for kw in POSITIVE_KEYWORDS))
    negative = sum(1 for c in comments if any(kw in c.get('text', '').lower() for kw in NEGATIVE_KEYWORDS))
    neutral = len(comments) - positive - negative
    total = len(comments)

    lines.append("## Sentiment")
    lines.append("")
    lines.append(f"- Positive: {positive} ({positive/total*100:.0f}%)" if total else "- Positive: 0")
    lines.append(f"- Negative: {negative} ({negative/total*100:.0f}%)" if total else "- Negative: 0")
    lines.append(f"- Neutral: {neutral} ({neutral/total*100:.0f}%)" if total else "- Neutral: 0")

    return "\n".join(lines)


# =========================================================================
# CLI
# =========================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Cross-video comment engagement analysis.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python -m tools.youtube_analytics.comment_analysis --report
  python -m tools.youtube_analytics.comment_analysis --fetch --report
  python -m tools.youtube_analytics.comment_analysis --cached --report
  python -m tools.youtube_analytics.comment_analysis --video dQw4w9WgXcQ""",
    )
    parser.add_argument('--report', action='store_true',
                        help='Generate full report to channel-data/patterns/')
    parser.add_argument('--fetch', action='store_true',
                        help='Fetch fresh comment data from YouTube Data API v3')
    parser.add_argument('--cached', action='store_true',
                        help='Use cached data only (no API calls)')
    parser.add_argument('--video', type=str, default=None,
                        help='Single video ID for detailed breakdown')

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument('--verbose', '-v', action='store_true',
                           help='Verbose logging')
    verbosity.add_argument('--quiet', '-q', action='store_true',
                           help='Suppress info logging')

    args = parser.parse_args()
    setup_logging(args.verbose, args.quiet)

    # Default to --report if no action specified
    if not args.report and not args.fetch and not args.video:
        args.report = True

    # Load metadata
    metadata = load_video_metadata()
    if not metadata:
        logger.error("No video metadata found in analytics.db. Run backfill first.")
        sys.exit(1)

    # Fetch or load comment data
    if args.fetch:
        logger.info("Fetching comments from YouTube Data API v3...")
        video_ids = [args.video] if args.video else None
        fresh_data = fetch_all_comments(video_ids)

        if fresh_data:
            # Merge with existing cache
            existing = load_comments_from_json()
            existing.update(fresh_data)
            save_comments_json(existing)
            comment_data = existing
        else:
            logger.warning("No comments fetched. Falling back to cache.")
            comment_data = load_comments_from_json()
    else:
        comment_data = load_comments_from_json()

    if not comment_data:
        logger.warning("No comment data available. Generating DB-only report from comment counts.")
        if args.report:
            report = generate_db_only_report(metadata)
            REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(REPORT_PATH, 'w', encoding='utf-8') as f:
                f.write(report)
            logger.info("Report saved to %s", REPORT_PATH)
            print(report)
        else:
            logger.error("No comment data. Run with --fetch (requires YouTube Data API v3 commentThreads scope).")
        return

    logger.info("Comment data: %d videos. Metadata: %d videos.", len(comment_data), len(metadata))

    # Single video mode
    if args.video:
        report = single_video_report(args.video, comment_data, metadata)
        print(report)
        return

    # Full report mode
    if args.report:
        report = generate_report(comment_data, metadata)

        # Save to file
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(REPORT_PATH, 'w', encoding='utf-8') as f:
            f.write(report)
        logger.info("Report saved to %s", REPORT_PATH)

        # Also print to stdout (handle Windows cp1252 encoding)
        import sys
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        print(report)


if __name__ == '__main__':
    main()
