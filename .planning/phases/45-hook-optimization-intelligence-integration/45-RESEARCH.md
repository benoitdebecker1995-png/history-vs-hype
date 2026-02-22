# Phase 45: Hook Optimization & Intelligence Integration - Research

**Researched:** 2026-02-21
**Domain:** Prompt engineering — adding Rule 19 to script-writer-v2.md agent and wiring youtube-intelligence.md advisory into /script, /prep, /publish commands
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

- **Hook structure (Rule 19):** cold fact → myth → contradiction → payoff for first 60 seconds
- **Rule 19 flexibility:** must adapt to territorial vs ideological vs untranslated video types
- **Rule 19 integration:** must integrate naturally with existing Rules (especially Rule 1, Rule 6, Rule 17)
- **Retention triggers:** Rule 19 must include information gap, visual carrot, authority signals
- **Intelligence surfacing pattern:** follow Phase 44 channel-insights pattern — read file, display advisory block
- **Surfacing targets:** youtube-intelligence.md must surface during /script, /prep, /publish
- **Advisory format:** brief (2-3 lines), workflow-specific (hook tips for /script, format tips for /prep, title patterns for /publish)
- **Missing file behavior:** skip silently if intel file missing
- **Intel freshness:** reference live youtube-intelligence.md, not hardcoded assumptions
- **Staleness handling:** if data is stale (>30 days), note staleness but still use it
- **Fallback:** if no intel data at all, fall back to sensible defaults

### Claude's Discretion

- Exact hook formula variations per video type
- How Rule 19 interacts with existing Rules 1, 6, 17
- Intelligence section placement within command prompts
- Whether to combine with Phase 44's channel insights or keep separate

### Deferred Ideas (OUT OF SCOPE)

None — discussion stayed within phase scope.
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| HOOK-01 | Rule 19 in script-writer generates algorithm-optimized first 60 seconds (cold fact → myth → contradiction → payoff) | Research identifies exact placement in script-writer-v2.md, interaction with Rules 1/6/12/15/17, and formula variations per video type |
| HOOK-02 | Hook pass references YouTube Intelligence Engine data for current best practices | Research identifies what data is available in youtube-intelligence.md (algorithm mechanics, niche patterns, outlier analysis) and how to use it in Rule 19 |
| HOOK-03 | Hook includes retention triggers (information gap, visual carrot, authority signals) | Research maps existing STYLE-GUIDE patterns that deliver each trigger type; Rule 19 should reference these by section |
| INTEL-05 | Intelligence auto-surfaces relevant insights during /script, /prep, /publish generation | Research documents Phase 44 exact pattern (channel-insights.md advisory), confirms youtube-intelligence.md structure and query API, identifies insertion points in each command file |
</phase_requirements>

---

## Summary

Phase 45 has two tightly scoped deliverables: (1) a new Rule 19 in the `script-writer-v2.md` agent that structures the first 60 seconds using a cold fact → myth → contradiction → payoff formula informed by YouTube Intelligence Engine data, and (2) a brief intelligence advisory block in `/script`, `/prep`, and `/publish` commands that surfaces relevant youtube-intelligence.md insights at the right workflow moment.

Both deliverables are pure text file edits — no new Python code is required. The "Standard Stack" here is the existing prompt engineering pattern the repo already uses: Markdown `.md` agent files consumed by Claude at runtime. Phase 44 established a proven blueprint for the intelligence surfacing pattern (the channel-insights advisory block), and Phase 43 established a proven blueprint for how the agent reads the intel KB silently as background context. Phase 45 deepens both patterns.

The main design challenges are (1) making Rule 19 work across three distinct video types without becoming a rigid checklist, (2) threading Rule 19 cleanly between the already-complex Rules 1, 6, 12, and 15, and (3) writing the intel advisory block with enough specificity to be useful without being verbose.

