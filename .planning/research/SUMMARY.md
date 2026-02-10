# Project Research Summary

**Project:** v2.0 Channel Intelligence for History vs Hype YouTube Channel
**Domain:** AI-assisted YouTube content production with channel-aware capabilities
**Researched:** 2026-02-09
**Confidence:** HIGH

## Executive Summary

v2.0 transforms generic AI tools into channel-aware intelligence by adding three capabilities to an existing 17,300 LOC Python system: (1) script generation that matches creator voice patterns, (2) research workflow integration with NotebookLM, and (3) actionable analytics that provide concrete fixes, not just data. The key insight from research: most failures come from building MORE features when the problem is making EXISTING features produce output that matches creator needs.

The recommended approach is reference-document expansion over code proliferation. Voice pattern enforcement requires NO new code — only expanding STYLE-GUIDE.md Part 6 with voice patterns from high-performing transcripts (Belize: 23K views, Vance: 42.6% retention). The script-writer-v2 agent already reads this reference; enhancement happens through better documentation, not tool rewrites. NotebookLM integration must embrace manual workflow reality (no API exists) — build format converters and source recommenders, not brittle automation. Analytics need diagnostic messages with root causes ("retention dropped due to 45-second static map during legal explanation — add pattern interrupt") instead of raw metrics ("retention dropped 15% at 3:42").

The primary risk is Empty Patterns Syndrome: extracting voice patterns from <5 videos produces statistical noise, not signal. With only ~15 published videos, pattern confidence will be LOW-MEDIUM across all features. Mitigation: explicit confidence warnings, graceful degradation (hybrid manual+corpus patterns), and minimum corpus validation before extraction. The second risk is building features that don't get used (project context shows "tools exist but output doesn't match what creator needs"). Prevention: ship MINIMUM features solving ONE pain point completely, validate usage before building next phase, enforce complexity budget (max 20 commands, 10 agents, 25K LOC).

## Key Findings

### Recommended Stack

Core requirement: enhance existing Python 3.x stack (~17,300 LOC) with channel intelligence libraries. CRITICAL BLOCKER IDENTIFIED: Python 3.14.2 is incompatible with spaCy (no wheels available as of 2026-02-09). Downgrade to Python 3.13.x is MANDATORY before v2.0 development starts.

**Core technologies (NEW for v2.0):**
- **anthropic SDK** (>=1.87.1): Claude Opus 4.6 API integration for channel-aware script generation — official Python SDK with async/sync interfaces, streaming support
- **sentence-transformers** (>=3.1.0): Semantic similarity and text embeddings for voice pattern matching, finding similar past videos — industry standard with 15K+ models, runs locally (no API costs)
- **chromadb** (>=0.5.29): Local vector database for research embeddings, script patterns, performance data — lightweight DuckDB backend, <10ms query latency for 1K vectors
- **markitdown** (>=0.0.1a2): Document-to-markdown conversion for NotebookLM source extraction — Microsoft's LLM-focused converter, handles PDF/DOCX/PPTX

**Supporting libraries:**
- **jinja2** (>=3.1.5): Prompt template management for dynamic Claude API prompts
- **tiktoken** (>=0.8.0): Token counting to prevent 200K context window overflow
- **faststylometry** (>=0.1.0): Text style fingerprinting for voice pattern comparison (blocked by spaCy 3.14 incompatibility)
- **pydantic** (>=2.10.4): Data validation for API responses

**CRITICAL PATH:** Python version downgrade (3.14 → 3.13) must complete BEFORE installing v2.0 dependencies. Total new code estimate: ~950 lines (5% of existing codebase). Total disk space: ~600MB (sentence-transformers model: 420MB, other libraries: 180MB).

### Expected Features

Research reveals feature landscape divided into three tiers: table stakes (users expect), differentiators (competitive advantage), and anti-features (commonly requested but problematic).

