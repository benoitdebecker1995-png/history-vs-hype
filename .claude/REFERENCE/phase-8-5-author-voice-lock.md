# Phase 8.5: Author Voice & Delivery Lock

**Position:** After Phase 8 (Coverage Audit) → Before filming
**Type:** Non-blocking (advisory unless critical filmability issue)
**Purpose:** Verify script is speakable, consistent with author voice, and ready for camera

*Created: 2025-12-28*

---

## WHEN TO RUN

Run Phase 8.5 when:
- Script draft is approved (structure finalized)
- Research and fact-checking complete
- Coverage checkpoint passed
- Target runtime established
- Filming format decided (A-roll ratio, document readouts, maps)

Do NOT run if:
- Script structure is still being revised
- Research gaps remain open
- Video type classification is uncertain

---

## INPUTS

| Input | Source | Purpose |
|-------|--------|---------|
| Approved script draft | Project folder | Text to evaluate |
| `author-style.md` | `.claude/REFERENCE/` | Voice consistency reference |
| Target runtime | Script metadata | Pacing calibration |
| Filming format | Script metadata | A-roll/B-roll ratio expectations |

---

## DELIVERY CHECKS

### Check 1: Opening Cadence (0:00-0:45)

**Requirement:** First 45 seconds must establish neutrality, authority, and stakes in spoken-friendly rhythm.

| Element | Target | Flag If |
|---------|--------|---------|
| First sentence | ≤12 words, declarative | >15 words or question |
| Stakes statement | By 0:25 | Missing or after 0:30 |
| Authority marker | "I went to..." or equivalent | Missing entirely |
| Payoff/promise | By 0:40 | Missing or vague |

**Pass Criteria:** 3/4 elements present and speakable

---

### Check 2: Authority Markers

**Requirement:** Script must contain explicit author authority signals.

| Marker Type | Minimum | Example |
|-------------|---------|---------|
| "I went to the documents" | 1x in opening | "I went to the Nazi paperwork" |
| "Reading directly from" | ≥2x in script | "Reading from the judgment..." |
| "That's not my interpretation" | ≥1x after key evidence | After AU quote |

**Pass Criteria:** All three marker types present

---

### Check 3: Declarative Fragments

**Requirement:** Script uses punchy incomplete sentences for emphasis at key moments.

**Check for:**
- Period-separated emphasis phrases ("Not 1916. Fifteen years.")
- Single-word or two-word beats ("Neither signed." / "Restored.")
- Fragment-then-expansion pattern

**Pass Criteria:** ≥5 declarative fragments across script

---

### Check 4: Caveat Placement

**Requirement:** Caveats appear immediately after strong claims, not buried later.

**Pattern:** `[Strong claim] → [Immediate caveat within 2 sentences]`

**Check for:**
- "Now—one caveat..."
- "I should be clear..."
- "Whether that [difference/distinction]—scholars disagree"

**Pass Criteria:** ≥2 explicit caveats, none delayed >3 sentences from claim

---

### Check 5: Document Readout Spacing

**Requirement:** Primary source readouts are distributed for rhythm, not clustered.

| Script Length | Minimum Readouts | Maximum Gap |
|---------------|------------------|-------------|
| 6-8 min | 3-4 | 3 minutes |
| 10-12 min | 5-6 | 2.5 minutes |
| 13-15 min | 6-8 | 2.5 minutes |

**Check for:**
- Even distribution across acts
- No back-to-back readouts without camera break
- Key readout marked for emphasis (hold 6-8 seconds)

**Pass Criteria:** Distribution within limits, key moment identified

---

### Check 6: Breath/Beat Timing

**Requirement:** Script allows natural pauses for spoken delivery.

**Check for:**
- Sentences ≤25 words (breathing room)
- Paragraph breaks between major points
- Beat markers before emotional peaks (e.g., "But here's the thing...")
- No run-on sections >4 sentences without break

**Pass Criteria:** No section requires unnatural breath-holding

---

### Check 7: Filming Format Alignment

**Requirement:** Script markers match intended filming format.

| Format Element | Check |
|----------------|-------|
| A-roll ratio | `[ON-CAMERA]` markers present and distributed |
| VO sections | `[VO]` clearly marked, ≤30 sec each |
| Document displays | Readout text matches actual document |
| Map sequences | Geographic progression logical |

**Pass Criteria:** All format markers present and consistent

---

## OUTPUT

### Verdict Options

```
✅ READY TO FILM
All 7 checks pass. No delivery adjustments needed.

⚠️ MINOR DELIVERY ADJUSTMENTS RECOMMENDED
5-6 checks pass. Script filmable, but specific refinements would improve spoken delivery.
[List specific adjustments]

❌ DELIVERY ISSUES BLOCK FILMING
<5 checks pass. Significant spoken delivery problems would harm filming.
[List blocking issues]
```

### Blocking Threshold

Phase 8.5 is **non-blocking** unless:
- Opening cadence completely fails (no stakes, no authority, no payoff)
- Zero authority markers present
- Document readouts clustered in single section with 5+ minute gap elsewhere
- Sentences consistently >30 words with no breaks

---

## INTEGRATION WITH PHASE SYSTEM

```
Phase 1-6: Research, Scripting, Fact-Checking
    ↓
Phase 7: Creator Technique Integration (Shaun, etc.)
    ↓
Phase 8: Coverage Audit (training data sufficiency)
    ↓
→ Phase 8.5: Author Voice & Delivery Lock ←
    ↓
Filming
    ↓
Phase 9 (future): Stylistic Arbitration
```

**Phase 8.5 does NOT:**
- Modify research or sources
- Change script structure
- Add new evidence
- Alter video type classification
- Interact with Gates 0-3

**Phase 8.5 ONLY:**
- Verifies spoken delivery
- Confirms author voice consistency
- Checks filmability markers
- Flags breath/timing issues

---

## QUICK REFERENCE

| Check | Pass Threshold | Blocking? |
|-------|----------------|-----------|
| Opening Cadence | 3/4 elements | Only if 0/4 |
| Authority Markers | 3/3 types present | Only if 0/3 |
| Declarative Fragments | ≥5 across script | No |
| Caveat Placement | ≥2, not delayed | No |
| Document Readout Spacing | Within limits | Only if major clustering |
| Breath/Beat Timing | No unnatural sections | Only if multiple violations |
| Filming Format Alignment | Markers present | Only if markers missing |

---

## USAGE

**To run Phase 8.5:**

1. Confirm script is structurally approved
2. Open script and `author-style.md`
3. Run each check sequentially
4. Tally results
5. Issue verdict
6. If adjustments recommended, list specific line-level fixes

**Do not:**
- Rewrite sections for style preference
- Add new content
- Change argument structure
- Delay filming for minor issues
