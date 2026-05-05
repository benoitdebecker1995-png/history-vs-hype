# Contract: wiki-researcher

**Version locked:** 2026-05-05  
**Agent file:** `.claude/agents/wiki-researcher.md`  
**Assigned model:** Haiku (per `.brain/methodology/gemini-routing.md`)  
**Retrofit target:** Gemini handles WebFetch URL reads (Steps 1-2); Haiku assembles the structured brief

---

## Input shape

| Field | Type | Required | Example |
|-------|------|----------|---------|
| `topic` | string | YES | `"Treaty of Tripoli 1796"` |
| `project_path` | string | YES | `"video-projects/_IN_PRODUCTION/51-treaty-tripoli-article-11-2026"` |
| `hook_type` | enum: `territorial` \| `ideological` | NO | `"ideological"` |
| `modern_hook` | string | NO | `"2025 ICJ ruling on colonial-era treaties"` |

**Caller:** `.claude/commands/research.md` (line 369 — launches agent with topic + project_path)

---

## Output shape

**File written to:** `{project_path}/_research/00-PRELIMINARY-BRIEF.md`

**Required H2 sections (exact strings — schema contract):**

```
## EXECUTIVE SUMMARY
## TIMELINE
## KEY FIGURES
## CLAIMS TO VERIFY (Phase 2 Priorities)
## STANDARD NARRATIVE (What competitors will say)
## UNDEREXPLORED ANGLES (Your edge)
## MODERN RELEVANCE HOOKS (2024-2026)
## COMPETITOR LANDSCAPE
## ACADEMIC SOURCES (From Wikipedia References)
## DEBATES & CONTROVERSIES
## PRE-VERIFIED CLAIMS (From existing projects)
## RECOMMENDED NEXT STEPS
```

**Note:** `ACADEMIC SOURCES` section title may include a suffix (e.g., `+ American Diplomacy article citations`) — this is acceptable. The prefix `## ACADEMIC SOURCES` is the contract anchor.

**Required header block** (first 5 lines of file):
```
# Preliminary Brief: [Topic]

**Generated:** [date]
**Sources:** Wikipedia ([N] articles) + [N] news results + [N] competitor videos
**Time saved:** ~2-4 hours of manual browsing
```

---

## Downstream consumers

| Consumer | What it reads | How it uses output |
|----------|--------------|-------------------|
| `.claude/commands/research.md` (line 320) | `00-PRELIMINARY-BRIEF.md` full file | User reviews "Underexplored Angles" section; proceeds to Phase 2 (NotebookLM) |
| Human user | Same file | Manual review before research sprint |

**Breaking change definition:** Missing any required H2 section, or output file not written to the expected path.

---

## Canonical example

**File:** `video-projects/_IN_PRODUCTION/43-india-pakistan-partition-2026/_research/00-PRELIMINARY-BRIEF.md`  
**Sections present:** All 12 required H2 sections confirmed 2026-05-05.

---

## Retrofit notes (Phase 2.1)

**What changes after Gemini retrofit:**
- Steps 1-2 (Wikipedia WebFetch) → piped to `gemini -p` for extraction; output passed back as structured text
- Steps 3-4 (WebSearch) → remain on Haiku (search tool, not bulk read)
- Steps 5-6 (Grep + assemble) → remain on Haiku
- **Output schema: unchanged.** Same 12 sections, same file path. The diff harness at `tools/agent_contract_check.py` must pass before retrofit is merged.

**Validation procedure:**
1. Run pre-retrofit: `python tools/agent_contract_check.py --baseline video-projects/_IN_PRODUCTION/43-india-pakistan-partition-2026/_research/00-PRELIMINARY-BRIEF.md --agent wiki-researcher`
2. Apply Gemini retrofit
3. Run same topic through retrofitted agent → new output file
4. Run: `python tools/agent_contract_check.py --check <new-output-path> --agent wiki-researcher`
5. All 12 sections present = PASS. Any missing = FAIL, do not merge.
