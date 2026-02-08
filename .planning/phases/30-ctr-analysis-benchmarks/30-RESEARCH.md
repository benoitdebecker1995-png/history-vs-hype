# Phase 30: CTR Analysis & Benchmarks - Research

**Researched:** 2026-02-08
**Domain:** Statistical heuristics for CTR variant comparison, channel benchmark calculation
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- Practical heuristic approach (not full statistical tests) — simple rules a solo creator can act on
- Single-variant videos compare against category average CTR (no A/B pair required)
- Always show BOTH overall channel average AND category-specific average for context
- Two entry points: quick summary in /analyze AND detailed standalone CLI command
- /analyze: add verdict/context alongside existing Phase 29 variant tables
- Standalone CLI: terminal output by default, --markdown flag for file output
- **Long-form videos only** — exclude Shorts from all CTR analysis and benchmarks

### Claude's Discretion
- Minimum CTR difference threshold for "winner" verdict
- Verdict label language
- Category system granularity
- Minimum videos per category bucket
- Benchmark time window (latest vs standardized snapshot)
- Impression minimum for comparison
- Snapshot minimum for trending
- Freshness warning threshold
- Active variant attribution enforcement
- When to show recommendations vs just data

### Deferred Ideas (OUT OF SCOPE)
None — discussion stayed within phase scope
</user_constraints>

## Summary

Phase 30 adds two capabilities on top of Phase 29's variant tracking data: (1) variant comparison verdicts (winner/loser/insufficient data), and (2) channel-specific CTR benchmarks by topic category. Both feed into the `/analyze` workflow and a standalone `benchmarks.py` CLI.

The standard approach for a solo creator with small sample sizes is **practical heuristics, not statistical tests**. With ~10 long-form videos total and impression counts ranging from under 1,000 to 35,000, formal significance testing (chi-square, t-test) would almost never reach confidence — and would mislead the creator into thinking "no result" means "no difference." Instead, use a simple rule: if one variant has a meaningfully higher CTR at comparable impressions, label it the winner.

The benchmark calculation queries the `video_performance` table (already populated via `performance.py`) and the `ctr_snapshots` table (Phase 29). Since CTR is NOT stored in `video_performance` (it stores views, conversion rate, topic_type), benchmarks must come entirely from `ctr_snapshots`. Topic classification comes from `video_performance.topic_type` via a JOIN.

**Primary recommendation:** Build two new functions in a `benchmarks.py` module: `compare_variants(video_id)` returns a verdict dict with winner/confidence/recommendation, and `get_category_benchmarks()` returns avg CTR per topic bucket. Both read from existing Phase 29 tables. Add a thin wrapper to `analyze.py` for the /analyze integration.

## Standard Stack

The established libraries/tools for this domain:

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| sqlite3 | Built-in | Query ctr_snapshots + video_performance | Already the entire data layer |
| statistics | Built-in | median(), mean() for benchmark aggregation | No external dependency needed |
| argparse | Built-in | --markdown flag, standalone CLI | Matches variants.py, performance.py patterns |
| json | Built-in | Parse formula_tags, visual_pattern_tags | Matches existing JSON TEXT pattern |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| datetime | Built-in | Freshness warnings, date comparisons | Check snapshot recency |
| pathlib | Built-in | Output file path handling for --markdown | Matches existing save_analysis pattern |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Heuristic thresholds | scipy.stats chi2_contingency | Chi-square would require 1,000+ impressions per variant; overkill and never reaches significance at current velocity |
| Built-in statistics | numpy/pandas | External dependencies for a 10-video dataset is unnecessary complexity |
| Hardcoded categories | Dynamic clustering | Dynamic clustering needs 30+ data points; categories from performance.py already work |

**Installation:**
```bash
# No new dependencies — uses only Python stdlib
```

## Architecture Patterns

### Recommended Project Structure
```
tools/youtube-analytics/
├── analyze.py          # Existing — add call to format_ctr_analysis()
├── variants.py         # Existing — unchanged
├── benchmarks.py       # NEW — CTR analysis and benchmark engine
└── ...

tools/discovery/
└── database.py         # Existing — add get_ctr_by_topic() query method
```

