---
description: Pre-flight scorecard — evaluate a video project before filming/publishing
model: sonnet
---

# /preflight - Pre-Flight Scorer

Run a pre-flight scorecard on a video project to predict performance and catch problems before filming or publishing.

## Usage

```
/preflight                     # Auto-detect current project
/preflight [project-slug]      # Score a specific project
/preflight --gate topic        # Show only one gate's details
/preflight --compare A B       # Compare two projects side by side
```

## Flags

| Flag | Purpose | Example |
|------|---------|---------|
| (none) | Full scorecard | `/preflight 40-berlin-conference-1884-2026` |
| `--gate` | Zoom into one gate | `/preflight --gate script` |
| `--compare` | Compare two projects | `/preflight --compare 37-untranslated 40-berlin` |

---

## Step 1: Locate the Project

If user provides a slug, find the matching folder:

```python
from pathlib import Path
import glob

# Try matching the slug against _IN_PRODUCTION folders
slug = args or ""
matches = glob.glob(f"video-projects/_IN_PRODUCTION/*{slug}*")
if not matches:
    matches = glob.glob(f"video-projects/_READY_TO_FILM/*{slug}*")
if not matches:
    # Ask user
    pass
project_path = matches[0]
```

If no argument given and user is discussing a specific project in context, use that project.

## Step 2: Run the Scorer

```python
from tools.preflight.scorer import run_preflight
from tools.preflight.formatter import format_preflight_report

result = run_preflight(project_path)
report = format_preflight_report(result)
```

Display the full formatted report to the user.

## Step 3: Suggest Fixes

For any gate scoring below 70, provide **specific, actionable suggestions**:

### Topic gate < 70
- Suggest title reformulations that lean into higher-performing topic types
- Reference channel DNA: territorial + legal outperform general topics

### Script gate < 70
- If pacing FAIL: identify which sections drag and suggest cuts or pattern interrupts
- If low evidence density: suggest adding `[DOCUMENT]`, quote, or `[MAP]` markers
- If stumble issues: list the long sentences and suggest splits
- If no pull question: suggest a question to add in the hook
- **Run retention predictor** for content-type placement insights:
  ```python
  from tools.youtube_analytics.retention_predictor import predict_from_file
  result = predict_from_file(script_path)
  # Shows predicted retention curve + flagged drop-risk sections
  ```

### Title gate < 70
- If title too long/short: suggest trimmed or expanded variants
- If low tag count: suggest additional relevant tags
- If description too short: note what sections to add
- **Run outlier title dissector** for proven niche patterns:
  ```python
  result = subprocess.run(
      ['python', '-m', 'tools.benchmark.outlier_title_dissector', '--score', best_title],
      capture_output=True, text=True
  )
  # Shows scale word lift, two_sentence formula, entity specificity scores
  ```

### Duration gate < 70
- If too short: note which sections could expand with more evidence
- If too long: suggest sections to tighten (check thesis advancement)
- If low B-roll: suggest where to add visual markers

## Step 4: Offer Next Steps

After displaying the report, offer:

```
What next?
A) Fix flagged issues (I'll suggest specific rewrites)
B) Run full script review (/script-reviewer)
C) Generate metadata (/publish --metadata)
D) Compare with another project (/preflight --compare)
```

## --gate Flag

When `--gate` is specified, show only that gate's full details plus its sub-scores and specific issues. Skip the other gates.

## --compare Flag

When `--compare` is specified with two project slugs:
1. Run `run_preflight()` on both
2. Display a side-by-side table:

```
| Gate          | Project A | Project B |
|---------------|-----------|-----------|
| Topic         | 82        | 65        |
| Script        | 71        | 78        |
| Title         | 85        | 60        |
| Duration      | 95        | 70        |
| **Composite** | **78 (B)**| **68 (C)**|
```

3. Highlight which project is stronger and why

## Graceful Degradation

If any dependency is unavailable (spaCy, intel.db, YouTube API), the scorer returns neutral scores (50) with notes. Always display whatever data is available — partial scorecards are still useful.
