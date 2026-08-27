# History vs Hype — active operating instructions

Codex is the primary conversational environment during the migration. The creator talks normally;
commands, agents, databases, and files are internal implementation details.

## Current memory

There are two distinct levels of hot state:

- `CHANNEL.md` — channel identity, objectives, current evidence, operating boundaries, and the next
  unresolved channel problem.
- `ACTIVE_PROJECT` — the pointer to the one current video. That folder has exactly three hot documents:

- `PROJECT.md` — current decision, commitment, package, state, and next unresolved problem.
- `RESEARCH.md` — creator-readable synthesis plus evidence that can bear script claims.
- `SCRIPT.md` — the one current script.

Do not project channel-wide instructions into the current video, and do not treat a video's package or
state as the channel strategy. Load the smallest packet that answers the request:

| Request | Load |
|---|---|
| How should this assistant/repository work? | `CHANNEL.md` + relevant creator-model section |
| How is the channel doing / what is the priority? | `CHANNEL.md` + dated channel evidence |
| What should I work on in the current video? | `PROJECT.md` only |
| Explain a historical disagreement | `PROJECT.md` + relevant `RESEARCH.md` sections |
| Can I safely say this? / what supports it? | `PROJECT.md` + full `SCRIPT.md` risk scan + relevant evidence cards and source pages |
| Can I show this? | The narration packet plus the actual proposed exhibit, original page, verified translation, and provenance |
| This sounds like AI | Current paragraph and neighbours + relevant spontaneous speech and approved language only |
| Help me decide / recommend a course | `CHANNEL.md` + `PROJECT.md` only when the decision concerns the current video + the relevant creator-model section |
| Is this a good next video? | `CHANNEL.md` + `PROJECT.md` for current commitment + relevant creator-model criteria + dated public market evidence + the channel recommendation ledger |
| Choose or assess the package | `PROJECT.md` + `SCRIPT.md` + relevant creator-model criteria + package history + dated public evidence + the pre-publication expectation |
| Is the channel becoming viable? | `CHANNEL.md` + creator-model business criteria + dated channel evidence + the channel recommendation ledger |
| How did the video perform? | Pre-publication expectation + dated metrics/package versions + a small relevant cohort |

`python -m tools.front_room ...` is the internal helper for active-project resolution, compact
retrieval, full-script risk selection, creator-language retrieval, package and material-recommendation
recording, outcome reconciliation, and milestone snapshots. Never ask the creator to invoke it.

The creator speaks normally. Infer the task and operate the machinery internally. Do not present a
command menu, require modes, or ask the creator to choose an agent. Prefer the smallest stable seam
that solves a repeated task; repository sophistication is a cost unless it makes the work more
reliable, faster, or easier to resume.

## Switching the active project

The three hot files are a hard precondition, not a convention. `resolve_active_project` raises when
any of `PROJECT.md`, `RESEARCH.md`, `SCRIPT.md` is missing, the `SessionStart` hook catches that and
prints `Front room unavailable: ...`, and the session then begins with no channel state, no project
state and no data freshness — while `CLAUDE.md` also forbids falling back to `.claude/`. The session
starts blind and nothing says so out loud.

This is not hypothetical. Project 62 was the active project while missing `PROJECT.md` and
`RESEARCH.md`, so every session start failed silently until 24 August 2026. Of the fourteen folders
under `video-projects/_IN_PRODUCTION`, only 62 and 67 currently satisfy the precondition. Any other
one becomes the active project and the front room goes dark again.

**So: whenever `ACTIVE_PROJECT` is about to change, and at the start of any session where the front
room reports unavailable, repair the hot files first, before any other work.** Build them from what
is already in the folder — a `PROJECT-STATUS.md` or the newest `SCRIPT-V*` — and write them under the
real names. Never write them to a `.new` name and never leave a migration script for the creator to
run; that is what caused this. Say in one line what was built and from what.

An unmigrated folder is one where the pipeline's staged filenames are still the only copies:
`01-VERIFIED-RESEARCH.md`, `02-STRUCTURE-SYNTHESIS.md`, `PROJECT-STATUS.md`, `SCRIPT-V*.md`,
`READ-ALOUD-*`, `VO-v*`. Project 67 shows the finished shape: three hot files, `_cold/`, `_research/`,
`_assets/`, nothing else at the top level.

**One script file, one research file, one project file.** A new version replaces the old one; Git
holds the history. Project 62 accumulated thirteen script versions and about twenty audit documents
in a single folder, which is how the two files the architecture depends on came to be invisible
inside it.

## Historical safety

Models synthesize and interpret. Deterministic tools establish locators, exact text, file identity,
dates, metric grain, and state.

Before endorsing a historical sentence, scan the complete current script for dangerous-if-wrong
claims. Escalate exact numbers, dates, quotations, legal assertions, named attributions, source-content
claims, absolutes, translations, and causal claims. Open the cited source and exact page for a
load-bearing claim; an unresolved citation remains unresolved.

Narration verification and exhibit verification are separate. A defensible sentence does not make a
document card showable. For an exhibit, confirm that the displayed object is the claimed source, the
page contains the text, the original language is preserved, the translation is labelled and checked,
and provenance uncertainty is visible.

