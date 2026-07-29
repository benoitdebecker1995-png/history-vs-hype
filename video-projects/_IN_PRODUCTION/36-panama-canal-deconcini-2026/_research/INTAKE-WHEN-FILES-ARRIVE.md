# Intake brief — what to do the moment the files land on the laptop

> ## STATUS 2026-07-28, 18:0x — INTAKE RUN. Results below.
> | file | arrived | pre-registered test | verdict |
> |---|---|---|---|
> | **Carter, *White House Diary*** | ✅ | contemporaneous entry / 2010 annotation / absent? | **PASSED — contemporaneous, 27 Aug 1977, roman type.** Filed as Layer 11 (C105–C110) |
> | **Greene, *Getting to Know the General*** | ✅ | operational plan, or Torrijos talking? | **"Torrijos talking" — my C66 wording was an overstatement and has been narrowed.** Filed as Layer 12 (C111–C115) |
> | Escobar Bethancourt, *¡Colonia americana, no!* | ❌ **did not arrive** | — | **still open** |
> | Torrijos, *La batalla de Panamá* | ❌ **did not arrive** | — | **still open** |
> | Bird, *The Outlier* | not needed | — | Carter passed, so this was never required |
>
> **The Panamanian-voice gap is the only research item still open.** Panama's side is currently carried by
> two Americans (LaFeber, Jorden) and one Englishman (Greene) — all sympathetic, none Panamanian. It is not
> blocking: the video can be filmed without them. It is the difference between good and unimpeachable.

**Written 2026-07-28.** Purpose: when you drop the acquired sources on the machine, I run this without
asking you anything. Each entry says **where to put it**, **which claim it closes**, **the exact test**, and
**what happens if it fails**. Pre-registering the test means I can't retro-fit the verdict to what I hoped
to find — which is how C64 and C94 went wrong.

**Drop everything here:** `video-projects/_IN_PRODUCTION/36-panama-canal-deconcini-2026/_research/library/`
Filenames don't matter. PDF, EPUB or clean text all work. If a PDF is image-only I'll OCR it before
ingesting — the notebook silently fails on image PDFs (`reference-nlm-raw-read-verification`).

**Say "files are in"** and I start at #1.

---

## PRIORITY 1 — the one that changes the video

### 1. Jimmy Carter, *White House Diary* (Farrar Straus Giroux, 2010)

**Closes:** **C70** — currently **DOWNGRADED and unusable.**
> "It is obvious we cheated the Panamanians out of their canal."

**Why it matters:** a US president conceding the video's entire thesis in his own voice. It would be the
strongest single line in the project. **It currently reaches us at two removes** — Kai Bird's *The Outlier*,
quoted in a National Security Archive summary. Under Rule 1 that is **footnote-laundering** and it cannot
go on a card.

**The test, pre-registered:**
1. Locate the passage by index/date search. Diary entries are dated — **find the date.**
2. **Is it a contemporaneous diary entry, or a 2010 retrospective annotation?** The book interleaves both,
   and **C68 already caught one Panama passage that is an annotation, not a diary entry.** This is the
   likeliest failure mode.
3. Transcribe character-exact, with page.

**Verdicts:**
- **Contemporaneous entry** → [P] T1. **Goes on screen as the closing card.** Rewrite the Act 6 close.
- **Retrospective annotation** → still [P] but it is Carter-in-2010, not Carter-in-1978. **Usable, but the
  card must be dated 2010 and narrated as a later judgment.** Do not imply he wrote it at the time.
- **Not in the book at all** → **the claim dies.** Bird's *The Outlier* becomes the only route, and that is
  a biographer's paraphrase. **Cut it from the script.** Don't go looking for a third source to rescue it.

---

## PRIORITY 2 — the Panamanian voice gap

The dossier's honest weakness: **Panama's side is told almost entirely through two Americans** (LaFeber, a
US historian; Jorden, a US ambassador who is openly contemptuous of Torrijos — see the C46 and C82 guards).
Every one of these fixes that.

### 2. Rómulo Escobar Bethancourt, *Torrijos: ¡Colonia americana, no!* (1981)
Panama's **chief treaty negotiator** — the Panamanian counterpart to Jorden's *Panama Odyssey*.
- **Closes:** the C43 attribution — who actually authored the Appendix A–E fix. Right now it rests on
  **Jorden alone**, and Jorden was a participant with an interest in the story.
