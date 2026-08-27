---
name: package-video
description: Build and choose the title and thumbnail for a History vs Hype video. Use whenever Benoit asks about titles, thumbnails, packaging, CTR, why a video isn't getting clicks, what to call something, or asks you to test or score a package — and proactively once a script is locked, since packaging is the part he least enjoys and most needs taken off his hands.
---

# Package the video

Benoit does not enjoy this and says so. It is also the part of the job where his instincts are least trained, so this is work to take off him rather than consult him about at every step — bring him a recommendation and the reasoning, not a menu of twelve options.

## The line that cannot be crossed

Sharp packaging may frame a real dispute or a hypothesis the video will test. It may not promise a conclusion the evidence cannot support.

That is not squeamishness, it is the channel's entire proposition: a title that oversells is the same failure the videos exist to expose. The good version of this constraint is that it points at a better title anyway — the honest tension in the material is usually more interesting than the overclaim. If the answer is genuinely uncertain, the title can promise the *stakes* and the *investigation* rather than a verdict, and the video can return at the end to audit whether the opening claim survived.

## Titles

Start from what the video actually establishes, then find the sharpest true framing of it. Look at the ones that have worked: *The Country That Might Disappear*, *The Flat Earth Myth Was Invented in 1828. Here's Who Did It*, *The $24 Manhattan Sale Is a Myth. No Deed Exists*. Each names a recognisable thing and states a specific, checkable contradiction. None of them is a question with no answer, and none is a category label.

Tools: `vidiq_generate_titles` for volume, `vidiq_score_title` on the shortlist, and `vidiq_youtube_search` on the actual phrasing to see what a viewer would see next to it in results. A title that is strong in isolation and invisible beside its competitors is not strong.

Check three things on every candidate:

- Would someone who has never seen the channel understand the promise?
- Is the contradiction in it real and provable by this video?
- Does it survive being read on a phone at half size, next to five other thumbnails?

## Thumbnails

One recognisable object dominating the frame. The Belize thumbnail worked on a map; the document-card videos work on a page. What consistently fails is a collage — Homer and Virgil and ruins and a manuscript in one image reads as nothing at all. Those belong inside the video.

Text: minimal, three or four words at most, and it should do something the image cannot. Avoid restating the title.

Tools: `vidiq_similar_thumbnails` to see the competitive field before designing anything, `vidiq_generate_thumbnail` and `vidiq_refine_thumbnail` to iterate, `vidiq_score_thumbnail` on the finalists. The field scan matters more than the score — the job is to be the one image that looks different in that row, and a high score on something that looks like everything else is worse than a lower score that stands out.

## Use the channel's own record

`channel-data/` holds the real CTR history: `CTR-THUMBNAIL-FINDINGS-2026-06.md`, `CTR-TITLE-FORMULA-2026-06.md`, `PACKAGING-REFRESH.md`, and the SERP studies under `channel-data/serp-studies/`. These are actual observations from this channel rather than general YouTube advice, so they outrank anything generic — including anything in this file.

Be careful about how much weight they can bear. Most of the catalogue sits under 300 views, which means most package "tests" never got enough impressions to conclude anything. A package comparison needs real exposure before it supports a verdict; treat small-sample differences as noise and say so.

## Record the choice before the result

Write down the chosen title and thumbnail, why they were chosen, and what you expect to happen — before publishing. Then attach the actual numbers afterwards. Log thumbnail files by hash so a later change is traceable.

This is the discipline that turns uploads into evidence. Without it the channel has published four hundred times and still cannot say which packaging decisions worked, which is exactly the position it is in now.

## Retitling and re-thumbnailing old videos

Worth doing, but treat each swap as an experiment with a recorded before-state, not a cleanup task. Change one variable at a time — a simultaneous title and thumbnail swap teaches nothing. Give it enough exposure to mean something before drawing a conclusion.
