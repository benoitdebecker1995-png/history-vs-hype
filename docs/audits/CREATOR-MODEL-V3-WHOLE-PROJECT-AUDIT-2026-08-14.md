# Creator model v3 — whole-project audit

Date: 14 August 2026

## Verdict

Before correction, the repository did not reliably match Benoit's intended YouTube assistant. The
creator model had been imported, but the live architecture still mixed it with a command-driven legacy
system and incorrectly anchored channel-wide decisions to the current Donation of Constantine video.

The active path now matches the intended model in its core behavior: ordinary conversation is the
interface; channel state and current-video state are separate; creator speech is retrieved selectively;
historical claims and exhibits retain explicit verification requirements; and recommendations are
recorded with evidence, prediction, outcome, and scope rather than decided by composite scores.

The physical repository still contains a large legacy laboratory. It is preserved for recovery, not
treated as active doctrine. This audit does not claim that every old document has been rewritten.

## Audit boundary

Inspected the live assistant entrypoints, root state files, Codex hooks, creator-model import,
front-room retrieval and routing, recommendation/package/analytics seams, current active project,
tests, and the non-cold channel-data surface.

Per the active retrieval boundary, the audit did not load `.claude/`, `.agents/cold-skills/`,
`.codex/cold-agents/`, project `_cold/` folders, `_migration-snapshots/`, or source dossiers without an
exact locator. Their existence was checked only as legacy surface, not interpreted as current policy.

## Findings and corrections

### 1. Conversational interface — corrected

The old root entrypoints required slash commands, named agents, manual handoffs, fixed workflow gates,
and a “Calm Prosecutor” doctrine. `CLAUDE.md`, `GEMINI.md`, `START-HERE.md`, and `HANDOFF.md` are now thin
conversational adapters to the shared contract. The old `.claude/` system remains preserved but is
outside normal retrieval.

### 2. Channel and video state — corrected

Previously, `ACTIVE_PROJECT` and its `PROJECT.md` were the only hot state. This caused a repository-wide
creator model and channel strategy to be interpreted as instructions for the Donation video.
`CHANNEL.md` now holds channel identity, goals, current evidence, operating boundaries, and the current
channel problem. The active video's three hot documents remain independent.

### 3. Creator model coverage — corrected

The imported operating model already covered identity, voice, reasoning, historical method, research,
commitment, experimentation, growth, packaging, and collaboration. It now also captures the repository
requirements present in Benoit's raw speech: normal chat as the interface, invisible machinery,
manageable sophistication, selective context, broad reversible autonomy, approval before external or
irreversible action, and fewer evidence-backed recommendations.

### 4. Voice evidence integrity — corrected

The raw voice corpus is query-only and project ad-libs outrank general examples. Locator `A2-105` was
an assistant-written audit mislabeled between creator turns; it is now excluded from voice retrieval
so it cannot teach the system to imitate its own prose.

### 5. Strategy and learning scope — corrected

The recommendation ledger previously had only a `project_slug`, so channel workflow and business
decisions could be attached to the current video. The live seam now uses an internal channel scope for
topic, workflow, and business decisions and project scope for package and research decisions unless a
different scope is explicitly required. The mistaken workflow record was moved to channel scope; the
mistaken Donation package record created during the first audit was removed.

### 6. Evidence and analytics — partially matched

The system has dated analytics, CTR, market-intelligence, package-history, and recommendation seams.
It reports missing or stale data instead of substituting a score. It does not currently track revenue,
sponsorship income, or current YouTube Partner Program eligibility counters, so it cannot yet measure
the EUR 2,000 monthly viability target directly.

### 7. Historical and exhibit safety — matched

Full-script risk selection escalates exact numbers, dates, quotations, legal assertions, named
attributions, source-content claims, absolutes, translations, causal claims, and proposed exhibits.
Narration verification remains separate from exhibit verification and requires the exact source/page,
original language, labelled checked translation, and visible provenance uncertainty where relevant.

### 8. Legacy strategy material — contained, not removed

Many old feeds, audits, score files, and command references remain under `channel-data/`, `docs/`, and
legacy folders. The active contract and front room exclude them from normal decisions, and
`channel-data/README.md` now makes that boundary explicit. A bulk cleanup would create migration risk
without improving the current conversation path, so it was not performed.

## Remaining limitations

- Financial viability cannot be measured until revenue and sponsorship evidence is connected.
- The repository's full pytest suite cannot run in the current Python environment because pytest is
  not installed; import checks, live routing checks, and the available unittest suite were used.
- Old materials can still mislead a human who deliberately opens them without reading the active
  entrypoints. They are quarantined by policy and routing, not physically removed.
- Whether the assistant genuinely reduces workload must be judged through several real channel tasks;
  architecture alone cannot prove that outcome.

## Next test

Use normal conversation for the next real channel decision or production task. The system should load
the channel model automatically, use the active video only when relevant, make one supported
recommendation, expose meaningful uncertainty, and leave the implementation machinery invisible.
