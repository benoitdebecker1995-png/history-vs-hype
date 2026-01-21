# Phase 2: Style Consolidation - Research

**Researched:** 2026-01-20
**Domain:** Script style guide consolidation and preference tracking
**Confidence:** HIGH

## Summary

Research into the existing style documentation reveals a well-developed but fragmented system. There are **9+ scattered files** containing style guidance, with significant overlap and inconsistent organization. The core challenge is not creating new rules, but consolidating existing ones into a single authoritative reference while preserving the depth of the current documentation.

The main style document (`scriptwriting-style.md`) already exists at 1,243 lines and functions as a de facto consolidated guide. The supplementary files provide extended examples and specialized context. The `script-writer-v2.md` agent references 13+ separate files before writing scripts, creating potential confusion and inconsistency.

**Primary recommendation:** Restructure `scriptwriting-style.md` as the authoritative single source, integrate key patterns from scattered files, demote remaining files to "extended examples" supplements, and bake core non-negotiable rules directly into the scriptwriter agent.

## Inventory of Scattered Style Files

### Primary Style Documents

| File | Location | Lines | Purpose | Overlap With |
|------|----------|-------|---------|--------------|
| `scriptwriting-style.md` | `.claude/REFERENCE/` | 1,243 | Comprehensive style guide (de facto main) | All below |
| `author-style.md` | `.claude/REFERENCE/` | 367 | Author-specific techniques (12 techniques) | scriptwriting-style |
| `VOICE-GUIDE.md` | `.claude/REFERENCE/` | 626 | Voice and delivery balance | USER-VOICE-PROFILE |
| `USER-VOICE-PROFILE.md` | `.claude/REFERENCE/` | 248 | User's actual speech patterns | VOICE-GUIDE |
| `USER-PREFERENCES.md` | `.claude/` | 1,832 | Mixed: working style + speaking patterns | scriptwriting-style |

### Supporting Template Files

| File | Location | Lines | Purpose |
|------|----------|-------|---------|
| `NARRATIVE-FLOW-RULES.md` | `.claude/REFERENCE/` | 286 | 10 rules for narrative flow |
| `SCRIPTWRITING-QUICK-REFERENCE.md` | `.claude/REFERENCE/` | 227 | One-page cheat sheet |
| `OPENING-HOOK-TEMPLATES.md` | `.claude/REFERENCE/` | 284 | Fill-in-the-blank templates |
| `CLOSING-SYNTHESIS-TEMPLATES.md` | `.claude/REFERENCE/` | ~200 (est) | Closing templates |
| `CREATOR-PHRASE-LIBRARY.md` | `.claude/REFERENCE/` | 291 | Natural language from creators |
| `creator-techniques.md` | `.claude/REFERENCE/` | 1,342 | Full technique documentation |
| `phase-8-5-author-voice-lock.md` | `.claude/REFERENCE/` | 233 | Pre-filming voice checks |

### Total Style Documentation
- **~5,000+ lines** across 11+ files
- Significant redundancy (USER-PREFERENCES speaking patterns duplicated in scriptwriting-style)
- Fragmented organization requires agents to read multiple files

## Key Style Patterns Extracted

### Core Non-Negotiable: Spoken Delivery

**Source:** All files agree this is the primary constraint.

| Rule | Example (Wrong) | Example (Right) |
|------|-----------------|-----------------|
| Ordinal dates | "June 16, 2014." | "On June 16th, 2014," |
| Contractions | "it is" | "it's" |
| Abbreviation expansion | "The AU" | "The African Union" |
| Define terms immediately | "estoppel" | "estoppel - a legal rule that..." |
| Flowing lists (informational) | "Britain. France. Egypt." | "Britain, France, Egypt" |
| Staccato (rhetorical only) | - | "Not a promise. Independence." |

### Voice Identity (Consolidated from 4+ files)

**Channel Voice:** Evidence-based referee between opposing camps. Not a polemicist. Not a fence-sitter. Someone who goes to the documents and reports what they actually say.

**Confidence level:** HIGH (consistent across all files)

| Voice Element | Source File | Pattern |
|---------------|-------------|---------|
| Both-extremes-wrong opening | author-style, scriptwriting-style | "One side says X. The other says Y. Both oversimplify." |
| "I went to the documents" authority | author-style | "I went to the documents. The actual treaty text." |
| Early payoff commitment | author-style | Deliver verdict within 45-60 seconds |
| Punchy declarative fragments | scriptwriting-style | "Neither was signed. It gets worse." |
| Immediate caveat insertion | author-style | "More than 35 states... Now - one caveat..." |
| Document-as-revelation | author-style | "The Nazis kept receipts for that, too." |

### Forbidden Phrases (Consensus across all files)

**Confidence level:** HIGH

```
NEVER USE:
- "Let me show you something"
- "Here's where it gets interesting"
- "Buckle up"
- "Stay with me here"
- "Here's the thing"
- "You won't believe"
- "SHOCKING"
- "Drop your thoughts below"
- "Smash that subscribe"
```

