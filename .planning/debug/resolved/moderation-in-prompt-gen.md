---
status: resolved
trigger: "Moderation scoring flags should be factored into prompt generation, not just flagged in synthesis output"
created: 2026-03-16T00:00:00Z
updated: 2026-03-16T00:00:00Z
---

## Current Focus

hypothesis: prompt_generator.py has zero awareness of moderation concerns; all moderation logic lives exclusively in synthesis_engine.py which runs AFTER prompts are generated
test: Read both files and trace data flow
expecting: No moderation imports, triggers, or scoring in prompt_generator.py
next_action: return diagnosis

## Symptoms

expected: When generating VidIQ/Gemini prompts, moderation-sensitive topics (genocide, holocaust, ethnic cleansing etc.) should influence the prompt text — e.g. instructing VidIQ to suggest monetization-safe title alternatives, or telling Gemini to factor in content sensitivity for thumbnail/hook suggestions
actual: Moderation scoring only happens in synthesis_engine.py AFTER external tool responses come back; prompts sent to VidIQ/Gemini contain no moderation awareness
errors: N/A — not a crash, a design gap
reproduction: Run generate_prompts() on any script containing HIGH-risk terms (e.g. holocaust, genocide) — the output EXTERNAL-PROMPTS.md will contain no moderation guidance
started: Always — moderation was designed as synthesis-only from the start

## Eliminated

(none needed — root cause is clear from code reading)

## Evidence

- timestamp: 2026-03-16
  checked: tools/production/prompt_generator.py (703 lines)
  found: Zero references to MODERATION_TRIGGERS, _score_moderation, _SAFE_ALTERNATIVES, or any moderation concept. The file imports nothing from synthesis_engine.
  implication: Prompt generation is completely moderation-unaware

- timestamp: 2026-03-16
  checked: tools/production/synthesis_engine.py lines 51-77, 442-481, 183-185
  found: MODERATION_TRIGGERS dict (HIGH/MEDIUM/LOW), _SAFE_ALTERNATIVES dict, _score_moderation() function all defined here. Moderation scoring happens at line 185 (after synthesis, on variant titles) and lines 200-203 (on description/tags). Thumbnail blueprints also use moderation (line 494-498).
  implication: All moderation logic is post-hoc — it flags problems in output but never prevents them upstream in prompt generation

- timestamp: 2026-03-16
  checked: prompt_generator.py _build_vidiq_prompts() lines 517-581
  found: 4 VidIQ prompts (keyword research, title optimization, tag strategy, description) — none mention content sensitivity, monetization risk, or safe alternatives
  implication: VidIQ gets no guidance about avoiding demonetization-risk terms

- timestamp: 2026-03-16
  checked: prompt_generator.py _build_gemini_prompt() lines 584-653
  found: Gemini creative brief asks for hook psychology, thumbnail concepts, curiosity gap, emotional triggers — but never mentions content moderation, sensitivity, or safe framing
  implication: Gemini gets no guidance about sensitive topic handling

## Resolution

root_cause: Moderation scoring (MODERATION_TRIGGERS, _SAFE_ALTERNATIVES, _score_moderation) lives exclusively in synthesis_engine.py and is only applied AFTER external intelligence comes back. prompt_generator.py — which creates the prompts SENT to VidIQ and Gemini — has zero moderation awareness. This means the external tools are never instructed to consider content sensitivity, monetization risk, or safe alternatives when generating their suggestions. The user then gets flagged moderation issues in the synthesis output that could have been avoided if the prompts had asked for moderation-aware suggestions upfront.

fix: (not applied — diagnosis only)
verification: (not applied — diagnosis only)
files_changed: []
