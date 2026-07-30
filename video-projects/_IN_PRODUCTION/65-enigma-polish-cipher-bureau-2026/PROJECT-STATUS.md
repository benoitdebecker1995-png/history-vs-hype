# Project Status — #65 Enigma / Polish Cipher Bureau

**Created:** 2026-07-30
**Origin:** cross-lingual demand discovery (see `memory/feedback-crosslingual-demand-discovery.md`).
Surfaced from the catalogue-wide English-request scan of Historia bez cenzury —
`channel-data/gap-hunter/HBC-ENGLISH-DEMAND-2026-07-30.txt`, rank 5 of 72 signal-carrying videos.
**Stage:** pre-research. Packaging gate cleared on demand + whitespace; title LOCK PENDING owner choice.

> ⚠ AUTO blocks (`<!-- AUTO:reconcile -->`, `<!-- AUTO:packaging-lock -->`) are **not** hand-written
> here on purpose. Run `packaging_lock.py` to stamp the packaging verdict and `/reconcile` for the
> lifecycle block — per ADR-0014, never hand-roll those fences.

---

## The claim being refereed

The popular English-language account is that Enigma was broken at Bletchley Park, principally by
Alan Turing. The Polish Cipher Bureau (Biuro Szyfrów) reconstructed the military Enigma
mathematically in 1932 — Marian Rejewski, with Jerzy Różycki and Henryk Zygalski — and at the
**Pyry conference near Warsaw in July 1939**, five weeks before the invasion, handed Britain and
France a working replica and the method.

**This is not a "Britain gets no credit" video.** Bletchley's achievement was real and
*different*: the wartime machine was progressively hardened and Bletchley broke it at industrial
scale, including Naval Enigma. The video's thesis is that **"who broke Enigma" is the wrong
question**, and showing why it's the wrong question is the whole episode. That is the shape the
owner asked for — proponents right about one part, extrapolating past it.

## Why this candidate and not the others

**The misconception belongs to the target audience.** Politically engaged men 25–44 in UK/US/CA
believe this story, largely from a 2014 film. Every other candidate from the cross-lingual seam
asked that audience to care about someone else's national grievance — the channel's worst-
converting pattern (its one breakout took 30,469 views to 152 subscribers). Here the correction is
aimed at the viewer, not at a foreign public. This property is the single discriminator that
separated survivors from kills across two days of discovery.

**Low moderation cost.** A credit dispute, not an atrocity dispute. Compare #62 Volhynia, whose
Polish-language original generated 17,053 comments including a Poland–Ukraine flame war. Channel
has 224 lifetime comments across 28 videos and cannot arbitrate a war.

## Demand — vidIQ, 2026-07-30

| Keyword | Est. monthly search | Competition | Overall |
|---|---:|---:|---:|
| **enigma code** (primary anchor) | **6,198** | **33.2** | **60.7** |
| bletchley park | 6,236 | 40.3 | 57.9 |
| alan turing | 98,056 | 47.4 | 65.7 |
| the imitation game | 58,623 | 45.5 | 64.5 |

**G1 demand floor: PASS** (6,198/mo, well over the 500/mo floor).
**Rankability: 100** — competition 33.2 is under 40, unusual for this channel at 515 subs.

### ⚠ "ENIGMA" IS A POLLUTED KEYWORD — do not use it as the SEO anchor (found 2026-07-30)

`country_search` on the bare term shows the top 12 keywords in **both** GB and PK are almost
entirely the **1990s new-age band Enigma** — *return to innocence*, *sadeness*, *the child in us*,
*enigma beats* — plus **phone-unlocking software** (*enigma unlock*, *enigma unlocked*) and
*ict enigma* (trading). **Not one codebreaking keyword appears in either country's top 12.**

- GB in-country volume, bare "enigma": **6,726**
- PK in-country volume, bare "enigma": **33,630 — 5× GB**

