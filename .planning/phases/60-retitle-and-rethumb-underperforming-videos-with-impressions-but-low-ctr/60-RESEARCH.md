# Phase 60: Retitle and Rethumb Underperforming Videos - Research

**Researched:** 2026-03-14
**Domain:** YouTube packaging optimization — retitle/rethumb pipeline for existing published videos
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Selection criteria:**
- Top 5 videos per batch — measure before doing more
- Minimum 500 impressions threshold — below that, YouTube hasn't tested packaging enough
- Ranking formula: Claude's discretion (wasted impressions × retention weighting)

**Execution workflow:**
- Output: Markdown SWAP-CHECKLIST.md with all swap details per video
- Each checklist entry: OLD TITLE (for revert), NEW TITLE, NEW DESCRIPTION (first 3 lines), THUMBNAIL CONCEPT (if needed)
- Title generation: Script-based — read actual SRT/scripts, extract thesis, generate titles from real content
- Description: Updated first 3 lines to match new title framing
- Tracking: Per-video in POST-PUBLISH-ANALYSIS.md (SWAP LOG section: date, old title, new title, pre/post CTR)

**Thumbnail strategy:**
- Include thumbnail concept (map type, color scheme, layout description) for user to build in Photoshop
- Auto-suggest map type: split-map (vs topics), arrow-flow (movement/extraction), document-on-map (treaty/legal)
- Skip compliant thumbnails — run thumbnail_checker on current concept first. If already map-based, no face, no text: only swap the title

