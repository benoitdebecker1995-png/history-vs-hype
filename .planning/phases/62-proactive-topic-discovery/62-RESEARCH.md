# Phase 62: Proactive Topic Discovery - Research

**Researched:** 2026-03-14
**Domain:** Python orchestration — autocomplete scraping, competitor RSS/API, Google Trends, LLM classification, SQLite
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

- **Scan trigger:** Manual only — `/discover --scan` runs full pipeline on demand. No cron/scheduled scans.
- **Signal sources:** All three (autocomplete, competitor, trends) run every time — single command, full picture.
- **Seed keywords:** ~20-30 hardcoded seeds from channel DNA categories (territorial disputes, colonial history, border conflicts, ideological myths, untranslated documents). Expandable.
- **Scoring formula:** Extended Belize formula — demand + map angle + news hook + no competitor coverage + subscriber conversion potential (5 factors). Topic type classification uses existing ideological=2.31% vs territorial=0.65% data.
- **Missing signals:** Score at neutral midpoint, not penalized. Flag as "unavailable".
- **Breakout boost:** Breakout trends get visible urgency flag and temporary score boost vs steady evergreen.
- **Competitor gap detection:** Keyword match first pass, LLM classification for ambiguous high-view titles. View threshold = relative (>2x channel average views), not fixed number.
- **Channel suggestions:** When untracked channels appear repeatedly, suggest them in discovery feed for manual addition to competitor_channels.json. Advisory only.
- **Breakout detection:** Google Trends "Breakout" label (>5000% increase) is primary trigger. Also flag >100% 30-day increase. Per-scan urgency only — no persistence/decay.
- **Output format:** Markdown report at `channel-data/DISCOVERY-FEED.md` — regenerated each scan. Top 10 opportunities. Separate from TOPIC-PIPELINE.md.
- **Command integration:** `--scan` is standalone flag on existing `/discover` command.
- **Pipeline separation:** `/next` can read DISCOVERY-FEED.md if available but does not require it.

### Claude's Discretion

- Number of autocomplete seeds per scan (research optimal count vs runtime tradeoff)
- Topic type classification approach (reuse topic_pipeline.py types vs extend)
- LLM model for ambiguous title classification (likely Haiku for cost)
- Whether to cache LLM classifications in keywords.db (probably yes for token savings)
- Channel suggestion threshold (3+ appearances is likely sweet spot)
- Channel suggestion presentation format
- Pipeline dedup approach (filter out own topics vs flag-and-mark)
- Urgency boost decay behavior (per-scan only is simplest)
- Whether DISCOVERY-FEED.md stays separate from TOPIC-PIPELINE.md (separate is cleaner)

### Deferred Ideas (OUT OF SCOPE)

- Scheduled/automated scanning (cron)
- DB-stored discovery feed with historical tracking
- Auto-populating TOPIC-PIPELINE.md from discovery feed
- Semantic similarity matching for competitor topics
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| DISC-01 | YouTube autocomplete miner scans channel niches and surfaces suggestions NOT already in pipeline or production | autocomplete.py exists, extract_keywords_batch() handles multi-seed; dedup via recommender.py's get_existing_topics() + keywords.db lookup |
| DISC-02 | Competitor release tracker monitors target channels, detects new uploads, flags coverage gaps where competitors got views but channel has no video | competitor_tracker.py fetch_all_competitors() is fully built; needs gap-detection layer using relative view threshold |
| DISC-03 | Google Trends pulse detects rising search interest with breakout detection and 30/90-day trend direction | trends.py TrendsClient exists; needs breakout label detection and multi-timeframe support |
| DISC-04 | `/discover --scan` combines all signals into ranked opportunities scored by extended Belize formula | discovery_scanner.py (new orchestrator) + extended scoring formula from topic_pipeline.py + opportunity.py |
| DISC-05 | Discovery feed deduplicates against pipeline (keywords.db, _IN_PRODUCTION/, _ARCHIVED/) | recommender.py get_existing_topics() + topic_matches_existing() already handle this; keywords.db has lifecycle_state |
</phase_requirements>