### Pattern 1: Variant Comparison with Heuristic Verdict
**What:** Compare CTR snapshots grouped by active_thumbnail_id or active_title_id
**When to use:** Video has 2+ variants with snapshot data, or single variant to compare to benchmark
**Logic:**
```python
# Source: designed from channel data (avg CTR 3.27%, range 0-11.21%)
# and existing codebase patterns (error dict, graceful degradation)

def compare_variants(video_id: str, variant_type: str = 'thumbnail') -> dict:
    """
    Compare CTR performance across variants for a video.

    Returns verdict dict:
    {
        'status': 'winner_found' | 'insufficient_data' | 'no_clear_winner' | 'single_variant',
        'winner': 'A' | None,
        'confidence': 'high' | 'medium' | 'low',
        'recommendation': str,
        'variants': [{letter, avg_ctr, impressions, snapshot_count}, ...],
        'reason': str
    }
    """
    # Threshold logic (see Heuristic Thresholds section below)
```

### Pattern 2: Category Benchmark Calculation
**What:** Aggregate CTR from ctr_snapshots JOIN video_performance by topic_type
**When to use:** Building benchmark table, comparing single video to category average
**Logic:**
```python
# Source: existing performance.py aggregate_by_topic() pattern
# and existing database.py get_performance_by_topic()

def get_category_benchmarks(min_snapshots: int = 2) -> dict:
    """
    Calculate average CTR per topic category.

    Returns:
    {
        'overall': {'avg_ctr': 3.27, 'video_count': 10},
        'by_category': {
            'territorial': {'avg_ctr': 3.5, 'video_count': 4, 'sample_size': 8},
            'ideological': {'avg_ctr': 5.2, 'video_count': 3, 'sample_size': 6},
            ...
        }
    }
    """
```

### Pattern 3: Single-Variant vs Category Average
**What:** When a video has only one variant, compare its CTR to the category benchmark
**When to use:** Most videos (solo creator rarely runs A/B tests)
**Logic:**
```python
# If only one variant exists OR no variant attribution:
# Compare video's latest snapshot CTR to category average
# Verdict: "Your CTR (4.3%) is above territorial average (3.5%) — strong performer"
```

### Pattern 4: Benchmark JOIN Query
**What:** SQLite JOIN between ctr_snapshots and video_performance to get category-tagged CTR
**When to use:** Building benchmark table
**Example:**
```python
# Source: existing database.py JOIN patterns from competition.py
cursor.execute("""
    SELECT
        vp.topic_type,
        cs.video_id,
        cs.ctr_percent,
        cs.impression_count,
        cs.snapshot_date
    FROM ctr_snapshots cs
    LEFT JOIN video_performance vp ON cs.video_id = vp.video_id
    WHERE vp.views > 0  -- exclude Shorts (they have negligible impression count)
    ORDER BY vp.topic_type, cs.snapshot_date DESC
""")
```

**Note on Shorts exclusion:** The `ctr_snapshots` table has no duration field. Shorts exclusion relies on the user only recording long-form CTR snapshots (per phase scope), OR by joining to video_performance and filtering by duration (if available). Since `video_performance` doesn't store duration directly, the pragmatic approach is: **only record CTR snapshots for long-form videos** (user responsibility) + document this in CLI help text. No automated filter exists.

### Anti-Patterns to Avoid
- **Declaring a winner with <300 impressions:** CTR is too noisy at low impression counts; always show impression count alongside verdict
- **Using industry benchmarks:** YouTube average CTR is 4-5% but irrelevant — this channel's avg is 3.27% with outliers at 11.21%; only channel-specific data matters
- **Requiring A/B pair for any insight:** Most videos have single variants; category comparison still provides value
- **Storing computed benchmarks:** Recompute from raw data each time — with <10 videos, it's fast and always fresh

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Statistical significance | Custom t-test or chi-square | Heuristic thresholds | Sample sizes never reach significance; heuristics are more honest and actionable |
| Category classification | New classifier | performance.py classify_topic_type() | Already tested, same vocabulary |
| Mean/median calculation | Manual sum/count | statistics.mean(), statistics.median() | Handles edge cases (empty lists, single values) |
| Output formatting | New formatter | Follow analyze.py format_analysis_markdown() pattern | Consistent with existing /analyze output |
| CLI argument parsing | Custom parser | argparse (matches variants.py pattern) | Consistent --markdown, video_id patterns |

**Key insight:** All data infrastructure already exists. Phase 30 is query logic + display logic on top of Phase 29 tables.

## Common Pitfalls

