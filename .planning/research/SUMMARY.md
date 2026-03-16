# Project Research Summary

**Project:** History vs Hype — v7.0 Packaging & Hooks Overhaul
**Domain:** YouTube edu/history content packaging — title scoring, hook generation, metadata optimization
**Researched:** 2026-03-16
**Confidence:** HIGH

## Executive Summary

The v7.0 milestone addresses a single root cause disguised as a multi-symptom problem: every tool that scores and generates packaging content is calibrated against this channel's own weak historical performance. The title scorer rates a "B" title against a ~3.5% CTR baseline derived from 48 videos averaging under 100 impressions each. The hook generator draws examples from 83 transcripts from a struggling channel. The metadata pipeline filters out emotional language that actually drives YouTube clicks. The result is a closed feedback loop where technically correct tools reinforce mediocre output because they have never been exposed to what success looks like from outside this channel's data.

The recommended approach is surgical and sequenced: inject external benchmark data first (what do top edu/history channels at 500K-1M subs actually achieve?), then recalibrate existing tools against that anchor, then extend hook and metadata generation to use competitor-derived patterns. This is not a rewrite — it is a recalibration. The architecture is already sound. The existing 5-phase build sequence from ARCHITECTURE.md correctly identifies that zero code should reference benchmark data that does not yet exist. Phase 1 is a research deliverable, not a code deliverable.

The key risk is over-engineering: adding more scoring signals from the same weak internal data source, creating an illusion of analytical precision while the baseline remains wrong. The single highest-leverage action is establishing an external benchmark — what CTR do the top 5 edu/history channels achieve? — and making that the passing threshold. Everything else should extend existing commands rather than add new standalone tools, because the solo creator constraint means every new invocation command reduces adoption of what already works.

---

## Key Findings

### Recommended Stack

The stack is almost entirely in place. With 48K+ LOC of working Python 3.11 tooling, three active SQLite databases (keywords.db v29, intel.db v2, analytics.db), and working integrations with YouTube Analytics API v2, YouTube Data API v3, youtube-transcript-api, and the Anthropic SDK, v7.0 requires exactly one new Python dependency: `Pillow>=10.0.0` added to the `[thumbnails]` extras in pyproject.toml (required by the already-installed imagehash library for thumbnail comparison).

The five new modules v7.0 adds — `competitor_transcripts.py`, `hook_analyzer.py`, `title_benchmark.py`, `thumbnail_analyzer.py`, `metadata_optimizer.py` — all run on the existing installed stack. Claude (via native Claude Code LLM) handles semantic classification tasks that would otherwise require heavy NLP libraries. This keeps the dependency footprint minimal and avoids the spaCy Python 3.14 compatibility debt that already exists as known tech debt.

**Core technologies:**
- `youtube-transcript-api` (existing): Batch-fetch first 90 seconds of competitor transcripts — zero API quota cost
- YouTube Data API v3 `videos.list` (existing, underused): Pull competitor tags and snippet data for ~1,000 already-tracked competitor videos — 1 quota unit per 50 IDs
- Claude Code native LLM (existing): Semantic 4-beat hook parsing and synthesis — established pattern from algo_synthesizer.py
- `textstat` (existing, not yet wired): Readability scoring for titles — two new signals in title_scorer.py with no new dependencies
- `imagehash` + `Pillow` (imagehash existing, Pillow new): Competitor thumbnail clustering against own thumbnails
- `sqlite3` stdlib (existing): All benchmark and metadata aggregation — dataset is under 10K rows, no Pandas needed

### Expected Features

**Must have (table stakes):**
- Title generation grounded in competitor patterns from intel.db — without external reference, the tool re-learns bad habits from own low-CTR data
- Hard-reject enforcement for year (-46% CTR) and colon (-28% CTR) patterns — already in PACKAGING_MANDATE.md but needs tighter tool enforcement
- Hook generation anchored in competitor evidence — Rule 19 4-beat structure is sound but examples are drawn from this struggling channel only
- Metadata description template with keyword-first structure — METADATA-CHECKLIST.md exists as manual reference only; needs tool enforcement
- Title scored against 3%+ CTR external target — current scorer maps own ~2.7% channel average, which rewards mediocrity

