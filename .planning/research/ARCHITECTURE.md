# Architecture Patterns for Script Quality, Discovery & NotebookLM Integration

**Domain:** YouTube content production workspace
**Researched:** 2026-01-27
**Milestone:** v1.2 - Script Quality & Discovery
**Confidence:** HIGH (existing codebase analysis + 2026 tooling research)

---

## Executive Summary

This architecture research addresses how to integrate three new capabilities into an existing YouTube content production workspace:

1. **Script quality improvements** - Better first drafts with natural spoken delivery
2. **Discovery/SEO optimization** - Topic research, keyword analysis, title optimization
3. **NotebookLM workflow integration** - Streamlined research-to-script pipeline

**Key finding:** The existing architecture (slash commands → Python scripts → Markdown reference) is well-suited for all three additions. No major structural changes needed.

**Recommendation:** Follow established patterns with targeted enhancements to existing components rather than building parallel systems.

---

## Existing Architecture Analysis

### Current Component Structure

**Slash Commands (`.claude/commands/*.md`):**
- Entry points for user actions
- Orchestrate workflows across multiple tools
- 12 commands currently (research, script, verify, analyze, patterns, etc.)
- Pattern: Commands define what to do, agents/scripts do the work

**Python Scripts (`tools/youtube-analytics/*.py`):**
- Data processing and API integration
- 10 scripts covering metrics, retention, CTR, comments, patterns
- Pattern: Pure data → return dicts with `{error: "msg"}` on failure
- Pattern: CLI-friendly with `--flags` for variants

**Reference Docs (`.claude/REFERENCE/*.md`):**
- Knowledge base for agents and commands
- STYLE-GUIDE.md is authoritative for script style
- Templates for research, scripts, metadata
- Pattern: Markdown files with structured sections

**Agents (`.claude/agents/*.md`):**
- Specialized behaviors for complex tasks
- script-writer-v2 is main scriptwriting agent
- Pattern: Agent reads reference docs, applies rules, produces output

**Video Projects (`video-projects/_IN_PRODUCTION/`):**
- Per-video folders with standard file structure
- 01-VERIFIED-RESEARCH.md, SCRIPT.md, PROJECT-STATUS.md
- Pattern: Lifecycle folders (_IN_PRODUCTION, _READY_TO_FILM, _ARCHIVED)

### Architecture Strengths

1. **Separation of concerns:** Commands orchestrate, scripts process data, agents produce content
2. **Discoverability:** `/help` and `/status` make system navigable
3. **Reference-driven:** Knowledge in markdown, not hardcoded in agents
4. **Solo-creator optimized:** Everything runs through Claude Code
5. **Git-tracked evolution:** Script and style changes tracked without file proliferation

### Integration Points Identified

| New Feature | Natural Integration Point | Why |
|-------------|---------------------------|-----|
| Script quality improvements | script-writer-v2 agent + STYLE-GUIDE.md | Agent already reads style guide, just needs enhanced rules |
| Discovery/SEO tools | New Python scripts in tools/youtube-analytics/ | Matches existing pattern (analyze.py, patterns.py) |
| NotebookLM workflow | /research and /sources slash commands | Already handle research phase, need NotebookLM bridge |

---

## Recommendation 1: Script Quality Improvements

### Architecture: Enhance Existing Components

**Don't create:** New script-writer-v3 agent, separate quality-check tool, standalone polish script

**Do enhance:** script-writer-v2 agent, STYLE-GUIDE.md, /script command

### Component Changes

**`.claude/agents/script-writer-v2.md`**
- Add pre-writing checklist enforcement (verify identity stake, check coverage gaps)
- Add post-writing quality gates (stumble test, "here's" count, forbidden phrase scan)
- Add auto-detection for common patterns (transcript snippets → spoken delivery)
- Keep existing reference-reading pattern

**`.claude/REFERENCE/STYLE-GUIDE.md`**
- Add "Common Script Issues" section with before/after examples
- Add "First Draft Quality Checklist" for agents
- Add "Revision Triggers" (when to apply which fixes)
- Maintain single-source-of-truth status

