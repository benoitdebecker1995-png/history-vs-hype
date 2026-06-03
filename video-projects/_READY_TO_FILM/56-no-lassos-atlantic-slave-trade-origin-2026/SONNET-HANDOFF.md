# Sonnet Handoff — #56 Post-Rewrite Quality Gates

**Created:** 2026-05-25 by Opus, end of execution session
**Purpose:** D.10 quality gates after major v3 rewrite. Two tasks: Fig Tree re-scan + 01-VERIFIED-RESEARCH.md update.

---

## Context (read first)

Today (2026-05-25) the script `02-SCRIPT-DRAFT.md` was rewritten across 9 sections per `REWRITE-PLAN-2026-05-25.md`. Both files are in:

`D:\History vs Hype\video-projects\_READY_TO_FILM\56-no-lassos-atlantic-slave-trade-origin-2026\`

User feedback during read-aloud drove the rewrite. Major changes:
- **Conceed beat:** widened from Trans-Saharan/Muslim-only (Ahmed Baba) to two-form steelman (Ahmed Baba + Olaudah Equiano Igbo primary). Equiano was uploaded to Saltwater Slavery notebook today; pp. 13-14 verbatim now on screen.
- **NEW Bridge beat:** between Evidence 1 (Zurara raid) and Mid-Pivot (João III). Fills the 80-year gap 1444→1526 with French/Davis/Lovejoy verified sources.
- **NEW Evidence Section 4 (1518 Gorrevod asiento):** promoted from B-roll to 5th document. Donnan Vol I pp. 41-42 primary on screen.
- **Romanus Pontifex section:** lowered overclaim ("engineered top-down" → "licensed the system"), added Russell p. 250 citation closing the loop on operators citing the bull as authority.
- **De Marees:** reframed with interpretation BEFORE and AFTER the quote (was a confirmation-risk issue).
- **Hook + Closing:** updated to "five documents" framing.

The rewrite plan file (`REWRITE-PLAN-2026-05-25.md`) has section-by-section detail (D.1 through D.9). Trust it as the source of truth for what changed and why.

---

## Task 1: Fig Tree prose-scan against v3

**Goal:** Diagnose any vocabulary/register regressions in the v3 script. Confirm the corporate-jargon cluster identified in v2 (engineered top-down, scaled, iterative, rewiring, architecture, retooled, supply-demand inversion, mass-commodity market, diplomatic steamroller) is cleaned up. Surface any new Fig Tree-foreign prose introduced by the rewrite.

**Notebook ID:** `f42a08bd-76ff-4612-b5c5-9411efc9bcf2` (Fig Tree — Editing Patterns & Format C Structure Analysis)

**Steps:**

1. **Rename stale v2 source** in notebook from `02-SCRIPT-DRAFT-v2-CURRENT-2026-05-24` to `ARCHIVED-02-SCRIPT-DRAFT-v2-STALE-do-not-query`. Source ID: `01c3d6a5-ac35-4fd3-a646-462efbedf1f7`.

2. **Upload current v3** using `source_add` with `source_type=text`, `wait=true`. Title: `02-SCRIPT-DRAFT-v3-CURRENT-2026-05-25`. Pass the full current `02-SCRIPT-DRAFT.md` content. (Stripping `[BRACKETED visual cues]` and `[CITATION:...]` tags is optional — the query handles them.)

3. **Run the same prose-naturalness scan query** as v2. Use the query template from `PROSE-SCAN-2026-05-24.md` PART A — same structure. Scope `source_ids` to current v3 + 26 Fig Tree transcripts.

4. **The 26 Fig Tree transcript source IDs** are in `PROSE-SCAN-2026-05-24.md` (the source_ids array used in v2 scan; just swap out the v2 script ID for the new v3 ID and remove the stale v2).

5. **Save results** to `PROSE-SCAN-2026-05-25.md` in same project folder. Format closely matches `PROSE-SCAN-2026-05-24.md`. Mark **CONVERGENT flags** explicitly — if a v2 flag survives in v3, mark it as REGRESSION. If new flags emerge from rewritten sections, mark NEW.

6. **Cross-reference with user read-aloud flags** in `PROSE-SCAN-2026-05-24.md` PART C (Opus #1-9 friction points) — note any that the v3 rewrite resolved or that survive.

**Authentication:** If NotebookLM auth expired, do NOT keep retrying. Ask user to run `! nlm login` in the prompt. Note: known cosmetic UnicodeEncodeError on Windows console at end of `nlm login` — auth succeeds despite the traceback. User can confirm by re-trying the query.

**Don't:**
- Re-litigate any v3 decisions. Just diagnose.
- Don't edit `02-SCRIPT-DRAFT.md`. The script is locked pending user's tomorrow-morning read-aloud.

---

## Task 2: Update 01-VERIFIED-RESEARCH.md

**Goal:** Single-source-of-truth alignment. Script now cites sources that aren't documented in the research file.

**New sources to add** (all verified today via Saltwater Slavery notebook query):

| Source | Page | Used in script | Saltwater notebook source ID |
|---|---|---|---|
| Howard French, *Born in Blackness* (W. W. Norton, 2021) | p. 66 | D.3 Bridge — Cadamosto/Arguim 800-1000/yr | (notebook bibliography 9) |
| Howard French, *Born in Blackness* | p. 116 | D.3 Bridge — Madeira/São Tomé prototype | (notebook bibliography 9) |
| Davis, foreword to Eltis & Richardson *Atlas of the Transatlantic Slave Trade* (Yale UP, 2010) | p. xiv | D.3 Bridge — sugar-island prototype | `80a6452a-0d52-4a5f-bd08-751417bc70e7` |
| Paul E. Lovejoy, *Transformations in Slavery*, 3rd ed. (Cambridge UP, 2012) | p. 45, Table 3.1 | D.3 Bridge — 1450-1500: 81K, 1501-1600: 338K | `c7458a61-703d-4c8b-98be-610ac7175137` |
| Lovejoy, *Transformations in Slavery* | Introduction | D.2 Conceed — transformation thesis | same ID as above |
| Elizabeth Donnan, *Documents Illustrative of the History of the Slave Trade to America*, Vol I (Carnegie 1930) | pp. 41-42, Doc 2 | D.8b Evidence 4 — 1518 Gorrevod asiento verbatim | `2350e779-8e69-4ee7-9865-94294e4e1488` |
| P. E. Russell, *Prince Henry "The Navigator": A Life* (Yale UP, 2000) | p. 250 | D.8 Evidence 3 — operators cited papal bulls | (notebook bibliography 17) |
| Olaudah Equiano, *The Interesting Narrative of the Life of Olaudah Equiano*, 3rd ed. (London, 1790) | pp. 13-14 | D.2 Conceed — Igbo inter-polity slavery primary | `cadd94eb-6fa0-4d98-901e-8b775ab3e869` |
| Patrick Manning, *Slavery and African Life* (Cambridge UP, 1990) | ch. 4 | D.7 de Marees — two-tier price (newly deployed) | (already in research file as scholarly source, mark NEWLY DEPLOYED) |

**Note:** Davis *Inhuman Bondage* p. 221 (Wolof/Bamana terms) was in the prior draft of D.2 but was REMOVED in the final upgrade swap to Equiano-only. Do NOT add it to BEAT entries; leave it where it already lives in the research file as supporting evidence not on screen.

**How to update — follow existing structural pattern:**

1. **Add new BEAT — Bridge: Raid → System (✅ VERIFIED 2026-05-25):** Mirror existing BEAT 1-4 structure. Include verbatim blocks for French p. 66 Cadamosto factory volumes, French p. 116 Madeira/São Tomé, Davis Atlas p. xiv sugar islands, Lovejoy p. 45 Table 3.1 volumes, Lovejoy intro transformation thesis. Each with `Location`, `Validated for`, `Validated against` (with Saltwater Slavery notebook source ID), `Validation date: 2026-05-25`.

2. **Add new BEAT 5 — 1518 Gorrevod Asiento (✅ VERIFIED 2026-05-25):** Mirror BEAT 4 structure exactly. Verbatim quote from Donnan Vol I pp. 41-42 Doc 2. Note: this **promotes asiento to 5th document**, breaking original "four documents" framing. Document the decision rationale (per `REWRITE-PLAN-2026-05-25.md` decision B.1, user approved 2026-05-25): asiento operationalizes the 1455 papal license; structurally important enough to override the brand promise.

3. **Update existing BEAT — Conceed enrichment (Ahmed Baba section, currently dated 2026-05-24):**
   - Note that Equiano is now PAIRED with Ahmed Baba in a two-form steelman (Trans-Saharan/Muslim + sub-Saharan inter-polity).
   - Add a sub-section: **Equiano Mi'raj-equivalent verbatim (✅ VERIFIED 2026-05-25)** with the pp. 13-14 quote, source ID `cadd94eb-6fa0-4d98-901e-8b775ab3e869`.
   - Add Equiano material held in reserve (notebook query returned 5 HIGH-confidence quotes; only pp. 13-14 is on screen — list the others as available for D.10 enrichment):
     - p. 12 — "Adultery... was sometimes punished with slavery or death"
     - p. 14 — "great sacks... applied to that infamous purpose" (foreshadows kidnapping)
     - p. 18 — "different was their condition from that of the slaves in the West Indies!"

4. **Update existing BEAT 4 — Romanus Pontifex:** Add Russell p. 250 to supporting citations section. Russell's quote: *"Henry... had much more powerful authority than tradition or the Siete partidas to justify his engagement in the slave trade. Various earlier papal bulls could be interpreted as giving him the right to take slaves in Guinea."* This is the close-the-loop citation that operators relied on the bulls. Mark validated 2026-05-25.

5. **Add pronunciation entries** to existing pronunciation list:
   - **Lorenzo de Gorrevod** — lor-EN-zoh deh gor-eh-VOHD (Italian/Savoyard, governor of Bresa)
   - **Alvise Cadamosto** — ahl-VEE-zeh kah-dah-MOH-stoh (Venetian)
   - **Olaudah Equiano** — oh-LOW-dah eh-kwee-AH-noh (anglicized standard pronunciation)

6. **Update file header status block:** Change "Phase 1 COMPLETE — all four exhibits ✅ verified" to reflect five exhibits + bridge + steelman enrichment. Update validation date to 2026-05-25. Note the v3 deltas verified.

7. **Update Atlantic-volume table** (if useful): the table currently has Atlantic peak 80K/year + 65K average. Lovejoy Table 3.1 provides additional period totals (1450-1500: 81K, 1501-1600: 338K) — could be added as additional columns or footnote to the existing table. Keep the 80K peak figure script uses.

**All entries follow** the existing `Validated for / Validated against / Validation date` pattern from BEATs 1-4. Saltwater Slavery notebook source IDs are the validation anchors. Validation date for all new entries: **2026-05-25**.

---

## Things NOT in scope for this handoff

- **Do NOT touch** `02-SCRIPT-DRAFT.md` content. Script is locked pending user's tomorrow-morning read-aloud.
- **Do NOT** re-run structure-checker-v2 agent. Different gate, separate workflow.
- **Do NOT** update `03-FACT-CHECK-VERIFICATION.md`. User will run that separately after tomorrow's read-aloud.
- **Do NOT** add 6th-document. The 5-doc framing is locked.
- **Do NOT** modify `REWRITE-PLAN-2026-05-25.md`. It's an audit-trail artifact.

---

## After both tasks complete

Report back to user with:

1. **Fig Tree v3 scan summary:**
   - Number of flags surfaced (vs 12 in v2)
   - Convergent flags (vs Opus read-aloud Opus #1-9 from `PROSE-SCAN-2026-05-24.md` PART C)
   - REGRESSIONS (v2 flags surviving in v3)
   - NEW flags from rewritten sections
   - Corpus-level observations (clean vs persistent jargon clusters)

2. **01-VERIFIED-RESEARCH.md update confirmation:**
   - Sections added/modified
   - All Saltwater Slavery notebook source IDs documented
   - Validation date set to 2026-05-25

3. **Suggest next steps:**
   - User does read-aloud + records, marks friction
   - Then 03-FACT-CHECK-VERIFICATION.md cross-check
   - Then `/prep` skill for B-roll + edit-guide
   - Then film

---

## Reference paths

- Script: `D:\History vs Hype\video-projects\_READY_TO_FILM\56-no-lassos-atlantic-slave-trade-origin-2026\02-SCRIPT-DRAFT.md`
- Research (needs update): `01-VERIFIED-RESEARCH.md` (same folder)
- Rewrite plan (audit trail): `REWRITE-PLAN-2026-05-25.md` (same folder)
- Prior Fig Tree scan (template): `PROSE-SCAN-2026-05-24.md` (same folder)
- YouTube metadata (don't touch): `YOUTUBE-METADATA.md` (same folder)
- Opener decision history (don't touch): `OPENER-DECISION.md` (same folder)
- Project status (don't touch — managed by /reconcile): `PROJECT-STATUS.md` (same folder)

## Tool reminders

- NotebookLM MCP tools are deferred — use ToolSearch with `select:mcp__notebooklm__notebook_list,mcp__notebooklm__notebook_get,mcp__notebooklm__notebook_query,mcp__notebooklm__source_add,mcp__notebooklm__source_rename` to load schemas before calling
- Key notebook IDs:
  - **Fig Tree** (prose scans): `f42a08bd-76ff-4612-b5c5-9411efc9bcf2`
  - **Saltwater Slavery** (research verification): `a7d430b1-cba8-43b4-9f86-f4ab12e5560f`
- `nlm login` is interactive — if auth expires mid-task, ask user (not Bash) to run `! nlm login`

## Model context

Opus 4.7 handled the planning + execution. Sonnet 4.6 is appropriate for these D.10 quality-gate tasks per `feedback-model-selection.md`: mechanical query interpretation + structured admin doc update. Opus reserved for tomorrow's post-read-aloud final polish where judgment calls will be needed.

---

**End of handoff.** Sonnet: begin with Task 1, ask user for `! nlm login` if needed.