**Primary recommendation:** Add Rule 19 to script-writer-v2.md immediately after Rule 18 (Document-Structured Mode). Wire intel advisory into /script (hook-specific), /prep (format/pacing), and /publish (title patterns) using identical structural pattern to Phase 44 channel-insights advisory. Keep both advisories separate (they serve different data sources).

---

## Standard Stack

### Core

| File | Purpose | Why Standard |
|------|---------|--------------|
| `.claude/agents/script-writer-v2.md` | Agent prompt governing all script generation | Already has Rules 1–18; Rule 19 extends this file |
| `.claude/commands/script.md` | /script command entry point | Already has KB load section; gains intel advisory |
| `.claude/commands/prep.md` | /prep command entry point | Already has channel-insights advisory from Phase 44 |
| `.claude/commands/publish.md` | /publish command entry point | Already has channel-insights advisory from Phase 44 |
| `channel-data/youtube-intelligence.md` | Live intel KB (auto-generated by /intel --refresh) | Sole data source for HOOK-02 and INTEL-05 |
| `.claude/REFERENCE/STYLE-GUIDE.md` | Style authority (Parts 6, 8, 9) | Rule 19 references Part 6.1 opening formulas and Part 8 hook patterns |
| `.claude/REFERENCE/OPENING-HOOK-TEMPLATES.md` | Fill-in-the-blank hook templates | Tier 2 reference; Rule 19 points here for specific variants |

### Supporting

| File | Purpose | When to Use |
|------|---------|-------------|
| `tools/intel/query.py` | Python query interface for intel.db | Used by /script staleness check (already wired in Phase 43) — no new usage needed |
| `channel-data/channel-insights.md` | Own-channel performance data (Phase 44) | Separate from intel advisory; keep the two distinct |

### No New Dependencies

This phase requires zero new Python files, zero new npm packages, and zero new database schema changes. All work is prompt engineering in `.md` files.

---

## Architecture Patterns

### Current State: What Already Exists

Understanding what is already built is essential to avoid duplicating work or conflicting with existing rules.

**Script-writer-v2.md existing hook-related rules:**

| Rule | Content | Interaction with Rule 19 |
|------|---------|--------------------------|
| Rule 1 (VERBATIM FACTS ONLY) | No invented facts | Rule 19 cold fact must come from research |
| Rule 6 (SPOKEN DELIVERY) | Stumble test, forbidden phrases, "Here's" limit | Rule 19 formula must pass Rule 6 spoken delivery check |
| Rule 9 (PROVEN TECHNIQUE INTEGRATION) | Opening Hook Selection table (Data Comparison, Common Knowledge Trap, Visual-First Map, Pattern + Exception, Both Extremes Wrong) | Rule 19 is the ALGORITHMIC layer on top of Rule 9 — Rule 9 picks hook TYPE, Rule 19 adds the 60-second STRUCTURE |
| Rule 12 (VOICE PATTERN APPLICATION) | Part 6.1 opening formulas mandatory | Rule 19 references Part 6.1 for video-type-specific formula choices |
| Rule 15 (CREATOR TECHNIQUE LIBRARY) | Part 8 cross-creator validated hooks | Rule 19 can reference Part 8.1 for creator-validated opening hook techniques |
| PRE-SCRIPT INTELLIGENCE section | Reads youtube-intelligence.md silently, uses for internal decisions | Rule 19 makes this silent read ACTIVE — the agent now explicitly maps intel data to hook choices |
| STEP 8 (Hook Strategy) in Reasoning Framework | Current hook strategy: 0:00-0:05 direct thesis, 0:05-0:15 myth + stakes, 0:15-0:30 evidence promise | Rule 19 replaces/supersedes STEP 8 as the canonical hook structure; they should be harmonized |

**Key insight on Rule 9 vs Rule 19:** Rule 9 Section A ("Opening Hook Selection") picks a hook TYPE based on video category. Rule 19 should be the structural overlay that takes whatever hook type was selected and wraps it in the cold fact → myth → contradiction → payoff four-beat structure within 60 seconds. They are complementary, not competing.

