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
/script --variants [project] # Generate hook/structure variants, then write script
/script --new --variants [project]  # Combine: new script with variant generation
/script --document-mode [project]  # Document-structured script (clause-by-clause walkthrough)
/script --revise [project]   # Revise existing script
/script --review [project]   # Review script for issues
/script --teleprompter [project]  # Export clean text for filming
```

## Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `--new` | Write new script from verified research | `/script --new 19-flat-earth-medieval-2025` |
| `--document-mode` | Generate clause-by-clause document walkthrough script | `/script --document-mode 35-gibraltar-treaty-utrecht-2026` |
| `--revise` | Revise existing SCRIPT.md | `/script --revise 19-flat-earth-medieval-2025` |
| `--review` | Comprehensive quality review | `/script --review 19-flat-earth-medieval-2025` |
| `--teleprompter` | Export clean text for filming | `/script --teleprompter 19-flat-earth-medieval-2025` |
| `--variants` | Generate hook and structure variants before full script | `/script --variants 35-gibraltar-treaty-utrecht-2026` |

---

## WRITE NEW SCRIPT (`--new` or default)

Generate a script using the script-writer-v2 agent.

## YouTube Intelligence Check (Auto-run Before Every Script)

Before generating any script, run the intelligence staleness check and load the KB:

### Step 1: Staleness Check

```python
import sys
sys.path.insert(0, '.')
from tools.intel.kb_store import KBStore
from pathlib import Path

if Path('tools/intel/intel.db').exists():
    s = KBStore()
    is_stale = s.is_stale()
    if is_stale:
        print('STALE')
else:
    is_stale = True
    print('NOT_INITIALIZED')
```

If stale or not initialized, run refresh before proceeding:

```python
import sys
sys.path.insert(0, '.')
from tools.intel.refresh import run_refresh, get_refresh_summary
result = run_refresh(force=True)
print(get_refresh_summary(result))
```

### Step 2: Load YouTube Intelligence KB

Read `channel-data/youtube-intelligence.md` for current algorithm and niche intelligence:

```python
from pathlib import Path
kb_path = Path('channel-data/youtube-intelligence.md')
if kb_path.exists():
    kb_content = kb_path.read_text(encoding='utf-8')
    print(kb_content)
```

Use the KB to inform script structure decisions:
- **Algorithm Mechanics:** What satisfaction signals does YouTube reward? What matters for longform?
- **Niche Patterns:** What duration is working in the niche? What title formulas dominate?
- **Competitor Landscape:** What topics are competitors covering now? What gaps exist?
- **Outlier Analysis:** What made the outlier videos succeed? Can that pattern be applied here?

**Do NOT display the KB dump to the user** — use it as internal context for structure and hook decisions.

**Advisory Display:** After loading the KB, display a brief 2-3 line advisory summarizing the most relevant intelligence for this script. Focus on algorithm priorities, niche patterns, and any outlier hook patterns. See "YouTube Intelligence Context (Auto-run)" section below for format.

## YouTube Intelligence Context (Auto-run)

Before generating output, check for YouTube algorithm and niche intelligence:

1. Read `channel-data/youtube-intelligence.md` if it exists
2. Use as **internal context** for hook and structure decisions — do NOT dump full file to user
3. Display a brief 2-3 line advisory block:

```
--- YouTube Intelligence Context ---
[Extract 2-3 most relevant lines from youtube-intelligence.md for this workflow]
Example: Algorithm priority: viewer satisfaction (very_high weight). Niche trend: 20-30min docs dominating.
Hook pattern from outliers: "legal fiction exposed" frame drove 4x median views.
---
```

4. If file does not exist, skip silently — NEVER block generation on missing intelligence
5. If last refresh date is >30 days old, add note: "(Intel last refreshed [date] — consider running /intel --refresh)"
6. Intelligence is advisory — inform hook and structure decisions, never dictate

**For /script:** Focus on:
- **Algorithm signals:** What satisfaction signals matter most right now (AVD, CTR, satisfaction surveys)
- **Hook patterns:** What hook types are working in outlier videos (from Outlier Analysis section)
- **Niche format trends:** What video lengths and formats are performing (from Niche Patterns section)
- **Competitor gaps:** What topics competitors are NOT covering (differentiation opportunities)

## Before Writing

**Read these reference files:**
- `.claude/REFERENCE/STYLE-GUIDE.md` - **AUTHORITATIVE** style reference (voice, delivery, patterns)
  - **Part 6:** Voice patterns (proven History vs Hype patterns)
  - **Part 8:** Creator technique library (cross-validated patterns from 80+ transcripts) — auto-updated with `python tools/youtube-analytics/pattern_synthesizer_v2.py --update`
  - **Part 9:** Retention playbook (data-driven retention rules) — auto-updated with `python tools/youtube-analytics/playbook_synthesizer.py --update`
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

## PRE-SCRIPT INTELLIGENCE

Before generating a script, the system automatically surfaces relevant past performance insights.

### Automatic Display

When topic type is known (territorial, ideological, fact-check, general), the system displays:
- **Topic Performance:** How this topic type has performed historically (retention, conversion)
- **Retention Lessons:** What caused viewer drop-offs in similar past videos
- **Suggested Patterns:** Which STYLE-GUIDE.md Part 6 voice patterns work best for this topic type
- **Past hook and structure choice patterns** for this topic type (from variant history)

### How to Use

The pre-script intelligence block appears automatically before script generation begins.
Use these insights to inform structure decisions:
- If past territorial videos lost viewers during treaty text → show treaty on screen instead
- If causal chains correlated with high retention → prioritize "which meant that" transitions
- If topic type has low sample size → insights flagged as "low confidence"

### Technical Details

Insights come from:
- `tools/youtube-analytics/feedback_queries.py` → `get_pre_script_insights(topic_type)`
- `tools/youtube-analytics/topic_strategy.py` → `generate_topic_strategy()`
- Past POST-PUBLISH-ANALYSIS data stored in keywords.db

### Requirements

- At least 1 past video of the same topic type must exist in the feedback database
- Run `python tools/youtube-analytics/feedback.py backfill` to populate feedback data

### Implementation (For Claude)

**Run this automatically (do not ask user):**
```bash
cd tools/youtube-analytics && python -c "
from feedback_queries import get_pre_script_insights
topic = '{topic_type}'  # Determine from user's topic (territorial, ideological, colonial, legal)
insights = get_pre_script_insights(topic)
if insights:
    print(insights)
