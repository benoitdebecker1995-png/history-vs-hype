# Project Research Summary

**Project:** History vs Hype YouTube Workspace v1.6 Click & Keep
**Domain:** YouTube Content Production Workflow - Analytics Integration & Script Quality
**Researched:** 2026-02-06
**Confidence:** HIGH

## Executive Summary

The v1.6 Click & Keep milestone extends an existing YouTube production system (197 subs, 82K views, 30-35% retention) with three integrated features: thumbnail/title A/B tracking, script pacing analysis, and post-publish feedback loops. Research reveals this is fundamentally an **integration project**, not a greenfield build. The workspace already has analytics fetching (ctr.py, retention.py), database infrastructure (keywords.db with auto-migration), and NLP tools (spaCy, textstat). New features require only two library additions (ImageHash 4.3.2 for thumbnail pattern analysis, textstat upgrade to 0.7.12 for readability metrics) and primarily involve wiring existing components together.

The recommended approach leverages the workspace's established patterns: error dict returns, auto-migrating SQLite schema, lazy imports for optional dependencies, and markdown report outputs. Build order prioritizes database schema extensions first (enables parallel development), then tracking/analysis modules, then feedback integration closing the learning loop. The critical architectural insight: don't build new capabilities, extend existing ones. Thumbnail tracking extends video_performance table and /analyze command. Pacing analysis extends flow.py checker. Feedback integration parses existing POST-PUBLISH-ANALYSIS.md files into queryable database for /script command.

Key risks center on small sample size statistics (197 subs = low impression volume), sequential testing treated as simultaneous A/B (impression sources change over video lifecycle), and pacing metrics disconnected from retention reality. Mitigation: enforce 1,000+ impression minimums before declaring winners, track impression source distribution, validate pacing warnings against actual retention drops post-publish. The channel's low volume (1-2 videos/month) makes this a **learning-per-video** optimization challenge, not a high-throughput automation problem. Design for data collection quality over speed.

## Key Findings

### Recommended Stack

The existing stack handles 95% of requirements. Only two additions needed: ImageHash 4.3.2 for thumbnail pattern analysis and textstat 0.7.12 upgrade for enhanced readability metrics. The workspace already has Python 3.11-3.13, SQLite with video_performance table (Phase 19), YouTube Analytics API integration (ctr.py, retention.py), spaCy 3.8+ for NLP, and production pipeline (parser.py with --package flag). Phase 13.1 model assignments need refresh from Claude 3.5 names (haiku/sonnet/opus) to current 4.x lineup (claude-haiku-4-5, claude-sonnet-4-5, claude-opus-4-6).

**Core technologies:**
- **ImageHash 4.3.2**: Perceptual hash generation for thumbnail pattern clustering — enables pattern extraction (map vs face, text vs image) without computer vision APIs or manual tagging. Pure Python, uses existing Pillow dependency.
- **textstat 0.7.12 (upgrade from 0.7.3)**: Readability and sentence complexity metrics — adds quantitative pacing detection (Flesch-Kincaid, sentence variance) beyond spaCy's qualitative flow checking.
- **SQLite (existing)**: Database extensions via auto-migration pattern — thumbnail_variants table, feedback columns in video_performance. Zero breaking changes.
- **spaCy 3.8+ (existing)**: Sentence parsing, entity recognition, NER — foundation for pacing analysis (entity density, sentence variance).
- **YouTube Analytics API v2 (existing)**: CTR, retention, impression sources — note CTR requires manual entry (not available via API).

**What NOT to add:**
- Computer vision APIs (Google Vision, AWS Rekognition) — ImageHash perceptual hashing sufficient
- NLTK — redundant with spaCy, adds 1.5GB
- Hugging Face Transformers — overkill for readability metrics, 500MB+ models
- pandas — SQLite handles analytics aggregation
- Separate A/B testing frameworks — YouTube doesn't offer true simultaneous A/B, sequential testing uses simple timestamp tracking

### Expected Features

Research confirms three feature domains with clear table stakes vs differentiator boundaries. The channel's context (solo creator, 1-2 videos/month, 197 subs) drives requirements toward **data tracking + pattern recognition**, not enterprise automation.

