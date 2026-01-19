# Architecture

**Analysis Date:** 2025-01-19

## Pattern Overview

**Overall:** Document-Driven Content Production Pipeline

**Key Characteristics:**
- Markdown-first knowledge management with hierarchical reference system
- Phase-gated workflow with explicit quality gates blocking progression
- Agent-assisted automation through Claude Code slash commands
- Single-source-of-truth pattern for verified facts
- Lifecycle-based project state management

## Layers

**Configuration Layer:**
- Purpose: Define channel values, user preferences, and system behavior
- Location: `.claude/`
- Contains: Agent configs, command definitions, reference documents, templates
- Depends on: Nothing (foundational)
- Used by: All agents, commands, and workflows

**Command Layer:**
- Purpose: Entry points for user-initiated workflows
- Location: `.claude/commands/`
- Contains: Slash command definitions (`.md` files with frontmatter)
- Depends on: Configuration Layer, Agent Layer
- Used by: User via `/command-name` invocations

**Agent Layer:**
- Purpose: Specialized AI agents for complex tasks
- Location: `.claude/agents/`
- Contains: `script-writer-v2.md`, `fact-checker.md`, `structure-checker-v2.md`, etc.
- Depends on: Reference documents in `.claude/REFERENCE/`
- Used by: Commands, orchestration workflows

**Reference Layer:**
- Purpose: Style guides, workflow documentation, technique libraries
- Location: `.claude/REFERENCE/`
- Contains: `scriptwriting-style.md`, `workflow.md`, `creator-techniques.md`, `PROVEN-TECHNIQUES-LIBRARY.md`
- Depends on: Channel values (Tier 1 authority)
- Used by: Agents when writing scripts, fact-checking

**Template Layer:**
- Purpose: Reusable starting structures for projects
- Location: `.claude/templates/`
- Contains: `01-VERIFIED-RESEARCH-TEMPLATE.md`, `02-SCRIPT-DRAFT-TEMPLATE.md`, `03-FACT-CHECK-VERIFICATION-TEMPLATE.md`
- Depends on: Reference Layer for content patterns
- Used by: `/new-video` command to initialize projects

**Project Layer:**
- Purpose: Active video production with all research and scripts
- Location: `video-projects/`
- Contains: Per-video folders with research, scripts, metadata
- Depends on: Template Layer (initialization), Agent Layer (processing)
- Used by: User during production

**Resource Layers:**
- Purpose: Supporting content and tools
- Locations: `library/`, `research/`, `transcripts/`, `tools/`, `channel-data/`
- Contains: Academic PDFs, research compilations, competitor transcripts, utility scripts, analytics
- Depends on: Nothing (input data)
- Used by: NotebookLM research, competitor analysis, script development

## Data Flow

**New Video Production:**

1. User invokes `/new-video` command
2. Command reads template from `.claude/templates/01-VERIFIED-RESEARCH-TEMPLATE.md`
3. Creates project folder in `video-projects/_IN_PRODUCTION/[number]-[topic-slug-year]/`
4. Initializes `01-VERIFIED-RESEARCH.md`, placeholder files, `PROJECT-STATUS.md`
5. User researches using NotebookLM, populates verified research doc
6. Quality gate: 90%+ claims verified before proceeding
7. Agent writes script from verified facts only
8. Cross-check phase validates script against research
9. Quality gate: 100% match required for filming approval
10. Project moves to `_READY_TO_FILM/` when certified

**Fact Verification Flow:**

1. Claim identified in research
2. Check `.claude/VERIFIED-CLAIMS-DATABASE.md` for existing verification
3. If not found: Research with NotebookLM (academic sources)
4. Verify with 2+ Tier 1-2 sources
5. Record exact quote with page number
6. Mark status: VERIFIED / RESEARCHING / UNVERIFIABLE
7. Add to project's `01-VERIFIED-RESEARCH.md`
8. Optionally add to shared claims database for future videos

**Script Generation Flow:**