else:
    print('No past performance insights available yet. Run: python feedback.py backfill')
"
```

**Topic type detection:** When user describes their topic, classify into: territorial, ideological, colonial, legal, general. Use this classification for the query.

**Display the insights block** at the start of your response before proceeding with script generation. This gives the user context about what worked/failed in similar past videos.

**If no insights available:** Skip silently. Do not block script generation.

### RETENTION SCORING (Post-Generation)

After script generation is complete, run retention scoring on the output:

1. Parse the generated script with ScriptParser
2. Import and call `score_all_sections(sections, topic_type)` from retention_scorer.py
3. Call `format_retention_warnings(scored_sections)` to get formatted warnings
4. Display warnings to user BEFORE finalizing script

**Output format:**
```
## RETENTION RISK ASSESSMENT

| Section | Risk | Score | Top Warning |
|---------|------|-------|-------------|
| Introduction | LOW | 0.82 | - |
| The Treaty of 1859 | HIGH | 0.38 | Section 280 words exceeds territorial avg 150 |
| Modern Consequences | LOW | 0.91 | - |

**HIGH RISK sections should be revised before filming.**
```

**Implementation for Claude:**
```python
import sys
sys.path.insert(0, 'tools/youtube-analytics')
try:
    from retention_scorer import score_all_sections, format_retention_warnings
    SCORER_AVAILABLE = True
except ImportError:
    SCORER_AVAILABLE = False

# After script generation:
if SCORER_AVAILABLE:
    from tools.production.parser import ScriptParser
    parser = ScriptParser()
    sections = parser.parse_file(script_path)
    scored = score_all_sections(sections, topic_type)
    warnings = format_retention_warnings(scored)
    # Display warnings to user
