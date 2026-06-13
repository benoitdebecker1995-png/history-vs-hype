# Contract: competitor-gap

**Version locked:** 2026-05-05  
**Agent file:** `.claude/agents/competitor-gap.md`  
**Assigned model:** Sonnet (per `.brain/methodology/gemini-routing.md`)

---

## Input shape

| Field | Type | Required | Example |
|-------|------|----------|---------|
| `topic` | string | YES | `"Treaty of Tordesillas"` |
| `competitor_transcripts` | list of strings | YES | `["transcript 1", "transcript 2"]` |
| `project_path` | string | NO | `"video-projects/_IN_PRODUCTION/42-tordesillas"` |

**Caller:** `.claude/commands/research.md` (Phase 1 landscape mapping).

---

## Output shape

**File written to:** `{project_path}/_research/02-COMPETITOR-GAP-ANALYSIS.md`

**Required H2 sections (exact strings — schema contract):**

```
## COMPETITOR LANDSCAPE SUMMARY
## THE "STANDARD NARRATIVE" (What everyone says)
## COMMON VISUAL PATTERNS (B-roll tropes)
## KEY FIGURES & EVENTS (Overlap map)
## THE "YOUTUBE CONSENSUS" (Common oversimplifications)
## IDENTIFIED KNOWLEDGE GAPS
## UNDERSERVED AUDIENCE QUESTIONS
## PRIMARY SOURCE ADVANTAGES (Unused documents)
## UNIQUE ANGLE RECOMMENDATION
## CHANNEL DNA ALIGNMENT (Systems > Narratives)
## TITLING & PACKAGING OPPORTUNITIES
## STRATEGIC VERDICT
```

**Required header block:**
```
# Competitor Gap Analysis: [Topic]

**Analyzed:** [N] videos ([Channel Names])
**Total Views Sampled:** [X.XM]
**The Opportunity:** [1-sentence summary]
```

---

## Downstream consumers

| Consumer | What it reads | How it uses output |
|----------|--------------|-------------------|
| `script-writer-v2` | `02-COMPETITOR-GAP-ANALYSIS.md` | Uses "Gaps" to ensure the script doesn't just repeat what is already on YouTube. |

**Breaking change definition:** Missing any required H2 section or failure to identify at least one "Primary Source Advantage".

---

## Canonical baseline

**Project:** Tordesillas Video.  
**Gaps found:** No one mentions the exact Latin wording of the 1494 treaty or its 2025 ICJ relevance.
