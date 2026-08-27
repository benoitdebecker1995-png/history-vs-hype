# Brain Hygiene — 2026-08-27

## Queue ingested

None. `.brain/_queue/` was empty.

## Lint findings

**5 findings. 1 fixed this run, 2 need your hand, 2 are structural.**

**FIXED — dead internal link in §2.** `.claude/FACT-CHECK-SIMPLIFICATION-RULES.md` did not exist; the
file lives at `.claude/REFERENCE/FACT-CHECK-SIMPLIFICATION-RULES.md`. Row corrected. I path-checked
the other §2 targets; that was the only broken one.

**NEEDS YOU — §1 points at the wrong drive.** All five rows in the Multi-Root Map say
`D:\History vs Hype\`; the repo is on `G:`. The memory root is wrong the same way — it reads
`...\D--History-vs-Hype\memory\`, but the live path is `G--History-vs-Hype`. §1 is a MANUAL section,
so the routine will not touch it.

**NEEDS YOU — the routine's own glob is stale.** STEP 3c globs
`video-projects/_IN_PRODUCTION/*/01-VERIFIED-RESEARCH.md`. Projects #62 and #67 have migrated to the
three-file shape and now use `RESEARCH.md`, so the routine skips them silently — and will skip every
project that migrates next. Five projects still use the old name. Fix is one line in
`.claude/routines/brain-hygiene.md`: glob both names. I did not edit the routine spec; that's outside
this run's write scope.

**STRUCTURAL — §2 routed into superseded material with no precedence marker.** `channel-data/README.md`
declares most top-level `channel-data/` files historical laboratory, "not current instruction," with
current state in `CHANNEL.md` and creator authority in `creator-model/OPERATING-MODEL.md`. §2 had no
rows for any of the new authority surfaces and nothing warning that the old rows are archival. Added a
precedence block plus nine rows.

**STRUCTURAL — §4 was four weeks stale.** Last refresh 2026-07-29. The creator-model v3 import, the
audience/corrections work, the packaging diagnosis, the ADR batch, and the `AGENTS.md` contract layer
all landed since and were never logged.

### Clean

- **0 dead external links** — because no URLs exist in `.brain/**/*.md` at all. The check is vacuous
  here, not passing.
- **0 orphan pages** — re-verified directly rather than inherited from the prior run. All 228
  `sources/` slugs have an inbound mention from `topics/` (78 files). `threads/` is still empty.
- **0 stale `[UNVERIFIED]` claims** — the 11 grep hits are all this routine's own past reports in
  `_inbox/`, quoting its own template.

### Not checkable

**Open contradictions.** `~/llm-brain/wiki/contradictions/` is outside the working directory and could
not be read. Recorded in §5 as UNKNOWN, not as zero — the prior index claimed `0` for this, which
overstated what had actually been checked.

## Index changes

- **§2** — precedence block added (AGENTS.md / CHANNEL.md / OPERATING-MODEL.md as active authority;
  `channel-data/` top level as laboratory; `.claude/` as migration history). Nine rows added for the
  new surfaces. One dead path corrected.
- **§4** — all three prior entries pruned (2026-07-22 and 2026-07-28, past the 14-day window).
  Eleven entries added covering the August architecture work, dated by each artifact's own as-of date
  with a note that they all landed in git on 2026-08-27.
- **§5** — health block refreshed; contradictions downgraded to UNKNOWN; open findings listed inline.
- **§6** — rewritten to carry both research-file shapes, record zero `llm-brain` crossrefs across the
  whole `_IN_PRODUCTION` tree, and flag the stale glob.
- §1 and §3 untouched (MANUAL).

## One note on the prior run

The 15:17 headless run reported that `Glob` "lies about" the `_IN_PRODUCTION` research path — that it
returned no files while five existed. I could not reproduce it: `Glob` returned all seven research
files correctly this run. Whatever happened there, it does not look like a standing tool defect, and
I'd not act on that claim without seeing it again.

---

# Second run — 2026-08-27 22:00 (the scheduled nightly slot)

The 15:44 run above fired off-schedule. This is the 22:00 routine. Appended rather than overwritten
so the earlier findings survive.

## Queue ingested

None. `.brain/_queue/` still empty.

## Lint findings

**No new findings.** I re-ran every check independently instead of inheriting the 15:44 results:

- **0 orphan pages** — recomputed, not copied: 228 `sources/` notes, every slug mentioned from
  `topics/` (78 files). `threads/` is still empty.
- **0 dead internal links** — all 32 resolvable `§2` targets re-checked on disk. (A first pass
  flagged 21 "missing"; all 21 were artifacts of my own matching — `YYYY-MM-DD` placeholders,
  paths relative to `channel-data/`, bare `.py` filenames listed as a group, and the `memory/` root
  which lives outside the repo. None were real.)
- **0 dead external links** — still zero URLs anywhere in `.brain/**/*.md`. Vacuous, not passing.
- **0 stale `[UNVERIFIED]` claims** — 12 grep hits, all this routine's own `_inbox` reports quoting
  its template.
- **Contradictions: still UNKNOWN.** I tried to read `~/llm-brain/wiki/contradictions/` three ways.
  The sandbox refuses any path outside `G:\History vs Hype`. Worth being precise: a `Glob` for
  `llm-brain/**/*.md` returned "no files found," and that is **not** evidence the wiki is gone — it
  is the search being blocked. Recorded as UNKNOWN again, never as zero.

The **3 open findings still need your hand** — none are fixable from inside this routine's write
scope, and all three carry over unchanged: the `D:\` paths in §1, the `D--History-vs-Hype` memory
root in §1, and the stale STEP 3c glob in the routine spec.

## Index changes

- **§2 — one row added.** `channel-data/serp-studies/` had no index row at all, and it is not a
  small corpus: **75** title studies plus topic-level ones. Each study carries an explicit limits
  block — top-12 on a few queries cannot establish that a competitor does not exist. I put that
  warning into the row itself rather than just the pointer, because the failure it documents already
  happened once: on 2026-07-29 a "cleanest whitespace of the session" claim went into project #64 and
  greenlit it, while a 736,169-view specialist video had existed since 2022.
- **§4 — one bullet pruned.** The `2026-08-01` serp-studies entry aged past the 14-day window
  (cutoff 2026-08-13). I added the §2 row *first* so pruning it lost nothing — a standing lookup
  belongs in §2; §4 is only the recency feed. Left a one-line note in §4 recording why.
- **§4 — nothing prepended.** Four files changed today, none of them §4 material: `index.md` is this
  routine's own output, `channel-data/youtube-intelligence.md` is a daily regenerated feed (logging
  it nightly would flood the section), and the two `#62` files are video-project artifacts already
  tracked by §3 and Routine 4.
- **§5** — health block refreshed; queue line added; each figure now says whether it was re-verified
  or inherited.
- **§6** — re-checked, substantively unchanged. Still zero `~/llm-brain/` references anywhere under
  `_IN_PRODUCTION`; 15 projects, 7 with a research file (5 old shape, 2 migrated), 8 with none.
- §1 and §3 untouched (MANUAL).

## One judgment call worth flagging

STEP 3a says to prune anything older than 14 days, full stop. Applied literally that rule fights the
§4 convention of dating bullets by the artifact's own as-of date — the August work landed in git on
the 27th but is dated 14–26 Aug, so entries start aging out within a day or two of first appearing.
Tomorrow the `2026-08-14` bullets fall out the same way. I pruned as specified rather than quietly
bending the rule, but the fix is to decide which date §4 is keyed to: the artifact's or the day the
routine first saw it. That is a spec question, not a lint finding.
