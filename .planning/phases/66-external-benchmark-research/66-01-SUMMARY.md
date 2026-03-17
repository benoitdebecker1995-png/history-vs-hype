---
phase: 66
plan: 01
status: complete
started: 2026-03-17
completed: 2026-03-17
---

## Summary

Extracted real benchmark data from 5 YouTube channels (4 format-matched + 1 title-pattern-only) using yt-dlp for video metadata and youtube-transcript-api for hook transcripts.

## Key Results

- **239 videos analyzed** across 5 channels with real view counts
- **26 hooks extracted** from actual YouTube transcripts (22 usable after filtering sponsor reads)
- **15 3x+ outlier videos** identified across all channels
- CTR tracker confirmed fresh snapshot (2026-03-17, 48 videos)

## Deviations

1. **Shaun excluded** — has 192K subscribers (plan assumed 760K). Below 500K threshold. Result: 4 format-matched channels instead of planned 5.
2. **7 hooks failed** — 4 Fall of Civilizations (en-GB only, rate-limited), 3 Toldinstone (IP rate-limited). Backfill script written at `tools/benchmark/backfill_hooks.py`.
3. **VidIQ not used** — user confirmed VidIQ only useful for keyword search volume/competition, not CTR verification.
4. **No "versus" benchmark** — only 1 versus title found in sample (n=1, LOW confidence).

## Artifacts

### key-files.created
- `channel-data/niche_benchmark.json` — views/sub ratio benchmarks by pattern and topic type
- `channel-data/niche-hook-patterns.md` — human-readable hook analysis with verbatim examples
- `.claude/REFERENCE/HOOK-PATTERN-LIBRARY.md` — agent-parseable hook library (5 pattern sections)
- `tools/benchmark/extract_channel_data.py` — yt-dlp channel extraction script
- `tools/benchmark/extract_hooks.py` — transcript hook extraction script
- `tools/benchmark/build_deliverables.py` — builds all 3 deliverables from raw data
- `tools/benchmark/backfill_hooks.py` — fills missing hooks after rate limit clears
- `tools/benchmark/raw_data/` — raw JSON per channel + verified hooks

### key-files.modified
- `.planning/STATE.md` — updated with phase 66 progress

## Self-Check: PASSED

- [x] niche_benchmark.json exists with metadata, by_pattern (5 types), by_topic_type (3 types)
- [x] niche_benchmark.json channels_sampled >= 5 (has 5)
- [x] niche-hook-patterns.md exists with verbatim transcript hooks
- [x] HOOK-PATTERN-LIBRARY.md has >= 4 pattern sections (has 5)
- [x] CTR tracker run confirmed fresh (2026-03-17)
- [x] All data from real YouTube sources, no training-data fabrication
