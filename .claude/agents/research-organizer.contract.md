# Contract: research-organizer

**Version locked:** 2026-05-05  
**Agent file:** `.claude/agents/research-organizer.md`  
**Assigned model:** Sonnet (per `.brain/methodology/gemini-routing.md`)

---

## Input shape

| Field | Type | Required | Example |
|-------|------|----------|---------|
| `preliminary_brief` | string | YES | `(Output from wiki-researcher)` |
| `extracted_claims` | string | YES | `(Output from claims-extractor)` |
| `project_path` | string | YES | `"video-projects/_IN_PRODUCTION/X"` |

**Caller:** `/research` orchestration (Transition from Phase 1 to Phase 2).

---

## Output shape

**File written to:** `{project_path}/01-VERIFIED-RESEARCH.md`

**Required H2 sections (exact strings — schema contract):**

```
## RESEARCH MISSION & UNIQUE ANGLE
## ACADEMIC SOURCE HIERARCHY (Phase 2 Sources)
## VERIFIED TIMELINE (With Source Anchors)
## CORE CLAIMS (Verified with Page Numbers)
## THE "BOTH EXTREMES" FRAMEWORK (Steel-man)
## HISTORIOGRAPHICAL PROBLEMS (What is contested?)
## PRIMARY SOURCE VISUAL MAP (B-roll list)
## MODERN RELEVANCE & HOOKS
## SMOKING GUN QUOTES (Directly from sources)
## NOTEBOOKLM EXTRACTION LOG
## REMAINING UNKNOWN GAPS
## PRODUCTION READINESS VERDICT
```

**Required header block:**
```
# Verified Research: [Topic]

**Status:** 90% Verification Threshold [Met/Not Met]
**Academic Sources:** [N] monographs + [N] peer-reviewed papers
**Primary Sources:** [N] documents identified for screen
```

---

## Downstream consumers

| Consumer | What it reads | How it uses output |
|----------|--------------|-------------------|
| `script-writer-v2` | `01-VERIFIED-RESEARCH.md` | Primary source of truth for all script claims. |
| `fact-checker` | Same file | Reference baseline for final verification. |

**Breaking change definition:** Missing "Core Claims" section or failure to provide page numbers for Tier 2 academic sources.

---

## Canonical baseline

**Project:** India-Pakistan Partition 1947  
**Status:** Phase 1 complete (internet research), Phase 2 ready (10+ academic sources identified)  
**Files present:** ✅ 01-VERIFIED-RESEARCH.md (50+ claims, both extremes identified)
**Verification status:** ~60% of claims marked ✅ from Phase 1, remaining ⏳ for Phase 2.