**Key insight on STEP 8 vs Rule 19:** STEP 8 in the Reasoning Framework gives a timing breakdown (0:00-0:05, 0:05-0:15, 0:15-0:30) that partially overlaps with what Rule 19 will specify. The planner should decide whether to update STEP 8 to reference Rule 19, or leave STEP 8 as a brief placeholder and make Rule 19 the full specification.

**Phase 43 decision note (from 43-03-SUMMARY.md):**
> "PRE-SCRIPT INTELLIGENCE in script-writer-v2 is 'light integration' — reads as silent background context, does not display KB dump; Phase 45 deepens with Rule 19"

This means Phase 43 intentionally left PRE-SCRIPT INTELLIGENCE as shallow. Phase 45 is supposed to deepen it — Rule 19 is where the deepening happens.

### Pattern 1: Rule 19 Structure

**What:** A numbered rule in script-writer-v2.md that governs the first 60 seconds of any script using a four-beat structure, with video-type variations and intelligence data integration.

**Four-beat formula (from CONTEXT.md):**
1. **Cold fact** — A specific, surprising, verified fact stated without commentary (first ~10 seconds)
2. **Myth** — The common belief that seems to contradict or explain the fact (next ~10 seconds)
3. **Contradiction** — The gap between the myth and reality; why the myth fails (next ~15 seconds)
4. **Payoff** — What the viewer will discover; the stakes; why this matters NOW (final ~25 seconds)

**Retention triggers to embed within the four beats:**
- **Information gap** (Loewenstein gap theory): Create a question the viewer wants answered by the end. Usually introduced in the Contradiction beat: "But what actually caused this?" or "So why did they sign it?"
- **Visual carrot**: Promise B-roll that will appear — a map, a document scan, a graph. "I found the original treaty. Here's what it actually says." This is what keeps the viewer watching past the hook.
- **Authority signal**: Establish credibility within first 60 seconds. "I read the original [document/archive/academic source]." This is the "I went to the primary sources" moment.

