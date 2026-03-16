---
status: resolved
phase: 54-external-intelligence-synthesis
source: 54-01-SUMMARY.md, 54-02-SUMMARY.md
started: 2026-03-01T00:00:00Z
updated: 2026-03-16T12:00:00Z
---

## Current Test

[testing complete]

## Tests

### 1. Generate VidIQ + Gemini prompts from a project script
expected: Running `generate_prompts()` on a project with a script (e.g., bermeja #31) produces an EXTERNAL-PROMPTS.md file in the project folder. The file contains 4 sequenced VidIQ Pro Coach prompts (Step 1-4) and 1 Gemini creative brief (Step 5), each copy-paste ready. Script context is auto-adapted — full hook/intro if short enough, topic summary if too long.
result: pass

### 2. Prompts degrade gracefully without intel.db
expected: Running prompt generation when intel.db is missing or empty still produces all 5 prompts. Competitor context section is omitted or notes "run /intel --refresh for competitor data." No crashes or errors.
result: pass

### 3. Intake parser classifies pasted VidIQ keyword response
expected: Pasting a VidIQ keyword response into `classify_paste()` returns type "keyword_data" with high confidence (>0.7). The parsed result includes extracted keyword scores and metadata.
result: pass

### 4. Intake parser classifies pasted title suggestions
expected: Pasting title suggestions from VidIQ or Gemini into `classify_paste()` returns type "title_suggestions" with reasonable confidence. Extracted titles are captured in the parsed output.
result: pass

### 5. Intake session saves to EXTERNAL-INTELLIGENCE.json
expected: After classifying one or more pastes, calling `save_session()` creates/updates EXTERNAL-INTELLIGENCE.json in the project folder. File contains session_id, timestamp, and all classified entries with parseable_ratio tracking.
result: pass
note: User wants this to happen automatically (no manual save_session call)

### 6. Synthesis engine produces 3-variant metadata package
expected: Running `synthesize()` with a populated EXTERNAL-INTELLIGENCE.json produces a METADATA-SYNTHESIS.md file with 3 distinct variants: Variant A (Keyword-Optimized), Variant B (Curiosity Gap), Variant C (Authority Angle). Each variant has a title + thumbnail blueprint pairing. Plus one recommended description and one tag set.
result: pass

### 7. Content moderation scoring flags trigger words
expected: If a title, description, tag, or thumbnail concept contains sensitive terms (e.g., "Holocaust", "genocide", "massacre"), the synthesis output includes moderation risk notes (HIGH/MEDIUM/LOW) with safe alternatives. Moderation is informational — never blocks output.
result: issue
reported: "this should be taken into account when creating the prompts"
severity: minor

### 8. Thumbnail blueprints include AI-generation tagging
expected: Each thumbnail blueprint in METADATA-SYNTHESIS.md includes per-element tagging: elements marked as VidIQ image generator, Napkin AI, or manual Photoshop work. AI-generatable elements include ready-to-paste generation prompts.
result: pass
note: User prefers Gemini Nanobanana and VidIQ image creation model instead of Napkin AI

### 9. /publish --prompts flag works in Claude Code
expected: Running `/publish --prompts [project]` in Claude Code triggers the prompt generation workflow. Claude reads the publish.md command and uses generate_prompts() to produce EXTERNAL-PROMPTS.md for the specified project.
result: pass

### 10. /publish --intake flag works in Claude Code
expected: Running `/publish --intake` in Claude Code starts the intake session. Claude prompts user to paste VidIQ/Gemini responses one at a time, classifies each, confirms what was extracted, and saves to EXTERNAL-INTELLIGENCE.json.
result: issue
reported: "i would want to be able to paste all responses at once"
severity: minor

## Summary

total: 10
passed: 8
issues: 2
pending: 0
skipped: 0

## Gaps

- truth: "Moderation scoring flags should be factored into prompt generation, not just flagged in synthesis output"
  status: resolved
  reason: "User reported: this should be taken into account when creating the prompts"
  severity: minor
  test: 7
  root_cause: "prompt_generator.py has zero moderation awareness. MODERATION_TRIGGERS, _SAFE_ALTERNATIVES, and _score_moderation() live exclusively in synthesis_engine.py and are only applied after external intelligence comes back. Prompts sent to VidIQ/Gemini never instruct those tools to consider content sensitivity or monetization risk."
  artifacts:
    - path: "tools/production/prompt_generator.py"
      issue: "generate_prompts(), _build_vidiq_prompts(), _build_gemini_prompt() have no moderation context"
    - path: "tools/production/synthesis_engine.py"
      issue: "Moderation constants (lines 51-77) and _score_moderation() (lines 442-481) are trapped here"
  missing:
    - "Extract moderation constants to shared module or import from synthesis_engine"
    - "Call _score_moderation() on script text inside generate_prompts()"
    - "Thread moderation result into _build_vidiq_prompts() and _build_gemini_prompt()"
    - "Add monetization-awareness guidance to VidIQ Step 2 and Gemini creative brief when sensitivity detected"
  debug_session: ".planning/debug/moderation-in-prompt-gen.md"

- truth: "Intake session should accept all pasted responses at once instead of one at a time"
  status: resolved
  reason: "User reported: i would want to be able to paste all responses at once"
  severity: minor
  test: 10
  root_cause: "Intake is one-at-a-time by design at three levels: publish.md --intake is a sequential loop, classify_paste() scores one blob against all 5 types (bulk paste causes cross-contaminating signals), save_session() persists one result per call. No splitting or segmentation logic exists."
  artifacts:
    - path: "tools/production/intake_parser.py"
      issue: "classify_paste (line 75) is single-winner, save_session (line 159) is single-entry"
    - path: ".claude/commands/publish.md"
      issue: "--intake flow (lines 489-516) is sequential one-paste loop"
  missing:
    - "Add split_bulk_paste() using step markers from EXTERNAL-PROMPTS.md as segment boundaries"
    - "Add classify_bulk_paste() that splits then classifies each segment independently"
    - "Add save_batch() wrapper for bulk persistence"
    - "Update --intake flow in publish.md with bulk paste mode"
  debug_session: ".planning/debug/intake-batch-paste.md"
