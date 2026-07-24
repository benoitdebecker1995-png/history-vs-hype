# HANDOFF — #62 Volhynia: rough-cut review → on-screen primary documents
**Written 2026-07-23 for a fresh context window. Self-contained: read the files named here, don't assume prior chat.**

## Where this stands, and who touched it

#62 (Volhynia / OUN-UPA, "Zelensky Honored These WWII Heroes. Poland Calls Them Nazis.") is **filmed and rough-cut.** History with modern relevance, document-led referee format — see `CLAUDE.md` channel DNA. Collaborators on the current state, so you don't misread deliberate work as drift:

- **Script:** fact-checked V8 (`VO-v8-referee-draft.md`) by Claude, then **trimmed to ~13 min by the creator with ChatGPT** into `TELEPROMPTER-FILMED-2026-07-23.md` (the teleprompter he actually read). The trim deliberately cut several V8 beats (Redesha 2nd sentence, the closing thesis question, the Napoleon parallel, the "remembers/buries"+Bucha close opening, the explicit "thousands" on the SB purge). **These are intentional creator cuts, NOT errors — do not "restore" them.**
- **Post-film audit:** `/verify --audio` already run → `VO-ATTRIBUTION-AUDIT.md`, verdict **GREEN** (no landmine broken, no false claim). One optional one-word VO pickup logged: "Snyder working **for** Motyka's research" → "**from**" (credit direction preserved, so not a hard block).
- **The creator has now done the rough cut** → `rough cut.srt` (399 cues, ends ~13:11).

## Your three tasks, in order

### TASK 1 — Diff the rough cut, find what the EDIT removed and why
Baseline = `TELEPROMPTER-FILMED-2026-07-23.md` (what he intended to say). Delivered = `rough cut.srt` (what shipped). List every beat/sentence the *edit* dropped or reordered vs the teleprompter (the timecodes in the SRT are offset +1h; 01:mm = mm real). For each cut, infer the likely reason (runtime, stumble, redundancy) and classify: **safe trim** vs **⚠ load-bearing loss**. A load-bearing loss = a cut that removes a beat the argument needs (a number, an attribution, a landmine-carrying qualifier, a causal joint). Report those; don't touch the safe ones.

