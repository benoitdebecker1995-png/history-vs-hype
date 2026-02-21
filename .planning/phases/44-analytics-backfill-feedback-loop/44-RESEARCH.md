# Phase 44: Analytics Backfill & Feedback Loop - Research

**Researched:** 2026-02-21
**Domain:** Python analytics pipeline, SQLite data integration, markdown parsing, command integration
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Backfill scope & sources:**
- Import ALL POST-PUBLISH-ANALYSIS files (both in project folders and channel-data/analyses/)
- Enrich with YouTube API data where available — parse analysis files first, then layer on API metrics
- Include all videos 2+ minutes (exclude Shorts), even those without POST-PUBLISH-ANALYSIS files — use YouTube API to create entries
- Idempotent + update: safe to re-run anytime, upserts existing records with latest API data

**Insight surfacing behavior:**
- Surface ALL insight types: retention patterns, topic performance, and format insights
- Insights are advisory, not prescriptive — guide experimentation, don't constrain it
- Surface insights during ALL production commands: /script, /prep, /publish, /research --new
- Generate a standalone channel insights report file (like youtube-intelligence.md) AND load it as context during production commands
- Key principle from user: "I want insights but also keep experimenting until I find a winning formula" — insights inform, never dictate

**Topic recommendation updates:**
- Balance proven patterns with experimentation: boost topics matching successful categories, but also surface novel/underexplored opportunities
- Composite score blending views, retention, and subscriber conversion
- Show reasoning for each recommendation — "similar to your Essequibo video (23K views, 19 subs)"

**Command design:**
- Per-video progress during backfill: "Importing Essequibo (1/15)... done"

### Claude's Discretion

- Incomplete data handling threshold (how sparse is too sparse to import)
- Whether to use existing analytics.db or create new consolidated DB
- Confidence flagging for insights (strong signal vs early signal)
- Insights presentation format (brief summary before script + silent agent context, or other)
- Recency weighting for topic recommendations (~15 videos, channel is evolving)
- Command structure: whether backfill is /analyze --backfill, standalone, or other
- Where insights report command lives (/patterns --insights, /analyze --insights, or other)
- Auto-add on /analyze vs manual re-run for new videos
- Dry-run mode: whether it adds value given idempotent design
- Data quality warnings in backfill output
- Auto-regeneration of insights report after /analyze runs
- Whether to also parse CHANNEL_ANALYTICS_MASTER.md and CSV files

### Deferred Ideas (OUT OF SCOPE)

None — discussion stayed within phase scope

</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| ANLYT-01 | Backfill command populates analytics DB from existing POST-PUBLISH-ANALYSIS files and YouTube API | `feedback_parser.backfill_all()` + `performance.fetch_catalog_metrics()` already exist. New backfill CLI wraps both, adds API enrichment layer, produces progress output. |
| ANLYT-02 | Channel-specific insights surface automatically during /script generation (what works for YOUR channel) | `feedback_queries.get_pre_script_insights()` already plumbed into `/script` command — but DB is nearly empty (only 2 videos have lessons_learned). ANLYT-01 must run first to populate it. Channel insights report file feeds all other commands. |
| ANLYT-03 | Analytics data feeds into topic recommendations with updated performance patterns | `topic_strategy.generate_topic_strategy()` already queries `video_performance` table. 146 records exist but `topic_type` is mis-classified ('general' dominates). Enriched DB enables correct classifications and composite scoring. |

</phase_requirements>

## Summary

Phase 44 has a critical dependency chain that must be understood before planning: **the infrastructure to do everything this phase requires already exists, but the database is sparsely populated**. The key insight is that this phase is primarily a data population and integration wiring task, not a new-code-from-scratch task.