1. Agent reads `.claude/REFERENCE/scriptwriting-style.md` (mandatory)
2. Agent reads project's `01-VERIFIED-RESEARCH.md`
3. Applies creator techniques from `creator-techniques.md`
4. Follows spoken delivery rules (contractions, conversational dates)
5. Outputs to `02-SCRIPT-DRAFT.md`
6. Structure checker validates retention mechanics

**State Management:**
- Project state tracked in `video-projects/PROJECT_STATUS.md` (global)
- Per-project state in `[project]/PROJECT-STATUS.md` (local)
- Lifecycle stages: `_IN_PRODUCTION/` -> `_READY_TO_FILM/` -> `_ARCHIVED/`

## Key Abstractions

**Video Project:**
- Purpose: Container for all production artifacts of a single video
- Examples: `video-projects/_IN_PRODUCTION/21-haiti-independence-debt-2025/`
- Pattern: Numbered prefix + topic slug + year suffix

**Verified Research Document:**
- Purpose: Single source of truth for all facts in a video
- Examples: `01-VERIFIED-RESEARCH.md` in each project
- Pattern: Section-based with verification status markers (checkmarks)

**Script Draft:**
- Purpose: Production-ready spoken script
- Examples: `02-SCRIPT-DRAFT.md` (may have versioned iterations)
- Pattern: Hook -> Tension -> Evidence -> Synthesis -> CTA structure

**Quality Gate:**
- Purpose: Blocking checkpoint preventing progression with errors
- Examples: 90% verification gate, 100% cross-check gate
- Pattern: Checklist in workflow documentation with BLOCKED status

**Agent Configuration:**
- Purpose: Specialized AI behavior for specific tasks
- Examples: `script-writer-v2.md`, `fact-checker.md`
- Pattern: Frontmatter metadata + mission + constraints + rules

## Entry Points

**Primary Entry Points:**

**`/new-video` Command:**
- Location: `.claude/commands/new-video.md`
- Triggers: Project initialization workflow
- Responsibilities: Create folder structure, copy templates, set up tracking

**`/script` Command:**
- Location: `.claude/commands/script.md`
- Triggers: Script generation from verified research
- Responsibilities: Invoke script-writer agent with proper context

**`/fact-check` Command:**
- Location: `.claude/commands/fact-check.md`
- Triggers: Academic peer review process
- Responsibilities: Cross-check script against sources

**`/youtube-metadata` Command:**
- Location: `.claude/commands/youtube-metadata.md`
- Triggers: Metadata generation
- Responsibilities: Create title, description, tags, timestamps

**Secondary Entry Points:**

**`CLAUDE.md`:**
- Location: `D:\History vs Hype\CLAUDE.md`
- Triggers: Context loading for any Claude Code session
- Responsibilities: Provide channel DNA, workflow overview, critical reminders

**`START-HERE.md`:**
- Location: `D:\History vs Hype\START-HERE.md`
- Triggers: Human onboarding
- Responsibilities: Quick start guide, workflow navigation

## Error Handling

**Strategy:** Prevention through quality gates rather than correction

**Patterns:**
- BLOCKING gates prevent progression (90% verification, 100% cross-check)
- Verification status markers track claim confidence
- Post-publication review captures errors within 48 hours
- Corrections log documents and prevents repeat errors
- `_CORRECTIONS-LOG.md` tracks errors for system improvement

**Recovery:**
- Failed gate returns script to previous phase
- Citation spot-check failure triggers full audit
- Unverified claims flagged with `[NEEDS VERIFICATION: ...]`

## Cross-Cutting Concerns

**Logging:**
- Project progress in `PROJECT-STATUS.md` files
- Channel analytics in `channel-data/` directory
- Performance tracking in `VIDEO-ANALYTICS-LOG.md`

**Validation:**
- Tier 1-2 source requirement for academic claims
- Word-for-word quote verification
- Archive reference precision checking (e.g., HW 16/23 not HW 16/32)

**Authentication:**
- NotebookLM for source-grounded research
- VidIQ for YouTube optimization
- No API authentication (human-in-loop with AI assistance)

---

*Architecture analysis: 2025-01-19*
