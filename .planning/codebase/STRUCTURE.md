# Codebase Structure

**Analysis Date:** 2025-01-19

## Directory Layout

```
D:\History vs Hype\
├── .claude/                    # Claude Code configuration and intelligence
│   ├── agents/                 # Specialized AI agents
│   ├── commands/               # Slash command definitions
│   ├── PROMPTS/                # Standalone prompts for external tools
│   ├── REFERENCE/              # Style guides, workflows, technique libraries
│   ├── skills/                 # Modular capabilities for agents
│   ├── templates/              # Project initialization templates
│   ├── tools/                  # Utility scripts (transcript fetching)
│   ├── _ARCHIVE/               # Deprecated configurations
│   ├── settings.local.json     # Local Claude settings
│   ├── USER-PREFERENCES.md     # User speaking patterns, working style
│   └── VERIFIED-CLAIMS-DATABASE.md  # Reusable verified facts
├── .planning/                  # Planning and codebase analysis
│   └── codebase/               # Architecture documentation
├── channel-data/               # Channel analytics and strategy
│   ├── analytics-exports/      # YouTube Studio exports
│   ├── archive/                # Historical data
│   └── *.md/*.csv              # Performance databases, competitor analysis
├── guides/                     # Production workflow guides
├── library/                    # Academic source library
│   ├── by-topic/               # PDFs organized by subject
│   └── for-notebooklm/         # Prepared sources for research
├── research/                   # Research compilations and outputs
│   ├── active/                 # In-progress research
│   ├── completed/              # Finished research
│   └── _archive/               # Old research
├── templates/                  # Production templates
│   ├── automation/             # Automated workflow templates
│   └── project-templates/      # B-roll, filming notes
├── tools/                      # Utility tools and scripts
│   ├── ffmpeg/                 # Video processing
│   ├── history-clip-tool/      # Clipping utilities
│   └── yt-dlp.exe              # YouTube downloader
├── transcripts/                # Competitor and reference transcripts
│   ├── Alex O'Connor/          # Creator-specific folders
│   ├── Fall of Civilizations/
│   ├── Historia Civilis/
│   ├── Knowing Better/
│   ├── Kraut/
│   ├── RealLifeLore/
│   ├── Shaun/
│   ├── haiti/                  # Haiti research transcripts
│   ├── niche-research/         # Niche creator analysis
│   └── *.srt/*.vtt/*.txt       # Individual transcripts
├── video-ideas/                # Topic brainstorming
├── video-projects/             # Active production projects
│   ├── _ANALYTICS/             # Video performance analysis
│   ├── _ARCHIVED/              # Published/cancelled projects
│   ├── _IN_PRODUCTION/         # Active research and scripting
│   ├── _READY_TO_FILM/         # Approved scripts
│   ├── _CORRECTIONS-LOG.md     # Error tracking
│   └── PROJECT_STATUS.md       # Global status tracker
├── _archive-old/               # Legacy files
├── CLAUDE.md                   # Primary Claude Code instructions
├── START-HERE.md               # Quick start guide
└── VERIFIED-WORKFLOW-QUICK-REFERENCE.md  # One-page workflow
```

## Directory Purposes

**.claude/:**
- Purpose: All Claude Code intelligence and configuration
- Contains: Commands, agents, skills, reference docs, templates
- Key files: `USER-PREFERENCES.md`, `VERIFIED-CLAIMS-DATABASE.md`, `settings.local.json`

**.claude/agents/:**
- Purpose: Specialized AI agents for complex tasks
- Contains: `script-writer-v2.md`, `fact-checker.md`, `structure-checker-v2.md`, `research-organizer.md`, `claims-extractor.md`, `diy-asset-creator.md`

**.claude/commands/:**
- Purpose: Entry points for user-initiated workflows
- Contains: `new-video.md`, `script.md`, `fact-check.md`, `youtube-metadata.md`, `extract-claims.md`, `respond-to-comment.md`, etc.

**.claude/REFERENCE/:**
- Purpose: Style guides, technique libraries, workflow documentation
- Contains: `scriptwriting-style.md`, `workflow.md`, `creator-techniques.md`, `PROVEN-TECHNIQUES-LIBRARY.md`, `RETENTION-CTR-PLAYBOOK.md`
- Key files: `workflow.md` (Tier 1 authority), `channel-values.md` (brand DNA)

**.claude/templates/:**
- Purpose: Project initialization templates
- Contains: `01-VERIFIED-RESEARCH-TEMPLATE.md`, `02-SCRIPT-DRAFT-TEMPLATE.md`, `03-FACT-CHECK-VERIFICATION-TEMPLATE.md`, `FILMING-READY-CERTIFICATION-TEMPLATE.md`

**video-projects/:**
- Purpose: All video production work
- Contains: Lifecycle folders with project subfolders
- Key files: `PROJECT_STATUS.md` (global tracker), `_CORRECTIONS-LOG.md` (error tracking), `PROJECT_REGISTRY.md` (quick path lookup)

