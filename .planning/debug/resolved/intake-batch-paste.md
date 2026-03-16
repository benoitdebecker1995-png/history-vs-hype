---
status: resolved
trigger: "Intake session should accept all pasted responses at once instead of one at a time"
created: 2026-03-16T00:00:00Z
updated: 2026-03-16T00:00:00Z
---

## Current Focus

hypothesis: The intake flow is one-at-a-time by design - both the command protocol and the classify_paste function assume a single response type per paste
test: Read classify_paste and publish.md --intake flow
expecting: No batch/splitting logic exists
next_action: return diagnosis

## Symptoms

expected: User pastes all 5 VidIQ/Gemini responses at once, system auto-splits and classifies each
actual: System prompts for one paste at a time in a loop (paste -> classify -> confirm -> next paste -> done)
errors: N/A (not a crash, a UX friction issue)
reproduction: Run /publish --intake, observe one-paste-at-a-time loop
started: Always been this way - original design

## Eliminated

(none - root cause identified on first pass)

## Evidence

- timestamp: 2026-03-16
  checked: tools/production/intake_parser.py - classify_paste function (lines 75-135)
  found: classify_paste takes a single text string and scores it against ALL 5 types simultaneously, returning only the single best-scoring type. There is no concept of splitting input or detecting multiple response types within one paste.
  implication: The function is fundamentally single-type-per-call

- timestamp: 2026-03-16
  checked: .claude/commands/publish.md - --intake session flow (lines 489-516)
  found: The documented flow is an explicit loop: (1) prompt for paste, (2) classify, (3) show preview, (4) confirm, (5) save, (6) prompt for next or "done". Each iteration handles exactly one response type.
  implication: The command protocol enforces one-at-a-time by design

- timestamp: 2026-03-16
  checked: intake_parser.py - signal patterns and scoring (lines 38-73, 211-259)
  found: Each response type has distinct regex signals (keyword_data has volume/competition patterns, title_suggestions has numbered lists, etc.). These signals are type-specific enough that a bulk paste containing multiple response types would confuse the scorer - signals from different types would all fire, and the "best score wins" logic would pick one type for the entire paste.
  implication: classify_paste would misclassify a bulk paste because signals from multiple types would cross-contaminate

- timestamp: 2026-03-16
  checked: intake_parser.py - save_session (lines 159-204)
  found: save_session saves exactly one classified result per call. No batch save capability.
  implication: Even if splitting worked, persistence is also single-item

## Resolution

root_cause: |
  The intake flow is one-at-a-time by design at THREE levels:
  1. **Command protocol** (publish.md lines 495-501): The --intake session flow is a sequential prompt/paste/confirm loop
  2. **classify_paste function** (intake_parser.py line 75): Takes one text blob, scores against all 5 types, returns single best match. A bulk paste with multiple response types would have cross-contaminating signals making classification unreliable.
  3. **save_session function** (intake_parser.py line 159): Saves one classified result per call, no batch support.

  There is NO splitting/segmentation logic anywhere. The system has no way to detect where one response ends and the next begins within a single paste.

fix: (not applied - diagnosis only)
verification: (not applied)
files_changed: []
