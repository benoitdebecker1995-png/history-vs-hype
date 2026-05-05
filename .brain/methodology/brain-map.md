# Brain Map — Multi-Root Knowledge Architecture

Five roots hold the project's knowledge. This doc explains what lives where, what does NOT, and who maintains each root.

## The five roots

### 1. `channel-data/` — Channel intelligence (live)

**What lives here:** Analytics, CTR baselines, POST-PUBLISH-ANALYSIS per video, competitor tracking, topic pipeline, A/B testing log, channel strategy audits, format experiments, CHANNEL_ANALYTICS_MASTER.

**What does NOT live here:** Methodology docs, verified source quotes, Claude-instruction files.

**Maintained by:** Daily routines (cloud + Desktop). Never manually reorganise — routines write to known paths.

**Key files:**
- `CHANNEL_ANALYTICS_MASTER.md` — aggregate stats
- `analyses/POST-PUBLISH-ANALYSIS-*.md` — per-video deep dives
- `TOPIC-PIPELINE.md` — greenlight candidates
- `competitor-drops/YYYY-MM-DD.md` — Routine 1 output
- `modern-relevance/YYYY-MM-DD.md` — Routine 2 output

---

### 2. `tools/benchmark/` — Playbooks (versioned)

**What lives here:** Title/thumbnail/hook formulas derived from niche-wide analysis (n=42-388). WAVE analysis outputs (1-8). Outlier corpus. Structural findings. These are durable recipes, not live data.

**What does NOT live here:** My channel's specific performance data (that's `channel-data/`). Claude prompts.

**Maintained by:** Research sprints. Versioned, not live-updated.

**Key files:**
- `THUMBNAIL-NICHE-ANALYSIS.md` — 650-thumb benchmark
- `PER-CHANNEL-THUMBNAIL-PLAYBOOK.md` — per-channel patterns
- `TITLE-TO-OVERLAY-OPERATION-MAP.md` — text overlay decisions
- `WAVE-8-SCRIPT-TECHNIQUES.md` — technique library
- `TRANSCRIPT-STRUCTURE-ANALYSIS.md` — structural patterns

---

### 3. `.brain/` — New artifacts (additive)

**What lives here:** Verified quotes by book (project-scoped, extends `~/llm-brain/wiki/quotes/`), cross-source synthesis threads, methodology docs (this file, routing, handoff), routine inbox, raw ingestion queue.

**What does NOT live here:** Anything that already has a home in `channel-data/` or `tools/benchmark/`. Don't duplicate — index them.

**Maintained by:** Routine 5 (nightly, Desktop). Manual additions via `_queue/` drop.

**Key dirs:**
- `_inbox/` — routine output (dated files, never auto-deleted)
- `_queue/` — paste raw content here, Routine 5 digests it
- `sources/` — verified quotes by book with page numbers
- `threads/` — cross-source synthesis narratives
- `methodology/` — decision docs (this file, routing, handoff)

---

### 4. `~/llm-brain/wiki/` — Cross-project methodology (global)

**What lives here:** Entities (people, places, treaties), concepts (mechanisms, frameworks), quotes by book, cross-source threads, patterns. Used across multiple projects, not History vs Hype specific.

**What does NOT live here:** Channel-specific performance data, Claude-instruction files.

**Maintained by:** `/brain-ingest`, `/brain-ingest-batch`, Routine 5 (partially). Use `~/llm-brain/wiki/index.md` as the entry point.

---

### 5. `~/.claude/projects/D--History-vs-Hype/memory/` — Behavioral memory

**What lives here:** User feedback rules, behavior corrections, channel stats snapshot, workflow observations, competitors findings, analytics patterns. Feeds Claude's context at session start.

**What does NOT live here:** Live data, methodology docs, source quotes.

**Maintained by:** Auto-memory system (Stop hooks, explicit `/remember` calls). Use `MEMORY.md` as the catalog.

---

## Decision tree: where do I put X?

```
Is it a live/daily data artifact (analytics, competitor drops, modern relevance)?
  → channel-data/  (or .brain/_inbox/ if from a routine)

Is it a niche-wide formula/playbook derived from corpus analysis?
  → tools/benchmark/

Is it a verified quote with page number from an academic source?
  → .brain/sources/<book-slug>.md  (project-scoped)
  → ~/llm-brain/wiki/quotes/<book-slug>.md  (if cross-project useful)

Is it a cross-source synthesis narrative connecting multiple sources?
  → .brain/threads/<topic-slug>.md

Is it a Claude-instruction file (prompt, template, voice guide, skill)?
  → .claude/REFERENCE/ or .claude/agents/ or .claude/commands/
  → NOT in .brain/ (those are prompts, not knowledge)

Is it a user behavior rule or feedback correction?
  → ~/.claude/projects/D--History-vs-Hype/memory/feedback-*.md

Is it a decision about the project's architecture or methodology?
  → .brain/methodology/  (e.g., routing rules, handoff playbook)

Is it an entity or concept with cross-project value (treaty, person, doctrine)?
  → ~/llm-brain/wiki/entities/ or ~/llm-brain/wiki/concepts/

Is it raw content dropped for later processing?
  → .brain/_queue/  (Routine 5 will digest it)

Unsure? Drop it in .brain/_queue/ and let Routine 5 classify it.
```