**Should have (competitive differentiators):**
- Hook scorer with 4-beat completeness check — automated verification that cold_fact, myth, contradiction, and payoff beats are all present, plus title-fulfillment check in first sentence (addresses the "2% dropout" = 17.1% avg viewer loss in first 10-30 seconds)
- Competitor-anchored title scoring with niche percentile display — advisory context, not a hard gate ("niche median is 5.2% CTR — you are in the bottom third")
- Content-grounded title and thumbnail generation — reads the script for the specific number, document name, and named conflict entities before generating candidates
- Versus title recommender — flags when topic has two named entities and no versus variant has been generated; versus scores ~3.7% CTR (underused)
- Self-referential loop detector — flags when a scoring pattern is based on fewer than N=5 internal examples, forcing fallback to competitor benchmarks
- Hook style recommender by topic type — territorial disputes prefer cold_fact (28.2% avg retention, n=11); ideological myth-busting prefers myth-contradiction (29.3% avg retention, n=2)

**Defer (v2+):**
- Full competitor formula library ingestion: medium complexity, low urgency once external benchmark anchoring is working
- Metadata bundle coherence check (title + thumbnail + description all reference same hook element): useful but manual review is adequate until enough videos are produced under the new system
- Topic-type CTR benchmark segmentation (political vs territorial vs ideological targets): implement as phase 2 once baseline competitor-anchored scoring is working
- A/B thumbnail testing: YouTube's tool requires 10K+ views per video; channel gets 100-500 views; any result is noise

### Architecture Approach

The architecture is an incremental extension of the existing pipeline, not a new system. The v6.0 entry points (/greenlight, /script, /publish, /preflight, /retitle) remain unchanged in invocation; v7.0 adds benchmark context to their output and wires hook_scorer.py into the /script --hooks flag that currently exists but is unimplemented. The critical design principle is that benchmark data is advisory, not a hard gate — the own-channel score remains primary, the niche percentile is additive context. This avoids blocking /greenlight on niche benchmarks when the channel's own measured CTR (3.8% declarative) is already below niche median but is still real measured performance.

**Major components:**
1. `benchmark_store.py` (new) — reads `niche_benchmark.json` and `intel.db niche_title_patterns`; provides `get_niche_baseline(pattern)` with graceful None fallback on missing data
2. `hook_scorer.py` (new) — pure Python heuristics, <50ms; scores hook variants after agent generation so user sees ranked selection; called by /script command, not by the agent (avoids circular feedback loop)
3. `hook_pattern_library.py` (new) — queryable by video type (territorial, ideological, how-why, myth-bust); minimum 50% of examples from channels with 100K+ subscribers
4. `title_scorer.py` (modified) — adds `benchmark=True` param and `benchmark_context` key to score dict; backward-compatible; own-channel score unchanged
5. `intel/refresh.py Phase 11` (modified) — automated monthly competitor title pattern extraction to intel.db niche_title_patterns table
6. `script-writer-v2` Rule 23 (modified) — hook pattern awareness; Rule content lives in HOOK-PATTERN-LIBRARY.md (Tier 2 reference), not inline in the 1,100-line agent prompt; requires audit of Rules 19-22 for consolidation before adding

### Critical Pitfalls

1. **The self-referential scoring loop** — The title scorer's PATTERN_SCORES are derived from the channel's own CTR data where the "A" ceiling is ~3.8% declarative. Top edu/history channels average 6-12% CTR. Prevention: anchor the absolute passing threshold to external niche data; internal measured penalties (colon: -28%, year: -46%) remain valid as relative modifiers but the baseline floor must be externally calibrated. Warning sign: a title scores 78/100 and still gets <2% CTR after publishing.

