"""
YouTube Video Comments Fetcher and Categorizer

Fetches comments from a video using YouTube Data API v3 and categorizes them
into Questions, Objections, Requests, and Other.

Usage:
    CLI:
        python comments.py VIDEO_ID
        python comments.py VIDEO_ID --max-comments 50

    Python:
        from comments import fetch_and_categorize_comments

        result = fetch_and_categorize_comments('VIDEO_ID')
        print(result['categories']['questions'])
        print(result['category_counts'])

Returns:
    JSON dict with categorized comments on success:
        {
            "video_id": "...",
            "total_fetched": int,
            "categories": {
                "questions": [...],
                "objections": [...],
                "requests": [...],
                "other": [...]
            },
            "category_counts": {"questions": N, "objections": N, ...},
            "fetched_at": "ISO timestamp"
        }

    dict with error on failure:
        {"error": "Error message", "video_id": "..."}

Dependencies:
    - auth.py (Phase 7) for OAuth2 authentication
    - google-api-python-client
"""

import sys
import json
import re
from datetime import datetime

from auth import get_authenticated_service

try:
    from googleapiclient.errors import HttpError
except ImportError:
    HttpError = Exception


def fetch_video_comments(video_id: str, max_comments: int = 100) -> list[dict] | dict:
    """
    Fetch comments for a video with pagination.

    Uses YouTube Data API v3 commentThreads.list() endpoint.
    Comments are returned sorted by relevance (top comments by likes/replies first).

    Args:
        video_id: YouTube video ID (e.g., 'dQw4w9WgXcQ')
        max_comments: Maximum comments to fetch (default 100, max 100 per API call)

    Returns:
        list of comment dicts on success:
            [
                {
                    "text": "Comment content...",
                    "author": "Username",
                    "likes": int,
                    "published_at": "ISO timestamp",
                    "reply_count": int
                },
                ...
            ]

        dict with error on failure:
            {"error": "Error message", "video_id": "..."}
    """
    try:
        youtube = get_authenticated_service('youtube', 'v3')
        comments = []
        next_page_token = None

        while len(comments) < max_comments:
            # Calculate how many to fetch this iteration
            remaining = max_comments - len(comments)
            fetch_count = min(100, remaining)  # API max is 100 per call

            request = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=fetch_count,
                order='relevance',  # Top comments by likes/replies first
                textFormat='plainText',
                pageToken=next_page_token
            )
            response = request.execute()

            for item in response.get('items', []):
                snippet = item['snippet']['topLevelComment']['snippet']
                comments.append({
                    'text': snippet['textDisplay'],
                    'author': snippet['authorDisplayName'],
                    'likes': snippet.get('likeCount', 0),
                    'published_at': snippet['publishedAt'],
                    'reply_count': item['snippet'].get('totalReplyCount', 0)
                })

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break  # No more pages

        return comments

    except HttpError as e:
        status_code = e.resp.status if hasattr(e, 'resp') else None

        if status_code == 403:
            # Check if comments are disabled
            error_reason = str(e)
            if 'commentsDisabled' in error_reason:
                return {
                    'error': 'Comments are disabled for this video',
                    'video_id': video_id
                }
            return {
                'error': 'API quota exceeded or permission denied',
                'video_id': video_id,
                'details': str(e)
            }
        elif status_code == 404:
            return {
                'error': 'Video not found',
                'video_id': video_id
            }
        else:
            return {
                'error': f'API error (HTTP {status_code})',
                'video_id': video_id,
                'details': str(e)
            }

    except Exception as e:
        return {
            'error': f'Unexpected error: {type(e).__name__}',
            'video_id': video_id,
            'details': str(e)
        }


