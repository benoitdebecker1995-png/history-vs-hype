---
name: diagnosing-retention
description: Reads a History vs Hype video's audience-retention curve against its script to find where viewers leave and why, and returns specific script changes for the next video. Use when asked about retention, watch time, drop-off, why people don't finish, whether an opener works, or how a video actually performed beyond views. Distinguishes structural problems from noise on low-view videos.
---

# Diagnosing retention

Views measure the thumbnail and title. Retention measures the video. They fail for different reasons and confusing them wastes work — a strong retention curve on a video nobody clicked is a packaging problem, and a weak curve on a video with good click-through means the promise was not kept.

## Get the curve

```
vidiq_channel_analytics
  channelId: the channel
  report: audience_retention
  filters: video==VIDEO_ID
```

That returns `audienceWatchRatio` across a hundred points of elapsed time, plus `relativeRetentionPerformance` where YouTube has enough data — the relative figure is more useful than the absolute one, because it compares against videos of similar length rather than against an ideal.

Then get the transcript or the script and map timestamps to beats, so a drop can be attributed to something specific rather than to a percentage.

## Read the first thirty seconds separately

The opening is a different question from the rest of the video and needs a different fix.

A steep opening drop usually means one of three things: the thumbnail and title promised something the first sentences do not deliver; the video takes too long to reach the actual question; or the opening is doing setup that the viewer did not ask for yet. All three are fixable in the writing and none is fixable in the edit.

Compare the opening drop across several videos before concluding anything about a single one — an opener problem that recurs is a craft pattern worth changing, while one bad opener is one bad opener.

## Read the body for beats that did not earn their place

In the rest of the curve, look for shape rather than absolute level:

- **A cliff** — an abrupt drop at one point. Something specific happened there. Find the beat and name it.
- **A slope** — steady decline with no feature. Usually the argument stopped progressing; the viewer is being told more about something they already understood.
- **A recovery or plateau** — attention returning. Note what was on screen, because that is a thing to do more of. Recoveries are more informative than drops and get looked at less.
- **A drop at a document or exhibit** — the visual was doing less work than assumed, or it interrupted the argument rather than advancing it.

## Be honest about sample size

Most videos on this channel have low view counts, and a retention curve built from a small number of sessions is noisy. A curve from a few dozen viewers cannot support a confident claim about a specific beat.

Say the sample size alongside the finding. Where the numbers are too thin, look for patterns across several videos rather than resolution within one — and where even that is thin, say the evidence does not support a conclusion. Manufacturing a diagnosis from noise is how the previous system generated documents that changed nothing.

The channel's earlier retention and opener work is in `channel-data/` — the opener craft and retention diagnosis files, and the analyses folder. Check whether a finding is new before presenting it as new.

## Output

Specific script changes, not a description of the curve. "Viewers drop 22% between 1:10 and 1:40, which is the treaty-background section — that context arrives before the viewer has a reason to want it, so move it after the first document" is useful. "Retention declines through the middle third" is not.

## The timing rule that matters

Retention findings apply to the **next** video. They are not grounds for reopening a locked script or refilming a finished one — that is `deciding-to-ship`, and past a filming lock the bar is that the video is wrong, not that it could hold attention better.

The exception is a video not yet filmed, where a recurring opener pattern is worth fixing before recording rather than after.
