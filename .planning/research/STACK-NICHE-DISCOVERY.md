# Technology Stack: Niche Discovery Additions (v1.3)

**Project:** History vs Hype YouTube Workspace
**Research Domain:** Stack additions for v1.3 niche discovery milestone
**Researched:** 2026-01-31
**Overall Confidence:** HIGH

---

## Executive Summary

This research focuses on stack additions needed for v1.3 niche discovery capabilities. The existing stack (~9,000 lines Python) already includes YouTube Data API v3, YouTube Analytics API v2, OAuth2 authentication, and SQLite for keyword storage.

**Core Finding:** Add 3 lightweight libraries for demand research and competitor analysis. Avoid paid tools (VidIQ/TubeBuddy API). Extend existing `tools/discovery/` module with new demand and competition capabilities.

**Integration Strategy:** Build on validated v1.2 foundation (YouTube APIs, SQLite, OAuth2). Add demand research layer (Google Trends), enhance competition analysis (YouTube scraping fallback), implement opportunity scoring formula.

---

## Recommended Stack Additions

### Demand Research Layer

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| **trendspyg** | 0.3.0+ | Google Trends data | pytrends archived April 2025. trendspyg is actively maintained replacement with 188K+ config options, CLI + Python API, real-time trending searches. FREE unlimited usage |
| **python-youtube** | 0.9.8+ | YouTube Data API wrapper | Cleaner interface than raw google-api-python-client. Modern `pyyoutube.Client` API for channel/video metadata. Simplifies quota management |
| **scrapetube** | Latest (Jan 2026) | YouTube scraping (no API quota) | Scrapes channels/playlists/search WITHOUT YouTube API quota consumption. Fallback when 10K daily quota exhausted. Updated Jan 2026, actively maintained |

### Data Analysis Layer (Already Exists)

| Technology | Current Version | Purpose | Notes |
|------------|-----------------|---------|-------|
| **pandas** | 2.3.3+ | Data manipulation | Already in use for analytics. Reuse for opportunity scoring calculations |
| **numpy** | 2.4.1+ | Numerical operations | Already in use. Latest version (Jan 10, 2026) |
| **SQLite** | Built-in | Keyword/trend storage | Already used in `tools/discovery/keywords.db`. Extend schema for trends + competitor cache |

### Database Layer Extensions

Extend existing SQLite schema in `tools/discovery/keywords.db`:

```sql
-- Trend data from trendspyg
CREATE TABLE trends (
    keyword TEXT,
    timestamp INTEGER,
    interest INTEGER,      -- 0-100 scale from Google Trends
    region TEXT,
    source TEXT DEFAULT 'trendspyg',
    PRIMARY KEY (keyword, timestamp, region)
);

-- Competitor channel cache (avoid redundant API calls)
CREATE TABLE competitor_channels (
    channel_id TEXT PRIMARY KEY,
    channel_name TEXT,
    subscriber_count INTEGER,
    view_count INTEGER,
    video_count INTEGER,
    last_updated INTEGER
);

-- Competitor video cache
CREATE TABLE competitor_videos (
    video_id TEXT PRIMARY KEY,
    channel_id TEXT,
    title TEXT,
    view_count INTEGER,
    like_count INTEGER,
    comment_count INTEGER,
    duration_seconds INTEGER,
    published_at INTEGER,
    last_updated INTEGER,
    FOREIGN KEY (channel_id) REFERENCES competitor_channels(channel_id)
);

-- Opportunity scores (reusable across research sessions)
CREATE TABLE opportunity_scores (
    topic TEXT PRIMARY KEY,
    demand_score REAL,        -- 0-4 (from trends)
    competition_score REAL,   -- 0-4 (inverse of saturation)
    fit_score REAL,           -- 0-4 (document-friendly)
    hook_score REAL,          -- 0-4 (modern relevance)
    total_score REAL,         -- Sum (max 16)
    calculated_at INTEGER
);
```

---

## Installation Commands

### Core Additions (Required)

```bash
# Demand research
pip install trendspyg[cli,analysis]>=0.3.0

# YouTube Data API wrapper
pip install python-youtube>=0.9.8

# YouTube scraping fallback (no API quota)
pip install scrapetube
```

### Verify Existing Dependencies (Should Already Be Installed)

```bash
# From v1.2 script-checkers and analytics
pip install pandas>=2.3.0
pip install numpy>=2.4.0

# From v1.1 YouTube Analytics API
pip install google-api-python-client
pip install google-auth-oauthlib
pip install google-auth-httplib2
```

### Environment Variables (No Changes Needed)

Existing OAuth2 flow already has `youtube.readonly` scope for YouTube Data API v3. No new API keys required.

---

## What NOT to Add (And Why)

### ❌ pytrends (Google Trends library)

**Why avoid:**
- **CRITICAL:** Archived April 17, 2025 with no official replacement
- No maintenance, known issues unaddressed
- Breaks frequently when Google changes backend
- "Not built for scale, reliability, or production use"

