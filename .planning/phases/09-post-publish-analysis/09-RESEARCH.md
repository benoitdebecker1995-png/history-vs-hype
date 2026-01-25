# Phase 9: Post-Publish Analysis - Research

**Researched:** 2026-01-25
**Domain:** YouTube Analytics + Comment Processing + Performance Benchmarking
**Confidence:** HIGH (core implementation) / LOW (CTR alternatives)

## Summary

Phase 9 builds on Phase 8's data pull scripts to create a unified post-publish analysis command. The core challenge is aggregating metrics, retention, and comments into a single analysis with automated lessons—plus resolving the CTR limitation.

The YouTube Data API v3 provides robust comment fetching via `commentThreads.list()`. Channel averages can be calculated by fetching metrics for recent videos and aggregating. ASCII retention visualization is straightforward with libraries like asciichartpy or custom implementation. The main uncertainty is CTR—the YouTube Analytics API has a known, unresolved limitation where CTR metrics are inconsistently available.

**Primary recommendation:** Implement the analysis command using existing Phase 8 scripts, add comment fetching via Data API, calculate benchmarks from historical video data, and handle CTR gracefully with fallback to manual input or prompt user to check YouTube Studio.

## Standard Stack

### Core (Already Available from Phase 8)

| Library | Version | Purpose | Status |
|---------|---------|---------|--------|
| google-api-python-client | Latest | YouTube APIs | Already installed |
| google-auth-oauthlib | Latest | OAuth2 authentication | Already installed |
| auth.py | Phase 7 | Centralized authentication | Already exists |
| metrics.py | Phase 8 | Views, watch time, engagement | Already exists |
| retention.py | Phase 8 | Retention curve + drop-offs | Already exists |
| ctr.py | Phase 8 | CTR fetcher with fallback | Already exists |
| video_report.py | Phase 8 | Combined report generator | Already exists |

### New Components Needed

| Component | Purpose | Implementation |
|-----------|---------|----------------|
| comments.py | Fetch and categorize comments | New - YouTube Data API v3 |
| channel_averages.py | Calculate benchmarks | New - aggregate historical data |
| analyze.py | Main orchestrator script | New - combines all modules |
| `/analyze` command | Slash command wrapper | New - .claude/commands/analyze.md |

### Supporting (Optional)

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| asciichartpy | 1.5.25 | ASCII line charts | Optional - retention visualization |
| re (built-in) | N/A | Video ID extraction from URL | Required |
| json (built-in) | N/A | Data serialization | Required |

**Installation (if using asciichartpy):**
```bash
pip install asciichartpy
```

## Architecture Patterns

### Recommended Script Structure

```
tools/youtube-analytics/
├── auth.py              # OAuth2 (Phase 7) - EXISTS
├── metrics.py           # Core engagement - EXISTS
├── retention.py         # Retention curve - EXISTS
├── ctr.py               # CTR fetcher - EXISTS
├── video_report.py      # Combined report - EXISTS
├── comments.py          # NEW: Comment fetcher
├── channel_averages.py  # NEW: Benchmark calculator
├── analyze.py           # NEW: Main orchestrator
└── credentials/
    ├── client_secret.json
    └── token.json
```

### Pattern 1: Video ID Extraction from URL

**What:** Parse YouTube URLs to extract video ID
**When to use:** User provides URL instead of raw video ID

```python
import re
from urllib.parse import urlparse, parse_qs

def extract_video_id(url_or_id: str) -> str:
    """
    Extract YouTube video ID from URL or return as-is if already an ID.

    Supports:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://youtube.com/shorts/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    - Raw VIDEO_ID (11 characters)
    """
    # If already looks like a video ID (11 alphanumeric + hyphens/underscores)
    if re.match(r'^[\w-]{11}$', url_or_id):
        return url_or_id

    # Parse URL
    parsed = urlparse(url_or_id)

    # youtu.be/VIDEO_ID
    if parsed.netloc in ('youtu.be', 'www.youtu.be'):
        return parsed.path.lstrip('/')[:11]

    # youtube.com/watch?v=VIDEO_ID
    if 'youtube.com' in parsed.netloc:
        if parsed.path == '/watch':
            query = parse_qs(parsed.query)
            if 'v' in query:
                return query['v'][0][:11]
        # /shorts/VIDEO_ID or /embed/VIDEO_ID
        for prefix in ('/shorts/', '/embed/', '/v/'):
            if parsed.path.startswith(prefix):
                return parsed.path[len(prefix):][:11]

    raise ValueError(f"Could not extract video ID from: {url_or_id}")
```

