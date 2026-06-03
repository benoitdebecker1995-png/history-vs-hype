# PLAN — Hijab #52 Session Improvements
**Date:** 2026-05-21
**Source:** `session-findings-52-hijab-2026-05-20.md` + grill session 2026-05-21 (Opus)
**Implementer:** Sonnet
**Scope:** Three skill-file extensions (P7/P8/P10) + one user-action item (B-roll patch for live #52 video). Memory updates already applied — see "What's already done" below.

---

## 0. What's already done (do NOT redo)

The following were applied by Opus before this plan was written. Sonnet does NOT need to touch them:

| File | Change |
|---|---|
| `memory/feedback-notebook-citation-grounding.md` | New "Scope extension — verbatim verification ≠ attribution verification (added 2026-05-21)" section |
| `memory/feedback-earn-your-inclusion.md` | New "Scope extension — metadata-level earned-inclusion (added 2026-05-21)" section |
| `memory/feedback-postmortem-methodology.md` | New "Extension — second methodology-bias dimension (added 2026-05-21)" section |
| `memory/feedback-broll-patch-for-postfilm-slips.md` | **New file created** |
| `memory/feedback-auditors-edge.md` | New "Tier-vibe" section (T1/T2/T3 sliding preference; not a tag system) |
| `memory/MEMORY.md` | Index updated for all five files above |

The full memory paths are under `C:\Users\Benoi\.claude\projects\D--History-vs-Hype\memory\`.

---

## 1. P7 — Extend `/verify` with attribution mandate

**File to edit:** `D:\History vs Hype\.claude\commands\verify.md`

**Problem this solves:** Hijab #52 shipped the "Lloyd Jones / scopic regime" cite-selection drift because the verification pipeline checks "is this quote verbatim in the cited source" but does not check "is this scholar the originator of the term."

**What to add:** A new section in `verify.md` titled `## Attribution Mandate (for `X named/coined/termed Y` claims)`.

**Behavior the section must specify:**

1. **Grep trigger phrases.** During `/verify`, grep the script for these trigger phrases:
   - `named` / `was named by` / `named it`
   - `coined` / `coined the term`
   - `termed` / `termed it`
   - `called this` / `called it`
   - `labelled this` / `labeled this`
   - `the [Name] regime` / `the [Name] system` / `the [Name] framework` / `the [Name] principle` / `the [Name] effect`
   - `the [Name] term` / `[Name]'s term`
2. **For each match, output:** `[ATTRIBUTION-CHECK]: line N — "<matched-phrase>" — scholar=<Name>, term=<Y> — needs bidirectional NotebookLM round-trip.`
3. **Bidirectional round-trip requirement (the actual verification step).** For each flagged claim, the verifier (user or agent) must run TWO NotebookLM queries:
   - Query A: *"Where does the term `<Y>` originate / who introduced it?"* (origin direction)
   - Query B: *"Does `<Name>` use / describe / discuss `<Y>` in their work?"* (user direction)
   - Both queries must return consistent results. If Query A surfaces a *different* scholar than `<Name>`, the script's attribution is at risk — either rewrite to the more-authoritative scholar, or downgrade the claim from origination to description.
4. **Annotation requirement.** Once verified, the script line gets an inline annotation: `[ATTRIBUTION-VERIFIED: <Name> originated <Y> per <NotebookLM source IDs>]` OR `[ATTRIBUTION-DOWNGRADED: <Name> describes but did not originate <Y>; primary cite is <Other-Name>]`.
5. **DRAFT-LOCKED gate (Format C only).** Format C scripts cannot reach DRAFT-LOCKED with any `[ATTRIBUTION-CHECK]` lines that lack a corresponding `[ATTRIBUTION-VERIFIED]` or `[ATTRIBUTION-DOWNGRADED]` annotation. Format A/B treats this as recommendation, not gate.
6. **Shared-conceptual-space sub-class flag.** When the verifier finds that 2+ scholars work in cognate territory on the same concept (e.g., Geissinger + Llewellyn-Jones on veil-as-social-regulation), the script must use the *most-authoritative-in-subfield* scholar, not just any scholar who uses the term. This is a judgment call surfaced by the bidirectional query, not an automated rule.

**Where to place the section:** After the existing verification phases / before the existing "Sign-off" / "Output" section, wherever that lives in `verify.md`. Read the file first to find the natural insertion point.

**Cross-reference to add at the top of the new section:** "See `memory/feedback-notebook-citation-grounding.md` §'verbatim verification ≠ attribution verification' for the why and the Hijab #52 origin."

**Acceptance:** After the edit, a dry-run of `/verify` on a script containing "Historian X named this the Y regime" should output an `[ATTRIBUTION-CHECK]` flag for that line.

---

## 2. P8 — Extend `/publish` with metadata-drift gate

**File to edit:** `D:\History vs Hype\.claude\commands\publish.md`

**Problem this solves:** Hijab #52's `YOUTUBE-METADATA.md` was authored pre-filming and silently drifted from the finished cut on four dimensions (title promise, dangling description, wrong chapter timestamps, source-list scholars not load-bearing). The drift survived until publish-day when Opus planning caught it.

**What to add:** A new section in `publish.md` titled `## Metadata-Drift Gate (post-rough-cut, pre-publish)`.

**Behavior the section must specify:**

1. **Inputs required to run the gate:**
   - `YOUTUBE-METADATA.md` (the file being checked)
   - The finished-cut SRT (the source of truth — locate via Glob for `*.srt` in the project folder; prefer the most recent / "finished cut" / "final" file)
   - The locked `SCRIPT.md` (only used as supplementary context, not authority)
2. **Four drift checks to run:**

   **a. Chapter-timestamp grounding.** Parse the SRT for structural pivots. For each chapter in `YOUTUBE-METADATA.md`:
   - Compare the chapter's timestamp against the SRT's actual structural transitions.
   - If the chapter timestamp falls outside the SRT's actual runtime, flag as `[CHAPTER-DRIFT: chapter "<name>" timestamp <T> exceeds SRT runtime <R>]`.
   - If the chapter timestamp doesn't correspond to a structural pivot in the SRT (±5s tolerance), flag as `[CHAPTER-DRIFT-PIVOT: chapter "<name>" timestamp <T> doesn't match any SRT pivot]`.
   - Output a proposed re-derivation: a new chapter list with timestamps grounded in actual SRT pivots.

   **b. Source-list earned-inclusion.** Extract scholar names from the description's source list. Grep the SRT for each name:
   - If a listed scholar's name does NOT appear in the SRT: flag as `[SOURCE-LIST-UNUSED: scholar "<Name>" listed but not named in finished cut]`. Default action: cut from list.
   - Extract scholar names from the SRT (heuristic: capitalized first-name + last-name pairs preceded by trigger words like "Historian," "Per," "Scholar," "according to," or appearing in citation-tag positions). For each SRT-named scholar NOT in the description list: flag as `[SOURCE-LIST-MISSING: scholar "<Name>" named in cut but not in description]`. Default action: add to list.

   **c. Title-promise earned-inclusion.** Parse the title (and all A/B variants) for promise patterns:
   - Numeric claims ("Three Medieval Scholars," "Two Countries," "229 Ethnic Groups")
   - Named-entity claims ("Lord Cromer," "Ibn al-Jawzi")
   - Mechanism-word claims ("Forbidden," "Mandatory," "Forged")
   - For each promise, check the SRT delivers it. If "Three Medieval Scholars" is promised but only one is named in the cut: flag as `[TITLE-PROMISE-UNFULFILLED: variant "<title>" promises <claim> but cut delivers <actual>]`.

   **d. Dangling-text grep.** Grep the description body for:
   - Sentences ending in em-dash, en-dash, or hyphen without trailing punctuation
   - Sentences cut mid-clause (heuristic: line ends with a preposition, conjunction, or bare auxiliary verb)
   - Unclosed parentheses, quotes, or em-dash pairs
   - Flag each as `[DESCRIPTION-DANGLING: line N — "<text>"]`.

3. **Output: `YOUTUBE-METADATA-DRIFT.md` in the project folder.** Contains:
   - Summary count of each flag class
   - Detailed flag list with proposed remediation per flag
   - Final section: "Override decisions" — user accepts or overrides each flag with rationale
4. **Gate behavior.** `/publish` cannot proceed past the drift gate until either:
   - All flags have been remediated (metadata file edited)
   - OR all flags have been explicitly overridden in `YOUTUBE-METADATA-DRIFT.md` with a one-line rationale per override

**Where to place the section:** Before any publish/upload step in `publish.md`. The gate runs early in the `/publish` flow, before the user invests time in tag refinement and clip selection.

**Cross-reference to add at the top of the new section:** "See `memory/feedback-earn-your-inclusion.md` §'metadata-level earned-inclusion' for the three tests baked into this gate, and the Hijab #52 origin."

**Acceptance:** After the edit, a dry-run of `/publish` on the Hijab #52 folder's `YOUTUBE-METADATA.md` (pre-fix state, if recoverable from git) should output all four drift flags. (Post-fix state should output zero — already remediated this session.)

---

## 3. P10 — Extend `/reconcile` with lifecycle-transition snapshot refresh

**File to edit:** `D:\History vs Hype\.claude\commands\reconcile.md`

**Problem this solves:** Per-project memory snapshots (e.g., `52-hijab-production-state.md`) silently drift as a project moves across lifecycle boundaries. Future-Claude reads them at the start of next session as authoritative when they're frozen at a prior point in time.

**What to add:** A new section in `reconcile.md` titled `## Lifecycle-Transition Snapshot Refresh`.