**Must have (table stakes):**
- **Manual CTR Entry UI** — CTR not available via API, 10-second prompt per video
- **Thumbnail Variant Storage** — file paths + manual pattern tags (map/face/text/document)
- **Title Variant Tracking** — log variants with timestamps for test window comparison
- **Sentence Length Variance** — detect rushed delivery in dense script segments (>15 std dev)
- **Readability Delta Detection** — flag complexity spikes between sections (>10 point Flesch drops)
- **POST-PUBLISH-ANALYSIS Parser** — extract CTR, retention drops, SEO issues from markdown to database

**Should have (competitive):**
- **Statistical Significance Calculator** — know when CTR difference is real vs noise (prevents false positives)
- **Channel-Specific CTR Benchmarks** — compare to territorial dispute average, not generic YouTube
- **Entity Density Heatmap** — detect "wall of nouns" syndrome (>25% proper nouns per paragraph)
- **Complexity Score Per Section** — combine variance + readability + entity density → 0-100 score
- **Pre-Creation Insight Lookup** — query similar topics before script generation, surface past retention warnings

**Defer (v2.0 — insufficient training data):**
- **Retention Heatmap Prediction** — requires 30+ videos with retention data (currently ~15)
- **Thumbnail Visual Pattern Analysis (ImageHash clustering)** — requires 20+ tracked thumbnails
- **Topic Success Probability Estimator** — requires 20+ videos for meaningful predictions
- **Hook Strength Scorer** — needs retention correlation data

**Anti-features (deliberately avoid):**
- Real-time CTR dashboard — creates anxiety without actionable insights for low-volume channel
- AI auto-generated thumbnails — defeats evidence-based strategy (maps/documents)
- Automated title optimization — risks clickbait that violates documentary tone
- Browser automation for YouTube Studio — high maintenance, account risk, not a bottleneck

### Architecture Approach

v1.6 extends existing architecture through data layer additions and component integration, not refactoring. The workspace follows established patterns: error dict returns (graceful degradation), CLI + Python API dual interface (supports /commands and direct imports), auto-migration schema (zero manual SQL), lazy loading for optional dependencies (tools work without full stack), and markdown report outputs (human-readable, version-controllable, Claude-parseable).

**Major components:**

1. **Database Extensions** — Add thumbnail_variants table and feedback columns to video_performance via auto-migration pattern (_ensure_thumbnail_table, _ensure_feedback_columns). Enables parallel development of trackers and feedback modules.

2. **Thumbnail Tracking** — New thumbnail_tracker.py computes ImageHash perceptual hashes (average, perceptual, difference), stores with CTR metrics. New thumbnail_patterns.py clusters similar thumbnails via Hamming distance, correlates with CTR. Integrates with existing /analyze command.

3. **Pacing Analysis** — New checkers/pacing.py extends script-checkers with quantitative metrics (sentence variance per 100-word window, Flesch delta between sections, entity density per paragraph). Integrates with existing cli.py and flow.py checker orchestration.

4. **Feedback Loop** — New feedback_loader.py parses POST-PUBLISH-ANALYSIS markdown files, extracts CTR/retention/discovery data, stores in video_performance table. /script command queries feedback before generation to surface relevant lessons automatically.

