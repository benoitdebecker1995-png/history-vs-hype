---
description: Retitle underperforming videos — audit, generate candidates, output swap checklist
model: sonnet
---

# /retitle - Retitle Pipeline Entry Point

Orchestrate the full retitle/rethumb pipeline for published videos that got impressions but failed to convert at target CTR. Audits underperformers, generates script-based title candidates, scores them, checks thumbnail compliance, and outputs a copy-paste-friendly SWAP-CHECKLIST.md.

## Usage

```
/retitle                  # Full pipeline: audit → generate → score → SWAP-CHECKLIST.md
/retitle --audit          # Ranked underperformer list only, no candidate generation
/retitle --check [id]     # 7-day post-swap measurement, compare pre/post CTR
/retitle --revert [id]    # Pull old title from SWAP LOG for copy-paste revert
```

## Flags

| Flag | Purpose | Example |
|------|---------|---------|
| (none) | Full retitle pipeline for top 5 | `/retitle` |
| `--audit` | Show ranked underperformers only | `/retitle --audit` |
| `--check` | Measure 7-day post-swap CTR delta | `/retitle --check LrthC_8Hb2Y` |
| `--revert` | Display old title from SWAP LOG | `/retitle --revert LrthC_8Hb2Y` |

---

## CRITICAL INSTRUCTIONS (apply to all modes)

**NEVER suggest titles from generic topic knowledge. ALWAYS read the actual SRT/script and base ALL suggestions on specific content from the video.** This is the channel's competitive advantage — titles must emerge from the actual evidence and thesis, not from the title of a topic.

**Score threshold: 65 minimum. REJECTED grade = hard block.** Show scores for all candidates so the user can compare. A title with score 72 beats a title with score 68 — always sort by score descending.

**SWAP-CHECKLIST.md is ephemeral** — regenerated each run. The SWAP LOG in POST-PUBLISH-ANALYSIS.md is the permanent record (see `/retitle --check`).

**Measurement window:** For retitles of existing videos, use the 7-day measurement window. See `tools/SWAP-PROTOCOL.md` for swap timing guidance, but note the 7-day override for existing published videos (not 48h — older videos need more time for the algorithm to re-test new packaging).

---

## FULL PIPELINE (default `/retitle`)

### Step 1: Load Context

Read `channel-data/patterns/CROSS-VIDEO-SYNTHESIS.md` to understand the current performance landscape. Use as internal context — do NOT dump the full file to the user.

### Step 2: Audit Underperformers

```python
import sys
sys.path.insert(0, '.')
from tools.retitle_audit import audit, format_report

results = audit(min_impressions=500, top_n=5)
```

### Step 3: Apply Retention Weighting

Re-sort results by priority score to surface content-quality wins trapped by bad packaging:

```python
def retention_bonus(ret):
    if ret is None: return 0
    if ret >= 35: return 0.5
    if ret >= 25: return 0.25
    return 0

results.sort(key=lambda r: -(r['wasted_impressions'] * (1 + retention_bonus(r.get('retention')))))
```

**Rationale:** A video with 50.5% retention and 1.83% CTR is a pure packaging failure — fixing the title will convert. A video with 13% retention and 1.11% CTR has dual issues (packaging AND content) — a title fix won't hold viewers. Retention-weighting prioritizes the former.

**Exclusion rule:** Videos with retention < 15% should be noted as "HIGH RISK — content issues likely" in the checklist, but still included if wasted impressions are high enough.

### Step 4: Generate Title Candidates Per Video

For each of the top 5 videos:

**a. Script-based generation (primary):**

```python
from tools.retitle_gen import generate_script_titles, CANDIDATES, VIDEO_PROJECT_MAP

script_titles = generate_script_titles(video_id, current_title)
```

**b. Fallback chain (if script_titles is empty):**
1. First fallback: `CANDIDATES` dict in `retitle_gen.py` — check `CANDIDATES.get(video_id, {}).get('options', [])`
2. Second fallback: Read `channel-data/RETITLE-RECOMMENDATIONS.md` and extract options for the video

**Always surface which source was used** per video so the user knows whether titles are script-derived or pre-generated.

**c. Score all candidates:**

```python
from tools.title_scorer import score_title

# Deduplicate, preserve order
all_options = list(dict.fromkeys(script_titles + manual_options))

scored = [(t, score_title(t)) for t in all_options]
scored.sort(key=lambda x: -x[1]['score'])

# Filter: block REJECTED grade and score < 65
valid = [(t, s) for t, s in scored if s['grade'] != 'REJECTED' and s['score'] >= 65]
```

If no candidates pass the threshold, note "NO VALID CANDIDATES — all options scored below 65 or REJECTED" and show the highest-scoring blocked option with its rejection reason so the user understands why.

### Step 5: Thumbnail Compliance Check

**If VIDEO_PROJECT_MAP[video_id] is not None** (project folder exists):