**`.claude/commands/script.md`**
- Add `--quality-gate` flag for strict enforcement mode
- Add `--polish` flag for teleprompter-ready cleanup
- Absorb quality checks into existing `--review` flag

### Why This Pattern Works

**Leverage existing authority:** STYLE-GUIDE.md is already the canonical style reference. Adding quality rules there means all future agents inherit them.

**Incremental improvement:** script-writer-v2 already has 13 rules. Adding quality gates is natural extension, not architectural shift.

**No parallel systems:** Don't create separate quality-checker that duplicates script-writer knowledge. Keep quality rules in one agent.

**Matches user workflow:** User runs `/script`, gets better first draft. No new commands to learn.

### Implementation Approach

1. Enhance STYLE-GUIDE.md with quality patterns (LOW confidence items from existing scripts)
2. Update script-writer-v2 with pre-flight checks and post-generation validation
3. Test on 3-5 existing scripts to validate improvements
4. Add `--polish` flag to `/script` for final teleprompter cleanup

---

## Recommendation 2: Discovery/SEO Optimization

### Architecture: New Python Scripts + New Slash Command

**Don't create:** API integration to VidIQ (no API available), web scraping for keyword data, complex ML prediction models

**Do create:** New Python scripts following established patterns, new `/discover` slash command

### Component Structure

**New: `tools/youtube-analytics/discovery.py`**
- Keyword research using YouTube autocomplete API
- Search volume estimation (relative, not absolute)
- Competition analysis (existing video count, view distribution)
- Returns structured data: `{keywords: [...], competition: {...}, recommendations: [...]}`

**New: `tools/youtube-analytics/title_optimizer.py`**
- Title variant generation following channel DNA patterns
- CTR prediction based on historical title patterns
- A/B test suggestions
- Returns: `{variants: [...], predictions: {...}, test_plan: {...}}`

**New: `.claude/commands/discover.md`**
- Entry point for discovery workflow
- Flags: `--keywords TOPIC`, `--titles TOPIC`, `--competition TOPIC`
- Orchestrates Python scripts, formats output for user

**Enhanced: `channel-data/patterns/TOPIC-ANALYSIS.md`**
- Discovery tools write findings here
- Becomes source of truth for "what topics work"
- Pattern recognition from `/patterns` informs future discovery

### Data Flow

```
User: /discover --keywords "medieval flat earth"
  ↓
discover.md command reads request
  ↓
Calls discovery.py with topic
  ↓
discovery.py queries YouTube autocomplete, analyzes results
  ↓
Returns {keywords: [...], volume: {...}, competition: {...}}
  ↓
Command formats as markdown, saves to project folder
  ↓
User reviews findings, decides to proceed or pivot
```

### Why This Pattern Works

**Follows Python script pattern:** Same structure as analyze.py (orchestrator), metrics.py (data fetcher), patterns.py (analyzer)

**No external dependencies:** Uses YouTube APIs already authenticated, no new API keys needed

**Graceful degradation:** If YouTube autocomplete unavailable, falls back to manual keyword list + competition check

**Integrates with existing workflow:** Discovery findings inform `/research --new` project creation

### API Integration Strategy

**YouTube Data API v3 (already authenticated):**
- Search API for keyword competition analysis
- Video metadata for view distribution on topic
- Channel data for competitor research

**YouTube autocomplete (public endpoint):**
- No auth required
- Returns search suggestions for partial queries
- Proxy for relative search volume

**No VidIQ API:** VidIQ has no public API. Use existing Pro subscription for manual validation only.

### Implementation Approach

1. Create discovery.py with YouTube autocomplete + Data API integration
2. Create title_optimizer.py using existing title pattern data from TITLE-PATTERNS.md
3. Add /discover command following /analyze pattern
4. Test on 5 topics (2 successful videos, 3 hypothetical)
5. Validate recommendations against VidIQ Pro manual checks

---

## Recommendation 3: NotebookLM Workflow Integration

### Architecture: Document Bridge, Not API Integration

**Critical constraint:** NotebookLM has no API (as of Jan 2026). Cannot automate.

**Don't create:** Automated NotebookLM query system, API wrapper, browser automation

