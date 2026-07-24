# Topic notes are derived, and only quotations may be quoted

**Date:** 2026-07-22
**Status:** accepted

Research in this repo has always been filed **per video**. Each project owns a
`01-VERIFIED-RESEARCH.md`, and that file is the single source of truth for its
episode. The consequence went unnoticed for 30 episodes: nothing accumulates
*across* episodes. `.brain/sources/` and `.brain/threads/` were specified in
`.brain/README.md` and sat at **zero files**; `graphify-research` stayed at ~110
sparse nodes because the only thing it had to chew on was 16 episode-shaped
dossiers. Episode N+1 costs the same as episode N.

This ADR introduces `.brain/topics/` — the same verified claims re-filed by
**concept** — and fixes the two rules that keep it trustworthy.

## The decision

**1. `.brain/topics/` and `.brain/sources/` are fully derived. Never hand-edit.**

`tools/brain/topic_mine.py` regenerates both directories from
`.brain/topics/_extracted/*.json`, deleting stale notes on every build. The
truth source remains `01-VERIFIED-RESEARCH.md` — a correction goes upstream into
the dossier and is re-mined, never patched into a topic note. `.brain/threads/`
is the opposite and stays hand-written: it holds *our* synthesis, the argument
layer, and the miner does not touch it.

This completes the source / topic / argument split across three existing roots:

| Layer | Root | Authorship |
|---|---|---|
| Source — what they said | `.brain/sources/` | derived |
| Topic — claims by concept | `.brain/topics/` | derived |
| Argument — what we say | `.brain/threads/` | hand-written |

**2. Extraction is bulk-read work; it may COPY but never AUTHOR.**

Mining 1 MB of dossiers is dispatched to Gemini Flash per the standing
bulk-read routing. That is only safe because the model is not trusted: every
`verbatim` field is validated in code as an exact substring of the originating
dossier (`normalize()` folds smart quotes, dashes and markdown emphasis —
formatting only, never words). A reworded, "repaired", or hallucinated quote
fails the match, is stripped, and is logged to `_rejected.jsonl`. Every `source`
must already appear in the dossier, or the claim is dropped. This satisfies the
historian skill's web/Gemini verbatim ban structurally rather than by trusting a
prompt.

**3. An exact-substring match proves provenance, not utterance.**

This is the subtle one, and it was wrong in the first implementation. A verbatim
that matches the dossier may still be the dossier's *own summarising prose* —
`Ratified by Adams: June 10, 1797` is a research note, not something anyone
said. Rendering it inside quote marks would manufacture a quotation that no
source ever uttered: exactly the failure `/verify` 7.8 and the `primary-source`
skill exist to catch, arrived at from a new direction. So claims carry two
distinct booleans:

- `verbatim_verified` — the text is provably from the dossier.
- `verbatim_is_quote` — the dossier itself presents it as a quotation (a `>`
  blockquote line, or a quote-wrapped run).

**Only `verbatim_is_quote` text is ever rendered inside quote marks**, in topic
notes and source notes alike. Verified prose keeps its claim and drops its
quotes entirely rather than being laundered into one.

**4. Concept vocabulary is authored, not inferred.**

Extraction invents a fresh slug per dossier, so the raw vocabulary explodes
(~120 slugs from a single 53-claim file). `_taxonomy.json` maps aliases to
canonical concepts and is written **by hand**. Deciding that
`colonial-boundary-inheritance` and `uti-possidetis-juris` are one idea is the
editorial judgment the whole exercise exists to produce; automating it would
re-create the sprawl it is meant to fix. Unmapped slugs render as
`status: provisional` with a banner, and the index lists them separately — they
are visible debt, not silent guesses.

## Considered alternatives

- **Adopt Obsidian.** Rejected. The system this is modelled on ships as an
  Obsidian vault, but the notes here are markdown-on-disk with wikilinks and a
  graph layer already — adopting Obsidian would add a fourth knowledge home next
  to the dossiers, NotebookLM, and graphify without adding a capability. The
  transferable part was the filing discipline, not the software.
- **Regex-parse the dossiers instead of using a model.** Rejected on evidence:
  of 30 dossiers, exactly one uses the `### F<N>` convention. Heading structure
  is genuinely heterogeneous, so a parser would silently under-collect.
- **Trust the model's verbatims and spot-check.** Rejected. The first run
  stripped 15 of 52 quotes; all 15 turned out to be markdown-formatting drift,
  but the guard is what let us know that rather than assume it.
- **Let the extractor own the concept vocabulary.** Rejected — see 4.
- **Hand-write topic notes.** Rejected as the *starting* move: 30 dossiers is a
  backfill, not an authoring task. Hand-writing resumes at the argument layer,
  which is where judgment actually pays.

## Consequences

- `python -m tools.brain.topic_mine build` is safe to re-run at any time and is
  the only supported way to change `.brain/topics/` or `.brain/sources/`.
- New episodes are mined by re-running `extract`; the miner skips dossiers that
  already have an extraction unless `--force` is passed.
- **Re-litigation guard:** a future pass that finds verified claims rendered
  without quote marks and offers to "restore the quotes" should be answered with
  §3. The quotes were not lost; that text was never a quotation.
- `.brain/README.md` gains `topics/` in its root table, and its "what lives
  elsewhere" contract is unchanged.