**Behavior the section must specify:**

1. **Trigger condition.** When `/reconcile` detects that a project is moving across a lifecycle boundary:
   - `_IN_PRODUCTION/` → `_READY_TO_FILM/`
   - `_READY_TO_FILM/` → `_ARCHIVED/published/`
   - (Any cross-folder move counts)
2. **Snapshot detection.** Check whether a per-project memory snapshot exists for this project at `C:\Users\Benoi\.claude\projects\D--History-vs-Hype\memory\<NN>-<slug>-production-state.md` (pattern: number-slug-production-state.md).
3. **If snapshot exists:** Fire an `AskUserQuestion` with this exact prompt:

   > "Memory snapshot `<NN>-<slug>-production-state.md` was last substantively updated on `<date>`, which predates the current lifecycle transition (`<from>` → `<to>`). The snapshot may contain stale state — old titles, old thumbnail concepts, old folder paths. How should this be handled?"

   With these options:
   - **Refresh inline** — Open the snapshot, update fields known to have changed (current folder location, locked title, locked thumbnail concept, locked thesis). Save with new dated entry appended.
   - **Mark stale, defer refresh** — Append a `> STALE AS OF <date> — superseded by <transition>` block at the top of the snapshot. Future sessions will see the stale-flag and re-derive from current files.
   - **Accept as-is** — User explicitly judges the snapshot is still current despite the transition. Append a `> CONFIRMED CURRENT AT <date>` block at the top.
