---
deprecated: true
replaced_by: /prep --edit-guide
---

> **DEPRECATED:** This command has been replaced by `/prep --edit-guide`.
> Run `/help` to see current commands.

[Original content below for reference]
---

---
description: Generate shot-by-shot visual staging guide from A-roll transcript
---

You are creating an editing guide for filmed A-roll footage. Generate a comprehensive shot-by-shot breakdown following the **MANDATORY FORMAT** below.

## BEFORE YOU START

1. **Read the SRT file** - Get exact timestamps, total runtime, identify transcription errors
2. **Read the SCRIPT.md** - Understand argument structure and intended visuals
3. **Compare runtimes** - Script estimate vs actual SRT runtime (identifies pacing drift)
4. **Identify cut candidates FIRST** - Before shot-by-shot breakdown

---

## MANDATORY FORMAT REQUIREMENTS

**Every editing guide MUST include these elements in this order:**

### 1. HEADER WITH RUNTIME COMPARISON
```markdown
# [VIDEO TITLE] - EDITING GUIDE

**Project:** [folder-name]
**Script Estimate:** [X] min
**Actual SRT Runtime:** [Y] min
**Delta:** [+/-Z] min ([needs trimming / on target / has room])
**Date Created:** [date]
```

**Runtime Estimation:**

*Script estimate calculation:*
- Count words in SCRIPT.md (exclude stage directions, headers)
- Divide by 150 (average speaking pace for this channel)
- Result = approximate minutes

*SRT actual runtime:*
- Check last timestamp in SRT file
- This is the real recorded duration

*Delta interpretation:*
| Delta | Status | Action |
|-------|--------|--------|
| **+3 min or more** | Needs trimming | Use Priority 1 cuts first, then Priority 2 |
| **+1-3 min** | Light trimming | Priority 1 cuts should be sufficient |
| **On target (+/- 1 min)** | Good | Focus on pacing, not cutting |
| **-1 min or more** | Too short | May be rushed - check pacing, add breathing room |

[Content truncated for brevity - see original file for full content]