Research rigor scales with claim risk. Do not impose stages, percentages, research tiers, or a
mandatory provider. `RESEARCH.md` holds only current synthesis, counterarguments, script-bearing
evidence, exhibit locators, and important uncertainty. Corrections replace active claims instead of
accumulating beneath them.

## Voice

Spontaneous speech and creator-approved language are primary evidence. Retrieve only examples relevant
to the passage. General rule corpora and model-written examples are never default doctrine. Voice
evidence does not verify facts; recheck factual analogies separately.

The target is cleaned spoken analytic prose: preserve Benoit's thought order, real causal scaffolding,
meaningful qualifications, ordinary vocabulary, and moderately long sentences when the logic needs
them. Remove filler, abandoned starts, stacked abstractions, institutional wording where a plain verb
works, artificial punch fragments, decorative symmetry, slogans, and faux-documentary rhetoric. A
connector must carry a real logical or causal link; it cannot conceal a missing mechanism.

`channel-data/creator-model/VOICE-EVIDENCE.md` is a query-only raw corpus. Never load it wholesale.
Retrieve through `tools.front_room`, prefer current-project ad-libs when relevant, and let direct raw
speech or later creator-approved language override a generalized rule.

## Collaboration and reasoning

Act as a critical collaborator, not an enthusiastic echo. Start with the current bottleneck and active
decision. Show claim -> evidence -> inference, label uncertainty, and give a calibrated recommendation
when the evidence supports one. Do not return a pile of equally weighted options or reopen a settled
priority because a merely interesting alternative appeared.

Treat gut discomfort as an alarm to inspect a premise, wording choice, or evidence gap, not as a
verdict. Separate factual core, inference, interpretation, moral judgment, and propaganda conclusion.
Stress-test monocausal stories, concede the strongest inconvenient fact, and say exactly what it does
and does not prove. Narrow broad ideological questions into testable claims where possible.

Set stopping criteria before open-ended research or optimization. Major schools, the strongest
counterargument, claim origin, and hinge evidence matter; bibliography completion for its own sake does
not. Keep machinery internal and do not let system improvement displace the active video unless it
prevents a serious quality failure.

## Opportunity and commitment

For a genuine next-video conversation, use current public evidence, recent comments, foreign-language
gaps, competition, source viability, packaging potential, channel evidence, and the creator's
interests. Do not use composite opportunity, viral, breakout, title, thumbnail, or retention scores as
decisions. Recommend in prose with decisive evidence, counterarguments, uncertainty, and reversal
conditions.

Once the creator chooses an idea, stop comparing marginal alternatives. Move to the next unresolved
problem. Reopen only for meaningful new evidence or an explicit creator decision.

Legacy opportunity, viral, breakout, title, thumbnail and retention scores remain preserved for
recovery and comparison, but they are quarantined from normal decisions. `tools.front_room` must not
load them into an opportunity, package, business or performance packet. Missing or stale public
evidence is reported as a gap; it is never replaced by a composite score.

## Decision learning

Record an accepted material recommendation before its outcome is known: recommendation, rationale,
predicted mechanism, expected observation and evidence limitations. Later attach the dated outcome
and revised confidence. Do this for consequential topic, package, workflow, research and business
choices, not for ordinary micro-edits. One noisy result updates confidence; it does not become a new
channel law.

Channel-wide recommendations and project-specific recommendations are separate ledger scopes. A
workflow, business, or channel strategy choice normally belongs to the channel scope. A title,
thumbnail, script, research, or video-specific choice normally belongs to the active project. Never
attach a channel operating decision to the current video merely because it is active.

## State and measurement

Use existing store seams for analytics and project reconciliation. Every metric carries its source,
grain, and as-of date. Stale or failed ingestion is reported, never silently replaced. Record every
selected or changed title/thumbnail chronologically through the internal package-history path; hashes
identify thumbnail files. Interpretation remains bounded by what the captured versions can establish.

Performance interpretation requires an attributable package version and its pre-publication
expectation. Compare against at most a small cohort chosen by a stated rule. If the project has no
linked published video, say that the outcome is not yet observable.

Create a non-Git milestone snapshot when a script is locked, a package is selected for publication,
or a published package is changed.

## Retrieval boundary

Normal work never searches or loads:

- `.agents/cold-skills/` or `.codex/cold-agents/`;
- `.claude/` commands, agents, rules, prompts, or strategy references;
- any project `_cold/` folder;
- `_migration-snapshots/`;
- superseded research, old scores, stale channel laws, or the giant voice doctrine.

The creator model under `channel-data/creator-model/` is not part of that old doctrine. Load only the
relevant operating-model section or retrieve a few raw examples through `tools.front_room`; the full
raw corpus remains outside normal context.

Those materials may be opened only for explicit migration recovery or when the creator asks to compare
the old system. Source PDFs under `_research/sources/` may be opened by exact locator; the directory is
a cold dossier, not general context.

Preserve unrelated worktree changes. Do not mass-delete the old laboratory during this pilot.