4. **If snapshot does NOT exist:** Skip the prompt. No-op.
5. **At archive transition (`_READY_TO_FILM/` → `_ARCHIVED/`):** The existing lessons-promotion prompt is unchanged (per `memory/feedback-project-reconciliation.md`). The new snapshot-refresh prompt fires *before* the lessons-promotion prompt, not after — refresh-or-mark-stale first, then lessons-promotion gates snapshot deletion.

**Where to place the section:** Inside the existing `/reconcile` lifecycle-transition logic, wherever the folder-move detection lives. Read `reconcile.md` first to find the natural insertion point.

**Cross-reference to add at the top of the new section:** "See `memory/feedback-project-reconciliation.md` for the broader reconcile lifecycle rule and the Hijab #52 stale-snapshot origin."

**Acceptance:** After the edit, running `/reconcile 52-hijab` (when the folder eventually moves to `_ARCHIVED/published/`) should fire the snapshot-refresh prompt BEFORE the lessons-promotion prompt. Both prompts then run in sequence.

---

## 4. User-action items (NOT Sonnet's scope, but listed for completeness)

These cannot be implemented by Sonnet — they're either video-editing work or out-of-scope content decisions. The user (Benoit) handles these.

**B-roll patch for live #52 video (D1 resolution from the grill):**
- The video is live with the "Historian Lloyd Jones" VO at ~01:02:19 for "scopic regime."
- Per the grill, this is cite-selection drift (not factual wrongness) and gets patched at the B-roll layer per [[feedback-broll-patch-for-postfilm-slips]].
- Concrete patch: add an additive on-screen card overlapping or immediately following the existing scopic-regime beat: *"See also: Aisha Geissinger, *Gender and Muslim Constructions of Exegetical Authority*, Brill 2015, p. 216 fn. 25"*
- Phrase additively (further reading), not correctively. Do NOT pin a YouTube correction comment.
- This requires the existing edit project — Sonnet cannot do this.

