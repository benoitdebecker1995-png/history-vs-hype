# WHICH BARRIER HAS DEMAND — first measurement

**Date:** 2026-07-29 · **Corpus:** 330 videos · 30 channels · **79,920 comments** · 9,712 tagged signals
**Question:** set by the owner interview the same day — he declined to pre-commit on which access
barrier the channel should lead with, and assigned it to measurement. This is the first answer.
**Store:** `intel.db.comment_signals` · view: `HARVEST-DIGEST.md` · code: `tools/discovery/gap_hunter.py`

## How to execute this doc

Read §1 and §4. §4 is the part that changes what gets made next. **Nothing here locks a barrier** —
§3 says why the evidence isn't strong enough to.

---

## 1. The result

Signals per 1,000 comments. **Rows = what viewers ask for. Columns = what the channel they're
watching already serves.** The diagonal is supply-induced and near-meaningless; the off-diagonal
cells are demand appearing where it *isn't* being met.

| viewers ask for ↓ / channel serves → | enclosure | language | ideology | reach | **all** | n |
|---|---:|---:|---:|---:|---:|---:|
| **language** | **8.35** | 26.33 | **6.79** | 2.49 | **7.33** | 586 |
| **ideology** | 2.00 | 2.55 | 5.50 | 2.81 | 3.49 | 279 |
| **method** | 1.28 | 2.41 | 1.52 | 1.09 | 1.39 | 111 |
| **enclosure** | 0.72 | 3.54 | 0.68 | 0.60 | 0.91 | 73 |
| **archive** | 1.28 | 2.12 | 0.64 | 0.32 | 0.80 | 64 |

*Corpus denominators: enclosure 17,973 · ideology 26,380 · language 7,065 · reach 28,502 comments.*

**Language is voiced twice as often as anything else** — 586 of 1,113 barrier-tagged signals (53%) —
and, unlike the others, it is voiced heavily on channels that are *not* serving it: 8.35/1k on
enclosure channels and 6.79/1k on ideology channels. That is the one genuine off-diagonal signal in
the table.

**Nothing else separates.** Ideology, method, enclosure and archive all sit between 0.8 and 3.5.

---

## 2. Three things that are NOT findings, and why

**a) Like-weight cannot rank barriers. Every class is outlier-driven.**

| barrier | n | median | p90 | mean | max |
|---|---:|---:|---:|---:|---:|
| language | 586 | 2 | 49 | 33.2 | 3,291 |
| ideology | 279 | 5 | 97 | 62.0 | 5,947 |
| method | 111 | 3 | 44 | 30.9 | 797 |
| enclosure | 73 | 1 | 19 | 28.9 | 580 |
| archive | 64 | **4** | 32 | **176.0** | **10,104** |

`archive`'s mean of 176 comes from a **single** comment praising Johnny Harris's use of primary-source
footage. Its median is 4. Any barrier ranking by average likes is measuring one viral comment.
`aggregate_barriers()` now reports median and p90 beside the mean so this can't be re-hidden.

**b) The first version of this measurement was wrong, and I ran it before catching it.**
The initial classifier scored `enclosure` highest at 98 average likes. Auditing the actual comments
showed the top hits were *"first time i've heard the narrator angry"* (14,865), *"bro has never heard
of planning things"*, *"never heard anyone say ANZ like that"* — the patterns `never heard` /
`had no idea` / `mind blowing` are ordinary English idiom, and viral jokes were driving the score.
Patterns tightened to require withheld knowledge (curriculum, schooling, access to scholarship);
`ideology` likewise lost bare `myth` / `narrative` / `bias` / `agenda`, which are just how comment
sections talk. **Enclosure fell from 443 signals to 73.** Treat any earlier number as void.

**c) Low enclosure signal is an instrument limit, not evidence against enclosure.**
People do not write *"why was I never taught this"* — they write nothing, or they write about the
topic. Comment mining measures what viewers **say**, and enclosure demand is mostly silent.
**This method cannot test the enclosure thesis.** Retention and search behaviour could; comments can't.

---

## 3. The hard constraint on the one positive finding

The language signal is real, but look at where it concentrates. The highest-engagement language
comments are overwhelmingly on **scripture and ancient-text channels** — ReligionForBreakfast,
Let's Talk Religion, Esoterica, World of Antiquity, Ancient Americas — and they are about **Arabic,
Greek, Hebrew, Syriac, Tupi**:

- *"It's crazy how much evangelical theology is based on poorly translated Greek transcriptions of Hebrew texts. Typo theology"* — 287 likes
- *"I don't know where people get the audacity to correct experts on translations of languages they're not fluent in"* — 457
- *"As someone who's fluent in Arabic, it's very clear to me that Al-Khal' and Al-Hafd are normal Dhikr, not Quranic Chapters"* — 451

**The owner reads FR/ES/DE/Dutch.** The hottest language pocket is in languages he cannot verify, and
the channel's rule is real quotes with page numbers from sources he can check. His languages show up
mainly on History With Hilbert, Three Arrows and Ancient Americas, at materially lower volume.

So the honest statement is: **the language barrier draws the most demand, and the channel can only
reach part of it.** Volhynia-style work (Polish/Ukrainian) already required outside verification;
that cost is the strategy's real price, not a detail.

⚠ Also: roughly 15–20% of `language` hits are still false positives (*"administrative translation for
'we don't know what we're doing'"*). The 2× lead over ideology survives that; a 20% lead would not.

---

## 4. What this changes

1. **Language-barrier work is promoted from "the Untranslated series" to the channel's best-evidenced
   demand.** It has been treated as one format among several. It's the only barrier with an
   off-diagonal signal.
2. **Prefer source languages the owner reads** — and when a topic needs one he doesn't, budget the
   verification cost explicitly at greenlight rather than discovering it mid-research.
3. **Do not kill the enclosure thesis on this data.** It is untested, not disproven. If it matters
   enough to decide, it needs a different instrument — a deliberate A/B between an enclosure-framed
   and a language-framed video, measured on retention, not comments.
4. **Barrier demand is a niche-audience phenomenon.** On the mass-reach channels (RealLifeLore,
   Johnny Harris, Wendover, Mr. Beat) *no* barrier clears 2.9/1k. Combined with the standing finding
   that **serve size, not click-through, is this channel's binding constraint**
   (`BREAKOUT-MECHANICS-2026-07.md`), the sober reading is that barrier-led topics build a loyal
   audience and **should not be expected to fix discovery**. Those are two different problems.

## 5. Re-running this

```bash
python -m tools.discovery.gap_hunter --sweep --videos 330 --comments 200 --min-views 15000 --no-skip-swept
```
Then `--reclassify` (free, no API) after any pattern change, and `--digest`. Both now refuse to
half-finish rather than silently truncating — two truncation bugs found and fixed during this run.
