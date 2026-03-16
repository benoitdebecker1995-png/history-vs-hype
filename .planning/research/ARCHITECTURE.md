# Architecture Research: v7.0 Packaging & Hooks Overhaul

**Domain:** Integrating improved hook generation, external-benchmark title scoring, and metadata optimization into existing YouTube content production workspace
**Researched:** 2026-03-16
**Confidence:** HIGH (full codebase context)

---

## Integration Context

**Problem:** The current tooling scores titles and generates hooks against the channel's own low-CTR history. The title_scorer.py baseline scores are calibrated to a ~3.5% average CTR channel. Hook generation (Rule 19) uses a 4-beat formula with youtube-intelligence.md for algorithm context, but the OPENING-HOOK-TEMPLATES.md and script-writer-v2 agent lack grounding in what top edu/history channels actually do in their first 60 seconds. The publish pipeline generates metadata without niche-benchmarked keyword data beyond what VidIQ provides manually.

**Solution (v7.0):** Replace self-referential scoring with external-benchmark scoring. Add a hook pattern library derived from outlier analysis of top-performing channels. Integrate benchmark signals at every packaging touchpoint (/greenlight, /script, /publish).

---

## Current Architecture Map (v6.0 Baseline)

```
ENTRY POINTS
  /greenlight → demand_checker.py + title_scorer.py + thumbnail_checker.py
  /script     → script-writer-v2 (Opus) reads STYLE-GUIDE.md + youtube-intelligence.md
  /publish    → title_scorer.py gate + metadata.py + synthesis_engine.py
  /preflight  → preflight/scorer.py (topic + script + title + duration gates)
  /retitle    → retitle_audit.py + retitle_gen.py + title_scorer.py

SCORING ENGINES
  title_scorer.py
    ├── Static PATTERN_SCORES (calibrated to own channel CTR)
    ├── DB enrichment via title_ctr_store.py → keywords.db
    │     └── ctr_snapshots JOIN video_performance
    └── Hard rejects: year, colon, "The X That Y"

HOOK GENERATION
  script-writer-v2 agent
    ├── Rule 19: 4-beat formula (Cold Fact → Myth → Contradiction → Payoff)
    ├── Rule 20: Retention pattern constraints (from own 46-video analysis)
    ├── .claude/REFERENCE/OPENING-HOOK-TEMPLATES.md (fill-in-the-blank)
    └── youtube-intelligence.md (algorithm mechanics, competitor landscape)

METADATA PIPELINE
  /publish --prompts → prompt_generator.py → EXTERNAL-PROMPTS.md
  /publish --intake  → intake_parser.py → EXTERNAL-INTELLIGENCE.json
  /publish --synthesize → synthesis_engine.py → METADATA-SYNTHESIS.md

INTELLIGENCE LAYER
  tools/intel/
    ├── refresh.py → 10-phase orchestrator (algo + competitors + RSS)
    ├── kb_store.py → intel.db
    ├── kb_exporter.py → channel-data/youtube-intelligence.md
    └── competitor_tracker.py → competitor RSS + YouTube API

DATABASES
  keywords.db (v29)  → title patterns, CTR snapshots, video_performance
  intel.db (v2)      → algorithm KB, competitor data, niche patterns
  analytics.db       → script choices, creator techniques, script edits
```

---

## v7.0 Architecture Additions

### New Components

| Component | Location | Purpose |
|-----------|----------|---------|
| `benchmark_store.py` | `tools/` | External CTR benchmark data store — reads niche outlier data, provides comparison scores |
| `hook_pattern_library.py` | `tools/` | Extracted hook patterns from top edu/history channels, queryable by video type |
| `hook_scorer.py` | `tools/` | Score hook variants against proven patterns (information gap, authority signal, visual carrot density) |
| `HOOK-PATTERN-LIBRARY.md` | `.claude/REFERENCE/` | Human-readable hook pattern catalog consumed by script-writer-v2 |
| `niche_benchmark.json` | `channel-data/` | Researched niche CTR benchmarks (target: 4-7% for edu/history niche) |

### Modified Components