The `video_performance` table in `tools/discovery/keywords.db` has 146 rows (competitor + own channel videos), but only 2 of them have `lessons_learned` populated. The analytics.db in `tools/youtube-analytics/` is completely empty (0 tables). All the parsing, insight, and strategy logic is already written and working — it just has no data to query. The `feedback_parser.py` module already contains `backfill_all()` which scans all POST-PUBLISH-ANALYSIS files and loads into `keywords.db`. The gap is that it has never been run comprehensively, and YouTube API enrichment (views, retention, CTR) is missing for most videos.

Two existing JSON pre-fetches contain the richest data: `_longform_enriched.json` (20 own-channel videos with impressions, CTR, avg_retention, final_retention) and `_longform_metrics.json` (40 videos with basic metrics). These should be the primary import source rather than re-fetching from the API, since API quota is limited.

The insight surfacing mechanism is already wired into `/script` via `get_pre_script_insights()` in `feedback_queries.py`. However, `/prep`, `/publish`, and `/research --new` have no equivalent wiring yet. The channel insights report should be a separate file (e.g., `channel-data/channel-insights.md`) distinct from the YouTube Intelligence KB (`channel-data/youtube-intelligence.md`), since the latter covers algorithm/competitor intelligence while this covers own-channel performance patterns.

**Primary recommendation:** Build a `tools/youtube-analytics/backfill.py` module that (1) loads JSON pre-fetches into `video_performance`, (2) parses all POST-PUBLISH-ANALYSIS files via existing `backfill_all()`, (3) re-classifies topic types using proper TAG_VOCABULARY, (4) generates `channel-data/channel-insights.md`, then wire this into all four commands via a shared utility function.

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| `sqlite3` | stdlib | Database read/write to keywords.db | Already in use across all tools |
| `pathlib` | stdlib | File discovery for POST-PUBLISH-ANALYSIS files | Already used in `feedback_parser.find_analysis_files()` |
| `json` | stdlib | Load pre-fetched JSON files (_longform_enriched.json etc.) | Already in use |
| `re` | stdlib | Extract video IDs and metrics from markdown | Already used in `feedback_parser.extract_metrics()` |
| `statistics` | stdlib | mean(), median() for topic aggregation | Already used in `topic_strategy.py` |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `argparse` | stdlib | CLI argument parsing for backfill command | Standard pattern across all tools in repo |
| `datetime` | stdlib | Timestamp tracking and recency weighting | Already used universally |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| keywords.db (existing) | analytics.db (empty) | analytics.db is empty and has no schema — using keywords.db avoids double-migration and leverages existing `video_performance` table with 146 rows already |
| Pre-fetched JSON files | YouTube API calls | JSON files have enriched data (CTR, retention) already fetched; API quota is limited; JSON is the faster, safer choice |

**Installation:** No new dependencies needed. All stdlib.

---

## Architecture Patterns

### Existing Infrastructure Map

```
tools/youtube-analytics/
├── backfill.py              [NEW - Phase 44 primary deliverable]
├── feedback_parser.py       [EXISTS - backfill_all(), find_analysis_files(), parse_analysis_file()]
├── performance.py           [EXISTS - fetch_video_performance(), classify_topic_type()]
├── feedback_queries.py      [EXISTS - get_pre_script_insights(), get_insights_preamble()]
├── topic_strategy.py        [EXISTS - generate_topic_strategy(), format_strategy_markdown()]
├── analyze.py               [EXISTS - run_analysis(), save_analysis()]
├── _longform_enriched.json  [EXISTS - 20 own-channel videos, full metrics + CTR + retention]
├── _longform_metrics.json   [EXISTS - 40 own-channel videos, basic metrics]
└── analytics.db             [EXISTS but empty - NOT to be used]

tools/discovery/
└── keywords.db              [EXISTS - video_performance table has 146 rows, 2 with lessons]

channel-data/
├── youtube-intelligence.md  [EXISTS - competitor/algorithm intel, auto-generated by Phase 43]
└── channel-insights.md      [NEW - own-channel performance patterns, Phase 44 deliverable]

.claude/commands/
├── script.md                [EXISTS - already calls get_pre_script_insights() for /script]
├── prep.md                  [EXISTS - needs channel-insights wiring]
├── publish.md               [EXISTS - needs channel-insights wiring]
└── research.md              [EXISTS - needs channel-insights wiring]
```

