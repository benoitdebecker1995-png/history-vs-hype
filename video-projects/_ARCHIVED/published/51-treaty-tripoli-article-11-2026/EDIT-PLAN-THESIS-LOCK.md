# Edit Plan — Thesis Lock (#5: Invisible-Until-Named)

**Locked thesis:** *Historical texts remain dormant until domestic culture wars require new ammunition.*
**Thesis type:** Invisible-until-named.
**Decision date:** 2026-04-27.
**Constraint:** filming is locked. VO pickup only. Minimum-scope intervention.

---

## What this plan does in one sentence

Cut the last 4.5 seconds of the existing rough-cut close, drop in a ~19-second VO pickup over the `timeline-133-years.html` graphic plus a Crane lower-third super, and the video locks onto thesis #5 with no other re-edit needed.

---

## The locked closing line (decided 2026-04-27)

> *"But Article 11 meant almost nothing until nineteenth-century activists started arguing over the public funding of Christian clergy. The text itself didn't change, but the country did, and we simply projected our new cultural divides onto an old piece of paper."*

**43 words across two sentences. ~19 seconds at calm-prosecutor pace.**

**Why this line landed:**
- **Voice match — your exact "X didn't, but Y did" rhythm.** *"The text itself didn't change, but the country did"* is the same shape as your on-tape *"It wasn't a forgery or a big hoax, it was a translation gap..."* Direct rhythmic callback to your own voice.
- **Anchor: "an old piece of paper"** (the artifact). Closing line points at something physical on screen, satisfies the document-anchored close rule (rough-cut Lesson #31).
- **Job A delivered:** dormancy mechanism — *"meant almost nothing until... arguing over the public funding of Christian clergy."* Names the specific 19th-century domestic fight verbatim from Crane's notebook source (no fabrication).
- **Job B delivered, IMPLIED not stated:** the constructivist thesis ("history sources don't carry inherent objective meaning") emerges from the binary contrast *"the text itself didn't change, but the country did, and we simply projected our new cultural divides..."* The audience builds the thesis from the comparison — no TED-talk-register claim needed.
- **Pairs cleanly with the kept setup line.** Arc: "today it's a weapon" → "it used to be nothing" → "the change is in us, not the document."
- **Crane verbal citation REMOVED from the VO** (per rough-cut Lesson #29). Citation lives in a lower-third super (see B-roll table below) so the voiceover narrates the *story*, not the academic apparatus.

**Booth instructions for the pickup:**
- Match the existing mic, room, and tone of the rough-cut takes (same setup if possible, same time of day for HVAC continuity).
- Record 3-4 clean takes of the full two-sentence line.
- Maintain calm-prosecutor register — verdict delivered evenly, not punched. Understatement does the work.
- Natural breath between the two sentences (the period after "Christian clergy" is ~0.5s breath, not a hard pause).
- Slight emphasis lift on *"didn't change, but the country did"* — this is the binary that carries the thesis; let the contrast land naturally without over-pointing it.
- Leave 2 seconds of silent room tone on either side of the line for clean edit-in/edit-out.
- Save takes as `vo-pickup-close-take-1.wav` through `take-4.wav` next to the existing audio.

---

## Exact edit operations

Reference: `tripoli, rough cut, instincts.srt`. The SRT uses a +1 hour timecode offset — subtract `01:00:00` from each timestamp to get real video time. Closing region runs to real time **6:24.5** (rough cut endpoint).

### KEEP from existing tape (no change)

Audio from the Crane quote through and including the first sentence of the improvised close:

| SRT lines | SRT timecode | Video time | Spoken text |
|---|---|---|---|
| 170-174 | 01:06:01.733 → 01:06:15.599 | 6:01.7 → 6:15.6 | *"Crane writes on page 405: 'the language of article 11 was wielded as often by Christian nationalists as by militant secularists.'"* |
| 174-176 | 01:06:15.599 → ~01:06:19.5 | 6:15.6 → ~6:19.5 | *"Today this English text is wielded as the ultimate weapon in a modern culture war."* |

The "modern culture war." landing falls inside SRT line 176 (`01:06:16.633 → 01:06:20.033` for "weapon in a modern culture war. But the"). The natural breath after "war." occurs at approximately **video time 6:19.5** — that's the cut point.

### CUT from existing tape

| SRT lines | SRT timecode | Video time | Cut audio |
|---|---|---|---|
| 176 (tail) – 179 | ~01:06:19.5 → 01:06:24.533 | ~6:19.5 → 6:24.5 | *"But the Arabic original, it's just a mundane letter between two politicians."* |

**Total cut from existing tape:** **~5.0 seconds** (real measured duration based on SRT timestamps, not the earlier ~6s estimate).

**Why cut:** this line anchors to the wrong artifact for thesis #5. "The Arabic original is just a letter" supports thesis #2 (mechanism / clerical typo), not thesis #5 (constructed-meaning / dormancy → activation). Save the existing "mundane letter" line in a B-roll-of-cuttings folder — it's the spine of a future thesis-#2 sequel.

### INSERT new VO + lower-third

Drop the locked two-sentence VO over the `assets/timeline-133-years.html` graphic.

**Audio handoff:** the cut from existing tape (after "war.") to the new VO needs a clean transition. Two operations:
1. **100ms crossfade** between the existing "war." trailing edge and the start of the new VO's silent room tone. Smooths any room-ambience mismatch.
2. **0.5s silence beat** between the trailing edge of "modern culture war." and the start of new VO sentence 1. The visual cut to the timeline graphic happens during this silence — the eye lands on the graphic before the VO speaks.

**Visual cut:** synchronized with the audio cut. Hard cut from whatever was on screen during "modern culture war" (likely an Article 11 close-up or held shot) to full-frame `timeline-133-years.html` at video time 6:19.5.

**Long-hold treatment for the timeline graphic** (it's on screen ~22 seconds total):
- Sentence 1 (~9s): static graphic, full frame.
- Sentence 2 (~10s): at the breath between sentences, cross-fade-in a subtle highlight on the central "133 YEARS OF SILENCE" label (from `_shared.css` accent color `#E8D9A8` to a brighter pulse) — visual punctuation matching the verbal pivot from "the text didn't change" to "but the country did."
- Final 2s: held silence on the graphic with the highlighted state.

The graphic-pulse implementation can be either:
- **Editor crossfade:** render two stills of the timeline (unhighlighted + highlighted) and crossfade in the editor at the pivot moment. Simplest. Can render the highlighted variant from a modified `timeline-133-years.html` (just bump the `.silence-label` color and add subtle scale: 1.05 transform).
- **Animated HTML:** add a CSS keyframe pulse to `.silence-label` that triggers at the right video frame. More work for marginal gain.

Recommend the editor crossfade.

### Final closing structure (after edit)

```
[6:01.7, existing tape KEEP, on-screen `quote-card-5-crane-405.html`]
"Crane writes on page 405: 'the language of article 11 was wielded as
often by Christian nationalists as by militant secularists.'"

[6:15.6, existing tape KEEP, on-screen Article 11 close-up or held shot]
"Today this English text is wielded as the ultimate weapon in a modern
culture war."

[6:19.5, HARD CUT — visual + audio]
- Visual: Article 11 / held shot → full-frame `timeline-133-years.html`
- Audio: 100ms crossfade existing tape → new VO room tone

[6:19.5 → 6:20.0, 0.5s silence on the graphic — eye lands]

[6:20.0, NEW VO sentence 1, on-screen timeline graphic + lower-third
super fades in over the bottom third]
"But Article 11 meant almost nothing until nineteenth-century activists
started arguing over the public funding of Christian clergy."

[6:29.0, ~0.5s breath / lower-third fades out, graphic-label cross-fade
begins to highlighted state]

[6:29.5, NEW VO sentence 2, on-screen timeline graphic with highlighted
"133 YEARS OF SILENCE" label]
"The text itself didn't change, but the country did, and we simply
projected our new cultural divides onto an old piece of paper."

[6:39.5, hold on timeline graphic, 2s silence]

[6:41.5, FINAL CUT to black or end-screen]
```

**Total cut from existing tape:** ~5.0 seconds (the "Arabic original / mundane letter" line).
**Total VO added:** ~19 seconds (43-word locked close + 0.5s pre-silence + 0.5s mid-breath + 2s post-silence = ~22s of new graphic-on-screen time).
**Net runtime change:** **+17 seconds** vs the rough cut. Original 6:24.5 → new ~6:41.5.

**Runtime flag:** the new total runtime (~6:41) is over the 6:00 stated target in `PROJECT-STATUS.md`. The rough cut was already at 6:24, so this is +17s on top of an already-over cut. Per the channel data (12-min hard cap, 8-12 min sweet spot), 6:41 is well within retention parameters. Acceptable trade for thesis lock.

---

## B-roll + lower-third for the closing region

| Video time | Beat | B-roll asset / on-screen element |
|---|---|---|
| 6:01.7 | Crane quote (kept tape) | `assets/quote-card-5-crane-405.html` — fade in over reading the verbatim Crane quote. Hold through the kept tape. |
| 6:15.6 | "modern culture war" (kept tape) | Brief composite or Article 11 close-up from the HathiTrust scan. Keeps the document on screen during the weaponization line. Acceptable fallback: dim to charcoal if no fitting B-roll. |
| 6:19.5 | HARD CUT to timeline graphic | `assets/timeline-133-years.html` — full-frame, 4K screenshot. Single still until the pulse cue. |
| 6:20.0 | Lower-third super fades in (1.5s ease) | Citation lower-third — see spec below. Fades out at 6:29.0 before VO sentence 2. |
| 6:20.0 | VO sentence 1 over graphic | "But Article 11 meant almost nothing until nineteenth-century activists started arguing over the public funding of Christian clergy." |
| 6:29.0 | Lower-third fades out (0.5s) + label pulse begins | Crossfade timeline graphic from unhighlighted state → highlighted "133 YEARS OF SILENCE" state (0.5s ease). |
| 6:29.5 | VO sentence 2 over highlighted graphic | "The text itself didn't change, but the country did, and we simply projected our new cultural divides onto an old piece of paper." |
| 6:39.5 | Hold in silence, 2s | Static highlighted graphic, no audio. The silence is the verdict. |
| 6:41.5 | Final cut | To black or end-screen. |

**Critical:** the timeline graphic is the visual anchor for the new VO. Don't cut away from it after 6:19.5 until the final cut. Silence + held graphic = the thesis landing.

### Lower-third super spec (Crane citation, 6:20.0 → 6:29.0)

Carries the verbal Crane citation that we removed from the VO. Lives in the bottom 18% of the frame, fades in/out, doesn't compete with the timeline graphic above it.

**Three-line stack, left-aligned, bottom-left of frame:**
```
Line 1 (4px gold accent line, 80px wide, color #E8D9A8)
Line 2 (serif, ~32px cream #F4EDE0):    Jacob Crane
Line 3 (sans italic, ~20px muted #B8A88E):  "Reading American Secularism in the
                                              1797 Treaty of Tripoli"
Line 4 (sans uppercase, ~14px, letterspaced 0.18em, color #8A7B66):
                                              AMERICAN QUARTERLY 72:2 (2020), P. 405
```

Match the design system in `assets/_shared.css`. Same typography, same color palette, same gold accent.

**Animation:**
- Fade in: 1.5s ease-in starting at video time 6:20.0 (synchronized with the start of VO sentence 1).
- Fade out: 0.5s ease-out starting at 6:29.0 (just before VO sentence 2). The lower-third does NOT compete with the thesis-landing line — sentence 2 is the verdict, and the citation has done its job by then.

**If you want me to build this lower-third as an HTML/CSS asset** (render-and-screenshot like the other graphics), say the word and I'll add `assets/lower-third-crane.html` to the asset library.

### Asset modification needed: timeline-133-years label pulse

The existing `assets/timeline-133-years.html` has the "133 YEARS OF SILENCE" label as a static element. For the pulse cue at 6:29.0:

**Option A (recommended) — render a second still:** I duplicate `timeline-133-years.html` as `timeline-133-years-highlighted.html` with the `.silence-label` boosted (color → brighter cream, font-weight bumped, transform: scale(1.06)). You crossfade between the two stills in your editor at the pivot moment. Cleanest, most editor-controllable.

**Option B — animate inside the HTML:** add a CSS keyframe pulse to the existing file triggered at a fixed time. Limits when you can use the graphic to scenarios where the timing exactly matches the recorded VO.

Tell me to ship Option A and I'll add the highlighted variant to the asset library now.

---

## Pickup record protocol

1. **Setup match:** same mic, same room, same distance, same level. Compare a test take against the rough-cut audio waveform / EQ — if it sounds different, fix before the real take.
2. **Tone match:** listen to the last 30 seconds of your existing close before recording. Match that energy. Don't try to "punch" the verdict — the verdict lands because of WHAT it says, not HOW.
3. **Take count:** 3-4 clean takes minimum. Variations on emphasis ("paper for 133 years" vs "Then somebody needed it") so the editor can pick.
4. **Editor split:** save the takes as `vo-pickup-close-take-A1.wav`, `take-A2.wav`, etc. in `_research/documents/` or wherever the original audio lives.

---

## What this leaves on the table (intentional)

This minimum-scope plan does NOT:
- Reframe the hook to lead with dormancy (would require re-recording the cold open — out of scope).
- Add a mid-video insert to push thesis #5 explicitly during the Crane section (Modest scope, declined).
- Reshoot any on-camera material (filming locked — not possible).

If retention data on the published video shows the audience disengages before the close lands, the next-tier intervention is the Modest scope (close + mid-video insert). Until then, the single VO pickup is the highest-leverage minimum.

---

## Update to project artifacts after edit lock

When the new close is in the cut and approved:

1. Update `PROJECT-STATUS.md` — add a "Locked thesis (2026-04-27)" line under packaging:
   *"Thesis: Historical texts remain dormant until domestic culture wars require new ammunition. (Type: invisible-until-named.) Locked closing line: [chosen Option A/B/C verbatim]."*
2. Update `02-SCRIPT-DRAFT.md` — add `**Thesis (≤12 words):**` and `**Thesis Type:**` to the metadata block per Rule 36 (script-writer-v2 v14.4).
3. Update `YOUTUBE-METADATA.md` description first line — consider whether the chosen thesis line should appear as the description's lead sentence (per `publish` skill: "First line = thesis/hook").

---

## Sequel seed (separate move, not part of this edit)

Thesis #5 is the strongest universalizable thesis surfaced by NotebookLM. Same sentence ("dormant text → activated by later culture wars") could caption:
- The Second Amendment's individual-rights interpretation (post-Heller 2008)
- The 14th Amendment's incorporation doctrine (long dormant, activated mid-20th century)
- Magna Carta (largely irrelevant for centuries, rediscovered in the 17th century English Civil War)
- The Commerce Clause (dormant, then activated post-1937)
- The 1948 Genocide Convention (dormant for ~50 years until ICTY/ICTR)

A sequel video that walks 3-4 of these cases under thesis #5 is a strong channel-growth move (anchor the pattern as a series). If you want, I can plant this as `999.x` backlog item via `/gsd-add-backlog` or write a one-pager seed file in `channel-data/`. Tell me if/where.
