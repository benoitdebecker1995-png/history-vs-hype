# Phase 43: YouTube Intelligence Engine - Research

**Researched:** 2026-02-20
**Domain:** Data scraping, SQLite storage, YouTube algorithm mechanics, competitor intelligence
**Confidence:** MEDIUM (algorithm mechanics HIGH from official sources; scraping library stability MEDIUM; niche patterns MEDIUM from secondary sources)

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Knowledge Base Content:**
- Deep algorithm mechanics: full model of browse vs search vs suggested pipelines, satisfaction signals, audience segments, shadow metrics — not just practical tips
- Full niche intelligence: formats, lengths, hook styles, thumbnail patterns, title formulas, posting frequency, audience overlap for history/edu niche
- Longform only — ignore Shorts strategy entirely
- Include SEO/discovery trends: trending search terms and topic interest in history/edu niche
- Absorb and replace existing manual analysis files (SCRIPT-STRUCTURE-ANALYSIS.md, COMPETITOR-TITLE-DATABASE.md) — one source of truth
- Research best algorithm sources during planning (user doesn't have strong preferences on specific sources)
- Purge outdated data on refresh — knowledge base always reflects current reality

**Refresh Mechanism:**
- Integrated into workflow: auto-refresh when starting pre-production commands (/research --new, /script) if data is stale — no separate refresh command needed
- Show changes after refresh: display summary of what's new/changed since last run
- No time limit on refresh duration — comprehensiveness over speed
- Purge outdated data — replace, don't accumulate

**Query Interface:**
- Both natural language AND structured flags: natural language for exploration, structured flags for common queries (algorithm summary, competitor report, niche trends)
- Light integration now: script-writer agent reads KB and incorporates insights into decisions (hook structure, pacing). Phase 45 deepens this.
- Agent reads KB approach: intelligence is consumed by agents as context, not shown as tips

**Competitor Monitoring:**
- Research which channels to track during planning phase (beyond the 5 style references)
- Full analysis per competitor upload: titles, views, upload dates, video length, thumbnail style, topic category, engagement signals
- Include AI-generated analysis of WHY outlier videos performed (pattern identification)

### Claude's Discretion

- Storage format (SQLite vs markdown vs hybrid)
- Raw + insights vs insights-only storage decision
- Temporal tracking (changelog vs current-state-only)
- Channel size focus (small channel specific vs general + small)
- Confidence/reliability rating system for claims
- Niche scope filter (style-match channels vs broad history/edu)
- Data sources for refresh (web search vs custom scrapers vs YouTube API)
- Command name (/intel vs extending /discover)
- Output depth defaults (concise vs detailed)
- Source citations in query results
- Agent access scope (which agents read KB)
- Topic overlap alerting
- Competitor lookback period
- Channel management approach (config file vs command)
- Infrastructure sharing with /patterns command

### Deferred Ideas (OUT OF SCOPE)

None — discussion stayed within phase scope
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| INTEL-01 | Local knowledge base stores algorithm mechanics (AVD, CTR, satisfaction signals, browse vs search priorities) | Resolved: SQLite hybrid with JSON columns stores structured algorithm model; web-scraped from vidIQ/outlierkit/Creator Insider on refresh |
| INTEL-02 | Knowledge base stores niche-specific patterns (what history/edu formats, lengths, hooks are performing) | Resolved: Competitor RSS feeds provide format/length/title data; AI analysis layer extracts patterns at refresh time |
| INTEL-03 | Web scraper refreshes algorithm knowledge from authoritative sources (Creator Insider, Think Media, vidIQ blog, etc.) | Resolved: requests + feedparser for RSS/blog scraping; Claude Code summarization synthesizes findings into KB |
| INTEL-04 | Competitor tracker monitors top history/edu channels for viral content and format trends | Resolved: YouTube RSS feeds (free, no API quota) provide last 15 uploads per channel; YouTube Data API fills gaps for view counts and duration |
</phase_requirements>

---

## Summary

This phase builds a local YouTube intelligence knowledge base in Python, stored as SQLite, that auto-refreshes on pre-production command invocation. The two core data domains are (1) algorithm mechanics, sourced from authoritative creator-industry blogs and YouTube's own official communications, and (2) competitor/niche patterns, sourced from YouTube RSS feeds augmented by the existing YouTube Data API integration.

The standard stack is: `requests` + `feedparser` for web content fetching, the existing `google-api-python-client` for video metadata enrichment, `sqlite3` (stdlib) for storage, and Claude Code's own LLM layer (via the `notebooklm_bridge.py` pattern from Phase 42.1) for synthesizing scraped web content into structured algorithm knowledge. The `/intel` command is recommended over extending `/discover` because the query patterns are fundamentally different — `/discover` is keyword/topic research while `/intel` is strategic intelligence.

The recommended architecture is a **hybrid SQLite + Markdown** approach: SQLite stores structured competitor data (videos, channels, view counts, dates) and algorithm signal weights as versioned records; a generated Markdown file (`channel-data/youtube-intelligence.md`) serves as the agent-readable KB snapshot that script-writer-v2 loads. This sidesteps SQLite read complexity inside Claude Code agent contexts while keeping the underlying data queryable and structured.

**Primary recommendation:** Use YouTube RSS feeds as the backbone for competitor tracking (free, no quota), enrich with YouTube Data API for view counts and duration (existing OAuth2 setup), and use Claude Code LLM synthesis for algorithm knowledge extraction from scraped blog content.

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| `sqlite3` | stdlib | Structured storage for competitor data, channel registry, algorithm snapshots | Already used in tools/discovery/; no new dependencies |
| `requests` | 2.32.5 (installed) | HTTP fetching for blog content and RSS discovery | Already installed; simple, battle-tested |
| `feedparser` | 6.x (needs install) | Parse YouTube RSS feeds and blog Atom feeds | Purpose-built RSS/Atom parsing; handles encoding, malformed feeds |
| `google-api-python-client` | 2.189.0 (installed) | YouTube Data API for view counts, duration, video details | Already installed and authenticated (auth.py in tools/youtube-analytics/) |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `json` | stdlib | Store algorithm signal blob, pattern summaries in SQLite JSON columns | Use for flexible schema areas that evolve over time |
| `datetime` / `pathlib` | stdlib | Staleness tracking, file paths | All timestamp logic |
| Claude Code LLM (notebooklm_bridge pattern) | n/a | Synthesize scraped blog content into structured algorithm model | Algorithm knowledge extraction only — not for competitor data |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| feedparser | scrapetube | scrapetube is more powerful (gets all channel videos) but fragile — YouTube actively blocks scrapers; RSS feeds are officially supported by YouTube and return last 15 videos free |
| YouTube RSS (15 video limit) | YouTube Data API (playlistItems.list) | RSS is free with no quota; API costs 1 unit/call but can paginate beyond 15. Use RSS as primary, API only for enrichment |
| SQLite | Pure Markdown files | Markdown is simpler to read in agents but can't be queried, sorted, or diffed efficiently; hybrid gives both |
| Claude Code LLM synthesis | Manual curation | Algorithm sources update frequently; LLM synthesis allows periodic re-ingestion without manual work |

**Installation:**
```bash
pip install feedparser
# All other dependencies already installed
```

---

## Architecture Patterns

### Recommended Project Structure

```
tools/
└── intel/
    ├── __init__.py
    ├── kb_store.py          # SQLite schema, read/write operations
    ├── algo_scraper.py      # Scrapes vidIQ/Creator Insider/Think Media blogs
    ├── algo_synthesizer.py  # LLM synthesis of scraped content into algorithm model
    ├── competitor_tracker.py # RSS feed fetching + YouTube Data API enrichment
    ├── pattern_analyzer.py  # Detects outlier videos, format trends
    ├── kb_exporter.py       # Generates youtube-intelligence.md from SQLite
    ├── refresh.py           # Orchestrator: runs all refresh components
    └── query.py             # /intel command query interface
channel-data/
└── youtube-intelligence.md  # Agent-readable KB snapshot (generated, not edited)
.claude/commands/
└── intel.md                 # /intel command definition
```

### Pattern 1: Hybrid Storage (SQLite + Generated Markdown)

**What:** SQLite holds structured data (competitor videos, channel configs, algorithm snapshot records). A generated Markdown file is the agent-facing view updated on each refresh.

**When to use:** Any time agent code needs to read KB content without running Python. Agents read the Markdown; Python queries SQLite.

**Example:**
```python
# kb_exporter.py — generates agent-readable snapshot
def export_kb_to_markdown(db_path: str, output_path: str) -> dict:
    """
    Reads SQLite, writes youtube-intelligence.md.
    Called at end of every refresh cycle.
    Returns {'written_to': path, 'sections': list}
    """
    conn = sqlite3.connect(db_path)
    algo = _load_algorithm_snapshot(conn)
    competitors = _load_competitor_summary(conn)
    niche = _load_niche_patterns(conn)

    md = _render_markdown(algo, competitors, niche)
    Path(output_path).write_text(md, encoding='utf-8')
    return {'written_to': output_path, 'sections': ['algorithm', 'competitors', 'niche']}
```

### Pattern 2: YouTube RSS Feed Fetching

**What:** YouTube provides an official RSS feed for every channel: `https://www.youtube.com/feeds/videos.xml?channel_id=CHANNEL_ID`. Returns last 15 videos with title, video ID, published date, and description. No API key required.

**When to use:** Primary method for competitor upload monitoring. Free, no quota, officially supported.

**Example:**
```python
# competitor_tracker.py
import feedparser
import requests

YOUTUBE_RSS = "https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"

def fetch_channel_recent(channel_id: str, channel_name: str) -> dict:
    """
    Fetch last 15 videos from channel RSS feed.
    Returns {'channel_id': str, 'videos': list[dict]} or {'error': msg}
    """
    url = YOUTUBE_RSS.format(channel_id=channel_id)
    try:
        feed = feedparser.parse(url)
        if feed.bozo and not feed.entries:
            return {'error': f'RSS parse failed for {channel_name}'}

        videos = []
        for entry in feed.entries:
            videos.append({
                'video_id': entry.yt_videoid,
                'title': entry.title,
                'published': entry.published,
                'description': entry.summary[:500] if hasattr(entry, 'summary') else '',
                'channel_id': channel_id,
                'channel_name': channel_name,
            })
        return {'channel_id': channel_id, 'videos': videos}
    except Exception as e:
        return {'error': str(e)}
```

### Pattern 3: YouTube Data API Enrichment

**What:** RSS feeds lack view counts and duration. The existing `tools/youtube-analytics/auth.py` and YouTube Data API (quota: 1 unit per list call) can enrich up to 50 videos per call with view count, duration, and like count.

**When to use:** After RSS fetch, batch enrich the video IDs. The existing Google Cloud project and OAuth token handle auth.

**Example:**
```python
# competitor_tracker.py
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'youtube-analytics'))
from auth import get_authenticated_service

def enrich_videos_with_metadata(video_ids: list[str]) -> dict:
    """
    Batch fetch view counts, duration for up to 50 video IDs.
    Costs 1 API quota unit per call (up to 50 IDs).
    Returns {video_id: {'views': int, 'duration': str, 'likes': int}}
    """
    youtube = get_authenticated_service('youtube', 'v3')
    response = youtube.videos().list(
        part='statistics,contentDetails',
        id=','.join(video_ids[:50])
    ).execute()

    result = {}
    for item in response.get('items', []):
        vid_id = item['id']
        stats = item.get('statistics', {})
        content = item.get('contentDetails', {})
        result[vid_id] = {
            'views': int(stats.get('viewCount', 0)),
            'likes': int(stats.get('likeCount', 0)),
            'duration': content.get('duration', ''),  # ISO 8601: PT15M30S
        }
    return result
```

### Pattern 4: Algorithm Content Scraping + LLM Synthesis

**What:** Blog posts from vidIQ, Creator Insider, Think Media, and outlierkit publish algorithm updates. Scrape with `requests`, extract text, pass to Claude Code LLM (via `notebooklm_bridge.py` pattern) to produce a structured algorithm model.

**When to use:** Algorithm knowledge refresh. Not used for competitor tracking.

**Example:**
```python
# algo_scraper.py
ALGO_SOURCES = [
    {'name': 'vidIQ Algorithm Guide', 'url': 'https://vidiq.com/blog/post/understanding-youtube-algorithm/', 'type': 'blog'},
    {'name': 'OutlierKit Algorithm Updates', 'url': 'https://outlierkit.com/resources/youtube-algorithm-updates/', 'type': 'blog'},
    {'name': 'Creator Insider YouTube', 'channel_id': 'UCr-pWa7LMHX71Uhr7D4wqMQ', 'type': 'rss'},
    {'name': 'Think Media Blog', 'url': 'https://www.thinkmarketing.com/blog/', 'type': 'blog'},
]

def scrape_source(source: dict) -> dict:
    """
    Fetch content from a single algorithm source.
    Returns {'source': name, 'content': text, 'fetched_at': iso_timestamp}
    """
    if source['type'] == 'rss':
        feed = feedparser.parse(YOUTUBE_RSS.format(channel_id=source['channel_id']))
        text = '\n'.join(e.title + ': ' + getattr(e, 'summary', '') for e in feed.entries[:10])
    else:
        resp = requests.get(source['url'], timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
        # Simple text extraction — BeautifulSoup optional enhancement
        text = resp.text[:8000]  # Limit to prevent token explosion
    return {'source': source['name'], 'content': text, 'fetched_at': datetime.utcnow().isoformat()}
```

### Pattern 5: Staleness Check (Auto-Refresh Trigger)

**What:** Every pre-production command (`/research --new`, `/script`) checks if KB is stale before starting. Stale = last refresh older than 7 days.

**When to use:** Inject at command entry points. Show refresh summary if refresh occurred.

**Example:**
```python
# refresh.py
def is_stale(db_path: str, max_age_days: int = 7) -> bool:
    """Check if KB needs refresh based on last_refresh timestamp in sqlite"""
    conn = sqlite3.connect(db_path)
    row = conn.execute("SELECT last_refresh FROM kb_meta ORDER BY id DESC LIMIT 1").fetchone()
    if not row:
        return True
    last = datetime.fromisoformat(row[0])
    return (datetime.utcnow() - last).days >= max_age_days

def run_refresh(db_path: str) -> dict:
    """Full refresh: algo sources + competitor feeds. Returns change summary."""
    # 1. Scrape algo sources, synthesize with LLM, write to algo_snapshots table
    # 2. Fetch competitor RSS feeds, enrich with API, write to competitor_videos table
    # 3. Run outlier detection on new videos
    # 4. Export to youtube-intelligence.md
    # 5. Update kb_meta.last_refresh
    ...
```

### Pattern 6: Outlier Detection

**What:** A video is an outlier if its view count is >= 3x the channel's median recent view count. This is the "viral content" flag from INTEL-04.

**When to use:** Run after each competitor refresh. Flag outlier videos in competitor_videos table and surface in reports.

**Example:**
```python
# pattern_analyzer.py
def detect_outliers(videos: list[dict], multiplier: float = 3.0) -> list[dict]:
    """
    Flag videos that outperform the channel median by multiplier.
    Input: list of videos with 'views' field.
    Output: same list with 'is_outlier' bool added.
    """
    import statistics
    view_counts = [v['views'] for v in videos if v.get('views', 0) > 0]
    if len(view_counts) < 3:
        return [{**v, 'is_outlier': False} for v in videos]
    median = statistics.median(view_counts)
    return [{**v, 'is_outlier': v.get('views', 0) >= median * multiplier} for v in videos]
```

### SQLite Schema (Recommended)

```sql
-- Algorithm knowledge: one snapshot per refresh
CREATE TABLE algo_snapshots (
    id INTEGER PRIMARY KEY,
    refreshed_at TEXT NOT NULL,
    source_names TEXT NOT NULL,  -- JSON array of sources used
    algorithm_model TEXT NOT NULL,  -- JSON: full model blob
    signal_weights TEXT,  -- JSON: {ctr: 'high', avd: 'high', satisfaction: 'very_high', ...}
    longform_insights TEXT,  -- JSON: insights specific to longform
    confidence TEXT DEFAULT 'medium'
);

-- Competitor channel registry (config)
CREATE TABLE competitor_channels (
    channel_id TEXT PRIMARY KEY,
    channel_name TEXT NOT NULL,
    channel_url TEXT,
    subscriber_count INTEGER,
    niche_category TEXT,  -- 'style-match', 'broad-history', 'geopolitics'
    track_active INTEGER DEFAULT 1,
    added_at TEXT NOT NULL
);

-- Competitor video store (rolling window, purge on refresh)
CREATE TABLE competitor_videos (
    video_id TEXT PRIMARY KEY,
    channel_id TEXT REFERENCES competitor_channels(channel_id),
    title TEXT NOT NULL,
    published_at TEXT NOT NULL,
    views INTEGER,
    likes INTEGER,
    duration_seconds INTEGER,
    description TEXT,
    is_outlier INTEGER DEFAULT 0,
    outlier_reason TEXT,
    fetched_at TEXT NOT NULL
);

-- Niche pattern snapshots
CREATE TABLE niche_snapshots (
    id INTEGER PRIMARY KEY,
    refreshed_at TEXT NOT NULL,
    format_patterns TEXT,  -- JSON: {top_formats: [...], avg_length_min: 22, ...}
    hook_patterns TEXT,    -- JSON: {common_hooks: [...], title_formulas: [...]}
    trending_topics TEXT   -- JSON: [{topic, channel, views, published_at}, ...]
);

-- Metadata / staleness tracking
CREATE TABLE kb_meta (
    id INTEGER PRIMARY KEY,
    last_refresh TEXT,
    last_export TEXT,
    version INTEGER DEFAULT 1
);

CREATE INDEX idx_competitor_videos_channel ON competitor_videos(channel_id);
CREATE INDEX idx_competitor_videos_outlier ON competitor_videos(is_outlier);
CREATE INDEX idx_competitor_videos_published ON competitor_videos(published_at);
```

### Anti-Patterns to Avoid

- **Storing raw HTML in SQLite:** Extract text before storage. Raw HTML bloats the DB and slows reads.
- **Using scrapetube for competitor tracking:** It scrapes YouTube's internal API, breaks without warning when YouTube changes page structure. RSS feeds are officially supported.
- **Separate DB for intel:** Avoid creating a third SQLite database. Use `tools/intel/intel.db` as the new standalone DB (separate from `keywords.db` and `analytics.db` to keep concerns clean).
- **Refreshing on every /script call:** Staleness check is cheap; full refresh is expensive. Check first, refresh only if stale.
- **Storing algorithm claims without confidence ratings:** Algorithm docs vary in quality. Every insight should carry a confidence tag (high/medium/low) based on source authority.
- **Hardcoding competitor channel IDs in code:** Store in `competitor_channels` table. Management via `/intel --add-channel` or a config JSON file.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| RSS feed parsing | Custom XML parser | feedparser | Handles encoding, malformed feeds, all RSS/Atom variants |
| YouTube channel upload list | Custom scraper | YouTube RSS feed or Data API playlistItems | RSS is officially supported, scraper breaks on structure changes |
| View count enrichment | HTML scraping | YouTube Data API videos.list (1 quota unit/call, 50 IDs per call) | Existing auth setup, quota generous enough for 15 channels × weekly = negligible cost |
| Auth to YouTube API | Custom OAuth flow | tools/youtube-analytics/auth.py | Already built and token-cached |
| Blog text extraction | Full BeautifulSoup spider | requests + simple text strip | Claude LLM handles messy text; full parsing is over-engineered for this use case |
| Pattern detection across channels | ML model | Simple statistics (median × multiplier) | Outlier detection with 15 videos/channel doesn't need ML |

**Key insight:** This phase is primarily a data pipeline, not an ML system. Simple statistics and LLM synthesis outperform complex custom algorithms for the data volumes involved (15 channels × 15 videos = 225 data points per refresh).

---

## Common Pitfalls

### Pitfall 1: YouTube RSS 15-Video Limit
**What goes wrong:** RSS feeds return only the 15 most recent videos. For a channel that uploads daily, 15 videos = 2 weeks. For weekly uploaders, 15 videos = 4 months.
**Why it happens:** YouTube deliberately limits RSS to 15 items.
**How to avoid:** For history/edu channels that upload infrequently (1-2 per month), 15 videos is 6-12 months of data — sufficient. On first-run setup, optionally use YouTube Data API `playlistItems.list` to backfill the uploads playlist (paginate to get 50-200 videos). Store in `competitor_videos` table permanently; RSS updates it going forward.
**Warning signs:** Channels with high upload frequency (daily/weekly) will show incomplete trend data from RSS alone.

### Pitfall 2: Algorithm "Knowledge" Staleness vs. Data Staleness
**What goes wrong:** Algorithm blog content is synthesized at refresh time. If the synthesis prompt doesn't ask for date-specific information, the LLM may blend old and new algorithm claims.
**Why it happens:** LLM synthesis conflates training knowledge (pre-2025) with scraped content (current).
**How to avoid:** Synthesis prompt must explicitly instruct: "Only use information from the scraped content below. Ignore your training knowledge. Note the publication date of each source. Flag any conflicting claims across sources."

### Pitfall 3: Python 3.14 + spaCy (Known Issue)
**What goes wrong:** spaCy is incompatible with Python 3.14. The existing codebase notes this.
**Why it happens:** spaCy hasn't released 3.14-compatible wheels as of 2026-02-20.
**How to avoid:** Phase 43 code should NOT import spaCy. All NLP in this phase is handled by LLM synthesis, not spaCy. This is clean.

### Pitfall 4: YouTube Data API Quota for Competitor Enrichment
**What goes wrong:** 15 channels × 15 videos = 225 video IDs to enrich. At 50 IDs per API call = 5 calls × 1 unit = 5 quota units per refresh. With 10,000 units/day, this is negligible. BUT: if the code accidentally calls `search.list` (100 units each) instead of `videos.list` (1 unit each), quota burns fast.
**Why it happens:** Developers use search to find videos by query rather than fetching by ID.
**How to avoid:** NEVER use `search.list` in this phase. Always fetch by video ID via `videos.list`. RSS provides the video IDs directly.

### Pitfall 5: Agent Context Size
**What goes wrong:** If `youtube-intelligence.md` is too large, it consumes significant context window when loaded by script-writer-v2.
**Why it happens:** Comprehensive KB dumps everything into one file.
**How to avoid:** Design the exported Markdown with sections that can be partially loaded. Target total size under 3,000 words. Use concise, scannable formats (tables, bullets) rather than prose. Script-writer-v2 can load specific sections.

### Pitfall 6: scrapetube Fragility
**What goes wrong:** If the plan uses scrapetube for competitor data, it will break unpredictably when YouTube changes their internal API structure.
**Why it happens:** scrapetube scrapes YouTube's internal Innertube API (undocumented). Last release was September 2025, showing it's still maintained, but fragility is inherent.
**How to avoid:** Use YouTube RSS feeds as primary. Reserve scrapetube as optional enhancement only (graceful degradation, never required for core functionality). The STATE.md already notes "scrapetube not installed (graceful degradation)."

---

## Code Examples

### Competitor Channel Config File (Recommended Over Hardcoding)

```json
// tools/intel/competitor_channels.json
{
  "channels": [
    {"id": "UCIjc5FMDlQj2PEyFjqBQRTw", "name": "Kraut", "category": "style-match"},
    {"id": "UCpW4cR0RF0mVzCzBo8PXQBA", "name": "Fall of Civilizations", "category": "style-match"},
    {"id": "UCQeRaTukNYft1_6AZPACnog", "name": "RealLifeLore", "category": "broad-history"},
    {"id": "UCMmaBzfCCwZ2KqaBJjkj0fw", "name": "Kings and Generals", "category": "broad-history"},
    {"id": "UCNjln6WWND4Ks-lbXGFMBhA", "name": "Shaun", "category": "style-match"},
    {"id": "UCrPSeQVnJLJL9CWDlm3UCiQ", "name": "Knowing Better", "category": "style-match"},
    {"id": "UCyEqailAaj8e2dCuhB2CfhA", "name": "Wendover Productions", "category": "broad-history"},
    {"id": "UCXqRJ7f3VoRHvJRrHEVa7rg", "name": "Johnny Harris", "category": "geopolitics"},
    {"id": "UC-LDY-f9VH3Hbj8bHVs5Blw", "name": "Historia Civilis", "category": "style-match"},
    {"id": "UC7DSoc3FERbByiRNBbO76Vg", "name": "Toldinstone", "category": "broad-history"},
    {"id": "UCHa2IaUVA07YSZrkiDO4XUQ", "name": "HistoryMarche", "category": "broad-history"}
  ]
}
```

Note: Channel IDs above are approximate — verify against actual YouTube channel pages before hardcoding. The config file approach lets the user add/remove channels without code changes.

### Algorithm Synthesis Prompt (LLM Integration)

```python
# algo_synthesizer.py
SYNTHESIS_PROMPT = """You are analyzing YouTube algorithm documentation from official and authoritative sources.

SCRAPED CONTENT (use ONLY this, ignore your training data):
{scraped_text}

Extract and structure the following as JSON:
{{
  "signal_weights": {{
    "ctr": "very_high|high|medium|low",
    "avd": "very_high|high|medium|low",
    "satisfaction": "very_high|high|medium|low",
    "session_continuation": "very_high|high|medium|low",
    "upload_consistency": "very_high|high|medium|low"
  }},
  "pipeline_mechanics": {{
    "browse_feed": "how it works for longform, 1-2 sentences",
    "search": "how it works for longform, 1-2 sentences",
    "suggested": "how it works for longform, 1-2 sentences"
  }},
  "longform_specific": ["insight1", "insight2", ...],
  "satisfaction_signals": ["signal1", "signal2", ...],
  "avd_thresholds": "any specific % thresholds mentioned",
  "ctr_thresholds": "any specific % thresholds mentioned",
  "small_channel_notes": "any mentions of small channel behavior",
  "sources_used": ["source1", "source2", ...],
  "confidence": "high|medium|low",
  "synthesis_date": "{date}"
}}

Rules:
- ONLY use information from the scraped content above
- If sources conflict, note both and mark confidence as low
- If information is absent, use null, not assumptions
- Longform means 10+ minute videos; exclude all Shorts guidance
"""
```

### /intel Command Structure (Recommended)

```
/intel                          # Full intelligence report (algo + competitors + niche)
/intel --algo                   # Algorithm mechanics only
/intel --competitors            # Competitor uploads this week
/intel --outliers               # Only viral/outlier videos detected
/intel --niche                  # Niche format/length/hook patterns
/intel --refresh                # Force refresh regardless of staleness
/intel --add-channel CHANNEL_ID # Add competitor to tracking list
/intel --query "how does browse feed work"  # Natural language query
```

### Script-Writer-V2 KB Integration Point

The agent already has 18 rules. Rule 19 (Phase 45) will be the full hook optimization rule. For Phase 43 (light integration), add a KB read step to the existing pre-script intelligence block:

```markdown
### PRE-SCRIPT INTELLIGENCE (existing section in script.md)
...
3. **KB Intelligence (Phase 43):** Read `channel-data/youtube-intelligence.md` sections:
   - Algorithm: current satisfaction signals, what YouTube rewards in longform
   - Niche: recent format trends, outlier video patterns
   - Surface as internal context for structure decisions, not as displayed tips
```

---

## Authoritative Algorithm Sources (Researched)

Based on web research, the following sources provide the most reliable YouTube algorithm intelligence for longform history/edu content:

| Source | Type | Authority | Update Frequency | Access |
|--------|------|-----------|-----------------|--------|
| **Creator Insider** (YouTube channel) | Official YouTube | HIGHEST | Irregular (2-4/month) | YouTube RSS |
| **vidIQ blog** (vidiq.com/blog) | Industry tool, proprietary data | HIGH | Weekly | Web scraping |
| **OutlierKit** (outlierkit.com/resources) | Niche tool with YouTube access | HIGH | Monthly | Web scraping |
| **Buffer Resources** (buffer.com/resources) | Marketing platform | MEDIUM | Monthly | Web scraping |
| **Hootsuite Blog** (hootsuite.com) | Social platform | MEDIUM | Monthly | Web scraping |
| **Think Media Blog** | Creator educator | MEDIUM | Irregular | Web scraping |

**Not recommended as primary sources (MEDIUM-LOW):**
- Generic SEO blogs (imarkinfotech, dataslayer) — aggregate other sources, add noise
- Social media marketing sites (Metricool, SproutSocial) — focus on Shorts/social, not longform

**Creator Insider RSS feed URL:** `https://www.youtube.com/feeds/videos.xml?channel_id=UCr-pWa7LMHX71Uhr7D4wqMQ`
*(Verify this channel ID — search YouTube for "Creator Insider" official YouTube channel)*

---

## Competitor Channel List (Researched)

Channels to track beyond the 5 style references (Kraut, Fall of Civilizations, Shaun, Knowing Better, Alex O'Connor):

**Tier 1: Style-Match (closest DNA):**
- Historia Civilis — Roman history, minimalist, intellectual
- Toldinstone — Ancient Greece/Rome, academic

**Tier 2: Broad History/Edu (same audience):**
- RealLifeLore — Geography/maps, same 25-44 male demographic
- Kings and Generals — Military history, animated
- Wendover Productions — Logistics/systems (audience overlap)
- Johnny Harris — Geopolitics journalism

**Tier 3: Watch for Format Innovations:**
- HistoryMarche — Military animated history
- Asianometry — Deep technical/historical analysis

**Recommended tracking: 8-10 channels total.** 5 style-match + 3-5 broader history. This gives enough data points for pattern detection without refresh overhead.

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Watch time as primary signal | Satisfaction signals (surveys + behavior) | Mid-2024, dominant by 2026 | Shorter, higher-satisfaction videos can outperform longer padded ones |
| Shorts affecting long-form algorithm | Fully decoupled | Late 2025 | History vs Hype is longform-only — this is now clean separation |
| CTR as primary discovery signal | CTR + session continuation | 2025 | Must keep viewers watching AND watching next video |
| Browse feed based on broad topics | Personalized watch-history clusters | February 2026 | Niche history content gets better reach to interested viewers |
| Small channels struggling to compete | YouTube actively surfaces small channels | 2025 | 450-subscriber channels can get tested with larger audiences |
| View count as outlier metric | View count relative to channel median | Ongoing | Use channel-relative outlier detection, not absolute views |

**Algorithm signal weight hierarchy (2026, from vidIQ and OutlierKit sources):**
1. Viewer Satisfaction — VERY HIGH (increased 2026)
2. Click-Through Rate — HIGH (stable)
3. Average View Duration — HIGH (stable)
4. Session Contribution — MEDIUM-HIGH (increased 2026)
5. New Viewer Attraction — MEDIUM (new 2026)
6. Upload Consistency — MEDIUM (stable)

---

## Decisions Recommended (Claude's Discretion Items)

Based on research, here are recommendations for all discretion items:

| Decision Item | Recommendation | Rationale |
|--------------|----------------|-----------|
| Storage format | **Hybrid: SQLite + generated Markdown** | SQLite for structure/queries; Markdown for agent reads |
| Raw vs insights-only | **Both: raw in SQLite, insights in Markdown export** | Raw allows re-analysis; insights for consumption |
| Temporal tracking | **Current-state-only with last_refresh timestamp** | Changelog adds complexity; staleness check is sufficient |
| Channel size focus | **General + small-channel notes flagged** | Algorithm increasingly surfaces small channels; relevant |
| Confidence ratings | **Three-tier: high/medium/low per claim** | Algorithm blogs vary in authority; source tracking matters |
| Niche scope filter | **Style-match primary + broad-history secondary** | Two-tier competitor list, labeled in DB |
| Data sources | **YouTube RSS (primary) + YouTube Data API (enrichment) + web scraping (algo)** | Layered approach: free tier first |
| Command name | **/intel** | `/discover` is keyword research; `/intel` is strategy |
| Output depth defaults | **Concise by default, --verbose for detail** | Agent context budget matters |
| Source citations | **Yes, always — source name + URL in KB** | Matches channel's academic sourcing philosophy |
| Agent access scope | **script-writer-v2 reads KB; other agents optional** | Highest value integration point |
| Topic overlap alerting | **Yes: flag if new video = same topic as planned video** | Prevents duplicate effort |
| Competitor lookback | **30 days default (last refresh window)** | RSS gives 15 videos; most channels upload < 15/month |
| Channel management | **config JSON file (tools/intel/competitor_channels.json)** | Simple, version-controlled, no separate command needed |
| Infrastructure sharing | **Separate from /patterns** | /patterns = own channel data; /intel = external intelligence |

---

## Open Questions

1. **Creator Insider Channel ID Verification**
   - What we know: Creator Insider is YouTube's official creator-facing channel
   - What's unclear: Need to verify exact channel ID (UCr-pWa7LMHX71Uhr7D4wqMQ is approximate)
   - Recommendation: Planner should include a task to verify and hardcode this before algo_scraper.py is built

2. **Competitor Channel ID Verification**
   - What we know: Approximate channel IDs were found for style-match competitors
   - What's unclear: Several IDs (especially Historia Civilis, HistoryMarche) need verification from YouTube page source
   - Recommendation: Build channel ID lookup utility or verify manually during planning

3. **LLM Synthesis Integration Method**
   - What we know: notebooklm_bridge.py (Phase 42.1) established the pattern for Claude Code LLM calls
   - What's unclear: Whether algo_synthesizer.py should call the same bridge or implement direct API call
   - Recommendation: Reuse notebooklm_bridge.py pattern for consistency; the bridge already handles the anthropic SDK setup

4. **Algorithm Source HTML Parsing Depth**
   - What we know: Simple `requests` can fetch blog HTML; the text content contains the algorithm intelligence
   - What's unclear: Some modern blogs use JavaScript rendering (React/Next.js), making static requests miss content
   - Recommendation: Test vidIQ and OutlierKit URLs with simple requests during implementation. If JS-rendered, add playwright as optional fallback (not primary).

5. **How script-writer-v2 accesses KB: path resolution**
   - What we know: Agent reads files at relative paths
   - What's unclear: Whether `channel-data/youtube-intelligence.md` resolves correctly from agent context
   - Recommendation: Use the same absolute path pattern as other reference files in script-writer-v2 (all use `.claude/REFERENCE/` or `channel-data/` relative paths)

---

## Sources

### Primary (HIGH confidence)
- vidIQ Algorithm Guide (https://vidiq.com/blog/post/understanding-youtube-algorithm/) — algorithm signal weights, CTR/AVD thresholds
- OutlierKit Algorithm Updates (https://outlierkit.com/resources/youtube-algorithm-updates/) — 2026 ranking factor table, satisfaction signal shift
- marketingagent.blog satisfaction signals (https://marketingagent.blog/2025/11/04/youtubes-recommendation-algorithm-satisfaction-signals-what-you-can-control/) — shadow metrics, named signal types (WSS, QCR, RD, VLI)
- YouTube RSS feed documentation — `https://www.youtube.com/feeds/videos.xml?channel_id=CHANNEL_ID` is officially supported
- YouTube Data API v3 quota documentation (developers.google.com) — 1 unit per videos.list, 100 units per search.list
- scrapetube GitHub (github.com/dermasmid/scrapetube) — v2.6.0 released September 2025, 489 stars, confirmed active
- feedparser PyPI (pypi.org/project/feedparser) — actively maintained RSS/Atom parser

### Secondary (MEDIUM confidence)
- Buffer YouTube Algorithm Guide (buffer.com/resources/youtube-algorithm/) — satisfaction signals, browse vs. search distinction
- Medium/YouTube Algorithm 2026 (medium.com) — small channel prioritization claim
- feedspot/async.com — history channel lists for competitor identification
- similarchannels.com — Fall of Civilizations audience overlap data

### Tertiary (LOW confidence)
- Specific competitor channel IDs — sourced from multiple forum/wiki references, need verification
- Algorithm signal weight percentages — synthesized from multiple secondary sources; not from official YouTube documentation

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all libraries verified as installed or pip-installable; YouTube RSS is an officially documented URL format
- Architecture: HIGH — patterns drawn from existing codebase conventions (error dict, auth.py reuse, SQLite schema patterns from keywords.db)
- Algorithm mechanics: MEDIUM — sourced from credible industry blogs, not YouTube's internal documentation (which is not public)
- Competitor channels: MEDIUM — channel list researched but IDs need verification
- Pitfalls: HIGH — RSS 15-video limit and API quota math are verifiable facts; others from standard engineering experience

**Research date:** 2026-02-20
**Valid until:** 2026-03-20 (algorithm landscape stable; competitor channel IDs permanent once verified)