### Pattern 1: Backfill Pipeline (Three-Stage)

**What:** Import data from JSON pre-fetches → POST-PUBLISH-ANALYSIS markdown → API fallback
**When to use:** New backfill.py module, `run_backfill()` entry point

```python
# Source: existing patterns in performance.py + feedback_parser.py

def run_backfill(project_root: Path, force: bool = False) -> dict:
    results = {'imported_json': 0, 'imported_md': 0, 'api_enriched': 0, 'errors': []}

    # Stage 1: Load pre-fetched JSON (fastest, most complete data)
    results['imported_json'] = _import_from_json(project_root)

    # Stage 2: Parse POST-PUBLISH-ANALYSIS files (adds lessons, drop points)
    md_result = backfill_all(project_root, force=force)  # existing function
    results['imported_md'] = md_result['processed']
    results['errors'].extend(md_result.get('details', []))

    # Stage 3: Re-classify topic types (fix 'general' dominance)
    _reclassify_topics(project_root)

    return results
```

**Stage 1 detail — JSON import with progress output (per locked decision):**
```python
def _import_from_json(project_root: Path) -> int:
    json_path = project_root / 'tools' / 'youtube-analytics' / '_longform_enriched.json'
    if not json_path.exists():
        json_path = project_root / 'tools' / 'youtube-analytics' / '_longform_metrics.json'

    with open(json_path, 'r') as f:
        videos = json.load(f)

    db = KeywordDB()
    count = 0
    total = len(videos)

    for i, video in enumerate(videos, 1):
        title_short = video.get('title', 'Unknown')[:30]
        print(f"Importing {title_short} ({i}/{total})... ", end='', flush=True)

        # Upsert into video_performance (idempotent)
        result = db.add_video_performance(
            video_id=video['video_id'],
            title=video['title'],
            views=video.get('views', 0),
            # ... other fields
            # enriched fields:
            avg_retention_pct=video.get('avg_retention'),
        )
        if 'error' not in result:
            count += 1
            print("done")
        else:
            print(f"ERROR: {result['error']}")

    db.close()
    return count
```

### Pattern 2: Channel Insights Report Generation

**What:** Query aggregated channel data and write `channel-data/channel-insights.md`
**When to use:** After backfill completes; also after each new `/analyze` run

```python
# Source: pattern from topic_strategy.format_strategy_markdown() + youtube-intelligence.md style

def generate_channel_insights(project_root: Path) -> dict:
    """
    Generates channel-data/channel-insights.md with own-channel performance patterns.
    Distinct from youtube-intelligence.md (which covers algorithm/competitor data).

    Returns: {'saved_to': path, 'video_count': N, 'error': optional}
    """
    strategy = generate_topic_strategy()  # existing function
    patterns = extract_winning_patterns()  # existing function

    # Build report
    lines = [
        "# Channel Performance Insights",
        "",
        f"> Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC",
        "> Auto-generated by tools/youtube-analytics/backfill.py",
        "",
        "## Own-Channel Patterns",
        # ... topic performance table, top performers, conversion leaders
        # ... CONFIDENCE flagging: '(strong signal, 5+ videos)' vs '(early signal, 1-2 videos)'
    ]

    output_path = project_root / 'channel-data' / 'channel-insights.md'
    output_path.write_text('\n'.join(lines), encoding='utf-8')

    return {'saved_to': str(output_path), 'video_count': N}
```

### Pattern 3: Multi-Command Insight Surfacing

**What:** Load channel-insights.md as context in /prep, /publish, /research --new
**When to use:** Adding to .claude/commands/prep.md, publish.md, research.md

