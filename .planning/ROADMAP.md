# Roadmap: History vs Hype Workspace

## Milestones

- **v1.0 MVP** - Phases 1-7 (shipped 2026-01-19)
- **v1.1 Analytics & Learning Loop** - Phases 8-10 (shipped 2026-01-26)
- **v1.2 Script Quality & Discovery** - Phases 11-14 (shipped 2026-01-30)
- **v1.3 Niche Discovery** - Phases 15-18 (in progress)

## Phases

<details>
<summary>v1.0 MVP (Phases 1-7) - SHIPPED 2026-01-19</summary>

### Phase 1: File Cleanup
**Goal**: Remove redundant files and establish clean baseline
**Plans**: 3 plans

Plans:
- [x] 01-01: Identify deprecated files and folder sprawl
- [x] 01-02: Archive duplicates and consolidate scattered docs
- [x] 01-03: Create canonical structure documentation

### Phase 2: Style Consolidation
**Goal**: Single authoritative style guide
**Plans**: 2 plans

Plans:
- [x] 02-01: Merge style fragments into STYLE-GUIDE.md
- [x] 02-02: Extract creator patterns from transcripts

### Phase 3: Research Structure
**Goal**: Organized research with verified facts database
**Plans**: 3 plans

Plans:
- [x] 03-01: Design verified research workflow
- [x] 03-02: Create VERIFIED-CLAIMS-DATABASE.md
- [x] 03-03: Template NotebookLM session logs

### Phase 4: Workflow Simplification (DEFERRED)
**Goal**: Fewer commands, better discovery
**Status**: Deferred to after slash command implementation

### Phase 5: Competitive Intelligence
**Goal**: Track what works in the niche
**Plans**: Not executed (covered by Phase 6)

### Phase 6: Pattern Extraction
**Goal**: Extract working patterns from competitors
**Plans**: 1 plan

Plans:
- [x] 06-01: Build title database and script structure analysis

### Phase 7: Slash Commands
**Goal**: Phase-organized command system
**Plans**: 1 plan

Plans:
- [x] 07-01: Implement 10 phase-organized commands with flags

</details>

<details>
<summary>v1.1 Analytics & Learning Loop (Phases 8-10) - SHIPPED 2026-01-26</summary>

### Phase 8: API Foundation
**Goal**: YouTube Analytics API integration
**Plans**: 3 plans

Plans:
- [x] 08-01: OAuth2 setup and credential management
- [x] 08-02: API client with error handling
- [x] 08-03: Data models and caching

### Phase 9: Data Pull Scripts
**Goal**: Automated analytics retrieval
**Plans**: 3 plans

Plans:
- [x] 09-01: Video metrics fetcher
- [x] 09-02: Batch operations and export
- [x] 09-03: CLI with config validation

### Phase 10: Pattern Recognition
**Goal**: Cross-video learning system
**Plans**: 3 plans

Plans:
- [x] 10-01: Post-publish analysis reports
- [x] 10-02: Pattern detection across videos
- [x] 10-03: Slash commands and monthly summaries

</details>

<details>
<summary>v1.2 Script Quality & Discovery (Phases 11-14) - SHIPPED 2026-01-30</summary>

### Phase 11: Script Quality Checkers
**Goal**: Automated quality checks for spoken-delivery scripts
**Plans**: 2 plans

Plans:
- [x] 11-01: Foundation infrastructure + stumble/scaffolding checkers
- [x] 11-02: Repetition detection + flow analysis checkers

### Phase 12: Voice Fingerprinting
**Goal**: Learn speech patterns from existing transcripts
**Plans**: 2 plans

Plans:
- [x] 12-01: Corpus builder and pattern extractor modules
- [x] 12-02: Pattern applier and CLI integration

### Phase 13: Discovery Tools
**Goal**: SEO and keyword research for topic discovery
**Plans**: 3 plans

Plans:
- [x] 13-01: Database schema + autocomplete extraction + keyword CLI
- [x] 13-02: Intent classification + discovery diagnostics + /analyze extension
- [x] 13-03: Metadata checker + VidIQ workflow + /discover command

### Phase 13.1: Token Optimization (INSERTED)
**Goal**: Reduce token usage by assigning appropriate models to tasks
**Plans**: 2 plans

Plans:
- [x] 13.1-01: Add model assignments to 13 skill files
- [x] 13.1-02: Update agent model assignments + create reference documentation

### Phase 14: NotebookLM Workflow
**Goal**: Streamlined research-to-script pipeline
**Plans**: 1 plan

Plans:
- [x] 14-01: Expand prompt templates + session log template + citation extraction

</details>

<details open>
<summary>v1.3 Niche Discovery (Phases 15-18) - IN PROGRESS</summary>

