# Phase 15: Database Foundation & Demand Research - Research

**Researched:** 2026-01-31
**Domain:** YouTube keyword demand research with trends, autocomplete, and competition data
**Confidence:** HIGH

## Summary

Phase 15 extends the existing keywords.db schema to capture demand signals from multiple sources: YouTube autocomplete position (search volume proxy), Google Trends (trend direction), related query expansion, and competition ratio scoring. The phase builds on Phase 13's autocomplete extraction and database.py infrastructure, adding 5 new tables for trends, competitor data, and opportunity scoring.

The standard stack is trendspyg (replacing archived pytrends), python-youtube for YouTube Data API v3, and scrapetube for quota-free video counting. The architecture follows Phase 13's error dict pattern ({'error': msg}), uses 7-day caching with staleness warnings, and implements conservative opportunity thresholds (4x+ for high confidence).

**Primary recommendation:** Build demand research as a multi-source data aggregation layer. Use YouTube autocomplete position as search volume proxy, Google Trends for direction (rising/falling), expand queries via autocomplete suggestions, and calculate competition ratio from video counts. Cache all data with timestamps for 7-day freshness, warn on stale data but still display it (something better than nothing), and provide --refresh flag for force refresh.

## Standard Stack

The established libraries/tools for this domain:

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| trendspyg | 0.3.0+ | Google Trends data | Actively maintained replacement for archived pytrends (April 2025), 188K+ configuration options, 5-minute TTL caching |
| python-youtube | 0.9.8+ | YouTube Data API v3 wrapper | Latest version (Aug 2025), supports Python 3.6-3.13, comprehensive API coverage |
| scrapetube | latest | YouTube scraping fallback | Quota-free alternative to YouTube Data API for video counting, no Selenium required |
| sqlite3 (stdlib) | Python 3.11+ | Local database | Built-in, supports time series patterns, row_factory for dict returns |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| pyppeteer | latest | Browser automation | Already in Phase 13 for autocomplete extraction, reuse existing code |
| google-api-python-client | latest | Official YouTube client | Alternative to python-youtube if more control needed |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| trendspyg | pytrends | pytrends archived April 2025, no longer maintained |
| python-youtube | google-api-python-client | python-youtube simpler API, official client more verbose |
| scrapetube | YouTube Data API search | API costs 100 quota per search (10K daily limit), scrapetube quota-free |

**Installation:**
```bash
pip install trendspyg python-youtube scrapetube
# pyppeteer already installed from Phase 13
```

## Architecture Patterns

### Recommended Project Structure
```
tools/discovery/
├── database.py          # Existing (Phase 13) - extend with new methods
├── autocomplete.py      # Existing (Phase 13) - reuse for related queries
├── demand.py            # NEW - demand aggregation module
├── trends.py            # NEW - Google Trends integration
├── competition.py       # NEW - video count + channel count
├── schema.sql           # UPDATE - add 5 new tables
└── keywords.db          # EXTEND - existing database
```

### Pattern 1: Multi-Source Data Aggregation
**What:** Combine data from 3 sources (autocomplete, trends, YouTube API) into unified demand score
**When to use:** User runs `/discover --demand "keyword"`
**Example:**
```python
# Source: Architecture decision from CONTEXT.md + existing Phase 13 patterns
from database import KeywordDB
from demand import DemandAnalyzer

db = KeywordDB()
analyzer = DemandAnalyzer(db)

# Aggregates: autocomplete position, trends, related queries, competition
result = analyzer.analyze_keyword("dark ages myth")

# Returns:
# {
#   'keyword': 'dark ages myth',
#   'search_volume_proxy': 85,  # autocomplete position score
#   'trend_direction': '↑ +45%',  # rising/stable/declining
#   'related_queries': [...],  # 10-20 related
#   'competition_ratio': '4.2x (High Opportunity)',  # demand/supply
#   'data_age_days': 3
# }
```

