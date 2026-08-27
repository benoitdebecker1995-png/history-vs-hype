# Editing Guide — #62 Volhynia ("Zelensky Honored These WWII Heroes. Poland Calls Them Nazis.")

**Source:** `rough cut.srt` (399 cues) vs `TELEPROMPTER-FILMED-2026-07-23.md` (as-filmed baseline) + `SCRIPT.md` v7.0 (on-screen card ground truth)
**Region covered:** Full video, 13 min 11 sec (SRT timecodes are offset +1h; `01:mm:ss` = `mm:ss` real)
**Generated:** 2026-07-24 · Post-production Phase 3

> Companion doc: `_research/ON-SCREEN-CARD-MATCH-2026-07-24.md` (Task 3 — every surviving on-screen card matched to its document + provenance verdict). This guide covers the CUT; that doc covers what goes ON the cut.

---

## TL;DR — top 7 actions

1. **🔴 AUDIO IS TOO QUIET — fix before anything ships.** Master measures **‑31.9 LUFS integrated** (YouTube target −14). Viewers will crank the volume; YouTube will not boost you up. A flat +18 dB gain would clip (true-peak is already −9.1 dBTP → +18 dB = +8.8 dBTP). **Loudness-normalize to −14 LUFS with a true-peak limiter at −1 dBTP** at export.
2. **🔴 Run `/fix` before burning in captions.** The SRT is auto-transcription: ~20 proper-noun/foreign-term garbles (Motyka→"modica/Moptikka", Klyachkivsky→"Krijakzkiewski", Volhynia→"Volnya/Warnia/Wolnia", Poryck→"Porek", "hit"→"hid", "round up"→"random", "finished"→"Finnish"). Full list below. Do NOT hand-fix in this guide.
3. **⚠ Place the two MANDATORY captions (load-bearing — the VO dropped their spoken markers):** the **Redesha duress caption** (~6:40) and the **Snyder verbatim + name** (~5:32 and ~13:36). See Caption pass + card-match doc.
4. **⚠ Restore two load-bearing beats the EDIT dropped** (Task 1): the **Bandera-confined-during-the-massacres** fairness qualifier (fixable as a caption) and the trailing **"in the Congo"** on the Leopold II close. Details in Segment notes.
5. **Fix two stumbles left in the cut:** the ~2s dead gap at cue 108→109 (01:03:29→01:03:31) and the doubled "it was restricted again, it was restricted again" at cues 348–349 (~11:24).
6. **Documents as active characters (edit-stage rule):** no document on screen >5s without a zoom/highlight/overlay pointing at the word that matters. Applies to every card in the card-match doc.
7. **Film-at-13:11 is on target** — under the channel's soft 12-min guide but this video's depth-earns-length call was made at the grill and the cut already trimmed ~1.5 min off the teleprompter. No further runtime cuts needed.

---

## How the cut tracks the script

The cut follows `TELEPROMPTER-FILMED-2026-07-23.md` (the ChatGPT ~13-min trim the creator actually read) almost line-for-line, with the edit dropping five further beats. This means the **on-screen card map in `SCRIPT.md` v7.0 is a superset** — several v7.0 cards (Napoleon, the full doctrine walk, the Gaj rescuers, the custody fan-in for the "signed directive" beat) have no VO home in the cut and are NOT needed. The card-match doc reconciles this.

**Verbal-divergence verdict (Diff A):** every intentional ad-lib the creator added is grounded and improves the script (see `VO-ATTRIBUTION-AUDIT.md`). The only losses that matter are the five EDIT cuts below.

---

## Segment notes — decisions & issues only

Clean beats omitted. Only beats carrying a decision, a dropped element, or a stumble are listed. Real timecodes.

