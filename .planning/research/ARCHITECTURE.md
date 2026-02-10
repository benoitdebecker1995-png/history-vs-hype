# Architecture Research: v2.0 Channel Intelligence Integration

**Domain:** YouTube content production workspace — channel-aware AI features
**Researched:** 2026-02-09
**Confidence:** HIGH (existing codebase analysis complete)

## Integration Context

**Problem:** v1.0-v1.6 built ~17K lines of tooling, but outputs don't match production needs. Script generation is generic, research tools and NotebookLM are disconnected, analytics show data without actionable next steps.

**Solution:** Three channel-aware features that integrate with existing architecture:
1. **Channel-aware script generation** — voice/style data into script-writer-v2 agent
2. **Research-to-NotebookLM bridge** — tools connect with manual NotebookLM workflow
3. **Actionable analytics** — retention patterns mapped to script sections

**Critical constraint:** NotebookLM has NO API — all integration must support manual upload/download workflow.

---

## Existing Architecture (v1.6 Baseline)

### System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      CONFIGURATION LAYER                         │
│  .claude/ (agents, commands, reference docs, templates)         │
├─────────────────────────────────────────────────────────────────┤
│                        COMMAND LAYER                             │
│  14 slash commands (research, script, prep, publish, etc.)      │
├─────────────────────────────────────────────────────────────────┤
│                         AGENT LAYER                              │
│  6 specialized agents (script-writer-v2, fact-checker, etc.)    │
├─────────────────────────────────────────────────────────────────┤
│                        TOOL LAYER                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ youtube-     │  │ script-      │  │ discovery/   │          │
│  │ analytics/   │  │ checkers/    │  │              │          │
│  │ (~12.3K LOC) │  │ (~3.2K LOC)  │  │ (~1.8K LOC)  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐                                                │
│  │ production/  │                                                │
│  │ (~2.1K LOC)  │                                                │
│  └──────────────┘                                                │
├─────────────────────────────────────────────────────────────────┤
│                        DATA LAYER                                │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ keywords.db (SQLite) — PRAGMA user_version = 27          │   │
│  │ - keywords, opportunities, video_performance             │   │
│  │ - thumbnail_variants, title_variants, ctr_snapshots      │   │
│  │ - video_feedback, what_worked, what_failed               │   │
│  └──────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ video-projects/ (markdown-first project folders)         │   │
│  │ - _IN_PRODUCTION/, _READY_TO_FILM/, _ARCHIVED/           │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Existing Component Responsibilities