| Component | Change | Why |
|-----------|--------|-----|
| `title_scorer.py` | Add `--benchmark` mode that compares scores against niche averages, not just own history | Own CTR is too low to use as aspirational baseline |
| `title_scorer.py` | Add `benchmark_context` key to score dict with niche percentile | Lets commands show "This scores in the top 30% of edu/history niche" |
| `title_ctr_store.py` | Add `get_benchmark_context(pattern, niche_data)` function | Centralizes benchmark comparison logic |
| `.claude/agents/script-writer-v2.md` | Add Rule 23: Hook Pattern Awareness | Agent reads HOOK-PATTERN-LIBRARY.md for proven patterns from niche outliers |
| `.claude/REFERENCE/OPENING-HOOK-TEMPLATES.md` | Add niche-grounded examples from outlier analysis | Current examples are self-referential; need top-performing channels as evidence |
| `.claude/commands/greenlight.md` | Add benchmark display in title scoring block | Show niche context alongside own-channel score |
| `.claude/commands/publish.md` | Add benchmark context to title scoring gate | Flag when a title underperforms niche avg even if it passes own-channel gate |
| `.claude/commands/script.md` | Add `--hooks` flag processing that calls hook_scorer.py | Currently `--hooks` is listed but not implemented |
| `tools/intel/refresh.py` | Add Phase 11: niche title pattern extraction from tracked competitor recent uploads | Feed benchmark_store with fresh competitor title data |

---

## Data Flow: v7.0 Complete Picture

### Flow A: External Benchmark Ingestion (Run Once, Refresh Monthly)

```
RESEARCH PHASE (manual, done once per milestone)
  Researcher analyzes top edu/history channels
  → Extracts: avg CTR ranges, title patterns, hook structures, metadata patterns
  → Writes to: channel-data/niche_benchmark.json
              channel-data/niche-hook-patterns.md (raw findings)

AUTOMATION LAYER (ongoing, via /intel --refresh)
  tools/intel/refresh.py Phase 11
    ├── Reads: competitor_channels.json (tracked channels)
    ├── Fetches: recent video titles via YouTube Data API
    ├── Classifies: titles by pattern (detect_pattern())
    └── Writes: intel.db → niche_title_patterns table
               (pattern, sample_count, est_avg_ctr_range, last_updated)

benchmark_store.py
  ├── Reads: niche_benchmark.json (researched baselines)
  ├── Reads: intel.db niche_title_patterns (live competitor data)
  └── Provides: get_niche_baseline(pattern) → {low, mid, high, percentile_fn}
```

### Flow B: Hook Generation (Per Script)

```
/script --hooks [project]   OR   /script --variants [project]
    │
    ├── Read: .claude/REFERENCE/OPENING-HOOK-TEMPLATES.md
    ├── Read: .claude/REFERENCE/HOOK-PATTERN-LIBRARY.md  [NEW]
    ├── Read: channel-data/youtube-intelligence.md
    │
    ▼
script-writer-v2 (Rule 19 + Rule 20 + Rule 23 [NEW])
    │
    ├── Generates: 3 hook variants (Cold Fact / Myth-Bust / How-Why)
    │               Each variant: 100-150 words, labeled by type
    │
    ▼
hook_scorer.py  [NEW — called by /script command, not agent]
    ├── Scores each variant on:
    │     - Information gap density (0-10)
    │     - Visual carrot specificity (0-10)
    │     - Authority signal present? (0/5)
    │     - Pattern match vs HOOK-PATTERN-LIBRARY (0-10)
    ├── Returns: ranked variants with scores
    └── Writes: score block displayed to user before they pick

User picks hook → logged to analytics.db script_choices
```

### Flow C: Title Scoring with Benchmark Context (All Commands)

```
score_title(title, db_path=..., benchmark=True)  [MODIFIED]
    │
    ├── Existing logic: detect pattern, apply hard rejects, bonuses/penalties
    ├── DB enrichment: get_pattern_ctr_from_db() → own channel avg
    ├── Benchmark context [NEW]: benchmark_store.get_niche_baseline(pattern)
    │     → {channel_avg: 3.7%, niche_low: 3.5%, niche_mid: 5.2%, niche_high: 8.0%}
    │
    └── Returns extended dict with:
          'score': 75                    (unchanged — own channel calibrated)
          'benchmark_context': {
            'channel_avg_ctr': 3.7,
            'niche_mid_ctr': 5.2,
            'niche_percentile': 35,       # Channel's CTR is at 35th percentile
            'gap_to_niche_mid': +1.5,     # Need +1.5% CTR to match niche median
          }

DISPLAY IN COMMANDS:
  /greenlight:  "Title: 75/B — but niche median is 5.2% CTR. You're in the bottom third."
  /publish:     "Score 75/B (vs niche mid 5.2%). Consider: [stronger pattern suggestion]"
  /preflight:   Benchmark gap adds advisory flag (not a hard block)
```

### Flow D: Metadata Optimization (Post-Script)