**Must have (table stakes):**
- Script generation from verified research (EXISTS but needs voice pattern integration)
- Analytics data access (EXISTS via /analyze)
- Source citation tracking (EXISTS in VERIFIED-RESEARCH.md)
- Retention drop detection (EXISTS via retention.py)
- Quality checkers (EXISTS: stumble, flow, scaffolding)

**Should have (differentiators):**
- **Voice pattern library** — Scripts match creator's proven voice (Belize 23K views, Vance 42.6% retention), not generic AI. Patterns documented in STYLE-GUIDE.md, enforced by script-writer-v2 agent. HIGH value, MEDIUM complexity.
- **Academic source preparation for NotebookLM** — Bridge from "need sources for topic" to "here are 10 university press books ready for upload." Addresses research bottleneck (2-4 hours identifying sources). MEDIUM complexity.
- **NotebookLM extraction prompts** — Structured chat templates that extract verified facts with page numbers into VERIFIED-RESEARCH.md format. 5x faster than manual copy-paste. LOW complexity.
- **Retention-script correlation** — Map retention drops to script sections with actionable fixes ("3 videos dropped at 3min during legal explanations — add pattern interrupt"). Closes learning loop. MEDIUM complexity.
- **Feedback-aware script generation** — /script queries past performance before writing, applies lessons automatically. Prevents repeating mistakes. LOW complexity (v1.6 builds database foundation).

**Defer (v2+):**
- Thumbnail pattern analysis (wait for v1.6 Click & Keep foundation)
- Evidence display timing validator (requires video timeline integration)
- Topic success predictor (requires 30+ videos for reliability)
- Competitor analysis (nice to have, not essential)

**Anti-features (deliberately avoid):**
- Auto-generate thumbnails from B-roll (defeats evidence-based strategy)
- AI voice cloning (talking head channel needs on-camera authority)
- Real-time CTR dashboard (creates anxiety without actionable insights for 1-2 videos/month)
- Automated title optimization (risks clickbait violations of documentary tone)
- Script auto-revision (removes creator voice)

### Architecture Approach

Integration strategy follows existing patterns: markdown-first data flow, tool-assisted manual workflow, extend-don't-replace, reference hierarchy over code logic. NO database schema changes required (v27 sufficient). Focus on reference document expansion, not tool proliferation.

**Major components:**

1. **Voice Pattern Enhancement (Channel-Aware Scripts)** — Expand STYLE-GUIDE.md Part 6 with voice patterns from high-performing transcripts. Update script-writer-v2 agent to emphasize Part 6. NO new code needed — pure reference document expansion.

2. **Research Bridge (NotebookLM Integration)** — New tools/research/ modules: notebooklm_bridge.py (~300 LOC) generates academic source lists, citation_extractor.py (~200 LOC) parses NotebookLM output to VERIFIED-RESEARCH.md format. Extends /sources command with --notebooklm-prep and --extract-citations flags.

3. **Actionable Analytics (Retention Mapping)** — New tools/youtube-analytics/ modules: retention_mapper.py (~250 LOC) maps drop points to script sections, insights_generator.py (~200 LOC) generates concrete recommendations. Extends analyze.py orchestrator and adds --actionable flag to /analyze command.

**Integration points:**
- Voice patterns: STYLE-GUIDE.md → script-writer-v2 agent (existing read pattern)
- Research bridge: /sources command → format converters (manual upload/download preserved)
- Analytics: analyze.py → retention mapper → insights generator → POST-PUBLISH-ANALYSIS.md

**Build order:**
- Phase A: Voice patterns (3-5 hours, LOW risk, reference docs only)
- Phase B: NotebookLM bridge (6-8 hours, MEDIUM risk, manual workflow dependency)
- Phase C: Actionable analytics (8-10 hours, MEDIUM risk, depends on script parsing accuracy)

Total new code: ~950 lines (5% of existing 17,300 LOC codebase).

### Critical Pitfalls

Research identified seven pitfalls, three CRITICAL (block progress), four MODERATE (reduce value).

