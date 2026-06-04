---
description: Full pre-upload scorecard — 5 script-stage gates + conditional rendered-asset QC (topic/script/title/thumb/duration + image + audio)
model: opus
---

# /preflight — Pre-Upload Scorecard

One command, two layers:

1. **Script-stage readiness** — the existing 5-gate engine (`tools/preflight/scorer.py`): topic, script, title/metadata, thumbnail-concept, duration → weighted composite + READY/REVIEW/NOT-READY verdict. This is meaningful from the moment a script + metadata exist.
2. **Render QC** (conditional) — runs **only** when the rendered assets exist: the exported thumbnail image (`thumbnail_image_audit.py`) and the final cut audio (`audio_loudness.py`). These are NOT folded into the composite (they don't exist at script stage and would dilute it) — they're a separate pass/fail block that hard-blocks upload on a thumbnail that blends in.

Use it twice in a project's life: at script-lock (layer 1 only) and pre-upload (both layers).

## Usage

```
/preflight                          # Auto-detect active _IN_PRODUCTION / _READY_TO_FILM project
/preflight [project-folder]         # Explicit project
/preflight [project] --serp-ids a,b,c   # Supply competitor video IDs for thumbnail differentiation
/preflight [project] --save         # Also write PREFLIGHT-SCORECARD.md to the project folder
```

## Flags

| Flag | Purpose |
|------|---------|
| *(default)* | Auto-detect single in-production/ready project. If multiple, list and ask. |
| `[project-folder]` | Use a specific project folder. |
| `--serp-ids a,b,c` | Competitor YouTube video IDs for the thumbnail SERP-differentiation check. If omitted, the command tries `_research/comment-mining/*.info.json`; if none, it runs the image audit *without* differentiation and notes it. |
| `--save` | Append the full report to `[project]/PREFLIGHT-SCORECARD.md`. Default: chat only. |
| `--no-render` | Skip layer 2 even if assets exist (script-stage check only). |

---

## Procedure

### Step 1 — Resolve project

Auto-detect: Glob `video-projects/_IN_PRODUCTION/*/` and `video-projects/_READY_TO_FILM/*/`. Exactly one → use it. Multiple → list with working titles, ask. Zero → tell the user to run `/research --new` first. Explicit `[project-folder]` → Glob for a folder ending with that name across both lifecycle dirs.

### Step 2 — Layer 1: script-stage scorecard

Run the engine and render it:

```python
import sys; sys.path.insert(0, '.')
from tools.preflight.scorer import run_preflight
from tools.preflight.formatter import format_preflight_report
result = run_preflight("<project_path>")
print(format_preflight_report(result))
```

Display the rendered report verbatim. Every gate degrades gracefully (missing data → neutral 50 + note, never an exception), so this never hard-fails. Note the composite verdict: **READY (≥70) / REVIEW (50–69) / NOT READY (<50)**.

### Step 3 — Layer 2: Render QC (conditional)

Skip entirely if `--no-render`, or if neither asset exists. Otherwise:

**3a. Locate assets.** Glob the project folder for:
- Rendered thumbnail: `*.png` / `*.jpg` NOT under `_research/` (prefer a file whose name contains `thumb`).
- Final cut: `*.mp4` (prefer one named `final` / `rough-cut` if multiple; note which you picked).

If neither exists, print `Render QC: deferred — no exported thumbnail or final cut found.` and go to Step 4.

**3b. Resolve competitor IDs for the thumbnail check.** Priority:
1. `--serp-ids` if passed.
2. Else parse `_research/comment-mining/*.info.json` for the top 3–5 `id` values by `view_count` (one-liner already used by `/thumbnail` Step 2.5).
3. Else: run the image audit without `--serp-ids` and note "differentiation skipped — no competitor IDs."

**3c. Run the checks** (only for assets that exist):

```bash
python -m tools.preflight.thumbnail_image_audit "<thumb>" --serp-ids <ids>
python -m tools.preflight.audio_loudness "<final-cut.mp4>"
```

**3d. Interpret:**

| Check | BLOCK (hard) | FLAG (advisory) | PASS |
|---|---|---|---|
| Thumbnail differentiation | `BLENDS IN` (>0.70) | `TYPICAL` (0.55–0.70) | `STRONG` (<0.55) |
| Thumbnail tech | res < 1280×720, or file > 2MB | low contrast | compliant |
| Audio | — | outside −16…−12 LUFS, or peak > −1 dBTP | in band |

- If `open_clip_torch` missing, the image audit falls back to a histogram proxy (flagged, directional) — report it as such, don't treat as authoritative.
- If ffmpeg missing, audio returns `MISSING` — surface `winget install Gyan.FFmpeg`, do NOT block.

### Step 4 — Combined verdict

Print one consolidated verdict line:

- **UPLOAD-READY** — composite ≥ 70 AND no Render-QC BLOCK.
- **REVIEW** — composite 50–69, OR any Render-QC FLAG with no BLOCK.
- **NOT READY** — composite < 50, OR any Render-QC BLOCK (e.g., thumbnail BLENDS IN, sub-spec resolution).

A thumbnail `BLENDS IN` or sub-spec resolution overrides a passing composite to NOT READY — a strong script behind an invisible thumbnail still doesn't get the click.

### Step 5 — Save (if `--save`)

Write the layer-1 report + the Render-QC block + the combined verdict to `[project]/PREFLIGHT-SCORECARD.md` with a dated header. Don't overwrite blindly — if the file exists, append a new dated run section.

---

## Failure modes

| Case | Behavior |
|------|----------|
| No script / no metadata | Layer 1 still runs; the affected gate scores 0 and flags it. Surface as NOT READY. |
| Project ambiguous | List candidates, ask once. |
| Image audit errors (corrupt file) | Report the error for that check, continue with the rest. Don't abort the whole scorecard. |
| ffmpeg / open_clip missing | Degrade per Step 3d. Never hard-fail the command on a missing optional dep. |

---

## Integration

- **`/publish` Gate 3** runs the same two rendered-asset checks at metadata time. `/preflight` is the broader scorecard that *also* covers script/title/duration — run it for a single go/no-go; `/publish` for metadata authoring.
- **`/thumbnail`** generates concepts (pre-render); `/preflight` audits the exported result.
- **`/editing-guide` Diff D** is the earliest audio catch; `/preflight` is the pre-upload backstop.
- Engine: `tools/preflight/scorer.py` + `formatter.py`. Rendered checks: `tools/preflight/thumbnail_image_audit.py` + `audio_loudness.py`. Deps: `tools/preflight/requirements.txt`.
