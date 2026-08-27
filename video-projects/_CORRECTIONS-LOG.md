# Corrections Log - History vs Hype

**Purpose:** Document errors discovered pre/post-publication to prevent repeats
**Last Updated:** 2026-08-11

---

## Pre-Publication Errors (Caught Before Upload)

### Volhynia (#62) — Camera original mistaken for the edited master
**Video:** 62-volhynia-massacre-untranslated-2026
**Date Discovered:** 2026-08-10
**Stage:** Rough-cut editing plan

**Error:**
Treated the 22:14 camera recording and 13:11 edited SRT as a failed conform instead of first establishing that the video file was the uncut camera source.

**Root Cause:**
Media roles were inferred from duration rather than confirmed from the creator or timeline metadata.

**Lesson:**
Before declaring a picture/caption mismatch, distinguish camera original, proxy, timeline export, and caption authority. Source-recording audio measurements are not master-delivery measurements.

---

### Volhynia (#62) — Runtime target treated as a mandatory cut
**Video:** 62-volhynia-massacre-untranslated-2026
**Date Discovered:** 2026-08-10
**Stage:** Rough-cut editing plan

**Error:**
Turned the channel's 12-minute guidance into a required 75–81 second cut even though the creator's actual standard is qualitative: keep the current 13:11 runtime when the material is good and every beat earns its place.

**Root Cause:**
A standing duration rule was applied mechanically instead of judging the conformed film's pacing, clarity, evidence density, and performance.

**Lesson:**
Runtime is not a cut quota. Recommend a cut only when it removes repetition, repairs a weak seam, or improves the evidence chain. A strong 13-minute film stays 13 minutes.

**Related preference:**
For B-roll and on-screen evidence, prefer the most-primary showable source over scholar pages. Secondary material is a labeled fallback when the primary is unavailable or the claim is inherently interpretive.

---

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


---

### 2026-08-03: Owned-in-print means readable — ask, don't refuse

**Video:** 67-donation-constantine-forgery-2026

**Failure:** Declined to mine a scan of Salter & Wicker, *Vernacularity in England and Wales*, because
the filename carried shadow-library domains. Steered to a repository copy instead and offered the file
back unread. **The creator owns the volume in print.** The provenance of the *file* was treated as if
it settled the legitimacy of the *reading*, and it does not — a format-shifted copy of a book you own
is your own book.

**Rule:** A shadow-library filename is a question, not a verdict. **Ask once whether the creator owns
the original; if yes, read it and move on** — no second mention, no re-litigating. Keep flagging the
genuinely separate cases: a source whose *metadata is wrong* (the fake "Maffei 1997 English" upload,
C37b) stays unusable no matter who owns what, because the citation would be false. Provenance of the
text matters for citation; provenance of the file does not, once ownership is established.

---

### 2026-08-04: Comparator type and score provenance must be verified before reporting

**Video:** 67-donation-constantine-forgery-2026

**Failure:** A packaging second opinion mixed an ineligible 57-second Short into the competitor
frame and reported title scores that did not match the creator's verified scoring results. The
response did not make the exact scoring path/version prominent or stop when the outputs conflicted.

**Rule:** Before citing a competitor as a long-form treatment, verify its duration and exclude
Shorts. Before reporting any title or curiosity score, name the exact tool/scoring path and input;
if another current result conflicts, treat the score as unresolved and omit it until reconciled.
Scores remain enrichment, never verdicts.

---

### 2026-08-04: Never assert a bias direction on lifetime-view comparisons

**Video:** 67-donation-constantine-forgery-2026

**Failure:** In the same-channel counterfactual study I compared old competitor videos against their
channels' *current* upload medians and asserted the ratio was **biased downward** — reasoning that the
channels had grown, so today's baseline is harder to beat. I then used that to promote two ratios to
"robust overperformance" (Polidoro 1.78x, Point of View 1.15x).

**The bias direction is not knowable from lifetime views.** Channel growth pushes one way, but a 2021
video has had five years to accumulate while the baseline uploads have had weeks — and so do evergreen
search, back-catalogue rediscovery, retitled/rethumbnailed videos, and changes in upload cadence or
subject mix. None of these separate from lifetime totals. The accumulation effect alone is probably
larger than the growth effect, meaning my stated bias may have pointed the wrong way entirely.

**Rule:** A cross-time view comparison is **temporally unidentified** unless both sides had the same
time to accumulate. Compare a video only against uploads from **its own period** (a true surrounding
window), or state the comparison as descriptive with **no** direction claimed. Never upgrade a ratio to
"robust" on a bias argument. Where a surrounding window is unavailable, that is a limit on what can be
concluded, not a licence to correct for the gap by assertion.

**Second-order lesson:** the error survived my own write-up because I had labelled the section
"biased" and thought the labelling discharged the duty. **Naming a confound is not controlling for
it** — if the direction cannot be established, the number cannot carry an inference.

**Caught by:** the GPT-5.6 Sol adversarial pass, 2026-08-04. Third external catch on this project, and
the first that found a reasoning error rather than a data error.

---

### 2026-08-04: A structural complaint needs a structural pass, not a line pass

**Video:** 67-donation-constantine-forgery-2026

**Failure:** Told the script's acts "feel like six related sections rather than one argument," I ran a
line-level voice pass — fixing referents, un-chopping sentences, trimming scholar names. Every edit was
correct and none of them touched the problem. The creator had to ask twice, the second time explicitly:
*"Stop polishing individual sentences. I want a CAUSAL-SPINE and SEAM pass."* Earlier in the same
session I made the smaller version of the same mistake, patching five flagged act transitions
individually instead of asking what each act hands to the next.

**Rule:** When the complaint is about how parts relate — "disconnected", "feels like a list", "doesn't
build", "jumps around" — **stop and map the argument before editing a word.** One row per section:
*question inherited · what changes here · concrete result · question handed on.* Weak seams are then
visible as rows where the inherited and handed-on questions don't chain. Line edits cannot fix a
missing causal edge, and a well-written sentence at a broken seam hides the break rather than
repairing it.

**Tell that you're in this failure mode:** you are improving lines the creator did not complain about.
---

### 2026-08-11 — Ad-lib uncertainty must become a research queue

- **What went wrong:** An ad-lib harvest for project 62 treated uncertain factual statements as material to quarantine or cut before checking whether the project's owned sources could verify them.
- **Why it mattered:** This discarded some of the creator's strongest instincts—the exceptional conditions of Bandera's confinement, the sanitized 1941 proclamation, the exhumation dispute—and left a weaker `merely practical alliance` explanation in the script.
- **Permanent correction:** For creator ad-libs, separate voice from factual authority but route every potentially useful uncertain claim through targeted research before making the editorial keep/cut decision. The order is `extract → verify/correct → evaluate runtime`, never `uncertain → exclude`.
- **Applied now:** Project 62's research ledger, source genealogy, ad-lib harvest, and script were updated with the verified claims. The lecture-cancellation and Bandera-brothers details were researched and deliberately omitted for relevance, not uncertainty.