```
/publish --prompts [project]
    │
    ├── Existing: load intel.db for competitor context
    ├── NEW: load niche_benchmark.json for description/tag structure patterns
    ├── NEW: include hook pattern examples in VidIQ prompt template
    └── Generates: EXTERNAL-PROMPTS.md with benchmark-informed prompts

/publish --intake [project]
    └── (unchanged — user pastes VidIQ/Gemini responses)

/publish --synthesize [project]
    │
    ├── Existing: 3 variants (keyword, curiosity, authority)
    ├── NEW: benchmark alignment check per variant
    │     → "Variant A uses 'how_why' pattern (own channel: 3.3% avg, niche: 4.8% avg)"
    └── Outputs: METADATA-SYNTHESIS.md with benchmark context per variant
```

---

## Component Boundaries

| Component | Responsibility | Reads From | Writes To |
|-----------|---------------|------------|-----------|
| `benchmark_store.py` | Niche baseline lookups | `niche_benchmark.json`, `intel.db` | (read-only) |
| `hook_pattern_library.py` | Hook pattern queries | `HOOK-PATTERN-LIBRARY.md`, `intel.db` | (read-only) |
| `hook_scorer.py` | Score hook variant text | `HOOK-PATTERN-LIBRARY.md`, hook variant text | Score dict (in-memory) |
| `title_scorer.py` (modified) | Title scoring + benchmark context | `keywords.db`, `niche_benchmark.json` | Score dict (in-memory) |
| `intel/refresh.py` Phase 11 | Extract competitor title patterns | YouTube Data API, `competitor_channels.json` | `intel.db` niche_title_patterns |
| `HOOK-PATTERN-LIBRARY.md` | Reference doc for agent | (authored by researcher) | Read by script-writer-v2 |
| `script-writer-v2` Rule 23 | Apply hook patterns during generation | `HOOK-PATTERN-LIBRARY.md` | Hook variants in script |

---

## Integration Points: New vs Modified

### New Components (Build These)

```
tools/benchmark_store.py
  - Class: BenchmarkStore
  - Methods: get_niche_baseline(pattern), get_all_patterns(), is_stale()
  - Data source: channel-data/niche_benchmark.json + intel.db niche_title_patterns
  - Fallback: Returns None on any error — title_scorer.py shows scores without benchmark context

tools/hook_scorer.py
  - Function: score_hook(hook_text) → dict
  - Checks: information_gap_present, visual_carrot_specificity, authority_signal, pattern_type
  - Returns: {score: int, breakdown: dict, recommendation: str}
  - Used by: /script command (not by agent — agent generates, command scores and presents)

tools/hook_pattern_library.py
  - Function: get_patterns_by_type(video_type) → list[dict]
  - Function: get_top_examples(n=3) → list[dict]
  - Data source: .claude/REFERENCE/HOOK-PATTERN-LIBRARY.md (parsed) or intel.db
  - Used by: hook_scorer.py, /script command display

.claude/REFERENCE/HOOK-PATTERN-LIBRARY.md
  - Format: Categorized examples with channel attribution, view count context, pattern analysis
  - Sections: Territorial, Ideological, How-Why, Myth-Bust (matching script-writer-v2 video types)
  - Populated by: Research phase (v7.0 researcher), updated by /intel --refresh Phase 11

channel-data/niche_benchmark.json
  - Schema: {pattern: {low_ctr, mid_ctr, high_ctr, source, sample_size, last_updated}}
  - Populated by: Research phase (v7.0 researcher)
  - Updated by: /intel --refresh Phase 11 (competitor title pattern extraction)
```

### Modified Components (Touch These)

