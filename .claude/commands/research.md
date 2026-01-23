---
description: Start new video project OR conduct topic research (Pre-production Phase 1)
---

# /research - Pre-production Research Entry Point

Start a new video project or research an existing topic. This command consolidates project setup, topic research, and NotebookLM preparation.

## Usage

```
/research                    # Interactive: asks what you need
/research --new [topic]      # Create new project folder + start research
/research --topic-only       # Research without creating project
/research --existing [path]  # Research for existing project
```

## Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `--new` | Create project folder + full setup | `/research --new "Library of Alexandria"` |
| `--topic-only` | Research only, no project creation | `/research --topic-only "Chagos Islands"` |
| `--existing` | Add research to existing project | `/research --existing 19-flat-earth-medieval-2025` |

---

## NEW PROJECT WORKFLOW (`--new` or default)

### Step 1: Gather Project Information

Ask the user:
1. **Topic:** What's the video about?
2. **Hook Type:** Territorial (colonial → conflict) OR Ideological (myth → belief)?
3. **Modern hook:** What 2024-2026 event makes this relevant?
4. **Opponent (if fact-check):** Who are you fact-checking?

### Step 2: Check Claims Database FIRST

Before creating anything, check for existing verified research:

1. **Read:** `.claude/VERIFIED-CLAIMS-DATABASE.md`
2. **Search for:** Topic keywords, related subjects, overlapping time periods
3. **If claims found:**
   - Note which claims are already verified
   - These go directly into 01-VERIFIED-RESEARCH.md
   - Mark as "Previously verified: [date], [video]"
   - Only research claims NOT already in database
4. **If no claims found:** Proceed with full research

### Step 3: Create Project Folder

**Location:** `video-projects/_IN_PRODUCTION/[number]-[topic-slug-year]/`

**Auto-detect next number:** Check highest existing number in `_IN_PRODUCTION/`

**Create structure:**
```
[number]-[topic-slug-year]/
  01-VERIFIED-RESEARCH.md      (from template)
  SCRIPT.md                     (placeholder)
  03-FACT-CHECK-VERIFICATION.md (placeholder)
  PROJECT-STATUS.md             (track progress)
  _research/                    (for NotebookLM outputs)
    00-NOTEBOOKLM-SOURCE-LIST.md
    01-PRELIMINARY-RESEARCH.md
    02-NOTEBOOKLM-PROMPTS.md
```

### Step 4: Initialize Research Files

**01-VERIFIED-RESEARCH.md** - Copy from `.claude/templates/01-VERIFIED-RESEARCH-TEMPLATE.md`
- Fill in project name, date, topic categories
- Pre-populate with any claims from VERIFIED-CLAIMS-DATABASE

**PROJECT-STATUS.md** - Create with phase tracking:
- Phase 1: Research (current)
- Phase 2: Script (locked until 90% verified)
- Phase 3: Fact-check (locked until script complete)

### Step 5: Conduct Preliminary Research

**Phase 1: Internet Research (Map the landscape)**

Research the topic to identify:
- Key claims to verify
- Academic sources needed
- Modern relevance connections (2023-2026 news)
- Opposing viewpoints to address

**Output to:** `_research/01-PRELIMINARY-RESEARCH.md`

### Step 6: Create NotebookLM Source List

Based on preliminary research, create:
- `_research/00-NOTEBOOKLM-SOURCE-LIST.md`

**Standards (from NOTEBOOKLM-SOURCE-STANDARDS.md):**
- University press publications ONLY (Cambridge, Oxford, Chicago, Harvard)
- Top-tier scholars (endowed chairs, major universities)
- Critical editions of primary sources
- Budget is UNLIMITED - recommend best sources regardless of price

### Step 7: Report and Next Steps

```
Project created: video-projects/_IN_PRODUCTION/[folder]/

Files created:
- 01-VERIFIED-RESEARCH.md (start here)
- SCRIPT.md (placeholder - locked until research 90% verified)
- 03-FACT-CHECK-VERIFICATION.md (placeholder)
- PROJECT-STATUS.md
- _research/00-NOTEBOOKLM-SOURCE-LIST.md (sources to download)
- _research/01-PRELIMINARY-RESEARCH.md (internet research)

Claims from database: [X claims pre-populated / None found]

NEXT STEPS:
1. Download sources from 00-NOTEBOOKLM-SOURCE-LIST.md
2. Upload to NotebookLM
3. Run /sources to generate verification prompts
4. Verify claims and update 01-VERIFIED-RESEARCH.md
5. When 90%+ verified, run /script to write
```

---

## TOPIC-ONLY WORKFLOW (`--topic-only`)

Skip project creation, just research a topic:

1. Check VERIFIED-CLAIMS-DATABASE for existing research
2. Conduct preliminary internet research
3. Identify academic sources needed
4. Generate NotebookLM source recommendations
5. Output research summary (not saved to project folder)

**Use when:** Exploring topic viability before committing to video

---

## EXISTING PROJECT WORKFLOW (`--existing`)

Add research to an existing project:

1. **Find project:** Use glob to locate folder
2. **Check current state:** What research exists?
3. **Identify gaps:** What claims need verification?
4. **Conduct targeted research** for gaps
5. **Update 01-VERIFIED-RESEARCH.md** with new findings

**Use when:** Adding research to in-progress project

---

## Quality Gates (Enforced)

**Gate 1: Research → Script**
Cannot proceed to scripting until:
- [ ] 90%+ claims verified
- [ ] All major quotes word-for-word exact
- [ ] All archival refs precise
- [ ] All numbers have 2+ sources
- [ ] 01-VERIFIED-RESEARCH.md status: "READY TO WRITE SCRIPT"

---

## Reference Files

- **Templates:** `.claude/templates/01-VERIFIED-RESEARCH-TEMPLATE.md`
- **Research subfolder:** `.claude/templates/_RESEARCH-SUBFOLDER-TEMPLATE.md`
- **Source standards:** `.claude/REFERENCE/NOTEBOOKLM-SOURCE-STANDARDS.md`
- **Claims database:** `.claude/VERIFIED-CLAIMS-DATABASE.md`

---

## After Completion

When project setup is complete, suggest:

> "Project created! Your next step: Load sources into NotebookLM and verify claims in 01-VERIFIED-RESEARCH.md.
> When research is 90%+ verified, run `/script` to write from verified facts."

**If topic-only mode:** Suggest creating full project if topic looks viable:

> "Research complete. This topic has [X] key claims to verify.
> Ready to commit? Run `/research --new` to create the project folder."

---

## Absorbed Commands

This command consolidates functionality from:
- `/new-video` - Project creation and setup
- `/find-topic` - Topic research and validation
- `/deep-research` - Comprehensive topic research

All original functionality preserved through flags and workflow stages.
