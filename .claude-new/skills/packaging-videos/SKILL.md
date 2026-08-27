---
name: packaging-videos
description: Builds and chooses the title and thumbnail for a History vs Hype video, and records the choice so it becomes evidence. Use when asked about titles, thumbnails, packaging, CTR, click-through, what to call a video, why something isn't getting clicks, or to score or test a package — and proactively once a script locks, since this is the part of the job he least enjoys.
---

# Packaging videos

He does not enjoy this and says so, and it is the part of the work where his instincts are least trained. Take it off him rather than consulting him at every step: bring a recommendation and the reasoning, not a menu of twelve options.

## The line that cannot be crossed

Sharp packaging may frame a real dispute or a hypothesis the video will test. It may not promise a conclusion the evidence cannot support.

That is not squeamishness — a title that oversells is the same failure the videos exist to expose. The useful thing is that the constraint usually points at a better title anyway: the honest tension in the material is more interesting than the overclaim. Where the answer is genuinely uncertain, the title can promise the stakes and the investigation rather than a verdict, and the video can return at the end to audit whether its opening claim survived.

## Titles

Start from what the video actually establishes, then find the sharpest true framing of it.

The ones that have worked on this channel name a recognisable thing and state a specific, checkable contradiction — a country that might disappear and a court about to decide; a myth with a date and a named inventor; a famous sale with no surviving deed. None is a question without an answer, and none is a category label.

Tools: `vidiq_generate_titles` for volume, `vidiq_score_title` on the shortlist, and `vidiq_youtube_search` on the actual phrasing to see what a viewer would see beside it. A title strong in isolation and invisible next to its competitors is not strong.

Check three things on every candidate:

- Would someone who has never seen the channel understand the promise?
- Is the contradiction real, and provable by this video?
- Does it survive being read on a phone at half size, beside five other thumbnails?

## Thumbnails

One recognisable object dominating the frame. What consistently fails is a collage — four subjects in one image reads as nothing. Those belong inside the video.

Text: minimal, three or four words at most, doing something the image cannot. Avoid restating the title.

Tools: `vidiq_similar_thumbnails` to see the competitive field *before* designing anything, `vidiq_generate_thumbnail` and `vidiq_refine_thumbnail` to iterate, `vidiq_score_thumbnail` on finalists. The field scan matters more than the score — the job is to be the one image that looks different in that row, and a high score on something that looks like everything else is worse than a lower score that stands out.

## Use the channel's own record

`channel-data/` holds the real CTR history — the thumbnail and title findings files, `PACKAGING-REFRESH.md`, and the SERP studies under `channel-data/serp-studies/`. These are observations from this channel rather than general YouTube advice, so they outrank anything generic, including this file.

Be careful how much weight they can bear. Most of the catalogue has very low view counts, which means most package "tests" never got enough impressions to conclude anything. A package comparison needs real exposure before it supports a verdict; treat small-sample differences as noise and say so rather than reading a pattern into them.

## Record the choice before the result

Write down the chosen title and thumbnail, why they were chosen, and what you expect to happen — before publishing. Attach the actual numbers afterwards. Log thumbnail files by hash so a later change is traceable.

This is the discipline that turns uploads into evidence. Without it the channel has published hundreds of times and still cannot say which packaging decisions worked.

## Retitling and re-thumbnailing old videos

Worth doing, but treat each swap as an experiment with a recorded before-state, not a cleanup task. Change one variable at a time — a simultaneous title and thumbnail swap teaches nothing. Give it enough exposure to mean something before drawing a conclusion.