```markdown
## Channel Insights Check (Auto-run)

Before generating output, load channel performance context:

```python
from pathlib import Path
insights_path = Path('channel-data/channel-insights.md')
if insights_path.exists():
    channel_insights = insights_path.read_text(encoding='utf-8')
    # Use as internal context — do NOT dump raw to user
    # Surface as brief advisory block
```

**Display format (brief, not blocking):**
```
--- Channel Performance Context ---
Top format: territorial (avg 1,950 views, 0.63% conversion)
Best retention: KGB/Palestine video (42.0%)
Low signal: insights based on ~15 videos — experiment freely
---
```
```

### Pattern 4: Composite Topic Scoring

**What:** Score topics by blending views + retention + subscriber conversion
**When to use:** `generate_topic_strategy()` extension, feeds /next command

```python
# Composite score: weighted blend per user decision
def composite_score(views, avg_retention, conversion_rate, weights=None):
    if weights is None:
        # Balanced for ~15-video channel (evolving channel, no over-weighting)
        weights = {'views': 0.4, 'retention': 0.35, 'conversion': 0.25}

    # Normalize each metric to 0-1 scale against channel max
    views_n = views / channel_max_views
    retention_n = avg_retention  # Already 0-1
    conversion_n = conversion_rate / channel_max_conversion

    return (views_n * weights['views'] +
            retention_n * weights['retention'] +
            conversion_n * weights['conversion'])
```

### Anti-Patterns to Avoid

- **Using analytics.db:** It is empty with no schema. All existing tools use `keywords.db`. Do not create migration to analytics.db — use the existing `video_performance` table in keywords.db exclusively.
- **Re-fetching YouTube API for backfill:** The JSON pre-fetches already have CTR and retention data. API quota is limited. Use JSONs as primary data source; only fall back to API for videos not in JSONs.
- **Blocking /script on no data:** The existing `get_pre_script_insights()` already returns empty gracefully. New commands should do the same — never block production on missing analytics.
- **Duplicating youtube-intelligence.md:** `channel-insights.md` covers OWN channel performance; `youtube-intelligence.md` covers algorithm mechanics and competitors. Keep them separate.
- **Over-prescriptive insights:** Per locked user decision, insights are advisory. Never frame them as "you must do X." Use language like "has worked well historically" not "always do."

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| POST-PUBLISH-ANALYSIS parsing | Custom markdown parser | `feedback_parser.parse_analysis_file()` | Already handles all fields: video_id, metrics, lessons, drop_points, discovery diagnosis |
| DB write for lessons/feedback | Custom insert | `db.store_video_feedback(video_id, feedback_data)` | Handles upsert, 'no_match' case, error dict pattern |
| Video performance upsert | Custom SQL | `db.add_video_performance(...)` | Full upsert with all 14 metric fields, topic classification |
| Topic strategy aggregation | Custom groupby | `topic_strategy.generate_topic_strategy()` | Full aggregation with confidence flagging, best/worst, next steps |
| Pre-script insight formatting | Custom formatter | `feedback_queries.get_pre_script_insights()` + `format_pre_script_display()` | Already produces display-ready text with confidence labels |
| File discovery scan | Custom glob | `feedback_parser.find_analysis_files(project_root)` | Scans all 4 lifecycle folders + channel-data/analyses/ correctly |
| Topic classification | Custom keyword match | `performance.classify_topic_type(title)` | Uses TAG_VOCABULARY with 7 categories |

**Key insight:** ~90% of the logic for this phase already exists. The primary work is: (1) wiring JSON import into a backfill orchestrator, (2) generating channel-insights.md, (3) adding insight loading to 3 commands that lack it, and (4) fixing the topic mis-classification problem.

---

## Common Pitfalls

### Pitfall 1: Topic Classification Dominance of 'general'