**CRITICAL:**

1. **Empty Patterns Syndrome (Voice Fingerprinting)** — Extracting voice patterns from <5 videos produces statistical noise, not signal. Pattern confidence thresholds misaligned (HIGH = freq ≥5, but with 3 videos no patterns reach HIGH). Creator sees 0-3 changes per script despite 1,500 words, perceives feature as broken, abandons it. **Prevention:** Validate corpus size ≥5 videos before extraction OR show LOW confidence warning. Graceful degradation with fallback to manual rules. One-command rebuild (/voice --rebuild) to reduce friction. Hybrid approach: manual overrides + corpus patterns.

2. **Generic Output Despite Channel Context (Brand Fragmentation)** — Script-writer-v2 agent has access to 50+ reference files but doesn't consistently apply rules. Output contains forbidden phrases despite style guide. Creator spends 2-3 hours editing "channel-aware" output. Training data (generic YouTube) overpowers channel-specific context. **Prevention:** Validation layer with three tiers (HARD BLOCKS = must pass before output shown, STYLE RULES = validate against STYLE-GUIDE.md, CHANNEL DNA = verify documentary tone). Two-pass generation: draft → validation → regenerate if violations → final check. Modular context injection (only relevant context per task, not dumping all 50 files). Pre-flight checklist automation (forbidden phrases, term definitions, contractions, both-extremes framework).

3. **NotebookLM "Bridge" Adds Friction Instead of Reducing It** — NotebookLM has no API. "Bridge" features add manual export steps instead of eliminating them. Manual steps: 8 before bridge, 9 after bridge. Creator tries feature once, abandons it. Real bottleneck is source identification (2-4 hours), not citation formatting (15 min). **Prevention:** Define "bridge" realistically as formatting helper, not automation. Document manual steps explicitly with [MANUAL] tags. Focus on source recommendation (academic book lists with ISBNs, download links) over citation formatting. Wait for official NotebookLM API (Google announced enterprise version 2026) instead of brittle browser automation.

**MODERATE:**

4. **Actionable Analytics That Produce Data, Not Decisions** — Analytics show "retention dropped 15% at 3:42, pacing score 18.3" but no guidance on WHAT to fix or HOW. Creator stares at dashboard, doesn't change behavior. Same mistakes repeated across videos. **Prevention:** Diagnostic messages with root cause analysis ("retention dropped due to 45-second static map during legal explanation — break into 20-second segments with zoom/highlight"). Decision-focused output format (structured around "Should we use this style again?" not raw metrics). Integration with production commands (surface insights WHERE decisions are made, not end of report). Pattern extraction with confidence scoring (N≥3 for patterns, report sample size and confidence intervals).

5. **Over-Engineering for 1-2 Videos/Month Workflow** — Feature roadmap includes automated A/B testing scheduler, variant recommendation engine, thumbnail clustering, multi-platform publishing. Solo creator publishes 1-2 videos/month. 80% of features never used. Pattern from project context: "Risk is building MORE tools that don't get used." **Prevention:** Ship minimum viable solution (manual CTR entry sufficient, not automated scheduler). One pain point solved completely > many pain points partially addressed. Feature gating by usage metrics (don't build Phase N+1 until Phase N features used ≥3 times). Complexity budget: max 20 commands (current: 14), 10 agents (current: 6), 25K LOC (current: 17,300).

6. **Small Dataset False Patterns** — With 15 videos, pattern analysis identifies "videos with <30 sec hooks have 8% higher retention." Creator applies pattern, retention doesn't improve. Pattern was statistical noise (confounding variables ignored, regression to mean not accounted for). **Prevention:** Minimum sample size requirements (N≥5 for patterns, N≥10 for topic-specific patterns). Report ranges not single numbers (retention: 35.2% average, range: 28.1%-42.6%, ±6.2% SD). Multi-factor analysis accounting for confounding variables (hook length + thumbnail type + topic type combined). Flag outliers explicitly (Essequibo 1,905 views is outlier with unique news hook, don't expect replication).

