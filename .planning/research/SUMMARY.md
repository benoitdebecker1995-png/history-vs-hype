# Project Research Summary

**Project:** History vs Hype v1.2 - Script Quality & Discovery
**Domain:** YouTube content production workspace enhancement
**Researched:** 2026-01-27
**Confidence:** HIGH

## Executive Summary

This research evaluates adding script quality improvements, discovery/SEO optimization, and NotebookLM workflow automation to an existing YouTube content production workspace. The creator currently spends 5.5 hours per video on script revision cycles and faces low impression counts despite strong retention (30-35%). The channel has 543 lines of documented voice patterns and an established academic research workflow, but AI-generated scripts need heavy revision and topic discovery is manual guesswork.

**Recommended approach:** Enhance existing components rather than building parallel systems. Use Claude API for script generation with prompt caching ($0.50-$1.20/month), YouTube autocomplete + pytrends for free keyword research, and structured prompt templates for NotebookLM workflow optimization. The existing architecture (slash commands → Python scripts → Markdown reference) can absorb all three additions without structural changes.

**Critical risk:** Voice dilution. AI tools trained on billions of sources create gravitational pull toward generic patterns. The channel's competitive advantage is its fusion of Kraut's causal chains with Alex O'Connor's conversational authority - generic "improvement" suggestions will destroy what makes retention work. Prevention: Use AI as analyzer (flags issues), not writer (creator fixes in own voice). Second risk: SEO over-optimization breaking documentary tone. Mitigation: Implement AUTO-REJECT rules before seeing suggestions (no clickbait, emotional manipulation, or vague pronouns).

## Key Findings

### Recommended Stack

The existing Python-based architecture with Claude Code integration is well-suited for all three additions. No major infrastructure changes needed - this is an enhancement milestone, not a rebuild.

**Core technologies:**
- **Claude Sonnet 4.5 API** (script generation) - 200K context window fits entire style guide + research. Prompt caching reduces costs 90% and latency 85%. Estimated $0.50-$1.20/month for 2 scripts.
- **py-readability-metrics + textstat** (script quality) - Industry-standard readability scoring. Target: 60-70 Flesch Reading Ease, 12-18 word sentence length for spoken delivery.
- **spaCy** (repetition detection) - N-gram analysis to flag repeated phrases within 500-word windows. Catches AI's tendency to say same thing 3+ times.
- **YouTube autocomplete endpoint** (discovery) - Undocumented but stable. Community-validated for years. Reveals what viewers actually search for.
- **pytrends** (Google Trends) - Unofficial scraper for search volume trends. Fragile (breaks when Google changes backend) but free and maintained by community.
- **YouTube Data API v3** (already integrated) - Extend existing auth for search/competition analysis. 10,000 unit daily quota = ~95 keyword analyses.

