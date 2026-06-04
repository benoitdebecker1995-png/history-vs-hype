# Tool Inventory

**Updated:** 2026-03-21

## YouTube Analytics (`tools/youtube_analytics/`)
- `analyze.py` — Post-publish analysis (long-form only!). Usage: `python -m tools.youtube_analytics.analyze VIDEO_ID --save --markdown`
- `patterns.py` — Cross-video pattern reports. Usage: `python -m tools.youtube_analytics.patterns --all`
- `auth.py` — OAuth2 (scopes: yt-analytics.readonly, youtube.readonly, youtube.force-ssl)
- `backfill.py` — DB population from JSON/markdown. `run_backfill(Path('.'))`
- `playbook_synthesizer.py` — Updates STYLE-GUIDE.md Part 9 from retention data
- `retention_analysis.py` — Content-type to retention mapping (42 videos, 4200 data points). `--report`
- `script_srt_deviation.py` — Script vs filmed SRT comparison (20 projects). `--report`
- `comment_analysis.py` — Comment text mining with real API. `--fetch --report`
- `pacing_analysis.py` — WPM/sentence pacing vs retention (non-finding). `--cached --report`
- `traffic_analysis.py` — Traffic source breakdown. `--report`
- `velocity_analysis.py` — First 48h velocity curves. `--report`
- `geography_analysis.py` — Audience geography by topic. `--report`
- `search_term_analysis.py` — Search queries driving traffic. `--report`
- `curve_shape_analysis.py` — Retention curve shape classification. `--cached --report`
- `ctr_by_source_analysis.py` — CTR by traffic source. `--report`
- `endscreen_analysis.py` — End screen click-through. `--report`
- `retention_predictor.py` — **NEW** Predict retention curve from script before filming. `--project SLUG` or `--script PATH`
- `auto_srt_fixer.py` — **NEW** Auto-generate SRT fixes from corrections dictionary. `--project SLUG` or `--srt PATH`
- `description_gap_filler.py` — **NEW** Find missing high-value keywords in descriptions. `--report`
- API is READ-ONLY — cannot modify titles, thumbnails, descriptions

## Discovery (`tools/discovery/`)
- `news_hook_monitor.py` — **NEW** Scan Google News RSS for pipeline topic spikes. `--scan --report`

## Benchmark (`tools/benchmark/`)
- `outlier_title_dissector.py` — **NEW** Extract title patterns from 3x+ outlier videos. `--report` or `--score "Title"`

## YouTube Intelligence (`tools/intel/`)
- `query.py` — Query algorithm knowledge, competitor data, niche patterns
- `competitor_tracker.py` / `competitor_patterns.py` — Track competitor channels
- `algo_synthesizer.py` / `algo_scraper.py` — Algorithm mechanics
- `topic_scorer.py` / `topic_vocabulary.py` — Score topic viability
- `pattern_analyzer.py` — Analyze patterns across videos
- `kb_store.py` / `kb_exporter.py` — Knowledge base storage
- `refresh.py` — Refresh intel data
- Invoked via `/intel` skill

## Discovery (`tools/discovery/`)
- `keywords.py` + `keywords.db` — Keyword research database (SQLite)
- `autocomplete.py` — YouTube autocomplete suggestions
- `diagnostics.py` — Discovery diagnostics (used by analyze.py)
- `opportunity.py` — Opportunity scoring
- `competition.py` — Competition analysis
- `demand.py` / `trends.py` — Demand estimation
- `recommender.py` — Topic recommendations
- `metadata_checker.py` — Check metadata quality
- `orchestrator.py` — Orchestrates discovery workflow
- Invoked via `/discover` skill