**Consequence:** the 668,122/mo figure for bare "enigma" in the related-keywords table is
**band and software traffic, not this topic.** The real anchor is the specific phrase
**"enigma code" (6,198/mo, competition 33.2)**. Do not put bare "enigma" in tags or treat that
volume as addressable. Title must carry "Enigma" adjacent to a WWII cue so the phrase disambiguates.

### POCKET RISK: CANNOT BE RESOLVED PRE-PUBLISH — accepted as a known risk

Instruments exhausted: `topMarkets` empty for "enigma code" and "bletchley park"; `countryVolume`
returned **null for GB, US, PK and IN alike** (parameter accepted, no data exists at this
granularity). Per ADR-0020 that silence is **not** a clean result and is not being recorded as one.

Indirect evidence is mixed and mildly negative: the WWII parent cluster is
PK 21.8% / IN 15.4% / US 6.8% ("world war 2"), PK 15.3% / VN 13.5% ("ww2"),
VN 21.2% / PK 15.2% ("alan turing"). Counter-signal: "the imitation game" US 16.7%,
"benedict cumberbatch" GB 20% / US 13.3%.

**Reframe that lowers the stakes of this gate:** keyword `topMarkets` describes *search* demand,
and **search is only ~6.5% of this channel's traffic**. The pocket outcome is decided by who
**browse** serves it to — 98.4% of views come from non-subscribers — and that is unknowable before
publish. So this gate was never capable of answering the question for this channel. Treat pocket
geography as a **post-publish measurement** on day 1–7 (`impressions_daily` + viewer geography),
per the three-video experiment design agreed 2026-07-30, not as a pre-lock blocker.

## Whitespace — VERIFIED above 50 under the ADR-0020 referee-absence protocol

**Instruments and date recorded per `tools/TOPIC-RUBRIC.md` § referee-absence protocol.**

**1. SERP scan, 4 framings** (2026-07-30) —
`channel-data/serp-studies/titles/SRC-enigma-polish-cipher-2026-07-30.md`
Queries: *who really broke the enigma code* · *polish mathematicians broke enigma* ·
*enigma code rejewski cipher bureau* · *bletchley park enigma poland credit*

**2. Full-catalogue check, 19 channels, ~15,000 catalogue entries** (2026-07-30, uploads playlists
via `playlistItems`, NOT `vidiq_outliers` and NOT `intel.db` — neither can prove absence):
TIKhistory (511 uploads, **0 Enigma videos**) · Simple History (1,324, **0**) · Mark Felton (991,
**0**) · Kings and Generals (1,500, **0**) · Real Time History (74, **0**) · Historigraph (140,
**0**) · Veritasium (523, **0**) · Epic History · The Front · Numberphile · Computerphile ·
Timeline · The Great War · History Hit · Biographics · Dark Docs · Today I Found Out ·
The History Guy · WW2TV.

**3. Every candidate referee ID-verified** via `videos().list`:

| Views | Duration | Channel | Title |
|---:|---|---|---|
| 34,368 | 11m46s | The Front | How these Heroic Polish Codebreakers set the Foundations… |
| 19,857 | **1m08s** | Epic History | Enigma Code: The Polish Breakthrough (a **Short**) |
| **4,126** | **1h01m38s** | WW2TV | The First Enigma Code-Breaker: Marian Rejewski |

**Total Polish-credit adjudication: 58,351 views. The only long-form treatment has 4,126.**

Assertion ecosystem, ID-verified: Timeline 8,126,507 · Numberphile 6,687,581 + 5,369,876 ·
Computerphile 2,909,000 + 1,442,848 + 695,592 · Timeline/Turing 2,126,875 · Biographics 389,218 ·
History Hit 133,372 — plus *Imitation Game* clip 3,689,378 and QI 2,325,140 (from the SERP).

**≈28M assertion : 58K adjudication ≈ 480:1.**

**Required phrasing:** searched those four framings, catalogue-checked those 19 channels,
**did not find** a referee at scale. NOT "no referee exists."

## Title — LOCK PENDING (owner picks)