```
title_scorer.py
  - score_title() signature: add benchmark=False param (backward compatible)
  - Returns: add 'benchmark_context' key (None when benchmark=False or data unavailable)
  - CLI: add --benchmark flag

title_ctr_store.py
  - Add: get_benchmark_context(pattern, benchmark_store) → dict|None
  - Lazy import benchmark_store to avoid circular deps (same pattern as existing lazy imports)

.claude/agents/script-writer-v2.md
  - Add Rule 23: Hook Pattern Awareness
  - Rule reads HOOK-PATTERN-LIBRARY.md (Tier 2 reference, as-needed)
  - Instruction: "When writing hook, consult HOOK-PATTERN-LIBRARY.md for the video type.
    Apply the pattern structure that matches this video's type. Note which pattern used."
  - Size check: Agent is currently ~1,100 lines. Rule 23 + new Tier 2 reference entry = ~15 lines.

.claude/REFERENCE/OPENING-HOOK-TEMPLATES.md
  - Add section: "Niche Outlier Examples" under each video type template
  - Each example attributed to channel + view count + what makes it work
  - No structural change to existing 4-beat formula — examples enrich it

.claude/commands/greenlight.md
  - Title scoring block: add benchmark_context display when available
  - Show: niche percentile + gap-to-median alongside own-channel score
  - No change to verdict logic — benchmark is advisory

.claude/commands/publish.md
  - Gate 1 (title score): add benchmark context display
  - Advisory block: "Niche median for [pattern] is X% CTR — your title is calibrated to Y%"
  - synthesis_engine.py: add benchmark_context per variant to METADATA-SYNTHESIS.md

.claude/commands/script.md
  - --hooks flag: currently listed in flags table but implementation unclear
  - Add processing: after agent generates hook variants, pipe through hook_scorer.py
  - Display scored variants to user before they pick

tools/intel/refresh.py
  - Add Phase 11: title pattern extraction
  - For each competitor in competitor_channels.json: fetch last 20 video titles via YouTube Data API
  - Run detect_pattern() on each
  - Write to intel.db niche_title_patterns table
  - Estimated: ~30 lines, falls back gracefully if API unavailable

intel.db schema
  - Add table: niche_title_patterns
    (pattern TEXT, sample_count INT, last_updated TEXT, source_channels TEXT)
  - Migration: intel.db v2 → v3
  - Use existing PRAGMA user_version pattern
```

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Benchmark as Hard Gate

**What it is:** Blocking /greenlight or /publish because a title scores below the niche median.

**Why bad:** The channel's own CTR data (3.8% declarative) IS below niche median, but it's real performance. Hard-blocking on niche benchmarks would reject titles that would actually work for this channel. Benchmarks show aspiration, not viability.

**Instead:** Display benchmark context as advisory. "Niche median is 5.2% — your title is calibrated to 3.8% avg. Consider if a stronger pattern is available." Hard blocks remain: year, colon, the_x_that.

### Anti-Pattern 2: Hook Scorer Driving Agent Generation

**What it is:** Feeding hook_scorer.py output back into script-writer-v2 as a hard constraint.

**Why bad:** The agent already has Rule 19 (4-beat formula), Rule 20 (retention constraints from 46-video analysis), and HOOK-PATTERN-LIBRARY.md via Rule 23. Adding a scoring feedback loop creates circular generation that inflates token usage and adds latency. The agent generates good hooks — the scorer helps the user pick between them.

**Instead:** hook_scorer.py is called by the /script command after agent generation, not by the agent. The output is a selection aid for the user, not a regeneration trigger.

### Anti-Pattern 3: New Title Scoring Scale

**What it is:** Recalibrating the 0-100 title score to reflect niche benchmarks instead of own-channel history.

**Why bad:** The existing scale (`score = min(100, max(0, int(ctr_percent * 17)))`) calibrates to own channel data, which commands depend on. Changing the scale breaks every existing reference to "score 65+ = go" across greenlight.md, publish.md, preflight/scorer.py.

**Instead:** Benchmark context is a parallel display, not a replacement score. Own-channel score remains primary; benchmark is additive context.

### Anti-Pattern 4: Agent Rule Accumulation Without Audit

**What it is:** Adding Rule 23 without checking current agent size and whether existing rules can be consolidated.

**Why bad:** script-writer-v2 has 22+ rules. The PITFALLS.md from v3.0 identified prompt bloat as the top risk. Past intervention: v3.0 consolidated agent from 1,284 to 788 lines with a 43.6% reduction.

**Instead:** Before adding Rule 23, audit Rules 19-22 for consolidation opportunities. Rule 23 content (hook patterns from niche) is mostly reference material that belongs in HOOK-PATTERN-LIBRARY.md (which the agent reads), not inline in the agent prompt.

---

## Suggested Build Order

Dependencies drive this order. Each phase produces artifacts consumed by the next.