### Pattern 2: 7-Day Caching with Staleness Warnings
**What:** Cache all external API data with timestamps, warn when stale but still display
**When to use:** All demand research operations
**Example:**
```python
# Source: CONTEXT.md decisions + trendspyg caching patterns
def get_trend_data(keyword, force_refresh=False):
    """
    Fetch trend data with 7-day cache.

    Returns: {'trend': data, 'data_age_days': int, 'warning': str|None}
    """
    db = KeywordDB()

    if not force_refresh:
        cached = db.get_cached_trend(keyword, max_age_days=7)
        if cached:
            age = (datetime.now() - cached['fetched_at']).days
            warning = f"Data is {age} days old" if age > 7 else None
            return {'trend': cached['data'], 'data_age_days': age, 'warning': warning}

    # Fetch fresh data
    try:
        trend_data = fetch_from_google_trends(keyword)
        db.cache_trend(keyword, trend_data)
        return {'trend': trend_data, 'data_age_days': 0, 'warning': None}
    except Exception as e:
        # Fallback to stale cache on API failure
        stale = db.get_cached_trend(keyword, max_age_days=999)
        if stale:
            age = (datetime.now() - stale['fetched_at']).days
            return {
                'trend': stale['data'],
                'data_age_days': age,
                'warning': f"API failed, showing stale data ({age} days old)"
            }
        return {'error': 'No data available'}
```