**Do create:** Structured prompt library, research template system, manual workflow optimization

### Component Structure

**Enhanced: `.claude/REFERENCE/NOTEBOOKLM-SCRIPTWRITING-PROMPTS.md`**
- Expand from 5 use cases to 15+ targeted prompts
- Add copy-paste templates for common queries
- Add verification prompts (cross-check claims across sources)
- Add scriptwriting prompts (quote extraction, causal chain identification)

**New: `.claude/templates/NOTEBOOKLM-RESEARCH-WORKFLOW.md`**
- Step-by-step research process
- Checklist for each phase (upload → audio overview → targeted queries → verification)
- Quality gates (when to mark claims ✅ VERIFIED)
- Examples of good vs bad NotebookLM usage

**Enhanced: `.claude/commands/sources.md`**
- Add `--notebooklm-prompts` flag to generate targeted prompts for uploaded sources
- Add `--verification-checklist` flag for cross-checking claims
- Generate prompts based on video type (territorial dispute, myth-busting, fact-check)

**New: `video-projects/_IN_PRODUCTION/[project]/_research/02-NOTEBOOKLM-SESSION.md`**
- Track what was asked, what was verified, what remains uncertain
- Record citation page numbers from NotebookLM citations
- Log where sources disagree (to address in script)

### NotebookLM → Claude Bridge Strategy

**The manual workflow:**

1. **User uploads sources to NotebookLM** (10-20 PDFs per video)
2. **Claude generates targeted prompts** via `/sources --notebooklm-prompts`
3. **User runs prompts in NotebookLM**, clicks citations for page numbers
4. **User copies findings to 02-NOTEBOOKLM-SESSION.md**
5. **Claude reads session log**, marks claims ✅ VERIFIED in 01-VERIFIED-RESEARCH.md
6. **Script-writer-v2 reads verified research**, writes from verified facts only

**Why manual?**

- NotebookLM has no API (confirmed Jan 2026)
- Browser automation brittle (frequent UI changes)
- Copy-paste faster than automation for 20-30 queries per video
- User needs to evaluate source quality anyway

**Where automation helps:**

- Generate optimal prompts for specific source types
- Parse copied NotebookLM output into structured format
- Cross-reference verified claims against VERIFIED-CLAIMS-DATABASE.md
- Detect gaps in verification (LOW confidence items)

### Workflow Optimization Points

**Point 1: Source Upload Prep**
- `/sources --notebooklm-prep` generates source list with naming convention
- Identifies optimal sections to upload (not entire 500-page books)
- Suggests organization strategy (primary sources notebook, academic sources notebook)

**Point 2: Targeted Prompt Generation**
- `/sources --notebooklm-prompts` reads preliminary research, generates specific queries
- Customizes prompts by video type (territorial dispute needs treaty excerpts, myth-busting needs historiographical review)
- Outputs copy-paste ready prompts

**Point 3: Verification Parsing**
- User copies NotebookLM output to 02-NOTEBOOKLM-SESSION.md
- `/sources --parse-session` reads session log, extracts verified claims with page numbers
- Updates 01-VERIFIED-RESEARCH.md with ✅ marks

**Point 4: Gap Detection**
- Before script writing, `/verify --pre-script` scans research for LOW confidence items
- Generates additional NotebookLM prompts for gaps
- Blocks script writing until 90%+ verified

### Why This Pattern Works

**Accepts the constraint:** No API means manual steps. Optimize manual workflow instead of fighting it.

**Reduces cognitive load:** Claude generates prompts, user just runs them. No "what should I ask NotebookLM?"

**Maintains verification rigor:** Copy-paste forces user to read findings, evaluate source quality, check citations.

**Integrates seamlessly:** Fits into existing `/sources` command, uses existing research file structure.

### Implementation Approach

1. Expand NOTEBOOKLM-SCRIPTWRITING-PROMPTS.md from 5 to 15+ use cases
2. Create NOTEBOOKLM-RESEARCH-WORKFLOW.md template
3. Add `--notebooklm-prompts` flag to `/sources` command
4. Add 02-NOTEBOOKLM-SESSION.md to project templates
5. Test on next 2 videos, refine based on friction points