```
Phase 1: Research Foundation (no code)
  ├── Research top edu/history channels (hook patterns, title patterns, CTR ranges)
  ├── Create channel-data/niche_benchmark.json
  ├── Create channel-data/niche-hook-patterns.md (raw research findings)
  ├── Create .claude/REFERENCE/HOOK-PATTERN-LIBRARY.md (structured for agent use)
  └── DEPENDS ON: nothing — pure research
  PRODUCES: benchmark data and hook library that all other phases consume

Phase 2: Title Scorer Upgrade (touches title_scorer.py)
  ├── Create tools/benchmark_store.py (reads niche_benchmark.json)
  ├── Modify title_scorer.py: add benchmark=True param + benchmark_context output
  ├── Modify title_ctr_store.py: add get_benchmark_context()
  └── DEPENDS ON: Phase 1 (niche_benchmark.json must exist)
  PRODUCES: title_scorer.py that surfaces niche context alongside own-channel score

Phase 3: Command Integration — Scoring (touches greenlight.md, publish.md)
  ├── Modify /greenlight: display benchmark_context in title scoring block
  ├── Modify /publish: display benchmark context in Gate 1
  ├── Modify synthesis_engine.py: add benchmark context per variant
  └── DEPENDS ON: Phase 2 (benchmark_context key in score dict)
  PRODUCES: all packaging commands show niche context

Phase 4: Hook Generation Upgrade (touches script-writer-v2, OPENING-HOOK-TEMPLATES.md)
  ├── Audit Rules 19-22 for consolidation before adding Rule 23
  ├── Add Rule 23 to script-writer-v2.md (reads HOOK-PATTERN-LIBRARY.md)
  ├── Update OPENING-HOOK-TEMPLATES.md with niche-grounded examples
  ├── Create tools/hook_scorer.py
  ├── Create tools/hook_pattern_library.py
  ├── Modify /script command: add hook_scorer.py call after --hooks/--variants generation
  └── DEPENDS ON: Phase 1 (HOOK-PATTERN-LIBRARY.md must exist)
  PRODUCES: hooks scored against niche patterns, user sees ranked variants

Phase 5: Intelligence Refresh Integration (touches intel/refresh.py, intel.db)
  ├── Add intel.db niche_title_patterns table (schema v3 migration)
  ├── Add refresh.py Phase 11: competitor title pattern extraction
  ├── Update benchmark_store.py to also read intel.db niche_title_patterns
  └── DEPENDS ON: Phase 2 (benchmark_store.py must exist to update it)
  PRODUCES: automated monthly refresh of niche title pattern benchmarks
```

**Phase ordering rationale:**
- Phase 1 must precede all others — zero code can reference data that doesn't exist yet
- Phase 2 before Phase 3 — commands can't display benchmark_context before score_title() returns it
- Phase 4 is independent of Phases 2-3 — hook improvements don't require title benchmark work
- Phase 5 last — automation layer. Manual JSON baseline works during earlier phases

---

## Integration Points Summary

| Touchpoint | What Changes | Who Calls It |
|------------|-------------|--------------|
| `score_title()` | Returns `benchmark_context` dict | /greenlight, /publish, /preflight |
| `/greenlight` display | Shows niche percentile | User entry point |
| `/publish` Gate 1 | Shows benchmark gap advisory | User entry point |
| `script-writer-v2` Rule 23 | Reads HOOK-PATTERN-LIBRARY.md | /script command |
| `/script --hooks` | Pipes variants through hook_scorer.py | User entry point |
| `/intel --refresh` | Runs Phase 11 title extraction | Automated (Task Scheduler) |
| `intel.db` | Adds niche_title_patterns table | benchmark_store.py |

---

## Scalability Considerations

| Concern | Current State | v7.0 Change | Risk |
|---------|--------------|-------------|------|
| `benchmark_store.py` on missing data | — | Returns None, graceful degradation | LOW — existing fallback pattern |
| Agent prompt size | ~1,100 lines (post v6.0 consolidation) | +~15 lines for Rule 23 | LOW — well within budget |
| `hook_scorer.py` latency | — | Pure Python regex/heuristics, <50ms | NONE |
| intel.db migration v2→v3 | v2 stable | Add one table, PRAGMA user_version | LOW — existing pattern |
| niche_benchmark.json staleness | — | Monthly refresh via Phase 11 or manual update | MEDIUM — data drift if not refreshed |

---

## Sources

- Codebase read: `tools/title_scorer.py`, `tools/title_ctr_store.py` (actual code, 2026-03-16)
- Codebase read: `.claude/agents/script-writer-v2.md` Rules 19-22 (actual prompt, 2026-03-16)
- Codebase read: `.claude/REFERENCE/OPENING-HOOK-TEMPLATES.md` (actual reference doc, 2026-03-16)
- Codebase read: `.claude/commands/greenlight.md`, `publish.md`, `script.md` (actual commands, 2026-03-16)
- Codebase read: `tools/preflight/scorer.py`, `tools/intel/refresh.py` (actual code, 2026-03-16)
- Prior research: `.planning/research/ARCHITECTURE.md` v3.0 (2026-02-12) — integration patterns
- Project context: `.planning/PROJECT.md` — validated decisions, known tech debt
- Data from codebase: keywords.db v29, intel.db v2, analytics.db schema patterns

---

*Researched: 2026-03-16 for v7.0 Packaging & Hooks Overhaul milestone*
