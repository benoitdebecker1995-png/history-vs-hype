---
description: Final AI-pattern pass on a locked script before filming
model: opus
---

# /polish - Final voice pass on a locked script

Strip AI writing fingerprints from a locked script before filming. Eliminates staccato fragments used as flourish, decorative metaphors, redundant restatements, vague meta-transitions, and attribution slips. Verifies thesis throughline and viewer-followability. Uses force-think-before-rewrite methodology — articulate intent in one sentence, then write a normal sentence; no folds, no clever parallels.

**Designed to reproduce what was done manually with Sonnet in the 2026-05-14 Hijab voice pass.** Origin and rationale: `C:\Users\Benoi\.claude\plans\velvety-tinkering-finch.md`.

## Usage

```
/polish                              # Auto-detect most recent _READY_TO_FILM/ project with SCRIPT.md
/polish [project-slug]               # Explicit project
/polish --quick [project-slug]       # Skip Phase 1, go straight to pattern detection
/polish --thesis-only [project-slug] # Just Phase 1 throughline check, no pattern scan
/polish --no-notebook [project-slug] # Skip NotebookLM verification (offline mode)
```

## Flags

| Flag | Purpose | Example |
|------|---------|---------|
| (none) | Auto-detect single project in `_READY_TO_FILM/`. If multiple, ask. If zero, error. | `/polish` |
| `[project-slug]` | Explicit project folder name | `/polish 52-hijab-women-rights-2026` |
| `--quick` | Skip Phase 1, scan for AI patterns only | `/polish --quick 52-hijab-women-rights-2026` |
| `--thesis-only` | Run Phase 1 only (throughline + followability check) | `/polish --thesis-only 52-hijab-women-rights-2026` |
| `--no-notebook` | Skip notebook verification queries | `/polish --no-notebook 52-hijab-women-rights-2026` |

---

## CRITICAL: Sync rule

The 10 pattern categories in Phase 2 are sourced from `feedback-scriptcollab.md` → "Voice-Pass Patterns" section. **If a new pattern is added there, update this command's category list to match.** The two files MUST stay in sync — the command file is the executable surface, the memory file is the canonical ruleset.

---

## Phase 0 — Context Load (FIRST ACTION, parallel reads)

Before any other behavior fires, read these in parallel (one message, multiple Read tool calls):

1. `<project>/SCRIPT.md` — the locked script
2. `<project>/PROJECT-STATUS.md` — current lifecycle state
3. `C:\Users\Benoi\.claude\projects\D--History-vs-Hype\memory\feedback-scriptcollab.md` — canonical Voice-Pass Patterns ruleset
4. `C:\Users\Benoi\.claude\projects\D--History-vs-Hype\memory\feedback-staccato-delivery.md` — fragment + frequency-cap rule
5. `D:\History vs Hype\.claude\REFERENCE\WRITING-VOICE-AND-STYLE.md` — Calm Prosecutor voice, antecedent clarity, contractions
6. `D:\History vs Hype\.claude\REFERENCE\THESIS-DISCIPLINE.md` — 9-step throughline procedure (used in Phase 1 lite mode)
7. `D:\History vs Hype\.claude\REFERENCE\NOTEBOOKLM-SCRIPTWRITING-PROMPTS.md` — Use Case 18 thesis articulation + attribution verification

Also locate the project's NotebookLM notebook ID — either from the project's memory snapshot (e.g., `52-hijab-production-state.md`) OR from `<project>/PROJECT-BRIEF.md` if present. Store it for Phase 2 notebook queries. If `--no-notebook` flag is set, skip this.

Do NOT begin Phase 1 until all reads complete.

---

## Phase 1 — Throughline + Viewer-Followability (lightweight)

Skip if `--quick`. Run as the sole phase if `--thesis-only`.

**Goal:** confirm the storyline holds and a viewer landing cold can follow each section. NOT a redesign — a sanity check.

Steps:

1. **Locate the locked thesis** (≤12 words) in SCRIPT.md metadata or opening section
2. **Walk each section**. For each, two one-sentence checks:
   - **Throughline:** what work does this section do for the thesis?
   - **Followability:** can a viewer landing here cold follow along? Are antecedents clear? Are unfamiliar terms introduced before use?