**What goes wrong:** 146 rows in video_performance, but most are classified as 'general'. The TAG_VOCABULARY in `performance.py` uses keywords like 'dispute', 'border', 'myth', 'colonial' but many channel videos have titles that don't match these keywords (e.g., "Iran Wrote a Democratic Constitution" doesn't match any category despite being 'colonial' or 'legal').

**Why it happens:** Keyword matching on title only; titles often don't contain TAG_VOCABULARY keywords.

**How to avoid:** After JSON import, run re-classification with expanded vocabulary. Also add title-based heuristics for known videos. Re-classification should be idempotent and run after every backfill.

**Warning signs:** `generate_topic_strategy()` showing most videos under 'general' category.

### Pitfall 2: Double-Counting own-channel vs Competitor Videos

**What goes wrong:** The `video_performance` table mixes own-channel videos (from `performance.py --fetch-all`) with competitor videos pulled by the intel tools. The 146 existing rows include both. Insights generated from this mixed pool would be misleading.

**Why it happens:** No `is_own_channel` flag on the table. Own-channel videos tend to have higher views (e.g., 28K for Belize) but competitor data also exists.

**How to avoid:** Filter by known own-channel video IDs from JSON pre-fetches when generating insights. The `_longform_enriched.json` and `_longform_metrics.json` are the authoritative list of own-channel long-form videos (20 and 40 respectively).

**Warning signs:** Insights referencing competitor channel video titles.

### Pitfall 3: analytics.db Confusion

**What goes wrong:** `tools/youtube-analytics/analytics.db` exists but is completely empty (0 tables, schema version 0). A planner might create a new schema there thinking it's the intended store.

**Why it happens:** The file was likely created as a placeholder or during a previous failed migration attempt.

**How to avoid:** Use `tools/discovery/keywords.db` exclusively. The `video_performance` table there already has the data and schema. Do not create new tables in analytics.db.

### Pitfall 4: Sparse POST-PUBLISH-ANALYSIS Files

**What goes wrong:** Most analysis files in the project were generated during API token refresh errors (RefreshError) and contain mostly empty data — no views, no retention, no comments. Only the project-folder analyses (6 files) have some useful data; the channel-data/analyses/ files (4 files) have mostly empty data.

**Why it happens:** The `/analyze` command was run when OAuth token had expired, producing "RefreshError" for all API calls.

**How to avoid:** During backfill, treat "Performance data unavailable" files as low-quality — import video_id and file existence but don't overwrite good API data with null values. The JSON pre-fetches are more reliable than the markdown files for metrics.

**Warning signs:** `parse_analysis_file()` returning `views=None`, `avg_retention=None` for most files.

### Pitfall 5: Insight Report Replacing youtube-intelligence.md

**What goes wrong:** Building channel-insights.md with the same structure as youtube-intelligence.md, causing confusion about which file to read.

**Why it happens:** Both are performance-oriented markdown files in channel-data/.

**How to avoid:** Clear separation of concerns. `youtube-intelligence.md` = algorithm mechanics + competitor landscape (auto-generated by Phase 43 intel tools, refreshed from RSS/web). `channel-insights.md` = own-channel historical performance (generated by backfill.py, updated after each /analyze run). Different headers, different update triggers, different content.

### Pitfall 6: Recency Bias in a 15-Video Dataset

**What goes wrong:** With only ~15-20 own-channel long-form videos, any topic type with 1-2 videos produces statistically unreliable insights. The existing `topic_strategy.py` already handles this with confidence flags ('low' for <3 videos, 'medium' for <6). However, the user specifically noted "I want to keep experimenting" — so insights must lean advisory.

**How to avoid:** Always display confidence level with insights. For 1-2 video topic types, use language: "early signal (2 videos) — continue experimenting." For 3+ videos: "moderate signal." For 6+ videos: "strong signal." The channel currently has no topic type with 6+ videos, so all insights are early-to-moderate signal.

---

## Code Examples

### Loading JSON Pre-Fetches into video_performance

