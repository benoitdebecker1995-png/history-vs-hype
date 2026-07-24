---
name: "source-command-refactor"
description: "Run the next eligible step in UPGRADE-PLAN.md (one step, then stop)"
---

# source-command-refactor

Use this skill when the user asks to run the migrated source command `refactor`.

## Command Template

# /refactor

Executes exactly **one** step from `/UPGRADE-PLAN.md` — the first `[TODO]` step whose dependencies are all `[DONE]` — then commits and stops.

> **Plan target history:** originally ran `REFACTOR-PLAN.md` (47/47 done, archived at `docs/archive/REFACTOR-PLAN.md` 2026-06-12). Now targets `UPGRADE-PLAN.md`. An explicit argument overrides: `/refactor <plan-file>`.
>
> **`[INTERACTIVE]` steps:** UPGRADE-PLAN marks some steps `[INTERACTIVE]` (grill sessions, approval walks). Only run those when the user is live in the session; from a phone fire-and-forget context, skip to the next non-interactive eligible step and report the skip.

Designed for phone use: fire the command, one atomic change lands, you decide when to fire the next one.

## What this command does

1. Read `/UPGRADE-PLAN.md` from the repo root.
2. Find the first step marked `[TODO]` whose every dependency (per the step's `Deps:` line and the dependency map at the top of the file) is `[DONE]`.
3. Execute that step's `**Prompt:**` block **exactly** — no improvisation, no scope creep.
4. Run the step's `**Verify:**` command. If it fails, abort per the failure protocol below.
5. Edit `UPGRADE-PLAN.md`: flip that step's `[TODO]` → `[DONE]` and update the `Last advanced` line in the Status Tracker to today's date + step ID.
6. Stage all touched files plus `UPGRADE-PLAN.md`.
7. Commit using the step's `**Commit:**` message verbatim.
8. **Stop.** Do not advance to the next step. Do not push to remote.

## Strict rules for this command

- **One step per invocation.** No matter how easy the next step looks, stop after one commit.
- **No scope creep.** If you spot something else broken (typo, dead import, "while I'm here"), record it in the `Drift log` section at the bottom of `UPGRADE-PLAN.md` and continue with the assigned step only.
- **Verify is non-negotiable.** If the `Verify:` block fails, do NOT mark `[DONE]`. Mark `[DOING]`, write what failed under `Drift log`, commit any work-in-progress with message `WIP: <step-id> verify failed — see drift log`, then stop and report.
- **No push.** Never run `git push`. Local commit only.
- **Don't touch unrelated paths.** `.Codex/`, `video-projects/`, `channel-data/`, `library/`, `transcripts/`, `research/` are off-limits unless the step explicitly references them.
- **Don't ask for clarification on the step's intent.** The Prompt block is the spec. If it's truly ambiguous, mark the step `[BLOCKED]`, write the question in the step's body in `UPGRADE-PLAN.md`, commit just the file edit, and stop.

## Procedure

### Step 1 — Read the plan

```
Read /UPGRADE-PLAN.md in full.
```

### Step 2 — Pick the next eligible step

Walk steps in order. The first one matching ALL of these is the target:

- Status is `[TODO]` (not `[DOING]`, `[DONE]`, or `[BLOCKED]`)
- Every step listed in its `Deps:` line is `[DONE]`

Edge cases:
- **A `[DOING]` step exists.** That's an interruption marker from a previous session. Report: `[DOING] step <ID> from prior session — review and either complete or roll back to [TODO] before running /refactor again.` Then stop. Do nothing else.
- **The next-eligible step has unmet deps.** Skip it; it should already be `[BLOCKED]`. If it isn't, mark it `[BLOCKED]` and continue searching for the next eligible step.
- **No eligible step found.** Either everything is `[DONE]` (report `All steps complete.`) or every remaining step is `[BLOCKED]` (report which deps are missing). Stop.

### Step 3 — Execute the Prompt block

Read the step's `**Prompt:**` fenced block. Execute it as if it were a direct instruction, with one modification: **do not let it instruct you to mark itself `[DONE]` or commit** — that's this command's job in steps 5–7. Do everything else the prompt says.

If the prompt produces files outside the documented scope, abort and report.

### Step 4 — Verify

Run the step's `**Verify:**` block. Treat any non-zero exit code, failed assertion, or unexpected output as failure.

**On verify failure:**
1. Edit `UPGRADE-PLAN.md`: change that step's status to `[DOING]`.
2. Append to `Drift log` (last section of the file): `### <step-id> failed verify on <date>` followed by a 2-3 sentence description of what failed.
3. Stage everything currently changed.
4. Commit: `WIP: <step-id> verify failed — see drift log`.
5. Stop. Report the failure to the user in 2 sentences.

### Step 5 — Mark done

Edit `UPGRADE-PLAN.md`:
- Change the step's `## <ID> [TODO]` heading to `## <ID> [DONE]`.
- Update the Status Tracker: change `Last advanced: <prev>` to `Last advanced: <YYYY-MM-DD> (<step-id>)`. Also increment the `Done:` count by 1.

### Step 6 — Commit

```bash
git add -A
git commit -m "<exact commit message from the step's Commit: line>"
```

Do **not** add `Co-Authored-By` or any extra body — keep the commit message exactly as specified by the step. The plan's commit messages are designed to be greppable.

### Step 7 — Stop

Report in 1-2 sentences:
- Which step ran
- Commit hash (last 8 chars)
- What's next eligible (just the ID and one-line title)

Do not run another step. Do not offer to. The user fires `/refactor` again when ready.

## Failure / abort protocol

If at any point you can't proceed (missing dep, ambiguous instruction, tool error, repo in unexpected state, uncommitted changes blocking work):

1. Do NOT mark the step `[DONE]`.
2. Edit `UPGRADE-PLAN.md`: mark the step `[BLOCKED]` and add a `> **Blocker:** <description>` line directly under the step heading.
3. Commit just the plan file: `git add UPGRADE-PLAN.md && git commit -m "refactor: block <step-id> — <one-line reason>"`.
4. Report the blocker to the user. Stop.

## Sanity check before starting

Before reading the plan, verify the working tree is clean:

```bash
git status --porcelain
```

If output is non-empty, report `Working tree dirty — commit or stash before /refactor` and stop. The plan's atomic-commit guarantee depends on starting from a clean tree.

## Related

- The plan itself: `/UPGRADE-PLAN.md`
- Plan provenance: interview + grill session 2026-06-12 (`~/.Codex/plans/quizzical-gliding-goblet.md`); grill resolutions baked into UPGRADE-PLAN.md § "Why this plan exists"
- Predecessor: `docs/archive/REFACTOR-PLAN.md` (audits `.planning/audits/48-53`, all done except F4 → tracked as UPGRADE-PLAN T1)