### TASK 2 — Is further editing necessary?
Run **`/editing-guide`** against `rough cut.srt` — it's the canonical segment-by-segment editing playbook from a rough cut (Post-production Phase 3). Then:
- Re-run **`/verify --audio 62-volhynia-massacre-untranslated-2026`** on the CUT SRT (the earlier audit was on the raw filmed take; the SRT is what actually ships — the skill *prefers* the cut SRT for exactly this reason).
- Confirm the two **mandatory captions** have a home in the cut (they're load-bearing given VO drops): the **Redesha duress caption** ("testimony to Soviet interrogators, HDA SBU f. 13, spr. 1020" — now the ONLY signal that quote came from an interrogation) and **Snyder's verbatim + name** (VO paraphrases "a restored Poland").

### TASK 3 — Find the primary documents to show on screen (the main job)
Every ON-SCREEN card in the script must be matched to a real, showable, correctly-provenanced document. **`_research/SOURCE-GENEALOGY.md` is the single source of truth for on-screen provenance** — work from it, don't re-derive. Load the **`primary-source`** skill first (on-screen-provenance discipline + the SOURCE-GENEALOGY ledger), and spawn the **`primary-source-hunter`** agent for any card whose document isn't yet acquired or whose provenance verdict is open.

**Already acquired — do NOT re-hunt these** (`_research/exhibits/` + `_research/genealogy/`): the 1941 Act of Restoration facsimiles (Stetsko autograph + sanitized reprint), Bandera photos, Volhynia map, Lipniki 1943 photo, Siemaszko registry pages, Klym Savur **Order No. 11** (the logistics-not-liquidation contrast exhibit), and genealogy scans: `mcbride-p648.png` (Klymchak report), `mcbride-p642.png`, `litopys-ns9-*` (protocol header, Savur directive, massacre confession), `RL-p236` Hitler-question. Index: `_research/exhibits/EXHIBITS-INDEX.md`; card map: `ON-SCREEN-SOURCES.md` + `RECORD-CARDS.md`; exact locators: `_research/CARD-PINS-2026-07-21.md`.

**Still likely needed / to confirm against the cut** (walk the script's ON-SCREEN blocks in `VO-v8-referee-draft.md` and the teleprompter): the 2026 decree + White Eagle revocation stills; the post-WWI map; Dontsov; the Kolodzinskyi *Military Doctrine* page; the Bandera-arrest/Sachsenhausen custody card; the Poryck/registry visuals; the historian-positions card; the Stelmashchuk protocol + Gorshkov notes + the 24 Jun 1943 letter *as published* + the custody diagram; the exhumation-arc + reconciliation cards; Napoleon/Leopold close stills (Napoleon only if that beat survived the cut — it was trimmed from the teleprompter, so check the SRT first).

## Binding constraints — carry these verbatim (from `_research/SCRIPT-PRE-REFEREE-2026-07-22.md` line 52 + `SOURCE-GENEALOGY.md`)
1. **No authenticated signed kill order exists or is showable.** Never card one, never invent one. The "signed order" Polish historians cite = the same unreachable folio HDA SBU spr.11315 (Row 5c) — never present it as a producible document.
2. **The letter (24 Jun 1943) is a published transcription that reports an ORAL directive** — never "signed," never "we have the letter." Show it AS PUBLISHED with the inaccessibility caption.
3. **The Klymchak report** is "a UPA after-action report, preserved in a Soviet case file, reproduced by historians" — **NOT** "a signed archival document" (McBride's own fn.63: he couldn't review the folio).
4. **Kolodzinskyi card = «польський елємент» / "the Polish element"**, from *Ukraina Moderna* 20 (2013) **p.266** + Himka **p.154**. ⚠ The old "Himka p.389" cite is WRONG (that page is unrelated Jewish testimonies). Card shows the source's own words, not "population."
5. **Never card:** the quarantined "disappear from the face of the earth / 16 to 60" web quote (mistranslation, wrong date); any FSB 2026 dump material (hostile + part-fabricated); the web "September 29 / youngest ones" Klymchak translation (wrong wording AND date).
6. **Redesha duress caption mandatory + legible** (see Task 2). Card verbatim char-exact (McBride pp.648/653): "would never again **to** try to lay claim" is the printed wording — card is char-exact, VO speaks naturally.
7. **On-screen quote cards are char-exact**; any PL/UA verbatim reaching a card gets the **Check-A** friend-translation pass before lock. Every on-screen card must have a `SOURCE-GENEALOGY.md` row (verdict + verbatim + page); a card with no ledger row is a flag — hunt it or add the inline-confirmed row.
8. **Re-verify the 2026 facts week-of-upload** (decree, White Eagle revocation = "three weeks," exhumation timeline) — the only time-sensitive claims.

## Reference map
- Cut: `rough cut.srt` · Teleprompter: `TELEPROMPTER-FILMED-2026-07-23.md` · Fact-checked script: `VO-v8-referee-draft.md`
- Provenance ledger (authority): `_research/SOURCE-GENEALOGY.md` · Card locators: `_research/CARD-PINS-2026-07-21.md`
- Claim ledger: `01-VERIFIED-RESEARCH.md` · Landmines: `_research/SCRIPT-PRE-REFEREE-2026-07-22.md` line 52
- On-screen map: `ON-SCREEN-SOURCES.md` · `RECORD-CARDS.md` · exhibits: `_research/exhibits/EXHIBITS-INDEX.md`
- B-roll plan: `_research/BROLL-PRODUCTION-GUIDE.md` · Post-film audit: `VO-ATTRIBUTION-AUDIT.md`
- Skills: load **`primary-source`** (on-screen discipline) + **`production-map`** (routing); agent: **`primary-source-hunter`**; commands: **`/editing-guide`**, **`/verify --audio`**, then **`/fix`** (subtitle correction) → **`/publish`**.

## Done-standard
- Task 1: a list of edit-cuts classified safe vs ⚠load-bearing, with a recommendation on each ⚠.
- Task 2: `/editing-guide` output + a clean `/verify --audio` on the cut SRT + confirmation the two mandatory captions are placed.
- Task 3: every ON-SCREEN card matched to an acquired showable file with a SOURCE-GENEALOGY row and correct provenance framing; a short "still to acquire" list for anything not yet in `_research/exhibits/`. Do NOT overwrite `SCRIPT.md` or invent documents. Flag one specific beat for the creator only if a card genuinely can't be sourced within the constraints.
