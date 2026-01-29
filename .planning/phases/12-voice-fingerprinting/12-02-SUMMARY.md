---
phase: 12-voice-fingerprinting
plan: 02
subsystem: script-analysis
tags: [pattern-application, regex, word-boundaries, cli-integration]

# Dependency graph
requires:
  - phase: 12-01
    provides: voice-patterns.json structure and corpus analysis infrastructure
  - phase: 11-script-quality-checkers
    provides: CLI infrastructure and BaseChecker pattern
provides:
  - Voice pattern application with VoicePatternApplier class
  - CLI integration with --voice, --show-voice-changes, --rebuild-voice flags
  - Case-preserving word substitutions with word boundaries
  - Anti-pattern removal with whitespace normalization
  - Lazy imports to avoid srt dependency blocking pattern application
affects: [script-generation, scriptwriting-workflow]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Lazy imports via __getattr__ to avoid blocking dependencies"
    - "Word boundary regex with case-preserving replacement"
    - "Transform-then-check pattern (voice patterns applied before checkers)"
    - "Graceful degradation when patterns file missing"

key-files:
  created:
    - tools/script-checkers/voice/pattern_applier.py
  modified:
    - tools/script-checkers/voice/__init__.py
    - tools/script-checkers/cli.py

key-decisions:
  - "Lazy imports to avoid srt dependency blocking pattern_applier usage"
  - "Case-preserving replacement (capitalize if original capitalized)"
  - "Only apply HIGH-confidence patterns (frequency >= 5)"
  - "Voice patterns applied BEFORE checkers (transform then check)"
  - "script_path made optional (nargs='?') to support --rebuild-voice standalone"

patterns-established:
  - "Lazy module loading via __getattr__ for optional dependencies"
  - "Word boundary regex: r'\\b' + re.escape(formal) + r'\\b'"
  - "Whitespace normalization after removal: re.sub(r'\\s+', ' ')"
  - "format_voice_changes() for human-readable modification summary"

# Metrics
duration: 5min
completed: 2026-01-29
---

# Phase 12 Plan 02: Voice Pattern Application Summary

**CLI-integrated pattern applier with case-preserving word substitutions, anti-pattern removal, and lazy imports to avoid blocking dependencies**

## Performance

- **Duration:** 5 min
- **Started:** 2026-01-29T04:36:48Z
- **Completed:** 2026-01-29T04:42:49Z
- **Tasks:** 3
- **Files modified:** 3

## Accomplishments

- Created VoicePatternApplier class with apply_word_substitutions() and remove_anti_patterns()
- Integrated voice patterns into CLI with --voice, --show-voice-changes, --rebuild-voice flags
- Implemented lazy imports via __getattr__ to avoid srt dependency blocking pattern_applier
- Case-preserving word replacement using regex with word boundaries
- Transform-then-check workflow (voice patterns applied before quality checkers)

## Task Commits

Each task was committed atomically:

1. **Task 1: Create pattern applier module** - `689b00a` (feat)
   - voice/pattern_applier.py with VoicePatternApplier class
   - apply_word_substitutions() for HIGH-confidence substitutions
   - remove_anti_patterns() for phrase removal
   - Case-preserving replacement with word boundaries
   - Lazy imports in __init__.py to avoid srt dependency blocking

2. **Task 2: Integrate with CLI** - `1cc9d00` (feat)
   - Added --voice, --show-voice-changes, --voice-patterns flags
   - format_voice_changes() displays modifications summary
   - Voice patterns applied BEFORE checkers run (transform then check)
   - Graceful handling of missing voice-patterns.json
   - Updated help text and examples

3. **Task 3: Add corpus rebuild command** - (implemented in Task 2 commit `1cc9d00`)
   - --rebuild-voice command to regenerate voice-patterns.json
   - Auto-detect projects directory relative to CLI or script path
   - Print summary after rebuild (videos analyzed, patterns found)
   - Clear error message when srt not installed

**Plan metadata:** (pending final commit)

## Files Created/Modified