### Phase 15: Database Foundation & Demand Research
**Goal**: User can quantify demand for topics
**Dependencies**: Phase 13 (keywords.db schema)
**Requirements**: DEM-01, DEM-02, DEM-03, DEM-04
**Plans**: 2 plans

**Success Criteria:**
1. User can input a seed keyword and get search volume proxy (autocomplete position score)
2. User can see trend direction for a keyword (rising/stable/declining with percentage change)
3. User can expand a seed keyword into 10-20 related queries
4. User can see competition ratio score showing demand vs. supply balance

Plans:
- [x] 15-01-PLAN.md — Schema extension + DemandAnalyzer foundation
- [x] 15-02-PLAN.md — External data integration + CLI + /discover --demand

### Phase 16: Competition Analysis
**Goal**: User can identify gaps in existing coverage
**Dependencies**: Phase 15 (demand data foundation)
**Requirements**: COMP-01, COMP-02, COMP-03, COMP-04

**Success Criteria:**
1. User can see video count and unique channel count for a keyword
2. User can filter out low-quality content to see real competition
3. User can see what format competitors use (animation vs. documentary, political vs. legal angles)
4. User can see differentiation score identifying which angles are missing

**Plans**: 2 plans

Plans:
- [x] 16-01-PLAN.md — Classifiers module + schema extension + database methods
- [x] 16-02-PLAN.md — CompetitionAnalyzer extension + quality filtering + differentiation + CLI

### Phase 17: Format Filtering
**Goal**: Topics are filtered by production constraints
**Dependencies**: Phase 16 (competition data)
**Requirements**: FMT-01, FMT-02, FMT-03

**Success Criteria:**
1. Topics requiring animation are flagged as hard blocks before research investment
2. Topics are scored 0-4 for document-friendliness (treaty-heavy = 4, concept-heavy = 0)
3. User can verify academic source availability for a topic before committing

**Plans**: 2 plans

Plans:
- [x] 17-01-PLAN.md — Production constraint foundation (animation detection + document scoring)
- [x] 17-02-PLAN.md — Source hints + CLI for production constraint evaluation

### Phase 18: Opportunity Scoring & Orchestrator
**Goal**: User gets ranked topic opportunities with full context
**Dependencies**: Phases 15, 16, 17 (all data layers)
**Requirements**: OPP-01, OPP-02, OPP-03, OPP-04, OPP-05
**Plans**: 2 plans

**Success Criteria:**
1. User can see combined opportunity score (demand x gap x fit / effort) for any topic
2. Production constraints are weighted in scoring (animation-required topics score 0 regardless of demand)
3. Channel DNA rules auto-reject topics (clickbait language, news-first framing automatically filtered)
4. Opportunities track lifecycle status from DISCOVERED through PUBLISHED
5. User can generate Markdown opportunity report with all decision factors documented

Plans:
- [ ] 18-01-PLAN.md — OpportunityScorer + lifecycle state tracking + Channel DNA filtering
- [ ] 18-02-PLAN.md — OpportunityOrchestrator + report generation + CLI

</details>

## Progress

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. File Cleanup | v1.0 | 3/3 | Complete | 2026-01-19 |
| 2. Style Consolidation | v1.0 | 2/2 | Complete | 2026-01-19 |
| 3. Research Structure | v1.0 | 3/3 | Complete | 2026-01-19 |
| 4. Workflow Simplification | v1.0 | 0/0 | Deferred | - |
| 5. Competitive Intelligence | v1.0 | 0/0 | Covered by Phase 6 | - |
| 6. Pattern Extraction | v1.0 | 1/1 | Complete | 2026-01-19 |
| 7. Slash Commands | v1.0 | 1/1 | Complete | 2026-01-19 |
| 8. API Foundation | v1.1 | 3/3 | Complete | 2026-01-26 |
| 9. Data Pull Scripts | v1.1 | 3/3 | Complete | 2026-01-26 |
| 10. Pattern Recognition | v1.1 | 3/3 | Complete | 2026-01-26 |
| 11. Script Quality Checkers | v1.2 | 2/2 | Complete | 2026-01-28 |
| 12. Voice Fingerprinting | v1.2 | 2/2 | Complete | 2026-01-29 |
| 13. Discovery Tools | v1.2 | 3/3 | Complete | 2026-01-29 |
| 13.1 Token Optimization | v1.2 | 2/2 | Complete | 2026-01-30 |
| 14. NotebookLM Workflow | v1.2 | 1/1 | Complete | 2026-01-30 |
| **15. Database Foundation & Demand Research** | **v1.3** | **2/2** | **Complete** | 2026-01-31 |
| **16. Competition Analysis** | **v1.3** | **2/2** | **Complete** | 2026-02-01 |
| **17. Format Filtering** | **v1.3** | **2/2** | **Complete** | 2026-02-01 |
| **18. Opportunity Scoring & Orchestrator** | **v1.3** | **0/2** | **Planned** | - |
