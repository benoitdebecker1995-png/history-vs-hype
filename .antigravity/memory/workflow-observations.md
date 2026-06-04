# Workflow Observations

Things learned about how the user actually works (vs how CLAUDE.md describes the ideal).

## Publishing Cadence (2026)
- User publishes in SERIES: a long-form video + 5-7 Shorts from the same topic
- Shorts go out daily over a week, long-form usually publishes early in the series
- Recent series: Bermeja (5 Shorts + 1 LF), Gibraltar (6+ Shorts + 1 LF), Vichy (1 Short + 1 LF so far)
- This means project status jumps from "researching" to "published" quickly — status files get stale fast

## Project State Reconciliation (drift is a bug, not a feature — fixed 2026-05-12)
- When user says "I uploaded/released/published X" / "X is live" / "X went up" — invoke `/reconcile <X>` immediately. The utterance IS the write trigger. Do NOT just look up the video and assume file state. Do NOT just acknowledge.
- `/reconcile` owns: folder moves (`_IN_PRODUCTION/` → `_READY_TO_FILM/` → `_ARCHIVED/published/`), AUTO block in per-folder PROJECT-STATUS.md, root PROJECT_STATUS.md + PROJECT_REGISTRY.md regeneration, `.brain/index.md §3`, memory snapshot deletion on archive (with lessons-promotion prompt — INTERACTIVE mode only).
- Per-folder PROJECT-STATUS.md narrative (below `<!-- /AUTO:reconcile -->`) is hand-written and never overwritten.
- Nightly Routine 6 (08:30) catches publishes missed in conversation. Routine 6 NEVER touches memory snapshots — interactive `/reconcile` does that.
- Truth sources: filesystem → lifecycle stage; `analytics.db` → publish status; in-folder narrative → hand-written.

## Shorts Strategy
- User creates Shorts separately (not through /publish --clips)
- Shorts use YouTube's built-in "link a video" feature, not description links
- Shorts perform well (500-1200 views) but don't visibly drive long-form traffic
- Don't waste time analyzing Shorts with the /analyze tool

## Title/Thumbnail Decisions
- User creates all 3 thumbnail variants (PSD + PNG) BEFORE upload for YouTube native A/B rotation from day 1
- Title/thumbnail pairings are designed together — each title bridges its thumbnail to the hook (bridge strategy, 2026-04-11)
- User adapts packaging to the finished edit, not the other way around ("play the hand you're holding")
- User is responsive to data-backed swap recommendations — Bermeja title swap was immediate once shown data
- Folder lifecycle updates lag behind reality — published videos may still be in _IN_PRODUCTION/

## Video Production
- User films talking head at home
- Uses DaVinci Resolve for editing
- Voiceover recorded separately for B-roll sections
- B-roll is maps, documents, and historical images (not stock footage)

## Script-to-Camera Adaptation (Berlin Conference #40, 2026-03-10)
First systematic comparison of script (02-SCRIPT-DRAFT.md v6) vs actual SRT. Key findings:

**23.4% of script was cut** (1,605 → 1,229 words). The script targeted ~11 min but filmed at ~9 min.

### What Gets Cut (pattern: academic scaffolding)
- **Jargon/technical terms:** "hegemony imperative", "irredentism", "pre-emptive colonisation", "terra nullius", "Organisation of African Unity" — all defined in script, all dropped during filming
- **Secondary examples:** Ewe, Bakongo, Afar ethnic splits all cut. Only Somali kept. Great Zimbabwe cut. Menelik steelman cut.
- **Detailed mechanisms:** Article 35 coastal-vs-interior distinction cut. "Bilateral treaties between 1888 and 1908" cut. "Half a year less schooling" stat cut.
- **Somali detail trimmed:** Flag star symbolism kept but simplified. Ogaden War specifics, Northern Frontier District, five partitioned regions explanation all cut.
- **Leopold detail trimmed:** "Belgium may be a small country" full quote cut — only "magnificent African cake" and "no right to know" kept.
- **Nuance/steelman:** Menelik paragraph and "safety valve" steelman cut from close.

### What Gets Added (pattern: conversational punches)
- **Conversational bridges:** "The big players were all there", "And even the US", "He said that.", "And look at the cost"
- **Dramatic emphasis:** "giving one man an entire country", "the city of a million people", "eight days straight"
- **Updated facts:** "In March 2026, the United States sanctioned Rwanda's military" — added a news hook that wasn't in the script
- **Personal voice:** "So, I went back and read...", "That's another video on its own"

### Implications for Script Writing
1. **Write ~25% longer than target** — user will cut academic scaffolding during filming. A 9-min target needs a ~12-min script.
2. **Jargon gets cut even when defined** — don't rely on technical terms. Use plain language in the script itself; save jargon for text overlays only.
3. **Secondary examples are expendable** — the user keeps ONE strong example per point and cuts the rest. Script should mark primary vs secondary examples clearly.
4. **Steelmans/nuance get sacrificed for pacing** — the user prioritizes momentum over completeness. Put the strongest steelman early (where it survives) not in the close (where it gets cut).
5. **Ad-libs are SHORT conversational punches** — the user's natural delivery adds 3-6 word bridges. Scripts should leave room for these rather than scripting every transition.
6. **News hooks get updated at filming** — user adds current events not in the script. Don't over-specify "modern relevance" sections; leave them flexible.
7. **Leopold/villain sections get the most faithful delivery** — dramatic quotes survive nearly verbatim. Write these tight.

## What User Wants From Claude
- Post-publish monitoring and data analysis
- Title/thumbnail optimization backed by data
- Research assistance and fact-checking
- Script writing (using /script)
- Pattern recognition across videos
- Keeping project files organized and current
- NOT: generic YouTube advice, motivational talk, or speculation without data