### Approved Phrases (From USER-VOICE-PROFILE and scriptwriting-style)

**Confidence level:** HIGH

```
USE:
- "This might surprise you but..."
- "The reality is..."
- "On top of that..."
- "If we are being fair..."
- "As you can see..."
- "Here's what [X] actually says." (2-4x per script max)
- "please subscribe" (polite CTAs)
```

### "Here's" Usage (Resolved conflict)

**Conflict:** USER-VOICE-PROFILE says "not banned", older guidance was more restrictive.

**Resolution (from scriptwriting-style):**
- 2-4 "Here's" per script = natural
- 10+ "Here's" per script = overuse
- Works well for document reveals: "Here's what the treaty actually says."

**Confidence level:** HIGH

## Current script-writer-v2.md Agent Structure

### Reference Files Read (13+ Files)

The agent currently reads these files before writing:

| File | Purpose |
|------|---------|
| `scriptwriting-style.md` | Complete style guide |
| `creator-techniques.md` | Full technique documentation |
| `PROVEN-TECHNIQUES-LIBRARY.md` | Copy-paste patterns |
| `retention-mechanics.md` | Hook formulas, retention triggers |
| `channel-values.md` | Brand DNA, non-negotiables |
| `breakout-retention-audit.md` | Pre-filming audit protocol |
| `NARRATIVE-FLOW-RULES.md` | 10 rules for narrative flow |
| `USER-VOICE-PROFILE.md` | User's actual voice patterns |
| `SCRIPTWRITING-QUICK-REFERENCE.md` | One-page cheat sheet |
| `OPENING-HOOK-TEMPLATES.md` | First 60 seconds templates |
| `CLOSING-SYNTHESIS-TEMPLATES.md` | Final 60-90 seconds templates |
| `CREATOR-PHRASE-LIBRARY.md` | Natural language from creators |
| `USER-PREFERENCES.md` | User's natural speaking patterns |
| `02-SCRIPT-DRAFT-TEMPLATE.md` | Output template |
| `SCRIPTWRITING-DEBUNKING-FRAMEWORK.md` | Debunking psychology |
| `FORMAT-TEMPLATES.md` | 5 signature series structures |

### Agent Rules Structure

The agent has **12 explicit rules** baked in:
1. Verbatim facts only
2. Logic bridge required
3. Audience zero (define everything)
4. High-risk details require exact quotes
5. Research files first
6. Mandatory read-aloud pass
7. Spoken delivery check
8. Natural delivery patterns
9. Debunking framework
10. Narrative flow
11. Proven technique integration
12. User voice patterns

**Observation:** Rules 6-12 largely duplicate content from reference files. The agent both references files AND has rules baked in, creating potential for inconsistency.

### Quality Checklists

The agent has **5+ separate quality checklists** at the end:
- Structure checklist
- Evidence checklist
- Steelman checklist
- Spoken Delivery checklist
- User Voice Patterns checklist
- Narrative Flow checklist
- Voice Profile Check
- Breakout & Retention Audit
- Debunking Quality Check

**Problem:** Overlapping checklists with redundant items.

## Recommended Organization for Consolidated Guide

### Proposed Structure: STYLE-GUIDE.md

```markdown
# History vs Hype Style Guide

## Part 1: Core Identity (NON-NEGOTIABLE)
- Channel voice: evidence-based referee
- Spoken delivery (must sound natural read aloud)
- Forbidden phrases (list)
- Approved phrases (list with context)

## Part 2: Spoken Delivery Rules
- Date formats
- Contractions
- Abbreviation expansion
- Term definitions
- List formatting (staccato vs flowing)
- The "Here's" rules

## Part 3: Voice Patterns
- Your transition words (But, So, Now, etc.)
- High-performance patterns (Zero/None, Stakes immediate, etc.)
- Casual asides (1-2 per script)
- Fragments for emphasis
- Signature phrases to use

## Part 4: Structure & Flow
- Opening patterns (brief, link to templates)
- Narrative flow rules (10 rules, condensed)
- Quote integration (3-step pattern)
- Transition bridges
- Section openings (concrete, not abstract)
- Closing patterns (brief, link to templates)

## Part 5: Creator Techniques (Summary)
- Kraut: causal chains
- Shaun: document-first debunking
- Alex O'Connor: intellectual honesty
- Knowing Better: source verification
- (Link to creator-techniques.md for full patterns)

## Part 6: Quality Checklist (Unified)
- Single consolidated checklist combining all current ones

## Appendices
- A: Copy-paste phrases (from CREATOR-PHRASE-LIBRARY)
- B: Opening templates (link to OPENING-HOOK-TEMPLATES)
- C: Closing templates (link to CLOSING-SYNTHESIS-TEMPLATES)
```

### File Disposition

