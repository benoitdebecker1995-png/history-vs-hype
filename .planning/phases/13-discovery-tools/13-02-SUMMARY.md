---
phase: 13
plan: 02
subsystem: discovery
tags: [intent-classification, dna-fit, diagnostics, analyze-command]
requires:
  - 13-01 (keyword database and autocomplete)
  - 09-01 (channel_averages for benchmarks)
provides:
  - intent_mapper.py (6-category classification)
  - diagnostics.py (discovery issue diagnosis)
  - /analyze with discovery diagnostics section
affects:
  - Future keyword evaluation workflows
  - Post-publish video analysis
tech-stack:
  added: []
  patterns:
    - Intent pattern matching with confidence scoring
    - DNA fit scoring (positive/negative signals)
    - Channel-specific diagnostic thresholds
key-files:
  created:
    - tools/discovery/intent_mapper.py
    - tools/discovery/diagnostics.py
  modified:
    - tools/youtube-analytics/analyze.py
decisions:
  - title: Confidence scoring approach
    choice: "1 match = 0.33, 2 = 0.66, 3+ = 1.0 (not ratio-based)"
    rationale: "Single strong pattern match should qualify (e.g., 'myth' in MYTH_BUSTING)"
    alternatives: "Ratio-based (matched/total) required too many pattern matches"

  - title: DNA fit signal weighting
    choice: "Positive signals +0.2 each, negative -0.3 each, base 0.5"
    rationale: "Negative signals (clickbait/conspiracy) should be stronger penalty"
    alternatives: "Equal weighting made clickbait too easy to pass"

  - title: Diagnostic threshold for impressions
    choice: "50% of channel average = LOW_IMPRESSIONS"
    rationale: "Channel-specific, accounts for varying channel sizes"
    alternatives: "Absolute threshold would fail for small/large channels"

  - title: Discovery diagnostics placement
    choice: "After Lessons section in /analyze output"
    rationale: "Lessons = what happened, Discovery = why it happened"
    alternatives: "Before lessons would interrupt narrative flow"

  - title: Graceful degradation pattern
    choice: "DISCOVERY_AVAILABLE flag with try/except import"
    rationale: "analyze.py works even if discovery module missing"
    alternatives: "Hard dependency would break existing /analyze installs"

metrics:
  duration: 71.5 minutes
  completed: 2026-01-30
---

# Phase 13 Plan 02: Intent Classification & Discovery Diagnostics Summary

**One-liner:** 6-category intent classification with DNA fit scoring + channel-specific discovery diagnostics integrated into /analyze

## What Was Built

### Intent Classification (DISC-02)

**File:** `tools/discovery/intent_mapper.py` (475 lines)

**6 History-Niche Categories:**
1. **MYTH_BUSTING** - Correcting historical misconceptions (patterns: myth, debunk, false, etc.)
2. **TERRITORIAL_DISPUTE** - Border conflicts (patterns: border, dispute, claim, etc.)
3. **PRIMARY_SOURCE** - Document analysis (patterns: treaty, manuscript, archive, etc.)
4. **MECHANISM_EXPLAINER** - How things worked (patterns: how did, process, system, etc.)
5. **TIMELINE_CORRECTION** - Chronology corrections (patterns: when, timeline, date, etc.)
6. **IDEOLOGICAL_NARRATIVE** - Belief analysis (patterns: why, ideology, narrative, etc.)

**Functions:**
- `classify_intent(query, min_confidence=0.3)` - Match against categories, return primary + secondary
- `calculate_dna_fit(query)` - Score 0-1 with GOOD_FIT/MARGINAL/POOR_FIT recommendation
- `classify_title(title)` - Convenience wrapper for intent + DNA fit
- `save_classification_to_db(keyword_id, classification)` - Database integration

**CLI Usage:**
```bash
python intent_mapper.py "dark ages myth"
python intent_mapper.py "secret history" --json
python intent_mapper.py --batch "myth1, myth2, myth3"
```

**DNA Fit Signals:**
- **Positive:** evidence, document, source, proof, archive, manuscript, fact, debunk, scholar
- **Negative:** conspiracy, secret, hidden, shocking, "you won't believe", "don't want you"

**Confidence Scoring:** 1 match = 0.33, 2 matches = 0.66, 3+ matches = 1.0

### Discovery Diagnostics (DISC-03)

**File:** `tools/discovery/diagnostics.py` (434 lines)

**Diagnostic Logic:**
- **Low impressions** (< 50% channel avg) → SEO/metadata issue
- **Low CTR** (< 4%) → Title/thumbnail issue
- **Both low** → Topic selection issue

**Functions:**
- `get_diagnostic_thresholds(channel_averages)` - Channel-specific thresholds
- `diagnose_discovery(video_metrics, channel_averages, ctr)` - Full diagnosis with fixes + learnings
- `format_diagnosis_markdown(diagnosis)` - Markdown output

