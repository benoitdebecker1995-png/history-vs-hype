# Phase 5 Context: Workflow Simplification

**Gathered:** 2026-01-22
**Source:** User discussion (4 areas, 16 questions)

---

## User Workflow Profile

### How User Works
- **Entry point:** Mix depending on the day - no single starting command
- **Command usage:** Describes what they want, lets Claude figure it out
- **Memory:** Doesn't remember commands - asks Claude or checks docs
- **Mental model:** Guidance-oriented ("help me figure out what to do")

### What User Wants
- **Wizard for new projects**, direct commands for existing work
- **Proactive suggestions** - always suggest next steps after milestones
- **Unified system** - merge GSD + video commands into one
- **~10-12 commands** with clear categories (not current ~20)
- **Phase-based organization:** Pre-production → Production → Post-production

### Documentation Reality
- User **never reads CLAUDE.md** - Claude reads it
- User **relies entirely on Claude** to know the system
- Documentation is FOR Claude, not the user
- Quick reference only if Claude can't help

---

## Design Principles (Derived)

### 1. Claude as Interface
User talks to Claude in natural language. Claude handles routing to commands, tools, workflows. User shouldn't need to memorize anything.

### 2. Proactive Guidance
Always suggest next steps. After script completion → suggest fact-check. After fact-check → suggest filming prep. Don't wait to be asked.

### 3. Context-Aware Routing
Detect project state automatically. If in `_IN_PRODUCTION/` with SCRIPT.md but no FACT-CHECK.md → suggest fact-checking. Smart defaults.

### 4. Unified System
No parallel systems (GSD vs. video commands). One coherent workflow that handles both system maintenance AND video production.

### 5. Phase-Based Organization
Organize everything by production phase:
- **Pre-production:** Research, topic selection, source gathering
- **Production:** Scripting, fact-checking, filming prep
- **Post-production:** Editing, metadata, publishing, corrections

### 6. Discoverable Capabilities
Two modes:
- **Automatic:** Claude suggests relevant actions during work
- **Manual:** Interactive menu/list when user asks "what can I do?"

---

## Command Consolidation Direction

### Current (~20 commands)
```
/new-video, /script, /fact-check, /fix-subtitles, /edit-guide,
/clip-suggestions, /youtube-metadata, /extract-claims, /teleprompter,
/respond-to-comment, /publish-correction, /save-comment, /evaluate-feedback,
/test-titles, /zero-budget-assets, /notebooklm-prompts, /suggest-sources,
/find-topic, /deep-research, /format-sources
```

### Target (~10-12 organized by phase)

**Pre-production (3):**
- `/research` - Topic research, source gathering, NotebookLM setup
- `/sources` - Source recommendations, formatting, NotebookLM prompts

**Production (4):**
- `/script` - Write/revise script (absorbs /teleprompter as flag)
- `/verify` - Fact-check verification (absorbs /extract-claims)
- `/prep` - Filming prep (absorbs /edit-guide, /zero-budget-assets)

**Post-production (3):**
- `/publish` - Metadata, titles, descriptions (absorbs /youtube-metadata, /test-titles)
- `/fix` - Subtitle fixes (keeps /fix-subtitles focused)
- `/engage` - Comments, corrections (absorbs /respond-to-comment, /publish-correction, /save-comment)

**Meta (2):**
- `/status` - Project status, what's next (smart router)
- `/help` - Capability discovery with phase organization

### Commands to Remove/Merge
- `/new-video` → Merged into smart `/status` detection + `/research`
- `/evaluate-feedback` → Merge into `/verify` or remove (rarely used)
- `/clip-suggestions` → Merge into `/publish`
- `/find-topic`, `/deep-research` → Merge into `/research`
- GSD commands → Behind the scenes, not user-facing

---

## Entry Point Design

### Smart Router Concept (`/status` or just asking)

When user says "what should I do?" or runs `/status`:

1. **Detect context:**
   - Current directory → which project?
   - Files present → which phase?
   - Git status → recent work?

2. **Assess state:**
   - Has VERIFIED-RESEARCH.md? → Research done
   - Has SCRIPT.md? → Script exists
   - Has FACT-CHECK.md? → Verified
   - Has YOUTUBE-METADATA.md? → Ready to publish

3. **Suggest next action:**
   - "You have verified research but no script. Ready to write? (`/script`)"
   - "Script complete. Want to run fact-check? (`/verify`)"
   - "All production files ready. Next: filming prep (`/prep`)"

### Natural Language Routing

User says: "I want to start a video about X"
Claude: Detects no existing project → offers to create folder, start research

User says: "The script is done"
Claude: Detects SCRIPT.md exists → suggests fact-check

User says: "What can I do?"
Claude: Shows phase-organized menu of relevant options

---

## Documentation Restructure

### CLAUDE.md Optimization
- Keep comprehensive (Claude reads it)
- Add machine-readable sections for routing logic
- Remove user-facing explanations (user asks Claude)

### User-Facing Docs (Minimal)
- `START-HERE.md` - One paragraph + "ask Claude"
- Phase checklists (optional reference)
- Style guide (for when user wants to review voice/tone)

### Reference Files (Claude-Facing)
- Keep in `.claude/REFERENCE/`
- Optimize for Claude parsing
- Remove redundancy

---

## Success Criteria for Phase 5

1. **User can work without remembering commands**
   - Natural language → Claude routes appropriately
   - Proactive suggestions after each milestone

2. **~10-12 consolidated commands**
   - Organized by phase
   - Clear mental model

3. **Smart status/routing**
   - `/status` or natural question → context-aware response
   - Automatic next-step suggestions

4. **Unified system**
   - GSD absorbed into main workflow
   - No parallel command sets

5. **Documentation serves Claude**
   - CLAUDE.md optimized for AI
   - User asks Claude instead of reading docs

---

## Questions Resolved

| Question | Resolution |
|----------|------------|
| Wizard vs. direct commands? | Both: wizard for new, direct for existing |
| How many commands? | ~10-12 with phase categories |
| GSD + video commands? | Merge into one system |
| Documentation for whom? | Claude (user asks Claude) |
| Discovery method? | Proactive suggestions + browsable menu |

---

## Implementation Notes

### Phase 5 Plans Should Cover:
1. Command consolidation (merge ~20 → ~10-12)
2. Smart router implementation (`/status` or natural language)
3. Proactive suggestion system (milestone → next step)
4. Documentation restructure (Claude-optimized)
5. Phase-based organization throughout

### Dependencies:
- Phase 4 complete (SCRIPT.md standardization) ✅
- Existing command definitions in `.claude/commands/`
- CLAUDE.md current structure

### Constraints:
- Maintain backward compatibility during transition
- Don't break existing projects mid-production
- Preserve all functionality (consolidate, don't remove capabilities)
