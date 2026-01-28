# Phase 12 Context: Voice Fingerprinting

**Created:** 2026-01-28
**Phase Goal:** Learn speech patterns from existing transcripts

## Requirement

**SCRIPT-05:** Voice fingerprinting — analyze transcripts to learn speech patterns, flag violations

## Key Decisions

### Training Approach

**Learn from script→transcript differences, not raw transcripts.**

The user follows AI-generated scripts but modifies them during delivery to sound more natural. The fingerprinting should:
1. Compare written scripts to final transcripts (SRT files)
2. Extract patterns from the modifications
3. Apply those patterns to new scripts during generation

**Corpus:** Hybrid approach
- Analyze all available video pairs (script + transcript)
- Weight modifications that improved delivery
- Both scripts and SRT files available for most videos

### Pattern Types

**All pattern types equally important:**

1. **Sentence breaking** — How long sentences are split for breath/clarity
2. **Word substitutions** — Formal→conversational swaps (e.g., "utilize"→"use")
3. **Rhythm markers** — Where pauses, emphasis, transitions are added

**Anti-patterns tracked:**
- Words/phrases consistently removed during delivery
- Constructions that get restructured every time

### Integration Strategy

**Bake into scriptwriter, not post-hoc flagging.**

Instead of:
```
Script generated → Voice checker flags violations → User fixes
```

Use:
```
Script generated WITH voice patterns already applied → Output sounds natural
```

**Optional transparency:** `--show-voice-changes` flag shows where patterns were applied

### Threshold Behavior

**Evolving thresholds:**
- Confidence grows as more transcript comparisons are added
- Initial patterns from bulk analysis
- Updates after each new video published

### Storage

**Pattern library:** `tools/script-checkers/voice-patterns.json`

Structure (preliminary):
```json
{
  "sentence_patterns": {
    "max_preferred_length": 18,
    "break_triggers": ["which", "that", "because"]
  },
  "word_substitutions": {
    "utilize": "use",
    "commence": "start"
  },
  "anti_patterns": {
    "phrases_to_avoid": ["it should be noted that", "in order to"]
  },
  "confidence": {
    "videos_analyzed": 10,
    "last_updated": "2026-01-28"
  }
}
```

### Workflow Integration

**Initial build:**
1. Bulk analyze all available script+transcript pairs
2. Generate initial voice-patterns.json

**Ongoing updates:**
1. After publishing new video, run transcript comparison
2. Update patterns with new data

**Scriptwriter integration:**
1. /script command loads voice-patterns.json
2. Applies patterns during generation
3. Optional: --show-voice-changes to see what was applied

## Open Questions for Research

1. What diff algorithm works best for script↔transcript comparison?
2. How to handle SRT timing data — use for pause detection?
3. Minimum corpus size for reliable patterns?
4. How to weight recent videos vs. older ones?

## Dependencies

- **Phase 11 complete:** Uses script-checkers infrastructure
- **Requires:** Script files in video-project folders
- **Requires:** SRT transcripts from published videos

## Success Criteria (from ROADMAP)

1. User can analyze existing video transcripts to build speech pattern library
2. User can flag script violations of established voice patterns
3. User can see suggestions aligned with personal delivery style

**Note:** Criterion 2 is satisfied by integration into scriptwriter (violations prevented, not just flagged).

---

*Context gathered: 2026-01-28*
