---
phase: 06
plan: 02
subsystem: competitive-intelligence
tags: [gap-analysis, topic-selection, prioritization]

dependency-graph:
  requires: [06-CONTEXT]
  provides: [gap-database, topic-scoring-system]
  affects: [topic-selection-workflow, VIDEO-IDEAS-PRIMARY-SOURCES]

tech-stack:
  added: []
  patterns: [composite-scoring, priority-thresholds]

key-files:
  created:
    - .claude/REFERENCE/GAP-DATABASE.md
  modified: []

decisions:
  - id: scoring-formula
    choice: "Demand + Competition + Fit + Hook (max 16)"
    rationale: "Four factors cover market opportunity (demand, competition) and channel alignment (fit, hook)"

  - id: priority-thresholds
    choice: "13-16 high, 9-12 medium, 5-8 low, <5 skip"
    rationale: "Requires strong scores across multiple factors for high priority"

  - id: underserved-definition
    choice: "Low competition OR missing angle OR poor quality"
    rationale: "From CONTEXT.md - any of three criteria qualifies as underserved"

metrics:
  duration: 3 minutes
  completed: 2026-01-23
---

# Phase 6 Plan 02: Gap Database Summary

Gap identification system with composite scoring for underserved topic prioritization.

---

## What Was Built

Created GAP-DATABASE.md providing a systematic way to identify and prioritize underserved topics for the channel.

**Key Components:**

1. **Underserved Criteria** - Topic qualifies if:
   - Low competition (few videos exist)
   - Missing angle (no primary-source/myth-busting approach)
   - Poor quality (shallow, inaccurate, or pre-2020 coverage)

2. **Composite Scoring System:**
   - Demand (1-5): Search volume, comment requests, news relevance
   - Competition (1-5): 5 = no good coverage, 1 = saturated
   - Channel Fit (1-5): History-first, myth-busting, primary sources
   - Modern Hook (+1 bonus): Current event connection 2024-2026
   - **Total: Max 16 points**

3. **Priority Thresholds:**
   - 13-16: High priority - strong opportunity
   - 9-12: Medium priority - good opportunity
   - 5-8: Low priority - passion project only
   - <5: Skip - poor fit or saturated

4. **Initial Gap Population** (7 gaps identified):

| Topic | Score | Why Underserved |
|-------|-------|-----------------|
| Diary of Merer (Pyramid Logistics) | 14 | Massive demand; NO papyrus logistics angle in existing content |
| King-Crane Commission (Ignored Map) | 14 | Syria/Iraq ongoing; 1919 document vs Sykes-Picot untouched |
| Bald's Leechbook (Medieval Medicine) | 14 | MRSA study modern hook; 9th century manuscript ignored |
| Medieval Court Rolls | 13 | Almost NO coverage; 1290 court records available |
| Viking Law Code (Gragas) | 13 | TV fluff saturated; NO legal code angle |
| Antarctic Treaty 2048 | 12 | Legal fiction pattern; deadline approaching |
| Egyptian Will of Naunakhte | 12 | 3000-year-old contract; low competition |

---

## Workflow Integration

**Quick-Check Before Topic Selection:**
1. Check GAP-DATABASE.md for high-priority gaps (13+)
2. Check VIDEO-IDEAS-PRIMARY-SOURCES for topics with sources ready
3. Score new ideas before committing
4. Mark selected topic as "In Production"

---

## Commits

| Hash | Description |
|------|-------------|
| 8c1b908 | Create gap database structure with scoring system |
| 7aac72c | Populate gap database with 7 scored opportunities |

---

## Deviations from Plan

None - plan executed exactly as written.

---

## Next Steps

1. When selecting next video topic, check GAP-DATABASE.md first
2. Add new gaps as they're discovered (competitor comments, VidIQ, academic papers)
3. Update gap status when topics move to production
4. Archive gaps when addressed or determined not viable

---

*Completed: 2026-01-23*