**D2 — Postmortem v2 candidate rule promotions:**
- Tracked in `52-hijab-postmortem-v2.md`, separate from this plan. Out of scope.

**D3 — Force-archive #52 vs wait for Routine 6:**
- Administrative; the Routine 6 backstop runs ~08:30 daily and archives automatically once `analytics.db` refreshes with the new YouTube Video ID. Wait is the default; force-archive only needed if user wants immediate transition.

**Arabic-source verification capability (parked):**
- The OCR + NotebookLM Arabic-corpus pilot is parked until the next Arabic-source video enters `_IN_PRODUCTION/`. No video in the current slate triggers it (#56 Slave Trade is Portuguese/Latin, #3 Monroe is Spanish/Latin, parked Haiti is French). Memory rule [[feedback-auditors-edge]] tier-vibe documents the interim posture: aspire T1, accept T2 when primary inaccessible, use T3 honestly (with "Scholar X concludes..." framing) when no other option.

---

## 5. Implementation order for Sonnet

Recommended sequential order. Each task is independent — can pause between them.

1. **P10 first** (smallest, cheapest, lowest-risk wire-in to existing `/reconcile` flow).
2. **P7 second** (medium complexity; the attribution-check pass touches `/verify` core logic).
3. **P8 third** (highest complexity; SRT parsing + four flag classes + drift report generation).

Each task should end with:
- A read-back of the edited section to confirm the change landed
- A one-line entry in the project's commit if any (Sonnet, do NOT commit unless explicitly asked — user controls commits)

---

## 6. Verification checklist for Sonnet (at end of each task)

For each of P7, P8, P10:

- [ ] Read the existing skill file end-to-end before editing
- [ ] Identified natural insertion point (don't append at the end if a more coherent location exists earlier)
- [ ] Cross-reference to relevant memory file included at the top of the new section
- [ ] Section follows the existing skill file's tone, header style, and structure
- [ ] No new files created (extensions only — per [Tool Discovery Before Proposing], extend existing tools rather than creating sister tools)
- [ ] Final read-back of the edited file confirms the change is present and well-placed

---

## 7. What's explicitly NOT in scope

- No CONTEXT.md changes (no new domain language emerged)
- No ADR creation (none of the changes are hard-to-reverse architectural decisions)
- No T1/T2/T3 tag schema added to `03-FACT-CHECK-VERIFICATION.md` template (the tier-vibe is a preference, not a tag system; existing P/S/S→P stays in `feedback-research-audit.md`)
- No `/verify-attributions` or `/refresh-metadata` standalone commands (P9 was subsumed by P7; P8 lives inside `/publish`)
- No retroactive re-tagging of past projects
- No memory snapshot deletion (the snapshot-refresh prompt lets the user choose; deletion remains gated by interactive `/reconcile`)

---

## 8. Cross-reference index for Sonnet

When implementing, the following memory files describe the *why* behind each tool extension. Skim before editing each skill file:

| Tool extension | Read this memory file first |
|---|---|
| P7 (`/verify` attribution mandate) | `feedback-notebook-citation-grounding.md` (especially the 2026-05-21 extension) |
| P8 (`/publish` metadata-drift gate) | `feedback-earn-your-inclusion.md` (especially the 2026-05-21 extension) |
| P10 (`/reconcile` snapshot refresh) | `feedback-project-reconciliation.md` (existing rule) + `52-hijab-production-state.md` (the snapshot that drifted) |

End of plan.