7. **Manual Workflow Automation That Isn't** — Feature promised: "Automated feedback loop." Reality: Creator still runs separate commands (analyze.py VIDEO_ID, then slash_commands.py script TOPIC), manually reads POST-PUBLISH-ANALYSIS.md, manually applies lessons. Automation didn't eliminate steps, just moved them. **Prevention:** Workflow consolidation (one command queries past performance automatically, not two separate commands). Proactive surfacing not passive embedding (show insights BEFORE script generation with "acknowledge to continue" prompt). Integration at decision points (surface during generation, not after). Enforce workflow dependencies (can't skip insight review).

## Implications for Roadmap

Based on research, v2.0 should follow three-phase structure prioritizing reference enhancement over code proliferation. Total implementation: 3-4 weeks (17-23 hours estimated).

### Phase 1: Voice Pattern Library (Channel-Aware Scripts)
**Rationale:** Highest value, lowest risk. No code changes needed — pure reference document expansion. Script-writer-v2 agent already reads STYLE-GUIDE.md, just needs better voice patterns documented in Part 6. Addresses primary pain point from project context: "Scripts are generic despite channel-aware agent."

**Delivers:**
- STYLE-GUIDE.md Part 6 expanded with voice patterns from high-performing transcripts (Belize, Vance)
- Sentence structure templates (Kraut causal chains: "consequently," "thereby," "which meant that")
- Phrase library (Alex O'Connor transitions, creator's proven phrases)
- script-writer-v2 agent frontmatter updated to emphasize Part 6

**Addresses features:**
- Voice pattern library (differentiator)
- Script generation from verified research (table stakes enhancement)

**Avoids pitfalls:**
- Empty Patterns Syndrome: Extract patterns from existing transcripts (≥5 videos), validate corpus size, show confidence warnings
- Generic Output Despite Context: Validation layer added (forbidden phrases, style rules, channel DNA checks before output shown)

**Research flags:** SKIP research-phase. Voice pattern extraction is well-documented (corpus linguistics, authorship attribution). Templates available in existing STYLE-GUIDE.md structure.

**Estimated effort:** 3-5 hours

---

### Phase 2: NotebookLM Research Bridge
**Rationale:** Addresses research bottleneck (2-4 hours identifying academic sources). Builds format converters and source recommenders, NOT automation (NotebookLM has no API). Tool-assisted manual workflow matches existing architecture pattern.

**Delivers:**
- tools/research/notebooklm_bridge.py: Generate academic source lists (university press titles, ISBNs, download links)
- tools/research/citation_extractor.py: Parse NotebookLM output to VERIFIED-RESEARCH.md format
- /sources command extended with --notebooklm-prep and --extract-citations flags
- NOTEBOOKLM-SOURCE-STANDARDS.md workflow documentation with explicit [MANUAL] step tags

**Uses stack elements:**
- markitdown (>=0.0.1a2): Document-to-markdown conversion
- jinja2 (>=3.1.5): Source list template generation

**Implements architecture:**
- Tool-assisted manual workflow pattern (tools prepare/parse, human does critical work)
- Markdown-first data flow (NOTEBOOKLM-SOURCE-LIST.md, VERIFIED-RESEARCH.md)
- Extend-don't-replace (/sources command gets new flags, not new command)

**Addresses features:**
- Academic source preparation for NotebookLM (differentiator)
- NotebookLM extraction prompts (differentiator)
- Source citation tracking (table stakes enhancement)

**Avoids pitfalls:**
- NotebookLM Bridge Friction: Build format converters, not automation. Document manual steps explicitly. Focus on source recommendation (2-4 hour bottleneck) over citation formatting (15 min task). Wait for official API instead of brittle workarounds.

**Research flags:** SKIP research-phase for source list generation (standard prompt engineering). LIGHT research for citation extraction format (NotebookLM output structure varies, may need adjustment during implementation).

**Estimated effort:** 6-8 hours

---

### Phase 3: Actionable Analytics with Retention Mapping
**Rationale:** Closes learning loop — retention patterns mapped to script sections with concrete fixes. Builds on v1.6 feedback database foundation. Prevents repeating mistakes (retention drops at 3min in multiple videos despite being flagged).

**Delivers:**
- tools/youtube-analytics/retention_mapper.py: Map drop points to script sections (correlate timestamps with script structure)
- tools/youtube-analytics/insights_generator.py: Generate concrete recommendations ("break 42-word sentence at line 47 into two segments")
- feedback_queries.py extended with get_actionable_insights() method
- analyze.py orchestrator integrates mapping + insights
- /analyze command gets --actionable flag for insights-first output
- POST-PUBLISH-ANALYSIS template updated with "WHAT to fix" and "HOW to fix it" sections

**Uses stack elements:**
- sentence-transformers (>=3.1.0): Compare script sections to high-retention examples
- chromadb (>=0.5.29): Store retention patterns by topic type (territorial, ideological, legal)
- faststylometry (>=0.1.0): Detect voice drift in AI-generated sections (if corpus sufficient)
- spacy (existing): Extract linguistic features (entity density, sentence variance)

**Implements architecture:**
- Extend-don't-replace (analyze.py gets retention mapping, doesn't rewrite existing metrics)
- Integration at decision points (insights surfaced during /script generation, not just in reports)
- Proactive surfacing (show insights BEFORE generation with acknowledgment prompt)