| Component | Responsibility | Implementation |
|-----------|----------------|----------------|
| **keywords.db** | Central data store with auto-migration | SQLite + PRAGMA user_version pattern |
| **youtube-analytics/** | Performance tracking, CTR, feedback, retention | Python modules with error dict pattern |
| **script-checkers/** | Quality checks (pacing, flow, repetition, voice) | Python modules with configurable thresholds |
| **discovery/** | Topic research, competition analysis, recommendations | Python modules with database integration |
| **production/** | Script parsing, B-roll generation, metadata, teleprompter | Python parser module |
| **.claude/agents/** | Specialized AI agents for complex tasks | Markdown configs with frontmatter |
| **.claude/commands/** | Slash command entry points | YAML frontmatter + markdown |
| **.claude/REFERENCE/** | Style guides, workflow docs | Markdown reference files (STYLE-GUIDE.md primary) |

### Existing Patterns

**1. Error Dict Pattern** (universal across all tools):
```python
# NEVER raise exceptions
# Always return {'error': msg} on failure
def some_function():
    if problem:
        return {'error': 'Description of problem'}
    return {'status': 'success', 'data': results}
```

**2. Auto-Migration Pattern** (keywords.db):
```python
# PRAGMA user_version = 27
# Auto-detect schema version and migrate on connection
def _ensure_connection(self):
    if cursor.fetchone() is None:
        self.init_database()
    else:
        self._ensure_classification_columns()  # Phase 16
        self._ensure_production_columns()      # Phase 17
        self._ensure_variant_tables()          # Phase 27
```

**3. Feature Flag Pattern** (optional dependencies):
```python
# Graceful degradation when modules unavailable
try:
    from variants import register_variant
    VARIANTS_AVAILABLE = True
except ImportError:
    VARIANTS_AVAILABLE = False

# Later in code
if VARIANTS_AVAILABLE:
    display_variant_data()
```

**4. Reference Hierarchy Pattern** (agent context):
```
Tier 1 (MANDATORY): Read for every invocation
  - .claude/REFERENCE/STYLE-GUIDE.md (single source of truth)
  - .claude/templates/[TASK]-TEMPLATE.md

Tier 2 (AS NEEDED): Reference when relevant
  - .claude/REFERENCE/OPENING-HOOK-TEMPLATES.md
  - .claude/REFERENCE/creator-techniques.md
```

**5. Single Source of Truth Pattern** (verified research):
```
Per-project: video-projects/.../01-VERIFIED-RESEARCH.md
Cross-project: .claude/VERIFIED-CLAIMS-DATABASE.md
Quality gate: Can't write script until 90% claims verified
```

---

## v2.0 Integration Architecture

### Feature 1: Channel-Aware Script Generation

**Goal:** Script-writer-v2 agent outputs sound like creator's voice, integrate verified research automatically.

#### New Components

**NONE** — Pure reference document expansion.

#### Modified Components

| Component | Modification | Why |
|-----------|--------------|-----|
| **.claude/REFERENCE/STYLE-GUIDE.md** | Add Part 6: Voice Patterns (sentence structures, causal chain templates, phrase library) | Agent already reads this — no code changes |
| **.claude/REFERENCE/CREATOR-PHRASE-LIBRARY.md** | Expand with copy-paste natural language extracted from transcripts | Existing reference file, add corpus |
| **.claude/agents/script-writer-v2.md** | Update Tier 1 references to include new voice pattern sections | Agent config update only |

#### Data Flow

```
Existing:
  script-writer-v2 reads STYLE-GUIDE.md
    ↓
  Writes script to 02-SCRIPT-DRAFT.md

v2.0 Enhancement:
  script-writer-v2 reads STYLE-GUIDE.md (now with voice patterns)
    ↓
  Applies sentence structure templates from Part 6
    ↓
  Uses phrase library for natural transitions
    ↓
  Writes script matching creator voice to 02-SCRIPT-DRAFT.md
```

**Integration points:**
- Agent invocation: UNCHANGED (still reads STYLE-GUIDE.md)
- Output format: UNCHANGED (still writes markdown script)
- Quality checks: Existing voice_checker.py validates output

**Build order:**
1. Extract voice patterns from existing transcripts (corpus analysis)
2. Document patterns in STYLE-GUIDE.md Part 6 (reference expansion)
3. Update script-writer-v2 frontmatter to emphasize Part 6 (config update)
4. Test with existing `/script` command (no tool changes needed)

---

### Feature 2: Research-to-NotebookLM Bridge

**Goal:** Tools prepare sources for NotebookLM upload, extract verified research back into 01-VERIFIED-RESEARCH.md.

**Critical constraint:** NotebookLM has NO API. All integration is manual upload/download with tool assistance.

#### New Components

| Component | Purpose | Location |
|-----------|---------|----------|
| **notebooklm_bridge.py** | Generate source list from keywords, create upload checklist, parse NotebookLM output | tools/research/ |
| **citation_extractor.py** | Extract page numbers and quotes from NotebookLM responses | tools/research/ |

#### Modified Components

| Component | Modification | Why |
|-----------|--------------|-----|
| **/sources command** | Add --notebooklm-prep flag to generate NOTEBOOKLM-SOURCE-LIST.md | Entry point for bridge |
| **.claude/REFERENCE/NOTEBOOKLM-SOURCE-STANDARDS.md** | Add workflow section for bridge usage | User guidance |

#### Data Flow (Manual Steps Explicit)