---

## Cross-Feature Integration

### How Features Connect

**Discovery → Research → NotebookLM → Script Quality**

```
1. DISCOVERY PHASE
   User: /discover --keywords "medieval literacy rates"
   Output: Keywords, competition, recommended angle
   Saves to: PROJECT-STATUS.md "Discovery findings"

2. RESEARCH PHASE
   User: /research --new "Medieval Literacy Myth"
   Reads: Discovery findings (if exist)
   Creates: Project folder, source list, NotebookLM prompt templates

3. NOTEBOOKLM PHASE
   User uploads sources to NotebookLM
   User: /sources --notebooklm-prompts
   Claude generates: 15 targeted prompts
   User runs prompts, copies findings to 02-NOTEBOOKLM-SESSION.md
   User: /sources --parse-session
   Claude updates: 01-VERIFIED-RESEARCH.md with ✅ claims

4. SCRIPT QUALITY PHASE
   User: /script --new
   script-writer-v2 reads: Verified research only
   Applies: Enhanced quality gates from STYLE-GUIDE.md
   Produces: Better first draft with fewer revision cycles
   User: /script --review
   Claude validates: Quality checklist, suggests improvements
```

### Shared Data Structures

**PROJECT-STATUS.md tracks progression:**
```markdown
## Discovery Findings
- Top keywords: [...] (from /discover)
- Competition level: Low (from discovery.py)
- Recommended angle: [...] (from title_optimizer.py)

## Research Status
- Sources uploaded to NotebookLM: 15/20
- Verified claims: 45/50 (90% - ready for scripting)
- NotebookLM session: Complete (see _research/02-NOTEBOOKLM-SESSION.md)

## Script Status
- First draft quality score: 8/10 (from /script --review)
- Revision needed: Minor (spoken delivery polish)
```

### Quality Feedback Loop

**Post-publish analysis informs future improvements:**

1. `/analyze VIDEO_ID` produces performance data
2. `/patterns` identifies what script patterns correlate with performance
3. Discovery tools use pattern data to recommend topics
4. Script quality improvements prioritize high-impact fixes
5. NotebookLM prompts refined based on verification bottlenecks

---

## Architecture Comparison: Alternatives Considered

### Alternative 1: Standalone Script Quality Tool

**Approach:** Build separate quality-checker outside script-writer-v2

**Pros:**
- Could be run independently on any script
- Might be faster than agent re-generation

**Cons:**
- Creates parallel system with duplicate knowledge
- User must remember to run separate tool
- Quality rules diverge from scriptwriter over time
- Adds cognitive load (when to use which tool?)

**Verdict:** ❌ Rejected. Violates single-source-of-truth principle.

### Alternative 2: VidIQ API Integration

**Approach:** Integrate VidIQ for keyword research and title optimization

**Pros:**
- VidIQ has excellent keyword data
- Already using VidIQ Pro subscription

**Cons:**
- VidIQ has no public API (confirmed via research)
- Would require web scraping (brittle, against ToS)
- Adds external dependency and failure point

**Verdict:** ❌ Rejected. Technical constraint (no API) makes this infeasible.

### Alternative 3: NotebookLM Browser Automation

**Approach:** Use Playwright/Selenium to automate NotebookLM queries

**Pros:**
- Could eliminate manual copy-paste steps
- Might seem more "automated"

**Cons:**
- Brittle (breaks with every UI change)
- Requires headless browser infrastructure
- Slower than manual for 20-30 queries
- User still needs to evaluate source quality
- Violates ToS (potentially)

**Verdict:** ❌ Rejected. Manual workflow faster and more reliable for this use case.

### Alternative 4: All-New Discovery Command Suite

**Approach:** Create 5 separate commands for discovery (/keywords, /titles, /competition, /trends, /optimize)

**Pros:**
- Very granular control
- Each tool does one thing well

**Cons:**
- Too many commands to remember
- Fragments workflow (user must remember sequence)
- Doesn't match existing pattern (single command with flags)

**Verdict:** ❌ Rejected. Violates "simplify workflow" principle from v1.0.

---

## Implementation Roadmap