**Source:** Adapted from common patterns at [GitHub Gist](https://gist.github.com/afeld/1254889) and [regex101](https://regex101.com/library/fwFZqu)

### Pattern 2: Comment Fetching with Pagination

**What:** Fetch comments from YouTube Data API with pagination
**When to use:** ANALYSIS-04 requirement

```python
def fetch_video_comments(video_id: str, max_comments: int = 100) -> list[dict]:
    """
    Fetch comments for a video with pagination.

    Args:
        video_id: YouTube video ID
        max_comments: Maximum comments to fetch (default 100)

    Returns:
        List of comment dicts with text, author, likes, published_at
    """
    youtube = get_authenticated_service('youtube', 'v3')
    comments = []
    next_page_token = None

    while len(comments) < max_comments:
        response = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=min(100, max_comments - len(comments)),
            order='relevance',  # Top comments first by likes/replies
            textFormat='plainText',
            pageToken=next_page_token
        ).execute()

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
            break

    return comments
```

**Source:** [YouTube Data API - commentThreads.list](https://developers.google.com/youtube/v3/docs/commentThreads/list)

### Pattern 3: Comment Categorization

**What:** Classify comments into Questions, Objections, Requests
**When to use:** ANALYSIS-04 requirement

```python
def categorize_comments(comments: list[dict]) -> dict[str, list[dict]]:
    """
    Categorize comments into Questions, Objections, Requests.

    Uses keyword matching as heuristic. Claude can refine later.
    """
    categories = {
        'questions': [],
        'objections': [],
        'requests': []
    }

    question_patterns = [
        r'\?',  # Contains question mark
        r'^(what|why|how|when|where|who|can|could|would|is|are|do|does|did)\b',
        r'\b(wondering|curious|confused|understand)\b'
    ]

    objection_patterns = [
        r'\b(wrong|incorrect|false|misleading|disagree|actually|but)\b',
        r'\b(not true|don\'t think|doesn\'t make sense)\b',
        r'\b(mistake|error|inaccurate)\b'
    ]

    request_patterns = [
        r'\b(please|could you|can you|would you|video on|video about)\b',
        r'\b(cover|make|do|more on|next time)\b',
        r'\b(suggestion|recommend|topic|idea)\b'
    ]

    for comment in comments:
        text = comment['text'].lower()

        if any(re.search(p, text, re.I) for p in question_patterns):
            categories['questions'].append(comment)
        elif any(re.search(p, text, re.I) for p in objection_patterns):
            categories['objections'].append(comment)
        elif any(re.search(p, text, re.I) for p in request_patterns):
            categories['requests'].append(comment)

    return categories
```

### Pattern 4: Channel Averages Calculation

**What:** Calculate benchmark metrics from recent video history
**When to use:** ANALYSIS-02, ANALYSIS-03 requirements

```python
def calculate_channel_averages(last_n_videos: int = 10) -> dict:
    """
    Calculate channel averages from recent videos.

    Returns:
        dict with avg_views, avg_retention, avg_ctr (if available), etc.
    """
    # Fetch list of recent videos from channel
    youtube = get_authenticated_service('youtube', 'v3')

    # Get channel's recent uploads
    response = youtube.search().list(
        part='id',
        forMine=True,
        type='video',
        order='date',
        maxResults=last_n_videos
    ).execute()

    video_ids = [item['id']['videoId'] for item in response.get('items', [])]

    # Fetch metrics for each video
    metrics_list = []
    for vid in video_ids:
        result = get_video_metrics(vid)
        if 'error' not in result:
            metrics_list.append(result)

    if not metrics_list:
        return {'error': 'No video metrics available'}

    # Calculate averages
    return {
        'sample_size': len(metrics_list),
        'avg_views': sum(m['views'] for m in metrics_list) / len(metrics_list),
        'avg_watch_time_minutes': sum(m['watch_time_minutes'] for m in metrics_list) / len(metrics_list),
        'avg_likes': sum(m['likes'] for m in metrics_list) / len(metrics_list),
        'avg_comments': sum(m['comments'] for m in metrics_list) / len(metrics_list),
        'avg_subscribers_gained': sum(m['subscribers_gained'] for m in metrics_list) / len(metrics_list),
    }
```

### Pattern 5: ASCII Retention Curve

**What:** Generate ASCII visualization of retention curve
**When to use:** Visual retention display in terminal/markdown

**Option A: Using asciichartpy**
```python
import asciichartpy

def render_retention_curve(data_points: list[dict], height: int = 10) -> str:
    """Render retention curve as ASCII chart."""
    # Extract retention values (0.0 to 1.0) and scale to percentage
    values = [dp['retention'] * 100 for dp in data_points]

    config = {
        'height': height,
        'format': '{:5.1f}%'
    }

    return asciichartpy.plot(values, config)
```

**Option B: Custom implementation (no dependencies)**
```python
def ascii_retention_curve(data_points: list[dict], width: int = 60, height: int = 10) -> str:
    """
    Generate ASCII retention curve without external dependencies.

    Example output:
    100% |*
     90% | **
     80% |   ***
     70% |      ****
     60% |          *****
     50% |               ******
     40% |                     *******
     30% |                            *********
     20% |                                      ***
     10% |
      0% +----+----+----+----+----+----+----+----+----+----+
         0%  10%  20%  30%  40%  50%  60%  70%  80%  90% 100%
                           Video Progress
    """
    values = [dp['retention'] for dp in data_points]
    if not values:
        return "No retention data available"

    # Sample values to fit width
    step = max(1, len(values) // width)
    sampled = values[::step][:width]

    lines = []
    for row in range(height, -1, -1):
        threshold = row / height
        line = f"{int(threshold * 100):3d}% |"
        for val in sampled:
            line += "*" if val >= threshold else " "
        lines.append(line)

    # X-axis
    lines.append("     +" + "-" * len(sampled))
    lines.append("     0%      Video Progress      100%")

    return "\n".join(lines)
```

### Pattern 6: Project Folder Discovery

**What:** Find video project folder from video ID or title
**When to use:** ANALYSIS-06 requirement - linking analysis to project folder

```python
import glob
import os

def find_project_folder(video_id: str = None, video_title: str = None) -> str | None:
    """
    Find project folder matching video ID or title.

    Search strategy:
    1. Look for video ID in any file in project folders
    2. Match video title slug against folder names
    3. Return None if no match found

    Returns:
        Path to project folder, or None
    """
    base_path = "video-projects/_IN_PRODUCTION/"

    # Strategy 1: Search for video ID in project files
    if video_id:
        for folder in glob.glob(f"{base_path}*/"):
            for filepath in glob.glob(f"{folder}*.md"):
                with open(filepath, 'r', encoding='utf-8') as f:
                    if video_id in f.read():
                        return folder.rstrip('/')

    # Strategy 2: Match title to folder name
    if video_title:
        # Create slug from title (lowercase, hyphens)
        slug = re.sub(r'[^a-z0-9]+', '-', video_title.lower()).strip('-')

        for folder in glob.glob(f"{base_path}*/"):
            folder_name = os.path.basename(folder.rstrip('/'))
            # Check if slug words appear in folder name
            slug_words = slug.split('-')
            if any(word in folder_name.lower() for word in slug_words if len(word) > 3):
                return folder.rstrip('/')

    return None
```

### Anti-Patterns to Avoid

- **Scraping YouTube Studio for CTR:** Violates ToS, requires browser automation, fragile. Use API with fallback instead.
- **Fetching all comments always:** Use sampling (all if <100, top 100 by relevance if more) per CONTEXT.md.
- **Hardcoding channel averages:** Always calculate from recent videos dynamically.
- **Synchronous API calls:** For multiple videos, use async or batch where possible to avoid slow performance.

## Don't Hand-Roll

Problems with existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Video ID extraction | Custom regex from scratch | urllib.parse + simple regex | Edge cases already solved |
| ASCII charts | Character-by-character drawing | asciichartpy (optional) | Well-tested, handles scaling |
| Comment pagination | Manual page tracking | API's nextPageToken | Built into API design |
| OAuth2 flows | Token management | google-auth-oauthlib | Security-critical, complex |
| Date handling | String manipulation | datetime module | Timezone handling, ISO formats |

**Key insight:** Phase 8 already has the hard infrastructure (auth, metrics, retention, CTR). Phase 9 is primarily orchestration and presentation.

## Common Pitfalls

### Pitfall 1: CTR Data Unavailability

**What goes wrong:** Script crashes or returns partial data when CTR unavailable
**Why it happens:** YouTube Analytics API inconsistently provides CTR metrics ([Google Issue #254665034](https://issuetracker.google.com/issues/254665034))
**How to avoid:** Phase 8's ctr.py already implements graceful fallback with `ctr_available: False`
**Warning signs:** HTTP 400 errors when requesting CTR metrics

**Handling strategy:**
1. Use ctr.py's existing fallback mechanism
2. Report CTR status clearly: "CTR: 4.2%" OR "CTR: Check YouTube Studio"
3. Consider adding manual input option for user to paste CTR from Studio

### Pitfall 2: Comment API Quota Exhaustion

**What goes wrong:** Hitting daily quota limits from fetching too many comments
**Why it happens:** commentThreads.list costs 1 unit per call, max 100 comments per call
**How to avoid:** Use `order='relevance'` to get best comments first, limit to 100 total
**Warning signs:** 403 errors with quota messaging

### Pitfall 3: Missing Project Folder Mapping

**What goes wrong:** Analysis can't be saved to correct project folder
**Why it happens:** No direct mapping between YouTube video ID and local project folders
**How to avoid:** Search strategy (ID in files, title slug matching), fallback to central location
**Warning signs:** Analysis files scattered in wrong locations

### Pitfall 4: Benchmark Calculation on New Channels

**What goes wrong:** Division by zero or meaningless averages with few videos
**Why it happens:** New channels have insufficient historical data
**How to avoid:** Require minimum 3-5 videos for meaningful averages, show "insufficient data" otherwise
**Warning signs:** Averages that don't make sense (0 views average, etc.)

### Pitfall 5: Comment Categorization False Positives

**What goes wrong:** Keyword matching misclassifies comments
**Why it happens:** Simple regex can't understand context ("I don't think this is wrong" flagged as objection)
**How to avoid:** Use this as initial categorization, let Claude refine in the analysis
**Warning signs:** Obviously miscategorized comments in output

## Code Examples

### Complete Comment Fetcher (comments.py)

```python
# Source: YouTube Data API v3 documentation
# https://developers.google.com/youtube/v3/docs/commentThreads/list

"""
YouTube Video Comments Fetcher

Fetches and categorizes comments from a video using YouTube Data API v3.

Usage:
    from comments import fetch_and_categorize_comments

    result = fetch_and_categorize_comments('VIDEO_ID')
    print(result['categories']['questions'])
"""

from auth import get_authenticated_service
import re

def fetch_video_comments(video_id: str, max_comments: int = 100) -> list[dict]:
    """Fetch comments with pagination."""
    youtube = get_authenticated_service('youtube', 'v3')
    comments = []
    next_page_token = None

    while len(comments) < max_comments:
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=min(100, max_comments - len(comments)),
            order='relevance',
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
            break

    return comments


def categorize_comments(comments: list[dict]) -> dict[str, list[dict]]:
    """Categorize into Questions, Objections, Requests."""
    categories = {'questions': [], 'objections': [], 'requests': [], 'other': []}

    for comment in comments:
        text = comment['text'].lower()

        # Question detection
        if '?' in text or re.search(r'^(what|why|how|when|where|who|can|could|is|are|do)\b', text):
            categories['questions'].append(comment)
        # Objection detection
        elif re.search(r'\b(wrong|incorrect|false|disagree|actually|mistake|error)\b', text):
            categories['objections'].append(comment)
        # Request detection
        elif re.search(r'\b(please|could you|video on|video about|cover|suggestion)\b', text):
            categories['requests'].append(comment)
        else:
            categories['other'].append(comment)

    return categories


def fetch_and_categorize_comments(video_id: str, max_comments: int = 100) -> dict:
    """Main entry point: fetch and categorize comments."""
    comments = fetch_video_comments(video_id, max_comments)
    categories = categorize_comments(comments)

    return {
        'video_id': video_id,
        'total_fetched': len(comments),
        'categories': categories,
        'category_counts': {k: len(v) for k, v in categories.items()}
    }
```

### Slash Command Structure (/analyze)

```markdown
---
description: Run post-publish analysis on any video with benchmarks and lessons
---

# /analyze - Post-Publish Video Analysis

Comprehensive performance analysis with CTR comparison, retention drop-offs,
comment categorization, and automated lessons.

## Usage

```
/analyze VIDEO_ID_OR_URL
/analyze https://youtu.be/ABC123
/analyze ABC123def12
```

## What It Does

1. Fetches all metrics (views, watch time, engagement, CTR if available)
2. Pulls retention curve and identifies all significant drop-offs
3. Compares against channel average AND last 10 videos
4. Fetches and categorizes comments (Questions, Objections, Requests)
5. Generates automated observations and actionable lessons
6. Saves report to video project folder (if found) or channel-data/

## Output

Creates `POST-PUBLISH-ANALYSIS.md` with:
- Quick insights (above/below benchmarks)
- Performance metrics table
- ASCII retention curve visualization
- All drop-off points with timestamps
- Categorized comments (full list)
- Claude-generated lessons
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual YouTube Studio checks | API-based automated fetching | Phase 8 (2026-01) | Saves 15+ min per video |
| CTR always via API | Graceful fallback when unavailable | Phase 8 | No more crashes |
| No comment analysis | Automated categorization | Phase 9 | Identifies audience feedback patterns |
| Manual lesson writing | Claude-generated lessons | Phase 9 | Consistent insights |

**Deprecated/outdated:**
- YouTube API v2: Fully deprecated, use v3 only
- Direct CTR API access assumption: Known inconsistent since 2022

## Open Questions

Things that couldn't be fully resolved:

1. **CTR Availability**
   - What we know: API inconsistently returns CTR metrics, documented in Google Issue Tracker
   - What's unclear: No timeline for fix, no alternative API endpoint
   - Recommendation: Accept graceful fallback, optionally add manual input prompt
   - Confidence: LOW that API will improve, HIGH that current fallback strategy works

2. **Project Folder Mapping Accuracy**
   - What we know: Can search for video ID in files, match title slugs
   - What's unclear: How reliable is slug matching for all project names?
   - Recommendation: Implement search strategy, fallback to central analytics folder
   - Confidence: MEDIUM - will work for most cases, may need user override

3. **Comment Categorization Accuracy**
   - What we know: Keyword matching works for obvious cases
   - What's unclear: Edge cases, context-dependent meaning
   - Recommendation: Use as initial pass, Claude refines in analysis narrative
   - Confidence: MEDIUM - good enough for heuristic, not perfect

## Sources

### Primary (HIGH confidence)

- [YouTube Analytics API Metrics](https://developers.google.com/youtube/analytics/metrics) - Metric definitions, availability
- [YouTube Data API v3 - commentThreads.list](https://developers.google.com/youtube/v3/docs/commentThreads/list) - Comment fetching parameters
- [YouTube API Python Samples - comment_handling.py](https://github.com/youtube/api-samples/blob/master/python/comment_handling.py) - Official code patterns
- Phase 8 scripts (metrics.py, retention.py, ctr.py) - Existing working implementations

### Secondary (MEDIUM confidence)

- [Google Issue Tracker #254665034](https://issuetracker.google.com/issues/254665034) - CTR API limitation confirmation
- [asciichartpy on PyPI](https://pypi.org/project/asciichartpy/) - ASCII chart library
- [GitHub Gist - YouTube Video ID Regex](https://gist.github.com/afeld/1254889) - URL parsing patterns

### Tertiary (LOW confidence)

- WebSearch results on scraping alternatives - Not recommended, ToS concerns
- Third-party tools (TubeBuddy, VidIQ) for CTR - External dependency, not API-based

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Using existing Phase 8 infrastructure + documented APIs
- Architecture: HIGH - Clear module separation, patterns well-established
- Comment fetching: HIGH - Official API with good documentation
- CTR handling: MEDIUM - Fallback strategy solid, root issue unresolved
- Project folder discovery: MEDIUM - Heuristic-based, may need user override
- Comment categorization: MEDIUM - Keyword-based, refinable by Claude

**Research date:** 2026-01-25
**Valid until:** 60 days (APIs stable, CTR issue long-standing)