2. **Hook formula without emotional specificity** — Rule 19's 4-beat structure is sound but the fill instructions produce documentary narration, not click triggers. Prevention: hook generation rules must explicitly distinguish "scrolling stranger who has not yet clicked" from "viewer already watching"; cold_fact beat must be surprising to someone who knows nothing about the topic. The CLICKBAIT_PATTERNS filter in metadata.py must also be audited — it blocks "EXPOSED" wholesale while the active_verbs list in title_scorer.py allows "exposed" in declarative statements.

3. **Improving the scorer without improving the training data** — Adding new scoring dimensions derived from the channel's own 48 videos does not break the self-referential loop; it adds precision to a misaligned baseline. Prevention: before adding any new scoring signal, confirm it comes from external niche data. Budget for v7.0: at most 2-3 new signals total. The 65-point threshold is a policy floor, not a calculated cutoff, and should remain derived from external niche research.

4. **Retention data misapplied to click optimization** — Retention is already strong (30-35%); impressions are the bottleneck. Prevention: label every v7.0 deliverable as either "click-trigger" or "watch-trigger." Hooks optimized for 30-second retention are not the same optimization as hooks that make a stranger click.

5. **Tool count creep** — Every new standalone tool the creator must invoke reduces adoption of existing tools. Prevention: all new packaging features must extend existing commands (/publish flags, /preflight flags) rather than adding new standalone invocation points. If a new scorer exists, it replaces an existing one rather than sitting alongside it.

---

## Implications for Roadmap

Based on research, suggested phase structure:

### Phase 1: External Benchmark Research (Research Deliverable)
**Rationale:** All other phases depend on benchmark data that does not yet exist. Zero code should reference niche_benchmark.json or HOOK-PATTERN-LIBRARY.md before these files are authored. This phase has no code deliverables.
**Delivers:** `channel-data/niche_benchmark.json` (CTR ranges per pattern for top edu/history channels), `channel-data/niche-hook-patterns.md` (raw hook analysis from outlier videos), `.claude/REFERENCE/HOOK-PATTERN-LIBRARY.md` (structured for agent consumption), data freshness check on CTR snapshots (run ctr_tracker.py before any scorer rewrite)
**Addresses:** Competitor-anchored title scoring (prerequisite), hook style recommender (prerequisite), self-referential loop baseline calibration
**Avoids:** Pitfall 1 (self-referential loop), Pitfall 3 (more signals from weak data), Pitfall 5 (confirmation research rather than discovery research)

### Phase 2: Title Scorer Recalibration
**Rationale:** title_scorer.py is the central gate for every packaging touchpoint. Recalibrating its baseline is the highest-leverage single change in v7.0. Commands cannot display benchmark context before score_title() returns it.
**Delivers:** `tools/benchmark_store.py`, modified `title_scorer.py` (benchmark=True param, benchmark_context output), modified `title_ctr_store.py` (get_benchmark_context()), `tools/intel/title_benchmark.py` (pure SQL aggregation on existing intel.db competitor data), textstat readability signals wired into title_scorer.py
**Uses:** sqlite3 stdlib, existing google-api-python-client (videos.list competitor tags enrichment), textstat (already installed)
**Implements:** benchmark_store.py with graceful None fallback; backward-compatible score_title() signature
**Avoids:** Pitfall 1 (self-referential loop broken), Pitfall 3 (external signals only), Pitfall 9 (data freshness check before rewrite)

### Phase 3: Command Integration — Scoring Display
**Rationale:** Commands cannot show benchmark context before Phase 2 produces it. This phase makes the recalibrated scorer visible at every packaging touchpoint without changing any verdict logic.
**Delivers:** Modified `/greenlight` (niche percentile in title scoring block), modified `/publish` Gate 1 (benchmark gap advisory), modified `synthesis_engine.py` (benchmark context per variant in METADATA-SYNTHESIS.md)
**Addresses:** Title scored against external target (visible), niche percentile display, self-referential loop detector (visible in command output)
**Avoids:** Pitfall 1 (benchmark visible = loop detectable), Pitfall 10 (no new standalone tools — extends existing commands)