```

If retention_scorer not available, skip silently (graceful degradation).

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

### Workflow Steps

1. **Surface pre-script intelligence** (automatic)
   - Determine topic type from user input or project metadata
   - Call `get_pre_script_insights(topic_type)` to load past lessons
   - Display intelligence block to user before proceeding with script generation
   - Use insights to inform structure, pacing, and pattern choices

2. **Gather information and context** (see sections above)

3. **Generate script** using script-writer-v2 agent guidelines below

4. **Run retention scoring** on completed script and display risk assessment

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

## VARIANT GENERATION (`--variants`)

Generate opening hook and structural approach variants before writing full script.

### Flow
1. Surface past choice patterns for topic type (if any exist)
2. Generate 2-3 opening hook variants (labeled A/B/C)
3. User picks hook by letter
4. Generate 2 structural approach variants (labeled 1/2)
5. User picks structure by number
6. Proceed with full script generation using selected hook + structure

### Choice Logging
Choices are automatically logged to database for pattern recognition.
After 5+ choices, the system recommends preferred options based on your past patterns.

### Review Past Choices
```
python tools/youtube-analytics/technique_library.py --choices
python tools/youtube-analytics/technique_library.py --choices territorial
python tools/youtube-analytics/technique_library.py --choice-stats
```

---

## DOCUMENT-STRUCTURED MODE (`--document-mode`)

Generate scripts for clause-by-clause document walkthrough videos (Untranslated Evidence format).

### When to Use

Use document mode when:
- Video centers on untranslated or mistranslated primary document
- Goal is to reveal what document says in original language vs. English summaries
- Script should follow document's clause-by-clause order
- Visual format is split-screen (original left, translation right)

**Format reference:** `.claude/REFERENCE/UNTRANSLATED-EVIDENCE-FORMAT-GUIDE.md`

### Prerequisites

1. **Translation output exists:** Phase 40 translation pipeline completed
   - Formatted output file: `*-TRANSLATION-FORMATTED.md` in project folder
   - Cross-check complete (or explicitly skipped)
   - Legal annotations present
   - Surprise detection complete (optional)

2. **Translation verified:** `/verify --translation` returned GREEN or YELLOW verdict

### Workflow

**Step 1: Locate translation**
- Auto-detect: Search project folder for `*-TRANSLATION-FORMATTED.md`
- Override: Use `--translation PATH` to specify exact file

**Step 2: Parse document structure**
- Extract clauses (articles, sections, paragraphs)
- Identify surprise markers (MAJOR, NOTABLE, MINOR from surprise_detector)
- Load legal term annotations
- Determine clause ordering (document order or thematic grouping)

**Step 3: Generate script following format:**

**Structure:**
1. Cold Open (1-2 min) - Modern hook, stakes, preview
2. Document Introduction (2-3 min) - Context, translation status
3. Clause-by-Clause Walkthrough (bulk) - For each clause:
   - Context setup (talking head)
   - Read original (split-screen left)
   - Translate (split-screen right)
   - Explain significance (talking head)
   - Connect to myth (talking head)
4. Synthesis "What They Got Wrong" (3-5 min) - Recap surprises
5. Conclusion (1-2 min) - Return to hook, modern consequences

**Surprise handling:**
- Major/Notable surprises emphasized during walkthrough: "This is crucial—[reason]"
- All Major/Notable surprises recapped in Synthesis section
- Minor surprises mentioned inline only

**Original text in visual notes:**
```
[VISUAL SPLIT-SCREEN:
LEFT: Original [language] text - "[exact text]"
RIGHT: English translation - "[exact translation]"]
```

**Step 4: Quality checks**
- Every clause has 5 elements (context, read, translate, explain, connect)
- Surprises appear twice (inline + synthesis)
- Visual notes specify panel layout
- Spoken narration is natural and read-aloud friendly

### Flags

| Flag | Purpose |
|------|---------|
| `--translation PATH` | Specify translation file (overrides auto-detect) |
| `--group-thematic` | Allow thematic clause grouping instead of document order |
| `--teleprompter` | Export clean text after generation (strips visual notes) |

### Output

- **SCRIPT.md:** Full script with visual staging notes
- **SCRIPT-TELEPROMPTER.txt:** (if --teleprompter used) Clean spoken text only

### After Generation

**Proactive suggestion:**
> "Document-structured script complete. Next steps:
> 1. `/verify --script` - Fact-check before filming
> 2. `/prep --split-screen` - Generate split-screen edit guide
>
> Ready to verify? Run `/verify --script`"

### Example Usage

```bash
# Auto-detect translation in project folder
/script --document-mode 37-vichy-statut-juifs-2026

# Specify translation file explicitly
/script --document-mode 37-vichy-statut-juifs-2026 --translation path/to/translation.md

# Thematic grouping instead of document order
/script --document-mode 35-gibraltar-utrecht-2026 --group-thematic

# Generate script and export teleprompter text
/script --document-mode 37-vichy-statut-juifs-2026 --teleprompter
```

### Reference Files

- **Format guide:** `.claude/REFERENCE/UNTRANSLATED-EVIDENCE-FORMAT-GUIDE.md`
- **Agent rules:** `.claude/agents/script-writer-v2.md` Rule 18
- **Translation pipeline:** `tools/translation/cli.py`

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