**Video-type variations (Claude's discretion — these are research findings, not locked decisions):**

| Video Type | Cold Fact | Myth | Contradiction | Payoff |
|-----------|-----------|------|---------------|--------|
| Territorial | Current military/legal event with precise numbers (Essequibo pattern: "700 meters", "200,000 barrels") | Common belief about which country "owns" the area | Document/treaty that shows something different | ICJ ruling, referendum, or ongoing stakes |
| Ideological | Specific historical statistic that challenges the myth (Dark Ages: literacy rates; Crusades: specific chronicle) | The modern political claim/narrative this fact challenges | What academic sources actually show (quote stack setup) | How this myth is currently shaping policy/belief |
| Untranslated evidence | A line from the untranslated document that contradicts its English reputation | What English sources say the document says | What the original language actually says | Why the mistranslation has modern consequences |

**Relationship map (for Rule 19 to reference):**
- Rule 9, Section A → Pick hook TYPE (map hook for territorial, common knowledge trap for ideological)
- Rule 12 → Pick FORMULA from Part 6.1 matching video type
- Rule 15 → Check Part 8.1 for cross-creator validated hook techniques
- Rule 19 (new) → Apply FOUR-BEAT STRUCTURE within 60 seconds regardless of which hook type/formula is used

**Template for Rule 19:**

```
### RULE 19: ALGORITHM-OPTIMIZED HOOK (60-Second Structure)

**Activate for:** ALL scripts. This rule governs the first 60 seconds.

**Relationship to existing rules:**
- Rule 9 selects hook TYPE — apply that choice WITHIN this four-beat structure
- Rule 12 selects Part 6.1 FORMULA — use that formula to execute each beat
- Rule 15 checks Part 8.1 — verify the approach is cross-creator validated
- This rule is the STRUCTURAL LAYER that wraps around Rules 9, 12, 15 hook choices

**Before writing the hook, read the PRE-SCRIPT INTELLIGENCE section (above):**
- If youtube-intelligence.md is available: extract one actionable signal per beat (see below)
- If missing or stale: use Part 6.1 formulas as the primary reference

**The four-beat structure (60 seconds total):**

**BEAT 1: Cold Fact (0:00–0:10)**
[10 seconds / ~25 words]
- One specific, verifiable fact from your research
- Stated without commentary or context
- Must be concrete: a date, a number, a document name, a place
- Source: must exist in 01-VERIFIED-RESEARCH.md
- Intelligence signal: if outlier analysis shows "numerical precision" patterns drove outliers, lead with a precise statistic
- Example formula (territorial): "[Date]. [Location]. [Military/legal action with exact measurement]."
- Example formula (ideological): "[Historian name]'s [year] analysis put [specific number] on [claim]."

**BEAT 2: Myth (0:10–0:20)**
[10 seconds / ~25 words]
- The common belief that makes the cold fact seem impossible, irrelevant, or already explained
- Frame as what "most people" or "the dominant narrative" says
- Do NOT use forbidden phrases ("You won't believe", "SHOCKING")
- Intelligence signal: if niche patterns show "colon_split" or "question" title formulas dominating, mirror that framing in the myth beat
- Example formula: "But [most people / the popular story / the common assumption] says [myth]."

**BEAT 3: Contradiction (0:20–0:35)**
[15 seconds / ~37 words]
- The specific gap between the myth and reality
- Introduce the information gap: leave a question unanswered that the video will resolve
- Include the visual carrot: promise a document, map, or data that will appear
- Example formula: "But [document / study / primary source] shows something different. [What it shows]. That's the question this video answers."

**BEAT 4: Payoff (0:35–1:00)**
[25 seconds / ~62 words]
- Establish authority signal: "I read the original [source type]"
- State modern stakes: why this matters NOW (2025–2026)
- Preview the video's core argument without fully revealing it
- End with a forward-looking hook: what will the viewer understand by the end?
- Intelligence signal: if algorithm mechanics shows satisfaction/session continuation as "very_high" weight, emphasize what the viewer will be able to DO with this knowledge after watching
- Example formula (territorial): "Both sides cite [document] to prove their case. So I read that [document]. [What it reveals]. Right now [modern stakes]. And the answer changes [modern implication]."
- Example formula (ideological): "So I went to the primary sources. [What I found there]. This matters today because [modern policy/belief shaped by this myth]."

**After writing hook: verify against Rule 6 spoken delivery check**
- Read aloud: does it pass the stumble test?
- Count "Here's": 60-second hook should use 0–1 "Here's" maximum (budget 2–4 for full script)
- No forbidden phrases from Part 1

**Intelligence integration (how to use PRE-SCRIPT INTELLIGENCE data in this rule):**

| KB Section | Hook Beat | How to Use |
|------------|-----------|------------|
| Algorithm Mechanics → Satisfaction Signals | Beat 4 (Payoff) | If "very_high", emphasize viewer takeaway / what they'll be able to explain after watching |
| Niche Patterns → Title Formulas | Beat 2 (Myth) | Mirror the dominant title formula in how you frame the myth — colon_split framing works as a myth statement |
| Outlier Analysis → why outliers succeeded | Beat 1 (Cold Fact) | If outlier used "numerical precision" or "legal fiction" pattern, open with a precise number or legal status |
| Competitor Landscape → what's being covered | Beat 2 (Myth) | If competitors just covered the myth angle, differentiate by making your Cold Fact even more specific |

**If no intelligence data available:** Fall back to Part 6.1 formulas + Part 8.1 patterns as sole reference. Do not fabricate intelligence signals.
```

### Pattern 2: Intel Advisory Block in /script, /prep, /publish

**What:** A brief (2-3 line) advisory extracted from youtube-intelligence.md, displayed before the main workflow output of each command.

**Phase 44 established the exact template for this pattern:**

```
## [Source] Advisory (Auto-run)

Before generating output, check for [data source]:

1. Read `[data file]` if it exists
2. Use as **internal context** for decisions — do NOT dump full file to user
3. Display a brief 2-3 line advisory block:

```
--- [Advisory Name] ---
[Extract 2-3 most relevant lines for this workflow]
---
```

4. If file does not exist, skip silently — NEVER block generation on missing data
5. Insights are advisory — guide experimentation, never dictate choices
```

**For Phase 45, the same pattern applies to youtube-intelligence.md:**

| Command | Advisory Name | Focus | What to Extract |
|---------|--------------|-------|-----------------|
| `/script` | `YouTube Intelligence Advisory` | Hook + structure | Algorithm satisfaction signal weight + top outlier pattern if available + dominant niche duration |
| `/prep` | `YouTube Intelligence Advisory` | Format + pacing | Niche duration distribution + algorithm AVD signal weight |
| `/publish` | `YouTube Intelligence Advisory` | Title patterns | Top title formulas from Niche Patterns section + competitor recent activity if available |

**Placement decision (Claude's discretion):** Insert youtube-intelligence advisory AFTER the Phase 44 channel-insights advisory block in /prep and /publish. In /script, the YouTube Intelligence Check section already exists (from Phase 43) — the Phase 45 advisory should be an additional brief display line within that section (Step 2.5 after KB load), not a duplicate section.

**Staleness handling:** The intel.db/youtube-intelligence.md has its own staleness tracking (`is_stale()` already used in /script and /research). For the advisory display:
- If `last_refreshed` date in youtube-intelligence.md is >30 days ago: append "(data may be stale — run `/intel --refresh`)" to the advisory
- If file is missing entirely: skip silently (no error, no block)

**Current youtube-intelligence.md structure (verified from live file):**

```markdown
## Algorithm Mechanics
- Signal Weights table (Viewer Satisfaction: very_high, CTR: high, AVD: high, etc.)
- Pipeline Mechanics (Browse, Search, Suggested descriptions)
- Longform-Specific notes
- Satisfaction Signals summary

## Competitor Landscape
- Tracked Channels table
- Most Recent Uploads table

## Niche Patterns
- Format Stats (videos analyzed, avg duration)
- Title Formulas table (formula type, count, percentage)
- Trending Topics table

## Outlier Analysis
- (empty if no outliers detected)
```

**Advisory extraction logic per command:**

For `/script` — extract:
1. Top satisfaction signal: "Viewer Satisfaction: very_high → prioritize depth over hook brevity"
2. Top title formula from Niche Patterns (e.g., "colon_split: 30% of recent uploads")
3. Outlier pattern if available, else skip third line

For `/prep` — extract:
1. AVD signal weight: "Average View Duration: high → B-roll pacing matters"
2. Niche avg duration if available (currently shows "unknown" — display that honestly)
3. Session continuation signal if it differs from AVD

For `/publish` — extract:
1. Top 2 title formulas from Niche Patterns table
2. Recent competitor topic clusters from Trending Topics table

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Reading youtube-intelligence.md | New Python script | Read file directly in command with Path().read_text() | Phase 43 already established this pattern in /script |
| Staleness detection | New staleness function | Read "Last refreshed" date from youtube-intelligence.md header | The file already has the date embedded; parse it from the Markdown |
| Advisory display | Complex template engine | Simple Markdown text block (same as Phase 44 channel-insights) | Phase 44 shows this is sufficient |
| Hook formula library | New database or lookup | Reference existing OPENING-HOOK-TEMPLATES.md and Part 6.1 | Templates already exist — Rule 19 should POINT to them, not duplicate |
| Intelligence-to-hook mapping | Algorithmic decision tree | Plain English instructions in Rule 19 text | The agent is Claude — natural language instructions work better than decision trees |

**Key insight:** Every piece of infrastructure this phase needs already exists. The phase is about adding the missing INSTRUCTION LAYER that tells the agent how to use the infrastructure.

---

## Common Pitfalls

### Pitfall 1: Rule 19 Conflicts with Rule 9 Hook Selection

**What goes wrong:** Rule 19 specifies a four-beat structure, but Rule 9 already has an "Opening Hook Selection" table with different categories (Data Comparison, Common Knowledge Trap, Visual-First Map, etc.). The agent may apply both and produce a confused hook.

**Why it happens:** The two rules specify hook at different levels of abstraction. Rule 9 picks TYPE, Rule 19 picks STRUCTURE. Without explicit cross-referencing, the agent may treat them as competing choices.

**How to avoid:** Rule 19 must explicitly say: "Rule 9 selects the hook TYPE. Apply that selection within this four-beat structure. The two rules are complementary." Also update Rule 9 Section A to add: "See Rule 19 for the structural framework that wraps around your hook type choice."

**Warning signs:** Hook section reads like two different approaches glued together, or agent asks "which hook rule should I follow?"

### Pitfall 2: Rule 19 Cold Fact Not From Verified Research

**What goes wrong:** The agent invents or paraphrases a "cold fact" for impact rather than pulling verbatim from 01-VERIFIED-RESEARCH.md.

**Why it happens:** The four-beat formula creates pressure to start with something "shocking" — the agent may optimize for impact over accuracy.

**How to avoid:** Rule 19 must explicitly state: "The Cold Fact MUST come from 01-VERIFIED-RESEARCH.md. Check Rule 1 (VERBATIM FACTS ONLY). If no suitable cold fact exists in research, flag it — do not invent one."

**Warning signs:** Cold fact is suspiciously round-number or lacks source citation in research file.

### Pitfall 3: Intel Advisory Duplicates Channel Insights Advisory

**What goes wrong:** /prep and /publish end up with two adjacent advisory blocks that look nearly identical (one from channel-insights.md, one from youtube-intelligence.md), confusing the user about which is which.

**Why it happens:** Both advisory blocks use the same "--- [Name] ---" format. Without clear labeling, they blend.

**How to avoid:** Use distinct advisory names. Channel insights: `--- Channel Performance Context ---` (already established by Phase 44). YouTube intelligence: `--- YouTube Algorithm Intelligence ---` or similar. Also, keep the two advisories separated by at least one workflow section heading, or combine them with clear sub-headings if they naturally occur at the same point.

**Warning signs:** User feedback: "why are there two similar advisory blocks?"

### Pitfall 4: STEP 8 (Reasoning Framework) Conflicts with Rule 19

**What goes wrong:** The Reasoning Framework in script-writer-v2.md has "STEP 8: Hook Strategy" with a timing breakdown that partially overlaps with Rule 19's four-beat structure. Agent follows STEP 8 and ignores Rule 19 or vice versa.

**Why it happens:** STEP 8 was the pre-Phase-45 hook specification. Rule 19 is meant to replace/supersede it. Without updating STEP 8, both exist and potentially conflict.

**How to avoid:** When adding Rule 19, also update STEP 8 to say: "For hook structure, apply Rule 19 (Algorithm-Optimized Hook). STEP 8 is now a pointer to Rule 19." This makes the Reasoning Framework reference the Rule rather than specify duplicate logic.

**Warning signs:** STEP 8 and Rule 19 produce contradictory timing breakdowns.

### Pitfall 5: Intel Advisory Displaying Raw File Contents

**What goes wrong:** The advisory block dumps the entire youtube-intelligence.md instead of 2-3 curated lines.

**Why it happens:** Without clear extraction instructions, the agent reads the full file and outputs all of it.

**How to avoid:** The command file must specify EXACTLY what to extract. "Extract: (1) top satisfaction signal, (2) top title formula percentage, (3) outlier pattern if available." Be as specific as Phase 44 was: the Phase 44 pattern says "Extract 2-3 most relevant lines" with a concrete example. Phase 45 should provide similarly specific extraction guidance per command.

---

## Code Examples

### Advisory Block Pattern (Established by Phase 44, reuse exactly)

From `/prep` command (verified):

```markdown
## Channel Insights Context (Auto-run)

Before generating output, check for own-channel performance context:

1. Read `channel-data/channel-insights.md` if it exists
2. Use as **internal context** for decisions — do NOT dump full file to user
3. Display a brief 2-3 line advisory block:

```
--- Channel Performance Context ---
[Extract 2-3 most relevant lines from channel-insights.md for this workflow]
Example: Top format: territorial (avg 1,950 views). Best retention: 42.0%.
Low signal: ~15 videos — experiment freely.
---
```

4. If file does not exist, skip silently — NEVER block generation on missing analytics
5. Insights are advisory — guide experimentation, never dictate choices
```

Phase 45 replicates this pattern with `channel-data/youtube-intelligence.md` as source and workflow-specific extraction guidance.

### Intel Advisory (Phase 45 addition to /script)

The `/script` command already has a "YouTube Intelligence Check" section from Phase 43. Phase 45 adds a display step to Step 2:

```markdown
### Step 2: Load YouTube Intelligence KB

Read `channel-data/youtube-intelligence.md` for current algorithm and niche intelligence:

[existing code block stays]

**Step 2.5: Display Intelligence Advisory (Phase 45)**

After loading the KB, display a brief advisory block extracted from the key sections:

```
--- YouTube Algorithm Intelligence ---
[Extract from Algorithm Mechanics: top 1-2 signal weights most relevant to hook decisions]
[Extract from Niche Patterns: top title formula by percentage]
[Extract from Outlier Analysis: one pattern if available, else "No outlier patterns detected yet"]
---
```

If file is missing, skip this step silently.
If `Last refreshed` date in the file header is >30 days before today: append "(data may be stale — run `/intel --refresh`)"
```

### Phase 44 Insertion Points (Confirmed)

These are the exact points where Phase 44 inserted channel-insights advisories (confirmed by reading the live command files):

- **/prep:** After Flags table, before the first workflow section ("## EDIT GUIDE")
- **/publish:** After Flags table, before "## PRE-PUBLISH QUALITY GATES"
- **/research:** After Flags table, before first workflow section

Phase 45 youtube-intelligence advisory goes:
- **/script:** Within existing "YouTube Intelligence Check" section as Step 2.5
- **/prep:** After the Phase 44 channel-insights advisory, labeled distinctly
- **/publish:** After the Phase 44 channel-insights advisory, labeled distinctly

### Rule 19 Position in script-writer-v2.md

Current rules end at Rule 18 (DOCUMENT-STRUCTURED MODE). Rule 19 should be appended after Rule 18, before the "REASONING FRAMEWORK" section. This placement means Rule 19 activates for ALL scripts (it is not mode-specific like Rule 18).

STEP 8 in the Reasoning Framework should become a reference pointer:
```markdown
### STEP 8: Hook Strategy

**See Rule 19 (Algorithm-Optimized Hook) for the canonical 60-second structure.**

Rule 19 covers: cold fact → myth → contradiction → payoff, video-type variations, intelligence integration, and retention trigger embedding.
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Rule 9 hook type selection (no timing structure) | Rule 9 type + Rule 19 structural overlay | Phase 45 | Agent now has both WHAT and HOW for hooks |
| PRE-SCRIPT INTELLIGENCE reads KB silently, no explicit usage | Rule 19 maps specific KB sections to specific hook beats | Phase 45 | Intelligence becomes actionable, not decorative |
| No intel advisory in commands (/script, /prep, /publish) | Brief 2-3 line advisory per command | Phase 45 | User sees algorithm context at moment of production decision |
| STEP 8 specified hook timing | STEP 8 → Rule 19 pointer | Phase 45 | Single source of truth for hook structure |

---

## Open Questions

1. **Should STEP 8 be removed or just converted to a pointer?**
   - What we know: STEP 8 has a timing breakdown (0:00-0:05, 0:05-0:15, 0:15-0:30) that partially but not fully overlaps with Rule 19
   - What's unclear: Whether the existing STEP 8 timing breakdown provides value alongside Rule 19, or whether it creates confusion
   - Recommendation: Convert STEP 8 to a one-line pointer to Rule 19. The Rule 19 timing breakdown (10 sec / 10 sec / 15 sec / 25 sec) is more precise and supersedes STEP 8's version.

2. **How specific should Rule 19's "intelligence signal" instructions be?**
   - What we know: The live youtube-intelligence.md has limited data currently (30 videos analyzed, no outlier data, competitor channel list has only one test entry). The "intelligence signals" in Rule 19 may point to empty sections.
   - What's unclear: Will overly specific extraction instructions cause the agent to fail gracefully or produce errors when data is missing?
   - Recommendation: Follow the CONTEXT.md locked decision — "Fallback to sensible defaults if no intel data available at all." Rule 19 should say: "If KB section is empty or says 'No data', skip that signal — do not invent one."

3. **Separate advisories or combined in /prep and /publish?**
   - What we know: /prep and /publish already have Phase 44 channel-insights advisory. Adding a second advisory creates two adjacent blocks.
   - What's unclear: Whether combining them (one block, two data sources) is cleaner or whether distinct blocks per source is clearer
   - Recommendation: Keep separate. Channel insights = own-channel performance. YouTube intelligence = algorithm + niche patterns. These are distinct data sources and serve different decisions. Label them distinctly and let the planner decide final placement.

---

## Sources

### Primary (HIGH confidence)

- `G:/History vs Hype/.claude/agents/script-writer-v2.md` — Rules 1–18, PRE-SCRIPT INTELLIGENCE section, REASONING FRAMEWORK (including STEP 8), all quality checklists — read in full
- `G:/History vs Hype/.claude/commands/script.md` — YouTube Intelligence Check section, full command workflow — read in full
- `G:/History vs Hype/.claude/commands/prep.md` — Phase 44 channel-insights advisory pattern, full command workflow — read in full
- `G:/History vs Hype/.claude/commands/publish.md` — Phase 44 channel-insights advisory pattern, full command workflow — read in full
- `G:/History vs Hype/.claude/commands/intel.md` — /intel command, query interface — read in full
- `G:/History vs Hype/channel-data/youtube-intelligence.md` — Live KB structure, actual data content, staleness format — read in full
- `G:/History vs Hype/channel-data/channel-insights.md` — Phase 44 advisory data source, structure — read in full
- `G:/History vs Hype/.claude/REFERENCE/STYLE-GUIDE.md` — Parts 1–9: voice patterns, opening formulas, retention playbook, creator techniques — read in full
- `G:/History vs Hype/.claude/REFERENCE/OPENING-HOOK-TEMPLATES.md` — 6 hook templates with examples — read in full
- `G:/History vs Hype/.planning/phases/44-analytics-backfill-feedback-loop/44-02-PLAN.md` — Phase 44 channel-insights implementation details — read in full
- `G:/History vs Hype/.planning/phases/43-youtube-intelligence-engine/43-03-SUMMARY.md` — Phase 43 decisions, PRE-SCRIPT INTELLIGENCE light integration note — read in full
- `G:/History vs Hype/tools/intel/query.py` — Query interface API surface — read (partial)

### Secondary (MEDIUM confidence)

- `G:/History vs Hype/.planning/REQUIREMENTS.md` — Requirement definitions for HOOK-01–03, INTEL-05 — read in full
- `G:/History vs Hype/.planning/STATE.md` — Phase 43/44 decisions log — read in full
- `G:/History vs Hype/.planning/phases/45-hook-optimization-intelligence-integration/45-CONTEXT.md` — User decisions — read in full

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all files verified to exist; no new dependencies needed
- Architecture patterns: HIGH — Phase 44 channel-insights pattern directly confirmed; Rule 19 position and structure derived from reading all 18 existing rules
- Pitfalls: HIGH — conflicts with Rule 9/STEP 8 are directly verifiable from the live files; other pitfalls follow from the advisory display pattern

**Research date:** 2026-02-21
**Valid until:** Stable — these are `.md` files in a controlled repo; no external dependencies to expire. Re-research only if Phase 46 modifies script-writer-v2.md rules or command files significantly.
