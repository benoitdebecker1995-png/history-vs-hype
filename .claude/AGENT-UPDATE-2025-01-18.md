# Agent Update - January 18, 2025
## Anti-Repetition Rules Added to Script-Writer-v2

---

## What Was the Problem?

The **script-writer-v2** agent was creating scripts with excessive repetition:

### Issues Identified (Fuentes Fact-Check Video):
1. **Höfle Telegram mentioned 6 times** (should be 3 max)
2. **"Deportation records, statistical reports" repeated 4 times** (exact phrase)
3. **"Documentary evidence" repeated 7+ times**
4. **"The Nazis documented" repeated 4 times**
5. **"Erasing evidence" repeated 5+ times**
6. **Conclusion rehashed entire script** instead of being concise
7. **Total runtime: 11:01** (30 seconds too long due to repetition)

### Why This Happened:

The agent's **retention optimization strategy** included:
- Callback hooks every 90 seconds
- Pattern interrupts referencing earlier evidence
- Thesis reinforcement throughout

These are GOOD techniques, but the agent was:
- ❌ Using exact same phrases repeatedly
- ❌ Mentioning the same document 5-6 times
- ❌ Re-explaining concepts multiple times
- ❌ Creating a conclusion that repeated the body text

**Result:** Scripts sounded scripted and repetitive instead of natural and authoritative.

---

## What I Fixed

### Updated File:
**`.claude/agents/script-writer-v2.md`** → Version 2.1 (2025-01-18)

### New Section Added: "Technique 2.5: ANTI-REPETITION RULES"

#### Key Rules Implemented:

### 1. **THE THREE MENTION MAXIMUM**

For any piece of evidence:
- **First mention:** Full introduction with details (e.g., 1:00-2:00)
- **Second mention:** Brief callback (e.g., 4:00-5:00)
- **Third mention:** Visual montage in conclusion (minimal narration)

**NEVER mention the same document 4+ times.**

### 2. **VOCABULARY VARIATION RULE**

Never repeat the exact same phrase more than 2 times.

**Created vocabulary rotation table:**

| Concept | Variations to Use |
|---------|------------------|
| Documents | documents, records, paperwork, files, archives, evidence, sources |
| Evidence | evidence, proof, documentation, records, data, facts |
| Shows/Proves | shows, proves, demonstrates, reveals, confirms, documents |
| Ignoring | ignoring, erasing, dismissing, overlooking, contradicting |

### 3. **REPETITION SELF-AUDIT CHECKLIST**

Before outputting any script, the agent must:
- [ ] Run Ctrl+F on each major piece of evidence (no document mentioned 4+ times)
- [ ] Search repeated phrases ("deportation records," "documentary evidence")
- [ ] Vary if phrase appears 3+ times
- [ ] Count how many times each concept is explained
- [ ] Check conclusion doesn't rehash body text

### 4. **TARGET RUNTIME ADJUSTMENT**

- **Old target:** 10:30 (1,050 words)
- **New target:** 9:00-9:30 (850-950 words)

**Why:** Repetitive callbacks were adding 30-60 seconds without value. Tighter = better retention.

---

## Changes to Quality Assurance Checklist

Added new **ANTI-REPETITION CHECK** section:

```markdown
### ANTI-REPETITION CHECK (CRITICAL - NEW):
- [ ] Run Ctrl+F on each major piece of evidence - No document mentioned 4+ times
- [ ] Search "deportation records" or similar phrases - Varies if 3+ occurrences
- [ ] Search "documentary evidence" or similar - Varies if 3+ occurrences
- [ ] Search your thesis phrase (e.g., "erasing evidence") - Used 2 times max
- [ ] Read conclusion aloud - Does it repeat body text or use fresh phrasing?
- [ ] Count evidence mentions:
  - Main document: 3 times max
  - Secondary documents: 2-3 times max
  - Each concept explained once, not 3+ times
- [ ] Vocabulary variation: Same phrase not repeated 3+ times
- [ ] Conclusion length: Under 90 seconds (no rehashing entire script)
```

This checklist runs BEFORE the agent outputs any script.

---

## Impact on Future Scripts

### What Will Change:

