# Correction Format — Decision Synthesis

**Date:** 2026-04-24
**Inputs:** 3 Gemini reports + VidIQ STC analysis (all in this folder)
**Decision rubric:** from `correction-format-research-prompts.md`

---

## TL;DR

The VidIQ report built a full production package for **Treaty of Tripoli** because the keyword math is strongest (74K/mo vol, 30.9 comp). But Gemini's stress-test flagged it as politically radioactive, and it fails your channel DNA test ("will this matter in 10 years regardless of who's in power?").

After cross-filtering both reports against channel DNA, the honest winner is **Radcliffe Line / 1931 Census**.

---

## Cross-filter: Gemini rank × VidIQ verdict × Channel DNA

| Candidate | Gemini rank | VidIQ verdict | DNA test | Politically hot 2026? | Net |
|-----------|------------:|---------------|----------|----------------------|-----|
| Radcliffe Line (1931 census) | 5 | ✅ Low comp (5,241 vol / 23 comp) | ✅ | No (historical, not current flashpoint) | **TOP PICK** |
| Philippine Territory 1898 vs 1900 | 4 | ✅ Low comp (7,672 vol / 28.7 comp) | ✅ | Low (SE Asian, niche) | Strong #2 |
| Terra Nullius / Captain Cook | 6 | ✅ Low comp (4,430 vol / 23.6 comp) | ✅ | Low (Australian, 18th c.) | Strong #3 |
| Sherman 40 Acres and a Mule | 3 | ⚠️ Broad tag only (85K vol on "slavery" = wrong fit) | Partial | High (US reparations debate) | Skip |
| Waitangi | 2 | ⚠️ Tiny but rankable (3,980 / 28.3) | ✅ | Medium (NZ "Treaty Principles Bill" 2026) | Skip — active legislation |
| Treaty of Tripoli Art. 11 | 7 | ✅✅ Best keyword (74K / 30.9) | ❌ | High (US Christian-nation debate) | **VidIQ trap — skip** |
| Hitler 1938 Gun Law | 1 | ❌ Too competitive + high-heat | ❌ | High (US 2A debate) | Skip |
| Balfour Declaration | 8 | ✅ Lowest comp (7,194 / 16.5) | ❌ | Radioactive (Israel/Palestine 2026) | Skip |
| Bismarck Ems Dispatch | 9 (DROP) | — | ✅ | No | Skip — requires context dump |
| Magna Carta | 10 (DROP) | ⚠️ Too broad | ✅ | No | Skip — saturated |

---

## Why Radcliffe Line beats Tripoli despite weaker keyword math

**Tripoli pros:**
- 2,417 STC ratio (best in the list)
- Full production package already drafted
- Document is spectacular (Article 11 + missing Arabic passage)

**Tripoli cons (the honest ones):**
- Currently live US culture-war topic → attracts combative comments that wreck retention curves and tank the sub-conversion lift
- Fails the "10-year test" — this framing dates fast
- Gemini stress test called it a "magnet for culture war comments"
- Your memory explicitly flags "intellectual competence" triggers subs, not political hot takes

**Radcliffe pros:**
- Exact-match keyword "radcliffe line india and pakistan" at competition 23 — VidIQ says "low comp, exact-match niche" (one of only 3 clean ✅ ratings)
- 228 STC ratio — not the highest, but enough for a test video
- Document-forensic angle: contrast the 1931 Census numbers with the 1947 reality
- Taps 300M+ South Asian English audience (you already identified this segment via the Hamoodur Rahman pilot)
- Low political heat in 2026 (77 years old, no active legislation)
- Passes DNA: this is history-of-borders, not geopolitics-of-now
- Gemini tellability: YES, 30-second version works
- Gemini competition note: "Most videos are general 'Partition' overviews, not specific 'Census' forensically-focused" = gap

**Radcliffe cons:**
- Touches Indian/Pakistani nationalist narratives — need careful framing
- Lower keyword volume than Tripoli (5,241 vs 74,718)

---

## Format viability — SETTLED

Gemini's YouTube History Format Analysis is a solid green light on the 5-7 min document-first concept. The three failure modes it flagged are all addressable:

1. **Aesthetic boredom** → pattern interrupts every 90 sec (you already do this)
2. **AI-slop perception** → your voice is on camera = already mitigated
3. **Curiosity-utility gap** → title has to bridge niche document to universal curiosity

This is the first new format concept in the FORMAT-TEMPLATES.md that has external validation before first test.

---

## Recommended next step

Build Radcliffe Line as the Correction format pilot. Shape:

- **Working title candidates** (to score via `title_scorer.py`):
  - "Britain Drew India's Border With a 16-Year-Old Census"
  - "The Partition of India Used Data From 1931"
  - "One 1931 Document Explains Partition's Death Toll"
- **Runtime:** 6 min target
- **Document:** 1931 Census of India page(s) + Radcliffe's working map
- **Editing load:** LIGHT — one document + one map + talking head
- **Research state:** NONE in the system yet → full NLM round needed. Estimated 2-3 days to script.
- **Not in current pipeline folder yet** — will need new project folder under _IN_PRODUCTION

## Secondary — hold Tripoli for later

The Tripoli package that was already drafted isn't wasted. Save it. Six months from now, when the channel has more buffer and can absorb a comment-war week, it's a pre-built episode. Don't delete the work; park it.

## Archive

Save the full VidIQ production package (title variants, script outline, visual storyboard, metadata) as `TREATY-OF-TRIPOLI-PARKED-PACKAGE.md` in this folder. It stays available when the channel is ready for political-heat content.