```python
from tools.preflight.thumbnail_checker import check_project
import os

project_folder = f"video-projects/_IN_PRODUCTION/{VIDEO_PROJECT_MAP[video_id]}"
if os.path.exists(project_folder):
    result = check_project(project_folder)
    # result: {score, verdict, issues, passes}
```

**If no project folder** or no YOUTUBE-METADATA.md found: note "THUMBNAIL: Manual check required — no metadata file found."

**Auto-suggest thumbnail map type** based on content signals in the current title and diagnosis:

| Content Signal | Map Type | When to Apply |
|----------------|----------|---------------|
| Two actors / conflict / "vs" in title | split-map | Turkey vs Greece, Israel vs Palestine |
| Movement / extraction verbs (expelled, extracted, drained, escaped) | arrow-flow | Chagos Islands expulsion, border movement |
| Legal document / treaty as central evidence | document-on-map | Gibraltar Treaty, Statute of Jews |
| Multiple claimants (3+ countries named) | labeled-zone | South China Sea, multiple colonial zones |
| Default / fallback | split-map | Clean, high-contrast, most reliable format |

**Note on checker false positives:** `thumbnail_checker` may flag "no face shown" descriptions as FACE_SIGNALS hit. If the concept is clearly compliant (no face, map-based, no text), override the flag and note it in the checklist.

### Step 6: Generate SWAP-CHECKLIST.md

Write to `channel-data/SWAP-CHECKLIST.md` (overwrite each run — this file is ephemeral):

```markdown
# SWAP CHECKLIST — [today's date]

**Generated:** [today's date] | **Batch size:** 5 | **Measure at:** [today + 7 days]

> **Instructions:** Open this file in one window, YouTube Studio in another.
> Change all 5 titles on the same day for a clean 7-day comparison window.

---

## Video 1: [short title slug]

**Video ID:** `[video_id]`
**Studio link:** https://studio.youtube.com/video/[video_id]/edit
**Priority score:** [wasted_impressions × retention_multiplier] | **Diagnosis:** [from audit]

### OLD TITLE (copy to revert)
[Current title verbatim — exact copy for one-click revert]

### NEW TITLE
[Best candidate — score [XX]/100, grade [X], pattern: [pattern_name]]

### Title Source
[script-generated | CANDIDATES dict | RETITLE-RECOMMENDATIONS.md]

### All Scored Candidates
| Score | Grade | Title |
|-------|-------|-------|
| XX | A | [title] |
| XX | B | [title] |
| XX | REJECTED | [title] — [rejection_reason] |

### NEW DESCRIPTION (first 3 lines only — replace existing opening)
[Line 1: Primary keyword + video format, reframed for new title]
[Line 2: Specific event/topic, reframed]
[Line 3: Method/sources used]

### THUMBNAIL
**Status:** [SWAP NEEDED | COMPLIANT — TITLE ONLY | MANUAL CHECK REQUIRED]
**Type:** [split-map | arrow-flow | document-on-map | labeled-zone]
**Concept:** [2-3 sentence description for Photoshop — what to show, layout, text if any]
**Color scheme:** [e.g., warm gold left panel, cold grey right panel, red overlays for disputed zones]
**Checker result:** [PASS | REVIEW | FAIL — issues listed]

### PRE-SWAP METRICS (for comparison at 7-day check)
- CTR: [X.XX]% | Impressions: [N] | Retention: [X.X]% | Views: [N]

---

[Repeat for videos 2-5]

## Post-Swap Checklist

- [ ] All 5 titles changed in YouTube Studio
- [ ] All thumbnails updated (or confirmed compliant)
- [ ] SWAP LOG added to each POST-PUBLISH-ANALYSIS.md (template below)
- [ ] Calendar reminder set: **[today + 7 days]** — run `/retitle --check [id]` for each video

### SWAP LOG Entry Template (paste into each POST-PUBLISH-ANALYSIS.md)

```
## SWAP LOG

| Date | Type | Old Value | New Value | Pre-CTR | Post-CTR | Result |
|------|------|-----------|-----------|---------|---------|--------|
| [today] | title | "[old title]" | "[new title]" | [X.XX]% | TBD | pending |
```
```

### Step 7: Print Summary Table

After generating SWAP-CHECKLIST.md, display a summary to the user:

```
--- SWAP CHECKLIST READY ---
Saved: channel-data/SWAP-CHECKLIST.md
Measure date: [today + 7 days]

| # | Video | Old CTR | New Title (score) | Thumbnail |
|---|-------|---------|-------------------|-----------|
| 1 | [slug] | X.XX% | [title] (XX) | SWAP / COMPLIANT |
| 2 | [slug] | X.XX% | [title] (XX) | SWAP / COMPLIANT |
...

Run `/retitle --check [id]` for each video on the measurement date.
```

---

## AUDIT ONLY (`--audit`)

Run the audit without generating candidates or SWAP-CHECKLIST.

```python
import sys
sys.path.insert(0, '.')
from tools.retitle_audit import audit, format_report

results = audit(min_impressions=500, top_n=10)
```