5. **Model Assignment Refresh** — Update YAML frontmatter in 13 .claude/commands/*.md files from Phase 13.1 names (haiku/sonnet/opus) to current IDs (claude-haiku-4-5, claude-sonnet-4-5, claude-opus-4-6).

**Data flow integration:**
```
Creation → Script (queries past feedback) → Pacing check → Filming
         → Thumbnails A/B/C → Track variants → Hash computation

Publishing → /analyze → POST-PUBLISH-ANALYSIS.md → feedback_loader.py
          → Database storage → Pattern extraction → /patterns report

Next video → /script queries feedback → Lessons applied automatically
```

### Critical Pitfalls

Five critical pitfalls emerged from research, all solvable with design decisions in implementation:

1. **Small Sample Size Fallacy (A/B Testing)** — Testing with too few impressions leads to false positives. Even at 95% confidence, 26.4% chance of being wrong with small samples. Channel has 197 subs = naturally low impression volume. **Prevention:** Require 1,000+ impressions per variant before declaring winner. Run tests 7-14 days minimum. Require 2+ percentage point CTR difference (effect size), not just statistical significance. Validate patterns across 3+ tests before updating guidelines.

2. **Sequential Testing Treated as Simultaneous A/B** — Creator publishes with thumbnail A (Day 1-2), swaps to B (Day 3-4), compares CTR directly. But impression sources change over video lifecycle (subscribers → browse → suggested), creating apples-to-oranges comparison. **Prevention:** Track impression source distribution (Browse, Search, Subscriptions, Playlist via YouTube API). Normalize CTR by source or use extended test windows (7+ days per variant for full lifecycle).

3. **Pacing Analysis Detects Symptoms, Not Causes** — Checker flags "sentence variance 18.3 at lines 45-52" without explaining WHY or HOW to fix. Creator gets list of warnings without guidance. **Prevention:** Contextual warnings explaining root cause ("3 short sentences followed by 1 long sentence → rushed setup + dense explanation. Consider: break dense segment with transition"). Severity scoring (variance 16 vs 25). Actionable fix suggestions.

4. **Dead-End Insights (Feedback Loop Integration)** — /analyze generates POST-PUBLISH-ANALYSIS.md with valuable lessons ("drop at 3:15 due to pacing"), file saved, never referenced again. Next video repeats same mistake. **Prevention:** Parse markdown → database (feedback_loader.py). Query during /script generation automatically. Surface: "Similar videos had pacing drop at 3min — review structure." Close the learning loop.

5. **Pacing Metrics Disconnected from Retention Reality** — Script checker flags complexity spike at 3:15, but actual retention drop happens at 5:20 (caused by boring B-roll, not script). Tool credibility damaged. **Prevention:** Post-publish validation loop comparing pacing warnings to actual retention drops. Calibrate thresholds based on hit rate (if Flesch delta >20 predicts drop 70% of time, keep threshold; if 30%, raise to 30). Conservative warnings (flag HIGH confidence issues only).

## Implications for Roadmap

Based on research, suggested 5-phase structure optimizes for learning-per-video (not throughput) and closes feedback loop early:

### Phase 1: Database Foundation (Week 1)
**Rationale:** Database schema extensions enable parallel development of all tracking/analysis modules. Following established auto-migration pattern from v1.3-v1.5 means zero breaking changes to existing tools.

**Delivers:**
- thumbnail_variants table with perceptual hash storage
- Feedback columns in video_performance table (retention_drop_points, discovery_issues, lessons as JSON)
- Auto-migration methods (_ensure_thumbnail_table, _ensure_feedback_columns)

**Addresses:** Foundation for A/B tracking (FEATURES.md: thumbnail variant storage) and feedback loop (FEATURES.md: POST-PUBLISH-ANALYSIS parser)

**Avoids:** Breaking Existing Database Schema pitfall (PITFALLS.md Anti-Patterns) — uses nullable columns, no NOT NULL constraints

**Research flag:** SKIP RESEARCH-PHASE — SQLite schema extension well-documented, auto-migration pattern proven in v1.3-v1.5

---

### Phase 2A: Thumbnail Tracking (Week 2 - Parallel)
**Rationale:** With database ready, thumbnail tracking can develop independently. ImageHash library mature (4.3.2 stable, 20M+ PyPI downloads). Integration point with existing /analyze command is clean extension.

**Delivers:**
- thumbnail_tracker.py computing perceptual hashes (average, perceptual, difference)
- Manual CTR entry UI (CLI prompt, 10 seconds per video)
- Storage in thumbnail_variants table with test window snapshots (48h, 7d, 14d)

**Uses:** ImageHash 4.3.2 (STACK.md: perceptual hashing), Pillow 12.0+ (existing), SQLite (STACK.md: existing infrastructure)

**Implements:** Data collection foundation (FEATURES.md: table stakes features)

**Avoids:**
- Small Sample Size Fallacy (PITFALLS.md #1) — enforces 1,000+ impression minimum via validation
- Thumbnail Naming Chaos (PITFALLS.md #8) — validates THUMBNAIL-[A/B/C].png naming convention

**Research flag:** SKIP RESEARCH-PHASE — ImageHash documentation comprehensive, pattern clustering well-established technique

---

### Phase 2B: Pacing Analysis (Week 2 - Parallel)
**Rationale:** Independent of database changes, extends existing script-checkers. textstat already in requirements.txt (upgrade to 0.7.12), spaCy 3.8+ operational. Integration with cli.py follows established checker pattern.

**Delivers:**
- checkers/pacing.py with sentence variance, Flesch delta, entity density metrics
- Contextual warnings with root cause explanations (not just numbers)
- --pacing flag in cli.py for optional execution
- Config thresholds (variance >15, Flesch delta >20, entity density >0.4)

**Uses:** textstat 0.7.12 (STACK.md: readability metrics), spaCy 3.8+ (STACK.md: existing NLP), established checker orchestration pattern

**Implements:** Script pacing analysis foundation (FEATURES.md: table stakes quantitative metrics)

**Avoids:**
- Pacing Symptoms Not Causes (PITFALLS.md #3) — contextual warnings, severity scoring, actionable suggestions
- Pacing False Negatives (PITFALLS.md #11) — acknowledges limitations, doesn't oversell capability

**Research flag:** SKIP RESEARCH-PHASE — textstat + spaCy metrics straightforward, established threshold research available

---

### Phase 3: Thumbnail Pattern Analysis (Week 3)
**Rationale:** Requires Phase 2A complete (need tracked thumbnails with CTR data). Hamming distance clustering is computationally simple but requires validation strategy to avoid hash collision pitfall.

**Delivers:**
- thumbnail_patterns.py clustering visually similar thumbnails
- CTR correlation: "Map-focused thumbnails (7 videos) avg 8.2% CTR"
- Integration with /patterns command for cross-video insights
- Statistical significance calculator (prevents false positives)

**Uses:** ImageHash (STACK.md: perceptual hashing), SQLite GROUP BY queries (STACK.md: analytics aggregation)

**Implements:** Pattern recognition layer (FEATURES.md: differentiator features — channel-specific benchmarks)

**Avoids:**
- Perceptual Hash Collision (PITFALLS.md #5) — multi-hash strategy (2/3 agree), manual validation first 10 videos
- Over-Indexing on Outliers (PITFALLS.md #6) — requires N≥3 for pattern, reports mean + std dev + confidence intervals

**Research flag:** LIGHT RESEARCH — Hamming distance threshold tuning may need experimentation (start at <8, adjust based on validation)

---

### Phase 4: Feedback Loop Integration (Week 3-4)
**Rationale:** Database columns ready (Phase 1), analysis files exist. Pure integration work — parse markdown, store structured data, query during production. Closes learning loop: analyze → learn → apply → create.

**Delivers:**
- feedback_loader.py parsing POST-PUBLISH-ANALYSIS markdown to database
- Pre-creation insight lookup in /script command
- Success pattern extraction (identify top 20% videos, extract common features)
- Automated prompting: "Similar videos had pacing drop at 3:15 — review structure"

**Uses:** Markdown parsing (Python stdlib), SQLite queries (STACK.md: video_performance table exists), existing /script command

**Implements:** Feedback loop closure (FEATURES.md: differentiator — automated insight prompting)

**Avoids:**
- Dead-End Insights (PITFALLS.md #4) — parses markdown to queryable database, surfaces automatically
- Feedback Loader Brittleness (PITFALLS.md #10) — flexible regex parsing, graceful fallbacks, validation logging

**Research flag:** SKIP RESEARCH-PHASE — Markdown parsing straightforward, POST-PUBLISH-ANALYSIS.md format known

---

### Phase 5: Model Assignment Refresh (Week 4)
**Rationale:** Independent of other phases. Phase 13.1 used Claude 3.5 names (haiku/sonnet/opus), Anthropic released 4.x lineup. Simple YAML frontmatter updates in 13 command files.

**Delivers:**
- 6 Haiku files updated: status.md, help.md, fix.md, sources.md, prep.md, discover.md
- 6 Sonnet files updated: verify.md, publish.md, engage.md, analyze.md, patterns.md, research.md
- 1 Opus file updated: script.md
- Model IDs: claude-haiku-4-5, claude-sonnet-4-5, claude-opus-4-6

**Uses:** STACK.md model ID mapping (verified via Anthropic announcements)

**Avoids:** Model Assignment Mismatch (PITFALLS.md #9) — explicit model IDs, not tier aliases

**Research flag:** SKIP RESEARCH-PHASE — Model IDs verified, straightforward find-replace

---

### Phase Ordering Rationale

- **Database first (Phase 1)** enables parallel development of tracking (2A) and pacing (2B), minimizing critical path
- **Parallel Phase 2A/2B** maximizes development velocity, no dependencies between thumbnail tracking and script analysis
- **Pattern analysis after tracking (Phase 3)** requires data collection period, can't extract patterns without CTR data
- **Feedback loop mid-build (Phase 4)** closes learning loop ASAP, enables insight collection during later phase execution
- **Model refresh last (Phase 5)** has no dependencies, can run anytime, placed at end for flexibility

**Dependency graph:**
```
Phase 1 (Database) → Phase 2A (Thumbnail Tracking) → Phase 3 (Pattern Analysis)
                  → Phase 2B (Pacing Analysis) ───────┐
                  → Phase 4 (Feedback Loop) ──────────┤ (no blocking dependencies)
Phase 5 (Model Refresh) ────────────────────────────┘
```

**Integration testing (Week 4)** runs cross-component scenarios:
- New video workflow: Create script → pacing check → film → publish → track thumbnails → analyze CTR
- Feedback loop: Analyze video → parse feedback → create new script → verify lessons applied
- Pattern extraction: /patterns shows thumbnail + script patterns together

### Research Flags

**Phases needing deeper research during planning:**
- **Phase 3 (Thumbnail Pattern Analysis):** Hamming distance threshold tuning requires experimentation. Start conservative (<8), validate against manual tags first 10 videos, adjust based on cluster quality. May need 5-7 test cycles to stabilize threshold.

**Phases with standard patterns (skip research-phase):**
- **Phase 1 (Database Foundation):** SQLite schema extension well-documented, auto-migration pattern proven in v1.3-v1.5
- **Phase 2A (Thumbnail Tracking):** ImageHash library mature, perceptual hashing established technique
- **Phase 2B (Pacing Analysis):** textstat + spaCy metrics straightforward, thresholds from education research
- **Phase 4 (Feedback Loop):** Markdown parsing standard, POST-PUBLISH-ANALYSIS format known
- **Phase 5 (Model Refresh):** YAML frontmatter find-replace, model IDs verified

**Phase-specific validation requirements:**
- **Phase 2A:** Require 1,000+ impressions before declaring A/B winner (small sample size mitigation)
- **Phase 2B:** Validate pacing warnings against post-publish retention drops (calibrate thresholds)
- **Phase 3:** Manual validation of perceptual hash clusters (first 10 videos confirm clustering quality)
- **Phase 4:** Flexible markdown parsing (handle format variations gracefully)

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | **HIGH** | 95% of requirements met by existing stack. Two additions (ImageHash, textstat upgrade) are mature libraries with 20M+ downloads. Versions verified via PyPI 2026-02-06. |
| Features | **HIGH** | YouTube ecosystem 2026 well-researched (Test & Compare rollout confirmed, CTR API limitations documented). Table stakes vs differentiator boundaries clear from channel context (197 subs, 1-2 videos/month). |
| Architecture | **HIGH** | Extends existing patterns (error dict, auto-migration, lazy loading) proven in v1.1-v1.5. Integration points identified in codebase inspection. Zero breaking changes design. |
| Pitfalls | **HIGH** | Critical pitfalls (small sample size, sequential testing, feedback loops) well-documented in A/B testing literature. Prevention strategies proven (sample size validation, impression source tracking). |
| Model IDs | **MEDIUM** | Model IDs verified via Anthropic announcements (Opus 4.6 released Feb 2026), but exact SDK routing patterns unconfirmed. Tier aliases (haiku/sonnet/opus) may work if SDK maintains mappings. |

**Overall confidence:** HIGH

### Gaps to Address

Research revealed three areas requiring validation during implementation:

- **Hamming distance threshold tuning (Phase 3):** Optimal threshold for perceptual hash clustering unknown until tested with channel's thumbnails. Start conservative (<8), validate against manual tags, adjust iteratively. Budget 5-7 test cycles.

- **Pacing metric calibration (Phase 2B):** Sentence variance >15, Flesch delta >20, entity density >0.4 thresholds from education research may not predict retention for this channel's format (10-30 min educational, talking head + B-roll). Validate post-publish by comparing warnings to actual retention drops. Adjust thresholds based on hit rate.

- **Model routing verification (Phase 5):** Model IDs (claude-haiku-4-5, claude-sonnet-4-5, claude-opus-4-6) verified via Anthropic API docs, but exact SDK routing pattern unconfirmed. Test small command (e.g., /help with haiku) before bulk update. If full IDs rejected, check if tier aliases (haiku/sonnet/opus) maintained by SDK.

**Handling strategy:**
- **Threshold tuning:** Implement conservative defaults, add config override flags, log metrics to enable adjustment without code changes
- **Post-publish validation:** Build feedback loop (Phase 4) to automatically validate pacing warnings against retention drops, surface calibration recommendations
- **Model ID testing:** Verify with single command update before bulk changes, document routing pattern for future updates

## Sources

### Primary (HIGH confidence)

**Library Versions & Documentation:**
- [google-api-python-client 2.189.0 on PyPI](https://pypi.org/project/google-api-python-client/) — Released 2026-02-03
- [ImageHash 4.3.2 on PyPI](https://pypi.org/project/ImageHash/) — Perceptual hashing, 20M+ downloads
- [textstat 0.7.12 on PyPI](https://pypi.org/project/textstat/) — Readability metrics
- [spaCy 3.8.11 on PyPI](https://pypi.org/project/spacy/) — NLP toolkit
- [GitHub - JohannesBuchner/imagehash](https://github.com/JohannesBuchner/imagehash) — Perceptual hashing documentation

**YouTube Ecosystem 2026:**
- [YouTube Title A/B Testing Rolls Out Globally](https://www.searchenginejournal.com/youtube-title-a-b-testing-rolls-out-globally-to-creators/562571/) — Test & Compare native feature
- [YouTube Analytics API Documentation](https://developers.google.com/youtube/analytics) — CTR limitations, impression sources
- [YouTube API Python samples](https://github.com/youtube/api-samples/tree/master/python) — Implementation patterns

**Claude Models:**
- [Anthropic launches Claude Opus 4.6](https://www.cnbc.com/2026/02/05/anthropic-claude-opus-4-6-vibe-working.html) — Released Feb 2026
- [Claude Models Overview](https://platform.claude.com/docs/en/about-claude/models/overview) — Model IDs
- [Introducing Claude Haiku 4.5](https://www.anthropic.com/news/claude-haiku-4-5) — Haiku tier

### Secondary (MEDIUM confidence)

**A/B Testing Best Practices:**
- [Statistical Significance in A/B Testing – Complete Guide](https://blog.analytics-toolkit.com/2017/statistical-significance-ab-testing-complete-guide/) — Sample size requirements
- [How to avoid common data accuracy pitfalls in A/B testing](https://www.kameleoon.com/blog/data-accuracy-pitfalls-ab-testing) — Sequential testing issues
- [Four Common Mistakes When A/B Testing](https://towardsdatascience.com/four-common-mistakes-when-a-b-testing-and-how-to-solve-them-384072b57d75/) — Outlier over-indexing

**Script Pacing Research:**
- [How to Skyrocket Your YouTube Retention with the Right Video Script](https://key-g.com/blog/how-to-skyrocket-your-youtube-retention-with-the-right-video-script-a-proven-step-by-step-guide/) — Pacing retention impact
- [YouTube Audience Retention 2026: Benchmarks, Analysis & How to Improve](https://socialrails.com/blog/youtube-audience-retention-complete-guide) — Retention analysis
- [What Is Script Pacing and Why It Matters to You?](https://glcoverage.com/2024/10/25/script-pacing/) — Pacing definitions

**Feedback Loop Integration:**
- [The Ultimate Customer Feedback Loop Guide](https://getthematic.com/insights/customer-feedback-loop-guide) — Loop closure patterns
- [Overcoming challenges in AI feedback loop integration](https://www.glean.com/perspectives/overcoming-challenges-in-ai-feedback-loop-integration) — Integration challenges

### Tertiary (LOW confidence, requires validation)

**Perceptual Hashing:**
- [Duplicate image detection with perceptual hashing](https://benhoyt.com/writings/duplicate-image-detection/) — Hamming distance thresholds (needs validation with channel thumbnails)
- [ImageHash library tutorial](https://pythonhow.com/what/imagehash-library-tutorial/) — Clustering strategies (thresholds require tuning)

**Readability Metrics:**
- Educational research consensus on Flesch-Kincaid thresholds (validated for written text, may need calibration for spoken video scripts)

---
*Research completed: 2026-02-06*
*Ready for roadmap: yes*