```
Phase 1: Source Preparation
  User runs: /sources --notebooklm-prep
    ↓
  notebooklm_bridge.generate_source_list(topic, keywords)
    ↓
  Writes: NOTEBOOKLM-SOURCE-LIST.md
    - Recommended books (university press titles)
    - Where to find (JSTOR, Internet Archive, buy links)
    - Upload checklist [ ] Book 1, [ ] Book 2...

Phase 2: Manual Upload (USER ACTION)
  User downloads PDFs
    ↓
  User uploads to NotebookLM
    ↓
  User runs NotebookLM queries
    ↓
  User saves NotebookLM responses to local files

Phase 3: Extract Verified Research
  User runs: /sources --extract-citations NOTEBOOKLM-RESPONSE.txt
    ↓
  citation_extractor.parse_response(file)
    ↓
  Extracts:
    - Exact quotes with page numbers
    - Source attribution
    - Confidence markers
    ↓
  Writes: 01-VERIFIED-RESEARCH.md (formatted entries)
```

**Integration points:**
- Entry: `/sources` command with new flags
- Output: Markdown files (SOURCE-LIST, VERIFIED-RESEARCH)
- No database changes (markdown-first pattern)

**Build order:**
1. Create tools/research/ directory
2. Build notebooklm_bridge.py (source list generator)
3. Build citation_extractor.py (response parser)
4. Add --notebooklm-prep and --extract-citations flags to /sources
5. Document workflow in NOTEBOOKLM-SOURCE-STANDARDS.md

---

### Feature 3: Actionable Analytics

**Goal:** Retention patterns mapped to specific script sections, concrete next steps from data.

#### New Components

| Component | Purpose | Location |
|-----------|---------|----------|
| **retention_mapper.py** | Map retention drop points to script sections | tools/youtube-analytics/ |
| **insights_generator.py** | Generate actionable recommendations from patterns | tools/youtube-analytics/ |

#### Modified Components

| Component | Modification | Why |
|-----------|--------------|-----|
| **analyze.py** | Add retention section mapping, integrate insights generation | Enhance existing orchestrator |
| **feedback_queries.py** | Add get_actionable_insights() method | Query interface expansion |
| **/analyze command** | Add --actionable flag for insights-first output | CLI entry point |

#### Data Flow

```
Existing v1.6:
  analyze.py fetches retention curve
    ↓
  Displays drop points as timestamps
    ↓
  User manually correlates to script

v2.0 Enhancement:
  analyze.py fetches retention curve
    ↓
  retention_mapper.map_to_sections(script_path, drop_points)
    ↓
  Identifies: "30% drop at Section 3 (Historical Background)"
    ↓
  insights_generator.generate_recommendations(section, patterns)
    ↓
  Outputs:
    - "Add modern relevance hook at 4:20"
    - "Entity density 35% (threshold 25%) — add explanatory sentence"
    - "Similar videos with <30s hooks retained 42% vs 28%"
```

**Integration points:**
- Existing: analyze.py orchestrator, feedback database
- New: Section mapping logic, recommendation engine
- Output: Enhanced markdown report with actionable section

**Database changes:**

```sql
-- No new tables needed
-- Use existing: video_feedback, what_worked, what_failed
-- Queries join retention data + script sections + past patterns
```

**Build order:**
1. Create retention_mapper.py (section correlation logic)
2. Create insights_generator.py (recommendation templates)
3. Extend feedback_queries.py with actionable insights method
4. Modify analyze.py to integrate mapping + insights
5. Add --actionable flag to /analyze command
6. Update POST-PUBLISH-ANALYSIS template with insights section

---

## Integration Points Summary

### New Components Needed

| Component | Lines Est. | Purpose | Dependencies |
|-----------|------------|---------|--------------|
| tools/research/notebooklm_bridge.py | ~300 | Generate source lists | None |
| tools/research/citation_extractor.py | ~200 | Parse NotebookLM output | None |
| tools/youtube-analytics/retention_mapper.py | ~250 | Map retention to sections | production/parser.py |
| tools/youtube-analytics/insights_generator.py | ~200 | Generate recommendations | feedback_queries.py |

**Total new code:** ~950 lines (5% of existing codebase)

### Modified Components