### Phase 1: Script Quality Foundation (Week 1)

**Goal:** Produce better first drafts with fewer revisions

**Tasks:**
1. Enhance STYLE-GUIDE.md with quality patterns (2 hours)
2. Update script-writer-v2 with quality gates (4 hours)
3. Add `--quality-gate` flag to `/script` command (1 hour)
4. Test on 3 existing scripts, measure revision reduction (2 hours)

**Success metric:** 30% reduction in revision cycles (currently ~3 rounds, target ~2 rounds)

**Files changed:**
- `.claude/REFERENCE/STYLE-GUIDE.md` (add Quality Patterns section)
- `.claude/agents/script-writer-v2.md` (add quality gates)
- `.claude/commands/script.md` (add flag)

### Phase 2: Discovery Tools (Week 2)

**Goal:** Research topics systematically, optimize for discovery

**Tasks:**
1. Create `tools/youtube-analytics/discovery.py` (6 hours)
2. Create `tools/youtube-analytics/title_optimizer.py` (4 hours)
3. Create `.claude/commands/discover.md` (2 hours)
4. Test on 5 topics (2 successful, 3 hypothetical) (3 hours)

**Success metric:** Discovery recommendations match VidIQ Pro manual analysis 80%+ of time

**Files changed:**
- `tools/youtube-analytics/discovery.py` (new)
- `tools/youtube-analytics/title_optimizer.py` (new)
- `.claude/commands/discover.md` (new)
- `channel-data/patterns/TOPIC-ANALYSIS.md` (enhanced)

### Phase 3: NotebookLM Integration (Week 3)

**Goal:** Streamline research-to-script pipeline

**Tasks:**
1. Expand NOTEBOOKLM-SCRIPTWRITING-PROMPTS.md to 15+ use cases (3 hours)
2. Create NOTEBOOKLM-RESEARCH-WORKFLOW.md template (2 hours)
3. Add `--notebooklm-prompts` and `--parse-session` to `/sources` (4 hours)
4. Add 02-NOTEBOOKLM-SESSION.md to project template (1 hour)
5. Test on next 2 videos, measure time savings (research phase) (4 hours)

**Success metric:** 25% reduction in research phase time (currently ~8 hours, target ~6 hours)

**Files changed:**
- `.claude/REFERENCE/NOTEBOOKLM-SCRIPTWRITING-PROMPTS.md` (expanded)
- `.claude/templates/NOTEBOOKLM-RESEARCH-WORKFLOW.md` (new)
- `.claude/commands/sources.md` (enhanced)
- `.claude/templates/_research/02-NOTEBOOKLM-SESSION.md` (new)

### Phase 4: Integration Testing (Week 4)

**Goal:** Validate end-to-end workflow improvements

**Tasks:**
1. Full workflow test: Discovery → Research → NotebookLM → Script (8 hours)
2. Measure time savings vs v1.1 baseline (2 hours)
3. Collect user friction points, refine (4 hours)
4. Document lessons learned in .planning/research/LESSONS.md (2 hours)

**Success metric:**
- Script first-draft quality: 8/10+ (vs current ~6/10)
- Research-to-script time: <2 weeks (vs current ~3 weeks)
- User reports workflow feels smoother, not more complex

---

## Technical Specifications

### Discovery Tools: API Usage

**YouTube Data API v3:**
- Search endpoint: `search.list()` with `q=keyword&type=video&maxResults=50`
- Video metadata: `videos.list()` with `id=VIDEO_IDS&part=statistics,snippet`
- Quota cost: ~105 units per keyword analysis (search 3 + videos 100 + details 2)
- Daily quota: 10,000 units = ~95 keyword analyses per day

**YouTube Autocomplete API (unofficial but stable):**
- Endpoint: `http://suggestqueries.google.com/complete/search?client=youtube&ds=yt&q={query}`
- No auth required
- Returns JSON array of suggestions
- Rate limit: ~1 request per second (be respectful)