### Phase 4: Hook Generation Upgrade
**Rationale:** Independent of Phases 2-3. Can start after Phase 1 delivers HOOK-PATTERN-LIBRARY.md. Must audit Rules 19-22 before adding Rule 23 to avoid prompt bloat (prior v3.0 consolidation reduced agent from 1,284 to 788 lines).
**Delivers:** `tools/hook_scorer.py`, `tools/hook_pattern_library.py`, modified `script-writer-v2.md` Rule 23, updated `OPENING-HOOK-TEMPLATES.md` with niche-grounded examples, wired `/script --hooks` flag (currently exists but unimplemented), intel.db v2→v3 migration (competitor_hooks table), `tools/intel/competitor_transcripts.py`, `tools/intel/hook_analyzer.py`
**Uses:** youtube-transcript-api (existing), Claude Code native LLM for 4-beat parsing (existing), existing PRAGMA user_version migration pattern
**Addresses:** Hook quality scorer with 4-beat completeness check, hook style recommender by topic type, hook generation grounded in competitor evidence (50%+ from 100K+ sub channels)
**Avoids:** Pitfall 2 (emotional specificity in fill instructions — "scrolling stranger" criterion added), Pitfall 6 (academic-voice tension), Pitfall 7 (retention data does not drive hook generation)

### Phase 5: Intelligence Refresh Automation
**Rationale:** Automation layer last. Manual JSON baseline works during earlier phases. This phase prevents benchmark data from becoming stale.
**Delivers:** intel.db niche_title_patterns table (schema v3 migration), `refresh.py` Phase 11 (competitor title pattern extraction, ~30 lines), updated `benchmark_store.py` to read intel.db niche_title_patterns, `thumbnail_analyzer.py` (imagehash + Pillow for competitor thumbnail clustering), `metadata_optimizer.py` (top-N tags per topic cluster from competitor videos.list enrichment)
**Uses:** YouTube Data API v3 videos.list (part=snippet,tags for competitor IDs — 1 quota unit per 50 IDs), imagehash + Pillow (Pillow is the only new dependency in the entire milestone)
**Addresses:** Metadata description template enforcement, thumbnail concept generation, automated metadata tag benchmarking, CLICKBAIT_PATTERNS vs active_verbs reconciliation
**Avoids:** Pitfall 4 (clickbait filter reconciled), Pitfall 10 (extend /publish and /preflight, no new standalone invocations)

### Phase Ordering Rationale

- Phase 1 is non-negotiable first because no code in Phases 2-5 should reference data that does not yet exist. niche_benchmark.json and HOOK-PATTERN-LIBRARY.md must be researched and authored, not generated from the same weak internal data.
- Phase 2 before Phase 3 because commands cannot display benchmark_context before score_title() returns it. No circular dependency.
- Phase 4 is independent of Phases 2-3 and can be worked in parallel with Phase 3. The only dependency is Phase 1 (HOOK-PATTERN-LIBRARY.md must exist).
- Phase 5 last because it is the automation layer. The manual JSON baseline from Phase 1 is sufficient for Phases 2-4.
- The "extend, don't add" design rule applies across all phases: new features must extend existing commands rather than add new standalone invocation points.

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 1:** This is the research phase itself. Research questions must be scoped explicitly to click triggers (first 3 words of outlier hooks, emotional trigger vocabulary in highest-impression titles, thumbnail visual element correlation with outlier views). Risk of confirmation bias is HIGH — easy to research what top channels do in their scripts rather than what makes a stranger click.
- **Phase 4, Rule 23 scope:** Requires a pre-build audit of Rules 19-22 in script-writer-v2 for consolidation before adding. If Rules 20-22 can be consolidated, Rule 23 content likely belongs entirely in HOOK-PATTERN-LIBRARY.md as Tier 2 reference rather than inline in the agent prompt.