**Alternative:** trendspyg (modern replacement, 188K+ configurations, actively maintained)

**Confidence:** HIGH — Multiple sources confirm pytrends deprecation

**Sources:**
- [pytrends Archive Notice](https://github.com/GeneralMills/pytrends) — Archived April 17, 2025
- [Top 4 Pytrends Alternatives 2026](https://meetglimpse.com/software-guides/pytrends-alternatives/) — Why pytrends deprecated
- [trendspyg GitHub](https://github.com/flack0x/trendspyg) — Modern replacement with active maintenance

### ❌ Official Google Trends API (Alpha)

**Why avoid:**
- Still in limited alpha as of Jan 2026
- Requires application + approval (prioritizes researchers/journalists)
- "Won't be publicly available for another year" (as of Jan 2026)
- Restricted quotas, limited endpoints

**Alternative:** trendspyg (free, unlimited, no approval needed)

**When to reconsider:** If Google opens public access OR channel grows to enterprise scale

**Confidence:** HIGH — Official API not production-ready for solo creators

**Sources:**
- [Google Trends API Alpha Launch](https://blogs.garudmarketing.com/google-trends-api-alpha-launch/) — Application process, limitations
- [Google's July 2025 Update: The Google Trends API](https://thatware.co/july-2025-update-google-trends-api/) — Current alpha status

### ❌ VidIQ/TubeBuddy Paid API Access

**Why avoid:**
- VidIQ API only available at enterprise tier ($500+/year)
- TubeBuddy has no public API
- Would require browser automation (fragile, detection-prone)
- Channel already has VidIQ Pro subscription for manual use
- Can build equivalent scoring with free tools (YouTube Data API + Google Trends)

**Alternative approach:**
- Use VidIQ manually for inspiration and validation
- Build custom opportunity scoring with free APIs
- Cost: $0 (within existing API quotas)

**Confidence:** HIGH — VidIQ/TubeBuddy are manual tools, not programmatic APIs

**Sources:**
- [Best YouTube Analytics Tools 2026](https://outlierkit.com/blog/best-youtube-analytics-tools) — Tool comparison
- [VidIQ vs TubeBuddy](https://outlierkit.com/blog/vidiq-vs-tubebuddy) — Pricing and API availability

### ❌ Heavy ML Libraries (TensorFlow, PyTorch, scikit-learn)

**Why avoid:**
- Overkill for opportunity scoring (simple formula: demand × gap × fit / effort)
- Large dependencies (~500MB+ each for TF/PyTorch)
- Slow installation, potential version conflicts
- Rule-based filters sufficient for format compatibility

**Alternative approach:**
- Use pandas + numpy for scoring calculations (already installed)
- Implement scoring formula directly (no ML needed)
- Detection heuristics for animation requirements (title patterns, channel analysis)

**Confidence:** HIGH — Problem doesn't require ML complexity

### ❌ Web Scraping Frameworks (Scrapy, Selenium)

**Why avoid:**
- Already have pyppeteer for YouTube autocomplete (v1.2, working)
- scrapetube handles YouTube scraping without browser automation
- Scrapy is overkill for simple API/scraping tasks
- Selenium requires browser driver maintenance

**Current approach (keep):**
- pyppeteer + pyppeteer-stealth for autocomplete (already working in v1.2)
- scrapetube for channel/video scraping (lightweight, no browser)
- YouTube Data API for metadata (official, reliable)

**Confidence:** HIGH — Current tools cover use cases

---

## Integration Points with Existing Stack

### 1. Extend `tools/discovery/` Module

**Current structure (v1.2):**
```
tools/discovery/
├── autocomplete.py       # YouTube autocomplete scraper (pyppeteer)
├── intent_mapper.py      # 6-category intent classification
├── metadata_checker.py   # Pre-publish validation
├── diagnostics.py        # CTR vs impressions analysis
├── keywords.py           # Keyword extraction
├── database.py           # SQLite keyword storage
└── vidiq_workflow.py     # VidIQ manual workflow guide
```

**Add for v1.3:**
```
tools/discovery/
├── demand_research.py       # NEW: trendspyg integration for search volume
├── competitor_analysis.py   # NEW: python-youtube + scrapetube for competition
├── opportunity_scorer.py    # NEW: Scoring formula (demand × gap × fit)
└── format_filter.py         # NEW: Document-friendly vs animation detection
```

### 2. YouTube Data API Quota Management

**Current quota:** 10,000 units/day (default free tier)
**Reset:** Midnight Pacific Time

**Quota costs for niche discovery operations:**

| Operation | Quota Cost | Use Case |
|-----------|------------|----------|
| `search.list` | 100 units | Find videos on topic (competitor analysis) |
| `videos.list` | 1 unit | Get video metadata (batch 50 videos per call) |
| `channels.list` | 1 unit | Get channel statistics |
| `comments.list` | 1 unit | Analyze audience questions (already used in v1.1) |

**Quota budget example (niche discovery session):**
- Search 10 topics: 10 × 100 = 1,000 units
- Get metadata for 500 videos: 10 batches × 1 = 10 units (batched)
- Get 10 channel stats: 10 units
- **Total:** ~1,020 units (10% of daily quota)

**Efficiency strategies:**
1. **Cache aggressively** — Store channel/video data in SQLite (avoid duplicate API calls)
2. **Batch requests** — Request 50 video IDs per `videos.list` call (costs 1 unit, not 50)
3. **Fallback to scrapetube** — When quota exhausted, use scrapetube (no quota cost)
4. **Stale data acceptable** — Competitor metrics don't need real-time updates (cache for 7 days)

**Request quota increase (if needed):**
1. Complete compliance audit (show Terms of Service compliance)
2. Submit form: https://support.google.com/youtube/contact/yt_api_form
3. Provide realistic estimates with calculations
4. Show track record of responsible usage (v1.1 analytics already using API responsibly)

**Cost:** Free (approval based on merit and compliance, no fees)

**Confidence:** HIGH — Official process, existing API usage demonstrates compliance

**Sources:**
- [YouTube Data API Quota Calculator](https://developers.google.com/youtube/v3/determine_quota_cost) — Official quota costs
- [Quota and Compliance Audits](https://developers.google.com/youtube/v3/guides/quota_and_compliance_audits) — How to request increases
- [YouTube API Limits Guide](https://www.getphyllo.com/post/youtube-api-limits-how-to-calculate-api-usage-cost-and-fix-exceeded-api-quota) — Best practices

### 3. OAuth2 Flow (Already Working)

**Current implementation:** `tools/youtube-analytics/auth.py`
- Desktop app flow (port 8080)
- Token refresh automatic
- Credentials in `tools/youtube-analytics/credentials/`
- Scopes: `yt-analytics.readonly`, `youtube.readonly`

**No changes needed** — Existing auth already has `youtube.readonly` scope for YouTube Data API v3

**Confidence:** HIGH — v1.1 integration validates auth works

### 4. Rate Limiting for trendspyg

**Built-in rate limiting:**
- trendspyg includes respectful delays between requests
- Random jitter to avoid patterns
- Exponential backoff on errors
- Respects Google's robots.txt

**Best practices:**
- Don't hammer endpoints (defeats anti-detection measures)
- Batch queries when possible (1 query for multiple keywords)
- Cache results in SQLite (trends don't change minute-to-minute)
- Max 1-2 queries per minute (respectful rate)

**No quota limits** — trendspyg scrapes public Google Trends pages (free, unlimited)

**Confidence:** HIGH — trendspyg designed for responsible scraping

**Sources:**
- [trendspyg GitHub](https://github.com/flack0x/trendspyg) — Rate limiting documentation
- [How to Scrape Google Trends 2026](https://brightdata.com/blog/web-data/how-to-scrape-google-trends) — Best practices

---

## Recommended Implementation Approach

### Phase 1: Demand Research (Week 1)

**Add:** `tools/discovery/demand_research.py`

**Features:**
- Query Google Trends via trendspyg
- Get interest over time (5 years rolling window, weekly aggregation)
- Get related queries and rising topics
- Cache in SQLite `trends` table

**Example usage:**
```python
from tools.discovery.demand_research import get_trend_data

result = get_trend_data("medieval flat earth myth")
# Returns: {
#   'interest_over_time': [...],  # 5 years weekly data
#   'related_queries': [...],     # "flat earth medieval", etc.
#   'rising_queries': [...],      # Trending variations
#   'peak_interest': 73,          # Max interest score (0-100)
#   'avg_interest': 42,           # Mean interest score
#   'demand_score': 3.0           # 0-4 scale for scoring formula
# }
```

**Scoring formula:**
```python
# Convert Google Trends interest (0-100) to demand score (0-4)
if avg_interest >= 75:
    demand_score = 4.0  # High demand
elif avg_interest >= 50:
    demand_score = 3.0  # Medium-high demand
elif avg_interest >= 25:
    demand_score = 2.0  # Medium demand
else:
    demand_score = 1.0  # Low demand
```

### Phase 2: Competition Analysis (Week 2)

**Add:** `tools/discovery/competitor_analysis.py`

**Features:**
- Search YouTube for topic keywords (YouTube Data API)
- Get top 20 videos per topic
- Analyze: views, engagement, channel size, upload frequency
- Identify gaps (topics with high demand, low competition)
- Fall back to scrapetube if quota issues

**Example usage:**
```python
from tools.discovery.competitor_analysis import analyze_competition

result = analyze_competition("medieval literacy rates")
# Returns: {
#   'total_videos': 847,
#   'top_videos': [...],              # Top 20 by views
#   'avg_views': 12500,
#   'channel_sizes': [234000, 1200000, 45000, ...],
#   'saturation_score': 6.2,          # 0-10 scale (10 = saturated)
#   'competition_score': 2.4,         # 0-4 scale (inverse of saturation)
#   'gap_opportunity': 'medium'       # low/medium/high
# }
```

**Scoring formula:**
```python
# Convert saturation (0-10) to competition score (0-4)
# High saturation = low competition score
competition_score = 4.0 - (saturation_score * 0.4)

# Saturation factors:
# - Number of videos on topic (>1000 = saturated)
# - Channel sizes (many 1M+ channels = saturated)
# - Recent uploads (active niche = saturated)
# - View distribution (few top performers = gap opportunity)
```

**API quota fallback:**
```python
def get_video_list(topic, use_api=True):
    """Get videos with fallback to scrapetube"""
    if use_api and quota_available():
        # Use YouTube Data API (costs 100 units)
        return youtube_api_search(topic)
    else:
        # Fall back to scrapetube (no quota cost)
        return scrapetube_search(topic)
```

### Phase 3: Format Filtering (Week 3)

**Add:** `tools/discovery/format_filter.py`

**Features:**
- Analyze top videos for format requirements
- Flag: Animation-heavy, infographics, talking head, documentary
- Score: Document-friendliness (0-4)

**Detection heuristics:**
1. **Title patterns:**
   - "explained with animation" → animation required
   - "animated history" → animation required
   - "documentary" → document-friendly

2. **Channel analysis:**
   - Kurzgesagt, RealLifeLore → animation-focused
   - History Matters → animation-focused
   - Fall of Civilizations, Kraut → document-friendly

3. **Video duration vs content density:**
   - 10 min video with 50+ visual sources → document-friendly
   - 10 min video with 5 sources → likely animation-heavy

**Example usage:**
```python
from tools.discovery.format_filter import assess_format_fit

result = assess_format_fit("Sykes-Picot agreement")
# Returns: {
#   'format_type': 'documentary',
#   'animation_required': False,
#   'document_friendly': True,
#   'fit_score': 4.0,              # Perfect fit for channel
#   'reasoning': 'Top videos show treaty documents, maps, historical photos. Primary sources exist and are visually compelling.'
# }
```

**Scoring formula:**
```python
# Document-friendliness score (0-4)
if animation_required:
    fit_score = 1.0  # Poor fit (channel can't produce animations)
elif top_videos_show_documents:
    fit_score = 4.0  # Perfect fit (evidence-based format)
elif mixed_format:
    fit_score = 2.5  # Possible but challenging
else:
    fit_score = 1.5  # Unclear fit
```

### Phase 4: Opportunity Scoring (Week 4)

**Add:** `tools/discovery/opportunity_scorer.py`

**Features:**
- Combine demand (trends) + competition (saturation) + format fit + modern hook
- Calculate total score (max 16, matching existing gap scoring from v1.0)
- Rank topics

**Formula (from v1.0 Key Decisions in PROJECT.md):**
```
Score = Demand (0-4) + Competition (0-4) + Fit (0-4) + Hook (0-4)
Max: 16 points

Demand: Google Trends interest (0-24 = 1, 25-49 = 2, 50-74 = 3, 75-100 = 4)
Competition: Inverse saturation (many big channels = 1, gaps = 4)
Fit: Document-friendliness (animation required = 1, docs exist = 4)
Hook: Modern relevance (historical only = 1, active news hook = 4)
```

**Example usage:**
```python
from tools.discovery.opportunity_scorer import score_topic

result = score_topic("Chagos Islands UK treaty 2024")
# Returns: {
#   'topic': 'Chagos Islands UK treaty 2024',
#   'demand_score': 3.5,          # Rising interest (treaty news)
#   'competition_score': 3.0,     # Few quality videos
#   'fit_score': 4.0,             # Treaty documents available
#   'hook_score': 4.0,            # Active news (2024 treaty)
#   'total_score': 14.5,          # High opportunity
#   'recommendation': 'Strong candidate - high demand, low competition, perfect format fit, current news hook'
# }
```

**Hook scoring (manual input for now):**
```python
# Modern relevance hook (0-4)
# User specifies news hook when scoring topic

hook_types = {
    'active_news': 4.0,        # Current events, ongoing
    'recent_event': 3.0,       # 2023-2025 event
    'recurring_debate': 2.5,   # Evergreen but active
    'historical_only': 1.0     # No modern connection
}
```

---

## API Limits and Quotas Summary

### YouTube Data API v3

**Daily quota:** 10,000 units (free tier)
**Reset:** Midnight Pacific Time
**Current usage (v1.1):** ~300-500 units/day (analytics, comments)
**New usage (v1.3):** ~1,000 units per niche discovery session
**Budget headroom:** 8,000+ units/day available

**Mitigation strategies:**
- Cache competitor data (7-day TTL)
- Batch video metadata requests (50 per call)
- Fall back to scrapetube when quota low
- Request increase if needed (free, approval-based)

**Confidence:** HIGH — Sufficient quota for solo creator workflow

### Google Trends (via trendspyg)

**Quota:** None (scrapes public pages)
**Rate limiting:** Built-in respectful delays
**Cost:** Free, unlimited

**Best practices:**
- 1-2 queries per minute max
- Cache results (trends stable over days)
- Batch keywords when possible

**Confidence:** HIGH — Free, unlimited, maintained library

### scrapetube (YouTube scraping fallback)

**Quota:** None (scrapes public YouTube pages)
**Rate limiting:** None documented, use respectfully
**Cost:** Free

**Use cases:**
- Fallback when YouTube Data API quota exhausted
- Bulk video list retrieval (thousands of videos)
- Channel history analysis (all uploads)

**Confidence:** HIGH — Actively maintained, updated Jan 2026

**Sources:**
- [scrapetube GitHub](https://github.com/dermasmid/scrapetube) — Updated Jan 6, 2026
- [scrapetube Package Health](https://snyk.io/advisor/python/scrapetube) — Maintenance confirmation

---

## Version Verification Notes

All versions verified via web search on 2026-01-31:

**New libraries (v1.3):**
- **trendspyg 0.3.0**: Latest on PyPI (actively maintained)
  - Source: [trendspyg PyPI](https://libraries.io/pypi/trendspyg) — Version 0.3.0 confirmed
- **python-youtube 0.9.8**: Released 2025-08-22 (latest available)
  - Source: [python-youtube PyPI](https://pypi.org/project/python-youtube/) — Version 0.9.8 confirmed
- **scrapetube**: Updated 2026-01-06 (active maintenance)
  - Source: [scrapetube GitHub](https://github.com/dermasmid/scrapetube) — Jan 6, 2026 update confirmed

**Existing libraries (v1.2, verify current):**
- **pandas 2.3.3**: Current stable (released 2025-06-05)
  - Source: [pandas Release Notes](https://pandas.pydata.org/docs/whatsnew/index.html)
- **numpy 2.4.1**: Latest (released 2026-01-10)
  - Source: [NumPy News](https://numpy.org/news/) — Version 2.4.1 Jan 10, 2026
- **matplotlib 3.10.0**: Current (released 2024-12-14)
  - Source: [Matplotlib Dependency Policy](https://matplotlib.org/devdocs/devel/min_dep_policy.html)

**CRITICAL deprecation:**
- **pytrends**: Archived April 17, 2025 — DO NOT USE
  - Source: [pytrends GitHub](https://github.com/GeneralMills/pytrends) — Archive notice confirmed

---

## Alternatives Considered

| Category | Recommended | Alternative | Why Not Alternative |
|----------|-------------|-------------|---------------------|
| Google Trends | trendspyg | pytrends | Archived April 2025, no maintenance, breaks frequently |
| Google Trends | trendspyg | Official API (alpha) | Limited access, requires approval, won't be public for ~1 year |
| Google Trends | trendspyg | SerpApi/Glimpse (paid) | $29-99/mo, trendspyg is free and sufficient for solo creator |
| YouTube wrapper | python-youtube | google-api-python-client | Raw client verbose, python-youtube cleaner interface |
| YouTube scraping | scrapetube | yt-dlp | yt-dlp for downloads, scrapetube specialized for metadata scraping |
| YouTube scraping | scrapetube | Selenium/Scrapy | Heavier dependencies, scrapetube lightweight and sufficient |
| YouTube scraping | scrapetube | pyppeteer (v1.2) | Already using pyppeteer for autocomplete, scrapetube complements (different use cases) |
| Niche research | Build custom | VidIQ API | $500+/year for API access, can build equivalent with free tools |
| Niche research | Build custom | TubeBuddy API | No public API, would require fragile browser automation |
| Data analysis | pandas + numpy | scikit-learn/ML | Overkill for scoring formula, rule-based sufficient |

---

## Migration Notes (From v1.2 to v1.3)

### No Breaking Changes

**Existing stack continues to work:**
- `tools/youtube-analytics/` — No changes needed
- `tools/discovery/autocomplete.py` — Keep using pyppeteer (v1.2)
- `tools/discovery/intent_mapper.py` — Keep as-is
- OAuth2 flow — Already has `youtube.readonly` scope

### Additive Integration

**New modules extend existing:**
- Add 4 new Python files to `tools/discovery/`
- Extend SQLite schema (new tables, no migration of existing data needed)
- New CLI commands: `/discover --demand TOPIC`, `/discover --competitors TOPIC`

### Dependency Conflicts

**Watch for:**
- Python 3.14 + spaCy incompatibility (noted in PROJECT.md tech debt)
  - Solution: Use Python 3.11-3.13 for now
- trendspyg, python-youtube, scrapetube all support Python 3.6+ (no conflicts)

**No conflicts expected** — All new libraries are lightweight, pure Python or minimal C extensions

**Confidence:** HIGH — Additive changes, no replacements

---

## Testing Strategy

### Unit Tests

```python
# tests/test_demand_research.py
def test_trendspyg_integration():
    """Verify trendspyg returns valid trend data"""
    result = get_trend_data("dark ages myth")
    assert 'interest_over_time' in result
    assert isinstance(result['peak_interest'], (int, float))
    assert 0 <= result['demand_score'] <= 4

# tests/test_competitor_analysis.py
def test_youtube_api_search():
    """Verify YouTube Data API search works"""
    result = analyze_competition("medieval literacy")
    assert 'total_videos' in result
    assert result['total_videos'] > 0
    assert 0 <= result['competition_score'] <= 4

# tests/test_format_filter.py
def test_animation_detection():
    """Verify animation requirement detection"""
    result = assess_format_fit("Kurzgesagt evolution")
    assert result['animation_required'] == True
    assert result['fit_score'] < 2.0  # Poor fit for channel

# tests/test_opportunity_scorer.py
def test_end_to_end_scoring():
    """Verify full pipeline: trends → competition → format → scoring"""
    topic = "Chagos Islands UK treaty"
    score = score_topic(topic)
    assert 0 <= score['total_score'] <= 16
    assert 'recommendation' in score
```

### Integration Tests

```python
# tests/test_quota_fallback.py
def test_scrapetube_fallback():
    """Verify scrapetube fallback works when quota exhausted"""
    # Mock quota exhaustion
    with mock.patch('quota_available', return_value=False):
        result = get_video_list("test topic", use_api=True)
        # Should fall back to scrapetube, not fail
        assert len(result) > 0

# tests/test_cache_usage.py
def test_competitor_cache():
    """Verify SQLite cache reduces API calls"""
    # First call hits API
    analyze_competition("topic1")
    api_calls_1 = count_api_calls()

    # Second call (same topic) uses cache
    analyze_competition("topic1")
    api_calls_2 = count_api_calls()

    assert api_calls_2 == api_calls_1  # No new API calls
```

### Manual Testing Checklist

- [ ] Run demand research on known topics (verify scores match reality)
- [ ] Compare competitor analysis with manual VidIQ check
- [ ] Validate opportunity scores against actual video performance (historical data)
- [ ] Test quota fallback (intentionally exhaust quota, verify scrapetube works)
- [ ] Verify SQLite cache (second query should be instant)
- [ ] Check format detection (animation channels vs documentary channels)

---

## Deployment Checklist

- [ ] Install trendspyg with CLI extras: `pip install trendspyg[cli,analysis]`
- [ ] Install python-youtube: `pip install python-youtube>=0.9.8`
- [ ] Install scrapetube: `pip install scrapetube`
- [ ] Verify existing YouTube OAuth still works (no re-auth needed)
- [ ] Test trendspyg CLI: `trendspyg "dark ages myth"`
- [ ] Create new SQLite tables (see schema above)
- [ ] Add 4 new Python modules to `tools/discovery/`
- [ ] Update command system with `/discover --demand`, `/discover --competitors`
- [ ] Document quota usage expectations in `.planning/codebase/`
- [ ] Test quota fallback (scrapetube when API exhausted)
- [ ] Update `PROJECT.md` with v1.3 validated capabilities

---

## Cost Estimates

### Monthly Operating Costs (Solo Creator, 1-2 videos/month)

| Service | Usage | Cost | Notes |
|---------|-------|------|-------|
| **trendspyg (Google Trends)** | ~20 queries/month | FREE | Unlimited, no API key needed |
| **YouTube Data API** | 10,000 units/day quota | FREE | Already allocated in v1.1 |
| **scrapetube** | Fallback usage only | FREE | No quota, scrapes public pages |
| **python-youtube** | Wrapper around YouTube API | FREE | Library, not service |
| **SQLite** | Local database | FREE | Built into Python |

**Total New Costs: $0/month**

**One-Time Costs:** $0 (all open source, no paid tiers needed)

### Quota Usage Estimates

**Per niche discovery session (10 topics):**
- Demand research (trendspyg): 0 API units (no YouTube API usage)
- Competition analysis (YouTube Data API): ~1,020 units
- Format filtering (analyze cached videos): 0 units (uses cache)
- Opportunity scoring (calculation only): 0 units (local)

**Daily budget:** 10,000 units
**Sessions per day:** ~9 sessions before quota exhausted (then fall back to scrapetube)

**Realistic usage:** 1-2 discovery sessions per week = ~2,000-4,000 units/week (well within quota)

---

## Risk Assessment

### Technical Risks

| Risk | Severity | Likelihood | Mitigation |
|------|----------|-----------|------------|
| trendspyg breaks (Google backend change) | MEDIUM | LOW | Active maintenance, community fixes quickly. Fall back to manual Google Trends |
| YouTube Data API quota exhausted | LOW | LOW | Fallback to scrapetube (no quota cost). Request increase if needed (free) |
| scrapetube detection/blocking | LOW | LOW | Library maintained, no evidence of blocking. Fall back to API if issues |
| Format detection false positives | MEDIUM | MEDIUM | Heuristics tunable, human review remains final decision |
| Opportunity scores don't correlate with success | MEDIUM | MEDIUM | Track metrics vs. performance, iterate scoring formula |

### Integration Risks

| Risk | Severity | Likelihood | Mitigation |
|------|----------|-----------|------------|
| SQLite schema conflicts | LOW | LOW | New tables only, no changes to existing schema |
| Dependency version conflicts | LOW | LOW | All libraries support Python 3.6+, minimal dependencies |
| Command system complexity | MEDIUM | MEDIUM | Clear flag-based organization, comprehensive help text |

### Workflow Risks

| Risk | Severity | Likelihood | Mitigation |
|------|----------|-----------|------------|
| Over-reliance on automation reduces editorial judgment | MEDIUM | MEDIUM | Tools inform, don't decide. Opportunity scores are suggestions, not mandates |
| False confidence from metrics | LOW | MEDIUM | Validate scores against historical data. Track prediction accuracy |
| Tool maintenance burden | LOW | LOW | Minimal dependencies, stable libraries. trendspyg + scrapetube actively maintained |

---

## Future Considerations (Out of Scope for v1.3)

### Later Milestones

**If demand grows:**
- Apply for Google Trends API alpha access (more reliable, structured data)
- Request YouTube Data API quota increase (>10K/day) if hitting limits
- Add visualization dashboard (matplotlib charts for trend analysis)

**If analysis gets complex:**
- Add scipy for statistical analysis (correlation between scores and performance)
- Consider lightweight ML for pattern detection (only if rule-based insufficient)
- Implement A/B testing framework (compare opportunity scores vs. actual performance)

**Integration opportunities:**
- NotebookLM Enterprise API (when available) for source-based topic validation
- YouTube Analytics API for retention heatmap prediction (requires 30+ videos with data)
- Automated topic refresh (monthly re-scoring of topic database)

### NOT Recommended

- VidIQ/TubeBuddy paid subscriptions (already have VidIQ Pro for manual use, API not available)
- Heavy ML frameworks (overkill for scoring formula)
- Custom web scraping beyond scrapetube (maintenance burden, detection risk)
- Real-time monitoring dashboards (batch analysis sufficient for solo creator)
- Predictive analytics (CLAUDE.md explicitly excludes: "focus on learning, not prediction")

---

## Success Metrics

### How to Measure If This Stack Works

| Goal | Metric | Target | Measurement |
|------|--------|--------|-------------|
| **Topic validation** | Topics with >10K monthly searches identified | 50%+ of research sessions | Demand research module |
| **Gap identification** | Low-competition topics found | 2-3 per month | Opportunity scorer |
| **Time savings** | Topic research time | <1 hour (down from 2-3 hours) | Manual tracking |
| **Format filtering** | Animation-required topics flagged | 90%+ accuracy | Manual validation vs. actual videos |
| **Opportunity scoring** | High-scoring topics (12+) perform better | 2x better than low-scoring | Analytics correlation |
| **Quota efficiency** | API quota exhaustion | <1x per month | Quota monitoring |

### What "Good" Looks Like

**Demand Research:**
- Trend data available within 30 seconds per topic
- Related queries reveal adjacent topic opportunities
- Historical trends show whether topic is rising/stable/declining

**Competition Analysis:**
- Top 20 competitors identified with view counts, channel sizes
- Gap opportunities flagged (topics with demand but few quality videos)
- Format requirements clear (animation vs. documentary)

**Opportunity Scoring:**
- Topics ranked objectively (not just gut feeling)
- High-scoring topics (12-16) produce 2x better results than low-scoring
- Scores inform decision, human judgment remains

**Workflow:**
- Niche discovery takes <1 hour (down from 2-3 hours manual research)
- SQLite cache makes second queries instant
- Quota fallback seamless (user doesn't notice API vs. scraping)

---

## Confidence Assessment

| Area | Confidence Level | Reason |
|------|------------------|--------|
| **trendspyg** | HIGH | Actively maintained replacement for archived pytrends. 188K+ configs, CLI + Python API |
| **python-youtube** | HIGH | Official wrapper, well-documented, current version 0.9.8 (Aug 2025) |
| **scrapetube** | HIGH | Actively maintained (updated Jan 6, 2026), community-validated |
| **YouTube Data API integration** | HIGH | Already using in v1.1, OAuth2 working, quota sufficient |
| **SQLite schema extension** | HIGH | Simple additive changes, no migration complexity |
| **Opportunity scoring formula** | MEDIUM | Formula logical, needs validation against historical data |
| **Format detection heuristics** | MEDIUM | Rule-based approach reasonable, requires tuning |
| **Quota management** | HIGH | Fallback strategy (scrapetube) proven, cache reduces API calls |
| **Cost estimates** | HIGH | All tools free, no hidden costs, quota sufficient |
| **Integration complexity** | MEDIUM | 4 new modules, clear separation of concerns, additive only |

---

## Open Questions for Roadmap Creation

**Before building, clarify:**

1. **Scoring weights:** Should all 4 components (demand, competition, fit, hook) be weighted equally? Or prioritize format fit (channel constraint)?

2. **Hook scoring:** Modern relevance is manual input for now. Build automated news detection later, or keep manual?

3. **Cache TTL:** How long to cache competitor data? 7 days? 30 days? Trade-off: freshness vs. API quota

4. **Quota threshold:** At what quota level (e.g., 8,000/10,000 used) should we automatically fall back to scrapetube?

5. **Validation timeline:** How many topics to score before validating formula against historical performance? 20? 50?

6. **Batch vs. interactive:** Build as batch tool (score 10 topics at once) or interactive CLI (score 1 topic on demand)?

---

## Sources

### Library Documentation
- [trendspyg GitHub](https://github.com/flack0x/trendspyg) — Google Trends library (pytrends replacement)
- [trendspyg PyPI](https://libraries.io/pypi/trendspyg) — Version 0.3.0 confirmed
- [python-youtube PyPI](https://pypi.org/project/python-youtube/) — YouTube Data API wrapper, v0.9.8
- [scrapetube GitHub](https://github.com/dermasmid/scrapetube) — YouTube scraper, updated Jan 6, 2026
- [scrapetube Package Health](https://snyk.io/advisor/python/scrapetube) — Maintenance confirmation
- [pandas Documentation](https://pandas.pydata.org/docs/) — Data manipulation library
- [NumPy News](https://numpy.org/news/) — Version 2.4.1 (Jan 10, 2026)

### API Documentation
- [YouTube Data API Quota Calculator](https://developers.google.com/youtube/v3/determine_quota_cost) — Official quota costs
- [YouTube Data API Overview](https://developers.google.com/youtube/v3/getting-started) — API setup guide
- [Quota and Compliance Audits](https://developers.google.com/youtube/v3/guides/quota_and_compliance_audits) — How to request increases
- [YouTube API Limits Guide](https://www.getphyllo.com/post/youtube-api-limits-how-to-calculate-api-usage-cost-and-fix-exceeded-api-quota) — Best practices
- [Is the YouTube API Free?](https://www.getphyllo.com/post/is-the-youtube-api-free-costs-limits-iv) — Costs and limits

### Google Trends API
- [Google Trends API Alpha Launch](https://blogs.garudmarketing.com/google-trends-api-alpha-launch/) — Alpha details, application process
- [Google's July 2025 Update: The Google Trends API](https://thatware.co/july-2025-update-google-trends-api/) — Current status, limitations
- [Google Trends API Alpha Access](https://rankorbit.com/google-trends-api-alpha-search-insights/) — 5 years of data, quotas
- [How to Scrape Google Trends 2026](https://brightdata.com/blog/web-data/how-to-scrape-google-trends) — Best practices, trendspyg usage

### Niche Research Tools
- [Best YouTube Analytics Tools 2026](https://outlierkit.com/blog/best-youtube-analytics-tools) — VidIQ/TubeBuddy alternatives
- [VidIQ vs TubeBuddy](https://outlierkit.com/blog/vidiq-vs-tubebuddy) — Tool comparison, pricing, API availability
- [10 Best Niche Finder Tools For YouTube 2026](https://outlierkit.com/blog/best-niche-finder-tools-for-youtube) — Comprehensive tool overview
- [TubeLab Reviews 2026](https://outlierkit.com/blog/tubelab-reviews-features-alternatives) — API access comparison ($500+/year)

### Library Status
- [pytrends GitHub](https://github.com/GeneralMills/pytrends) — Archived April 17, 2025
- [Top 4 Pytrends Alternatives 2026](https://meetglimpse.com/software-guides/pytrends-alternatives/) — Why pytrends deprecated, trendspyg recommended
- [pytrends PyPI](https://pypi.org/project/pytrends/) — Last release April 13, 2023 (pre-archive)

### Technical References
- [YouTube Data API Search](https://developers.google.com/youtube/v3/docs/search/list) — Search endpoint documentation
- [pandas Release Notes](https://pandas.pydata.org/docs/whatsnew/index.html) — Version 2.3.3 (June 2025)
- [Matplotlib Dependency Policy](https://matplotlib.org/devdocs/devel/min_dep_policy.html) — Version 3.10.0 (Dec 2024)

---

*Research complete. Stack recommendations ready for roadmap creation.*