**Data structures:**
```python
# discovery.py output
{
  'topic': 'medieval flat earth',
  'keywords': [
    {'phrase': 'medieval flat earth myth', 'volume': 'high', 'competition': 'medium'},
    {'phrase': 'did medieval people believe earth flat', 'volume': 'medium', 'competition': 'low'},
    ...
  ],
  'competition': {
    'video_count': 45,
    'top_performer_views': 125000,
    'avg_views': 8500,
    'outlier_opportunity': True  # few videos, high best performer
  },
  'recommendations': [
    'Focus on "medieval people knew earth round" (fact-first framing)',
    'Differentiate with primary sources (manuscripts, quotes)',
    'Target keywords: medieval scholars, earth spherical, Columbus myth'
  ]
}

# title_optimizer.py output
{
  'topic': 'medieval flat earth',
  'variants': [
    {
      'title': 'Medieval Scholars Knew Earth Was Spherical',
      'pattern': 'Fact-first (no clickbait)',
      'predicted_ctr': 4.2,  # based on historical data
      'channel_dna_match': 'high'
    },
    {
      'title': 'The Flat Earth Myth Medieval People Never Believed',
      'pattern': 'Myth-negation',
      'predicted_ctr': 3.8,
      'channel_dna_match': 'medium'
    },
    ...
  ],
  'test_plan': {
    'primary': 'Medieval Scholars Knew Earth Was Spherical',
    'ab_test': 'The Medieval "Flat Earth" Myth Explained',
    'test_after': '48 hours'
  }
}
```

### Script Quality: Quality Gates

**Pre-writing quality gates (enforced by script-writer-v2):**
```python
PRE_FLIGHT_CHECKLIST = [
    "Identity stake assessed (High/Medium/Low)",
    "Coverage gap checked (sufficient research in field)",
    "Both extremes identified (if debunking video)",
    "Primary sources confirmed (3+ Tier 1 sources)",
    "Steelman section planned"
]
```

**Post-writing quality gates (automatic validation):**
```python
POST_GENERATION_CHECKS = {
    'stumble_test': 'Read aloud without awkward pauses',
    'heres_count': 'Count "here\'s" - must be 2-4 (not 10+)',
    'forbidden_phrases': 'Grep for banned phrases',
    'term_definitions': 'Every technical term defined on first use',
    'fragments_valid': 'Informational fragments converted to sentences',
    'contractions_present': 'it\'s not it is, they\'re not they are'
}
```

**Quality score calculation:**
```python
def calculate_quality_score(script: str) -> dict:
    """
    Returns quality score 1-10 and specific issues.

    Scoring:
    - 9-10: Production ready, minor polish only
    - 7-8: Good, needs targeted revision (1-2 sections)
    - 5-6: Needs revision (multiple issues)
    - 1-4: Major rewrite needed
    """
    issues = {
        'critical': [],  # Must fix (forbidden phrases, unverified claims)
        'important': [],  # Should fix (awkward delivery, repetition)
        'minor': []  # Nice to fix (style preferences)
    }

    # Run checks...

    score = 10
    score -= len(issues['critical']) * 2
    score -= len(issues['important']) * 0.5
    score -= len(issues['minor']) * 0.2

    return {
        'score': max(1, min(10, score)),
        'issues': issues,
        'verdict': 'ready' if score >= 9 else 'revision_needed'
    }
```

### NotebookLM: Prompt Templates

**Structured prompt generation by video type:**

