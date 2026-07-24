---
name: "source-command-script-research-pass"
description: "Full editor + head-of-research pass on a draft script — paragraph-by-paragraph NotebookLM verification (no context-economy skip), expository/predicate-drift, quote-card provenance, completeness, flow, writing polish, and script↔teleprompter lock discipline."
---

# source-command-script-research-pass

Use this skill when the user asks to run the migrated source command `script-research-pass`.

## Command Template

# /script-research-pass — the "editor + head of research" pre-lock pass

Reproduces the #58 Kurdistan 2026-06-04 pass. Acts as **script editor AND head of research**: makes the script backed by the notebook for *everything it says*, written with the channel's methods, and clean in throughflow — then leaves it one read-aloud away from lock.

## Usage
```
/script-research-pass [project]        # e.g. /script-research-pass 59-israel-palestine-partition-offer-2026
/script-research-pass [project] --research   # passes 1–3 only (notebook verification)
/script-research-pass [project] --writing    # passes 4–5 only (methods + flow)
```

## Prerequisites (check first, stop if unmet)
- `SCRIPT.md` exists in the project folder. If not (e.g. still Historian Stage A/B, no draft), STOP: "No draft script yet — this pass verifies a written script. Finish the draft first."
- A populated NotebookLM notebook for the project. Locate via `mcp__notebooklm__notebook_list` → match slug/topic. Record the notebook UUID. If `UNAUTHENTICATED`/expired: tell the user to run `! nlm login` (the `✓` UnicodeEncodeError on Windows is cosmetic — it authed), then `mcp__notebooklm__refresh_auth`; if refresh still reports stale, try the query anyway (the server often auto-detects new creds). See `memory/feedback-nlm-auth-autorecover.md`.
- Read `memory/feedback-attribution-audit.md` (3 checks) + `feedback-teleprompter-after-lock.md` before starting.

---

## PASS 1 — Paragraph-by-paragraph notebook verification (the core)

Go through `SCRIPT.md` **paragraph by paragraph**. Extract every factual claim. **No context-economy skip:** re-query every load-bearing and every on-screen claim THIS pass even if it carries a `C##` tag — the #58 lesson is that trusting prior grounding tags is exactly what hides drift. (You may skip only trivial connective prose.)

Batch by act (one `notebook_query` per act listing the act's claims as a numbered list), ≤5 calls in parallel; large results persist to a file → Read it. For each claim demand:
> `[SUPPORTED]` + verbatim quote + source/author/page · `[PARTIAL]` (state exactly what the source supports) · `[NOT FOUND]`. "Do NOT infer or use outside knowledge."

Apply all three attribution checks from `feedback-attribution-audit.md`:
- **Class A — argument attribution** (debunk TARGETS: "PERSON argued/read/treats X"): a source must show that person making that move, not merely confirm X is true.
- **Class B — expository attribution / predicate drift** (named NON-target authority/document: "[Authority]/[the treaty] said/required/established X"): the authority must assert the EXACT predicate (P2), not an adjacent P1. **HARD on every one in debunk format.** Batch one query per authority.
- **Provenance (7.8)** — every on-screen quote card matches its displayed source character-for-character; the cited source *reproduces* the verbatim (not footnote-launders it).

**Targeted re-query rule:** a first-pass `PARTIAL`/`NOT FOUND` on a load-bearing claim is a *suspicion, not a verdict* — fire a focused follow-up query naming the exact phrase + candidate sources before recommending any change. (On #58, three first-pass misses — "void before the ink was dry," Lloyd George "forgot Kurdistan," "six months" — were all verbatim on re-query.)

## PASS 2 — Completeness reconciliation
The attribution-trigger grep (Class A + B) is the master enumerator: **every entry must map to a verdict row in `03-FACT-CHECK-VERIFICATION.md`.** Any claim with no row = `[COVERAGE-GAP]`, blocks lock until rowed. (This is the gap that hid #57's Ptolemy line — zero fact-check rows.)

## PASS 3 — Modern-anchor web check
Any claim that postdates the notebook sources (a "look at [recent event]" closing anchor) is NOT in the notebook by definition → web-verify date AND content per `memory/feedback-cultural-moment-verification.md`. For I/P this is high-risk: current-events framing must be web-confirmed and dated.

---

## PASS 4 — Writing methods (the polish)
Apply the channel's methods, not generic prose-fixing:
- **Predicate precision / name only what the source names** (Rule 7) — the welding fix.
- **Attribution-tiering as neutrality** (`feedback-historian-mode.md` Rule 4 companion) — bind every contested claim to its holder and date ("most X hold…", "Al-Tabari affirmed…", "proponents of the Y reading point to…"); never hedge ("some say"), never adjudicate doctrine. **Load-bearing for the Claims-on-Trial series (#59)** — split verdicts, one weaponized claim-pair, doc on screen.
- **Baseline-before-exception** (`feedback-baseline-before-exception.md`) — every "but actually" beat gets the baseline first.
- **Concrete-first for abstract mechanisms** + **institutional anchoring** (`feedback-script-structural-architecture.md`).
- **Intellectual honesty** — keep the counter-acknowledgment hedges; do not let them get cut.

## PASS 5 — Throughflow
Run `/verify-flow-nlm [project] --flow` (the 10 narrative-flow rules + turn placement). Then check the **act handoffs** specifically: each transition should thread a callback word from the prior beat ("they had states → who *took* them"; "carve up, no king → WWI redraw"). Flag any topic-jump with no bridge.
- **Protect callback referents when cutting for length.** A back-pointer ("**that** betrayal wasn't a fluke", "rose up *again*", "this *time*") is only valid if its concrete antecedent is still on screen. Before deleting any detail as "color," scan forward for a thesis-line that calls back to it — cut the referent and the callback dangles. (#58 2026-06-10: the Bedirxan cousin-defection looked droppable but anchors "And that betrayal wasn't a fluke" three lines later. VOICE-PROFILE §Transitions, cutting-side corollary.)

---

## Applying fixes (script not yet filmed)
Edit `SCRIPT.md` directly for objective corrections (verbatim card drift, citation tags, predicate drift, restored hedges). Surface editorial choices (e.g. competing verbatim variants → pick the **most-supported**, i.e. most independently corroborated) for the user. Log every fix + every cleared suspicion in `03-FACT-CHECK-VERIFICATION.md` under a dated pass, and record attribution catches in `ATTRIBUTION-AUDIT.md`.

## Script ↔ teleprompter discipline (HARD)
`SCRIPT.md` is the single source of truth. **Do NOT create or hand-edit `SCRIPT-TELEPROMPTER.txt`** here — it is a post-lock one-way render (`feedback-teleprompter-after-lock.md`). If a teleprompter already exists and has diverged, the verified `SCRIPT.md` wins: reconcile or delete-and-regenerate-at-lock, never hand-patch. Read aloud from `SCRIPT.md` for the T1 lock gate; generate the teleprompter only after via `/script --teleprompter` (Step 0 lock gate).

## Output
A paragraph-by-paragraph verdict table (SUPPORTED/PARTIAL/NOT-FOUND + source), the list of applied fixes, surfaced editorial choices, the flow report, and a one-line gate verdict: clean-for-lock or blocking items. End by confirming the script is one read-aloud from lock, or list what blocks it.