---

## Summary

This phase is primarily **orchestration, not construction**. The four building blocks — autocomplete.py, trends.py, competitor_tracker.py, and recommender.py — already exist and work. What is missing is: (1) a scanner module that calls them all in sequence, (2) a gap-detection layer on competitor data, (3) breakout detection on trends data, (4) an extended Belize scoring formula, and (5) the `--scan` flag wired into the `/discover` command with markdown report output.

The existing codebase establishes clear patterns: error-dict returns, feature flags for optional deps, lazy imports for circular dependency avoidance, structured logging via `tools.logging_config`, and argparse CLI in `__main__` blocks. All new code must follow these patterns exactly. The `KeywordDB` at `tools/discovery/keywords.db` (schema v29) is the dedup source. `competitor_channels.json` at `tools/intel/competitor_channels.json` has 10 channels already configured.

**Primary recommendation:** Build a single `tools/discovery/discovery_scanner.py` orchestrator that wires all existing modules, add `--scan` to discover.md, write DISCOVERY-FEED.md to channel-data/. Four tasks: scanner module, scoring formula extension, `/discover --scan` command update, and test coverage.

---

## Standard Stack

### Core (already installed — no new deps needed)

| Library | Version | Purpose | Confidence |
|---------|---------|---------|------------|
| pyppeteer + pyppeteer-stealth | installed | autocomplete scraping | HIGH — in pyproject.toml |
| trendspyg | installed | Google Trends data | HIGH — confirmed in trends.py |
| feedparser | installed | competitor RSS feeds | HIGH — in competitor_tracker.py |
| requests | installed | HTTP fallback for RSS | HIGH — used in competitor_tracker.py |
| sqlite3 | stdlib | keywords.db queries | HIGH |
| anthropic SDK | installed | LLM title classification | HIGH — used in other tools |

### Optional / Conditional

| Library | Purpose | Feature Flag Pattern |
|---------|---------|---------------------|
| anthropic SDK | Haiku calls for ambiguous title classification | `LLM_AVAILABLE` flag, graceful degradation to keyword-only matching |
| trendspyg | Trends signal | `TRENDSPYG_AVAILABLE` — already in trends.py |
| feedparser | Competitor RSS | `FEEDPARSER_AVAILABLE` — already in competitor_tracker.py |

### No New Installations Required

All dependencies for Phase 62 are already in the project. The scanner is pure orchestration over existing modules.

---

## Architecture Patterns

### Established Codebase Patterns (MUST follow)

**Error-dict pattern** — never raise, always return:
```python
# Source: competitor_tracker.py, all discovery modules
return {'error': f'fetch failed: {exc}'}  # on failure
return {'results': [...], 'count': N}      # on success
```

**Feature flag pattern** — graceful optional deps:
```python
# Source: trends.py, competitor_tracker.py
try:
    from trendspyg import download_google_trends_csv
    TRENDSPYG_AVAILABLE = True
except ImportError:
    TRENDSPYG_AVAILABLE = False
```

**Lazy import pattern** — break circular deps:
```python
# Source: recommender.py _load_pattern_extractor()
def _load_pattern_extractor():
    try:
        from tools.youtube_analytics.pattern_extractor import extract_winning_patterns
        return extract_winning_patterns
    except ImportError:
        return None
```

**Structured logging** — never print() for diagnostic output:
```python
# Source: all tools modules
from tools.logging_config import get_logger
logger = get_logger(__name__)
logger.info("Processing %d/%d: %s", i + 1, len(seeds), seed)
```

**Absolute imports** — all cross-package:
```python
from tools.discovery.database import KeywordDB
from tools.intel.competitor_tracker import fetch_all_competitors
from tools.discovery.autocomplete import extract_keywords_batch
from tools.discovery.trends import get_trend_direction
```

### Recommended Project Structure for Phase 62

