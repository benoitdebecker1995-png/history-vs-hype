---
deprecated: true
replaced_by: /script --review
---

> **DEPRECATED:** This command has been replaced by `/script --review`.
> Run `/help` to see current commands.

[Original content below for reference]
---

---
description: Act as a critical viewer and review the script for credibility, retention, and engagement issues.
---

# /review-script - Comprehensive Script Analysis

Analyze a script for structure, voice authenticity, narrative flow, and retention issues before filming.

## Reference Files (MANDATORY)

Read before reviewing:
- `.claude/REFERENCE/NARRATIVE-FLOW-RULES.md` - 10 structural rules
- `.claude/REFERENCE/USER-VOICE-PROFILE.md` - Forbidden/approved phrases
- `.claude/REFERENCE/SCRIPTWRITING-QUICK-REFERENCE.md` - Copy-paste alternatives
- `.claude/REFERENCE/OPENING-HOOK-TEMPLATES.md` - Opening templates (first 60 sec)
- `.claude/REFERENCE/CLOSING-SYNTHESIS-TEMPLATES.md` - Closing templates (final 60-90 sec)
- `.claude/REFERENCE/CREATOR-PHRASE-LIBRARY.md` - Natural phrases from Kraut, Knowing Better, Shaun, Alex O'Connor
- `.claude/REFERENCE/scriptwriting-style.md` - Voice patterns
- `.claude/REFERENCE/retention-mechanics.md` - Retention triggers

---

## PART 1: FORBIDDEN PHRASE SCAN (Do First)

**Run grep for these patterns:**
```
(Let me show you|Here's where it gets interesting|And that's the key insight|Buckle up|Stay with me here|Here's the thing|You won't believe|SHOCKING)
```

**If found -> Flag as CRITICAL and provide rewrite using approved alternatives.**

### Forbidden Phrases
| Phrase | Replacement |
|--------|-------------|
| "Let me show you" | "Here's how..." / "As you can see..." |
| "Here's the thing" | "The reality is..." |
| "Buckle up" | (just cut it) |
| "Here's where it gets interesting" | "And that's when..." |
| "And that's the key insight" | "This is crucial." |
| "Stay with me here" | (just cut it) |

[Content truncated for brevity - see original file for full content]