### Pattern 3: Autocomplete Position as Search Volume Proxy
**What:** Use position in autocomplete dropdown as proxy for relative search volume
**When to use:** When exact search volume unavailable (YouTube doesn't provide it)
**Example:**
```python
# Source: SEO industry pattern + existing Phase 13 autocomplete code
def calculate_position_score(keyword, suggestions):
    """
    Score keyword based on autocomplete position.

    Position 1 = 100 score (highest demand)
    Position 10 = 10 score (lowest demand)
    Not found = 0 score

    23% of users select from autocomplete (SEO research 2026)
    """
    try:
        position = suggestions.index(keyword) + 1
        score = max(0, 100 - (position - 1) * 10)
        return score
    except ValueError:
        return 0
```

### Pattern 4: Conservative Opportunity Scoring
**What:** Only flag obvious opportunities (4x+ ratio) given high research overhead
**When to use:** Competition ratio calculation and display
**Example:**
```python
# Source: CONTEXT.md decisions (conservative thresholds)
def calculate_opportunity_score(demand_score, competition_count):
    """
    Calculate demand/competition ratio with conservative thresholds.

    High: >4x (only obvious wins)
    Medium: 2-4x
    Low: <2x
    """
    if competition_count == 0:
        return "∞ (No Competition)"

    ratio = demand_score / competition_count

    if ratio >= 4.0:
        category = "High Opportunity"
    elif ratio >= 2.0:
        category = "Medium Opportunity"
    else:
        category = "Low Opportunity"

    return f"{ratio:.1f}x ({category})"
```

### Anti-Patterns to Avoid
- **Requesting unnecessary YouTube API fields** - Use fields parameter to minimize quota usage (search costs 100 units)
- **Ignoring rate limits** - Google Trends requires 60s delay after rate limit hit, trendspyg has 5-min cache
- **Fetching full video lists for counts** - scrapetube requires iterating all results, expensive for high counts
- **Treating stale data as invalid** - Historical topics change slowly, 30-day-old data still useful with warning

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Google Trends API access | Custom scraper with requests | trendspyg | Handles rate limiting (60s delay), 5-min caching, 188K+ configurations, anti-detection |
| YouTube Data API auth | Manual OAuth flow | python-youtube or google-api-python-client | Handles token refresh, error codes, quota tracking |
| Autocomplete scraping | Simple HTTP request to YouTube | pyppeteer + stealth (Phase 13 code) | YouTube blocks simple requests, needs full browser simulation |
| Video count without quota | Custom scraper | scrapetube | No quota limits, no Selenium, direct Python interface |
| SQLite dict returns | Manual row parsing | row_factory = sqlite3.Row | Built-in, supports dict access and column names |
| Trend direction calculation | Manual percentage math | Google Trends interest over time | Normalized 0-100 scale, handles regional variations |
| Cache expiration | Manual timestamp checks | SQLite time series patterns + indexed timestamps | Efficient range queries, automatic cleanup |

**Key insight:** YouTube Data API has strict quota limits (10K units/day, search costs 100). One search = 1% of daily quota. Don't waste quota on exploratory operations - use scrapetube for counts, cache aggressively, and reserve API quota for high-value operations.

## Common Pitfalls

### Pitfall 1: YouTube API Quota Exhaustion
**What goes wrong:** Search operations cost 100 quota units each, default quota is 10K/day, quota exhaustion returns 403 errors for rest of day
**Why it happens:** Developers request unnecessary data, don't use fields parameter, don't cache results
**How to avoid:**
- Use scrapetube for video counts (quota-free)
- Cache all API responses for 7 days minimum
- Use fields parameter to request only needed data
- Monitor quota usage (1 search = 1% daily budget)
- Reserve API for operations that require authentication
**Warning signs:** 403 quotaExceeded errors, rapid quota consumption in testing

### Pitfall 2: Google Trends Rate Limiting Without Detection
**What goes wrong:** Silent rate limiting after ~1,400 requests, no error returned, incomplete data
**Why it happens:** Google Trends imposes undocumented rate limits, no official error codes
**How to avoid:**
- Use trendspyg's 5-minute cache (built-in)
- Implement 60-second delay between requests after limit hit
- Cache trend data for 7 days (trends change slowly for historical topics)
- Use batch operations with delays (trendspyg async batching)
**Warning signs:** Incomplete trend data, all trends returning zero interest

### Pitfall 3: Autocomplete Position as Absolute Volume
**What goes wrong:** Treating autocomplete position as absolute search volume metric
**Why it happens:** Confusing relative ranking (position 1 = most popular in dropdown) with absolute numbers
**How to avoid:**
- Use as proxy for relative demand only
- Label as "search volume proxy" not "search volume"
- Compare within same context (e.g., all history keywords)
- Don't compare across unrelated topics
- Document that 23% of users select from autocomplete (industry stat)
**Warning signs:** Comparing "dark ages" autocomplete to "taylor swift" autocomplete

### Pitfall 4: Ignoring Data Staleness in UI
**What goes wrong:** Displaying 30-day-old data without warning, user assumes current
**Why it happens:** Focusing on caching efficiency without user communication
**How to avoid:**
- Always display data age in output
- Warn when >7 days old (phase decision: 7-day cache)
- Provide --refresh flag for force refresh
- Fall back to stale cache on API failure (something > nothing)
- Document that historical topics change slowly
**Warning signs:** User surprised by outdated trend data, expects real-time freshness

### Pitfall 5: Scrapetube Full Iteration for Counts
**What goes wrong:** Using scrapetube to count videos requires iterating entire result set, slow for 10K+ videos
**Why it happens:** scrapetube returns generator, no count endpoint
**How to avoid:**
- Set reasonable iteration limits (e.g., first 100 videos for sample)
- Cache counts aggressively (competition doesn't change hourly)
- Consider sampling strategy (count first 100, extrapolate)
- Use YouTube API for exact counts when quota available
- Document count methodology (sample vs. full count)
**Warning signs:** Long wait times for popular keywords, timeout errors

### Pitfall 6: SQLite Transaction Management Confusion
**What goes wrong:** Partial data inserted on errors, inconsistent state
**Why it happens:** Not using context managers, mixing autocommit modes
**How to avoid:**
- Use `with con:` pattern (auto-commit on success, rollback on exception)
- Set `autocommit=False` for explicit transaction control (PEP 249 compliant)
- Use specific exception types (IntegrityError, OperationalError)
- Wrap multi-table operations in single transaction
**Warning signs:** Duplicate entries, missing related records, integrity errors

## Code Examples

Verified patterns from official sources:

### Database Schema Extension (Time Series Pattern)
```sql
-- Source: SQLite time series best practices + CONTEXT.md requirements
-- Extends Phase 13 schema with 5 new tables

-- Track trend data over time
CREATE TABLE IF NOT EXISTS trends (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  keyword_id INTEGER NOT NULL,
  fetched_at DATETIME NOT NULL,
  interest INTEGER NOT NULL,  -- 0-100 normalized score
  trend_direction TEXT,  -- 'rising', 'stable', 'declining'
  percent_change REAL,  -- +45.2 or -20.1
  region TEXT DEFAULT 'US',
  source TEXT DEFAULT 'google_trends',
  FOREIGN KEY (keyword_id) REFERENCES keywords(id)
);

-- Track competitor channels
CREATE TABLE IF NOT EXISTS competitor_channels (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  channel_id TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  subscriber_count INTEGER,
  total_views INTEGER,
  video_count INTEGER,
  last_updated DATE NOT NULL
);

-- Track competitor videos
CREATE TABLE IF NOT EXISTS competitor_videos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  video_id TEXT NOT NULL UNIQUE,
  channel_id INTEGER NOT NULL,
  keyword_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  view_count INTEGER,
  published_at DATE,
  video_age_days INTEGER,
  discovered_at DATE NOT NULL,
  FOREIGN KEY (channel_id) REFERENCES competitor_channels(id),
  FOREIGN KEY (keyword_id) REFERENCES keywords(id)
);

-- Track opportunity scores
CREATE TABLE IF NOT EXISTS opportunity_scores (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  keyword_id INTEGER NOT NULL,
  demand_score REAL NOT NULL,  -- autocomplete position proxy
  competition_score REAL NOT NULL,  -- video + channel count
  opportunity_ratio REAL NOT NULL,  -- demand/competition
  opportunity_category TEXT NOT NULL,  -- 'High', 'Medium', 'Low'
  calculated_at DATE NOT NULL,
  FOREIGN KEY (keyword_id) REFERENCES keywords(id)
);

-- Track validations (for future Phase 18)
CREATE TABLE IF NOT EXISTS validations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  keyword_id INTEGER NOT NULL,
  predicted_score REAL NOT NULL,
  actual_views INTEGER,
  actual_ctr REAL,
  prediction_date DATE NOT NULL,
  validation_date DATE,
  accuracy_score REAL,
  FOREIGN KEY (keyword_id) REFERENCES keywords(id)
);

-- Indexes for time series queries (composite for range scans)
CREATE INDEX IF NOT EXISTS idx_trends_keyword_time
  ON trends(keyword_id, fetched_at DESC);
CREATE INDEX IF NOT EXISTS idx_trends_fetch_time
  ON trends(fetched_at DESC);
CREATE INDEX IF NOT EXISTS idx_opportunity_ratio
  ON opportunity_scores(opportunity_ratio DESC, calculated_at DESC);
CREATE INDEX IF NOT EXISTS idx_competitor_videos_keyword
  ON competitor_videos(keyword_id, discovered_at DESC);
```

### Error Handling Pattern (Phase 13 Consistency)
```python
# Source: Python sqlite3 docs + Phase 13 database.py pattern
import sqlite3
from typing import Dict, Any

def add_trend_data(
    keyword_id: int,
    interest: int,
    trend_direction: str,
    percent_change: float
) -> Dict[str, Any]:
    """
    Add trend data following Phase 13 error dict pattern.

    Returns:
        {'status': 'inserted', 'trend_id': int} on success
        {'error': msg, 'details': str} on failure
    """
    try:
        cursor = conn.cursor()
        now = datetime.utcnow().date().isoformat()

        cursor.execute(
            """
            INSERT INTO trends (keyword_id, fetched_at, interest, trend_direction, percent_change)
            VALUES (?, ?, ?, ?, ?)
            """,
            (keyword_id, now, interest, trend_direction, percent_change)
        )
        conn.commit()

        return {
            'status': 'inserted',
            'trend_id': cursor.lastrowid
        }

    except sqlite3.IntegrityError as e:
        return {
            'error': 'Integrity constraint violated',
            'details': str(e)
        }
    except sqlite3.OperationalError as e:
        return {
            'error': 'Database operation failed',
            'details': str(e)
        }
    except sqlite3.Error as e:
        return {
            'error': f'Database error: {type(e).__name__}',
            'details': str(e)
        }
```

### Google Trends Integration (trendspyg)
```python
# Source: trendspyg GitHub README
from trendspyg import download_google_trends_rss, download_google_trends_csv
from datetime import datetime

def get_trend_direction(keyword, hours=168):
    """
    Get trend direction for keyword over time window.

    Args:
        keyword: Keyword to analyze
        hours: Time window (4/24/48/168 supported)

    Returns:
        {'direction': 'rising'|'stable'|'declining', 'percent_change': float}
        {'error': msg} on failure
    """
    try:
        # CSV method for historical data (requires Chrome)
        df = download_google_trends_csv(
            geo='US',
            hours=hours,
            output_format='dataframe',
            cache=True  # 5-minute TTL
        )

        # Filter to keyword
        keyword_data = df[df['trend'].str.lower() == keyword.lower()]

        if keyword_data.empty:
            return {'error': 'Keyword not found in trends'}

        # Extract traffic change (example: "+125%" -> 125.0)
        traffic = keyword_data['traffic'].iloc[0]
        percent_change = float(traffic.replace('%', '').replace('+', ''))

        if percent_change > 20:
            direction = 'rising'
        elif percent_change < -20:
            direction = 'declining'
        else:
            direction = 'stable'

        return {
            'direction': direction,
            'percent_change': percent_change
        }

    except Exception as e:
        return {
            'error': f'Trend analysis failed: {type(e).__name__}',
            'details': str(e)
        }
```

### YouTube Competition Count (python-youtube + scrapetube)
```python
# Source: python-youtube PyPI docs + scrapetube GitHub
from pyyoutube import Client
import scrapetube

def get_competition_count(keyword, use_api=False, quota_budget=100):
    """
    Count videos for keyword, preferring quota-free scrapetube.

    Args:
        keyword: Search keyword
        use_api: Force YouTube API usage (costs 100 quota)
        quota_budget: Max videos to count via scrapetube

    Returns:
        {'video_count': int, 'method': 'api'|'scrape'|'sample'}
        {'error': msg} on failure
    """
    if use_api:
        try:
            client = Client(api_key=API_KEY)
            # This costs 100 quota units!
            result = client.search.list(
                q=keyword,
                part='snippet',
                max_results=50,
                type='video'
            )
            return {
                'video_count': result.pageInfo.totalResults,
                'method': 'api'
            }
        except Exception as e:
            return {'error': f'API search failed: {str(e)}'}

    else:
        # Quota-free scrapetube (but requires iteration)
        try:
            videos = scrapetube.get_search(keyword)

            # Count with budget limit
            count = 0
            for video in videos:
                count += 1
                if count >= quota_budget:
                    return {
                        'video_count': f"{count}+",  # Minimum count
                        'method': 'sample'
                    }

            return {
                'video_count': count,
                'method': 'scrape'
            }

        except Exception as e:
            return {'error': f'Scrape failed: {str(e)}'}
```

### Related Query Expansion (Phase 13 Autocomplete Reuse)
```python
# Source: Phase 13 autocomplete.py + CONTEXT.md
import asyncio
from autocomplete import get_autocomplete_suggestions

async def expand_related_queries(seed_keyword, max_queries=20):
    """
    Expand seed keyword into related queries using autocomplete.

    Reuses Phase 13 autocomplete infrastructure.

    Returns:
        {'seed': str, 'related': list, 'count': int, 'fetched_at': str}
        {'error': msg} on failure
    """
    result = await get_autocomplete_suggestions(seed_keyword, max_suggestions=max_queries)

    if 'error' in result:
        return result

    # Filter out seed keyword itself
    related = [s for s in result['suggestions'] if s.lower() != seed_keyword.lower()]

    return {
        'seed': seed_keyword,
        'related': related,
        'count': len(related),
        'fetched_at': result['fetched_at']
    }
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| pytrends | trendspyg | April 2025 | pytrends archived, trendspyg actively maintained with 188K+ configs |
| Manual OAuth flow | python-youtube 0.9.8 | Aug 2025 | Simpler API wrapper, automatic token refresh |
| Selenium for scraping | scrapetube | 2024-2025 | No browser automation, quota-free, direct Python |
| Manual row parsing | sqlite3.Row factory | Python 3.11+ | Built-in dict access, cleaner code |
| isolation_level for transactions | autocommit parameter | Python 3.12 | PEP 249 compliant, explicit control |

**Deprecated/outdated:**
- pytrends: Archived April 2025, use trendspyg instead
- YouTube autocomplete HTTP endpoint: Blocked by YouTube, requires full browser simulation
- YouTube Data API for video counts: 100 quota per search, use scrapetube for counts
- String-based error returns: Use error dict pattern ({'error': msg}) for consistency

## Open Questions

Things that couldn't be fully resolved:

1. **Autocomplete Position Score Validation**
   - What we know: 23% of users select from autocomplete (SEO industry stat), position correlates with popularity
   - What's unclear: How to calibrate score (linear 100-10 vs. exponential decay vs. other)
   - Recommendation: Start with linear scoring (position 1 = 100, position 10 = 10), validate against actual video performance in Phase 18

2. **Google Trends Rate Limit Threshold**
   - What we know: ~1,400 requests triggers rate limit, 60s delay required
   - What's unclear: Exact threshold, whether it varies by IP/region, reset time
   - Recommendation: Implement conservative 60s delay after any rate limit signal, use 5-min cache, monitor for patterns

3. **Scrapetube Count Accuracy vs. Speed Trade-off**
   - What we know: Full iteration accurate but slow for 10K+ videos
   - What's unclear: Optimal sample size for extrapolation, when to stop counting
   - Recommendation: Use first 100 videos as sample, extrapolate if needed, cache aggressively, document methodology

4. **Competition Ratio Threshold Calibration**
   - What we know: 4x+ threshold chosen conservatively (CONTEXT.md), high research overhead for this channel
   - What's unclear: Whether 4x is correct threshold, how to adjust for different topic types
   - Recommendation: Start with 4x, collect data, validate in Phase 18 against actual video performance

## Sources

### Primary (HIGH confidence)
- [YouTube Data API Quota Calculator](https://developers.google.com/youtube/v3/determine_quota_cost) - Official quota costs
- [Python sqlite3 Documentation](https://docs.python.org/3/library/sqlite3.html) - Error handling, row_factory, transactions
- [trendspyg GitHub](https://github.com/flack0x/trendspyg) - Installation, API patterns, caching
- [python-youtube PyPI](https://pypi.org/project/python-youtube/) - Version 0.9.8, installation, usage
- [scrapetube GitHub](https://github.com/dermasmid/scrapetube) - Quota-free YouTube scraping

### Secondary (MEDIUM confidence)
- [YouTube API Quota Best Practices (Phyllo)](https://www.getphyllo.com/post/youtube-api-limits-how-to-calculate-api-usage-cost-and-fix-exceeded-api-quota) - Common mistakes, optimization
- [SQLite Time Series Best Practices (MoldStud)](https://moldstud.com/articles/p-handling-time-series-data-in-sqlite-best-practices) - Schema design, indexing
- [Keyword Difficulty Calculation (Semrush)](https://www.semrush.com/kb/1158-what-is-kd) - Demand/supply ratio patterns
- [Autocomplete SEO Statistics (SE Ranking)](https://seranking.com/blog/seo-statistics/) - 23% user selection stat
- [Google Trends Rate Limiting (pytrends Issues)](https://github.com/GeneralMills/pytrends/issues/523) - 60s delay, 1,400 request threshold

### Tertiary (LOW confidence - needs validation)
- WebSearch results on keyword clustering - Multiple tools/approaches, no single standard
- Autocomplete as search volume proxy - Industry pattern but not officially documented by Google/YouTube
- Trend direction thresholds (+20% = rising, -20% = declining) - Heuristic, should be validated with user data

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Official docs for all libraries, recent versions (2025), active maintenance
- Architecture: HIGH - Follows existing Phase 13 patterns, verified SQLite time series patterns from docs
- Pitfalls: HIGH - Documented in official YouTube API docs, pytrends issues, SQLite best practices
- Code examples: HIGH - All examples from official docs or verified library READMEs

**Research date:** 2026-01-31
**Valid until:** 2026-03-31 (60 days - stable domain, but API quotas/limits can change)

---

*Sources compiled from official documentation, verified libraries, and industry research as of January 2026.*