```
tools/discovery/
├── discovery_scanner.py    # NEW — main orchestrator for /discover --scan
├── autocomplete.py         # EXISTING — no changes needed
├── trends.py               # EXISTING — minor extension for breakout detection
├── database.py             # EXISTING — no changes needed
├── recommender.py          # EXISTING — no changes needed
└── opportunity.py          # EXISTING — no changes needed

tools/intel/
├── competitor_tracker.py   # EXISTING — no changes needed
└── competitor_channels.json # EXISTING — 10 channels configured

.claude/commands/
└── discover.md             # EXISTING — add --scan flag documentation

channel-data/
└── DISCOVERY-FEED.md       # NEW OUTPUT — regenerated on each scan
```

### Pattern 1: Scanner Orchestrator (discovery_scanner.py)

**What:** Single entry point that calls all three signal sources in sequence, deduplicates, scores, and writes the markdown report.

**When to use:** Called by `/discover --scan`. Not called by other modules.

```python
# Suggested module skeleton — follows established patterns
"""
Discovery Scanner — Proactive topic discovery pipeline.

Orchestrates autocomplete mining, competitor gap detection, and
Google Trends pulse into a unified ranked opportunity feed.

Usage:
    python -m tools.discovery.discovery_scanner
    python -m tools.discovery.discovery_scanner --limit 10
    python -m tools.discovery.discovery_scanner --json
"""

from tools.logging_config import get_logger
logger = get_logger(__name__)

# Hardcoded seed keywords (expandable) — channel DNA categories
CHANNEL_SEEDS = [
    # Territorial disputes
    "border dispute history", "territorial dispute explained",
    "sovereignty conflict", "partition history",
    "island dispute", "colonial border",
    # Colonial history
    "colonial history myth", "decolonization explained",
    "scramble for africa", "berlin conference history",
    "ottoman empire partition", "sykes picot explained",
    # Border conflicts
    "border conflict documentary", "icj ruling territory",
    "treaty border history", "disputed territory map",
    # Ideological myths
    "history myth debunked", "historical misconception",
    "propaganda history", "dark ages myth",
    "medieval myth explained", "history fact check",
    # Untranslated documents
    "untranslated document history", "primary source history",
    "original document revealed",
]

class DiscoveryScanner:
    def scan(self, limit: int = 10) -> dict:
        """Run full discovery pipeline. Returns ranked opportunities."""
        ...

    def _run_autocomplete(self) -> list[dict]: ...
    def _run_competitor_gaps(self) -> list[dict]: ...
    def _run_trends_pulse(self) -> list[dict]: ...
    def _deduplicate(self, candidates: list[dict]) -> list[dict]: ...
    def _score_extended_belize(self, candidate: dict) -> float: ...
    def _write_feed(self, ranked: list[dict]) -> str: ...
```

### Pattern 2: Extended Belize Scoring Formula

**What:** 5-factor weighted score combining the existing SAW components with subscriber conversion potential.

**Factors and weights (recommended):**

| Factor | Weight | Source | Notes |
|--------|--------|--------|-------|
| demand | 0.25 | autocomplete position score (0-100) | from keywords.db or live scrape |
| map_angle | 0.20 | keyword classification (territorial/colonial = map-heavy) | boolean → 0 or 100 |
| news_hook | 0.15 | NEWS_HOOK_KEYWORDS from topic_pipeline.py | 0/50/100 for none/medium/high |
| no_competitor | 0.20 | competitor gap detection (coverage gap exists?) | 0 or 100 |
| conversion_potential | 0.20 | topic_type classification × conversion rate data | ideological=100, territorial=28, colonial=65 |

**Missing signal = neutral midpoint (50), flagged as "unavailable":**
```python
# If trends data unavailable, score demand at 50 with flag
demand_score = result.get('search_volume_proxy', 50)
demand_available = 'search_volume_proxy' in result
```

**Breakout boost:** Add +15 to final score (before capping at 100) if breakout flag set:
```python
if candidate.get('is_breakout'):
    raw_score += 15
    notes.append("BREAKOUT: Temporary boost applied")
final_score = min(100, raw_score)
```

