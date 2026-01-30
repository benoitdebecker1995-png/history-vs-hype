---
description: Write, revise, review, or export scripts (Production Phase 1)
model: opus
---

# /script - Script Management Entry Point

Write new scripts, revise existing ones, review for issues, or export for teleprompter.

## Usage

```
/script                      # Interactive: write new or work on existing
/script --new [project]      # Write new script for project
/script --revise [project]   # Revise existing script
/script --review [project]   # Review script for issues
/script --teleprompter [project]  # Export clean text for filming
```

## Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `--new` | Write new script from verified research | `/script --new 19-flat-earth-medieval-2025` |
| `--revise` | Revise existing SCRIPT.md | `/script --revise 19-flat-earth-medieval-2025` |
| `--review` | Comprehensive quality review | `/script --review 19-flat-earth-medieval-2025` |
| `--teleprompter` | Export clean text for filming | `/script --teleprompter 19-flat-earth-medieval-2025` |

---

## WRITE NEW SCRIPT (`--new` or default)

Generate a script using the script-writer-v2 agent.

## Before Writing

**Read these reference files:**
- `.claude/REFERENCE/STYLE-GUIDE.md` - **AUTHORITATIVE** style reference (voice, delivery, patterns)
- `.claude/REFERENCE/PROVEN-TECHNIQUES-LIBRARY.md` - Hook formulas and retention techniques
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
- **`.claude/REFERENCE/SCRIPT-TO-DELIVERY-LESSONS.md`** - **NEW** Pre-filming polish (Iran Part 1 lessons)

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

See: `.claude/REFERENCE/STYLE-GUIDE.md` → Part 3 "Voice and Delivery"

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

**Proactive suggestion:** "Script complete. Run `/verify` to fact-check before filming."

---

## REVISE SCRIPT (`--revise`)

Work on an existing SCRIPT.md with specific improvements.

### Process

1. **Read current script:** Find and read SCRIPT.md
2. **Identify revision type:**
   - User feedback (specific sections to change)
   - Quality issues (from `/script --review`)
   - Fact-check findings (from `/verify`)
3. **Apply revisions** while preserving voice and structure
4. **Git tracks history** - no need for V2/V3 files

### Common Revision Types

| Type | Focus |
|------|-------|
| **Tightening** | Remove filler, redundancy, tangents |
| **Restructuring** | Reorder sections for better flow |
| **Evidence update** | Add/fix quotes and citations |
| **Voice correction** | Fix forbidden phrases, improve delivery |
| **Hook improvement** | Strengthen opening/closing |

---

## REVIEW SCRIPT (`--review`)

Comprehensive script analysis before filming. Absorbs `/review-script` functionality.

### Part 1: Forbidden Phrase Scan

Run grep for forbidden patterns:
```
(Let me show you|Here's where it gets interesting|And that's the key insight|Buckle up|Stay with me here|Here's the thing|You won't believe|SHOCKING)
```

**If found:** Flag as CRITICAL and provide rewrite.

### Part 2: Narrative Flow Check

- **Rule 1:** Terms introduced before use
- **Rule 2:** Bridge transitions between sections
- **Rule 3:** Quote integration (Setup → Quote → Implication)
- **Rule 4:** Implications after major facts
- **Rule 5:** Meta-commentary count within budget
- **Rule 6:** No repetition of same fact in different words

### Part 3: Voice Profile Check

- Approved phrases used correctly
- Formal language flagged (Furthermore → On top of that)
- Register check (educated casual, not academic)
- Read-aloud test (sentences under 25 words, contractions)

### Part 4: Structure Check

- Opening (0:00-1:00): Concrete detail, modern hook, both extremes
- Closing (final 60-90 sec): Returns to opening, answers "so what?"
- Modern relevance map (no gaps over 90 seconds)
- Both extremes pattern complete
- Steelman present

### Part 5: Retention Prediction

- Danger zones identified (0:00-0:08, 1:00-1:30, 3:00-4:00)
- Pattern interrupt check every 90-120 seconds
- Predicted retention curve

### Output Format

```markdown
## QUICK SUMMARY

**Forbidden Phrases:** [X found / Clean]
**Narrative Flow:** [X/10]
**Voice Match:** [X/10]
**Structure:** [Both Extremes / Other]
**Retention Risk:** [Low / Medium / High]

**VERDICT:** [Ready to film / Needs revision / Major issues]

## CRITICAL ISSUES (Must Fix)
[List with specific line numbers and fixes]

## IMPORTANT ISSUES (Should Fix)
[List with specific fixes]

## WHAT WORKS
[Strengths to preserve]
```

---

## TELEPROMPTER EXPORT (`--teleprompter`)

Export SCRIPT.md to clean text for filming.

### Process

1. Read SCRIPT.md from project folder
2. **Run Pre-Filming Polish checklist** (see `.claude/REFERENCE/SCRIPT-TO-DELIVERY-LESSONS.md`)
   - Cut academic attributions from flow
   - Cut "Do you see what this means?" phrases
   - Convert numbered lists to prose
   - Remove hedging words (essentially, basically, kind of)
3. Strip all markdown formatting (`#`, `**`, `[]`, etc.)
4. Strip B-roll notes (`[B-ROLL: ...]`)
5. Strip source citations (`[SOURCE: ...]`)
6. Strip metadata (target length, framing notes)
7. Preserve paragraph breaks for pacing
8. Output to SCRIPT-TELEPROMPTER.txt

### Output

- **File:** `SCRIPT-TELEPROMPTER.txt` in project folder
- **Format:** Plain text, clean paragraphs
- **Content:** Spoken words only

### Reports After Export

- Word count
- Estimated runtime (words / 150)
- Output file location

---

## Reference Files

- **Authoritative style guide:** `.claude/REFERENCE/STYLE-GUIDE.md`
- **Script template:** `.claude/templates/02-SCRIPT-DRAFT-TEMPLATE.md`
- **Narrative flow rules:** `.claude/REFERENCE/NARRATIVE-FLOW-RULES.md`
- **Voice profile:** `.claude/REFERENCE/USER-VOICE-PROFILE.md`
- **Opening templates:** `.claude/REFERENCE/OPENING-HOOK-TEMPLATES.md`
- **Closing templates:** `.claude/REFERENCE/CLOSING-SYNTHESIS-TEMPLATES.md`
- **Creator phrases:** `.claude/REFERENCE/CREATOR-PHRASE-LIBRARY.md`

---

## After Completion

When script generation completes, suggest:

> "Script saved to SCRIPT.md. Next recommended steps:
> 1. `/verify` - Run fact-check verification (recommended before filming)
> 2. `/prep --edit-guide` - Generate filming preparation guide
>
> Ready for fact-check? Run `/verify`"

**If review mode (`--review`):** Suggest based on verdict:

> **If Ready to film:** "Script passed review. Run `/verify` for fact-check before filming."
> **If Needs revision:** "Script has [X] issues to fix. Run `/script --revise` to address them."

**If teleprompter mode (`--teleprompter`):**

> "Teleprompter text exported to SCRIPT-TELEPROMPTER.txt.
> [Word count] words, estimated [X] minutes at 150 wpm.
> Ready to film!"

---

## Absorbed Commands

This command consolidates functionality from:
- Original `/script` - Script generation
- `/review-script` - Script quality review
- `/teleprompter` - Clean text export for filming

All original functionality preserved through flags.
