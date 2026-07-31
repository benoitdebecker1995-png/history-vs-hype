# Screen the `Historical negationism` frame — execution brief

This is a **screening** task, not discovery. The frame is enumerable and already identified. Your job is
to run all of it through a staged filter and return only what survives, plus a complete kill record.

## The frame

Wikipedia `Category:Historical negationism` — **54 entries**, free MediaWiki API. Enumerate exactly:

```
https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:Historical%20negationism&cmlimit=500&format=json
```

Also enumerate its immediate subcategories (`cmtype=subcat`) one level deep, and say how many entries
that adds. Do not recurse further.

**Report the exact count you retrieved.** A prior assessment said 54; verify rather than inherit it.

## What qualifies

A claim where history is being used to win a present-day political, ideological or moral argument, and
**no public referee exists at meaningful scale**. Full creator profile and audience in
`.claude/PROMPTS/blind-next-video-discovery.md` — read it. Summary: the creator shows *how* a claim can
be known false or uncertain, with a bounded exhibit the viewer can audit. Audience is politically
engaged men 25–44 in UK/US/DE/CA.

## Staged screen — cheap kills first. Do NOT run stage 3 on anything that fails 1 or 2.

**Stage 1 — free, no API. Kill on any of:**
- Not weaponised in *current* Western political argument (a purely historical dispute is out)
- No bounded exhibit possible — nothing a viewer could inspect on screen
- Audience is a single national/ethnic community outside UK/US/DE/CA
- Not stranger-legible: the stakes can't be understood without prior specialist knowledge
- **Collision:** appears in `analytics.db` published titles, `_IN_PRODUCTION/`, `_READY_TO_FILM/`,
  `_BACKLOG/`, or in the dedupe list below. Flag collisions loudly; existing projects are eligible on
  merit, so a collision is a FLAG not a kill — but say so explicitly.

**Stage 2 — vidIQ, survivors only.** `vidiq_keyword_research` on the plain parent anchor.
Record volume, competition, overall, and **`topMarkets`**. Kill if the pool is dominated by
non-target countries — that is the channel's worst-converting pattern (its one breakout took 30,469
views to 152 subscribers).

**Stage 3 — referee test, survivors only. ADR-0020 applies in full.**
- `serp_title_study` with **≥4 framings**: the partisan wording proponents use, neutral causal wording,
  and combinations with *historian / evidence / debate / debunk*
- **Full uploads-playlist catalogue-check of the 3–6 channels most likely to have refereed it** —
  not `vidiq_outliers` (ranks on breakout/recency, omits older videos even with `sort: viewCount`) and
  not `intel.db` (~100 recent uploads per channel only). Neither can prove absence.
- **ID-verify every reach figure and every candidate referee**:
  `youtube.videos().list(part='snippet,statistics,contentDetails', id=...)` — exact, 1 quota unit
- Write findings as *"searched \<queries\>, catalogue-checked \<channels\>, did not find a referee"*.
  **Never "no referee exists."**

## Dedupe list — already surfaced, do not re-propose as new

industrial revolution living standards · Arab vs Atlantic slave trade volumes · Leopold/Congo death
toll · Panama Canal DeConcini clause · Tacitus' Germania · Native American population collapse ·
African participation in the Atlantic trade · Shroud of Turin · Dead Sea Scrolls forgeries · Gulf of
Tonkin · Hitler Diaries · Magna Carta annulment · Vinland Map · Protocols of the Elders of Zion ·
Willie Lynch letter · Poland–Germany 1953 reparations · Britain's £20m slave-owner compensation ·
"100 million" communism death toll · Bengal famine 1943 · India colonial mortality · EU kept the peace ·
Marshall Plan · enclosure of the commons · Nordic homogeneity · Indian railways · witch hunts as
capitalist war on women · Barbary white slavery · Churchill "chief villain" · Rosa Parks · ancient
DNA/Aryan migration · Black Legend · Operation Legacy · Rome/immigration · Weimar/Hitler · New Deal ·
Reagan/Cold War · medieval peasants' working year · Nazis-were-socialists · NATO "not one inch" ·
Holodomor · trans clinic · Irish famine · Dresden · Wuchale · West Papua · Panglong · Asherah ·
Isaiah 7:14

If a frame entry maps onto one of these, mark it DUPLICATE and move on.

## Budget

Data API ~1 unit per `videos.list` call (50 IDs each) — cheap, use it freely. vidIQ costs 5 credits per
call — stage 2 only, one call per survivor. `serp_title_study` ~5s per query — stage 3 only.
If you exhaust a quota, **say which one and where you stopped.** Do not silently degrade.

## Deliver

1. **Exact frame size retrieved**, and subcategory count
2. **Complete screen table — all entries, one row each:** entry · verdict (KILL/DUPLICATE/FLAG/SURVIVE)
   · stage killed at · one-line reason. This is the reusable asset; do not omit rows.
3. **At most 3 survivors**, each with: the claim as proponents state it · current proponents with dates
   and ID-verified reach · the exhibit · demand incl. `topMarkets` · referee evidence (queries run,
   channels catalogue-checked, closest adjudicator ID-verified) · honest evidentiary map · strongest
   kill reason · confidence on demand / referee gap / exhibit separately
4. **Frame verdict:** was this worth screening? Yield rate, cost, and whether the remaining
   Wikipedia list-article family is worth doing next
5. **What you could not verify**, named

**Kill hard. Zero survivors is a valid and useful outcome** — it prices the frame. Do not promote a weak
entry to have something to show.

Write to `G:\History vs Hype\research\active\FRAME-SCREEN-NEGATIONISM-2026-07-30.md`.
Reply ≤200 words. Final line exactly: `OUTPUT: <absolute path>`