**Conversion potential mapping (from channel data):**
```python
CONVERSION_SCORES = {
    'ideological': 100,  # 2.31% sub rate — best
    'colonial': 65,      # good balance
    'territorial': 28,   # 0.65% sub rate — most views, low conversion
    'legal': 50,         # neutral — pairs with territorial
    'medieval': 40,
    'general': 25,
}
```

### Pattern 3: Competitor Gap Detection

**What:** Layer on top of `fetch_all_competitors()` that compares competitor video titles against own channel topics.

**Implementation approach:**

```python
# Step 1: Get channel average views for relative threshold
# Pull from tools/youtube_analytics/analytics.db or use hardcoded fallback
CHANNEL_AVG_VIEWS = 400  # fallback — 199K views / ~47 videos ≈ 4,234 but median is lower

# Step 2: Keyword match (first pass — fast, no API cost)
def _title_matches_channel_topic(title: str) -> bool:
    """Check if competitor video title overlaps with channel's topic space."""
    title_lower = title.lower()
    # Use same term lists as classify_topic() in topic_pipeline.py
    ...

# Step 3: Flag as coverage gap
def _is_coverage_gap(video: dict, existing_topics: list[str]) -> bool:
    """Competitor got views but we have no video."""
    views = video.get('views') or 0
    if views < CHANNEL_AVG_VIEWS * 2:
        return False  # Didn't "get views" by relative standard
    return not topic_matches_existing(video['title'], existing_topics)

# Step 4: LLM classification (second pass — ambiguous high-view titles only)
# Use Haiku model (cost-efficient), cache result in keywords.db
def _classify_with_llm(title: str) -> dict:
    """Classify ambiguous competitor title. Returns topic_type or None."""
    ...
```

**LLM caching in keywords.db:**
The `keywords` table schema v29 has a `production_constraints` JSON column. A new `competitor_classifications` table in keywords.db (added via migration) is cleaner. Alternatively, cache as a simple Python dict in the scanner (per-scan, no persistence) to avoid schema changes. Given the CONTEXT.md note "probably yes" for DB caching, a new table is preferred.

### Pattern 4: Breakout Detection in trends.py

**What:** Extend `TrendsClient.get_interest_over_time()` to return breakout flag and multi-timeframe data.

**Current limitation:** `trends.py` uses `download_google_trends_csv()` which only returns trending topics list, not historical interest-over-time for arbitrary keywords. The "Breakout" label from Google Trends means >5000% increase.

**What trendspyg actually supports:**
- `download_google_trends_csv()` — fetches top trending topics (not keyword-specific history)
- The current implementation searches the trending list for keyword matches
- For "breakout detection": if keyword appears in trending list with >5000% traffic change → breakout

**Recommended approach:** Keep existing TrendsClient but add:
```python
def is_breakout(self, keyword: str) -> dict:
    """
    Check if keyword is experiencing breakout interest.

    Returns:
        {'is_breakout': bool, 'percent_change': float, 'direction': str}
        or {'error': msg, 'is_breakout': False}
    """
    result = self.get_interest_over_time(keyword)
    if 'error' in result:
        return {'is_breakout': False, 'percent_change': 0, **result}

    pct = result.get('percent_change', 0)
    return {
        'is_breakout': pct > 5000,  # Google Trends "Breakout" threshold
        'is_rising': pct > 100,     # Strong rise flag
        'percent_change': pct,
        'direction': result.get('direction', 'stable'),
    }
```

### Anti-Patterns to Avoid