3. **Anchor check (Rule 37):** the locked anchor word (e.g., "free woman") must appear in opening, every mechanism beat, climax, close — same exact wording
4. **Walk-Away test:** state what the viewer leaves with. Match the thesis?
5. **Flag any section** that fails throughline OR followability. If failure is structural (a missing beat), surface as a content-addition candidate for Phase 2 handoff.

Output a short list (per-section one-liners + any flags). User approves/adjusts before Phase 2.

---

## Phase 2 — AI Pattern Detection + Rewrite

Skip if `--thesis-only`. Default phase otherwise.

### Step A — Scan and categorize

Read the full script. Tag every candidate against the 10 categories below. Sort into two buckets:

- **Unambiguous bucket** — clear violations that always get cut:
  - Clear staccato fragments restating the prior sentence
  - "Same X. Different Y." parallel flourishes
  - Double negatives that could be positive
  - Missing contractions in VO
  - Internet-era phrases ("history has receipts")
  - Standalone short fragments doing no factual work
- **Judgment bucket** — context-dependent, needs user input:
  - Metaphors that *might* be doing real work (test: can it be removed without losing information?)
  - Attribution shifts (scholar's claim vs presenter's claim)
  - Rewrites where the obvious fix is awkward
  - Fragments carrying real factual or rhythmic weight
  - Section-opening transitions

### Step B — Batch the unambiguous

Surface all unambiguous candidates in ONE message as a numbered diff list with proposed fixes. Example format:

```
Unambiguous batch (8 candidates):

1. Line 109 — staccato triplet
   OLD: "Five civilizations. One rule. The veil was a uniform."
   NEW: "The same rule ran through five different civilizations over two thousand years."

2. Line 159 — staccato fragments
   OLD: "Same system. Same logic. Free women cover. Slaves don't."
   NEW: "Umar's enforcement makes the class logic explicit — the veil marks a free woman."

...

Apply all, or hold specific items? ("apply all" / "hold 3, 5" / "hold all → judgment")
```

User responds. Apply the approved subset live in ONE atomic action. Items held over move to the judgment bucket.

### Step C — One-by-one the judgment bucket

For each candidate: surface ONE at a time, propose a fix with reasoning, wait for user. On approval, edit live. Then next. Do NOT batch judgment calls.

### Rewrite methodology (fires on EVERY proposed rewrite)

Before proposing any rewrite:

1. **State in one sentence what the line is trying to say.** If you can't articulate the intent, the line doesn't earn its place — propose a cut instead of a rewrite.
2. **If you can articulate it, write a normal sentence.** NOT a fold-with-dashes that smuggles the fragments back in. NOT a clever parallel structure. NOT a rhetorical flourish. Just say it.
3. **When user pushes back** with "weird" / "what do you want to say" / "rewrite it normal" / "doesn't sound like me" — that IS the protocol firing. Do not iterate on the existing phrasing. Restate intent from scratch, then propose again in plain prose.

### The 10 pattern categories (canonical — keep in sync with `feedback-scriptcollab.md`)

1. **Staccato fragments as flourish** — couplets ("Same instrument. Different uniforms."), triplets ("Three states. Three opposite rules. The same move."), standalone fragments after a complete sentence ("Not permanent obligations."), parallel staccato pairs that restate the previous sentence. User's rule (verbatim): *"AI really likes these staccato bullshit things."* **Cut every time** unless doing factual work the prior sentence didn't already do.

2. **Decorative metaphors** — spatial/architectural ("Mesopotamian floor," "walking into a building," "substrate/surface"), biological. Test: if the metaphor can be removed and only the image is lost, it's decorative. Cut.

3. **Redundant restatement** — any sentence that repeats what the previous sentence already said in different words. Cut.

4. **Vague meta-transitions** — "And here's where it sharpens," "Now here's the part," vague verbs masquerading as transitions. Cut, or replace with the actual content the section is about to deliver.

5. **Internet-era phrases** — "history has receipts," anything that sounds Twitter/blog rather than documentary voice. Cut.

6. **Parallel rhetorical flourish** — "Same X. Different Y." family ("Same instrument. Different uniforms.", "The garment doesn't change. The states using it do."). Always cut.

7. **Double negatives that obscure** — "not making a fake choice" → "is making a real choice." Convert.

