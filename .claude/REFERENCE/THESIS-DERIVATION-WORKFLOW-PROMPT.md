# Thesis Derivation Workflow Prompt

**Purpose:** Apply Rule 36 (Walk-Away Test) to any video project — derive the single-sentence thesis, audit candidates against voice, lock a closing line, and update project metadata. Born from the Tripoli Article 11 (project 51) workflow on 2026-04-27.

**Canonical methodology:** `.claude/REFERENCE/THESIS-DISCIPLINE.md` — universal 9-step throughline-finding procedure shared by script-writer-v2 (Rule 36) and article-writer (Rule 21). This workflow is the operator-invocable wrapper that applies that methodology to a specific project.

**How to use:** start a new Claude Code chat in the same repo. Paste the block below. Replace `{{PROJECT_FOLDER}}` with the project path (e.g., `video-projects/_IN_PRODUCTION/44-bakassi-peninsula-2026`) and `{{NOTEBOOK_ID}}` with the project's NotebookLM ID (find it in the project's `PROJECT-STATUS.md`).

---

## PASTE-READY PROMPT BLOCK

```
You are working on the History vs Hype YouTube channel repo. Apply Rule 36 (THESIS THROUGH-LINE) to a single video project. Your goal: derive a ≤12-word thesis, audit candidates against the creator's voice, lock the closing line, and update the project's metadata files.

PROJECT TO WORK ON: {{PROJECT_FOLDER}}
NOTEBOOKLM ID FOR THIS PROJECT: {{NOTEBOOK_ID}}

—————————————————————————————
PHASE 0 — Read the rules
—————————————————————————————

Before doing anything else, read these files. They are the rules. Do not skip.

1. .claude/agents/script-writer-v2.md — read Rule 36 (THESIS THROUGH-LINE) and Rule 32F.2b (visual Chekhov's gun). Both are in Tier 2.
2. .claude/REFERENCE/SCRIPT-TO-DELIVERY-LESSONS.md — read Lessons 25–32 (Tripoli rough-cut findings, including the Walk-Away Test).
3. .claude/REFERENCE/WRITING-VOICE-AND-STYLE.md PART 1 (Core Voice) — read the full part. This is the single source of truth for voice match. §1.4 (Sentence rhythm and the stumble test) and §3.1/§5.5 (Closings) are the most important.
4. .claude/REFERENCE/NOTEBOOKLM-SCRIPTWRITING-PROMPTS.md — read Use Case 18 (Thesis Articulation Check). You will run a variant of this against the project's notebook.
5. C:\Users\Benoi\.claude\projects\D--History-vs-Hype\memory\feedback-rough-cut-instincts.md — read the 8 instincts. They are the voice rules that govern candidate audit.
6. {{PROJECT_FOLDER}}/PROJECT-STATUS.md — current state of this project.
7. {{PROJECT_FOLDER}}/01-VERIFIED-RESEARCH.md — the verified evidence base.
8. {{PROJECT_FOLDER}}/02-SCRIPT-DRAFT.md (if exists) — current script.
9. Any rough-cut SRT in {{PROJECT_FOLDER}}/ if filming has happened.

—————————————————————————————
PHASE 1 — Detect project stage
—————————————————————————————

Determine the project's stage by reading PROJECT-STATUS.md and checking what files exist:

- STAGE A — Pre-script: 01-VERIFIED-RESEARCH.md exists, 02-SCRIPT-DRAFT.md does NOT exist. Thesis must be locked BEFORE script-writing begins.
- STAGE B — Post-script, pre-film: both research and script exist; no rough-cut SRT. Thesis lock either confirms current closing or proposes targeted script revisions.
- STAGE C — Post-film, pre-edit: research, script, AND a rough-cut SRT all exist. Thesis lock works within the constraint of what's already on tape (per Tripoli workflow). Use VO pickup if needed.
- STAGE D — Archived/published: research and final cut exist. Thesis derivation here is for sequel planning or retroactive learning, not for editing this video.

State the detected stage at the start of your response.

—————————————————————————————
PHASE 2 — Run NotebookLM Round 1: 5 thesis candidates
—————————————————————————————

Use the mcp__notebooklm__notebook_query tool against {{NOTEBOOK_ID}}. The prompt to run is the verbatim Use Case 18 prompt from NOTEBOOKLM-SCRIPTWRITING-PROMPTS.md, customized with this project's research.

Embed in the prompt:
- The case in 1-2 sentences (drawn from PROJECT-STATUS.md's "One-line pitch")
- The 3-5 strongest evidence points from 01-VERIFIED-RESEARCH.md (NOT all of them — just the spine)
- The list of sources actually uploaded to the notebook (find this in PROJECT-STATUS.md's NotebookLM section, or query the notebook itself with mcp__notebooklm__notebook_get)

Require the notebook to produce 5 candidates. Each must include:
1. Thesis sentence (≤12 words). Must be a CLAIM, bigger than the case, falsifiable.
2. Thesis type: power-asymmetry / time-shifted-meaning / system-as-designed / mechanism-over-narrative / invisible-until-named.
3. Single anchoring evidence passage (verbatim with page number from notebook sources).
4. Hook tee-up sentence (≤20 words, promises the question whose answer is the thesis).
5. Turn evidence — what evidence at 15–25% runtime makes the audience start FORMING the thesis themselves.
6. Closing line — exactly ≤12 words, anchored to a named artifact in the video, NOT an abstraction.

Plus a "what the notebook does NOT support" coda — name 1-2 candidate framings that the evidence cannot carry.

Save the raw output verbatim to {{PROJECT_FOLDER}}/THESIS-CANDIDATES-NLM.md.

Then ask the user: "Read the 5 candidates. Tell me where your instincts point. I'll share my read after."

WAIT for the user's pick before proceeding. Do not advance.

—————————————————————————————
PHASE 3 — Audit and lock the thesis
—————————————————————————————

When the user picks a candidate, AUDIT it honestly:

- Does the closing line anchor to a NAMED ARTIFACT (per Lesson 31)?
- Does the line use voice-matched register per WRITING-VOICE-AND-STYLE.md PART 1? (Hard rules: no staccato fragments for dramatic effect; no "and that's the real story" energy; no academic abstractions like "ideological architectures"; YES to longer flowing sentences with subordinate clauses, "But for X years..." pivots, three-adjective lists.)
- Does the thesis type pass the Universality Test? (The same sentence should plausibly caption ≥1 unrelated case in the channel pipeline.)

If any audit check fails, propose a voice-matched rewrite that preserves the thesis but fixes the voice issue. Do not silently fix without flagging.

Then ask the user to confirm the lock OR push for another notebook round.

—————————————————————————————
PHASE 4 — Apply to the project (branches by STAGE)
—————————————————————————————

STAGE A (pre-script): Add the thesis + thesis type to the SCRIPT METADATA block of a fresh 02-SCRIPT-DRAFT.md. The script-writer-v2 agent will use this to generate v1.

STAGE B (post-script, pre-film): Audit the existing 02-SCRIPT-DRAFT.md against the locked thesis. Check that the hook tees it up, the turn or 2nd hook makes it felt, and the closing lands it. If any of the 3 slots fail, propose a targeted script revision for that slot only — do not rewrite the whole script.

STAGE C (post-film, pre-edit): Run the Tripoli workflow.
- Compare the rough-cut closing audio to the locked thesis. If they don't align:
  - Run NotebookLM Round 2 for closing-line candidates that pair with what's already on tape. Save to CLOSING-LINE-CANDIDATES-NLM.md.
  - Audit candidates against WRITING-VOICE-AND-STYLE.md PART 1. Surface honest verdicts (which are reject-on-voice, which are salvageable). If round 2 drifts academic, run Round 3 with sharper voice constraints. Save each round to its own file.
  - When user locks a closing line, write EDIT-PLAN-THESIS-LOCK.md with: KEEP/CUT operations against the SRT (real video timestamps, accounting for any SRT timecode offset), VO pickup line + booth instructions, B-roll alignment, lower-third specs for any moved citations, runtime delta calculation.
  - Identify any HTML asset modifications needed (e.g., highlighted-state stills for graphic crossfades).

STAGE D (archived/published): Write a one-pager memo proposing how this thesis informs a sequel video or retroactive description-and-thumbnail revision. Do not modify the published video's existing files.

—————————————————————————————
PHASE 5 — Update metadata
—————————————————————————————

Once the thesis (and closing line, for stages B/C) is locked, update these files:

1. {{PROJECT_FOLDER}}/PROJECT-STATUS.md — add a "Locked thesis (YYYY-MM-DD)" section above "Locked packaging." Include thesis sentence, thesis type, Walk-Away Test result with universality cases, locked closing line (if applicable), closing structure summary with timestamps, decision trail pointing to the candidate files.

2. {{PROJECT_FOLDER}}/02-SCRIPT-DRAFT.md — at the top metadata block, add:
   - **Thesis (Rule 36, ≤12 words):** [verbatim]
   - **Thesis Type:** [type]
   - **Walk-Away Test:** PASSED — [universality cases]
   - **Locked closing line:** [verbatim, only for stages B/C]
   For stage C, also update Beat 6 with the precise edit cues (timestamps, lower-thirds, graphic states).

3. {{PROJECT_FOLDER}}/YOUTUBE-METADATA.md — replace the description's first paragraph with a thesis-anchored opening. Keep keyword anchors (head term within first 15 words) but lead with the thesis hook, not the case-summary opening. The publish skill says: "First line = thesis/hook, NOT generic topic."

—————————————————————————————
PHASE 6 — Sequel seed (optional, do not execute without user OK)
—————————————————————————————

Identify whether this thesis is a strong sequel candidate. A thesis qualifies if:
- It's universally applicable (same sentence captions ≥3 distinct cases in the channel's research pipeline or backlog)
- The channel doesn't already have a sequel-pattern series that subsumes it

If yes, propose to the user: "Plant this as a sequel seed in channel-data/TOPIC-PIPELINE.md or as a 999.x backlog item via /gsd-add-backlog?" Do not execute without explicit user OK.

—————————————————————————————
HARD RULES (do not violate)
—————————————————————————————

- Never propose a thesis without verifying its anchor evidence is verbatim in the project's notebook or 01-VERIFIED-RESEARCH.md.
- Never silently fix voice issues. If a candidate violates WRITING-VOICE-AND-STYLE.md PART 1, flag it explicitly and propose the rewrite. The user has explicitly rejected silent corrections.
- Never collapse two distinct thesis candidates into one because they sound similar — surface both and articulate the difference.
- Three options max for any branching question. Different ANGLES, not synonyms.
- After each major step, output: ✅ [what was completed]
- If the user pushes back on an audit verdict, defend with WRITING-VOICE-AND-STYLE.md PART 1 citations or notebook evidence. Do not flip on pushback alone.
- Stop conditions: do not modify any file outside {{PROJECT_FOLDER}}/ except .claude/REFERENCE/ files for read-only access. Do not push to git. Do not run /publish, /preflight, or any other channel skill without explicit user OK.

OUTPUT FORMAT

Each phase produces a brief status line + the artifact written. Do not narrate at length. Save artifacts to disk; do not paste them into chat unless the user asks.
```