**Output Structure:**
```python
{
  'diagnosis': {
    'primary_issue': 'LOW_IMPRESSIONS' | 'LOW_CTR' | 'BOTH' | 'NONE',
    'severity': 'HIGH' | 'MEDIUM' | 'LOW',
    'summary': 'One-line diagnosis'
  },
  'issues': [...],      # What's wrong
  'fixes': [...],       # Actionable fixes with priority
  'learnings': [...]    # Apply to future videos
}
```

**CLI Usage:**
```bash
python diagnostics.py VIDEO_ID
python diagnostics.py VIDEO_ID --ctr 3.5
python diagnostics.py VIDEO_ID --json
```

### /analyze Integration

**File:** `tools/youtube-analytics/analyze.py` (modified, now 1024 lines)

**Changes:**
1. Import discovery diagnostics with graceful degradation (`DISCOVERY_AVAILABLE` flag)
2. Call `diagnose_discovery()` in `run_analysis()` after lessons generation
3. Add "Discovery Diagnostics" section to `format_analysis_markdown()`

**Section Location:** After "Lessons" section, before "Errors" section

**Section Content:**
- Diagnosis summary (primary issue, severity)
- Issues detected (with benchmarks)
- Recommended fixes (with priority and rationale)
- Learnings for future videos (with application notes)

## Verification Results

**Test 1: Intent classification**
```bash
$ python intent_mapper.py "why did the USSR collapse"
Primary Intent: IDEOLOGICAL_NARRATIVE
  Confidence: 0.33
  Matched: why
```
✅ PASS

**Test 2: DNA fit with clickbait**
```bash
$ python intent_mapper.py "secret history they don't want you to know"
Channel DNA Fit: POOR_FIT
  Score: 0.0
  Reason: Clickbait/conspiracy signals detected
  Negative signals: secret, don't want you
```
✅ PASS

**Test 3: Diagnostic thresholds**
```python
get_diagnostic_thresholds({'avg_views': 1000, 'sample_size': 10})
# Returns: {'impressions_low': 500.0, 'ctr_low': 4.0, ...}
```
✅ PASS

**Test 4: Discovery availability**
```python
from analyze import DISCOVERY_AVAILABLE
# Returns: True
```
✅ PASS

## Example Outputs

### Intent Classification Example

**Query:** "dark ages myth"

**Output:**
```
Primary Intent: MYTH_BUSTING
  Confidence: 0.33
  Matched: myth
  Description: Correcting historical misconceptions

Channel DNA Fit: MARGINAL
  Score: 0.5
  Reason: Neutral tone - could work with proper framing
```

### Discovery Diagnostics Example

**Video:** Low-performing video with 200 views (channel avg: 1000)

**Output:**
```markdown
## Discovery Diagnostics

**Diagnosis:** SEO/metadata issue - YouTube not showing video to enough people
**Primary Issue:** LOW_IMPRESSIONS (Severity: HIGH)

### Issues Detected
- **LOW_IMPRESSIONS** (HIGH): Views 80% below channel average - YouTube not showing this video

### Recommended Fixes
- [IMMEDIATE] Add long-tail keywords to description
  - *Why:* Low impressions = YouTube doesn't understand topic relevance
- [HIGH] Add video to relevant playlists
  - *Why:* Increases discoverability through browse features

### Learnings for Future Videos
- Topic may have low search demand or high competition
  - *Apply to:* Future topic selection - verify search volume with keyword tools before committing
```

## Deviations from Plan

None - plan executed exactly as written.

## Performance Notes

**Intent classification:** Instant (no API calls)

**Discovery diagnostics:** Requires existing channel_averages data (Phase 9-01)

**Graceful degradation:** If discovery module unavailable, /analyze continues without Discovery Diagnostics section

## Integration Points

**Database (Phase 13-01):**
- `save_classification_to_db()` stores intent classifications in `keyword_intents` table

**Channel Averages (Phase 9-01):**
- `diagnose_discovery()` uses channel benchmarks for threshold calculations

**/analyze Command:**
- Discovery diagnostics appear automatically when `DISCOVERY_AVAILABLE = True`

## Next Phase Readiness

**Phase 13-03:** Keyword research automation (autocomplete scraping + intent classification)

**Ready to use:**
- Intent mapper for classifying scraped keywords
- DNA fit filter to exclude clickbait topics
- Diagnostics to analyze why videos underperform

**Remaining work:**
- Keyword research CLI (wrapper combining autocomplete + intent + database)
- Bulk keyword processing for topic research
- Export functionality for spreadsheet analysis

## Success Criteria Met

- [x] 6 intent categories defined and classifying correctly
- [x] DNA fit score identifies channel-appropriate vs clickbait topics
- [x] Diagnostics identifies LOW_IMPRESSIONS vs LOW_CTR issues correctly
- [x] /analyze output includes Discovery Diagnostics section
- [x] Learnings captured for future video improvement
- [x] Graceful degradation when discovery module unavailable

---

**Phase 13-02 Complete** - Intent classification and discovery diagnostics operational. /analyze now provides actionable discovery insights.
