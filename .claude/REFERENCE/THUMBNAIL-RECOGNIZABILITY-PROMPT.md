# Thumbnail Recognizability Prompt — Manual Gemini Template

**When to use:** When generating thumbnails for a video and the recognizable-anchor pool is unclear. Specifically: gut check fails the recognizability test ("would a cold viewer recognize this visual?") and you need broader cultural-memory data than Claude's main context can provide.

**How to use:**
1. Open Gemini Plus (web UI — no CLI access on Plus plan).
2. Replace `[TOPIC]` and `[VIDEO THESIS]` below with the video's specifics.
3. Paste the full prompt into Gemini, run with deep research mode.
4. Take the top-5 ranked shortlist back into the `/thumbnail` flow as a hard anchor-pool constraint in the notebook query.

**Origin:** Manhattan Purchase Myth (#45) session, 2026-05-07. The prompt surfaced the Alfred Fredericks 1909 painting as the Wikipedia default (a stronger anchor than the Ranney 1853 painting Claude was using), plus the Stuyvesant "wrong Peter" angle and the $24 cultural-idiom data. Multiple thumbnail iteration rounds collapsed into one once the anchor pool was constrained by this research.

---

## Prompt template

```
You are researching visual anchors for a YouTube thumbnail about [TOPIC].

The video's thesis: [VIDEO THESIS]

Your task: find every visual, artifact, image, or cultural touchstone that a general viewer — not a topic specialist — would already recognize and associate with this story. Not what experts know. What an average adult viewer carries in their head from school, films, news, or pop culture.

For each candidate, answer three questions:
1. How widely has this image/artifact been reproduced? (textbooks, Wikipedia, museum exhibits, TV documentaries, popular books, films — cite specifics)
2. Would a viewer recognize it in a 280×157px thumbnail with no caption?
3. Does it carry a built-in surprise or contradiction once the video's thesis is known — i.e., does it become MORE interesting when you learn the video's argument?

Research these categories specifically:

PAINTINGS AND ILLUSTRATIONS
- Which painting/illustration is the "default" image used by Wikipedia and major textbooks for this topic? Who made it, when?
- Are there other paintings or illustrations of this scene that have been widely reproduced?

DOCUMENTS AND ARTIFACTS
- Are there primary documents, artifacts, or objects commonly shown when this story is told?
- Are any of them recognizable to a general viewer outside specialist circles?

PLACES AND LANDMARKS
- Are there specific physical locations or landmarks the public associates with this story?
- How widely known are they — local, national, international?

PEOPLE
- Are any historical figures from this story widely recognized? (Test: does the average person recognize their portrait?)
- Are there any modern people or fictional characters associated with the story in pop culture?

SYMBOLS AND ICONS
- Numbers, phrases, idioms, or symbols embedded in cultural memory for this topic
- Famous uses in films, TV, jokes, political speeches, advertisements

POPULAR CULTURE
- Has this topic appeared in widely-seen films, TV shows, novels, songs, or commercials?
- Is it referenced in school curricula that would make it pre-loaded for specific national audiences?

For each visual you identify, rate it on two scales (1–5):
- RECOGNITION: Would a general viewer (not a specialist) recognize this in a thumbnail?
- CURIOSITY GAP: Does it create a stronger click impulse once you know the video's thesis?

End with a ranked shortlist of the top 5 most promising thumbnail anchors, ordered by RECOGNITION × CURIOSITY GAP product score. For each, name the specific overlay text approach (1–4 words) that would create the strongest curiosity gap WITHOUT spoiling the answer (no verdict words like "FICTION", "LIE", "FAKE" — the overlay should make the viewer ask a question, not give them the conclusion).
```

---

## Output format

Gemini's response should produce a table like:

| Rank | Visual Anchor | Recognition (1-5) | Curiosity Gap (1-5) | Product Score | Overlay Text Idea |
|---|---|---|---|---|---|
| 1 | [Visual] | 5 | 5 | 25 | [overlay] |
| 2 | [Visual] | 5 | 4 | 20 | [overlay] |
| ... | | | | | |

Take the top 2-3 anchors as the constraint pool for the `/thumbnail` notebook query. Reject any anchors below 12 product score (e.g., 3×4 floor) — they're too archival or too generic.

---

## Constraint reminder

Verdict overlay words ("FICTION", "LIE", "FAKE", "FORGED", "INVENTED", "TOTAL FICTION") are forbidden in the overlay output. Gemini's defaults will sometimes return these — strip them before passing the shortlist into the notebook query. Replace with itch overlays that open a question (date paradox, person paradox, "LEGEND", missing-element compression).