**Critical finding:** NotebookLM has NO production-ready API (Enterprise API in alpha, consumer API doesn't exist). Focus on workflow optimization (structured prompts, export templates) not technical integration. Manual copy-paste faster than browser automation for 20-30 queries per video.

### Expected Features

Research reveals three distinct feature categories with clear table stakes vs. differentiators:

**Must have (table stakes):**
- **Repetition Detection** - AI scripts repeat same facts/phrases 3+ times. Flag identical/near-identical phrases crossing threshold.
- **Flow Analyzer** - Topics introduced awkwardly without setup. Check narrative flow rules (terms defined before use, bridges between transitions).
- **Stumble Test Automation** - Sentences >25 words or complex subordinate clauses that work written but not spoken.
- **Long-Tail Keyword Extractor** - Videos target broad terms, not search queries. Extract 3-4 word phrases, cross-reference with autocomplete.
- **Search Intent Mapper** - "Why X?" vs "How X happened" vs "What is X?" are different intents requiring different titles.
- **Impression Diagnostic** - Simple logic: impressions <500 in 7 days = SEO issue. Impressions OK + CTR <2% = thumbnail/title issue.
- **Citation Extraction** - Manual copy-paste of NotebookLM page numbers is 40% of research time. Structured export format required.

**Should have (competitive differentiators):**
- **Voice Fingerprinting** - Learn user's actual speech patterns from existing transcripts (Somaliland, Bir Tawil, Iran). Build pattern library, flag violations. Biggest ROI for quality.
- **Retention Heatmap Preview** - Predict dropout zones before filming. ML model trained on 30 published videos. Worth filming better scripts, prevents 0-8 second dropout.
- **Title A/B Test Manager** - Track which title patterns drive impressions. 3 variants per video, track first 48 hours, log winners. Empirical data vs. guesswork.
- **Cross-Source Synthesizer** - "How do these 3 sources compare on [claim]?" Handles "Plutarch says X but Pausanias says Y" automatically.
- **Contradiction Detector** - Flag when sources disagree. Creates intellectual honesty opportunities ("Source A says X, Source B says Y...").

**Defer (v2+):**
- **Retention Heatmap** - Requires 30+ videos with retention data for ML training. Channel doesn't have this yet.
- **Google AI Overview Optimizer** - Format content for AI citation in AI Overviews. Nascent feature, ROI unclear.
- **Search Volume Estimator** - Predict impressions before publishing. High complexity, marginal benefit over autocomplete.

**Anti-features (deliberately NOT build):**
- Generic hook generator (violates documentary tone)
- Auto-script generator (quality control violation, produces "AI slop")
- Viral title optimizer (optimizes CTR without retention = clickbait)
- Comment auto-responder (brand voice can't be automated)
- Keyword stuffing tool (YouTube 2026 penalizes this)

### Architecture Approach

The existing architecture (slash commands → Python scripts → Markdown reference → agents) can absorb all three additions through targeted enhancements to existing components rather than parallel systems. This preserves single-source-of-truth principle and avoids cognitive overload.

**Major components:**

1. **Enhanced script-writer-v2 agent** - Add pre-writing checklist enforcement (verify identity stake, check coverage gaps) and post-writing quality gates (stumble test, "here's" count, forbidden phrase scan). Reads enhanced STYLE-GUIDE.md with quality patterns from existing scripts.

2. **New discovery module** (`tools/youtube-analytics/discovery.py` + `title_optimizer.py`) - Keyword research via YouTube autocomplete, competition analysis via YouTube Data API, title variant generation following channel DNA patterns. Accessed via new `/discover` slash command with flags.

3. **Workflow optimization for NotebookLM** - Structured prompt templates in NOTEBOOKLM-SCRIPTWRITING-PROMPTS.md (expand from 5 to 15+ use cases), new session log file (`02-NOTEBOOKLM-SESSION.md`) for tracking findings, enhanced `/sources` command with `--notebooklm-prompts` and `--parse-session` flags.

**Integration pattern:** Discovery → Research → NotebookLM → Script Quality form natural pipeline. PROJECT-STATUS.md tracks progression. Each component can be used independently or as integrated workflow.

### Critical Pitfalls

1. **Voice Dilution Trap** - AI tools improve "quality" metrics (grammar, flow, clarity) while destroying creator voice. Scripts become indistinguishable from generic YouTube content. The 543-line STYLE-GUIDE.md becomes useless because AI "corrects" intentional patterns (contractions → formal, "here's" eliminated as filler). Prevention: Use AI as analyzer only (flags issues), creator fixes in own voice. Vulnerable sections (hooks, conclusions, steelmanning) must be human-written. Early warning: Scripts pass quality checks but "feel off" when reading.

2. **SEO Over-Optimization Death Spiral** - Chasing keywords and CTR transforms documentary channel into clickbait. VidIQ suggests "SHOCKING Truth" titles, creator accepts because "data says it works," audience who subscribed for intellectual rigor leaves. Result: High CTR, terrible retention (wrong audience). Prevention: Implement AUTO-REJECT rules BEFORE seeing suggestions (no emotional manipulation, all-caps, vague pronouns, listicle formats). Channel DNA litmus test: "Would this work on PBS documentary? If no → reject."

3. **NotebookLM Manual Workarounds That Collapse** - Creator develops workarounds for 50-source limit (merging PDFs, splitting across notebooks). Works for one video, collapses at scale when managing 5+ videos with 20+ sources each. Citations break, file organization destroyed. Prevention: Accept the constraint, design around it. 10-20 excellent sources > 50 mediocre ones. Use NotebookLM Study Guides to extract maximum value from fewer sources. Maintain VERIFIED-RESEARCH.md as single source of truth, not NotebookLM.

4. **Prompt Over-Engineering Paralysis** - Creator writes 2,000-token mega-prompts trying to capture every STYLE-GUIDE.md nuance. AI output worse than simple prompts because model gets lost in complexity. Prevention: Task-specific micro-prompts (150 tokens max). Detection prompts ("Find repetitions"), not rewrite prompts ("Improve this section"). Layer 1: Detection → Layer 2: Analysis → Layer 3: Creator decides fix. Reference files, don't embed (upload STYLE-GUIDE.md, prompt says "Following style guide, identify violations").

5. **Breaking Existing Workflows with "Improvements"** - New script quality tool requires reformatting all scripts to JSON schema. Breaks existing `/script` command. Creator spends week on migration, realizes old workflow was better. 52% of projects experience scope creep when adding features. Prevention: Minimum viable addition (ONE feature at a time, test with ONE video). Backwards compatibility requirement (must work with existing files). Kill switch planning (document reversion process before adopting).

## Implications for Roadmap

Based on research, suggested 4-phase structure prioritizing quick wins before complex features:

### Phase 1: Script Quality Foundation (Week 1)
**Rationale:** Quick wins with immediate workflow improvement. Script quality issues cause most revision time currently. Enhance existing components (script-writer-v2 agent, STYLE-GUIDE.md) rather than building new systems.

**Delivers:** Better first drafts with fewer revisions (target: 30% reduction from ~3 rounds to ~2 rounds).

**Addresses table stakes features:**
- Stumble Test Automation - Flag sentences >25 words
- "Here's" Counter - Ctrl+F automation with recommendations when >4 uses
- Repetition Detection (basic) - Scan for identical phrases

**Avoids Pitfall 1 (Voice Dilution):** Quality gates warn, don't rewrite. Creator fixes issues in own voice. AI analyzer only.

**Technical tasks:**
- Enhance STYLE-GUIDE.md with quality patterns from existing scripts (2 hours)
- Update script-writer-v2 with quality gates (4 hours)
- Add `--quality-gate` flag to `/script` command (1 hour)
- Test on 3 existing scripts, measure revision reduction (2 hours)

**Research flag:** Standard patterns, no additional research needed.

---

### Phase 2: Discovery Tools (Week 2)
**Rationale:** Low impressions problem documented. Free tools (YouTube autocomplete + pytrends + existing YouTube Data API) provide 80% of value vs. paid APIs. New Python module following established patterns in `tools/youtube-analytics/`.

**Delivers:** Data-driven topic validation, keyword research in <10 minutes, title optimization with CTR predictions.

**Addresses table stakes features:**
- Long-Tail Keyword Extractor
- Search Intent Mapper
- Impression Diagnostic
- Metadata Consistency Check

**Avoids Pitfall 2 (SEO Over-Optimization):** Implement VIDIQ-CHANNEL-DNA-FILTER.md AUTO-REJECT rules FIRST, before generating suggestions. Discovery tools inform, don't decide - human validates before proceeding.

**Technical tasks:**
- Create `tools/youtube-analytics/discovery.py` with autocomplete + trends integration (6 hours)
- Create `tools/youtube-analytics/title_optimizer.py` using existing title pattern data (4 hours)
- Create `.claude/commands/discover.md` slash command (2 hours)
- Test on 5 topics (2 successful videos, 3 hypothetical), validate against VidIQ Pro (3 hours)

**Research flag:** YouTube autocomplete endpoint is undocumented but stable. Monitor for changes. pytrends breaks occasionally when Google changes backend - community usually fixes within days.

---

### Phase 3: NotebookLM Workflow Integration (Week 3)
**Rationale:** Research phase currently 8 hours per video. 25% reduction possible through structured prompts and export templates. No API available, so focus on workflow optimization not technical integration.

**Delivers:** Targeted prompts eliminate "what should I ask?" friction. 95%+ of verified claims have page number citations. Research phase time: 6 hours (down from 8).

**Addresses table stakes features:**
- Citation Extraction (via structured export format)
- Quote Export (copy-paste templates)
- Batch Query Runner (prompt library)

**Avoids Pitfall 3 (Manual Workarounds That Collapse):** Accept 50-source limit. Quality over quantity. 10-20 academic sources from university presses, not 50 blog posts. External citation management in VERIFIED-RESEARCH.md, not relying on NotebookLM for long-term storage.

**Technical tasks:**
- Expand NOTEBOOKLM-SCRIPTWRITING-PROMPTS.md from 5 to 15+ targeted use cases (3 hours)
- Create NOTEBOOKLM-RESEARCH-WORKFLOW.md template (2 hours)
- Add `--notebooklm-prompts` and `--parse-session` flags to `/sources` command (4 hours)
- Add 02-NOTEBOOKLM-SESSION.md to project templates (1 hour)
- Test on next 2 videos, measure time savings (4 hours)

**Research flag:** If NotebookLM releases production API mid-implementation, architecture supports retrofitting. Current manual workflow remains as fallback.

---

### Phase 4: Integration Testing & Refinement (Week 4)
**Rationale:** Validate end-to-end workflow improvements. Measure actual time savings vs. baseline. Identify friction points before declaring complete.

**Delivers:** Full Discovery → Research → NotebookLM → Script workflow tested. User-reported friction points documented. Lessons learned captured for future improvements.

**Addresses:** System integration, workflow validation, success metrics confirmation.

**Avoids Pitfall 5 (Breaking Existing Workflows):** Test reversion process. Ensure backwards compatibility. Kill switch validated for each component.

**Technical tasks:**
- Full workflow test: Discovery → Research → NotebookLM → Script (8 hours)
- Measure time savings vs v1.1 baseline: script quality, research time, discovery time (2 hours)
- Collect user friction points, refine components (4 hours)
- Document lessons in .planning/research/LESSONS.md (2 hours)

**Success criteria:**
- Script first-draft quality: 8/10+ (vs current ~6/10)
- Research-to-script time: <2 weeks (vs current ~3 weeks)
- User reports workflow feels smoother, not more complex

---

### Phase Ordering Rationale

**Why this order:**
- Phase 1 (Script Quality) builds foundation. Quality improvements apply to ALL future scripts, so highest ROI to implement first.
- Phase 2 (Discovery) is independent of script quality. Can be developed in parallel mindset, but implemented after to validate script improvements first.
- Phase 3 (NotebookLM) feeds into script quality. Better research → better scripts. But quality gates from Phase 1 help evaluate research completeness.
- Phase 4 (Integration) validates compound benefits. Each phase works independently, but integration creates multiplier effect.

**Dependency management:**
- Phases 1-2 are independent (no technical dependencies)
- Phase 3 depends on Phase 1 outputs (quality gates help identify research gaps)
- Phase 4 depends on all three prior phases

**Pitfall avoidance:**
- Each phase is ONE feature at a time (avoids scope creep)
- Each phase has backwards compatibility (can revert if needed)
- Each phase has kill switch (old workflow remains available)
- Phased rollout catches voice dilution early (Phase 1) before automation expands (Phases 2-3)

### Research Flags

**Phases needing deeper research during planning:**
- **Phase 2 (Discovery):** YouTube autocomplete endpoint is undocumented. Monitor for rate limiting or changes. pytrends is unofficial scraper - may need fallback strategy if Google blocks.
- **Phase 3 (NotebookLM):** Enterprise API in alpha, may become available. Architecture should support retrofit if API launches.

**Phases with standard patterns (skip research):**
- **Phase 1 (Script Quality):** Text analysis libraries (py-readability-metrics, textstat, spaCy) are well-documented with clear APIs. Standard NLP patterns.
- **Phase 4 (Integration):** Testing and refinement patterns are standard across all projects. No domain-specific research needed.

**Post-MVP research candidates (defer to v1.3+):**
- **Voice Fingerprinting:** Requires transcript analysis of user's actual delivery. Need 3-5 complete video transcripts with timing data. ML pattern recognition.
- **Retention Heatmap:** Requires 30+ videos with retention data for training. Channel doesn't have this dataset yet. Defer until ~40 videos published.
- **Cross-Source Synthesizer:** Complex NLP for comparing source positions. High complexity, marginal improvement over manual. Research if user friction indicates need.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Official Claude API, established Python libraries (spaCy, textstat), community-validated YouTube endpoints. Cost estimates based on transparent pricing. |
| Features | MEDIUM | User pain points documented (revision cycles, low impressions), but ROI projections are estimates. Time savings unvalidated until implementation. |
| Architecture | HIGH | Existing codebase analyzed (12 slash commands, 5,000 lines Python, 543-line STYLE-GUIDE.md). Proposed enhancements follow established patterns. |
| Pitfalls | HIGH | Voice dilution documented by AI writing researchers. SEO over-optimization is common YouTube creator mistake. NotebookLM limitations confirmed by multiple sources. |

**Overall confidence:** HIGH

Research based on official documentation (Claude API, YouTube Data API), community-validated tools (pytrends, autocomplete endpoint), and direct analysis of existing codebase. Feature complexity estimates are conservative. Pitfall research draws from 2026 YouTube ecosystem analysis and AI writing best practices.

### Gaps to Address

**Gap 1: YouTube autocomplete stability**
- **Issue:** Endpoint is undocumented, could change without notice.
- **Handling:** Build graceful fallback to manual keyword input. Monitor community tools (Apify, BOTSTER) for breakage warnings. Implement retry logic with exponential backoff.

**Gap 2: pytrends fragility**
- **Issue:** Breaks when Google changes Trends backend. Community fix lag can be days.
- **Handling:** Don't make pytrends blocking. If unavailable, Discovery tools still provide value via autocomplete + YouTube Data API. Document alternative: Glimpse API (commercial, overkill for solo creator but available).

**Gap 3: NotebookLM API uncertainty**
- **Issue:** Enterprise API in alpha. Consumer API roadmap unknown. Manual workflow may need to persist longer than ideal.
- **Handling:** Design structured prompts and export templates for current manual workflow. Architecture supports retrofit if API launches (existing prompt generation system becomes API caller instead of copy-paste generator).

**Gap 4: Voice fingerprinting requires transcripts**
- **Issue:** User has only 3 complete video transcripts currently (Somaliland, Bir Tawil, Iran Part 1). Voice pattern library may need 5+ for accuracy.
- **Handling:** Defer voice fingerprinting to v1.3 after more videos published. Phase 1 quality gates use documented patterns from STYLE-GUIDE.md (543 lines of explicit rules).

**Gap 5: Title optimization accuracy unknown**
- **Issue:** CTR predictions based on historical pattern matching, not predictive model. Accuracy untested.
- **Handling:** Start with pattern matching only. Track accuracy across 5+ videos. If predictions consistently wrong (>50% error), add ML model or simplify to pattern identification without prediction.

## Sources

### Primary (HIGH confidence)

**Official API Documentation:**
- [Claude API Pricing 2026](https://www.metacto.com/blogs/anthropic-api-pricing-a-full-breakdown-of-costs-and-integration) - Sonnet 4.5: $3/M input, $15/M output, prompt caching reduces 90%
- [YouTube Data API v3 Search](https://developers.google.com/youtube/v3/docs/search/list) - Official documentation, quota costs confirmed
- [NotebookLM Enterprise API](https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks) - Alpha status confirmed, consumer API doesn't exist

**Established Libraries:**
- [py-readability-metrics GitHub](https://github.com/cdimascio/py-readability-metrics) - Well-maintained, clear documentation
- [textstat PyPI](https://pypi.org/project/textstat/) - Industry standard for readability scoring
- [spaCy Documentation](https://spacy.io/) - Production-ready NLP library

**Existing Codebase:**
- `.claude/commands/` - 12 slash commands analyzed
- `tools/youtube-analytics/` - 10 Python scripts, ~5,000 lines
- `.claude/REFERENCE/STYLE-GUIDE.md` - 543 lines, authoritative style reference
- `.claude/agents/script-writer-v2.md` - 1,203 lines, comprehensive rule system

### Secondary (MEDIUM confidence)

**YouTube Discovery Tools:**
- [YouTube Autocomplete Scraper - Apify](https://apify.com/scraper-mind/youtube-autocomplete-scraper) - Community tool using same endpoint, confirms stability
- [Hacking YouTube Suggest API](https://dev.to/adrienshen/hacking-together-your-own-youtube-suggest-api-c0o) - Developer walkthrough of undocumented endpoint
- [pytrends GitHub](https://github.com/GeneralMills/pytrends) - Community-maintained, 6K+ stars, active development

**NotebookLM Workflow Research:**
- [NotebookLM Research Workflow 2026](https://www.geeky-gadgets.com/notebooklm-research-upgrade-2026/) - Automation features and limitations
- [Deep Research Workflow Guide](https://medium.com/@ferreradaniel/how-to-use-notebooklm-better-than-99-of-people-deep-research-workflow-guide-4e54199c9f82) - Advanced techniques, manual process validation
- [NotebookLM for YouTube Content Creation](https://medium.com/aimonks/from-research-notes-to-revenue-how-notebooklm-transforms-youtube-content-creation-in-2026-d283abdd73cd) - 2026 content workflow patterns

**AI Writing & Voice Preservation:**
- [How to Use AI Writing Tools Without Losing Voice 2026](https://rivereditor.com/guides/how-to-use-ai-writing-tools-without-losing-voice-2026) - Use AI as analyzer, not writer
- [Common AI Writing Mistakes](https://www.yomu.ai/resources/common-ai-writing-mistakes-and-how-to-avoid-them) - Repetition, generic patterns documented
- [Keeping Your Voice When Using AI](https://www.thetransmitter.org/from-bench-to-bot/keeping-it-personal-how-to-preserve-your-voice-when-using-ai/) - Targeted requests, custom instructions

### Tertiary (LOW confidence, needs validation)

**YouTube SEO Best Practices:**
- [YouTube SEO Optimization 2026 Guide](https://influenceflow.io/resources/youtube-seo-optimization-techniques-the-complete-2026-guide/) - General advice, not channel-specific
- [YouTube Audience Retention Benchmarks](https://socialrails.com/blog/youtube-audience-retention-complete-guide) - Industry averages, may not apply to educational content
- [YouTube Keyword Research Tools Comparison](https://prettyinsights.com/best-youtube-keyword-research-tools/) - Tool reviews, not performance data

**Scope Creep Statistics:**
- [Understanding Scope Creep in Project Management](https://projectmanagementacademy.net/resources/blog/pmp-scope-creep/) - 52% of projects experience it
- [What Is Scope Creep and How Can I Avoid It](https://www.projectmanager.com/blog/5-ways-to-avoid-scope-creep) - Prevention strategies

---

*Research completed: 2026-01-27*

*Ready for roadmap: YES*

*Next steps: Create detailed requirements for Phase 1 (Script Quality Foundation)*
