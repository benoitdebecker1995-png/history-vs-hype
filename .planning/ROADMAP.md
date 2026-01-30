# Roadmap: History vs Hype Workspace

## Milestones

- ✅ **v1.0 MVP** - Phases 1-7 (shipped 2026-01-19)
- ✅ **v1.1 Analytics & Learning Loop** - Phases 8-10 (shipped 2026-01-26)
- 🚧 **v1.2 Script Quality & Discovery** - Phases 11-14 (in progress)

## Phases

<details>
<summary>✅ v1.0 MVP (Phases 1-7) - SHIPPED 2026-01-19</summary>

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
<summary>✅ v1.1 Analytics & Learning Loop (Phases 8-10) - SHIPPED 2026-01-26</summary>

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

### 🚧 v1.2 Script Quality & Discovery (In Progress)

**Milestone Goal:** Produce better scripts faster, and make videos people actually find.

#### Phase 11: Script Quality Checkers
**Goal**: Automated quality checks for spoken-delivery scripts
**Depends on**: Nothing (first phase of v1.2)
**Requirements**: SCRIPT-01, SCRIPT-02, SCRIPT-03, SCRIPT-04
**Success Criteria** (what must be TRUE):
  1. User can scan script for repetitive phrases and get flagged sections with counts
  2. User can verify narrative flow (terms defined before use, smooth transitions)
  3. User can identify teleprompter stumble risks (long sentences, complex clauses)
  4. User can count scaffolding language ("Here's", "So", "Now") and get alerts when exceeded
**Plans**: 2 plans

Plans:
- [x] 11-01-PLAN.md — Foundation infrastructure + stumble/scaffolding checkers
- [x] 11-02-PLAN.md — Repetition detection + flow analysis checkers

#### Phase 12: Voice Fingerprinting
**Goal**: Learn speech patterns from existing transcripts
**Depends on**: Phase 11 (builds on quality checker infrastructure)
**Requirements**: SCRIPT-05
**Success Criteria** (what must be TRUE):
  1. User can analyze existing video transcripts to build speech pattern library
  2. User can flag script violations of established voice patterns
  3. User can see suggestions aligned with personal delivery style
**Plans**: 2 plans

Plans:
- [x] 12-01-PLAN.md — Corpus builder and pattern extractor modules
- [x] 12-02-PLAN.md — Pattern applier and CLI integration

#### Phase 13: Discovery Tools
**Goal**: SEO and keyword research for topic discovery
**Depends on**: Phase 11 (can run parallel to Phase 12)
**Requirements**: DISC-01, DISC-02, DISC-03, DISC-04
**Success Criteria** (what must be TRUE):
  1. User can extract long-tail keyword phrases from YouTube autocomplete
  2. User can classify titles by search intent (why/how/what patterns)
  3. User can diagnose discovery issues (low impressions = SEO, low CTR = title/thumbnail)
  4. User can verify metadata consistency across title/description/tags
**Plans**: 3 plans

Plans:
- [x] 13-01-PLAN.md — Database schema + autocomplete extraction + keyword CLI (DISC-01)
- [x] 13-02-PLAN.md — Intent classification + discovery diagnostics + /analyze extension (DISC-02, DISC-03)
- [x] 13-03-PLAN.md — Metadata checker + VidIQ workflow + /discover command (DISC-04)

#### Phase 13.1: Token Optimization via Model Assignment (INSERTED)
**Goal**: Reduce token usage by assigning Haiku to simple tasks, Sonnet to standard tasks, and Opus to complex creative tasks
**Depends on**: Phase 13 (uses existing skill/agent infrastructure)
**Requirements**: TOKEN-01 (Model assignment system for skills and agents)
**Success Criteria** (what must be TRUE):
  1. User can see which model is assigned to each skill/agent in configuration
  2. Simple tasks (status, help, fix) use Haiku for faster/cheaper execution
  3. Standard tasks (verify, publish, engage) use Sonnet for balanced performance
  4. Complex creative tasks (script-writer-v2) use Opus for highest quality
  5. Model assignments are documented and easily adjustable
**Plans**: 2 plans

Plans:
- [x] 13.1-01-PLAN.md — Add model assignments to skill files (13 commands)
- [x] 13.1-02-PLAN.md — Update agent model assignments + create reference documentation

#### Phase 14: NotebookLM Workflow
**Goal**: Streamlined research-to-script pipeline
**Depends on**: Phases 11 and 13 (quality checks + discovery inform research needs)
**Requirements**: NBLM-01, NBLM-02, NBLM-03
**Success Criteria** (what must be TRUE):
  1. User can select from 15+ structured prompt templates for research scenarios
  2. User can log NotebookLM sessions with standard format capturing findings
  3. User can paste NotebookLM output and get structured citation extraction
**Plans**: TBD

Plans:
- [ ] 14-01: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 11 → 12 → 13 → 13.1 → 14

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
| 14. NotebookLM Workflow | v1.2 | 0/1 | Not started | - |