```python
PROMPT_TEMPLATES = {
    'territorial_dispute': [
        "Extract all specific boundary descriptions from {source}. Include coordinates, landmarks, and territorial extent.",
        "What legal principles does {source} cite for territorial claims? Quote exact language.",
        "Compare {source_a} and {source_b} - where do they disagree on boundaries?",
        "What were the economic stakes mentioned in {source}? Specific resources, trade routes, etc.",
        "Who were the decision-makers? Extract names, titles, and institutional affiliations from {source}."
    ],
    'myth_busting': [
        "What primary sources from the period address {myth_topic}? List all mentions with dates.",
        "How do modern historians interpret {myth}? Summarize {scholar_1}, {scholar_2}, {scholar_3}.",
        "What evidence contradicts {myth}? Extract specific examples from {source}.",
        "Why did {myth} originate? What's the historiography of this misconception?",
        "What do scholars say people ACTUALLY believed about {topic}?"
    ],
    'fact_check': [
        "Did {person} claim {statement}? Find exact quote with source and date.",
        "What's the historical consensus on {claim}? Check {source_1}, {source_2}, {source_3}.",
        "What primary sources support or contradict {claim}?",
        "What context is missing from {claim}? What happened before/after?",
        "How have historians evaluated {claim}? Any scholarly rebuttals?"
    ]
}

def generate_notebooklm_prompts(video_type: str, topic: str, sources: list) -> list:
    """
    Generate targeted NotebookLM prompts based on video type and sources.

    Returns list of copy-paste ready prompts with placeholders filled.
    """
    template = PROMPT_TEMPLATES.get(video_type, PROMPT_TEMPLATES['myth_busting'])
    prompts = []

    for prompt_template in template:
        # Fill in placeholders
        prompt = prompt_template.format(
            source=sources[0] if sources else '[SOURCE]',
            topic=topic,
            myth_topic=topic
        )
        prompts.append(prompt)

    return prompts
```

---

## Risk Assessment

### Technical Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|-----------|------------|
| YouTube API quota exhaustion | HIGH - Discovery tools stop working | LOW - 95 analyses/day is generous | Implement quota monitoring, cache results |
| YouTube autocomplete endpoint changes | MEDIUM - Keyword research less reliable | MEDIUM - Unofficial endpoint | Graceful fallback to manual keyword input |
| NotebookLM UI changes | LOW - Workflow still works, just different | HIGH - Google updates frequently | Document visual guides for current UI |
| Quality gates too strict | MEDIUM - Blocks script progress | MEDIUM - Hard to calibrate | Make gates configurable with `--strict` flag |

