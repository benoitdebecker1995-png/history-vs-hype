---
deprecated: true
replaced_by: /research --new
---

> **DEPRECATED:** This command has been replaced by `/research --new`.
> Run `/help` to see current commands.

[Original content below for reference]
---

---
description: Start new video with 3-phase verified workflow (research -> script -> fact-check)
---

# New Video - Verified Workflow

You are setting up a new History vs Hype video project using the **3-phase verified workflow** that prevents fact-check errors.

## WORKFLOW OVERVIEW

**Phase 1:** Research + Verify simultaneously -> `01-VERIFIED-RESEARCH.md`
**Phase 2:** Write script from verified facts only -> `SCRIPT.md`
**Phase 3:** Cross-check script against research -> `03-FACT-CHECK-VERIFICATION.md`

**Goal:** Zero fact-check errors (like Fuentes HW 16/32, 8,000 Italian Jews)

---

## YOUR TASK

### Step 1: Gather Project Information

Ask the user:
1. **Topic:** What's the video about?
2. **Opponent (if applicable):** Who are you fact-checking? (Pax Tube, Nick Fuentes, etc.)
3. **Modern hook:** What current event makes this relevant? (2024-2025 news)
4. **Project number:** What number is this? (Check existing projects in `_IN_PRODUCTION/`)

### Step 2: Check Claims Database for Existing Verified Facts

Before creating the project folder, search for relevant verified claims:

1. **Read:** `.claude/VERIFIED-CLAIMS-DATABASE.md`
2. **Search for:** Topic keywords, related subjects, overlapping time periods
3. **If claims found:**
   - Note which claims are already verified
   - These can be used directly in 01-VERIFIED-RESEARCH.md
   - Mark as "Previously verified: [date], [video]"
   - Only research claims NOT already in database
4. **If no claims found:** Proceed with full research

This step prevents duplicate research and ensures consistency across videos.

### Step 3: Create Project Folder

**Location:** `video-projects/_IN_PRODUCTION/[number]-[topic-slug-year]/`

**Example:** `video-projects/_IN_PRODUCTION/5-french-colonialism-2025/`

**Create folder structure:**
```
[number]-[topic-slug-year]/
  01-VERIFIED-RESEARCH.md
  SCRIPT.md (placeholder for Phase 2)
  03-FACT-CHECK-VERIFICATION.md (placeholder for Phase 3)
  _research/ (for NotebookLM outputs, source PDFs, etc.)
```

[Content truncated for brevity - see original file for full content]
