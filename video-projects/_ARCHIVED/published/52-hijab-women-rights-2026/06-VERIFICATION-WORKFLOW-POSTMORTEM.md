# Verification Workflow Postmortem — Hijab #52 §V Card

**Date:** 2026-05-20
**Status:** Draft for user review
**Scope:** What went wrong with the §V on-screen card verification chain, and what to change at the workflow level so this doesn't repeat on Format C / forensic videos.

---

## TL;DR

A single on-screen card ("the elderly woman resembles the female slaves... the distinction which Sharia intended... passes away") burned ~3–4 days of verification work and reached film stage with `⏳ UNVERIFIED` still on it. Three candidate primaries were checked sequentially, all ruled out. An AI tool fabricated convincing Arabic verbatim that nearly went to film. The card's actual primary author is still unknown.

This is not a one-off. It's the fourth NotebookLM-grounding failure on this project alone. The script-writer-v2 rules to prevent this exist (Rule 42, Format C primary-document mandate) but the gate isn't enforced at the point it matters: before the script reaches DRAFT-LOCKED.

---

## Failure chain (compressed)

1. **Anchassi (2021)** — English passage with bracketed glosses found. Primary author not stated explicitly in the form we extracted.
2. **Attributed to Ibn al-Jawzī** (*Zad al-masīr* 6:63) in early script draft → user direct-checked → phrase absent from Jawzī's Q. 24:60 section. Rejected.
3. **Re-attributed to Ibn al-ʿArabī al-Mālikī** (*Aḥkām al-Qurʾān* Vol 3, Q. 24:60) based on Grok output. **Grok provided "verbatim Arabic"** including `وزال التمييز الذي قصد الشارع`.
4. **Direct primary check**: extracted full djvu text of akquia3 (Yedali scan of Aḥkām al-Qurʾān). Ibn al-ʿArabī's Q. 24:60 section has 4 masāʾil on jilbāb/khimār/modesty/tabarruj — **zero mention of slaves, distinction, ʿillat al-khidma, or Q. 33:59**. Grok's Arabic phrases do not exist in the actual text. Rejected.
5. **Geissinger search** initiated as candidate locator (the user said "it should be in here"). 30+ pages extracted; no direct quote found for a 12th-century scholar on this theme in the pages read.
6. **User pivots** to "find me any 12th-century scholar quote on this theme I can put on screen" — improvised Plan B because Plan A has burned days.

Throughout: script in `_READY_TO_FILM/`, rough cut exists, §V card carries `⏳ UNVERIFIED` annotation, publish blocked.

---

## What went wrong

### 1. AI fabrication of primary-source verbatim
Grok generated Arabic phrases attributed to Ibn al-ʿArabī's Q. 24:60 commentary that **do not exist in the actual text**. This is the most dangerous failure mode in the chain because the phrases were grammatically and stylistically plausible. Only the literal-string check on the actual djvu caught it. Without that check, the script ships with a fabricated citation on screen.

Already captured in `feedback-notebook-citation-grounding.md` (2026-05-20 scope extension) but worth restating: **AI-generated "verbatim Arabic" is a hypothesis, not a result.** It must be located via literal-string search in the actual primary before any use.

### 2. NotebookLM HIGH-confidence ≠ primary verification
Fourth instance on this project of NotebookLM grounding contradicted by direct primary check:
- Tabari defense quote (Mernissi paraphrase tagged to Tabari Vol 19; absent from Tabari)
- Musannaf Ibn Abi Shayba p. 135 (wrong edition/volume; conflated with Ibn Saʿd)
- Hafsa bint Sirin transmitter chain (Bewley shows Sawda → Khawla bint Qays instead)
- §V "distinction which Sharia intended" passage (Grok-fabricated attribution to Ibn al-ʿArabī)

Pattern is now memory; the gap is between memory and execution.

### 3. Script reached film stage with ⏳ row open
script-writer-v2 Rule 42 (added 2026-05-09) says: a script cannot be DRAFT-LOCKED if `03-FACT-CHECK-VERIFICATION.md` contains any ⏳ rows for blockquotes. The §V card has carried `⏳ UNVERIFIED` from its original attribution through to filmed state. **The rule exists; the gate didn't fire.**

The rule is written as a self-enforced check by the script-writer agent. Nothing structural prevents the user from filming a script that still has ⏳ rows — there's no hard pre-record gate.

### 4. Sequential primary-candidate checking
Jawzī checked → fail → THEN Ibn al-ʿArabī checked → fail → THEN Geissinger searched. Each step blocked on the previous. If all three had been launched in parallel from the moment Anchassi's English was found without a primary tag, the dead-ends would have been ruled out in hours instead of days.

This is a sub-case of the parallel-research principle that's worked well elsewhere (the `/editing-guide` pre-build during Gemini waits) but hasn't been applied to primary-source acquisition.

### 5. No pivot trigger
There's no rule that says "after N failed primary candidates, stop searching and switch to substitution mode." The current implicit rule is "keep chasing until you find it." For some passages that's right. For passages in the script's critical path with film already shot, it's wrong — the cost of further delay starts to exceed the cost of softening / substituting / cutting.

The user's final message in this session ("find me any 12th-century scholar quote on this theme") is them improvising this pivot without a pre-built escape valve.

