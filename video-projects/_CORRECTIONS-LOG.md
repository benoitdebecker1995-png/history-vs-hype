# Corrections Log - History vs Hype

**Purpose:** Document errors discovered pre/post-publication to prevent repeats
**Last Updated:** 2026-07-22

---

## Pre-Publication Errors (Caught Before Upload)

### Volhynia (#62) — Seven completed read-alouds overlooked
**Video:** 62-volhynia-massacre-untranslated-2026
**Date Discovered:** 2026-07-22
**Stage:** Script voice pass, pre-production

**Error:**
Recommended another complete read-aloud even though the creator had already completed seven passes, T1–T7, preserved in `_adlib/` and summarized in `SCRIPT.md`.

**Root Cause:**
The latest draft and summary were read, but the underlying iteration files were not inventoried before prescribing the next step.

**Lesson:**
Before requesting another creative or validation pass, inspect the project's existing pass artifacts and feedback trail. Never make the creator repeat completed work.

---

### Volhynia (#62) — Active project misidentified as Bandera (#63)
**Video:** 62-volhynia-massacre-untranslated-2026
**Date Discovered:** 2026-07-22
**Stage:** Script voice pass, pre-production

**Error:**
The active UPA-related script was identified as the parked Bandera follow-up (#63). The user was actually preparing the Volhynia massacre video (#62) for production.

**Root Cause:**
A related Bandera handoff was treated as proof of project identity before opening the supplied draft and the live Volhynia project files.

**Lesson:**
Related people and organizations can span adjacent projects. Identify the live project from the supplied artifact and active project files before applying a handoff.

---
### Bir Tawil - Claimant Dates Error
**Video:** 6-bir-tawil-2025
**Date Discovered:** 2025-12-04
**Stage:** Post-filming, pre-edit

**Error:**
Script said: "A Russian radio operator declared it the Kingdom of Middle Earth in 2014"
Reality: Dmitry Zhikharev (Russian DJ) declared it in November 2017

**Root Cause:**
- Script v4.1 claimed facts were "verified via Tier 4-5 sources"
- Verification was sloppy - sources were skimmed, not cross-checked
- Zhikharev *visited* in 2014 but *declared* kingdom in 2017 - this distinction was missed
- "Radio operator" was wrong - he's a DJ

**Fix Applied:**
- Re-record "2017" to punch over "2014" in audio
- "Radio operator" vs "DJ" left as minor error

**Lesson:**
- VERBATIM rule exists for a reason - don't paraphrase from memory
- Dates require exact source quotes, not interpretation
- "Visited" vs "declared" are different actions with different dates

---

### Bir Tawil - Hala'ib Size Error
**Video:** 6-bir-tawil-2025
**Date Discovered:** 2025-12-04
**Stage:** Post-filming, pre-edit

**Error:**
Audio says: "800,000 square miles"
Reality: 8,000 square miles

**Root Cause:**
- Likely misread or verbal slip during filming
- Not caught in filming review

**Fix Applied:**
- Text overlay showing "8,000 sq mi" on screen
- Visual overrides audio error

---

### Israel/Palestine (#59) — "84% of farmland" false SOURCE attribution
**Video:** 59-israel-palestine-partition-offer-2026
**Date Discovered:** 2026-07-03 (in edit)
**Stage:** Post-filming, in-edit

**Error:**
VO says: "the document's **annexes** show… the Jewish state was allocated 84% of the country's existing farmland."
Reality: the 84% is a real figure, but its source is Kattan p.152 → Khan's UN speech (A/PV.126, 28 Nov 1947) → an untitled UK-delegation paper. It is NOT in Res 181's annexes (which only draw boundaries). The on-screen card even credited "Kattan," contradicting the spoken "annexes."

**Root Cause:**
- Body prose (Beats 2–8) was drafted late / at filming; only the COLD OPEN got the line-by-line `03-FACT-CHECK` cross-check. Body VO claims were never source-audited at the sentence level.
- Attribution drift: paraphrasing "a British delegate's paper" into punchy VO "rounded it up" to the more authoritative-sounding "the plan's annexes."
- Verbatim-verification masked it: `ON-SCREEN-CARDS` verified the QUOTE + page ("✅ CLEAN") but not whether the SPOKEN sentence's source claim was right.

**Fix Applied:**
- Retired the 84%/Kattan card; replacement pickup VO + primary Sub-Cttee 2 card ("best agricultural lands… largely uncultivable"). See `05-EDITING-GUIDE` Issue #3, `ON-SCREEN-CARDS`, `01-VERIFIED-RESEARCH` C27.

**Lesson:** verify the SOURCE of a claim, not just that the number is real. "X shows/says N" must trace to the specific source that actually says it.

---

### Israel/Palestine (#59) — federal counter-offer: FALSE ALARM (checked the wrong source)
**Video:** 59-israel-palestine-partition-offer-2026
**Date:** 2026-07-03 (in edit)
**Stage:** Post-filming, in-edit

**What happened:** I flagged the VO line "a competing proposal drafted by India…" as a mis-credit (should be Lebanon/Iran per C17). On checking the actual **CUT** (`rought cut.srt`), the delivered line is *"drafted by India, Iran, and Yugoslavia"* — the accurate authors of the UNSCOP minority federal plan. So it is **defensible as delivered**; only a mild compression remains (the proposal formally tabled the night of the vote was Lebanon's). Downgraded to KEEP / optional-tighten.

**Root cause of the false alarm:** I audited the **uncut clean transcript** (which had an "India"-only take), not the **cut SRT** (what's actually in the video). The uncut transcript also mis-rendered the 84% line's wording ("annexes" vs the cut's "documents and access").

**Lesson:** for any VO / delivered-audio check, work from the **CUT SRT**, not the uncut/clean transcript — the cut is what's in the video; the uncut has different takes and transcription errors. (The 84% pickup still stands — its problem is the number's provenance, independent of wording.)

---

## Post-Publication Errors

*None yet*

---

## Error Prevention Checklist

Before filming, verify:
- [ ] All dates copied VERBATIM from sources
- [ ] All names spelled out with source
- [ ] All numbers double-checked against original
- [ ] Read script aloud checking for verbal traps (800 vs 800,000)
- [ ] Temporal distinctions preserved ("visited in X" vs "declared in Y")
- [ ] Occupations/titles exact from source (not paraphrased)

---

## Process Improvements Made

### 2025-12-04: Added RULE 4 to script-writer-v2.md

**File:** `.claude/agents/script-writer-v2.md`

**New rule:** HIGH-RISK DETAILS REQUIRE EXACT QUOTES

Dates, names, occupations, and temporal distinctions must be:
1. Copied verbatim from source (not typed from memory)
2. Include context ("visited" vs "declared" vs "claimed")
3. Verified before claiming "verified"

**Added to PRE-OUTPUT CHECKLIST:**
- Every year copied exactly from source?
- Every occupation/title exact?
- Temporal distinctions preserved?
- Name spellings copy-pasted?

**Triggered by:** Bir Tawil claimant dates error (2014 vs 2017, radio operator vs DJ)

---

### 2026-07-03: Fact-check the COMPLETE script before filming (primary) + post-film deviation backstop

**Gap:** The pre-film fact-check (`/verify --script`) was allowed to "pass" on #59's COLD OPEN only, while Beats 2–8 were still a beat-map. The body prose was then written and filmed **without being fact-checked**. The 84% number was sitting in the locked (un-fact-checked) body script; the "annexes" word was additionally ad-libbed at the mic. The real fix is upstream — a complete pre-film check — not a new post-film gate.

**Primary fix (the real one) — coverage-completeness gate, `/verify --script` Step 0 (IMPLEMENTED 2026-07-03):** fact-check is a PRE-FILM gate and only counts if it covers the WHOLE script. `03-FACT-CHECK-VERIFICATION.md` must have verdict rows for EVERY beat; a `PENDING-DRAFT`/beat-map section = `[COVERAGE-GAP]` = NOT film-ready. The command cannot return APPROVED, and the folder cannot move to `_READY_TO_FILM/`, with an open coverage gap. A fully fact-checked complete script means there is nothing left to catch after the camera rolls.

**Secondary (backstop) — `/verify --audio` (IMPLEMENTED 2026-07-03):** for the one class Step 0 can't reach — narrator ad-libs/misreads at the mic (#59: script said "the plan *gave* 84%" → tape said "the *annexes show* 84%"). Diff delivered transcript vs locked script; meaning-changing deltas = VO pickups. Cheap subagent diffs, Opus adjudicates. Recommended, not a hard gate.

**Triggered by:** #59 "84%" provenance error — the number sat in the un-fact-checked body script (the Step-0 failure this gate fixes). (A separately-flagged "India" line proved defensible once checked against the actual cut — see the false-alarm entry above; lesson: audit the CUT SRT, not the uncut transcript.)

---

### 2026-07-22: Define the disputed labels before testing the evidence

**Video:** 62-volhynia-massacre-untranslated-2026

**Failure:** The referee rewrite stated “Ukraine’s case,” “Poland’s case,” and a three-part evidence test before explaining the actual historiographical dispute: genocide, organized ethnic cleansing without the genocide label, or a two-sided Polish-Ukrainian war. It repeated the missing-order synthesis and inserted relevant facts without explaining why the viewer needed them at that moment.

**Rule:** First define what each position claims and why the label changes the burden of proof. Then let the evidence answer one live question at a time. Background, reconciliation, archive-access, and memory-politics beats need explicit causal jobs. Introduce named historians before quoting their verdicts. Archival chronology may rebut “later fabrication,” but cannot by itself prove clean interrogation wording or personal dishonesty.





---

### 2026-07-22: Line comments are diagnostic evidence, not a punch list

**Video:** 62-volhynia-massacre-untranslated-2026

**Failure:** Treated the creator’s annotations as isolated sentences to repair. Their repetition—“why?”, “why is this here?”, “who are these?”, “we already said this,” and “this does not sound like me”—was a coherent diagnosis of the script’s underlying reasoning and presentation model.

**Rule:** Infer the creator’s governing priorities before rewriting: causal necessity; audience orientation before abstraction; fair steelmanning followed by an evidence-weighted verdict; strict separation of document, inference, and accusation; named authority with relevance explained; no repeated synthesis; and spoken prose that discovers the argument with the viewer instead of announcing a formal framework. Apply these rules to the whole script, including places the creator did not mark.