Apply the same retention-weighting sort as the full pipeline.

Display the `format_report()` output verbatim, then append a **Retention-Weighted Priority** column to help the user understand re-ordering:

```
--- Retention-Weighted Priority ---
#1: [video title] — priority score [X] (wasted: [N] × bonus: [1.5x | 1.25x | 1.0x])
#2: [video title] — priority score [X]
...

Run `/retitle` (no flag) to generate title candidates and SWAP-CHECKLIST for the top 5.
```

Do NOT generate candidates or create any files.

---

## POST-SWAP MEASUREMENT (`--check [video-id]`)

### Step 1: Verify Measurement Window

Read `channel-data/analyses/POST-PUBLISH-ANALYSIS-[video_id].md`. Find the SWAP LOG section. Check the swap date.

If swap was < 7 days ago:
```
Swap was [N] days ago ([swap date]).
Check back on [swap_date + 7 days] for reliable data — older videos need 7 days for algorithm re-testing.
```

Stop. Do not proceed.

### Step 2: Collect Post-Swap CTR

Ask the user: "What CTR is showing in YouTube Studio for [video title] right now?"

(User opens YouTube Studio > Content > click video > Analytics > Impressions click-through rate)

### Step 3: Evaluate Result

```
Pre-swap CTR:  [X.XX]%
Post-swap CTR: [user-provided]%
Delta:         [+/- X.XX]%
```

**Success threshold:** +0.5% CTR or more.

**If SUCCESS (+0.5% or more):**
1. Update SWAP LOG in POST-PUBLISH-ANALYSIS.md: change `TBD` → `[post_ctr]%` and `pending` → `+[delta]% SUCCESS`
2. Update the video's CTR in `channel-data/patterns/CROSS-VIDEO-SYNTHESIS.md`
3. Run CTR feedback ingestion:
   ```python
   from tools.ctr_ingest import ingest_synthesis_ctr
   from tools.discovery.database import KeywordDB
   from pathlib import Path
   result = ingest_synthesis_ctr(Path('channel-data/patterns/CROSS-VIDEO-SYNTHESIS.md'), KeywordDB())
   print(f"CTR data ingested: {result['written']} written, {result['skipped']} skipped")
   ```
4. Report: "SUCCESS — CTR improved +[delta]%. Title swap data ingested for future scoring calibration."

**If FLAT or NEGATIVE (< +0.5%):**
1. Update SWAP LOG: change `pending` → `flat REVERTED` (or `[delta]% REVERTED`)
2. Show old title for immediate copy-paste:
   ```
   REVERT NOW — copy this title back into YouTube Studio:
   [old title verbatim]
   ```
3. Report: "No significant CTR improvement. Reverted. No second-chance candidates — reassess in next batch."

---

## REVERT (`--revert [video-id]`)

1. Read `channel-data/analyses/POST-PUBLISH-ANALYSIS-[video_id].md`
2. Find the most recent SWAP LOG entry for this video
3. Display old title for immediate copy-paste:

```
--- REVERT TITLE ---
Video: [video title]
Video ID: [id]
Studio link: https://studio.youtube.com/video/[id]/edit

OLD TITLE (copy this):
[old title verbatim]

After reverting in YouTube Studio, confirm here and I'll update the SWAP LOG status.
```

4. After user confirms revert: update SWAP LOG status to `reverted` with today's date

---

## Reference Files

- **Audit tool:** `tools/retitle_audit.py` — `audit()`, `format_report()`
- **Generation tool:** `tools/retitle_gen.py` — `generate_script_titles()`, `CANDIDATES`, `VIDEO_PROJECT_MAP`
- **Title scorer:** `tools/title_scorer.py` — `score_title()`
- **Thumbnail checker:** `tools/preflight/thumbnail_checker.py` — `check_thumbnail()`, `check_project()`
- **CTR ingestion:** `tools/ctr_ingest.py` — `ingest_synthesis_ctr()`
- **Swap protocol:** `tools/SWAP-PROTOCOL.md` — timing and rollback guidance
- **Retitle recommendations:** `channel-data/RETITLE-RECOMMENDATIONS.md` — fallback candidate pool
- **Performance data:** `channel-data/patterns/CROSS-VIDEO-SYNTHESIS.md` — master CTR/impressions table

---

## Integration with Production Workflow

```
[Monthly or when CTR data shows low performers]
/retitle --audit            # Review underperformers, understand the landscape
/retitle                    # Generate SWAP-CHECKLIST for top 5

[Swap day — do all 5 on same day]
[Open YouTube Studio, change titles + thumbnails per checklist]
[Add SWAP LOG section to each POST-PUBLISH-ANALYSIS.md]
[Set calendar reminder for 7 days]

[7 days later]
/retitle --check [id-1]     # Evaluate each video
/retitle --check [id-2]
...                         # Successful swaps auto-ingest CTR data for Phase 61 feedback loop
```
