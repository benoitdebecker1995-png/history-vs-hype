# Routine 1 — Daily Competitor Drop Scanner

**Purpose:** Every morning, know what the 10 tracked competitor channels uploaded in the last 24h and flag any upload that collides with an active project in `_IN_PRODUCTION/`.

**Schedule:** Daily, 07:00 local.
**Expected cost:** 1 of the 5 daily Routines credits.

---

## Paste this into claude.ai/code/routines (the "prompt" field)

```
You are operating inside the History vs Hype repository.

STEP 1 — Run the competitor drop scan:

  python -m tools.routines.competitor_drop_scan --lookback-hours 24

This fetches YouTube RSS for every channel in
channel-data/competitor-channels.yaml, identifies uploads in the last 24h,
and cross-references against video-projects/_IN_PRODUCTION/ for topic
overlap. It writes:
  - channel-data/competitor-drops/YYYY-MM-DD.json
  - channel-data/competitor-drops/YYYY-MM-DD.md

STEP 2 — Read the generated .md file for today.

STEP 3 — For every entry under "COLLISIONS":
  a. Fetch the video page (WebFetch) and pull: published date, view count,
     like count, duration, and the first 500 chars of the description.
  b. Compare its framing to the conflicting project's current YOUTUBE-METADATA.md
     (title, angle, thumbnail concept).
  c. Decide: is this a real collision (same angle, same audience) or a
     false positive (shared keywords, different topic)?
  d. If real: propose ONE concrete differentiation move for the affected
     project — different angle, different title frame, or different hook artifact.

STEP 4 — For every entry under "Other new uploads (no collision)":
  Scan the title only. If any looks like a format/packaging pattern worth
  stealing (e.g., a new hook type, a new comparison frame, an unusual thumbnail
  cue visible in the title), note it in one line.

STEP 5 — Append findings to channel-data/competitor-drops/YYYY-MM-DD.md
under a new section "## Analyst notes". Keep it terse — one paragraph per
collision, one line per pattern-steal candidate. Don't repeat what the
auto-generated report already contains.

STEP 6 — If there is at least one REAL collision OR one high-value pattern
to steal, commit the updated .md:
  git add channel-data/competitor-drops/
  git commit -m "competitor scan YYYY-MM-DD — <one-line summary>"
  git push

If nothing is interesting, still commit the raw report but skip the analyst
notes section entirely.

STEP 7 — Stop. Do not touch any other file. Do not modify video projects.
This is a read-mostly, report-only routine.
```

---

## Allowed tools (set in the Routines UI)
- Bash (for the python invocation, git)
- Read
- Write (to append analyst notes)
- WebFetch (for competitor video pages)
- Grep / Glob (to cross-reference projects)

## Guardrails
- **Never** edit files under `video-projects/_IN_PRODUCTION/*/SCRIPT-DRAFT.md` or similar.
- **Never** push to any branch other than `master`.
- If the scan errors out (network issue, RSS 403), commit the error report and stop — don't retry more than once.

## Interpreting results
- **0 collisions, 0 pattern-steals:** expected on most days. No action.
- **1+ collision on a filming-ready project:** urgent — flag in the next `/status` check.
- **Pattern-steal candidate:** add to `channel-data/TOPIC-PIPELINE.md` under a "Format ideas" section when you next run `/greenlight`.