8. **Attribution slips** — scholar's reconstruction reading as presenter's conclusion. Insert "as X shows" or "X's analysis reveals." If uncertain whether the script's claim matches what the scholar actually said, query the project notebook (see below).

9. **Theological/sensitive-topic scope drift** — when a topic touches theology, default to a scope statement ("I'll leave that to the theologians") rather than naming a theological opponent.

10. **Missing contractions** — "it is / does not / are not / her wearing of it" → "it's / doesn't / aren't / her choice to wear it" throughout VO.

### Notebook verification (fires during Phase 2)

When attribution is uncertain (category 8) OR when content addition is triggered (see below): use `mcp__notebooklm__notebook_query` against the project notebook ID loaded in Phase 0. Verify:
- What did the scholar actually claim, vs what the script implies?
- For new content additions: is there verified primary-source material to support it?

Cite source numbers and page numbers in proposed edits. Use `⏳ Verify` flag for any claim where the notebook gave high confidence but no exact page — these get resolved in Phase 3.

### Content addition (handoff inside Phase 2)

Triggered by ANY of:
- Phase 1 flagged a structural gap
- User initiates during the pass ("is there a moment where Y?" / "can we add something about Z?")
- Pattern detection has cut a beat so heavily it now lacks substance and needs replacement

Workflow:
1. Query project notebook for verified material on the topic
2. Propose the addition with explicit sourcing (named primary or secondary source + page)
3. Get user approval
4. Integrate into the script live
5. Resume pattern detection

**Boundary:** `/polish` may RECOMMEND additions when a gap is visible. User decides whether to pursue. The command does NOT silently insert new content.

---

## Phase 3 — Final Read + ⏳ Resolution + Memory Batch

After all Phase 2 candidates resolved:

1. **Read the full script top-to-bottom.** Flag anything that *sounds* unnatural read aloud:
   - Antecedents drifting across paragraph breaks (Rule from `WRITING-VOICE-AND-STYLE.md` PART 5.2)
   - Sentences too long for one breath
   - Unfamiliar terms used before introduction
   - "Here's" count exceeded budget (max 2-4 per script — see channel CLAUDE.md)
2. **Resolve all `⏳ Verify` flags** by running targeted notebook queries
3. **Confirm SOURCES section page numbers** match what's cited inline
4. **Memory batch:** during the pass, you should have been collecting any NEW patterns the user named with novel reactions ("cringy," "typical AI writing," "weird sentence again"). Surface these as a proposed update to `feedback-scriptcollab.md` → "Voice-Pass Patterns" section. Format:

```
New patterns identified during this pass:

1. [Pattern name] — [user's exact reaction]
   Example: [the line that triggered it]
   Proposed rule: [one-sentence rule for future passes]

2. ...

Approve, edit, or reject each before I update feedback-scriptcollab.md.
```

User approves → apply updates. Reject → discard. Edit → integrate user's preferred phrasing.

5. **Status check:** if the project's lifecycle changes (e.g., `SCRIPT-LOCKED` → `FILM-READY`), prompt the user to run `/reconcile <project-slug>`. Do NOT auto-modify the AUTO block in PROJECT-STATUS.md.

---

## Hard rules (apply at all times)

- **One candidate at a time in the judgment bucket.** Never batch judgment calls.
- **Force-think-before-rewrite on every rewrite.** State intent in one sentence first.
- **Plain English, not folded fragments.** A fix that strings the deleted fragments back together with dashes is still AI writing.
- **Live edits, not edit-lists.** Apply approved changes immediately to SCRIPT.md.
- **No emojis. No preamble past one sentence. No end-of-turn summaries.** Match the channel's terse style.
- **Trust the lock.** If the script is in `_READY_TO_FILM/`, assume thesis, structure, and facts are locked. Voice pass refines what's there, doesn't redesign.

## When NOT to run /polish

- Script is still in `_IN_PRODUCTION/` — use `/script --revise` or `/script --review` first
- Script has not had a fact-check pass — run `/verify` first
- Script's notebook ID is unavailable AND `--no-notebook` was not specified — Phase 0 fails clean, report it

## References

- **Plan & rationale:** `C:\Users\Benoi\.claude\plans\velvety-tinkering-finch.md`
- **Canonical patterns:** `feedback-scriptcollab.md` → "Voice-Pass Patterns" section
- **Origin session:** 2026-05-14 Hijab voice pass with Sonnet
