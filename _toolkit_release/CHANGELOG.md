# Changelog

## v1.0 — 2026-05-08

Initial release.

**Included:**
- `PACKAGING-SYSTEM.md` (and exported PDF) — 40-page methodology
- `scripts/title_scorer_standalone.py` — working title scorer, no dependencies
- `scripts/README.md` — usage and calibration guide

**Calibrated to:** A 47-video history channel with 33 videos of paired
CTR + impression data, plus 388 competitor titles and 650 competitor
thumbnails analyzed.

## Planned for v2.0 — Q3 2026 (free upgrade for v1 buyers)

**New scripts:**
- `packaging_autopilot.py` — 48-hour swap protocol automation reading
  YouTube Studio CSV exports
- `article_scorer.py` — newsletter article quality grader (16 checks)
- `subject_line_scorer.py` — email subject line grader
- `retitle_gen.py` — auto-generate retitle candidates from a video's
  opening hook
- `thumbnail_checker.py` — niche-specific thumbnail rule validator

**Architecture changes:**
- Pluggable adapter pattern so users can wire in their own analytics data
  without modifying the scoring core
- `PATTERN_SCORES` exposed via config file (no source-edit needed for
  calibration)
- Optional niche benchmark layer (drop in any competitor CSV; tools
  auto-derive comparisons)

**Methodology updates:**
- Two more case studies added once v1 buyer feedback comes in
- Updated calibration data from any v1 buyer who shares before/after CTR
  comparisons (anonymized)

## How to claim v2 free upgrade

Keep the email Gumroad sent you when you bought v1. When v2 ships, reply to
that email with subject "v2 upgrade" and you'll receive a fresh download
link at no charge.