- **Importing competitor_tracker at module level without feature flag** — feedparser may not be installed. Wrap in try/except with FEEDPARSER_AVAILABLE.
- **Calling asyncio.run() from inside an event loop** — autocomplete.py uses `asyncio.run()`. If the scanner is called from an async context, use `loop.run_until_complete()` instead.
- **Using print() for scanner progress** — use logger.info(). Only final markdown report output goes to stdout via print().
- **Hardcoding channel average views** — pull from analytics.db if available, fall back to constant. Don't fail if DB unavailable.
- **Blocking scan on any single signal failure** — if autocomplete fails (pyppeteer not installed), continue with competitor + trends. Each signal source is independent.
- **schema migration breaking existing tests** — if adding a competitors_cache table to keywords.db, use `IF NOT EXISTS` and PRAGMA user_version increment per Phase 52 migration pattern.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Dedup against existing topics | Custom string matcher | `recommender.py::topic_matches_existing()` + `get_existing_topics()` | Already handles word-level matching, 2-word overlap threshold, year stripping |
| Competitor channel fetching | New RSS/API client | `competitor_tracker.py::fetch_all_competitors()` | Handles RSS fallback, API enrichment, batch processing, error-dict pattern |
| Search volume proxy | New autocomplete scraper | `autocomplete.py::extract_keywords_batch()` | Has rate limiting, stealth, jitter, exponential backoff |
| Trends data | New pytrends/trendspyg wrapper | `trends.py::TrendsClient` | Has caching, rate limit handling, feature flag |
| Topic type classification | New keyword classifier | `topic_pipeline.py::classify_topic()` | Already has term lists for territorial/colonial/ideological/legal/medieval |
| Pattern multiplier | New scoring formula | `recommender.py::calculate_pattern_multiplier()` | Has geo monopoly, urgency, pattern matching |
| Keywords DB queries | Raw sqlite3 calls | `database.py::KeywordDB` | Handles schema migration, connection management |

---

## Common Pitfalls

### Pitfall 1: Autocomplete Runtime — Too Many Seeds

**What goes wrong:** With 20-30 seeds × (2s base + 1-3s jitter) per seed = 60-120 seconds minimum. Chrome launch overhead adds another 3-5s per seed if browser is not reused.

**Why it happens:** `extract_keywords_batch()` creates a new browser instance per seed via `asyncio.run(get_autocomplete_suggestions())`. Each call launches and closes Chrome.

**How to avoid:** Reuse the browser across seeds by refactoring the batch function to keep the browser open for the full batch, or limit to 10-15 seeds per scan. The CONTEXT.md explicitly puts seed count at "Claude's Discretion." Recommend 15 seeds for reasonable <90s runtime.

**Warning signs:** Scan taking >3 minutes. User calls it slow and stops using it.

### Pitfall 2: trendspyg Returns Trending Topics List, Not Keyword History

**What goes wrong:** The current `download_google_trends_csv()` fetches trending topics across all categories, then searches for the keyword in those results. A niche topic like "Sykes-Picot" will never appear in global trending topics and will always return `{'interest': 0, 'percent_change': 0, 'direction': 'stable', 'note': 'Keyword not in trending topics'}`.

**Why it happens:** Google Trends has two modes: (1) trending topics feed, (2) interest-over-time for specific keywords. `trendspyg` primarily wraps mode (1). Mode (2) requires `pytrends` `interest_over_time()` which is not installed.

**How to avoid:** Accept this limitation. The trends signal in the discovery feed will frequently be "unavailable" for niche history topics. Score at neutral midpoint (50) with "TRENDS: signal unavailable for niche topic" flag. Do not present missing trends data as a failure — it's expected behavior.

**Warning signs:** Every topic scores trends as 0 — this is correct for niche history topics.

### Pitfall 3: LLM Classification Cost Creep

**What goes wrong:** Calling Haiku for every competitor video title on every scan. With 10 channels × 15 videos = 150 titles per scan, uncached, this costs real tokens even at Haiku prices.

**Why it happens:** No cache → every scan re-classifies every title.

