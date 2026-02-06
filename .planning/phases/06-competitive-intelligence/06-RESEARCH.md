# Phase 6: Competitive Intelligence - Research

**Completed:** 2026-01-23
**Status:** Ready for planning

---

## Executive Summary

Phase 6 transforms existing competitive intelligence assets (creator-techniques.md, COMPETITOR-TITLE-DATABASE.md, SCRIPT-STRUCTURE-ANALYSIS.md) into an **active learning system** with:
1. Use-case organized technique lookup (not creator-organized)
2. Effectiveness tracking with feedback loop
3. Gap identification with composite scoring
4. Workflow integration at research and post-publish phases

**Key insight:** The foundation is strong (1,342 lines of technique documentation). The gap is organization and feedback systems.

---

## Current State Analysis

### What Exists (Strong Foundation)

| Asset | Location | Lines | Content |
|-------|----------|-------|---------|
| Creator Techniques | `.claude/REFERENCE/creator-techniques.md` | 1,342 | 7+ creators, 40+ techniques with transcript excerpts |
| Title Database | `channel-data/COMPETITOR-TITLE-DATABASE.md` | 305 | Title patterns, VidIQ analysis, formula rankings |
| Script Structure | `channel-data/SCRIPT-STRUCTURE-ANALYSIS.md` | 407 | Opening formulas, structure templates |
| Raw Transcripts | `transcripts/` | 30+ files | Kraut, Shaun, Alex O'Connor, RealLifeLore, etc. |

### Current Organization (Creator-Centric)

```
creator-techniques.md
├── Kraut (10 techniques)
├── Shaun (13 techniques)
├── Alex O'Connor (8 techniques)
├── Knowing Better (4 techniques)
├── Historia Civilis (5 techniques)
├── Fall of Civilizations (4 techniques)
├── RealLifeLore (10 techniques)
└── Quick Reference Tables (by creator)
```

**Problem:** User wants to ask "How do I open strong?" not "What does Kraut do?"

### Desired Organization (Use-Case Centric)

```
TECHNIQUES.md (reorganized)
├── Opening Hooks
│   ├── Pattern + Exception (Kraut)
│   ├── Quote Stack Demolition (Shaun)
│   ├── Zoom In and Things Get Strange (RealLifeLore)
│   └── [effectiveness ratings]
├── Building Arguments
│   ├── Causal Chain Connectors (Kraut)
│   ├── Comparative Framing (Kraut)
│   └── [effectiveness ratings]
├── Presenting Evidence
│   ├── Quote-Heavy Primary Sources (Shaun)
│   ├── Document on Screen (Channel DNA)
│   └── [effectiveness ratings]
└── Closing
    ├── Modern Echoes (Kraut)
    ├── Let Me Be Clear (Shaun)
    └── [effectiveness ratings]
```

---

## Gap Analysis: What's Missing

### 1. Use-Case Organization
**Current:** Techniques organized by creator (Kraut section, Shaun section, etc.)
**Needed:** Techniques organized by script phase (opening, arguments, evidence, closing)
**Work:** Restructure existing content, add cross-references

### 2. Effectiveness Tracking
**Current:** No tracking of which techniques were used or how they performed
**Needed:**
- Mark techniques as "tried" with video reference
- Track retention data for sections using technique
- Personal effectiveness rating (1-5)
**Work:** Add tracking fields, create update workflow

### 3. Gap Identification System
**Current:** No systematic gap analysis
**Needed:**
- Underserved topic detection (low competition / missing angle / poor quality)
- Composite scoring (demand + competition + channel fit)
- Quick-check workflow before each video
**Work:** Create gap database, define scoring criteria

### 4. Active Creator Discovery
**Current:** Static list of 7 creators
**Needed:**
- Two tiers: similar size (1K-50K) and large channels (500K+)
- Discovery signals: outlier videos, retention, growth rate
- Non-history channels when techniques relevant
**Work:** Create discovery workflow, define criteria

### 5. Workflow Integration
**Current:** Standalone reference files, no workflow touchpoints
**Needed:**
- Research phase: Check techniques competitors used on similar topics
- Post-publish: Evaluate technique effectiveness
- Topic selection: Quick gap check
**Work:** Add commands/hooks to existing workflow

---

## Implementation Approach

### Plan 1: Reorganize Techniques by Use Case

**Input:** Existing creator-techniques.md (1,342 lines)
**Output:** TECHNIQUE-LIBRARY.md organized by script phase

**Structure:**
```markdown
# Technique Library

## Opening Hooks
### Pattern + Exception
- **Source:** Kraut
- **When to use:** Opening any myth-busting video
- **Transcript excerpt:** [actual words]
- **Effectiveness:** [rating after use]
- **Used in:** [video references]

### Quote Stack Demolition
- **Source:** Shaun
...
```