| Current File | Disposition | Rationale |
|--------------|-------------|-----------|
| `scriptwriting-style.md` | **BECOMES** authoritative guide | Already most comprehensive |
| `author-style.md` | **MERGE** voice sections into main guide | Unique content only |
| `VOICE-GUIDE.md` | **DEMOTE** to supplement | Extended examples |
| `USER-VOICE-PROFILE.md` | **MERGE** approved/forbidden phrases | Core rules into main |
| `USER-PREFERENCES.md` | **EXTRACT** speaking patterns only | Keep working style separate |
| `NARRATIVE-FLOW-RULES.md` | **MERGE** condensed version | Keep as supplement for depth |
| `SCRIPTWRITING-QUICK-REFERENCE.md` | **KEEP** as quick reference | Different purpose (printable) |
| `OPENING-HOOK-TEMPLATES.md` | **KEEP** as template file | Link from main guide |
| `CLOSING-SYNTHESIS-TEMPLATES.md` | **KEEP** as template file | Link from main guide |
| `CREATOR-PHRASE-LIBRARY.md` | **KEEP** as appendix | Link from main guide |
| `creator-techniques.md` | **KEEP** as deep reference | Summary in main guide |

## Technical Approach for Preference Tracking

### Auto-Capture Mechanism

**Context decision:** Corrections captured directly to guide, no staging file.

**Implementation approach:**

1. **Detection pattern:** When user says "don't say X, say Y" or corrects a phrase in script feedback

2. **Capture format:**
```markdown
### [Category]
**Rule:** [Rule statement]
- Wrong: "[X]"
- Right: "[Y]"
- Rationale: [Why, if user provided]
- Added: [Date]
```

3. **Insertion location:** Add to appropriate section of STYLE-GUIDE.md based on category

4. **Categories for auto-detection:**
- Forbidden phrases (add to forbidden list)
- Approved phrases (add to approved list)
- Date formatting
- Term definitions
- Transition preferences
- Voice patterns

### Implementation Options

**Option A: Agent instruction update**
- Add rule to script-writer-v2.md: "When user corrects a phrase, add pattern to STYLE-GUIDE.md"
- Pros: Simple, immediate
- Cons: Relies on agent judgment for categorization

**Option B: Dedicated capture command**
- Create `/capture-preference` command that explicitly adds patterns
- Pros: Explicit, controlled
- Cons: Requires user to invoke

**Option C: Hybrid approach (RECOMMENDED)**
- Agent detects corrections automatically and proposes addition
- Agent asks: "Should I add this to the style guide?" before writing
- User confirms, agent adds to appropriate section

**Confidence level:** MEDIUM - Implementation depends on how reliably agent can detect correction patterns

## Scriptwriter Enforcement Approach

### Core Rules (Bake into Agent)

**These rules should be internalized in script-writer-v2.md:**

1. Spoken delivery check (mandatory read-aloud pass)
2. Forbidden phrases (grep check before output)
3. Term definition requirement (define on first use)
4. "Here's" count (2-4 max)

### Reference Rules (Keep in Guide)

**These rules should be in STYLE-GUIDE.md, referenced as needed:**

- Full creator technique patterns
- Extended phrase libraries
- Template collections
- Detailed examples

### Deviation Flagging

**Context decision:** Flag only major deviations (structural/voice), not minor wording.

**Major deviations (flag):**
- Missing spoken delivery check
- Forbidden phrase in script
- No term definitions
- Excessive "Here's" usage (>6)
- Essay voice instead of spoken voice

**Minor deviations (don't flag):**
- Slightly different transition word
- Phrase order variations
- Template customizations

## Open Questions

1. **Where to locate authoritative guide?**
   - Current `scriptwriting-style.md` is in `.claude/REFERENCE/`
   - Could rename to `STYLE-GUIDE.md` for clarity
   - Recommendation: Keep in same location, rename for authority

2. **How to handle speaking patterns in USER-PREFERENCES.md?**
   - Currently ~450 lines of speaking patterns in USER-PREFERENCES.md
   - Could merge into STYLE-GUIDE.md Part 3: Voice Patterns
   - Could keep separate but link
   - Recommendation: Merge core patterns, keep USER-PREFERENCES.md for working style only

3. **Preference capture verification?**
   - How to verify captured preferences are correct?
   - Recommendation: Agent proposes, user confirms before adding

## Sources

### Primary (HIGH confidence)
- Direct file analysis of all 11+ style files
- Pattern extraction from script-writer-v2.md agent structure
- Context from 02-CONTEXT.md phase decisions

### Secondary (MEDIUM confidence)
- Inference about what constitutes "major" vs "minor" deviations based on existing quality checklists

## Metadata

**Confidence breakdown:**
- Inventory of files: HIGH - Direct file reading
- Style patterns: HIGH - Extracted from existing documentation
- Agent structure: HIGH - Direct file reading
- Recommended organization: MEDIUM - Based on analysis, needs validation
- Preference tracking: MEDIUM - Implementation approach, untested

**Research date:** 2026-01-20
**Valid until:** 60 days (style documentation is stable)