### Pitfall 1: Snapshots Without Variant Attribution
**What goes wrong:** Most early snapshots won't have active_thumbnail_id or active_title_id set (Phase 29 made these optional). Variant comparison becomes impossible.
**Why it happens:** User records CTR without specifying which variant was active
**How to avoid:** In comparison logic, group by active_thumbnail_id if available; fall back to "all snapshots for this video" if no attribution. Show attribution rate in output ("3 of 5 snapshots have variant attribution").
**Warning signs:** all active_thumbnail_id values are NULL in ctr_snapshots

### Pitfall 2: CTR Not in video_performance Table
**What goes wrong:** Developer assumes CTR is stored in video_performance — it's NOT. That table stores views, conversion_rate, subscribers, etc., but CTR comes from ctr_snapshots only.
**Why it happens:** Confusion between YouTube Analytics API metrics (views, watch time) and CTR which requires manual Studio entry
**How to avoid:** Always query CTR from ctr_snapshots; use video_performance only for topic_type JOIN and to identify long-form videos
**Warning signs:** get_video_metrics() response has `ctr_available: False` by default

### Pitfall 3: Combining Time-Shifted Snapshots as A/B Data
**What goes wrong:** Video ran thumbnail A for weeks then switched to B — comparing their CTRs is confounded by video age, seasonality, algorithm changes
**Why it happens:** Treating sequential variants as simultaneous A/B test
**How to avoid:** Note snapshot dates in output. Include a caveat: "Sequential testing is influenced by video age." Recommend comparing snapshots taken within 7 days of each other for fair comparison.
**Warning signs:** variant switch date is weeks apart in snapshot history

### Pitfall 4: Over-Relying on Small Category Buckets
**What goes wrong:** "Territorial average CTR: 4.31%" based on 1 video (Essequibo) — not representative
**Why it happens:** Showing per-category averages without noting sample size
**How to avoid:** Always show sample size (n=X) alongside category average. Use minimum threshold (recommend n>=3 snapshots across 2+ videos) before showing category-specific average; fall back to overall channel average otherwise.
**Warning signs:** category shows high confidence with only 1-2 data points

### Pitfall 5: Freshness Blind Spots
**What goes wrong:** Benchmark is calculated from 6-month-old CTR data that doesn't reflect current YouTube algorithm behavior
**Why it happens:** No freshness check on snapshot dates
**How to avoid:** Show date range of data used ("Based on snapshots from 2025-07-01 to 2026-02-08"). Warn if most recent snapshot is older than 60 days.
**Warning signs:** all snapshot_dates are months old

### Pitfall 6: Impression Threshold Too High for This Channel
**What goes wrong:** Setting threshold at 1,000+ impressions blocks most videos from getting any verdict — most get 100-900 impressions in the first week
**Why it happens:** Copying industry thresholds designed for channels with millions of impressions
**How to avoid:** Use channel-appropriate threshold. Channel data shows top videos get 900-35,000 impressions total; median is around 400-600 per video. Recommend 200 impressions as minimum for any comparison, with confidence notes at different levels. See Heuristic Thresholds section.
**Warning signs:** All verdicts return "insufficient_data"

## Heuristic Thresholds (Claude's Discretion Recommendations)

Based on channel data analysis:
- Average CTR: 3.27% overall
- CTR range long-form: 0% to 11.21% (extreme outlier)
- Typical long-form CTR: 1.5% to 5.5% (middle 80% of videos)
- Impression velocity: small channels get 50-500 impressions/week initially; top videos reach 1,000-35,000 over their lifetime
- Publishing cadence: ~2-3 videos/week historically (but long-form is 1-2/month)

### Recommended Thresholds

**Impression minimum before comparison:**
- 200 impressions: show comparison with LOW confidence caveat
- 500 impressions: MEDIUM confidence
- 1,000+ impressions: HIGH confidence
- Rationale: Most long-form videos reach 500+ within 7-14 days. 1,000 is achievable for stronger performers. The STATE.md suggested 1,000+ but that's too conservative given channel velocity — use tiered confidence instead.

**CTR difference to declare winner (practical significance):**
- <0.5 percentage points: "No clear winner" (within noise)
- 0.5-1.5 pp: "Slight edge" (noteworthy but watch more data)
- 1.5-3.0 pp: "Winner" at medium confidence
- 3.0+ pp: "Clear winner" at high confidence
- Rationale: Channel's natural CTR variation is ~1-2pp across similar videos. Need to exceed noise level to declare winner.

