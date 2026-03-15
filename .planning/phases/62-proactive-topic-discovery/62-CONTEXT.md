# Phase 62: Proactive Topic Discovery - Context

**Gathered:** 2026-03-14
**Status:** Ready for planning

<domain>
## Phase Boundary

Automated scanning finds high-demand topics matching the channel's strengths before competitors notice them. YouTube autocomplete reveals search demand, competitor tracker spots coverage gaps, Google Trends detects rising interest, and a unified discovery feed ranks opportunities by an extended Belize formula. Deduplicates against existing pipeline so only genuinely new opportunities surface.

Key insight: Most building blocks already exist as standalone tools (autocomplete.py, trends.py, competitor_tracker.py, news_scanner.py, recommender.py). This phase is primarily about **orchestrating** them into a unified proactive scanning pipeline, adding missing pieces (breakout detection, coverage gap flagging, channel suggestions), and producing a ranked discovery feed.

</domain>

<decisions>
## Implementation Decisions

### Scan trigger & frequency
- Manual only: `/discover --scan` runs the full pipeline on demand
- No scheduled/automatic scans — solo creator controls when
- All three signal sources (autocomplete, competitor, trends) run every time — single command, full picture
- Seed keywords auto-generated from channel DNA categories: territorial disputes, colonial history, border conflicts, ideological myths, untranslated documents (~20-30 seeds hardcoded, expandable)

### Scoring & ranking formula
- Extended Belize formula: demand + map angle + news hook + no competitor coverage + **subscriber conversion potential**
- Conversion potential uses topic type classification (ideological=2.31% vs territorial=0.65% from channel data)
- Missing signal sources score at neutral midpoint — not penalized, not boosted — with clear "unavailable" flag
- Breakout trends get visible urgency flag and temporary score boost vs steady evergreen demand

### Competitor gap detection
- Hybrid topic matching: keyword match on titles first pass, LLM classification for ambiguous high-view titles
- View threshold: relative to channel size (>2x channel average views = "got views"), not fixed number
- Channel suggestions: when untracked channels appear repeatedly in scan results, suggest them in the discovery feed for manual addition to competitor_channels.json
- Curated competitor_channels.json remains the primary source — suggestions are advisory only

### Breakout detection
- Google Trends "Breakout" label (>5000% increase) is the primary trigger
- Also flag topics with >100% 30-day increase
- Urgency is per-scan — no persistence or decay across scans

### Output format & integration
- Markdown report: `channel-data/DISCOVERY-FEED.md` — regenerated each scan
- Top 10 opportunities, ranked by extended Belize formula
- `/discover --scan` is standalone flag on existing `/discover` command
- Separate from TOPIC-PIPELINE.md — user promotes opportunities manually
- `/next` can read DISCOVERY-FEED.md if available but doesn't require it

### Claude's Discretion
- Number of autocomplete seeds per scan (research optimal count vs runtime tradeoff)
- Topic type classification approach (reuse topic_pipeline.py types vs extend)
- LLM model for ambiguous title classification (likely Haiku for cost)
- Whether to cache LLM classifications in keywords.db (probably yes for token savings)
- Channel suggestion threshold (3+ appearances is the likely sweet spot)
- Channel suggestion presentation format
- Pipeline dedup approach (filter out own topics vs flag-and-mark)
- Urgency boost decay behavior (per-scan only is simplest, but DB storage could enable 30-day decay)
- Whether DISCOVERY-FEED.md should stay separate from or auto-feed into TOPIC-PIPELINE.md (separate is cleaner)

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `tools/discovery/autocomplete.py`: YouTube autocomplete scraper (pyppeteer + stealth). Takes seed keywords, returns suggestions. Has rate limiting (2s + 1-3s jitter). CLI and Python API.
- `tools/discovery/trends.py`: Google Trends client (trendspyg). `get_trend_direction()` returns direction, percent_change, interest. 7-day cache. Feature flag TRENDSPYG_AVAILABLE.
- `tools/intel/competitor_tracker.py`: RSS feed fetcher + YouTube Data API enrichment. Last 15 videos per channel. competitor_channels.json config (~10 channels). Error-dict pattern.
- `tools/discovery/news_scanner.py`: Scans _IN_PRODUCTION projects for news relevance. Has SLUG_OVERRIDES mapping. Called by `/next --timely`.
- `tools/discovery/recommender.py`: TopicRecommender with pattern-weighted scoring. Scans _IN_PRODUCTION/ and _ARCHIVED/ for dedup. KeywordDB integration.
- `tools/discovery/opportunity.py`: OpportunityScorer with SAW formula. 4-dimension scoring. audience_potential as 4th dimension.
- `tools/discovery/database.py`: KeywordDB class — SQLite, schema v29. Central data store for discovery pipeline.
- `tools/research/competitor_gap.py`: Transcript analysis for competitor videos. Extracts topics, claims, figures, dates from transcripts.
- `tools/topic_pipeline.py`: Topic type multipliers, geographic monopoly bonus, news hook urgency scoring, hybrid topic detection.

### Established Patterns
- Error-dict pattern: return `{'error': msg}` on failure, never raise
- Feature flags: `TRENDSPYG_AVAILABLE`, `FEEDPARSER_AVAILABLE` for optional deps
- Lazy imports to break circular dependencies (recommender.py, diagnostics.py)
- Structured logging via `tools.logging_config.get_logger(__name__)`
- CLI entry points in `__main__` blocks with argparse

### Integration Points
- `/discover` command (`.claude/commands/`) — add `--scan` flag
- `channel-data/` directory — write DISCOVERY-FEED.md alongside existing reports
- `channel-data/TOPIC-PIPELINE.md` — discovery feed is separate but read by `/next`
- `keywords.db` — potential storage for LLM classifications cache
- `competitor_channels.json` — channel suggestion output references this file

</code_context>

<specifics>
## Specific Ideas

- Extended Belize formula adds subscriber conversion potential as 5th factor — the data shows ideological myth-busting converts at 3.5x the rate of territorial disputes
- Relative view threshold (>2x channel average) is smarter than fixed threshold — catches breakout topics from small competitors, not just big channels
- Channel suggestions emerge naturally from scan results — if an untracked channel keeps appearing in relevant searches, it's probably worth watching
- Per-scan urgency (no persistence) keeps things simple — the DISCOVERY-FEED.md is a snapshot, not a living document

</specifics>

<deferred>
## Deferred Ideas

- Scheduled/automated scanning (cron) — complexity vs value for solo creator doesn't justify now
- DB-stored discovery feed with historical tracking — markdown report is sufficient at current scale
- Auto-populating TOPIC-PIPELINE.md from discovery feed — manual curation is better until pipeline is proven
- Semantic similarity matching for competitor topics (vs keyword + LLM hybrid) — over-engineered for ~15 videos per channel

</deferred>

---

*Phase: 62-proactive-topic-discovery*
*Context gathered: 2026-03-14*
