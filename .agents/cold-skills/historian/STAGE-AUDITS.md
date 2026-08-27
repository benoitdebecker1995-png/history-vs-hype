# Stage-Boundary Audit Checklists

Run each checklist before confirming a stage transition. Claude surfaces the checklist; user confirms each item. Transition does not lock until checklist passes.

---

## Stage A → B (Historiographical Baseline locked)

Prerequisites before entering Stage B (Source Criticism):

- [ ] `_research/00-PRELIMINARY-BRIEF.md` exists; standard narrative vs. pop-myth contrast is articulated
- [ ] `RESEARCH-VIABILITY.md` shows verdict PROCEED or VIABILITY_OVERRIDE: true
- [ ] ≥3 specificity bombs identified (per P11.1a Check B) with credible source paths
- [ ] Thesis throughline drafted (≤12 words, specific action verb, per THESIS-DISCIPLINE.md)
- [ ] `_research/COMPETITOR-GAP-ANALYSIS.md` populated (Step 7 complete)
- [ ] `_research/00-NOTEBOOKLM-SOURCE-LIST.md` lists candidate Tier 1/2 sources with full citation details

**Historian skill note:** All content in Stage A is internet-sourced (Wikipedia, news, Google Scholar). Every claim is marked ❓ / RESEARCHING. No claim may be promoted to VERIFIED before Stage C NLM grounding. Verbatim passages from books/journals encountered in Stage A go to `## Candidate Quotes (Not Yet NLM-Verified)` in `01-VERIFIED-RESEARCH.md`, not to `## VERIFIED QUOTES`.

---

## Stage B → C (Source Criticism locked)

Prerequisites before entering Stage C (Corroboration):

- [ ] All Tier 1/2 sources uploaded to NLM notebook — **user confirms** (Claude cannot verify upload directly; surfaces checklist, user ticks)
- [ ] Notebook ID recorded in `01-VERIFIED-RESEARCH.md` under `## NOTEBOOKLM SOURCES`
- [ ] Provenance check per source recorded inline in `00-NOTEBOOKLM-SOURCE-LIST.md`: author / year / edition / translator / publisher
- [ ] Internal-criticism notes per source: primary bias, proximity to events, intent/audience
- [ ] No [S→P]-tagged load-bearing claim without a documented path to acquire its primary
- [ ] Mechanism-word candidates listed in `RESEARCH-VIABILITY.md` under "Mechanism-word candidates" (for P11.1b post-ingestion check)

**Historian skill note:** Stage B is the last point before Rule 1 (NLM-anchor) becomes enforced for verbatim text. Once Stage C begins, any verbatim quote being filed must have an NLM source ID. The `## Candidate Quotes` holding pen in `01-VERIFIED-RESEARCH.md` carries Stage A/B catches forward for resolution during Stage C.

---

## Stage C → Ready-to-Script

Prerequisites before `/script` can begin:

- [ ] 90%+ claims VERIFIED (✅) in `01-VERIFIED-RESEARCH.md`
- [ ] Every ✅ claim carries: [P]/[S]/[S→P] tier + T1/T2/T3 tier-vibe + NLM source ID (or web URL if web-sourced)
- [ ] Every ✅ verbatim quote has NLM source ID OR captured web URL — no bare verbatim text
- [ ] Every ✅ claim has a `Validated-for` stamp (verbatim text / attribution origin / edition+page / numeric value)
- [ ] Mechanism word LOCKED (not SOFTEN or SWAP) in `RESEARCH-VIABILITY.md` (P11.1b complete)
- [ ] `## CANDIDATE ANGLES` section populated in `01-VERIFIED-RESEARCH.md` (P11.2 angle-discovery complete)
- [ ] `## Candidate Quotes (Not Yet NLM-Verified)` section: each entry has either been promoted to `## VERIFIED QUOTES` (after NLM round-trip) or has a LIBRARY ACQUISITION entry in `SOURCE-ACQUISITION-QUEUE.md` or has been converted to paraphrase
- [ ] No `[FLAG: *]` is outstanding in PROJECT-STATUS.md without a logged resolution

**On pass:** update `01-VERIFIED-RESEARCH.md` status line to `READY TO WRITE SCRIPT`. Lock Stage C in `## Historian Stage State` with date.

**On fail:** list the specific failing items. Do not mark Stage C locked until all pass.
