---
name: "source-command-grill-angle"
description: "Pre-research angle interrogation — grills a video's thesis/hook one question at a time BEFORE /greenlight, then writes a GO / REFRAME / KILL verdict with the sharpened angle. Use before sinking research hours into a topic."
---

# source-command-grill-angle

Use this skill when the user asks to run the migrated source command `grill-angle`.

## Command Template

# /grill-angle — is this angle worth researching?

The cheapest place to fix the channel's #1 bottleneck (packaging → distribution; 27/56 videos die *not-clicked*) is **before research**, on the angle itself. This command interrogates the angle the way `/voice grill` interrogates a line — one question at a time — and ends on a verdict you can hand to `/greenlight`.

Runs on a topic idea or an existing project. It does NOT check demand/titles/thumbnails mechanically (that's `/greenlight`, which runs *after* this) and it is NOT about delivery (that's `/voice`). It sharpens the *thesis* so `/greenlight` packages something worth clicking.

## The grill loop (invariants)

- **One question at a time.** Ask, give your **recommended answer**, wait for his call, then advance. Multiple questions at once is bewildering.
- **Ask in chat**, never the truncating `AskUserQuestion` box — the answers are nuanced.
- **Facts you can look up, you look up** (competitor SERP, whether a claim is famous) — don't ask what a search settles. **Decisions are his**; put each to him.
- **Walk the tree in order**; a weak answer early (no one holds the belief; it's a WHY-narrative; it dies the 10-year test) can KILL the angle before the later questions matter.

## The decision tree (walk top-down)

Each rung is a known channel angle-strength lever; the parenthetical routes to where it's justified.

1. **The belief** — Who *actually* holds the myth you're busting, and where do they hold it? If you can't name a real audience that believes it, there is no myth to bust — reframe or kill. (*famous-gate*, [[feedback-famous-gate-myth-framing]])
2. **The anchor** — What FAMOUS parent keyword does a viewer search? Every angle needs a head-term anchor; obscure-only = no impressions. (*keyword ladder*, [[feedback-keyword-ladder-packaging]])
3. **The reveal** — What obscure, counterintuitive thing does that famous anchor deliver *into*? The gap between the two is the video. Anchor famous, deliver obscure.
4. **The claim on trial** — Reduce it to ONE weaponized claim (or a claim-pair) the video puts *on trial*. If you can't state the single claim, the spine is mushy. (referee/debunk architecture, [[feedback-debunk-architecture]])
5. **HOW > WHY** — Is the spine a **mechanism** (logistics, legal, administrative) or a politics/WHY narrative? The subscriber trigger is intellectual competence via *systems*. A WHY angle gets reframed to its HOW, or it loses the audience. (`AGENTS.md` subscriber trigger)
6. **The 10-year test** — Does the modern relevance survive a decade regardless of who's in power? Timely event = a hook only, never the spine. Evergreen, not news. (*history channel not geopolitics*, [[feedback-evergreen-not-news]])
7. **Identity guard** — Method-first, never a regional/geopolitics explainer. If the angle only works because of *where* it happened, it's off-identity. ([[feedback-channel-identity-not-regional]])
8. **The shareable gem** — What single fact does a viewer repeat at dinner? Distribution needs a spreadable core, not just a correct one.
9. **The click** — Can this become a title + thumbnail that gets CLICKED — recognition × stakes × curiosity, minus abstraction? Name the rough title and the thumbnail's one focal idea *now*; if you can't, the packaging fight is already lost. ([[reference-ctr-packaging-playbook]])
10. **Saturation** — Who already owns this thesis, and is your angle a *differentiation* or a retread? Use their saturated thesis as your SETUP, not your thesis. (`competitor-gap` agent for the real shelf.)

## Completion criterion

Done when a **verdict block** is written and every field is filled — a fuzzy field means the grill isn't finished:

```markdown
## Angle Grill — <topic> (<YYYY-MM-DD>)
**Verdict:** GO / REFRAME / KILL
**Sharpened thesis (1 line):** …
**Famous anchor → the reveal:** … → …
**Claim on trial:** …
**HOW-spine (mechanism):** …
**10-year rhyme:** …
**Shareable gem:** …
**Rough title + thumbnail focal:** …
**Differentiation vs the shelf:** …
**Open questions for /research:** …
```

Write it to the project's `_research/ANGLE-GRILL.md` (create the folder if the project exists); if there's no project folder yet, surface the block in chat and offer to create the project on a GO. **On GO → hand off to `/greenlight`** (it packages the sharpened thesis); on REFRAME → re-grill the changed rung; on KILL → say why, in one line, and stop before any research cost.

## Related
- `/greenlight` — the mechanical viability gate this feeds (demand + titles + thumbnails).
- `/voice grill` — the same one-at-a-time interrogation, applied to delivery instead of angle.
- `/next` — where topic *candidates* come from; this grills a candidate you've already chosen.