Phases with standard patterns (skip research-phase):
- **Phase 2:** title_scorer.py modification is well-understood; benchmark_store.py follows the existing kb_store.py and exporter patterns; backward-compatible API extension is standard.
- **Phase 3:** Command display changes are cosmetic integrations of data the scorer already returns. Standard display logic.
- **Phase 5:** intel.db migration follows the established PRAGMA user_version v1→v2 pattern. refresh.py Phase 11 follows the Phase 1-10 pattern. Well-documented throughout.

---

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Full codebase context; one new dependency (Pillow) is standard and version-compatible with Python 3.11-3.13; all other v7.0 work uses installed packages |
| Features | HIGH | Own-channel data n=47 (HIGH), competitor intel.db n=870 (MEDIUM-HIGH), hook-retention correlation n=17 (MEDIUM); small samples flagged per finding; thumbnail data n=4 vs n=4 (LOW — directional only) |
| Architecture | HIGH | Based on full codebase reads of actual source files, not inference; anti-patterns explicitly documented with prior-milestone evidence |
| Pitfalls | HIGH | Grounded in this channel's audited data and prior milestone retrospectives (v3.0 consolidation, v6.0 scoring baseline audit); not generic YouTube advice |

**Overall confidence:** HIGH

### Gaps to Address

- **External benchmark values are not yet researched:** niche_benchmark.json does not exist. The architecture and feature work all reference it, but the actual CTR numbers for top edu/history channels (Kraut, History Matters, Toldinstone, Knowing Better) must be researched and authored in Phase 1. This is the largest gap and the blocker for Phase 2.
- **Hook emotional specificity criteria are not yet defined:** HOOK-PATTERN-LIBRARY.md does not exist. What specifically distinguishes a click trigger from documentary narration needs to be grounded in outlier video analysis. Phase 1 must produce concrete linguistic examples, not structural diagrams.
- **CTR data snapshot freshness:** PACKAGING_MANDATE.md notes all CTR snapshots are from a single collection date (2026-02-23). Run ctr_tracker.py via Task Scheduler and validate data freshness before any v7.0 scorer rewrite. The colon and year penalties (large n) should remain as hard rejects regardless; pattern base scores are the targets for external recalibration.
- **Thumbnail data remains LOW confidence:** n=4 vs n=4 for map vs document thumbnails. Use as directional guidance only until thumbnail_analyzer.py in Phase 5 grows the sample.
- **CLICKBAIT_PATTERNS vs active_verbs inconsistency:** metadata.py filters "EXPOSED" wholesale while title_scorer.py allows "exposed" in declarative statements. Must be reconciled in Phase 5. Recommended resolution: block ALL-CAPS form, allow mixed-case in declarative context.

---

## Sources

### Primary (HIGH confidence)
- Own channel performance data — PACKAGING_MANDATE.md, CROSS-VIDEO-SYNTHESIS.md, HOOK-RETENTION-CORRELATION.md (n=47 videos, audited 2026-03-12)
- Codebase reads — `tools/title_scorer.py`, `tools/title_ctr_store.py`, `script-writer-v2.md`, `OPENING-HOOK-TEMPLATES.md`, `greenlight.md`, `publish.md`, `script.md`, `preflight/scorer.py`, `intel/refresh.py` (2026-03-16)
- intel.db competitor_videos — n=870 competitor videos with title formulas and view counts from RSS pipeline

### Secondary (MEDIUM confidence)
- youtube-intelligence.md competitor landscape — Kraut 604K, Knowing Better 952K, Shaun 760K, Fall of Civilizations 1.5M, Historia Civilis 1.1M top video pattern analysis
- COMPETITOR-TITLE-DATABASE.md — 870-video formula distribution ("other" 55.2%, "how_why" 24.1%, "colon_split" 13.3%)
- YouTube Creator Academy guidance — CTR norms 4-10% for edu/history niche (official source)

### Tertiary (LOW confidence)
- Thumbnail format comparison (n=4 vs n=4 map vs document) — directional only
- Versus pattern CTR (n=2) — directional, consistent with competitor usage but small sample

---
*Research completed: 2026-03-16*
*Ready for roadmap: yes*