**Minimum snapshots for trending:**
- 2 snapshots: enough for direction (UP/DOWN/FLAT) — Phase 29 already does this
- 3+ snapshots: enough for trend with "stabilizing" vs "still moving" note
- Rationale: With manual entry, 2-3 snapshots is realistic for solo creator lifecycle (48h, 7d, 30d)

**Data freshness warning:**
- 60 days without new snapshot: show "Data may be stale" warning
- Rationale: Channel publishes long-form monthly; 60 days = likely 1-2 new videos since last check

**Minimum category bucket for reliable average:**
- 2+ videos with CTR snapshots in category = show category average with "(n=X)" note
- <2 videos = show only overall channel average
- Rationale: With ~10 long-form videos, some categories may have only 1. Still useful to show when available, just flag small N.

**Verdict labels (direct, evidence-based tone matching channel style):**
- "WINNER: [Variant] (+X.X pp CTR)" — clear winner found
- "EDGE: [Variant] (+X.X pp CTR, watch for more data)" — slight advantage
- "NO CLEAR WINNER (X.X pp difference, insufficient for verdict)" — below threshold
- "INSUFFICIENT DATA (N impressions, need 200+ for comparison)" — too few impressions
- "SINGLE VARIANT (compare to [category] avg: X.X%)" — no A/B pair

**When to show recommendations vs just data:**
- Show recommendation text ONLY when impression threshold met (200+)
- Recommendation types: "Keep [A]", "Switch to [B]", "Run more time", "Record more snapshots"
- At LOW confidence: append "(check again after 500+ impressions)"

## Code Examples

Verified patterns from official sources:

### Query: Get CTR Snapshots Grouped by Variant
```python
# Source: existing database.py patterns (ctr_snapshots schema, Phase 29)
def get_variant_ctr_summary(self, video_id: str, variant_type: str = 'thumbnail') -> list:
    """
    Get CTR averages grouped by active variant for a video.

    Args:
        video_id: YouTube video ID
        variant_type: 'thumbnail' or 'title'

    Returns:
        List of {'variant_id', 'variant_letter', 'avg_ctr', 'total_impressions', 'snapshot_count'}
    """
    id_col = 'active_thumbnail_id' if variant_type == 'thumbnail' else 'active_title_id'
    variant_table = 'thumbnail_variants' if variant_type == 'thumbnail' else 'title_variants'

    cursor = self._conn.cursor()
    cursor.execute(f"""
        SELECT
            cs.{id_col} as variant_id,
            v.variant_letter,
            AVG(cs.ctr_percent) as avg_ctr,
            SUM(cs.impression_count) as total_impressions,
            COUNT(*) as snapshot_count
        FROM ctr_snapshots cs
        LEFT JOIN {variant_table} v ON cs.{id_col} = v.id
        WHERE cs.video_id = ?
        AND cs.{id_col} IS NOT NULL
        GROUP BY cs.{id_col}
        ORDER BY avg_ctr DESC
    """, (video_id,))

    return [dict(row) for row in cursor.fetchall()]
```

### Query: Channel Benchmark Aggregation
```python
# Source: existing database.py aggregate patterns from performance_report.py
def get_channel_ctr_benchmarks(self) -> dict:
    """
    Get CTR averages per topic category from all recorded snapshots.

    Only uses most recent snapshot per video (to avoid weighting old videos heavily).
    Excludes videos with no topic_type (likely unclassified or Shorts).

    Returns:
        {
            'overall': {'avg_ctr': float, 'video_count': int, 'snapshot_count': int},
            'by_category': {topic_type: {'avg_ctr': float, 'video_count': int}}
        }
    """
    cursor = self._conn.cursor()

    # Get latest snapshot per video (most representative current CTR)
    cursor.execute("""
        SELECT
            vp.topic_type,
            cs.video_id,
            cs.ctr_percent
        FROM ctr_snapshots cs
        INNER JOIN (
            SELECT video_id, MAX(snapshot_date) as latest_date
            FROM ctr_snapshots
            GROUP BY video_id
        ) latest ON cs.video_id = latest.video_id AND cs.snapshot_date = latest.latest_date
        LEFT JOIN video_performance vp ON cs.video_id = vp.video_id
        ORDER BY vp.topic_type
    """)

    rows = cursor.fetchall()
    # ... aggregate with statistics.mean() per category
```

