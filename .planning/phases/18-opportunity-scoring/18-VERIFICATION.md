---
phase: 18-opportunity-scoring
verified: 2026-02-01T14:30:00Z
status: passed
score: 10/10 must-haves verified
---

# Phase 18: Opportunity Scoring & Orchestrator Verification Report

**Phase Goal:** User gets ranked topic opportunities with full context
**Verified:** 2026-02-01T14:30:00Z
**Status:** PASSED
**Re-verification:** No - initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | User can see combined opportunity score (0-100) for any keyword | VERIFIED | `opportunity.py` lines 229-233: SAW formula calculation returns 0-100 score |
| 2 | Animation-required topics return score=None with block reason | VERIFIED | `opportunity.py` lines 187-197: Hard constraint check returns `score=None, category='Blocked'` |
| 3 | Channel DNA violations are auto-rejected before scoring | VERIFIED | `opportunity.py` lines 85-121: `_violates_channel_dna()` method with clickbait, news_first, politician_focus patterns |
| 4 | Score components (demand, gap, fit) are individually visible | VERIFIED | `opportunity.py` lines 263-281: `components` dict with raw, normalized, weight, contribution for each |
| 5 | Keywords have lifecycle state tracked in database | VERIFIED | `database.py` lines 1207-1357: `set_lifecycle_state()`, `get_lifecycle_state()`, `get_keywords_by_lifecycle()` methods |
| 6 | User can run single command to get complete opportunity analysis | VERIFIED | `orchestrator.py` lines 419-495: `main()` CLI with argparse |
| 7 | User can see all decision factors in one Markdown report | VERIFIED | `orchestrator.py` lines 206-243: `generate_report()` method + `templates/opportunity_report.md.j2` (118 lines) |
| 8 | User can filter keywords by lifecycle state | VERIFIED | `orchestrator.py` lines 444-457: `--list-state` flag calls `list_by_state()` |
| 9 | User can transition keywords through lifecycle states | VERIFIED | `orchestrator.py` lines 459-470: `--transition` flag calls `transition_keyword()` |
| 10 | Stale data triggers warnings in output | VERIFIED | `opportunity.py` lines 254-255: Warning added when `data_age_days > 7`; template lines 78-80 |

**Score:** 10/10 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `tools/discovery/opportunity.py` | OpportunityScorer class with scoring formula and channel DNA filtering | VERIFIED | 349 lines, exports OpportunityScorer and CHANNEL_DNA_VIOLATIONS |
| `tools/discovery/schema.sql` | Lifecycle state columns and history table | VERIFIED | Lines 197-215: lifecycle_state, lifecycle_updated_at, opportunity_score_final, opportunity_category columns + lifecycle_history table |
| `tools/discovery/database.py` | Lifecycle state methods | VERIFIED | 1374 lines total; lines 1207-1357 implement set_lifecycle_state, get_lifecycle_state, get_keywords_by_lifecycle |
| `tools/discovery/orchestrator.py` | OpportunityOrchestrator class combining all Phase 15-17 modules | VERIFIED | 499 lines, exports OpportunityOrchestrator and main() |
| `tools/discovery/templates/opportunity_report.md.j2` | Jinja2 template for Markdown opportunity reports | VERIFIED | 118 lines, contains `opportunity_score` usage |
| `.claude/commands/discover.md` | Updated /discover command with --opportunity flag | VERIFIED | Lines 17 and 29: `--opportunity` documented |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|----|--------|---------|
| orchestrator.py | demand.py | DemandAnalyzer instance | VERIFIED | Line 57: `self.demand = DemandAnalyzer(db)` |
| orchestrator.py | competition.py | CompetitionAnalyzer instance | VERIFIED | Line 58: `self.competition = CompetitionAnalyzer()` |
| orchestrator.py | opportunity.py | OpportunityScorer instance | VERIFIED | Line 59: `self.scorer = OpportunityScorer(db)` |
| orchestrator.py | database.py | KeywordDB instance | VERIFIED | Line 103: `self.db.get_production_constraints(keyword_id)` |
| orchestrator.py | format_filters.py | evaluate_production_constraints | VERIFIED | Line 107: `constraints = evaluate_production_constraints(keyword)` |
| opportunity.py | database.py | KeywordDB methods | VERIFIED | Lines 308, 339, 342, 344: Uses `self.db._conn`, `get_lifecycle_state()`, `set_lifecycle_state()` |

**Note:** The planned key_link from opportunity.py -> format_filters.py was implemented via the orchestrator layer instead. This is a better architecture (looser coupling) - opportunity.py receives constraints as parameters rather than importing format_filters directly.

### Requirements Coverage

| Requirement | Status | Supporting Truth(s) |
|-------------|--------|---------------------|
| OPP-01: Combined opportunity score | SATISFIED | Truth 1, 4 |
| OPP-02: Production constraints weighted | SATISFIED | Truth 2 |
| OPP-03: Channel DNA auto-filter | SATISFIED | Truth 3 |
| OPP-04: Lifecycle state tracking | SATISFIED | Truth 5, 8, 9 |
| OPP-05: Markdown opportunity reports | SATISFIED | Truth 7 |

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| None found | - | - | - | - |

No TODO, FIXME, placeholder, or stub patterns detected in opportunity.py or orchestrator.py.

### Human Verification Required

### 1. CLI End-to-End Test

**Test:** Run `python tools/discovery/orchestrator.py "treaty of versailles"` from command line
**Expected:** Complete opportunity analysis with score, components, demand, competition, production sections displayed
**Why human:** Requires actual execution with API calls to verify full pipeline

### 2. Report Generation Test

**Test:** Run `python tools/discovery/orchestrator.py "dark ages myth" --report`
**Expected:** Markdown report generated with all sections (score, demand, competition, production, next steps)
**Why human:** Requires visual inspection of output formatting

### 3. Lifecycle Transition Test

**Test:** Run `python tools/discovery/orchestrator.py --transition "test keyword" RESEARCHING`
**Expected:** Error message showing valid transitions from current state
**Why human:** Requires database interaction to verify state machine

### 4. Channel DNA Blocking Test

**Test:** Run `python tools/discovery/orchestrator.py "secret history of america"`
**Expected:** BLOCKED result with "Channel DNA violation: clickbait" reason
**Why human:** Requires execution to verify filtering works end-to-end

### Gaps Summary

No gaps found. All must-haves from both 18-01-PLAN.md and 18-02-PLAN.md are verified:

- OpportunityScorer class implements SAW formula with configurable weights
- Hard constraints (animation, channel DNA) filter before scoring
- Lifecycle states tracked with transition validation
- OpportunityOrchestrator combines all Phase 15-17 modules
- CLI provides complete workflow from analysis to lifecycle management
- Markdown report template covers all decision factors
- /discover command documentation updated with --opportunity flag

---

_Verified: 2026-02-01T14:30:00Z_
_Verifier: Claude (gsd-verifier)_
