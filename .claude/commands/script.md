---
description: Generate a video script using the proven History vs Hype formula (based on successful Vance and Essequibo videos)
---

# /script Command

Generate a script for History vs Hype using the script-writer-v2 agent.

## Before Writing

**Read these reference files:**
- `.claude/REFERENCE/scriptwriting-style.md` - Complete style guide
- `.claude/REFERENCE/retention-mechanics.md` - Hook formulas
- `.claude/REFERENCE/channel-values.md` - Brand DNA
- `.claude/USER-PREFERENCES.md` - Natural speaking patterns
- `.claude/REFERENCE/SCRIPTWRITING-DEBUNKING-FRAMEWORK.md` - Debunking psychology + public history
- `.claude/REFERENCE/NOTEBOOKLM-SCRIPTWRITING-PROMPTS.md` - Prompts for your uploaded books
- **`.claude/REFERENCE/NARRATIVE-FLOW-RULES.md`** - **MANDATORY** 10 rules for narrative flow
- **`.claude/REFERENCE/USER-VOICE-PROFILE.md`** - **MANDATORY** Forbidden/approved phrases from user's actual speech
- **`.claude/REFERENCE/SCRIPTWRITING-QUICK-REFERENCE.md`** - One-page cheat sheet (print this)
- **`.claude/REFERENCE/OPENING-HOOK-TEMPLATES.md`** - Fill-in-the-blank templates for first 60 seconds
- **`.claude/REFERENCE/CLOSING-SYNTHESIS-TEMPLATES.md`** - Fill-in-the-blank templates for final 60-90 seconds
- **`.claude/REFERENCE/CREATOR-PHRASE-LIBRARY.md`** - Natural language from Kraut, Knowing Better, Shaun, Alex O'Connor

## Format Template Selection (NEW - 2026-01-04)

**Before gathering information, identify if topic fits a signature format:**

Ask user:
```
Does this topic fit a format template?

1. ⭐ BOTH EXTREMES ARE WRONG - Two polarized online claims about same history?
2. DOCUMENT SHOWDOWN - Two competing documents for opposite claims?
3. TREATY AUTOPSY - Legal treaty with modern territorial dispute?
4. THE MAP THEY IGNORED - Documented alternative borders that were proposed?
5. SAME DAY DIFFERENT WAR - Multiple theaters on same date?
6. CUSTOM - None of the above

Which format? (Or type number)
```

**If format identified:**
- Read `.claude/REFERENCE/FORMAT-TEMPLATES.md` for full structure
- Follow template Act breakdown exactly
- Use series branding elements (title formula, intro, thumbnail)

## Gather Information

Ask the user:

1. **Topic:** What myth are you debunking?
2. **Hook Type:** Territorial (colonial → conflict) OR Ideological (myth → belief)?
3. **Modern hook:** What 2024-2025 event connects to this?
4. **Both extremes:** (if using "Both Extremes Wrong" format)
   - Extreme A (usually dismissive):
   - Extreme B (usually oversimplified):
5. **Research ready?** NotebookLM output or preliminary research?
6. **Smoking gun:** Key documents, statistics, word-for-word quotes?

## Coverage Checkpoint (Pre-Flight)

After classifying video type, check `.claude/REFERENCE/coverage-audit.md` Coverage Matrix:

| Video Type | Action |
|------------|--------|
| ✅ Sufficient | Proceed silently. No output. |
| ⚠️ Marginal | Emit one-line note with specific expansion recommendation. Proceed. |
| ❌ Underspecified | Emit short gap notice with concrete creator/video recommendations. Proceed. |

**Rules:**
- Never block output
- Never apologize
- Never ask permission
- Never repeat if user already acknowledged
- Use exact templates from coverage-audit.md

## Debunking Framework Check (NEW - 2026-01-02)

**Before writing, assess identity stake:**

