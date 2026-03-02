---
status: testing
phase: 54-external-intelligence-synthesis
source: 54-01-SUMMARY.md, 54-02-SUMMARY.md
started: 2026-03-01T00:00:00Z
updated: 2026-03-01T00:00:00Z
---

## Current Test

number: 1
name: Generate VidIQ + Gemini prompts from a project script
expected: |
  Running `generate_prompts()` on a project with a script (e.g., bermeja #31) produces an EXTERNAL-PROMPTS.md file in the project folder. The file contains 4 sequenced VidIQ Pro Coach prompts (Step 1-4) and 1 Gemini creative brief (Step 5), each copy-paste ready. Script context is auto-adapted — full hook/intro if short enough, topic summary if too long.
awaiting: user response

## Tests

### 1. Generate VidIQ + Gemini prompts from a project script
expected: Running `generate_prompts()` on a project with a script (e.g., bermeja #31) produces an EXTERNAL-PROMPTS.md file in the project folder. The file contains 4 sequenced VidIQ Pro Coach prompts (Step 1-4) and 1 Gemini creative brief (Step 5), each copy-paste ready. Script context is auto-adapted — full hook/intro if short enough, topic summary if too long.
result: [pending]

### 2. Prompts degrade gracefully without intel.db
expected: Running prompt generation when intel.db is missing or empty still produces all 5 prompts. Competitor context section is omitted or notes "run /intel --refresh for competitor data." No crashes or errors.
result: [pending]

### 3. Intake parser classifies pasted VidIQ keyword response
expected: Pasting a VidIQ keyword response into `classify_paste()` returns type "keyword_data" with high confidence (>0.7). The parsed result includes extracted keyword scores and metadata.
result: [pending]

### 4. Intake parser classifies pasted title suggestions
expected: Pasting title suggestions from VidIQ or Gemini into `classify_paste()` returns type "title_suggestions" with reasonable confidence. Extracted titles are captured in the parsed output.
result: [pending]

### 5. Intake session saves to EXTERNAL-INTELLIGENCE.json
expected: After classifying one or more pastes, calling `save_session()` creates/updates EXTERNAL-INTELLIGENCE.json in the project folder. File contains session_id, timestamp, and all classified entries with parseable_ratio tracking.
result: [pending]

### 6. Synthesis engine produces 3-variant metadata package
expected: Running `synthesize()` with a populated EXTERNAL-INTELLIGENCE.json produces a METADATA-SYNTHESIS.md file with 3 distinct variants: Variant A (Keyword-Optimized), Variant B (Curiosity Gap), Variant C (Authority Angle). Each variant has a title + thumbnail blueprint pairing. Plus one recommended description and one tag set.
result: [pending]

### 7. Content moderation scoring flags trigger words
expected: If a title, description, tag, or thumbnail concept contains sensitive terms (e.g., "Holocaust", "genocide", "massacre"), the synthesis output includes moderation risk notes (HIGH/MEDIUM/LOW) with safe alternatives. Moderation is informational — never blocks output.
result: [pending]

### 8. Thumbnail blueprints include AI-generation tagging
expected: Each thumbnail blueprint in METADATA-SYNTHESIS.md includes per-element tagging: elements marked as VidIQ image generator, Napkin AI, or manual Photoshop work. AI-generatable elements include ready-to-paste generation prompts.
result: [pending]

### 9. /publish --prompts flag works in Claude Code
expected: Running `/publish --prompts [project]` in Claude Code triggers the prompt generation workflow. Claude reads the publish.md command and uses generate_prompts() to produce EXTERNAL-PROMPTS.md for the specified project.
result: [pending]

### 10. /publish --intake flag works in Claude Code
expected: Running `/publish --intake` in Claude Code starts the intake session. Claude prompts user to paste VidIQ/Gemini responses one at a time, classifies each, confirms what was extracted, and saves to EXTERNAL-INTELLIGENCE.json.
result: [pending]

## Summary

total: 10
passed: 0
issues: 0
pending: 10
skipped: 0

## Gaps

[none yet]