**Addresses features:**
- Retention-script correlation (differentiator)
- Feedback-aware script generation (differentiator)
- Retention drop detection (table stakes enhancement)
- Channel-specific CTR benchmarks (differentiator)

**Avoids pitfalls:**
- Data Without Decisions: Diagnostic messages with root causes, decision-focused output, integration with production commands, pattern extraction with confidence scoring
- Small Dataset False Patterns: Minimum sample size validation (N≥5 for patterns, N≥10 for topic-specific), report ranges not single numbers, multi-factor analysis, flag outliers explicitly
- Manual Workflow Automation: Proactive surfacing (before script generation), workflow enforcement (acknowledge to continue), integration at decision points (not end of output)

**Research flags:** MEDIUM research needed for script section parsing accuracy (depends on production/parser.py capabilities). Retention timestamp mapping may require manual calibration per video (SRT timestamps vs YouTube Analytics timestamps alignment). Pattern extraction confidence thresholds need empirical validation with actual video data.

**Estimated effort:** 8-10 hours

---

### Phase Ordering Rationale

**Phase 1 first (Voice Patterns):**
- Zero code risk (reference docs only)
- Immediate value (scripts match proven voice)
- Establishes quality baseline for later phases
- Validates agent's ability to apply reference patterns before building more complex features

**Phase 2 second (NotebookLM Bridge):**
- Addresses research bottleneck (2-4 hours identifying sources)
- Independent of Phase 1 (can develop in parallel if needed)
- Manual workflow matches reality (no API)
- Format converters useful immediately (even with small corpus)

**Phase 3 last (Actionable Analytics):**
- Depends on Phase 1 completion (retention recommendations reference voice patterns)
- Requires script section parsing (depends on production/parser.py)
- Benefits from multiple videos published with Phase 1/2 enhancements (more data for patterns)
- Most complex integration (analytics + script generation + feedback database)

**Dependency chain:**
```
Phase 1 (Voice Patterns)
    └──enables──> Phase 3 (retention recommendations reference voice patterns)

Phase 2 (NotebookLM Bridge)
    └──independent──> Can develop in parallel

Phase 3 (Actionable Analytics)
    └──requires──> Phase 1 complete (voice baseline established)
    └──requires──> Multiple videos published (pattern validation)
```