| Component | Change Type | Impact |
|-----------|-------------|--------|
| .claude/REFERENCE/STYLE-GUIDE.md | Content expansion (Part 6) | HIGH (affects script quality) |
| .claude/REFERENCE/CREATOR-PHRASE-LIBRARY.md | Corpus expansion | MEDIUM |
| .claude/commands/sources.md | Add 2 flags | LOW (backward compatible) |
| .claude/commands/analyze.md | Add 1 flag | LOW (backward compatible) |
| .claude/agents/script-writer-v2.md | Reference update | LOW (config only) |
| tools/youtube-analytics/analyze.py | Add mapping + insights | MEDIUM (existing orchestrator) |
| tools/youtube-analytics/feedback_queries.py | Add insights method | LOW (extends existing API) |

### NO Changes Required

- Database schema (v27 sufficient)
- Existing tool modules (youtube-analytics, script-checkers, discovery)
- Slash command infrastructure
- Agent invocation mechanism
- Error dict pattern
- Auto-migration pattern
- Feature flag pattern

---

## Recommended Build Order

### Phase A: Voice Patterns (Channel-Aware Scripts)
**Goal:** Script outputs match creator voice
**Risk:** LOW (no tool changes, only reference docs)
**Effort:** 3-5 hours

1. Extract voice patterns from existing transcripts
   - Analyze sentence structures (Kraut causal chains)
   - Build phrase library (Alex O'Connor transitions)
   - Document patterns in STYLE-GUIDE.md Part 6
2. Update script-writer-v2.md frontmatter
3. Test with `/script` command on existing project
4. Validate with voice_checker.py

**Success criteria:** Script output uses documented patterns, passes voice checks

---

### Phase B: NotebookLM Bridge (Research Integration)
**Goal:** Tools assist manual NotebookLM workflow
**Risk:** MEDIUM (new module, manual workflow dependency)
**Effort:** 6-8 hours

1. Create tools/research/ directory
2. Build notebooklm_bridge.py
   - generate_source_list(topic, keywords)
   - create_upload_checklist(sources)
   - Returns markdown formatted list
3. Build citation_extractor.py
   - parse_response(text) → extract quotes + page numbers
   - format_for_verified_research(citations)
   - Returns markdown formatted entries
4. Extend /sources command
   - Add --notebooklm-prep flag (calls bridge.generate_source_list)
   - Add --extract-citations flag (calls extractor.parse_response)
5. Document workflow in NOTEBOOKLM-SOURCE-STANDARDS.md
6. Test with real NotebookLM session

**Success criteria:** Source list generates, citations extract correctly, manual workflow smooth

---

### Phase C: Actionable Analytics (Retention Mapping)
**Goal:** Analytics provide concrete script fixes
**Risk:** MEDIUM (depends on script section parsing accuracy)
**Effort:** 8-10 hours

1. Build retention_mapper.py
   - map_to_sections(script_path, retention_data)
   - Correlate timestamps to script sections
   - Return section-level drop analysis
2. Build insights_generator.py
   - generate_recommendations(section, patterns, feedback_db)
   - Query past patterns for similar topics
   - Return actionable fixes with specificity
3. Extend feedback_queries.py
   - Add get_actionable_insights(video_id)
   - Join retention + sections + patterns
4. Modify analyze.py
   - Integrate retention_mapper after fetching curve
   - Call insights_generator for recommendations
   - Add insights section to markdown output
5. Add --actionable flag to /analyze command
6. Test with video that has retention data

**Success criteria:** Drop points map to script sections, recommendations are specific and actionable

---

## Architectural Patterns Followed

### Pattern 1: Markdown-First Data Flow

**What:** Reference documents and project files are primary data store, not database.

**Where used:**
- Voice patterns → STYLE-GUIDE.md
- Source lists → NOTEBOOKLM-SOURCE-LIST.md
- Verified research → 01-VERIFIED-RESEARCH.md

**Why:** Matches existing architecture (document-driven content production pipeline).

**Trade-offs:**
- ✅ No schema changes needed
- ✅ Human-readable and versionable (git)
- ❌ Harder to query programmatically
- ✅ But: Tools generate markdown, agents read markdown (existing pattern)

---

### Pattern 2: Tool-Assisted Manual Workflow

**What:** Tools prepare and parse, human does the critical work.

**Where used:** NotebookLM bridge (no API, must be manual).

**Why:** Reflects reality — NotebookLM has no API, waiting for Enterprise version.

**Trade-offs:**
- ✅ Works today (no API blockers)
- ✅ Human verifies quality (academic sources)
- ❌ Not fully automated
- ✅ But: Tools reduce friction (source lists, citation extraction)

**Example:**
```
Manual step: Download PDFs and upload to NotebookLM
Tool assists: Generate list of WHICH PDFs to get and WHERE
Manual step: Run NotebookLM queries
Tool assists: Parse output into VERIFIED-RESEARCH.md format
```

---

### Pattern 3: Extend, Don't Replace

**What:** Add capabilities to existing components rather than rewriting.

**Where used:**
- analyze.py gets retention mapping (doesn't replace existing metrics)
- feedback_queries.py gets insights method (doesn't replace existing queries)
- STYLE-GUIDE.md gets Part 6 (doesn't invalidate existing parts)

**Why:** Preserves v1.6 functionality, reduces regression risk.

**Trade-offs:**
- ✅ Backward compatible
- ✅ Existing workflows unaffected
- ❌ Component complexity increases
- ✅ But: Complexity is managed (feature flags, optional parameters)

---

### Pattern 4: Reference Hierarchy Over Code Logic

**What:** Encode knowledge in reference documents, not hard-coded rules.

**Where used:**
- Voice patterns in STYLE-GUIDE.md (not Python rules)
- Phrase library in markdown (not code templates)
- Source standards in NOTEBOOKLM-SOURCE-STANDARDS.md (not validator rules)

**Why:** Easier to update without code changes, agents read naturally.

**Trade-offs:**
- ✅ Non-technical editing (markdown)
- ✅ Agents already read reference docs
- ❌ Harder to enforce programmatically
- ✅ But: Quality checks validate (voice_checker.py, fact-checker)

---

## Scaling Considerations

| Scale | Current (v1.6) | v2.0 Changes | Architecture Adjustments |
|-------|----------------|--------------|--------------------------|
| **15 videos** | Works fine | All features functional | None needed |
| **50 videos** | Pattern analysis improves with data | Insights more accurate | Consider feedback database indexing |
| **100+ videos** | Database queries slow | Retention mapping at scale | Add section-level retention cache table |

### Scaling Priorities

**1. First bottleneck: Retention mapping at 50+ videos**
- Current: O(n) script parsing on every /analyze call
- Fix: Cache section boundaries in database (new table: script_sections)
- When: After 40-50 published videos

**2. Second bottleneck: Voice pattern corpus at 100+ transcripts**
- Current: Manual extraction from transcripts
- Fix: Automated pattern detection using spaCy
- When: When manual corpus exceeds 100 examples

**3. Not a bottleneck: Reference document size**
- STYLE-GUIDE.md can grow to 10K+ lines
- Agents handle large context (Claude Opus 200K tokens)
- No action needed

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Trying to Automate NotebookLM Workflow

**What people might do:** Build scraper to auto-download NotebookLM responses.

**Why it's wrong:** NotebookLM has no API, scraping violates ToS, manual verification is the quality gate.

**Do this instead:** Build tools that assist manual steps (source lists, citation extraction), accept human-in-loop.

---

### Anti-Pattern 2: Hard-Coding Voice Patterns in Script Generator

**What people might do:** Add Python logic like "if sentence_type == 'causal': insert 'consequently'"

**Why it's wrong:** Agent already reads reference docs, hard-coding creates two sources of truth, harder to update.

**Do this instead:** Document patterns in STYLE-GUIDE.md, let agent apply naturally, validate with voice_checker.py.

---

### Anti-Pattern 3: Creating New Database Tables for Voice Patterns

**What people might do:** Store sentence templates in keywords.db.

**Why it's wrong:** Reference documents are primary data store (existing pattern), agents don't query databases directly.

**Do this instead:** Keep patterns in markdown, version control with git, agents read files.

---

### Anti-Pattern 4: Building "Smart" Retention Predictor

**What people might do:** ML model to predict retention from script features.

**Why it's wrong:** ~15 videos insufficient for training, prediction creates false confidence, actionable insights > predictions.

**Do this instead:** Pattern matching from past videos (descriptive), concrete recommendations based on what worked.

---

## Integration Testing Strategy

### Test 1: Voice Pattern Application
**Input:** Existing script without voice patterns
**Process:** Run `/script` with enhanced STYLE-GUIDE.md
**Expected:** Output uses documented patterns (causal chains, phrase library)
**Validation:** voice_checker.py passes, manual review confirms style match

### Test 2: NotebookLM Bridge End-to-End
**Input:** Topic "Treaty of Tordesillas" + keywords
**Process:**
1. Run `/sources --notebooklm-prep`
2. Manually download suggested PDFs
3. Upload to NotebookLM
4. Run queries, save responses
5. Run `/sources --extract-citations RESPONSE.txt`
**Expected:** SOURCE-LIST.md generated, citations extracted to VERIFIED-RESEARCH.md format
**Validation:** Citations have page numbers, sources match SOURCE-LIST

### Test 3: Retention Mapping
**Input:** Video with retention data + script file
**Process:** Run `/analyze VIDEO_ID --actionable`
**Expected:** Retention drops mapped to sections, recommendations specific
**Validation:** Section correlations accurate (±30s), recommendations reference past patterns

---

## Dependencies and Constraints

### External Dependencies

| Dependency | Current Version | v2.0 Impact |
|------------|-----------------|-------------|
| Python | 3.11-3.13 | No change (avoid 3.14 for spaCy) |
| spaCy | 3.x | No change (existing for stumble checker) |
| SQLite | 3.x | No change (schema v27 sufficient) |
| YouTube Analytics API | v2 | No change (existing integration) |
| NotebookLM | Web UI (no API) | Manual workflow dependency |

### Internal Dependencies

| Component | Depends On | v2.0 Change |
|-----------|------------|-------------|
| retention_mapper.py | production/parser.py | NEW dependency (section parsing) |
| insights_generator.py | feedback_queries.py | NEW dependency (pattern queries) |
| citation_extractor.py | None | Standalone (text parsing) |
| notebooklm_bridge.py | None | Standalone (markdown generation) |

### Constraints

**1. NotebookLM Has No API**
- Impact: All integration must support manual upload/download
- Mitigation: Tool-assisted workflow, not automation

**2. Small Dataset (~15 Videos)**
- Impact: Pattern analysis limited, no ML predictions
- Mitigation: Descriptive patterns only, no predictive models

**3. Solo Creator Workflow**
- Impact: Tools must be single-user friendly
- Mitigation: CLI-based, no collaboration features needed

**4. Backward Compatibility Required**
- Impact: Can't break existing v1.6 workflows
- Mitigation: Feature flags, optional parameters, extend not replace

---

## Sources

**Architecture Patterns:**
- [Python CLI Design Patterns](https://cli-guide.readthedocs.io/en/latest/design/patterns.html)
- [Things I've learned about building CLI tools in Python](https://simonwillison.net/2023/Sep/30/cli-tools-python/)
- [SQLite DB Migrations with PRAGMA user_version](https://levlaz.org/sqlite-db-migrations-with-pragma-user_version/)
- [Simple declarative schema migration for SQLite](https://david.rothlis.net/declarative-schema-migration-for-sqlite/)

**Existing Codebase:**
- .planning/codebase/ARCHITECTURE.md (v1.6 baseline)
- tools/youtube-analytics/analyze.py (orchestrator pattern)
- tools/discovery/database.py (auto-migration pattern)
- .claude/agents/script-writer-v2.md (reference hierarchy)
- .claude/REFERENCE/STYLE-GUIDE.md (single source of truth)

---

*Architecture research for: v2.0 Channel Intelligence Integration*
*Researched: 2026-02-09*