### Workflow Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|-----------|------------|
| Discovery tools recommend bad topics | HIGH - Wasted research effort | MEDIUM - Algorithm isn't perfect | Human validation required (don't auto-create projects) |
| NotebookLM integration adds friction | HIGH - Slows down instead of speeds up | LOW - Careful design | Test on 2 videos before full rollout |
| Script quality gates feel bureaucratic | MEDIUM - User bypasses them | MEDIUM - Perception issue | Make gates helpful, not punitive (suggest fixes, don't block) |
| Too many new commands | HIGH - Cognitive overload | LOW - Only 1 new command | Integrate into existing commands where possible |

### Scope Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|-----------|------------|
| Feature creep (trying to automate too much) | HIGH - Timeline slips, complexity explodes | MEDIUM - Common trap | Stick to manual workflow optimization for NotebookLM |
| Over-engineering discovery tools | MEDIUM - Diminishing returns | MEDIUM - Easy to add "nice to have" features | Start minimal, add based on user feedback |
| Script quality becomes AI cargo cult | LOW - Quality improves but for wrong reasons | LOW - User is sophisticated | Focus on spoken delivery and verification, not style rules |

---

## Success Metrics

### Script Quality

**Baseline (v1.1):**
- First draft quality: ~6/10 (usually needs 3 revision rounds)
- Common issues: Telegraph-style fragments, overuse of "here's", unnatural delivery
- Time to filming-ready script: ~2-3 days after research complete

**Target (v1.2):**
- First draft quality: 8/10+ (1-2 revision rounds max)
- Common issues reduced by 70%
- Time to filming-ready script: ~1 day after research complete

**Measurement:**
- Quality score from `/script --review` on first draft
- Count of revision cycles before `--teleprompter` export
- User-reported "feels like less rework"

### Discovery Tools

**Baseline (v1.1):**
- Topic research: Manual VidIQ browsing, ad-hoc keyword checking
- No systematic competition analysis
- Title optimization based on gut feel

**Target (v1.2):**
- Keyword research: 15-20 analyzed keywords per topic in <10 minutes
- Competition analysis: Automated view distribution, outlier detection
- Title optimization: 5 variants generated with CTR predictions

**Measurement:**
- Time to complete topic research (target: <30 minutes)
- Discovery recommendation accuracy vs VidIQ manual analysis (target: 80%+)
- Title variant CTR performance (A/B test 5 videos)

### NotebookLM Integration

**Baseline (v1.1):**
- Research phase time: ~8 hours per video
- Common friction: "What should I ask NotebookLM?"
- Verification incomplete (some claims marked ✅ without page numbers)

**Target (v1.2):**
- Research phase time: ~6 hours per video (25% reduction)
- Targeted prompts eliminate "what to ask" friction
- 95%+ of ✅ claims have page number citations

**Measurement:**
- Time from source upload to 90% verified (tracked in PROJECT-STATUS.md)
- Count of LOW confidence items at script-writing gate
- User-reported friction points in research phase

---

## Open Questions

### Discovery Tools

**Q: Should discovery tools auto-create project folders?**
**A:** No. Discovery should inform, not decide. User validates findings before running `/research --new`.

**Q: How to handle niches where YouTube autocomplete has no data?**
**A:** Fall back to manual keyword list + competition analysis. Tool provides value even without autocomplete.

**Q: Should title optimizer consider A/B test history across channel?**
**A:** Yes, but v1.2 starts with pattern matching only. v1.3 could add cross-video A/B learning.

### Script Quality

**Q: Should quality gates block script generation or just warn?**
**A:** Warn by default, block with `--strict` flag. Give user control.

**Q: How to avoid quality rules becoming cargo cult (following rules without understanding)?**
**A:** Every rule in STYLE-GUIDE.md must include "why" explanation. Rules serve spoken delivery, not arbitrary style preferences.

**Q: Should script quality improvements apply to existing scripts retroactively?**
**A:** Optional. Add `/script --upgrade-quality` flag to apply new rules to old scripts. Don't force.

### NotebookLM Integration

**Q: What if NotebookLM releases an API?**
**A:** Retrofit existing prompt generation system to call API instead of generating copy-paste templates. Architecture supports this.

**Q: Should session logs be AI-parseable or human-maintained?**
**A:** Both. Human copies findings to 02-NOTEBOOKLM-SESSION.md, Claude parses for verification status updates.

**Q: How to handle when sources disagree?**
**A:** Flag in session log, present both positions in script with "Source A says X, Source B says Y" structure. Don't hide contradictions.

---

## Sources

**Existing Codebase Analysis:**
- `.claude/commands/` (12 slash commands)
- `tools/youtube-analytics/` (10 Python scripts, ~5,000 lines)
- `.claude/agents/script-writer-v2.md` (1,203 lines, comprehensive rule system)
- `.claude/REFERENCE/STYLE-GUIDE.md` (559 lines, authoritative style reference)

**External Research:**

**YouTube SEO Tools (2026):**
- [vidIQ Features](https://vidiq.com/features/keyword-tools/) - Keyword research for YouTube creators
- [Ahrefs YouTube Keyword Tool](https://ahrefs.com/youtube-keyword-tool) - Free keyword ideas for 171 countries
- [YouTube SEO Best Practices 2026](https://www.learningrevolution.net/youtube-seo/) - Complete optimization guide
- [Top YouTube Keyword Research Tools 2026](https://prettyinsights.com/best-youtube-keyword-research-tools/) - Tool comparison

**NotebookLM for Content Creators:**
- [NotebookLM Research Workflow 2026](https://www.geeky-gadgets.com/notebooklm-research-upgrade-2026/) - Automation features
- [Deep Research Workflow Guide](https://medium.com/@ferreradaniel/how-to-use-notebooklm-better-than-99-of-people-deep-research-workflow-guide-4e54199c9f82) - Advanced techniques
- [NotebookLM for YouTube Content Creation](https://medium.com/aimonks/from-research-notes-to-revenue-how-notebooklm-transforms-youtube-content-creation-in-2026-d283abdd73cd) - 2026 content workflow
- [NotebookLM Complete Guide 2026](https://www.geeky-gadgets.com/notebooklm-complete-guide-2026/) - Work and study applications
- [NotebookLM Evolution 2023-2026](https://medium.com/@jimmisound/the-cognitive-engine-a-comprehensive-analysis-of-notebooklms-evolution-2023-2026-90b7a7c2df36) - Platform development

---

*Architecture research complete. Ready for implementation planning.*