**How this avoids pitfalls:**
- Empty Patterns Syndrome mitigated in Phase 1 with corpus validation
- Generic Output prevented in Phase 1 with validation layer
- NotebookLM friction avoided in Phase 2 with format converters (not automation)
- Over-engineering prevented by complexity budget enforcement (3 phases, ~950 new LOC, 6 new command flags vs. building 14 new commands)
- Small dataset false patterns addressed in Phase 3 with minimum sample size requirements
- Manual workflow automation achieved in Phase 3 with proactive surfacing

### Research Flags

**Phases needing deeper research during planning:**
- **Phase 3 (Actionable Analytics):** Script section parsing accuracy depends on production/parser.py capabilities. SRT timestamp alignment with YouTube Analytics timestamps may need manual calibration. Pattern extraction confidence thresholds require empirical validation with actual video data. Recommend /gsd:research-phase for retention mapping algorithm design.

**Phases with standard patterns (skip research-phase):**
- **Phase 1 (Voice Patterns):** Corpus linguistics and authorship attribution are well-documented. Template structure exists in STYLE-GUIDE.md. Extract patterns, document in markdown, agent applies naturally.
- **Phase 2 (NotebookLM Bridge):** Format conversion and prompt engineering are standard patterns. NotebookLM output structure may vary but adapts during implementation (not research-blocking).

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | All libraries verified available (except Python 3.14 blocker identified with resolution path). Existing similar projects validate technical feasibility. Official SDKs from Anthropic, Microsoft, ChromaDB. |
| Features | HIGH | Table stakes identified from existing codebase analysis. Differentiators validated from channel performance data (Belize 23K, Vance 42.6%). Anti-features discovered from competitor research and project context. |
| Architecture | HIGH | Integration patterns match existing codebase (markdown-first, tool-assisted manual, extend-don't-replace, reference hierarchy). No schema changes needed. Total new code <6% of existing. |
| Pitfalls | HIGH | Critical pitfalls validated from multiple sources: corpus linguistics research (Empty Patterns), AI content generation studies (Generic Output), NotebookLM ecosystem analysis (Bridge Friction). Moderate pitfalls from project context and v1.x lessons learned. |

**Overall confidence:** HIGH

Caveat: Confidence assumes Python 3.14 → 3.13 downgrade completes successfully. If downgrade blocked (organizational constraint, dependency conflicts), spaCy incompatibility blocks faststylometry (voice matching) and existing script-checkers. Alternative: wait for spaCy 3.14 wheels (timeline unknown) or build from source on Windows (high effort, error-prone).

### Gaps to Address

**Gap 1: NotebookLM output format variability**
- **What's unknown:** NotebookLM export format may vary by source type (PDF vs DOCX vs URL). Citation extraction regex patterns may need adaptation.
- **How to handle:** Build citation_extractor.py with flexible parsing patterns. Test with multiple NotebookLM exports during Phase 2 implementation. Document known format variations.

**Gap 2: Script section parsing accuracy**
- **What's unknown:** Existing production/parser.py may not provide section-level granularity needed for retention mapping. SRT timestamps may not align precisely with YouTube Analytics retention curve timestamps.
- **How to handle:** Validate parser.py capabilities during Phase 3 planning. If insufficient, extend with section boundary detection. Add manual timestamp calibration option if automatic alignment unreliable.

**Gap 3: Pattern confidence thresholds with small dataset**
- **What's unknown:** With ~15 videos, empirically determining "HIGH confidence = freq ≥X" thresholds is uncertain. Standard corpus linguistics uses 5-10 documents minimum, but channel context may differ.
- **How to handle:** Start with conservative thresholds (HIGH = freq ≥5, MEDIUM = freq ≥3, LOW = freq ≥2). Track pattern reliability as corpus grows. Adjust thresholds based on false positive/negative rates in production.

**Gap 4: Voice pattern extraction completeness**
- **What's unknown:** High-performing transcripts (Belize, Vance) may not cover all creator voice patterns (e.g., patterns specific to ideological myth-busting vs territorial disputes). Extracted patterns may be topic-specific, not universal voice.
- **How to handle:** Extract patterns from diverse video types (territorial, ideological, legal). Flag topic-specific patterns explicitly. Build general voice baseline + topic-specific overlays. Validate with creator review during Phase 1.

**Gap 5: Feedback loop closure validation**
- **What's unknown:** Proactive surfacing in Phase 3 may not guarantee insight application. Creator may acknowledge warnings but forget during script writing. Application rate >60% target may not be achievable without stronger enforcement.
- **How to handle:** Track insight application rate post-Phase 3. If <60%, consider stronger enforcement (e.g., "Apply recommended fix or explain why not applicable" prompt). Balance enforcement with creator autonomy (don't block workflow, just encourage compliance).

## Sources

### Primary (HIGH confidence)

**Stack Research:**
- [anthropics/anthropic-sdk-python](https://github.com/anthropics/anthropic-sdk-python) — Official Python SDK, version 1.87.1 features
- [SentenceTransformers Documentation](https://sbert.net/) — Semantic similarity implementation, model selection
- [ChromaDB Official Site](https://www.trychroma.com/) — Local vector database architecture, performance benchmarks
- [microsoft/markitdown](https://github.com/microsoft/markitdown) — Document conversion capabilities, format support
- [spaCy Issue #13885](https://github.com/explosion/spaCy/issues/13885) — Python 3.14 incompatibility confirmation

**Architecture Research:**
- Existing codebase analysis: .planning/codebase/ARCHITECTURE.md, tools/youtube-analytics/, .claude/agents/
- [SQLite DB Migrations with PRAGMA user_version](https://levlaz.org/sqlite-db-migrations-with-pragma-user_version/) — Auto-migration pattern
- [Python CLI Design Patterns](https://cli-guide.readthedocs.io/en/latest/design/patterns.html) — Error dict pattern, feature flags

**Pitfalls Research:**
- [Cold Start Problem in Machine Learning](https://spotintelligence.com/2024/02/08/cold-start-problem-machine-learning/) — Small dataset challenges
- [NotebookLM API Official Documentation](https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks) — API status (enterprise only, manual workflow required)
- Project context: User feedback on existing tool usage, v1.x lessons learned

### Secondary (MEDIUM confidence)

**Feature Research:**
- [10 Best AI Tools for YouTube Creators in 2026](https://aitoolsforcontentcreators.com/best-ai-tools-youtube-2026) — Competitive landscape
- [YouTube Retention Graphs Explained](https://www.opus.pro/blog/youtube-retention-graphs-explained) — Retention analysis patterns
- [NotebookLM Guide: 25 Pro Tips](https://atalupadhyay.wordpress.com/2025/08/09/notebooklm-guide-25-pro-tips-for-research-excellence/) — Workflow integration strategies

**Pitfalls Research:**
- [Use Generative AI Without Losing Brand Authenticity](https://www.aprimo.com/blog/use-generative-ai-for-content-creation-without-losing-brand-authenticity) — Generic output prevention
- [The Hidden Cost of Over-Engineering](https://dev.to/alisamir/the-hidden-cost-of-over-engineering-in-software-development-4dnk) — Feature bloat risks
- [Google Analytics Actionable Insights: 2026 Complete Guide](https://almcorp.com/blog/google-analytics-actionable-insights-complete-guide-2026/) — Decision-focused analytics

### Tertiary (LOW confidence)

**Voice Pattern Research:**
- [Best AI Voice Cloning Tools in 2026](https://fish.audio/blog/best-ai-voice-cloning-tools/) — Voice matching approaches (audio-focused, adapted for text patterns)
- [Introduction to stylometry with Python](https://programminghistorian.org/en/lessons/introduction-to-stylometry-with-python) — Authorship attribution techniques

---
*Research completed: 2026-02-09*
*Ready for roadmap: yes*