def categorize_comments(comments: list[dict]) -> dict[str, list[dict]]:
    """
    Categorize comments into Questions, Objections, Requests, and Other.

    Uses keyword matching as a heuristic. This provides initial categorization
    that can be refined by Claude for more nuanced analysis.

    Categories:
        - questions: Comments with questions (? or question words)
        - objections: Comments expressing disagreement or corrections
        - requests: Comments requesting new content or topics
        - other: Everything else (praise, general discussion, etc.)

    Args:
        comments: List of comment dicts from fetch_video_comments()

    Returns:
        dict with categorized comments:
            {
                "questions": [...],
                "objections": [...],
                "requests": [...],
                "other": [...]
            }
    """
    categories = {
        'questions': [],
        'objections': [],
        'requests': [],
        'other': []
    }

    # Question patterns: question marks, question words at start
    question_patterns = [
        r'\?',  # Contains question mark
        r'^(what|why|how|when|where|who|can|could|would|is|are|do|does|did|will|should|have|has)\b',
    ]

    # Objection patterns: disagreement, corrections
    objection_patterns = [
        r'\b(wrong|incorrect|false|misleading|disagree|actually|mistake|error|inaccurate)\b',
        r'\b(not true|don\'t think|doesn\'t make sense|that\'s not)\b',
    ]

    # Request patterns: asking for content
    request_patterns = [
        r'\b(please|could you|can you|would you|video on|video about)\b',
        r'\b(cover|make a video|do a video|more on|next time|suggestion|recommend|topic|idea)\b',
    ]

    for comment in comments:
        text = comment['text'].lower()
        categorized = False

        # Check questions first (most common actionable category)
        for pattern in question_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                categories['questions'].append(comment)
                categorized = True
                break

        if categorized:
            continue

        # Check objections (important for fact-checking channel)
        for pattern in objection_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                categories['objections'].append(comment)
                categorized = True
                break

        if categorized:
            continue

        # Check requests
        for pattern in request_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                categories['requests'].append(comment)
                categorized = True
                break

        if not categorized:
            categories['other'].append(comment)

    return categories


def fetch_and_categorize_comments(video_id: str, max_comments: int = 100) -> dict:
    """
    Main entry point: fetch and categorize comments for a video.

    Combines fetch_video_comments() and categorize_comments() into a single call.

    Args:
        video_id: YouTube video ID
        max_comments: Maximum comments to fetch (default 100)

    Returns:
        dict on success:
            {
                "video_id": "...",
                "total_fetched": int,
                "categories": {
                    "questions": [...],
                    "objections": [...],
                    "requests": [...],
                    "other": [...]
                },
                "category_counts": {"questions": N, ...},
                "fetched_at": "ISO timestamp"
            }

        dict on error:
            {"error": "...", "video_id": "..."}
    """
    # Fetch comments
    comments = fetch_video_comments(video_id, max_comments)

    # Check for error from fetch
    if isinstance(comments, dict) and 'error' in comments:
        return comments

    # Categorize
    categories = categorize_comments(comments)

    # Build result
    return {
        'video_id': video_id,
        'total_fetched': len(comments),
        'categories': categories,
        'category_counts': {
            'questions': len(categories['questions']),
            'objections': len(categories['objections']),
            'requests': len(categories['requests']),
            'other': len(categories['other'])
        },
        'fetched_at': datetime.utcnow().isoformat() + 'Z'
    }


if __name__ == '__main__':
    # CLI interface
    if len(sys.argv) < 2:
        print("Usage: python comments.py VIDEO_ID [--max-comments N]")
        print("\nFetches and categorizes YouTube video comments.")
        print("\nExample:")
        print("  python comments.py wCFReiCGiks")
        print("  python comments.py wCFReiCGiks --max-comments 50")
        print("\nCategories:")
        print("  - questions: Comments with questions")
        print("  - objections: Comments with disagreement/corrections")
        print("  - requests: Comments requesting new content")
        print("  - other: General comments")
        sys.exit(1)

    video_id = sys.argv[1]

    # Parse optional max-comments argument
    max_comments = 100
    args = sys.argv[2:]
    for i, arg in enumerate(args):
        if arg == '--max-comments' and i + 1 < len(args):
            try:
                max_comments = int(args[i + 1])
            except ValueError:
                print(f"Error: --max-comments must be a number, got '{args[i + 1]}'")
                sys.exit(1)

    result = fetch_and_categorize_comments(video_id, max_comments)
    print(json.dumps(result, indent=2))