All three pass the binding gates: `has_search_anchor` = **Poland** (real head term, first 40 chars),
clickbait brand-gate clean, `title_scorer` **68/100 (C)** — above the 65 threshold. All use the
two-sentence Claim.Evidence. format, the channel's top-retention brand signal.

1. **"Poland Broke Enigma and Gave It to Britain. Nobody Says So."** ← recommended, strongest
   curiosity (the second sentence forces *why not?*), and it is the actual thesis.
   ⚠ minor accuracy note: "Nobody" is colloquial — three small videos do exist (above). Defensible
   about the *popular* story; soften if it grates.
2. **"Poland Handed Britain the Enigma Secret. Then Vanished."**
   ⚠ **accuracy problem** — they did not vanish. Rejewski survived to 1980, working in a factory;
   Różycki died in 1942, Zygalski in 1978 in Britain. Overstated per the style guide's ban on
   absolutist language. Prefer 1 or 3.
3. **"Poland Broke Enigma Before Britain Did. Here's the Proof."**
   Generic second half; "Here's" is rationed on this channel.

**Rejected at the gate:** *"Alan Turing Didn't Break Enigma First. Poland Did."* (51/D) and
*"Turing Got the Credit. Three Poles Got There First."* (51/D) both **FAIL `has_search_anchor`** —
"Turing" is not in the head-term list despite 98,056/mo. Two scorer defects were found and filed
as a separate task (`has_search_anchor` also **false-positives on the ordinary word "who"**, so
*"Who Really Broke Enigma?"* passed the anchor gate spuriously). Do not lock a "who" title until
that is fixed.

## Exhibits to obtain (Phase 2 — NOT yet verified)

- **Rejewski's own postwar accounts** and his mathematical reconstruction — the permutation-theory
  attack on the rotor wiring. The showable artefact is his own writing, not a summary.
- **The Pyry conference, July 1939** — what was handed over, to whom, and on whose record. Both a
  British and a French account exist; they differ in emphasis. That divergence is the source
  criticism.
- **Bertrand (1973)** and **Winterbotham, *The Ultra Secret* (1974)** — the books that created the
  public Bletchley story. Winterbotham is the provenance question: what the first popular account
  left out, and why.
- **Sir Dermot Turing, *X, Y & Z: The Real Story of How Enigma Was Broken*** — the modern
  scholarly reconstruction, by Alan Turing's nephew. ⚠ **He is not new.** The correction already
  exists in print; this video popularises it. Say so on screen — do not present it as a discovery.
- The Polish Embassy lecture (63,088 views) is Dermot Turing delivering it. Watch before scripting.

## Honest risks

1. **Pocket risk unresolved** (above). Highest-priority pre-lock check.
2. **Not an original finding.** The scholarship is settled and published. The claim is "nobody has
   told this at scale, with the sources on screen," which is true and narrower.
3. **Serve, as always.** Median 302 browse impressions; 29 of 56 videos under 350. Packaging was
   deliberately optimised on the last two uploads and did not move it. Per the three-video
   experiment design agreed 2026-07-30, this video's job is to test whether **Suggested adjacency
   from #62 Volhynia** actually delivers the 4–7× measured on a stale, confounded sample.
   Pre-register that prediction before publishing.
4. **Register trap.** The Polish-grievance framing is available and would be a mistake — it turns
   an audience-correction video into an imported-grievance video, which is the failure mode this
   candidate was selected to avoid. Keep the subject "how the story got told," not "Poland was
   robbed."

## Next actions

1. Resolve `topMarkets` for the primary anchor (pocket gate).
2. Owner locks a title from the three above; run `packaging_lock.py` to stamp the AUTO block.
3. `/thumbnail` — 3 concepts. Text overlay mandatory (2–4 words); must NOT restate the title.
4. Then and only then, research: `/research` → Phase 2 NotebookLM (⚠ `nlm login` auth is expired
   and blocks Phase 2 — re-authenticate first).