---

## How to invoke this in a new chat

1. Open a new Claude Code chat in this repo.
2. Copy the prompt block above (everything between the triple-backticks).
3. Replace `{{PROJECT_FOLDER}}` with the target project path (e.g., `video-projects/_IN_PRODUCTION/44-bakassi-peninsula-2026`).
4. Replace `{{NOTEBOOK_ID}}` with the project's NotebookLM UUID (in PROJECT-STATUS.md under the NotebookLM section).
5. Paste and send.

Claude (in the new chat) will read the rules, detect the stage, and walk you through the workflow with the same pause points you experienced for Tripoli (notebook output → your instincts → audit → lock → metadata).

---

## Why this prompt works

- **Self-contained:** the new chat starts with zero context, but Phase 0 forces it to read all the canonical references before doing anything. No hallucinated rules.
- **Stage-aware:** Phase 1 detects whether the project is pre-script, post-script-pre-film, post-film-pre-edit, or archived. The workflow branches to the right intervention for each stage.
- **Voice-honest:** Phase 3 mandates the audit against WRITING-VOICE-AND-STYLE.md PART 1 and explicitly rejects silent corrections. The Tripoli workflow burned three rounds of NotebookLM before getting voice right; this prompt encodes that lesson up-front.
- **User-paced:** every phase has explicit pause points where the user's instincts drive the lock. Claude doesn't run ahead and over-commit to a thesis before the user has reacted.
- **Reproduces the Tripoli artifacts:** if you re-run this on Tripoli (project 51), you'd get THESIS-CANDIDATES-NLM.md → CLOSING-LINE-CANDIDATES-NLM.md → CLOSING-LINE-CANDIDATES-NLM-R3.md → updated EDIT-PLAN-THESIS-LOCK.md / PROJECT-STATUS.md / 02-SCRIPT-DRAFT.md / YOUTUBE-METADATA.md. Same pipeline, same artifacts.

---

## Project candidates ranked by thesis-derivation value

If you want to apply this to other projects, here's a starting order based on `video-projects/_IN_PRODUCTION/`:

| Project | Stage | Why now |
|---|---|---|
| 44-bakassi-peninsula-2026 | already filmed | Mentioned in feedback memory as a project where attribution chains broke and structural contradictions emerged. A locked thesis post-hoc would clarify whether the published cut actually carries one. |
| 47-operation-legacy-2026 | likely pre-/post-script | Operation Legacy's evidence pattern (UK destroyed records, then admitted some, then revised admissions over decades) is a near-perfect fit for the Time-Shifted Meaning or Invisible-Until-Named thesis types — high probability of a strong universal thesis. |
| 41-treaty-tordesillas-2026 | pre-/post-script | Same thesis type as Tripoli (a document whose meaning was constructed centuries after signing) — natural sequel material under thesis #5. |
| 39-adwa-wuchale-2026 | pre-/post-script | Wuchale's Italian-vs-Amharic translation gap is the textbook power-asymmetry thesis (mirror of Tripoli's Arabic-English gap, but with the asymmetry running the other direction). |

Run the prompt against any of these in a new chat to get the thesis lock for that video.