```python
# Source: existing pattern from performance.py fetch_video_performance()
# New code in backfill.py

import json
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent / 'discovery'))
from database import KeywordDB
from performance import classify_topic_type, classify_own_video

def import_from_json_prefetch(project_root: Path) -> dict:
    """
    Import own-channel video metrics from pre-fetched JSON files.
    Uses _longform_enriched.json (has CTR + retention) if available,
    falls back to _longform_metrics.json (basic metrics only).
    """
    analytics_dir = project_root / 'tools' / 'youtube-analytics'

    # Prefer enriched (has CTR + retention)
    enriched_path = analytics_dir / '_longform_enriched.json'
    metrics_path = analytics_dir / '_longform_metrics.json'

    json_path = enriched_path if enriched_path.exists() else metrics_path
    if not json_path.exists():
        return {'error': 'No JSON pre-fetch found', 'imported': 0}

    with open(json_path, 'r', encoding='utf-8') as f:
        videos = json.load(f)

    db = KeywordDB()
    imported = 0
    skipped = 0
    errors = []
    total = len(videos)

    print(f"Found {total} videos in {json_path.name}")
    print()

    for i, video in enumerate(videos, 1):
        video_id = video.get('video_id', '')
        title = video.get('title', 'Unknown')
        title_short = title[:35]

        print(f"  Importing {title_short}... ({i}/{total})", end=' ', flush=True)

        classification = classify_own_video(title)

        result = db.add_video_performance(
            video_id=video_id,
            title=title,
            views=video.get('views', 0),
            subscribers_gained=video.get('subscribers_gained', 0),
            subscribers_lost=video.get('subscribers_lost', 0),
            conversion_rate=_safe_conversion(
                video.get('views', 0),
                video.get('subscribers_gained', 0)
            ),
            watch_time_minutes=video.get('watch_time_minutes'),
            avg_view_duration_seconds=video.get('avg_view_duration_seconds'),
            likes=video.get('likes'),
            comments=video.get('comments'),
            shares=video.get('shares'),
            topic_type=classification['topic_type'],
            angles=classification['angles']
        )

        if 'error' not in result:
            imported += 1
            print("done")
        else:
            errors.append({'video_id': video_id, 'error': result['error']})
            print(f"ERROR: {result['error']}")

    db.close()
    return {'imported': imported, 'skipped': skipped, 'errors': errors}
```

### Channel Insights Report Generation

```python
# Source: pattern from topic_strategy.format_strategy_markdown()
# New function in backfill.py or separate channel_insights.py

def generate_channel_insights_report(project_root: Path) -> dict:
    """
    Generate channel-data/channel-insights.md from own-channel performance data.
    Covers: topic performance, top performers, format insights.
    Distinct from youtube-intelligence.md (algorithm/competitor focus).
    """
    from topic_strategy import generate_topic_strategy
    from performance import extract_winning_patterns  # if available

    strategy = generate_topic_strategy()
    if 'error' in strategy:
        return {'error': f'Cannot generate insights: {strategy["error"]}'}

    lines = [
        "# Channel Performance Insights",
        "",
        f"> Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC",
        f"> Videos analyzed: {strategy['total_videos']}",
        "> Auto-generated. Do not edit manually.",
        "",
        "---",
        "",
        "## Performance by Topic Type",
        "",
        "| Topic | Videos | Avg Retention | Avg Conv% | Signal |",
        "|-------|--------|---------------|-----------|--------|",
    ]

    for stat in strategy['topic_stats']:
        # Confidence label
        confidence_map = {'high': 'strong', 'medium': 'moderate', 'low': 'early'}
        signal = f"{confidence_map.get(stat['confidence'], '?')} ({stat['video_count']} videos)"
        lines.append(
            f"| {stat['topic']} | {stat['video_count']} | "
            f"{stat['avg_retention']:.1f}% | "
            f"{stat['avg_conversion']:.2f}% | {signal} |"
        )

    lines.extend([
        "",
        "## Top Performers",
        "",
    ])

    # Add best video per category
    for stat in strategy['best_performing'][:3]:
        best = stat['best_video']
        lines.append(
            f"**{stat['topic'].title()}:** {best['title']} "
            f"({best['conversion']:.2f}% conversion)"
        )

    lines.extend([
        "",
        "## Channel Signals",
        "",
        "Insights based on ~15 long-form videos. All signals are early-to-moderate.",
        "Experiment freely — these are patterns, not prescriptions.",
        "",
    ])

    for step in strategy['concrete_next_steps'][:4]:
        lines.append(f"- {step}")

    output_path = project_root / 'channel-data' / 'channel-insights.md'
    output_path.write_text('\n'.join(lines), encoding='utf-8')

    return {
        'saved_to': str(output_path),
        'video_count': strategy['total_videos']
    }
```