**How to avoid:** Cache LLM classifications with (title_hash → classification) in keywords.db. A simple approach: add a `competitor_title_cache` table. Check cache before calling LLM. Cache is permanent (competitor titles don't change meaning). On first scan, all 150 titles get classified. On subsequent scans, only new titles (published since last scan) get classified.

**Warning signs:** Each scan shows 150 LLM calls instead of only new-video count.

### Pitfall 4: Competitor Gap False Positives

**What goes wrong:** Flagging competitor videos as "coverage gaps" when the channel already has a video on the topic — because the keyword matcher isn't finding the match.

**Why it happens:** Folder name is "43-india-pakistan-partition-2026" but competitor title is "The History of the British Raj" — no keyword overlap detected, but functionally the channel covers this space.

**How to avoid:** Use the existing `topic_matches_existing()` word-overlap function (2+ common words threshold). Accept that it will miss some matches and occasionally flag false gaps. LLM pass only for high-view titles (views > 3x channel average) to reduce false positives on the cases that matter most.

**Warning signs:** DISCOVERY-FEED.md shows topics already in production as "coverage gaps."

### Pitfall 5: asyncio.run() Conflicts

**What goes wrong:** `discovery_scanner.py` calls `autocomplete.extract_keywords_batch()` which calls `asyncio.run()` inside. If the scanner is ever called from an async context (e.g., future agent refactor), this raises `RuntimeError: This event loop is already running`.

**Why it happens:** `asyncio.run()` cannot be called when an event loop is already running.

**How to avoid:** For Phase 62, the scanner is called from CLI/Claude Code only — synchronous context. Not an immediate problem. Document it and move on. Do not refactor asyncio handling.

---

## Code Examples

### Seed Keyword Set (Recommended 15 for runtime balance)

```python
# Source: Channel DNA categories from CLAUDE.md + CONTEXT.md
CHANNEL_SEEDS = [
    # Territorial / border (5)
    "territorial dispute history",
    "border dispute explained",
    "colonial border history",
    "disputed island history",
    "partition history explained",
    # Colonial / ideological (5)
    "colonial history myth",
    "historical misconception debunked",
    "scramble for africa history",
    "history propaganda explained",
    "dark ages myth debunked",
    # Legal / untranslated (3)
    "icj ruling history",
    "untranslated document history",
    "treaty history explained",
    # High-conversion wildcard (2)
    "history fact check documentary",
    "history vs reality",
]
```

### Relative View Threshold

```python
# Source: CONTEXT.md decision + CLAUDE.md channel stats
# Channel: 199K views across 47 long-form videos ≈ 4,234 avg
# But median is much lower — 3 outlier videos = 40K+ views pull the mean up
# Using 1,000 as practical relative baseline (conservative)

def _get_channel_avg_views() -> float:
    """Get channel average views from analytics DB, or use fallback."""
    try:
        from tools.youtube_analytics.analyze import get_channel_stats
        stats = get_channel_stats()
        return stats.get('avg_views_per_video', 1000)
    except Exception:
        return 1000  # Conservative fallback

def _competitor_got_views(video: dict, channel_avg: float) -> bool:
    """True if competitor video got >2x channel average views."""
    views = video.get('views') or 0
    return views >= channel_avg * 2
```

### DISCOVERY-FEED.md Output Format

```markdown
# Discovery Feed

**Scanned:** 2026-03-14 14:32
**Seeds:** 15 | **Autocomplete hits:** 87 | **Competitor videos scanned:** 147 | **Trends checked:** 15

> Signals: autocomplete=OK | competitor=OK | trends=PARTIAL (niche topics not in global trending)

## Top 10 Opportunities

| Rank | Score | Topic | Demand | Map | Hook | No Comp | Conversion | Flags |
|------|-------|-------|--------|-----|------|---------|------------|-------|
| 1 | 82 | belize sapodilla reef dispute | 78 | YES | high | YES | territorial | GEO-MONOPOLY |
| 2 | 75 | india partition untranslated document | 65 | YES | med | YES | colonial | - |
...

### 1. belize sapodilla reef dispute (82/100)

**Why now:** Competitor coverage gap — RealLifeLore covered Guatemala-Belize (890K views) but not Sapodilla
**Demand:** autocomplete position score 78/100
**Map angle:** YES — territorial dispute maps available
**News hook:** ICJ deadline approaching (HIGH urgency +15)
**Competitor coverage:** NONE in pipeline — GAP CONFIRMED
**Conversion type:** territorial (0.65% sub rate) + colonial (good balance)
**Channel suggestion:** None

**Action:** `/greenlight "sapodilla reef belize icj"` before researching

---

## Channel Suggestions (untracked channels appearing in results)

- **CGP Grey** (appeared 4 times in scan) — consider adding to competitor_channels.json
  Geography/systems format, potential topic overlap with territorial content

## Signal Quality

| Signal | Status | Notes |
|--------|--------|-------|
| Autocomplete | OK | 15 seeds, 87 suggestions |
| Competitor RSS | OK | 10 channels, 147 videos |
| Google Trends | PARTIAL | 15 keywords checked, 12 returned no data (niche — expected) |
| LLM Classification | OK | 23 titles classified, 112 from cache |

*Generated by `/discover --scan` — regenerated fresh each run*
```

### dedup logic

```python
# Source: adapted from recommender.py patterns
from tools.discovery.recommender import get_existing_topics, topic_matches_existing
from tools.discovery.database import KeywordDB

def deduplicate_candidates(candidates: list[dict]) -> list[dict]:
    """Filter out topics already in production, archived, or keywords.db pipeline."""
    existing = get_existing_topics()  # scans _IN_PRODUCTION/ and _ARCHIVED/
    db = KeywordDB()

    fresh = []
    for c in candidates:
        keyword = c['keyword']

        # Check folder-based dedup
        if topic_matches_existing(keyword, existing):
            logger.debug("Dedup (folder): %s", keyword)
            continue

        # Check keywords.db lifecycle state
        # Topics in SCRIPTING, FILMED, PUBLISHED, ARCHIVED = skip
        kw_record = db.get_keyword_by_text(keyword)
        if kw_record and kw_record.get('lifecycle_state') in ('SCRIPTING', 'FILMED', 'PUBLISHED', 'ARCHIVED'):
            logger.debug("Dedup (DB lifecycle %s): %s", kw_record['lifecycle_state'], keyword)
            continue

        fresh.append(c)

    db.close()
    return fresh
```

---

## State of the Art

| Old Approach | Current Approach | Notes |
|--------------|------------------|-------|
| Reactive topic selection (user decides ad-hoc) | Proactive scanning against channel seeds | This phase |
| All tools called separately | Unified `/discover --scan` orchestration | This phase |
| Fixed view threshold for competitor gap detection | Relative threshold (>2x channel avg) | CONTEXT.md decision |
| Manual channel monitoring | RSS feed + API enrichment via competitor_tracker.py | Already built |

---

## Open Questions

1. **trendspyg "Breakout" label detection reliability**
   - What we know: trendspyg returns `traffic` field as percent string (e.g., "+5000%"). The "Breakout" label in Google Trends UI appears when change exceeds 5000%.
   - What's unclear: Whether `download_google_trends_csv()` actually returns the breakout indicator separately or just the percentage. The current code parses percentage from the `traffic` field — need to verify 5000+ is the correct threshold for `is_breakout=True`.
   - Recommendation: Test against a known breakout topic. Use >5000% as threshold per CONTEXT.md. If the field is never > 5000 for niche history topics (very likely), the breakout flag will simply never trigger — which is acceptable.

2. **Channel average views source for relative threshold**
   - What we know: Channel has 199K+ views across 47 long-form videos = ~4,234 mean. But median is much lower due to 3 outlier videos (Belize 23K, Tariffs 7K, Bermeja 3K).
   - What's unclear: Whether analytics.db has a queryable `avg_views` field or whether it needs to be computed from video_performance table.
   - Recommendation: Default to 1,000 views as practical threshold (conservative, catches clear breakout competitor videos). Make it a configurable constant in discovery_scanner.py.

3. **LLM competitor title classification prompt**
   - What we know: Haiku is the model (cost). The 5 topic types are territorial/colonial/ideological/legal/medieval/general.
   - What's unclear: Whether a single-turn classification prompt is reliable enough, or whether a few-shot prompt is needed.
   - Recommendation: Use a structured prompt with the 5 categories and examples. Single-turn is sufficient for title classification — these are short inputs.

---

## Validation Architecture

Nyquist validation is enabled (no explicit `false` in config.json).

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest (installed, `tests/` directory exists) |
| Config file | `pyproject.toml` — `testpaths = ["tests"]` |
| Quick run command | `python -m pytest tests/test_discovery_scanner.py -x -q` |
| Full suite command | `python -m pytest tests/ -x -q` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| DISC-01 | Autocomplete miner returns suggestions, deduplicates against pipeline | unit | `pytest tests/test_discovery_scanner.py::test_autocomplete_dedup -x` | Wave 0 |
| DISC-02 | Competitor gap detection flags high-view topics not in own pipeline | unit | `pytest tests/test_discovery_scanner.py::test_competitor_gap_detection -x` | Wave 0 |
| DISC-03 | Trends pulse returns breakout flag and direction | unit | `pytest tests/test_discovery_scanner.py::test_trends_breakout -x` | Wave 0 |
| DISC-04 | Extended Belize formula scores 5 factors correctly | unit | `pytest tests/test_discovery_scanner.py::test_extended_belize_scoring -x` | Wave 0 |
| DISC-05 | Dedup filters topics in production/archived/db-pipeline | unit | `pytest tests/test_discovery_scanner.py::test_dedup_pipeline -x` | Wave 0 |

All tests require mocking external calls (pyppeteer, trendspyg, feedparser, anthropic). Use the established mock pattern from Phase 53 integration tests.

### Sampling Rate

- **Per task commit:** `python -m pytest tests/test_discovery_scanner.py -x -q`
- **Per wave merge:** `python -m pytest tests/ -x -q`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps

- [ ] `tests/test_discovery_scanner.py` — covers DISC-01 through DISC-05 with mocked external calls
- [ ] Fixtures: mock autocomplete result, mock competitor video list, mock trends result

*(No framework install needed — pytest already installed)*

---

## Sources

### Primary (HIGH confidence)
- Direct code inspection: `tools/discovery/autocomplete.py` — confirmed API, rate limiting, error-dict pattern
- Direct code inspection: `tools/discovery/trends.py` — confirmed TrendsClient, trendspyg usage, feature flag
- Direct code inspection: `tools/intel/competitor_tracker.py` — confirmed fetch_all_competitors(), RSS+API pattern
- Direct code inspection: `tools/discovery/recommender.py` — confirmed get_existing_topics(), topic_matches_existing(), calculate_pattern_multiplier()
- Direct code inspection: `tools/discovery/opportunity.py` — confirmed SAW formula, weights, component structure
- Direct code inspection: `tools/topic_pipeline.py` — confirmed classify_topic(), type_multipliers, NEWS_HOOK_KEYWORDS, GEOGRAPHIC_MONOPOLY_TARGETS
- Direct code inspection: `tools/intel/competitor_channels.json` — confirmed 10 channels, schema
- Direct code inspection: `.claude/commands/discover.md` — confirmed existing flags, confirmed --scan not yet present
- `.planning/phases/62-proactive-topic-discovery/62-CONTEXT.md` — all locked decisions

### Secondary (MEDIUM confidence)
- `.planning/STATE.md` — Phase 52 DB migration pattern, Phase 53 mock patterns, Phase 61 design decisions

### Tertiary (LOW confidence — inherent to trendspyg limitations)
- trendspyg breakout detection threshold (>5000%) — based on Google Trends UI knowledge, not confirmed against actual trendspyg output

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all dependencies confirmed via direct code inspection
- Architecture: HIGH — all patterns derived from existing codebase, not invented
- Scoring formula: HIGH — all weights/factors derived from channel data in CONTEXT.md and topic_pipeline.py
- Pitfalls: HIGH (runtime) / MEDIUM (trendspyg behavior) — runtime confirmed via code analysis; trendspyg breakout behavior is inferred

**Research date:** 2026-03-14
**Valid until:** 2026-06-14 (stable Python toolchain, no external API dependencies beyond what's already installed)
