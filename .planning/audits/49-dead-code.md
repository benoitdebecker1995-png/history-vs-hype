# Phase 49 Audit: Dead Code Cleanup

## 1. Known Dead Files

| File | Size | Referenced? | Verdict |
|------|------|-------------|---------|
| `tools/youtube-analytics/_csv_backfill.py` | ~276 lines | No imports found | DELETE |
| `tools/youtube-analytics/_competitor_fetch.py` | ~244 lines | No imports found | DELETE |
| `tools/youtube-analytics/_longform_all.json` | JSON artifact | No imports found | DELETE |
| `tools/youtube-analytics/_longform_enriched.json` | JSON artifact | No imports found | DELETE |
| `tools/youtube-analytics/_longform_ids.json` | JSON artifact | No imports found | DELETE |
| `tools/youtube-analytics/_longform_metrics.json` | JSON artifact | No imports found | DELETE |
| `tools/youtube-analytics/_backfill_ids.txt` | Text artifact | No imports found | DELETE |

All prefixed with `_` — convention for temporary/scratch files. None are imported anywhere.

## 2. datetime.utcnow() Usage

**Zero occurrences found.** The codebase already uses `datetime.now(timezone.utc)` or `datetime.now()` everywhere. This requirement is already satisfied (CLEAN-03 can be marked done immediately).

## 3. Potentially Unused Functions

Requires cross-reference analysis. Key candidates to audit:

### tools/discovery/database.py (2,927 lines — largest module)
This is the central DB module imported by 14+ files. Many of its 30+ public methods may be unused after various refactors. Audit needed:
- Check each public method against all callers
- Focus on methods added in early milestones (v1.0-v1.3) that may have been superseded

### tools/youtube-analytics/patterns.py (2,070 lines)
Large module with many helper functions. Candidate unused functions:
- Internal helper functions that may have been superseded by pattern_extractor.py or pattern_synthesizer_v2.py

### tools/prompt_evaluation.py (945 lines)
Standalone tool not referenced by any slash command or other module. May be entirely unused.

**Recommendation:** Run a targeted import analysis during execution — grep for each public function name across the codebase.

## 4. TODO/FIXME/HACK/DEPRECATED Comments

Only found in `tools/history-clip-tool/` (separate tool, out of scope) and one in `video_processor.py`:
```python
# video_processor.py:148
crop_mode: "center" for center crop, "face" for face tracking (TODO)
```

**No TODOs in the main tools/ Python code.** The codebase is clean in this regard.

## 5. Other Cleanup Candidates

### Backup directory
- `tools/discovery/backups/` — exists as untracked directory, likely contains old database copies

### Test data artifacts
- `tools/youtube-analytics/_longform_*.json` files (4 files, already listed above)
- `tools/youtube-analytics/_backfill_ids.txt` (already listed)

## Summary

| Category | Count | Action |
|----------|-------|--------|
| Dead files to delete | 7 | Immediate |
| datetime.utcnow() fixes | 0 | Already done |
| Potentially unused functions | TBD | Audit during execution |
| TODO/FIXME comments | 0 (in scope) | Clean |
| Backup directories | 1 | Review and delete |