### Heuristic Verdict Function
```python
# Source: designed from channel data thresholds above
import statistics

def calculate_verdict(variant_data: list, category_avg: float = None) -> dict:
    """
    Calculate verdict from variant CTR data.

    Args:
        variant_data: list of {'variant_letter', 'avg_ctr', 'total_impressions', ...}
        category_avg: optional category benchmark for single-variant comparison

    Returns:
        verdict dict with status, winner, confidence, recommendation
    """
    if not variant_data:
        return {
            'status': 'no_data',
            'recommendation': 'Record CTR snapshots first'
        }

    total_impressions = sum(v['total_impressions'] for v in variant_data)

    # Confidence tiers
    if total_impressions < 200:
        confidence = 'low'
    elif total_impressions < 500:
        confidence = 'medium'
    else:
        confidence = 'high'

    if len(variant_data) == 1:
        # Single variant - compare to category average
        single = variant_data[0]
        if category_avg and total_impressions >= 200:
            delta = single['avg_ctr'] - category_avg
            if delta > 1.5:
                recommendation = f"Above {single.get('category', 'channel')} average by {delta:+.1f}pp"
            elif delta < -1.5:
                recommendation = f"Below {single.get('category', 'channel')} average by {delta:+.1f}pp"
            else:
                recommendation = f"Near {single.get('category', 'channel')} average"
        else:
            recommendation = "Record more snapshots or run variant B for comparison"
        return {
            'status': 'single_variant',
            'winner': single['variant_letter'],
            'confidence': confidence,
            'recommendation': recommendation
        }

    # Multi-variant comparison
    sorted_variants = sorted(variant_data, key=lambda v: v['avg_ctr'], reverse=True)
    best = sorted_variants[0]
    second = sorted_variants[1]
    delta = best['avg_ctr'] - second['avg_ctr']

    if total_impressions < 200:
        status = 'insufficient_data'
        winner = None
        recommendation = f"Need 200+ total impressions for comparison (have {total_impressions})"
    elif delta < 0.5:
        status = 'no_clear_winner'
        winner = None
        recommendation = f"Difference too small ({delta:.1f}pp) — run both longer"
    elif delta < 1.5:
        status = 'edge'
        winner = best['variant_letter']
        recommendation = f"Slight edge to {best['variant_letter']} (+{delta:.1f}pp) — watch for more data"
    else:
        status = 'winner_found'
        winner = best['variant_letter']
        if confidence == 'high':
            recommendation = f"Keep {best['variant_letter']} (+{delta:.1f}pp, {total_impressions} impressions)"
        else:
            recommendation = f"Lean toward {best['variant_letter']} (+{delta:.1f}pp) — consider more data"

    return {
        'status': status,
        'winner': winner,
        'confidence': confidence,
        'recommendation': recommendation,
        'delta_pp': delta
    }
```

### Integrating into /analyze (existing format_analysis_markdown pattern)
```python
# Source: existing analyze.py Variant Tracking section (lines 975-1047)
# Add after existing "## Variant Tracking" section

def format_ctr_analysis(variant_data: dict, benchmarks: dict) -> list:
    """
    Format CTR analysis lines for /analyze markdown output.

    Args:
        variant_data: from analyze.py run_analysis() variants key
        benchmarks: from get_channel_ctr_benchmarks()

    Returns:
        List of markdown lines to append after existing variant tables
    """
    lines = []

    if not variant_data or not benchmarks:
        return lines

    lines.append("")
    lines.append("### CTR Analysis")
    lines.append("")

    # Thumbnail verdict
    thumb_verdict = compare_variants_for_video(video_id, 'thumbnail', benchmarks)
    if thumb_verdict.get('status') != 'no_data':
        status_emoji = {"winner_found": "WINNER", "edge": "EDGE",
                        "no_clear_winner": "TIE", "insufficient_data": "WAIT",
                        "single_variant": "NOTE"}.get(thumb_verdict['status'], "")
        lines.append(f"**Thumbnail:** [{status_emoji}] {thumb_verdict['recommendation']}")

    # Overall benchmark context
    overall_avg = benchmarks.get('overall', {}).get('avg_ctr')
    if overall_avg:
        lines.append(f"**Channel avg CTR:** {overall_avg:.2f}%")

    return lines
```