### Command Integration Pattern (for /prep, /publish, /research --new)

```markdown
## Channel Insights Context (Auto-run)

Before generating output, load own-channel performance context:

```python
from pathlib import Path

insights_path = Path('channel-data/channel-insights.md')
if insights_path.exists():
    channel_insights = insights_path.read_text(encoding='utf-8')
    # Use as silent context for decisions
    # Display brief advisory if topic type known
    print("--- Channel Performance Context ---")
    # Extract relevant lines from insights (topic performance, top signals)
    # Show 2-3 lines max
    print("---")
```

**Do NOT display full channel-insights.md dump.** Surface only a 2-3 line advisory block.
**Never block generation if file missing.** Graceful degradation: skip silently.
```

### Backfill CLI Interface

```python
# Source: argparse pattern from performance.py CLI
# New backfill.py CLI entry point

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Backfill analytics DB from existing channel data',
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Re-import even if data already exists (update mode)'
    )
    parser.add_argument(
        '--insights-only',
        action='store_true',
        help='Skip import, only regenerate channel-insights.md'
    )
    parser.add_argument(
        '--json-only',
        action='store_true',
        help='Only import from JSON pre-fetches (skip markdown parsing)'
    )

    args = parser.parse_args()
    project_root = Path(__file__).parent.parent.parent

    if args.insights_only:
        result = generate_channel_insights_report(project_root)
        print(f"Channel insights saved to: {result.get('saved_to', 'error')}")
    else:
        result = run_backfill(project_root, force=args.force)
        print(f"\nBackfill complete:")
        print(f"  JSON import: {result['imported_json']} videos")
        print(f"  Markdown import: {result['imported_md']} analyses")
        print(f"  Errors: {len(result.get('errors', []))}")
        print()
        # Auto-generate insights after backfill
        insights_result = generate_channel_insights_report(project_root)
        if 'error' not in insights_result:
            print(f"Channel insights saved to: {insights_result['saved_to']}")
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| feedback_parser.backfill_all() only imports markdown | Phase 44 wraps it + JSON pre-fetch layer | Phase 44 (now) | Richer data: CTR, retention, impressions from enriched JSON |
| /script is only command with pre-script insights | All 4 production commands surface insights | Phase 44 (now) | User gets channel context at /prep, /publish, /research |
| topic_strategy shows raw averages | Composite score (views + retention + conversion) | Phase 44 (now) | Better topic recommendations that balance all three signals |
| No own-channel insight file separate from intel | channel-insights.md generated automatically | Phase 44 (now) | Clear separation: own-channel patterns vs algorithm/competitor |

**No deprecated approaches.** All existing modules are valid and continue to be used.

---

## Open Questions

1. **Should backfill auto-run as part of /analyze?**
   - What we know: `/analyze` already calls `feedback_parser.parse_analysis_file()` and `db.store_video_feedback()` in `save_analysis()`. This auto-stores feedback after each new analysis.
   - What's unclear: Whether to also auto-regenerate `channel-insights.md` after each `/analyze` call.
   - Recommendation: Yes, auto-regenerate `channel-insights.md` after each `/analyze --save`. This keeps insights current without user action. Add 1 line to `analyze.py:save_analysis()`.

2. **Should CHANNEL_ANALYTICS_MASTER.md be parsed?**
   - What we know: It contains manually-maintained stats (total views, averages, by-video table). Parsing it would risk stale/wrong data.
   - What's unclear: Whether it contains data not available via API/JSON.
   - Recommendation: Do NOT parse it. It is a human-maintained artifact and may diverge from API data. JSON pre-fetches are more reliable and machine-generated.

3. **Should channel-data/data.csv and Table data.csv be parsed?**
   - What we know: `data.csv` is an untracked file (in git status). Its content is unknown.
   - What's unclear: Whether it contains unique data vs. the JSON pre-fetches.
   - Recommendation: Leave for Claude's discretion. The JSON pre-fetches have the canonical enriched data. Only add CSV parsing if data.csv contains data NOT in the JSON files.

4. **Command naming for backfill**
   - What we know: User left this to Claude's discretion. Existing `/analyze` runs per-video. Backfill is a bulk operation.
   - Recommendation: Standalone command `/analyze --backfill` is the most natural fit. It extends the existing analyze command family, signals "this is an analytics operation," and keeps the command namespace clean. Alternative: standalone `/backfill` slash command. Either works.

5. **Dry-run mode**
   - What we know: Idempotent design means re-running is always safe.
   - Recommendation: Skip dry-run mode. The idempotent upsert design already solves the "what will this do?" concern. Progress output ("Importing Essequibo (1/15)... done") provides visibility without needing a separate dry-run pass.

---

## Sources

### Primary (HIGH confidence)
- `G:\History vs Hype\tools\youtube-analytics\feedback_parser.py` — Complete backfill_all(), find_analysis_files(), parse_analysis_file() implementation
- `G:\History vs Hype\tools\youtube-analytics\performance.py` — fetch_video_performance(), classify_topic_type(), TAG_VOCABULARY
- `G:\History vs Hype\tools\youtube-analytics\feedback_queries.py` — get_pre_script_insights(), format_pre_script_display(), get_insights_preamble()
- `G:\History vs Hype\tools\youtube-analytics\topic_strategy.py` — generate_topic_strategy(), format_strategy_markdown()
- `G:\History vs Hype\tools\youtube-analytics\analyze.py` — run_analysis(), save_analysis(), find_project_folder()
- `G:\History vs Hype\.claude\commands\script.md` — PRE-SCRIPT INTELLIGENCE section, existing implementation pattern
- `G:\History vs Hype\tools\youtube-analytics\_longform_enriched.json` — 20 own-channel videos with CTR, retention, impressions
- `G:\History vs Hype\tools\youtube-analytics\_longform_metrics.json` — 40 own-channel videos with basic metrics
- `keywords.db` — video_performance schema confirmed (20 columns), 146 rows (2 with lessons_learned)

### Secondary (MEDIUM confidence)
- `G:\History vs Hype\channel-data\CHANNEL_ANALYTICS_MASTER.md` — Channel overview stats (manually maintained, may not reflect real-time)
- `G:\History vs Hype\channel-data\youtube-intelligence.md` — Structure reference for how Phase 43 generates its report

### Tertiary (LOW confidence)
- `G:\History vs Hype\.planning\STATE.md` — Context for what Phase 43 established about intel integration patterns

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all stdlib, all existing patterns in codebase
- Architecture: HIGH — existing modules confirmed working; gaps clearly identified
- Pitfalls: HIGH — confirmed via direct database inspection (146 rows, 2 with lessons_learned, analytics.db empty)
- Data landscape: HIGH — JSON pre-fetches confirmed with 20/40 own-channel videos and full enriched metrics

**Research date:** 2026-02-21
**Valid until:** 2026-03-21 (stable domain — own-channel data structure, no external API changes)