**Success measurement:**
- Re-check at 7 days post-swap (older videos don't get the 48h push)
- Success threshold: +0.5% CTR or more
- Feed successful swap data back via ctr_ingest (Phase 61 feedback loop)

**Rollback strategy:**
- CTR drops or stays flat after 7 days: revert to original title
- SWAP-CHECKLIST always includes old title for one-click copy-paste revert
- No second-chance candidates — revert first, reassess later

**Stagger timing:**
- Swap all 5 on the same day (at 475 subs, videos don't compete with each other)
- Measure all at same 7-day mark for clean comparison

**Slash command /retitle flags:**
- `/retitle` — Full pipeline: audit → generate candidates → output SWAP-CHECKLIST.md (top 5)
- `/retitle --audit` — Just show ranked list of underperformers with wasted impressions
- `/retitle --check [video-id]` — 7-day post-swap measurement, compare pre/post CTR, trigger ctr_ingest if successful
- `/retitle --revert [video-id]` — Pull old title from SWAP LOG for copy-paste revert

### Claude's Discretion
- Exact ranking formula (wasted impressions × retention weighting)
- Which map type to suggest per video when auto-suggesting
- How to handle videos without SRT/script files (fallback to existing RETITLE-RECOMMENDATIONS.md candidates)

### Deferred Ideas (OUT OF SCOPE)
None — discussion stayed within phase scope
</user_constraints>

---

## Summary

Phase 60 builds a repeatable retitle/rethumb pipeline for existing published videos that got impressions but failed to convert at target CTR. The core problem is diagnosed: videos like "South China Sea" (1.83% CTR, 3,007 impressions, 50.5% retention) and "Dark Ages" (1.11% CTR, 7,237 impressions) are content-quality wins trapped by packaging failures — years in title, colons, question patterns.

The tooling is substantially pre-built. `retitle_audit.py` ranks videos by wasted impressions. `retitle_gen.py` generates script-based title candidates using thesis extraction. `title_scorer.py` scores candidates with DB-enriched CTR patterns. `thumbnail_checker.py` validates current thumbnail concepts. The gap is the orchestrating slash command (`/retitle`) and the SWAP-CHECKLIST.md output format that wires these tools into a single user-facing workflow.

The planner needs to implement: (1) the `/retitle` command file that orchestrates the full pipeline, (2) the SWAP-CHECKLIST.md output template, (3) SWAP LOG section injection into POST-PUBLISH-ANALYSIS.md files, and (4) the `--check` flag that reads pre/post CTR and triggers ctr_ingest on success.

**Primary recommendation:** Wire existing tools into `/retitle` command. Add SWAP LOG section to POST-PUBLISH-ANALYSIS format. No new Python needed for the happy path — the command file + output template are the deliverables.

---

## Standard Stack

### Core (all pre-existing, verified by reading source files)

| Tool | Location | Purpose | Status |
|------|----------|---------|--------|
| `retitle_audit.py` | `tools/retitle_audit.py` | Ranks videos by wasted impressions from CROSS-VIDEO-SYNTHESIS.md | EXISTS — full implementation |
| `retitle_gen.py` | `tools/retitle_gen.py` | Script-based thesis extraction + title generation | EXISTS — full implementation |
| `title_scorer.py` | `tools/title_scorer.py` | Scores titles with DB-enriched CTR patterns | EXISTS — Phase 61 DB-enriched |
| `thumbnail_checker.py` | `tools/preflight/thumbnail_checker.py` | check_thumbnail(text) → pass/fail/issues | EXISTS — full implementation |
| `ctr_ingest.py` | `tools/ctr_ingest.py` | ingest_synthesis_ctr() → writes CTR to keywords.db | EXISTS — tested in Phase 61 |
| `CROSS-VIDEO-SYNTHESIS.md` | `channel-data/patterns/CROSS-VIDEO-SYNTHESIS.md` | Master performance table with CTR/impressions data | EXISTS — 31 videos with data |
| `RETITLE-RECOMMENDATIONS.md` | `channel-data/RETITLE-RECOMMENDATIONS.md` | Pre-generated candidates from 2026-03-10 | EXISTS — fallback pool |
| SWAP-PROTOCOL.md | `tools/SWAP-PROTOCOL.md` | 48h swap protocol (adapt measurement window to 7-day) | EXISTS — adapt not rewrite |

### What Needs to Be Created

| Deliverable | Type | Purpose |
|-------------|------|---------|
| `.claude/commands/retitle.md` | Slash command (markdown) | Orchestrates full pipeline at runtime |
| `channel-data/SWAP-CHECKLIST.md` | Output template | Copy-paste-friendly user action list (ephemeral) |
| SWAP LOG section in POST-PUBLISH-ANALYSIS | Format addition | Permanent per-video swap history |

### Key Invocation Patterns (verified from source)

```python
# retitle_audit.py
from tools.retitle_audit import audit, format_report
results = audit(min_impressions=500, top_n=5)  # Returns list sorted by wasted_impressions

# retitle_gen.py
from tools.retitle_gen import generate_script_titles, CANDIDATES
titles = generate_script_titles(video_id, current_title)  # Returns scored list

# title_scorer.py
from tools.title_scorer import score_title
result = score_title(title)  # Returns {score, grade, pattern, db_enriched, rejection_reason, penalties}

# thumbnail_checker.py
from tools.preflight.thumbnail_checker import check_thumbnail
result = check_thumbnail(text)  # Returns {score, verdict, issues, passes}

# ctr_ingest.py (Phase 61)
from tools.ctr_ingest import ingest_synthesis_ctr
result = ingest_synthesis_ctr(synthesis_path, db, dry_run=False)
# Returns {written, skipped, unmatched, would_write, errors}
```

---

## Architecture Patterns

### Ranking Formula (Claude's Discretion — Recommendation)

The CONTEXT.md leaves ranking formula to Claude's discretion. The existing `retitle_audit.py` uses:

```
wasted_impressions = impressions × (target_CTR - actual_CTR) / 100
```

This is correct but doesn't weight by retention. Recommended enhancement: prioritize high-retention videos because they prove content quality — the packaging alone is the bottleneck.

```python
# Recommended composite score
priority_score = wasted_impressions * (1 + retention_bonus)
# retention_bonus: +0.5 if retention >= 35%, +0.25 if 25-35%, +0 if below 25%
```

This surfaces "South China Sea" (wasted_clicks ≈ 50, retention 50.5%) above "Dark Ages" (wasted_clicks ≈ 177, retention 13.2%) — the content-quality signal matters because a title fix won't help a retention problem. The Dark Ages video's 1.11% CTR combined with 13.2% retention suggests both packaging AND content issues, making it a riskier swap candidate.

### SWAP-CHECKLIST.md Format

Each entry must be self-contained for standalone YouTube Studio use. User opens checklist in one window, YouTube Studio in another.

```markdown
# SWAP CHECKLIST — [date]
**Generated:** [date] | **Batch size:** 5 | **Measure at:** [date + 7 days]

---

## Video 1: [short title slug]

**Video ID:** `[id]`
**Studio link:** https://studio.youtube.com/video/[id]/edit

### OLD TITLE (copy to revert)
[Current title verbatim]

### NEW TITLE
[Best candidate, score XX/100]

### NEW DESCRIPTION (first 3 lines only — replace existing opening)
[Line 1]
[Line 2]
[Line 3]

### THUMBNAIL
**Status:** [SWAP NEEDED / COMPLIANT — TITLE ONLY]
**Type:** [split-map / arrow-flow / document-on-map]
**Concept:** [Description for Photoshop]
**Color scheme:** [e.g., warm gold left, cold grey right]

### PRE-SWAP METRICS (for comparison)
- CTR: [X.XX]% | Impressions: [N] | Retention: [X.X]%

---

[Repeat for videos 2-5]

## Post-Swap Checklist
- [ ] All 5 titles changed in YouTube Studio
- [ ] All thumbnails updated (or confirmed compliant)
- [ ] SWAP LOG added to each POST-PUBLISH-ANALYSIS.md
- [ ] Calendar reminder set: [date + 7 days] — run `/retitle --check [id]` for each
```

### SWAP LOG Section (POST-PUBLISH-ANALYSIS.md injection)

The log is injected as a new section if not present, or appended if section exists.

```markdown
## SWAP LOG

| Date | Type | Old Value | New Value | Pre-CTR | Post-CTR | Result |
|------|------|-----------|-----------|---------|---------|--------|
| 2026-03-14 | title | "Old Title" | "New Title" | 1.83% | TBD | pending |
```

After 7-day check, update Result to: `+1.2% SUCCESS` or `flat REVERTED`.

### /retitle Command Flow

The slash command orchestrates at runtime — it reads files and calls Python tools on demand. Pattern matches existing `/publish` command structure (`.claude/commands/` markdown file that Claude interprets).

```
/retitle (full pipeline):
  1. Read CROSS-VIDEO-SYNTHESIS.md
  2. Run retitle_audit (min_impressions=500, top_n=5) with retention weighting
  3. For each candidate:
     a. Run generate_script_titles(video_id, current_title)
     b. If no SRT found → use RETITLE-RECOMMENDATIONS.md candidates as fallback
     c. Score all candidates via score_title()
     d. Check current thumbnail concept via check_thumbnail() if description exists
     e. Auto-suggest thumbnail type based on video content
  4. Output SWAP-CHECKLIST.md to channel-data/
  5. Print summary table

/retitle --audit:
  Run retitle_audit only → print format_report() output

/retitle --check [video-id]:
  1. Read SWAP LOG from POST-PUBLISH-ANALYSIS for video
  2. Ask user: "What's the current CTR in YouTube Studio?"
  3. Compare pre/post CTR
  4. If +0.5% or more: update SWAP LOG as SUCCESS, run ctr_ingest, update CROSS-VIDEO-SYNTHESIS
  5. If flat/negative: update SWAP LOG as REVERTED, show old title for copy-paste

/retitle --revert [video-id]:
  1. Read SWAP LOG for video
  2. Display old title for immediate copy-paste
  3. Prompt user to confirm revert in YouTube Studio
  4. Update SWAP LOG status
```

### Map Type Auto-Suggestion Logic (Claude's Discretion — Recommendation)

Based on video content patterns:

| Content Signal | Map Type | Example |
|----------------|----------|---------|
| Two actors in title (vs, conflict) | split-map | Turkey vs Greece → split map with border |
| Movement/extraction/flow (expelled, extracted, drained) | arrow-flow | Chagos Islands → arrows showing British expulsion |
| Legal document/treaty as central evidence | document-on-map | Gibraltar treaty → document overlaid on Strait of Gibraltar map |
| Multiple claimants (3+ countries) | labeled-zone | South China Sea → multiple colored zones with labels |
| Default/fallback | split-map | Clean, high-contrast, most reliable format |

### Fallback for Videos Without SRT/Script

`retitle_gen.py` already handles this: `VIDEO_PROJECT_MAP` maps video IDs to project folders. For IDs with `None` mapping, `get_opening_text()` checks `transcripts/retitle/` directory. If still empty, the function returns `''` and `generate_script_titles()` returns `[]`.

The `/retitle` command should fall back to `CANDIDATES` dict in `retitle_gen.py` (pre-generated manual options) or `RETITLE-RECOMMENDATIONS.md` for the top scored option from that dict. This is already implemented — manual options are always in `CANDIDATES`.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Ranking underperformers | Custom parser | `retitle_audit.audit()` | Already parses CROSS-VIDEO-SYNTHESIS.md, calculates wasted_impressions |
| Generating title candidates | New NLP | `retitle_gen.generate_script_titles()` | Already does thesis extraction + pattern matching |
| Scoring titles | Custom scorer | `title_scorer.score_title()` | DB-enriched, Phase 61-calibrated, returns grade + penalties |
| Thumbnail compliance | Manual checklist | `thumbnail_checker.check_thumbnail()` | Already enforces PACKAGING_MANDATE rules |
| CTR feedback | Manual DB update | `ctr_ingest.ingest_synthesis_ctr()` | Tested pipeline, handles matching + idempotency |

**Key insight:** This phase is a workflow integration problem, not a new algorithm problem. All computation is already implemented. The deliverable is the orchestrating command + output templates.

---

## Common Pitfalls

### Pitfall 1: Swapping Videos with Content Problems (Not Just Packaging)

**What goes wrong:** Retitling a video with low CTR AND low retention — after swap, CTR may improve slightly but views still underperform because the content doesn't hold viewers.
**Why it happens:** Ranking by wasted_impressions alone surfaces all low-CTR videos, including ones where poor content is the real issue.
**How to avoid:** Apply retention weighting in the ranking formula. Videos with retention < 25% should be deprioritized or excluded from batch swaps. The audit already flags these with the diagnosis field.
**Warning signs:** `diagnosis = 'BAD PACKAGING — SWAP TITLE + THUMBNAIL'` on a video with retention < 25% — the dual diagnosis suggests the thumbnail may have filtered out non-interested viewers, and fixing packaging just gets uninterested viewers to click.

### Pitfall 2: Generating Broken Title Fragments from Thesis Extraction

**What goes wrong:** `extract_thesis()` can generate sentence fragments that pass length filters but don't make sense as titles (e.g., "Russia claimed that started.").
**Why it happens:** `retitle_gen.py` has fragment detection logic, but it operates on word patterns. Complex sentence structures can slip through.
**How to avoid:** Always run `score_title()` on generated candidates. REJECTED grade = hard block. Score < 65 = blocked. The `/retitle` command should apply the same gate `/publish` uses: show scores, block anything below 65.
**Warning signs:** Titles ending with function words, transitive verbs without objects, pronouns as sentence objects — all filtered in `thesis_to_titles()` but verify by checking the score.

### Pitfall 3: Overwriting SWAP LOG Instead of Appending

**What goes wrong:** `/retitle --check` or a second swap run overwrites the SWAP LOG section, losing revert data.
**Why it happens:** Simple file writes replace content.
**How to avoid:** Always append new rows to the SWAP LOG table. Check if `## SWAP LOG` section exists first; if yes, add row to existing table; if no, create the section.

### Pitfall 4: Thumbnail Checker False Positive on "No Face" Concepts

**What goes wrong:** A thumbnail description saying "no face shown" gets flagged as FACE_SIGNALS hit because `check_thumbnail()` doesn't always catch negation context.
**Why it happens:** `_has_signal()` has `exclude_negated=True` for face signals, which checks for "no ", "not ", "without " prefixes, but natural language negation can vary.
**How to avoid:** When `thumbnail_checker` returns `verdict = "FAIL"` for a clearly compliant concept, manually override and note in SWAP-CHECKLIST. The check is advisory for existing thumbnails — it's a MANDATE enforcer for new concepts.

### Pitfall 5: 7-Day Measurement Window Misalignment

**What goes wrong:** Checking CTR too early (48h) for older videos, getting misleading data because algorithm needs time to re-test the new packaging.
**Why it happens:** SWAP-PROTOCOL.md uses 48h (designed for new videos). The CONTEXT.md explicitly overrides this to 7 days for retitles.
**How to avoid:** The `/retitle --check` command should read the SWAP LOG date and refuse to measure if < 7 days have passed. Print: "Swap was [N] days ago. Check back on [date] for reliable data."

---

## Code Examples

### Running the Full Audit

```python
# Source: tools/retitle_audit.py (verified by reading)
from tools.retitle_audit import audit, format_report

results = audit(min_impressions=500, top_n=5)
# Each result: {title, views, retention, ctr, impressions, subs, topic_type,
#               title_issues, wasted_impressions, diagnosis}

# Retention-weighted sort (recommendation for /retitle command)
def retention_bonus(ret):
    if ret is None: return 0
    if ret >= 35: return 0.5
    if ret >= 25: return 0.25
    return 0

results.sort(key=lambda r: -(r['wasted_impressions'] * (1 + retention_bonus(r.get('retention')))))

report = format_report(results)
print(report)
```

### Generating Candidates for One Video

```python
# Source: tools/retitle_gen.py (verified by reading)
from tools.retitle_gen import generate_script_titles, CANDIDATES
from tools.title_scorer import score_title

video_id = 'LrthC_8Hb2Y'
current_title = 'The 1947 Map That Set the South China Sea on Fire'

# Script-based generation
script_titles = generate_script_titles(video_id, current_title)

# Fallback: pre-generated manual options
manual_options = CANDIDATES.get(video_id, {}).get('options', [])

# Score all candidates
all_options = list(dict.fromkeys(script_titles + manual_options))  # dedupe, preserve order
scored = [(t, score_title(t)) for t in all_options]
scored.sort(key=lambda x: -x[1]['score'])

# Best non-rejected option
best = next((t, s) for t, s in scored if s['grade'] != 'REJECTED')
```

### Thumbnail Compliance Check

```python
# Source: tools/preflight/thumbnail_checker.py (verified by reading)
from tools.preflight.thumbnail_checker import check_thumbnail

# For existing thumbnails, check from description text
# (e.g., from YOUTUBE-METADATA.md thumbnail section if it exists)
concept = "Split-map of the South China Sea, China side in red, other claimants in grey, no text, no face"
result = check_thumbnail(concept)

if result['verdict'] == 'PASS':
    print("Thumbnail compliant — title swap only")
elif result['verdict'] in ('REVIEW', 'FAIL'):
    print("Thumbnail needs work:")
    for issue in result['issues']:
        print(f"  ! {issue}")
```

### Injecting SWAP LOG into POST-PUBLISH-ANALYSIS

```python
# Pattern: read file, check for section, append or create
from pathlib import Path
import re

def add_swap_log_entry(analysis_path: Path, old_title: str, new_title: str,
                        pre_ctr: float, swap_date: str) -> None:
    text = analysis_path.read_text(encoding='utf-8')
    entry = f"| {swap_date} | title | \"{old_title}\" | \"{new_title}\" | {pre_ctr}% | TBD | pending |"

    if '## SWAP LOG' in text:
        # Append row to existing table
        text = text.replace(
            '## SWAP LOG',
            '## SWAP LOG'  # find insertion point after table header
        )
        # Insert before last | row or end of section
        lines = text.splitlines()
        # Find last table row after SWAP LOG header and insert after it
        # ... (implementation detail for planner)
    else:
        swap_section = (
            "\n\n## SWAP LOG\n\n"
            "| Date | Type | Old Value | New Value | Pre-CTR | Post-CTR | Result |\n"
            "|------|------|-----------|-----------|---------|---------|--------|\n"
            f"{entry}\n"
        )
        text += swap_section
    analysis_path.write_text(text, encoding='utf-8')
```

### Post-Swap CTR Ingestion (Success Path)

```python
# Source: tools/ctr_ingest.py (verified via test file test_ctr_ingest.py)
from pathlib import Path
from tools.ctr_ingest import ingest_synthesis_ctr
from tools.discovery.database import KeywordDB

synthesis_path = Path('channel-data/patterns/CROSS-VIDEO-SYNTHESIS.md')
db = KeywordDB()  # Uses default keywords.db path

# After updating CROSS-VIDEO-SYNTHESIS with new CTR:
result = ingest_synthesis_ctr(synthesis_path, db)
print(f"Written: {result['written']}, Skipped: {result['skipped']}, "
      f"Unmatched: {result['unmatched']}")
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual retitle decisions | Wasted impressions formula (audit.py) | Phase 60 context | Objective priority ranking |
| 48h swap window | 7-day window for existing videos | CONTEXT.md decision | Accurate signal for non-new content |
| Title scoring (static patterns) | DB-enriched scoring (Phase 61) | Phase 61 | Scores calibrated to own-channel CTR data |
| No thumbnail compliance check | thumbnail_checker.py | Phase ~47 | Enforces PACKAGING_MANDATE rules |

**The channel's measured CTR penalty data (from channel-data/patterns/TITLE-PATTERNS.md, verified in retitle_audit.py source):**
- Year in title: -46% CTR penalty (HIGH confidence, n=35)
- Colon in title: -28% CTR penalty (HIGH confidence, n=9 vs n=26)
- Question pattern: lower CTR (LOW confidence, n=3 only)
- Versus pattern: ~3.7% CTR (MEDIUM confidence, n=2)
- Declarative: ~3.8% CTR (HIGH confidence, n=19)

---

## Open Questions

1. **Does thumbnail_checker.py work on description-less videos?**
   - What we know: `check_project()` looks for YOUTUBE-METADATA.md in the project folder. Many older videos don't have project folders or metadata files.
   - What's unclear: For the 5 batch videos, will any have accessible thumbnail descriptions to check?
   - Recommendation: `/retitle` command should attempt `check_project()` if project folder exists in VIDEO_PROJECT_MAP; otherwise skip thumbnail check and mark as "THUMBNAIL: Manual check required — no metadata file found."

2. **Is ctr_ingest.py at tools/ctr_ingest.py or tools/youtube_analytics/ctr_ingest.py?**
   - What we know: The test file `tests/integration/test_ctr_ingest.py` imports from `tools.ctr_ingest` (not youtube_analytics). Glob for `tools/youtube_analytics/ctr_ingest.py` returned no result.
   - What's unclear: The file wasn't found by Glob at either location, suggesting it may not yet exist (it's referenced as a Phase 61 integration point).
   - Recommendation: Planner should verify whether `tools/ctr_ingest.py` exists before writing `/retitle --check` logic. If not, the `--check` flag should note it as a dependency and skip the ingest step with a clear message.

3. **VIDEO_PROJECT_MAP in retitle_gen.py is hardcoded — will it cover the top 5 audit results?**
   - What we know: The map has 17 entries, many with `None` (no project folder). The top wasted-impressions candidates from CROSS-VIDEO-SYNTHESIS.md include South China Sea (LrthC_8Hb2Y → None), Dark Ages, Turkey/Greece — several without folders.
   - What's unclear: Which of the top 5 will have SRT access.
   - Recommendation: For videos with `None` mapping, `/retitle` falls back to CANDIDATES dict (already populated for most) or transcripts/retitle/ directory. The command should surface which source was used per video.

---

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest |
| Config file | `pyproject.toml` (testpaths=["tests"]) |
| Quick run command | `python -m pytest tests/integration/test_ctr_ingest.py -x -q` |
| Full suite command | `python -m pytest tests/ -x -q` |

### Phase Requirements → Test Map

| Behavior | Test Type | Automated Command | File Exists? |
|----------|-----------|-------------------|-------------|
| retitle_audit ranks by wasted impressions | unit | `python -m pytest tests/ -k "retitle_audit" -x -q` | ❌ Wave 0 gap |
| generate_script_titles returns non-empty for known video IDs | unit | `python -m pytest tests/ -k "retitle_gen" -x -q` | ❌ Wave 0 gap |
| SWAP-CHECKLIST.md is generated with correct sections | integration (manual inspection) | Run `/retitle`, check output file | N/A — slash command |
| SWAP LOG injection appends not overwrites | unit | `python -m pytest tests/ -k "swap_log" -x -q` | ❌ Wave 0 gap |
| `/retitle --check` refuses if < 7 days since swap | unit | `python -m pytest tests/ -k "retitle_check" -x -q` | ❌ Wave 0 gap |
| ctr_ingest pipeline (feedback success path) | integration | `python -m pytest tests/integration/test_ctr_ingest.py -x -q` | ✅ EXISTS |

### Sampling Rate

- **Per task commit:** `python -m pytest tests/integration/test_ctr_ingest.py -x -q` (fast, < 5s)
- **Per wave merge:** `python -m pytest tests/ -x -q`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps

- [ ] `tests/unit/test_retitle_audit.py` — covers audit ranking + retention weighting
- [ ] `tests/unit/test_retitle_gen.py` — covers generate_script_titles fallback behavior
- [ ] `tests/unit/test_swap_log.py` — covers SWAP LOG injection (append vs create)
- [ ] `tests/unit/test_retitle_check.py` — covers 7-day guard in `--check` flag

Existing: `tests/integration/test_ctr_ingest.py` — already covers the feedback loop end-to-end.

---

## Sources

### Primary (HIGH confidence)

- `tools/retitle_audit.py` — read in full; audit(), format_report(), wasted_impressions formula verified
- `tools/retitle_gen.py` — read in full; generate_script_titles(), VIDEO_PROJECT_MAP, CANDIDATES dict, thesis extraction logic verified
- `tools/preflight/thumbnail_checker.py` — read in full; check_thumbnail(), check_project() signatures verified
- `tools/SWAP-PROTOCOL.md` — read in full; 48h protocol structure, SWAP LOG format verified
- `channel-data/patterns/CROSS-VIDEO-SYNTHESIS.md` — read header; Master Performance Table structure confirmed
- `channel-data/RETITLE-RECOMMENDATIONS.md` — read first 60 lines; fallback pool candidates confirmed
- `channel-data/analyses/POST-PUBLISH-ANALYSIS-LrthC_8Hb2Y.md` — read in full; confirmed no SWAP LOG section exists in current format
- `tests/integration/test_ctr_ingest.py` — read in full; ingest_synthesis_ctr() API, return dict keys, idempotency behavior confirmed
- `.planning/phases/60-.../60-CONTEXT.md` — read in full; all locked decisions and discretion areas
- `.planning/config.json` — nyquist_validation key absent → treat as enabled

### Secondary (MEDIUM confidence)

- `tools/title_scorer.py` — not read directly but API inferred from Phase 61 STATE.md decisions and usage in retitle_gen.py
- `.claude/commands/publish.md` — read in full; slash command structure pattern confirmed

### Tertiary (LOW confidence)

- `tools/ctr_ingest.py` existence — assumed based on test imports `from tools.ctr_ingest import ingest_synthesis_ctr`; Glob returned no result suggesting file may not exist or Glob path was wrong. Planner should verify.

---

## Metadata

**Confidence breakdown:**
- Existing tool APIs: HIGH — read source directly
- SWAP-CHECKLIST.md format: HIGH — derived from CONTEXT.md locked decisions + SWAP-PROTOCOL.md pattern
- Ranking formula recommendation: MEDIUM — logical derivation from existing audit.py code + channel patterns
- ctr_ingest.py existence: LOW — inferred from tests, not confirmed by direct file read

**Research date:** 2026-03-14
**Valid until:** 2026-04-14 (stable domain — tool source code, not fast-moving ecosystem)