- `tools/script-checkers/voice/pattern_applier.py` - Apply learned patterns to new scripts
  - VoicePatternApplier class loads patterns from JSON
  - apply_word_substitutions() with case-preserving regex replacement
  - remove_anti_patterns() with whitespace normalization
  - apply_voice_patterns() convenience function

- `tools/script-checkers/voice/__init__.py` - Lazy imports for optional dependencies
  - Direct export of pattern_applier (always available)
  - Lazy-load corpus_builder and pattern_extractor via __getattr__
  - Avoids srt import blocking pattern application

- `tools/script-checkers/cli.py` - CLI integration with voice flags
  - --voice: Apply learned patterns to script
  - --show-voice-changes: Display modification summary
  - --voice-patterns PATH: Custom patterns file location
  - --rebuild-voice: Regenerate patterns from corpus
  - format_voice_changes() for human-readable output
  - Voice application runs BEFORE checkers (transform then check)

## Decisions Made

**Lazy imports to avoid srt dependency:**
- Rationale: pattern_applier only needs JSON parsing, not srt library
- srt is only required for corpus_builder (--rebuild-voice)
- Lazy imports via __getattr__ allow pattern application without srt installed
- User experience: --voice works immediately, --rebuild-voice prompts for srt install

**Case-preserving replacement:**
- Rationale: "Utilize" -> "Use" not "use" (preserve sentence-initial capitalization)
- Implementation: Check match.group(0)[0].isupper(), capitalize replacement if True
- Maintains natural sentence structure

**Only HIGH-confidence patterns:**
- Rationale: Frequency >= 5 indicates consistent pattern, not occasional ad-lib
- MEDIUM patterns (freq 3-4) skipped to avoid over-applying
- User can lower threshold in future if needed

**Transform-then-check workflow:**
- Rationale: Voice patterns should apply before quality checkers analyze
- Modified script goes through checkers, not original
- Allows checking transformed script for issues

**script_path optional (nargs='?'):**
- Rationale: --rebuild-voice doesn't need a script path
- Changed from required positional arg to optional
- Error handling: require script_path unless --rebuild-voice

## Deviations from Plan

None - plan executed exactly as written.

Note: Task 3 (--rebuild-voice command) was implemented during Task 2 integration because it logically belonged with the other CLI flags. All Task 3 verification requirements were met.

## Issues Encountered

**Windows console encoding (UnicodeEncodeError):**
- Problem: cmd.exe can't display Unicode checkmarks in scaffolding checker output
- Not a code issue: checkers use Unicode in output, Windows console uses cp1252
- Workaround: Use --json flag for Windows compatibility, or redirect to file
- No fix needed: works correctly on UTF-8 consoles

## User Setup Required

**srt library required for corpus analysis (--rebuild-voice):**
- Pattern application (--voice) works without srt
- Corpus rebuild (--rebuild-voice) requires srt library
- Install: `pip install srt`
- See: tools/script-checkers/VOICE-SETUP.md for details

After installing srt, user should run:
```bash
cd tools/script-checkers
python cli.py --rebuild-voice
```

This will analyze all available script+SRT pairs and populate voice-patterns.json with learned patterns.

## Next Phase Readiness

**Ready for use in scriptwriting workflow:**
- ✅ Pattern application complete and CLI-integrated
- ✅ User can apply patterns with --voice flag
- ✅ User can see modifications with --show-voice-changes
- ✅ User can rebuild patterns with --rebuild-voice
- ⚠️ User must install srt and run --rebuild-voice to populate patterns

**Blockers:**
- None for phase completion
- User action required: install srt, run corpus analysis to populate patterns

**Workflow enabled:**
1. User publishes new video → run `python cli.py --rebuild-voice` to update patterns
2. User generates new script → run `python cli.py script.md --voice --show-voice-changes`
3. Pattern library grows more accurate with each video published

**Pattern library bootstrapping:**
- With 11 available video pairs, expect few patterns meeting min_frequency >= 3
- Library will grow as more videos are published and analyzed
- Current state documented in voice-patterns.json metadata

---
*Phase: 12-voice-fingerprinting*
*Completed: 2026-01-29*