**Key decisions:**
- Keep transcript excerpts (user preference)
- Add effectiveness field (initially blank)
- Add "used in" field for tracking
- Cross-reference to original creator section

### Plan 2: Create Gap Identification System

**Output:** GAP-DATABASE.md with scoring

**Structure:**
```markdown
# Gap Database

## Scoring Criteria
- **Demand (1-5):** Search volume, comment requests
- **Competition (1-5):** Existing coverage quality (5 = no good coverage)
- **Channel Fit (1-5):** History-first, myth-busting, primary sources
- **Modern Hook (bonus +1):** Current event connection

## Active Gaps

| Topic | Demand | Competition | Fit | Hook | Total | Status |
|-------|--------|-------------|-----|------|-------|--------|
| [example] | 4 | 5 | 4 | +1 | 14 | Researching |
```

**Discovery sources:**
- Competitor comment sections
- VidIQ keyword gaps
- Academic papers without YouTube coverage
- News events without history context

### Plan 3: Create Workflow Integration

**Touchpoints:**

1. **During /research:**
   - Prompt: "Check what techniques competitors used on [topic]"
   - Auto-suggest relevant techniques from library

2. **During /script:**
   - Prompt: "Which techniques are you using?"
   - Flag if no opening hook technique selected

3. **After publishing (new command):**
   - Prompt: "Which techniques did you try? How did they perform?"
   - Update effectiveness ratings

4. **Before topic selection:**
   - Quick gap database check
   - Surface high-scoring opportunities

### Plan 4: Create Creator Discovery System

**Two-tier structure:**

**Tier 1: Style Models (large, proven)**
- Kraut, Shaun, Alex O'Connor, Knowing Better, Historia Civilis, Fall of Civilizations
- RealLifeLore, Wendover, CaspianReport (added per context)

**Tier 2: Breakout Watchers (1K-50K subs)**
- To be populated through discovery workflow
- Focus: outlier videos, fast growth, high retention

**Discovery workflow:**
1. Monthly: Check VidIQ for new channels in niche
2. When found: Note outlier signal (which video, what metric)
3. If relevant: Extract technique, add to library

---

## File Structure Recommendation

```
.claude/REFERENCE/
├── TECHNIQUE-LIBRARY.md      # [NEW] Use-case organized techniques
├── creator-techniques.md     # [KEEP] Original creator-organized (reference)
├── GAP-DATABASE.md           # [NEW] Topic gaps with scoring
└── CREATOR-WATCHLIST.md      # [NEW] Two-tier creator tracking

channel-data/
├── COMPETITOR-TITLE-DATABASE.md  # [KEEP] Title patterns
├── SCRIPT-STRUCTURE-ANALYSIS.md  # [KEEP] Structure templates
└── TECHNIQUE-USAGE-LOG.md        # [NEW] What was tried, how it performed
```

---

## Workflow Integration Points

### /research Command
Add to research workflow:
```
After preliminary research, check:
- [ ] What techniques did competitors use on this topic?
- [ ] Any gaps in existing coverage? (missing angle, poor quality)
```

### /script Command
Add to script workflow:
```
Before writing:
- [ ] Select opening hook technique from library
- [ ] Note which techniques you're intentionally using

After draft:
- [ ] Does script use ≥3 causal connectors? (Kraut standard)
- [ ] Does script include comparative framing?
```

### New: Post-Publish Evaluation
Add command or prompt after video goes live:
```
/publish --evaluate (or integrated into /status)

- Which techniques did you try?
- What was retention at technique sections?
- Personal effectiveness rating (1-5)?
- Update TECHNIQUE-USAGE-LOG.md
```

---

## Success Criteria Mapping

| Requirement | Implementation | Verification |
|-------------|----------------|--------------|
| COMP-01: Technique tracking | TECHNIQUE-LIBRARY.md + TECHNIQUE-USAGE-LOG.md | User can lookup by use case |
| COMP-02: Gap identification | GAP-DATABASE.md with composite scoring | ≥5 gaps identified with scores |

---

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Reorganization loses information | Keep original creator-techniques.md as reference |
| Effectiveness tracking becomes stale | Integrate into post-publish workflow |
| Gap database not maintained | Quick-check prompt before each video |
| Too much overhead | Keep tracking lightweight (ratings, not essays) |

---

## Recommended Plan Sequence

1. **Plan 01:** Reorganize techniques into use-case library
2. **Plan 02:** Create gap database with scoring system
3. **Plan 03:** Create workflow integration (commands/prompts)
4. **Plan 04:** Create creator discovery system

**Wave structure:**
- Wave 1: Plans 01 + 02 (can run in parallel - independent files)
- Wave 2: Plans 03 + 04 (can run in parallel - independent integrations)

---

*Research completed: 2026-01-23*