### 6. Context-burn during long verification sessions
This session has read multiple large PDFs (Geissinger, Aḥkām al-Qurʾān djvu, Bewley, Tabaqat), drafted Grok prompts, extracted Arabic text, run sequential candidate checks. The verification-against-primary discipline is correct. The cost-per-attempt is not being tracked.

---

## Root causes

**RC1. The verification gate is theoretical, not structural.** Rule 42 lives in the agent's prompt. It doesn't exist as a hard checkpoint between "script written" and "script filmed." A `/reconcile`-style routine that scans `03-FACT-CHECK-VERIFICATION.md` for ⏳ rows before allowing transition to `_READY_TO_FILM/` would close it.

**RC2. AI tools are treated as verification rather than triage.** Grok said "Ibn al-ʿArabī Q. 24:60" with confident-looking Arabic. Without the akquia3 primary check, that would have been "the answer." For Format C, every AI-sourced primary attribution must be a hypothesis flagged for primary check, not a result.

**RC3. No time-box on primary chase + no pre-planned fallback.** Once a citation can't be located in the first-attribution primary, you're in a different problem (source-from-scratch) with unknown duration. No mechanism forces a pivot decision.

**RC4. Format C MANDATE not operationalized.** Memory says Format C MUST open the actual primary. There's no agent that runs over a script and refuses to advance it if any on-screen card cites a primary nobody has opened.

---

## Proposed improvements

Listed in order of leverage (highest first). Pick which to implement.

### P1. Hard pre-record gate on Format C (highest leverage)
Add a routine — `/check-film-ready` or extend `/reconcile` — that scans `03-FACT-CHECK-VERIFICATION.md` for any of: ⏳ rows on blockquotes, `[PRIMARY-CITED]` tags without `[PRIMARY-VERIFIED]` pair on Format C on-screen cards, missing page-pin on quoted citations. Refuses to mark a project `_READY_TO_FILM/` until clean.

This alone would have prevented this session.

### P2. AI-Arabic → literal-string check rule
When any AI tool (Grok, ChatGPT, Claude, NotebookLM) provides Arabic verbatim attributed to a primary source, that Arabic must be located via literal-string search in the actual primary PDF/djvu **before** the script uses it. Already in memory; promote to a structure-checker check: any blockquote in Format C with AI-tool origin in its trail must show a `[VERBATIM-MATCHED-IN-PRIMARY: <file>:<offset>]` annotation.

### P3. Substitution ladder
Pre-built in `.claude/REFERENCE/SUBSTITUTION-LADDER.md` (new file). When primary acquisition stalls past T hours with N candidates ruled out, force one of: (a) substitute different verifiable quote on same theme, (b) soften VO + drop on-screen card, (c) cut the beat. The ladder spells out which option fits which situation and how to revise the script.

This is the user's improvised Plan B from this session, formalized.

### P4. Parallel candidate search by default
When a passage's first-attribution primary fails, launch parallel searches across all plausible candidates (different scholars in same school, different works by same scholar, secondary scholarship like Geissinger) simultaneously. Use the Agent tool with multiple subagents. Don't sequentialize.

### P5. Time-box + checkpoint
After 3 failed primary checks for a single citation, mandatory user-checkpoint via AskUserQuestion: "Checked X, Y, Z — pivot to substitution ladder or keep chasing?" Prevents drift.

### P6. Format C source-tier tagging in 03-FACT-CHECK
Already in memory (P/S/S→P tagging). Make it required: every primary-citation row in `03-FACT-CHECK-VERIFICATION.md` for a Format C video must show `[PRIMARY-VERIFIED]` (opened the document, literal-string matched) or `[PRIMARY-CITED]` (scholar cites it, document not opened by us). The latter is not film-ready for on-screen cards.

---

## Artifacts to produce (proposed)

1. **This file** — done; awaiting review.
2. `.claude/REFERENCE/SUBSTITUTION-LADDER.md` — P3 SOP.
3. **Update `script-writer-v2.md` Rule 42** — strengthen language: "open-PDF citation required, not notebook confidence" for Format C on-screen primary cards.
4. **Add `/check-film-ready` command or extend `/reconcile`** — P1 hard gate.
5. **Update `structure-checker-v2.md`** — P2 + P6 checks: AI-Arabic literal-match annotation, [PRIMARY-VERIFIED] tag check on Format C.

---

## Immediate decision needed for §V

Three paths for the filmed §V on-screen card:

- **A. Substitute.** Find a different verifiable 12th-century scholar quote on the free/slave veiling distinction (al-Qurṭubī Q. 24:60 is the unchecked candidate; or Geissinger's discussion of the *concept* attributed without claiming a specific scholar). Re-record VO if needed, or use existing VO with a different on-screen card.
- **B. Soften.** Drop the on-screen card. Keep VO but rephrase to "scholars argued..." without a named attribution. No re-record needed if VO already supports this.
- **C. Cut.** Drop the §V beat entirely. May require re-edit.

Recommendation: B if VO permits, otherwise A with al-Qurṭubī as next candidate (single check, time-boxed to ~2 hours).

Decision belongs to user. After decision, this postmortem can be moved to `_inbox/` for cross-project lessons promotion.

---

**Note (2026-05-20):** Subsequent metadata-pass + SRT-fix + reconcile session findings are consolidated in `session-findings-52-hijab-2026-05-20.md` (Findings F1–F5, Improvements P7–P10, Promotion Candidates A–D). The §V analysis above remains the canonical record of the §V card chain failure.
