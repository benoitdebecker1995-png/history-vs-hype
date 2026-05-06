# Contract: fact-checker

**Version locked:** 2026-05-05  
**Agent file:** `.claude/agents/fact-checker.md`  
**Assigned model:** Sonnet (per `.brain/methodology/gemini-routing.md`)

---

## Input shape

| Field | Type | Required | Example |
|-------|------|----------|---------|
| `script_content` | string | YES | `"[Full script draft]"` |
| `verified_research` | string | YES | `(Content of 01-VERIFIED-RESEARCH.md)` |
| `project_path` | string | YES | `"video-projects/_IN_PRODUCTION/X"` |

**Caller:** `/verify` command or manual trigger after `02-SCRIPT-DRAFT.md` is complete.

---

## Output shape

**File written to:** `{project_path}/03-FACT-CHECK-VERIFICATION.md`

**Required H2 sections (exact strings — schema contract):**

```
## VERIFICATION SUMMARY (Pass/Fail)
## TIER 1: PRIMARY SOURCE MATCHES (100% Accuracy)
## TIER 2: ACADEMIC CONSENSUS VALIDATION
## QUOTE ACCURACY AUDIT
## STATISTICAL & DATA VERIFICATION
## CONTESTED CLAIMS & NUANCE CHECK
## VISUAL EVIDENCE ALIGNMENT (Script vs Research)
## FLAG: UNSOURCED ASSERTIONS
## FLAG: OVERSIMPLIFICATION RISKS
## HISTORIOGRAPHICAL FRAMING CHECK
## FINAL CORRECTIONS REQUIRED
## VERDICT & SIGN-OFF
```

**Required header block:**
```
# Fact-Check Verification Report: [Project Name]

**Date:** [date]
**Verification Status:** [APPROVED / PENDING REVISIONS / FAILED]
**Accuracy Score:** [X]%
**Critical Errors Found:** [N]
```

---

## Downstream consumers

| Consumer | What it reads | How it uses output |
|----------|--------------|-------------------|
| Human Producer | `03-FACT-CHECK-VERIFICATION.md` | Final quality gate before filming. |
| `script-writer-v2` | Same file | Used for "Red-to-Green" revision loop if failed. |

**Breaking change definition:** Missing the "VERDICT & SIGN-OFF" section or failing to flag a claim that exists in the script but is missing from research.

---

## Canonical baseline

**Project:** Crusades myth-check fact-video  
**Script:** 02-SCRIPT-DRAFT.md (1,847 words, 12:34 runtime)  
**Claims verified:** 47 total  
**Status breakdown:** ✅ 42 verified (2+ sources), ⚠️ 3 needs additional sources, ❌ 2 unverifiable  
**Verdict:** NEEDS REVISION (2 unverifiable claims must be removed or re-sourced before filming)