## Preflight (`tools/preflight/`)
- `scorer.py` — Pre-publish scoring (enhanced March 2026 with data-backed title patterns, publishing day check, opening hook analysis)
- `demand_checker.py` — Checks topic demand against keywords.db (VidIQ data). Limited to topics already in DB.
- `demand_scorer.py` — **NEW (2026-03-30)** Composite demand scorer using 3 free sources (no VidIQ needed):
  - YouTube Autocomplete (demand signal + keyword discovery)
  - pytrends with YouTube filter (calibrated volume estimation against known VidIQ anchors)
  - YouTube Data API top-result views (optional, needs YOUTUBE_API_KEY)
  - Usage: `python -m tools.preflight.demand_scorer "battle of thermopylae"`
  - Flags: `--json` for machine output, `--verbose` for debug
  - `/greenlight` falls back to this when demand_checker has no DB data
- `formatter.py` — Format preflight reports
- `thumbnail_checker.py` — Thumbnail concept validator
- Invoked via `/preflight` skill
- Title gate now scores: versus > declarative > how >> colon >> the_x_that
- Flags: year in title, question marks, "The [X] That [Verb]", bad publishing day

## Competitor Gap Analysis (`tools/research/competitor_gap.py`)
- `extract_topics_from_transcript()` — extracts topics, figures, dates, sources, primary source usage from a transcript
- `compare_coverage()` — compares our planned angles vs competitor coverage
- `format_gap_report()` — markdown report with standard narrative, unique angles, primary source advantage
- Agent: `.claude/agents/competitor-gap.md` — orchestrates WebSearch → transcript fetch → analysis → report
- Invoked via `/research --competitors "topic"` or `/research --competitors project-slug`
- Writes to `_research/COMPETITOR-GAP-ANALYSIS.md` when project path provided

## News Scanner (`tools/discovery/news_scanner.py`)
- Extracts pipeline topics from `_IN_PRODUCTION/` (skips published projects)
- Generates search queries for WebSearch-based news scanning
- Formats results as URGENT / TIMELY / EVERGREEN report
- Invoked via `/next --timely`
- Has slug-to-topic overrides for non-obvious project names

## Topic Pipeline (`tools/topic_pipeline.py`)
- Ranks future video topics by (search volume x channel fit x competitor gap)
- Usage: `python -m tools.topic_pipeline [--top N] [--save]`
- Saves to `channel-data/TOPIC-PIPELINE.md`
- Uses discovery DB keywords + own-channel performance + intel DB competitors
- Topic type multipliers: territorial 1.5x, ideological 1.4x, colonial 1.3x

## Important: Duration Check Before Analysis
Before running /analyze on any video, ALWAYS check duration via Data API:
```python
yt = get_authenticated_service('youtube', 'v3')
resp = yt.videos().list(id=VIDEO_ID, part='contentDetails').execute()
# Only analyze if > 3 minutes (PT3M)
```
Shorts (<3 min) should NEVER be analyzed — waste of API quota and produces misleading data.

## Data Assets

### Discovery DB (`tools/discovery/keywords.db`)
- 62 keywords tracked, 107 intent mappings, 78 trends
- 299 video performance records, 680 CTR snapshots
- 10 creator techniques catalogued
- Tables: keywords, keyword_intents, keyword_performance, trends, opportunity_scores, lifecycle_history, video_performance, thumbnail_variants, title_variants, ctr_snapshots, section_feedback, creator_techniques, script_choices

### Intel DB (`tools/intel/intel.db`)
- 9 competitor channels tracked: Kraut, Fall of Civilizations, Shaun, Knowing Better, Historia Civilis, Kings and Generals, Wendover, Johnny Harris, HistoryMarche
- 870 competitor videos catalogued
- 9 algorithm snapshots, 7 niche snapshots
- Last refreshed: 2026-03-01

### Channel Data CSVs (`channel-data/`)
- VidIQ CSV exports (Oct 2025, Nov 2025)
- YouTube Studio chart/table/totals exports (Dec 2024)

## Encoding Note (Windows)
When running Python scripts that output non-ASCII (accented characters), prefix with:
```bash
PYTHONIOENCODING=utf-8 python ...
```
Otherwise cp1252 codec errors on Windows. Use `.encode('ascii', 'replace').decode()` for safe terminal output.