- **Test:** does Escobar Bethancourt describe the Byrd/Church/Sarbanes typewriter drafting, and does his
  account **agree** with Jorden's? **If the two negotiators disagree, that is a `[FLAG: DIRECTION NEEDED]`
  fork and I stop and bring it to you** — it would go to the heart of the Act 7 payoff.
- Spanish. I read it directly; you have Spanish on the verifiable list.
- ⚠ His name is already in our primaries — he is the addressee of Bunker's letter in the deposited Panama
  Canal Treaty documents (UNTS 1280). Nice on-screen corroboration that he was the counterpart.

### 3. Omar Torrijos, *La batalla de Panamá* (1973)
- **Closes:** **C60** ("to resolve a problem, the first thing you have to do is make it a problem") and
  **C61** (the solidarity-of-neighbours line) — both currently quoted **through Jorden**, i.e. through the
  US ambassador. Torrijos's own book would make them **[P] from the man himself.**
- **Test:** find both lines in Spanish; if present, the Act 5 cards get sourced to Torrijos, not to Jorden.
- **If absent:** keep Jorden, but the card must read *"as recounted by the US ambassador"* — which is
  weaker and which the [[feedback-auditors-edge]] rule requires us to say.

### 4. Graham Greene, *Getting to Know the General* (1984)
- Already partially mined (**C66**, p.71 — the Gatun Dam plan that overturned my own C64 guard). **We have
  fragments, not the book.** Full text lets me check the surrounding pages, which matters because C66 is
  now load-bearing and rests on a single page.
- **Test:** read pp. 60–90 whole. **Does the context support "operational plan," or does Greene frame it as
  Torrijos talking?** C64 already went wrong once in this exact spot, in the opposite direction.
- ⚠ Standing guard: Greene is **a novelist, Torrijos's friend, and travelled to the 1977 signing on the
  Panamanian delegation.** Say so on screen whenever he's used.

---

## PRIORITY 3 — nice to have, not blocking

### 5. Kai Bird, *The Outlier* (2021)
Only needed if Carter's *Diary* fails the test at #1. Bird's footnote would at least name the real source.

### 6. *Department of State Bulletin*, 25 Feb 1974, pp. 181–185
The eight Kissinger–Tack principles. **Largely superseded** — C89 already upgraded this to FRUS. Acquire
only if you want the *published* text as a display card rather than the internal record.

---

## What I will do with all of them, in order

1. **Health-check ingestion first.** Every file gets `source_describe` before I trust a single query — the
   notebook fails silently on image PDFs and has burned this project before.
2. **Raw-read every load-bearing quote.** Not a notebook summary — the actual page. An empty `sources_used`
   means unverified, and `conversation_id` leaks across supposedly-scoped queries.
3. **Run the pre-registered test above, and report the verdict even when it kills the claim.** Three claims
   died that way this session (C64's guard, C94's march, C44's Reagan wording). That is the process working.
4. **File to `01-VERIFIED-RESEARCH.md` as a dated layer**, with tier tags and guards written *at filing
   time* — the guard written at filing time is what caught C94 within the hour.
5. **Then, and only then, the Act 5 / Act 7 rewrites** — both are drafted and waiting
   (`ACT5-RESTRUCTURE-PROPOSAL.md`; the Act 7 reshape is specified at the end of Layer 9).

---

## What does NOT need the files — already closed as of today

| was open | now |
|---|---|
| DeConcini text vs the actual amendment *(open since 11 June)* | **CLOSED** — character-exact vs the UN depositary text |
| Leadership Amendment wording | **CLOSED** — exact, and it is *treaty text*, which proves Maier's point from the document |
| Panama's counter-reservation | **CLOSED** — full text recovered; Panama names UN Charter Art. 2(4) itself |
| UNGA resolution date/vote | **CLOSED** — 29 Dec 1989, official UN text; recites Art. 2(4) and demands observance of the treaties |
| OAS 20–1 vote | **RESOLVED** — narrate-only, press-anchored; don't card it |
| Reagan's line | **CORRECTED** — ours was a stump variant; Reagan Library text now in hand, plus a better card |

**Primaries now stored in-project** at `_research/primary-texts/`: UNTS Vol. 1161 (Neutrality Treaty +
Panama's understandings), UNTS Vol. 1280 (Canal Treaty + US reservations), UNGA A/RES/44/240, Reagan's
"To Restore America" (31 Mar 1976). All free, all official, all displayable on screen.