| Identity Stake | Topic Examples | Framework Required? |
|----------------|----------------|---------------------|
| **High** | Territorial disputes, national founding myths, religious narratives | **MANDATORY** - Use full debunking framework |
| **Medium** | Colonial history, ideological movements, contested figures | **RECOMMENDED** - Use key principles |
| **Low** | Ancient civilizations, medieval Europe, scientific discoveries | **OPTIONAL** - Focus on historical thinking |

**If High or Medium stake, apply:**
1. **Fact-first headlines** (avoid repeating myth)
2. **Alternative explanations** (fill mental gaps, don't just negate)
3. **KISS principle** (3 key points max per section)
4. **Self-affirmation** (acknowledge shared values before corrections)
5. **Source credibility** (explain WHY myth was created)

**See:** `.claude/REFERENCE/SCRIPTWRITING-DEBUNKING-FRAMEWORK.md` for complete framework

**NotebookLM assistance:** Use prompts from `NOTEBOOKLM-SCRIPTWRITING-PROMPTS.md` for:
- Identity stake assessment (Use Case 2)
- Backfire effect prevention (Use Case 3)
- Historical thinking integration (Use Case 4)
- Trust-building language (Use Case 5)

---

## Write the Script

Use the script-writer-v2 agent guidelines:

### Hard Constraints
- **VERBATIM facts only** - Copy exactly from research
- **Logic bridges required** - Every A→B needs explicit connector
- **Audience zero** - Define every term immediately
- **Real quotes with citations** - Word-for-word from sources

### Structure
- **Opening:** Kraut sweep-then-specifics OR Alex conversational OR Historiographical problem framing
  - **For contested history:** Open with "Here's the problem: [why sources disagree]"
  - **Then introduce sources:** Name each source, when they wrote, their biases, their value
- **Evidence:** Modern relevance every 90 seconds, pattern interrupts every 2-3 min
  - **When sources contradict:** Present side-by-side with quotes on screen
- **Synthesis:** Return to both extremes, connect to present

### Quality Checklist
- [ ] Both extremes framed in opening
- [ ] Steelman section included
- [ ] Real quotes throughout with page numbers
- [ ] Filler count within budget (I think: 2-3, Now/So: 5-6)
- [ ] Read aloud for natural delivery

### Spoken Delivery (MANDATORY)
- [ ] No telegraph-style noun fragments ("Ambassadors. Embassies." → full sentence)
- [ ] Informational fragments combined into flowing sentences
- [ ] Rhetorical fragments preserved for emphasis only
- [ ] Passes the "Stumble Test" (read aloud without hesitation)

See: `.claude/REFERENCE/scriptwriting-style.md` → "SPOKEN DELIVERY RULES"

### Natural Delivery Patterns (MANDATORY - Added 2025-12-30)
- [ ] Abbreviations expanded ("African Union" not "AU")
- [ ] Parenthetical asides removed (no mid-sentence population numbers)
- [ ] Lists connected with commas (flowing, not staccato)
- [ ] "That is" for emphasis, "That's" for casual flow
- [ ] Declarative statements over rhetorical questions
- [ ] No "quote" markers before quoted text
- [ ] Explicit transitions ("The deal was this." not "The deal:")
- [ ] Personal ownership ("I found" not "they found")
- [ ] Polite CTAs ("please subscribe")

See: `.claude/USER-PREFERENCES.md` → "NATURAL DELIVERY PATTERNS" (Patterns 11-20)

## Output Location

Save to: `video-projects/[lifecycle]/[project]/SCRIPT.md`

Template: `.claude/templates/02-SCRIPT-DRAFT-TEMPLATE.md`

**Note:** Use `SCRIPT.md` as the canonical script file. Git tracks version history—no V2/V3/FINAL files needed.

## After Generation

Ask the user:
1. Does this opening grab you in 8 seconds?
2. Does the steelmanning feel fair to the other side?
3. Should I expand any section?
4. Ready for fact-checking?
