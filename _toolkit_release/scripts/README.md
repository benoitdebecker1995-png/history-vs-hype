# Scripts — Reference Implementation

This v1 release ships with **one fully working standalone script** that implements every rule in `PACKAGING-SYSTEM.md`. No external dependencies, no database setup, no calibration required to start.

## What's in here

| Script | What it does | Status |
|--------|--------------|--------|
| `title_scorer_standalone.py` | Scores titles 0-100 against pattern detection, hard rejects, and bonus signals from the methodology | **Ready — runs out of the box** |

## Quick start (60 seconds)

Requirements: Python 3.10 or newer. No pip installs needed.

```bash
python title_scorer_standalone.py "Your Title Here"
python title_scorer_standalone.py "Title A" "Title B" "Title C"
python title_scorer_standalone.py --file my_titles.txt
```

You'll get a score, grade (A-F or REJECTED), pattern detection, full breakdown of penalties and bonuses, and concrete fix suggestions.

## How the score maps to the methodology

Every line of `score_title()` corresponds to a rule in `PACKAGING-SYSTEM.md`:

| Code element | Methodology section |
|--------------|--------------------|
| `PATTERN_SCORES` dict (lines 31-38) | Section 2 — Six Title Patterns |
| `YEAR_PENALTY`, `COLON_PENALTY`, `THE_X_THAT_PENALTY` | Section 3 — Three Hard Rejects |
| `EVIDENCE_PROMISE_BONUS`, `ENTITY_BONUS`, etc. | Section 4 — Six Bonus Signals |
| `detect_pattern()` regex order | Section 2 — Order matters; first match wins |

Read the methodology, then read the code. The script is short on purpose — it's a teaching tool, not a black box.

## Calibrating to your channel

The `PATTERN_SCORES` are calibrated to one specific 47-video history channel. Yours will differ. After 30 days of CTR data, edit lines 31-38 directly:

```python
PATTERN_SCORES = {
    'versus':      75,   # Replace with: (your_versus_avg_ctr / your_overall_avg_ctr) * 50
    'declarative': 65,
    'how_why':     55,
    'question':    45,
    'colon':       30,
    'the_x_that':  10,
}
```

See `PACKAGING-SYSTEM.md` Section 8 for the full calibration plan.

You can also tune the word lists for your beat:

- `SCALE_WORDS` (line 67) — words signaling stakes
- `ACTIVE_VERBS` (line 73) — your channel's verb vocabulary
- `EVIDENCE_PHRASES` (line 79) — channel-specific evidence language
- `CONTROVERSY_WORDS` (line 86) — myth-busting/accusation framing
- entity regex in `has_named_entity()` (line 154) — countries/orgs/leaders relevant to your beat

## What's coming in v2 (free upgrade for v1 buyers)

Q3 2026 release will add:

1. **`packaging_autopilot.py`** — 48-hour swap protocol automation reading your YouTube Studio CSV exports
2. **`article_scorer.py`** — Same scoring logic for newsletter articles
3. **`subject_line_scorer.py`** — Email subject line grader
4. **`retitle_gen.py`** — Auto-generate retitle candidates from a video's opening hook
5. **`thumbnail_checker.py`** — Niche-specific thumbnail rule validator (text overlay, face/no-face, color contrast)

V2 will use a pluggable adapter pattern so you can wire in your own analytics data without touching the scoring core.

**Keep your Gumroad receipt email — v2 ships free to v1 buyers.**

## Support tiers

**Methodology buyers ($49):** Self-serve. The methodology *is* the support. Calibrate to your own channel as your data accumulates.

**Loom buyers ($99):** Send your channel link + 5 titles you want scored to the email in your receipt. You'll receive a 60-minute async Loom walkthrough showing the methodology applied to your specific channel within 5 business days.

## Encoding note

The scorer auto-configures UTF-8 stdout on Windows. If you see encoding errors on a non-Windows platform, run with:

```bash
PYTHONIOENCODING=utf-8 python title_scorer_standalone.py "Your Title"
```

---

*v1.0 — 2026-05-08*