**video-projects/_IN_PRODUCTION/:**
- Purpose: Active research and scripting projects
- Contains: Numbered project folders following `[number]-[topic-slug-year]/` pattern
- Each folder has: `01-VERIFIED-RESEARCH.md`, `02-SCRIPT-DRAFT.md`, `03-FACT-CHECK-VERIFICATION.md`, `PROJECT-STATUS.md`, `_research/`

**channel-data/:**
- Purpose: Analytics, strategy, competitor analysis
- Contains: `COMPETITOR-TITLE-DATABASE.md`, `SCRIPT-STRUCTURE-ANALYSIS.md`, CSV exports, improvement audits

**library/:**
- Purpose: Academic source PDFs for NotebookLM
- Contains: `by-topic/` folders (general-history, middle-east-history, reference-methodology), `for-notebooklm/` prepared sources
- Key files: `LIBRARY-INDEX.md`, `auto_rename_books.py`

**transcripts/:**
- Purpose: Competitor transcripts for style analysis
- Contains: Creator-specific folders (Kraut, Knowing Better, Shaun, Alex O'Connor, etc.), topic-specific folders (haiti/, niche-research/), individual `.srt`/`.vtt` files

## Key File Locations

**Entry Points:**
- `CLAUDE.md`: Primary Claude Code instructions (always loaded)
- `START-HERE.md`: Human quick-start guide
- `.claude/commands/new-video.md`: Main workflow entry

**Configuration:**
- `.claude/USER-PREFERENCES.md`: User speaking patterns, working style
- `.claude/settings.local.json`: Claude Code settings
- `.claude/REFERENCE/channel-values.md`: Brand DNA, non-negotiables

**Core Logic:**
- `.claude/REFERENCE/workflow.md`: Master workflow definition (Tier 1)
- `.claude/agents/script-writer-v2.md`: Script generation logic
- `.claude/agents/fact-checker.md`: Verification logic

**Testing:**
- No automated test framework (content production, not software)
- Quality gates serve as verification checkpoints

## Naming Conventions

**Files:**
- UPPERCASE-WITH-DASHES.md: Reference documents, guides
- numbered-prefix: Sequential files within projects (`01-VERIFIED-RESEARCH.md`)
- VERSION-suffix: Script iterations (`02-SCRIPT-DRAFT-V3.md`)
- topic-slug: Descriptive kebab-case (`haiti-independence-debt`)

**Directories:**
- _UPPERCASE_UNDERSCORES: Lifecycle folders (`_IN_PRODUCTION/`)
- lowercase-dashes: Creator transcript folders (`Knowing Better/`)
- number-topic-year: Project folders (`21-haiti-independence-debt-2025/`)

**Projects:**
- Pattern: `[number]-[topic-slug-year]/`
- Example: `21-haiti-independence-debt-2025/`
- Number: Sequential project number
- Slug: Descriptive topic identifier
- Year: Production year

## Where to Add New Code

**New Video Project:**
- Primary code: `video-projects/_IN_PRODUCTION/[number]-[topic-slug-year]/`
- Use `/new-video` command to initialize

**New Command:**
- Implementation: `.claude/commands/[command-name].md`
- Follow existing command structure with frontmatter

**New Agent:**
- Implementation: `.claude/agents/[agent-name].md`
- Follow agent template with MISSION, CONSTRAINTS, RULES sections

**New Reference Document:**
- Shared helpers: `.claude/REFERENCE/[DOCUMENT-NAME].md`
- Update relevant agent files to reference new doc

**New Template:**
- Location: `.claude/templates/[template-name].md`
- Update `/new-video` command if part of initialization

**Research Files:**
- Active research: `research/active/`
- Project-specific: `video-projects/[project]/_research/`

**Transcripts:**
- Creator-specific: `transcripts/[Creator Name]/`
- Working files: Project root

## Special Directories

**_IN_PRODUCTION:**
- Purpose: Active video projects being researched or scripted
- Generated: No (user-created via `/new-video`)
- Committed: Yes

**_READY_TO_FILM:**
- Purpose: Approved scripts ready for recording
- Generated: No (manual move after approval)
- Committed: Yes

**_ARCHIVED:**
- Purpose: Published or cancelled projects
- Generated: No (manual move after publication)
- Committed: Yes

**_research (within projects):**
- Purpose: NotebookLM outputs, source PDFs, raw materials
- Generated: No (user-populated)
- Committed: Yes

**_ARCHIVE (within .claude):**
- Purpose: Deprecated configurations
- Generated: No
- Committed: Yes (historical reference)

**library/temp:**
- Purpose: Temporary files during PDF processing
- Generated: Yes (by `auto_rename_books.py`)
- Committed: No (transient)

---

*Structure analysis: 2025-01-19*
