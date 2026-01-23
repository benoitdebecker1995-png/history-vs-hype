---
phase: 05-workflow-simplification
plan: 02
subsystem: commands
tags: [routing, help, discovery, proactive-guidance]

dependency_graph:
  requires:
    - "05-01 (8 consolidated commands)"
  provides:
    - "Smart status detection"
    - "Phase-organized help"
    - "Proactive next-step suggestions"
  affects:
    - "User workflow navigation"
    - "Command discovery"

tech_stack:
  added: []
  patterns:
    - "Context-aware routing"
    - "Natural language command mapping"
    - "Proactive suggestion system"

file_tracking:
  created:
    - ".claude/commands/status.md"
    - ".claude/commands/help.md"
  modified:
    - ".claude/commands/research.md"
    - ".claude/commands/script.md"
    - ".claude/commands/verify.md"

decisions:
  - id: "status-detection-order"
    choice: "Git status > recent files > directory scan"
    reason: "Most likely to find what user is working on"
  - id: "natural-language-mapping"
    choice: "Table-based routing examples"
    reason: "Clear pattern for Claude to match"
  - id: "proactive-suggestion-format"
    choice: "Blockquote with numbered next steps"
    reason: "Scannable, actionable, consistent"

metrics:
  duration: "3 minutes"
  completed: "2026-01-23"
---

# Phase 5 Plan 2: Smart Router and Help System Summary

**One-liner:** Context-aware /status command with project detection, phase-organized /help menu, and proactive next-step suggestions in key commands.

## What Was Built

### 1. Smart Status Router (`/status`)

Created `.claude/commands/status.md` (222 lines) with:

**Detection Logic:**
- Finds active project via git status and recent file modification
- Assesses project state by checking file existence (research, script, verification, metadata)
- Determines phase: Pre-production / Production / Post-production / Complete

**Output:**
- Project name and location
- Checklist of completed milestones
- Suggested next action with rationale
- Alternative actions

**Natural Language Support:**
- "What should I do?"
- "What's next?"
- "Where am I?"
- "Project status"

**Edge Cases:**
- No active project: Suggests `/research --new`
- Multiple projects: Lists with last modified, asks for selection
- Needs attention: Flags research gaps or failed verification

### 2. Phase-Organized Help (`/help`)

Created `.claude/commands/help.md` (165 lines) with:

**Structure:**
```
Pre-production (2): /research, /sources
Production (3): /script, /verify, /prep
Post-production (3): /publish, /fix, /engage
Meta (2): /status, /help
```

**Features:**
- Command tables with flags
- "When to use" guidance per phase
- Natural language routing examples
- Quick reference for full workflow
- Context-specific help for topics

### 3. Proactive Suggestion Rules

Added "After Completion" sections to key commands:

**research.md:**
- Suggests `/script` when 90%+ verified
- Offers project creation if topic-only mode

**script.md:**
- Suggests `/verify` after generation
- Context-aware for review/teleprompter modes
- Reports word count and estimated runtime

**verify.md:**
- If APPROVED: Suggests `/prep` and `/publish`
- If NEEDS REVISION: Points to 03-FACT-CHECK-VERIFICATION.md
- After claims extraction: Suggests full verification

## Verification Results

| Check | Result |
|-------|--------|
| Status detection logic | File contains project detection, phase assessment, suggestion generation |
| Help organization | Commands grouped by Pre-production, Production, Post-production, Meta |
| All commands present | All 10 consolidated commands listed with flags |
| Natural language routing | Examples table with 10+ common phrases |
| Proactive flow | research -> script -> verify chain established |
| YAML frontmatter | Present in all created/modified files |

## Commits

| Hash | Message |
|------|---------|
| 72da73f | feat(05-02): create smart status router command |
| 5d85ac2 | feat(05-02): create phase-organized help command |
| 2bbb4a6 | feat(05-02): add proactive next-step suggestions to commands |

## Design Decisions

### 1. Status Detection Order
**Choice:** Git status first, then recent files, then full directory scan
**Rationale:** Git status captures what user is actively editing; falls back gracefully

### 2. Natural Language as Primary Interface
**Choice:** Table-based routing with common phrases
**Rationale:** User doesn't need to memorize commands; describes intent, gets routed

### 3. Proactive Suggestions in Blockquotes
**Choice:** Blockquote format with numbered steps
**Rationale:** Visually distinct, scannable, consistent across commands

## Deviations from Plan

None - plan executed exactly as written.

## Phase 5 Status

| Plan | Status | Focus |
|------|--------|-------|
| 05-01 | COMPLETE | Command consolidation (20+ -> 8) |
| 05-02 | COMPLETE | Smart router + help + proactive suggestions |

**Phase 5 COMPLETE**

## Next Phase Readiness

Phase 6 (Competitive Intelligence) can now proceed.

**Prerequisites met:**
- 10 consolidated commands with clear phase organization
- Smart routing for context-aware suggestions
- Help system for capability discovery
- Proactive guidance flow through production pipeline

**User can now:**
- Ask "what should I do?" and get context-aware guidance
- Run `/status` to see project state and next action
- Run `/help` to discover commands by production phase
- Work through entire pipeline with proactive suggestions at each step