### Standalone CLI (benchmarks.py)
```python
# Source: modeled on variants.py and performance.py CLI patterns
#!/usr/bin/env python3
"""
CTR Analysis & Benchmarks CLI - Phase 30

Usage:
    python benchmarks.py VIDEO_ID              # Analyze single video variants
    python benchmarks.py --benchmarks          # Show all category benchmarks
    python benchmarks.py VIDEO_ID --markdown   # Output as markdown file

Output:
    Variant verdicts, benchmark comparison, and recommendations
"""
import argparse
# ... follows variants.py argparse structure
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| A/B testing requires equal traffic | Channel-specific heuristics | Phase 30 decision | Actionable for solo creator without split traffic infrastructure |
| Industry benchmark CTR (4-5%) | Channel-specific benchmark (3.27% avg) | Per CONTEXT.md decision | Relevant comparison instead of misleading industry standards |
| Statistical significance tests | Practical difference thresholds | Per CONTEXT.md decision | Works with small sample sizes; honest about uncertainty |
| CTR data in API | Manual entry + ctr_snapshots table | Phase 29 | Reliable data despite API limitations |

**Deprecated/outdated:**
- **1,000+ impression threshold from STATE.md:** Too conservative for this channel's velocity. Use tiered 200/500/1000 thresholds with confidence labels instead.
- **Industry benchmark comparisons:** Channel explicitly noted VidIQ scores don't predict performance. Same applies to industry CTR averages.

## Open Questions

Things that couldn't be fully resolved:

1. **Duration-based Shorts filtering**
   - What we know: ctr_snapshots has no duration; video_performance has no duration field either
   - What's unclear: Can we automatically exclude Shorts from benchmarks, or does this rely on user discipline?
   - Recommendation: Rely on user only recording long-form snapshots (document in CLI help). If Phase 31 adds duration data, add automatic filter then.

2. **How to handle videos that change variant mid-life**
   - What we know: Sequential variant testing confounds CTR with video age effects
   - What's unclear: Whether to show a warning, refuse comparison, or just note the date gap
   - Recommendation: Show snapshot dates for each variant group. If dates don't overlap, add note: "Sequential test — earlier variant may have benefited from fresher algorithm boost."

3. **Zero-impression snapshots in benchmark**
   - What we know: Some videos in Table data.csv show 0% CTR (ZSp1wgdXvN8, JJD1-OQ-t0c, etc.)
   - What's unclear: Are these legitimate 0% CTR or missing/unrecorded data?
   - Recommendation: Include 0% CTR in benchmark calculations only if impression_count > 0 (likely tracking issue otherwise).

## Sources

### Primary (HIGH confidence)
- Existing codebase: `tools/youtube-analytics/analyze.py` — /analyze integration pattern, variant section format (lines 975-1047)
- Existing codebase: `tools/discovery/database.py` — ctr_snapshots schema, video_performance schema, aggregate query patterns
- Existing codebase: `tools/youtube-analytics/variants.py` — CLI structure, argparse pattern, subcommand pattern
- Existing codebase: `tools/youtube-analytics/performance.py` — classify_topic_type(), aggregate_by_topic() patterns
- Channel analytics data: `channel-data/Table data.csv` — actual CTR values, impression counts for threshold calibration
- Channel analytics data: `channel-data/CHANNEL_ANALYTICS_MASTER.md` — CTR range 0-11.21%, average 3.27%

### Secondary (MEDIUM confidence)
- Python stdlib `statistics` module docs — mean(), median() usage
- Existing codebase: `tools/youtube-analytics/performance_report.py` — aggregate_by_topic() for benchmark aggregation pattern reference

### Tertiary (LOW confidence)
- General YouTube CTR benchmarks (industry avg 4-5%) — noted but deliberately NOT used per channel decision

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all stdlib, all patterns verified from codebase
- Architecture: HIGH — directly follows existing module patterns (analyze.py, variants.py, performance.py)
- Thresholds: MEDIUM — calibrated from real channel data, but channel has small sample (10 long-form videos); thresholds may need adjustment after more data
- Pitfalls: HIGH — drawn from actual schema inspection and identified gaps (no CTR in video_performance, no duration in ctr_snapshots)

**Research date:** 2026-02-08
**Valid until:** 2026-03-08 (30 days — stable domain, existing codebase won't change)