✅ **Evidence mentions reduced:**
- Höfle Telegram: 6 mentions → 3 mentions
- Major documents: Introduced once, referenced once, shown once in conclusion

✅ **Varied vocabulary:**
- "Deportation records, statistical reports" → "Nazi paperwork" → "their files" → "the archives"
- No exact phrase repeated 3+ times

✅ **Tighter conclusions:**
- Old: 2+ minutes rehashing everything
- New: 75-90 seconds with fresh phrasing

✅ **Shorter runtime:**
- Old: 10:30-11:00 (too long due to repetition)
- New: 9:00-9:30 (tighter, better retention)

✅ **More natural delivery:**
- Sounds less scripted
- Trusts viewers to remember key evidence
- Focuses on new information, not repetition

### What Won't Change:

✅ Retention optimization (hooks, pattern interrupts, modern connections)
✅ Authority markers and primary source emphasis
✅ "Both extremes" structure
✅ Educational value and nuance
✅ Voice and tone calibration

---

## Example: Before vs After

### BEFORE (v2.0 - Repetitive):

**Line 55:** "I went to the documents he's ignoring—Nazi deportation records, statistical reports, perpetrator documentation, and the Founding Fathers' own petitions to the King."

**Line 208:** "Remember that encrypted telegram?"

**Line 277:** "This is the evidence Fuentes calls 'not physical.' Deportation records. Statistical reports with coded language."

**Line 423:** "The Nazis documented their genocide in bureaucratic detail. Deportation logistics to death camps. Statistical reports using 'special treatment' as code for killing."

**Line 447:** "Nazi deportation records showing 1.27 million sent to death camps in one year."

**Result:**
- "Deportation records/logistics, statistical reports" appears 4 times
- Höfle Telegram mentioned 6 times
- Runtime: 10:30+

---

### AFTER (v2.1 - Varied):

**Line 40:** "I went to the Nazi paperwork—deportation logs, statistical reports, execution records—and the Founding Fathers' own petitions to the King."

**Line 350:** "Fuentes said maybe three hundred thousand total deaths. These Nazi records show 1.8 million by the end of 1942 alone."

**Line 530:** "From what I've seen in the actual Nazi files—the originals, not summaries—the pattern's clear."

**Line 905:** "Nazi logistics showing 1.27 million sent to death camps in one year."

**Result:**
- Each mention uses different phrasing
- Höfle Telegram mentioned 3 times (not 6)
- Runtime: 9:30

---

## How to Test

### For Next Script:

1. **After agent delivers script, run these searches:**
   - Ctrl+F: Name of main document (should appear 3 times max)
   - Ctrl+F: "deportation records" or similar repeated phrase
   - Ctrl+F: Your thesis phrase

2. **Count occurrences:**
   - If any phrase appears 4+ times → Agent failed the check
   - If conclusion repeats body text → Agent failed the check

3. **Check runtime:**
   - Should be 9:00-9:30, not 10:30+

### If Repetition Still Occurs:

Tell me which phrases are repeated and I'll tighten the rules further.

---

## Files Updated

1. **`.claude/agents/script-writer-v2.md`**
   - Added "Technique 2.5: ANTI-REPETITION RULES"
   - Updated Quality Assurance Checklist
   - Changed target runtime from 10:30 to 9:00-9:30
   - Version bumped to 2.1 (2025-01-18)

2. **`video-projects/_IN_PRODUCTION/3-fuentes-fact-check-2025/FINAL-SCRIPT.md`**
   - Updated to v5.0 with repetitions removed
   - Old v4.0 saved as `FINAL-SCRIPT-v4-OLD.md`

---

## Summary

**Problem:** Retention optimization created excessive repetition (same evidence mentioned 6 times, same phrases repeated 4+ times)

**Solution:** Added "Three Mention Maximum" rule, vocabulary variation requirements, and repetition self-audit checklist

**Result:** Future scripts will be tighter (9:00-9:30), more varied vocabulary, and less repetitive while maintaining retention optimization

**Version:** script-writer-v2 updated to v2.1 (2025-01-18)

---

**Next script you generate will automatically follow these anti-repetition rules.**