### Cold Open (0:00 → ~1:26)
- **Cue 1–7 (0:00): ARCHIVE HOLD.** McBride p.648 is a secondary reproduction, not the acquired report. Riabenko reports that the cited case 11315 contains no Klymchak document. Do not build or publish this evidence card until HDA SBU confirms the folio; otherwise replace or explicitly frame the quote as contested scholarly attribution.
- **⚠ Dropped (Task 1 #1):** teleprompter's cold-open closer *"And the question is: how far up the chain did it go?"* — not in the cut. **Verdict: safe trim** — "So I wanted to see what the documents actually support" (cue 43–44) already sets up the investigation. No action.
- **Cue 30–33 (~0:57):** historian-positions list (genocide / Second Polish-Ukrainian War / ethnic cleansing / Motyka "genocidal ethnic cleansing"). DIY text card. ⚠ Motyka number-guard does not apply here (label, not number).

### Two Stories (~1:36 → ~3:37)
- **🔴 Dropped (Task 1 #2) — LOAD-BEARING:** *"And during the massacres themselves, Bandera was still confined outside Ukraine. He had limited contact with the movement, but the surviving record does not show what he knew…"* Cut between cue 73 and 74 (~2:18). This is the fairness guardrail — the video names Bandera prominently but now never clarifies he was imprisoned throughout the 1943 killings. **FIX: restore as a caption** over the Bandera/Sachsenhausen beat (cue 62–63, ~1:57): *"Bandera was held in Sachsenhausen throughout the 1943 massacres; the record doesn't show what he knew."* VO pickup optional; caption is enough.
- **Cue 82–88 (~2:34):** 2015 Law #2538-1 + "decree from 2026 is an extension of that." Card = `rada.gov.ua` T1 screenshot (still to pull). Crimea 2014 archival.
- **Cue 101–106 (~3:12):** parliament acknowledges Ukrainian crimes + calls Volhynia genocide → Sejm 2016 resolution card (still to pull). SRT garble "caused Warnia a genocide" → `/fix`.
- **Stumble — cue 108→109 (01:03:29→01:03:31 = ~3:29):** ~2s dead gap mid-sentence ("turned … the UPA's earlier campaign"). Tighten the gap.

### How They Got There (~3:37 → ~5:00)
- **⚠ Dropped (Task 1 #3) — causal joint:** *"Then, in 1941, Germany invaded the Soviet Union and the OUN made its move."* Cut before cue 146 (~4:42) — the June 30 declaration now appears with no Barbarossa setup. **FIX (cheap): a date card** at cue 146: *"June 30, 1941 — days after Germany invaded the USSR."* No re-film.
- **Cue 118–121 (~3:50):** ad-lib ADDITION "both borderlands with Poland with a Polish minority" — grounded, KEEP (per audit).
- **Cue 126–140 (~4:05):** Dontsov (portrait, still to pull) + Kolodzinskyi "Military Doctrine" page. Card = *Ukraina Moderna* 20 (2013) **p.266** (owned PDF, render). ⚠ Card verbatim must read **«польський елємент» / "the Polish element,"** not "population."
- **Cue 146–154 (~4:42):** Stetsko Act of Restoration — autograph facsimile acquired; highlight the Hitler passage, no silent crop.

### The Army & The Attacks (~5:00 → ~7:36)
- **Cue 196–197 (~5:20):** SRT garble "What they needed at Army 4" → `/fix` ("Why they needed that army").
- **Cue 202–203 (~5:32):** "a restored Poland would try to reclaim the region." **🔴 MANDATORY caption:** Snyder verbatim + name (Snyder, *Reconstruction of Nations*, pp.166–167) — VO paraphrases what was a quotation. Must be on screen here.
- **Cue 208–214 (~6:40):** Redesha quote. **🔴 MANDATORY caption:** *"testimony to Soviet interrogators, HDA SBU f. 13, spr. 1020"* — the VO says only "later explained," so this caption is the video's ONLY duress marker, and CH7 asks the viewer to discount Stelmashchuk's confession on that ground. Must be legible. Card text char-exact ("would never again **to** try to lay claim" is the printed wording — see card-match doc).
- **Cue 215–223 (~6:55):** Bloody Sunday — Poryck + ~200 / ~4,000. SRT "hid"→"hit", "Porek"→"Poryck" → `/fix`.
- **Cue 224–230 (~7:15):** Siemaszko registry (36,000 names). Wall-of-names exhibit acquired. SRT drops "one by one" — safe.

### Was It Two-Sided? (~7:31 → ~8:50)
- **Cue 240–243 (~7:48):** 70K:20K. **🔴 MANDATORY caption:** Snyder + name + verbatim (p.204: *"about seventy thousand Poles to perhaps twenty thousand Ukrainians"*). Number-guard: never present 70K as Motyka's own figure. As-filmed "working **from** Motyka's research" is correct (the optional for→from pickup is moot — the cut already says "from").
- **Cue 246–248 (~8:00):** SB purge — "shot Ukrainians it considered unreliable, including men who refused to kill Poles." Card optional; if built, cite Piotrowski p.254 (corrected), hedge "according to."

### The Missing Paper (~8:50 → ~11:41)
- **Cue 279–282 (~9:07):** "Weapons ready. Death to Poles." Text card — **English + transliteration ONLY, no Cyrillic** (RL prints none). Attribute RL p.267.
- **Cue 287–301 (~9:21):** Klym Savur Order No. 11 forensic-contrast exhibit (acquired T1). ⚠ Show whole image; **never crop "зліквідувати."**
- **⚠ Dropped (Task 1 #4) — attribution:** *"Some Polish historians describe this as Klym Savur's signed directive. Motyka is more precise."* Cut before cue 342 (~11:12). **The landmine survives** — the next surviving line ("the letter reports an oral order. It is not the order itself," cue 343–344) is correct, so no false claim ships. **Verdict: acceptable.** Optional restore via a two-position caption; not a block.
- **Stumble — cue 348–349 (~11:24):** doubled "It was restricted again, it was restricted again." Jump-cut the repeat.
- **Cue 316–329 (~10:20):** Stelmashchuk confession + Gorshkov notes. Cards acquired at T2 (McBride p.642, Litopys p.442); Katchanovski Photo 1 optional upgrade (still to pull).

### Close (~11:41 → 13:11)
- **🔴 Dropped (Task 1 #5) — LOAD-BEARING:** the Leopold II sentence ends at "after everything" (cue 385, ~12:45) — **"that happened in the Congo" is gone.** The Belgium/Congo parallel is the close's emotional payoff and the line currently trails off. **FIX: restore "in the Congo"** (VO pickup or caption), OR check whether the filmed audio continues past the SRT cutoff and re-cut. Napoleon parallel was already trimmed in the teleprompter → **no Napoleon card needed.**
- **Cue 386–399:** the locked outro ("nothing wrong with looking to the past for heroes… please subscribe") is intact. ✅

---

## Pacing assessment

| Marker | Target | Rough cut | Delta |
|---|---|---|---|
| Total runtime | ~12 min (soft channel cap) / 13.9 min (SCRIPT.md v7.0 estimate) | **13:11** | Under the v7.0 estimate; ~1.2 min over the soft cap |

**Verdict: acceptable — no further trimming.** The cut already dropped ~1.5 min vs the teleprompter. The depth-earns-length call was made at the grill and confirmed twice. Let retention data decide.

---

## Caption pass — burned-in subtitles

**🔴 Run `/fix` before burn-in** — the SRT is raw auto-transcription with ~20 proper-noun/foreign-term errors. Representative (NOT exhaustive — `/fix` handles programmatically):

- "Gregor's modica" / "Moptikka" / "Motica" → **Motyka**
- "Volnya" / "Warnia" / "Wolnia" / "Vonia" → **Volhynia**
- "Krijakzkiewski" / "Klyrzkiewski" → **Klyachkivsky**; "Klim Stavur" → **Klym Savur**
- "Stelmakzuk" → **Stelmashchuk**; "Yeroslav Stetsko" → **Yaroslav Stetsko**
- "Dmitry Donsov" → **Dmytro Dontsov**; "Michailo Kolodinsky" → **Mykhailo Kolodzinskyi**
- "Ivan Katamzowski" → **Ivan Katchanovski**; "Redeschamp" → **Redesha**; "Bandań" → **Bandera**
- "Porek" → **Poryck**; "Simaszkos" → **Siemaszkos**; "Viatrovich" → **Viatrovych**
- "the UPA hid" → **hit**; "random Jews" → **round up Jews**; "Finnish job" → **finished job**; "all sites can inspect" → **all sides**; "had meant to carry it out" → **had men**; "and read the Genn building an army" → **and began building an army**; "What they needed at Army 4" → **Why they needed that army**

(Do NOT manually correct here — `/fix` is the tool.)

---

## Re-record / pickup checklist

Ranked by impact:

1. **HIGH — none strictly required.** No false claim ships; every landmine held (see `/verify --audio` verdict below).
2. **MEDIUM — "in the Congo" (Close).** Restore the trailing phrase — VO pickup (cleanest) or on-screen caption. The close currently trails off mid-analogy.
3. **MEDIUM — Bandera-confined fairness beat.** Restore as a caption (VO pickup optional). Guardrail against "you smeared Bandera."
4. **LOW — Barbarossa date card** (no re-film; a caption).
5. **OPTIONAL — pronunciation pickups** (Motyka, Poryck, Katchanovski, Klyachkivsky, Stelmashchuk). Take-selection at the edit; none change a claim.

**Don't re-record:**
- The cold-open "how far up the chain" line (safe trim).
- The "signed directive / Motyka is more precise" beat (landmine survives without it).
- Any beat the teleprompter deliberately trimmed from V8 (Napoleon, Redesha 2nd sentence, closing thesis question, "thousands" on the SB purge) — those are intentional creator cuts, not errors.

---

## Music & silence beats

| Time | Beat | Recommendation |
|---|---|---|
| 0:00–0:14 | Klymchak report cold open | Silence or low drone under the quote — let "needs of the battalion" land before any bed. |
| ~3:29 | dead gap (cue 108→109) | Tighten; don't let the pause read as a mistake. |
| ~6:55–7:20 | Bloody Sunday / Poryck | Pull music down; the ~200 / ~4,000 numbers carry the weight. |
| ~12:45–13:11 | Leopold II → outro | Let the personal turn breathe; music lifts into the CTA. |

---

## Audio loudness

(From Diff D — `python -m tools.preflight.audio_loudness "23072026_170736.mp4"`)

| Metric | Measured | YouTube target | Verdict |
|---|---|---|---|
| Integrated | **−31.9 LUFS** | −16…−12 (−14 ideal) | 🔴 **QUIET** (~18 dB under) |
| True peak | −9.1 dBTP | ≤ −1 | OK |
| Loudness range | 7.0 LU | 4–15 | OK |

**Action:** The master is ~18 dB below target. A flat +18 dB gain would push peaks to +8.8 dBTP (clipping), so **loudness-normalize to −14 LUFS with a true-peak limiter at −1 dBTP** at export (NLE loudness normalization, or `ffmpeg -af loudnorm=I=-14:TP=-1:LRA=11`). This is the single most important pre-upload fix — `/publish` Gate 3 is only a backstop.

---

## Done state

When this video is locked, you should have:
- [ ] Audio normalized to −14 LUFS / −1 dBTP (currently −31.9 LUFS — **blocking**)
- [ ] `/fix` run on the SRT (~20 transcription errors) before caption burn-in
- [ ] Redesha duress caption placed & legible (~6:40)
- [ ] Snyder verbatim + name placed (~5:32 "restored Poland" and ~7:48 70K:20K)
- [ ] "in the Congo" restored (VO pickup or caption)
- [ ] Bandera-confined fairness caption placed (~1:57)
- [ ] Barbarossa date card placed (~4:42) — optional but cheap
- [ ] Dead gap (~3:29) and doubled line (~11:24) tightened
- [ ] Every on-screen card matched per `_research/ON-SCREEN-CARD-MATCH-2026-07-24.md`, each with a zoom/highlight (no static doc >5s)
- [ ] Re-verify all 2026 facts week-of-upload (decree, White Eagle "three weeks," exhumation timeline)
