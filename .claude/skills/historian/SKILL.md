---
name: historian
description: Historian-mode research discipline for the History vs Hype channel. Enforces four hard rules and four stop-flags during active historical research. Use when: querying a NotebookLM notebook, working in `_IN_PRODUCTION/` project folders, reading or editing `01-VERIFIED-RESEARCH.md`, running any `/research` subcommand, or whenever Claude is acting as a historical researcher (filing claims, building source lists, adding content to verified research). DORMANT during project mechanics (Step 0: demand gate, folder creation, title pre-gen).
---

# Historian Mode

## Historian Stages

| Stage | Name | Trigger |
|---|---|---|
| 0 | Project Setup | Folder creation, demand gate, title pre-gen — **skill dormant** |
| A | Historiographical Baseline | Wiki brief → preliminary research → viability gate → competitor gap |
| B | Source Criticism | NLM source list → provenance check → user notebook upload |
| C | Corroboration | NLM ingestion → **iterative research loop** → claim verification → angle lock → triage |

Stages sit *inside* channel Phase 1 (Research). Channel Phases (Research/Script/Fact-check) are separate and unchanged.

## Stage-C Research Loop (how to iterate once sources are in)

Run the loop in [RESEARCH-LOOP.md](RESEARCH-LOOP.md): **assess → synthesize (competitor + comment-mine + packaging) → decide/lock angle → execute (NLM query *or* source-ask) → pressure-test thesis → loop.**

**First read the "Operator instincts" in RESEARCH-LOOP.md** — they ARE the loop's driving logic (push deeper than the obvious start; hold the angle loosely & let evidence lead; distrust "done"; decide by examining the *method* not just the answer; synthesize across roles; separate the emotional hook from the analytical spine; protect the channel's identity; treat the runtime cap as a forcing function). Anticipate these; apply them autonomously.

Core defaults that bit this channel hard:
- **Don't declare "research complete" early** — re-assess against the angle; there's almost always another seam (act-bridge, near-miss, the deeper *why*, the shareable gem).
- **Sources: breadth + quality + recency (2018+), never "free."** Access status is a footnote.
- **History-anchored is a STANDING CONSTRAINT** — modern = closing rhyme only, never a geopolitics explainer.
- **Competitor re-check on FULL TRANSCRIPTS** (yt-dlp auto-subs), run *after* deep research → use their saturated thesis as your SETUP, not your thesis; catch audience-expected beats you lack.
- **Auditor's-edge / honesty guards mandatory** — myth-bust over assertion; check timing; "states ≠ nation"; keep the scholarly complication; bust your own brief's claims when sources contradict them. Verify a thesis with a "supporting AND contradicting" query.
- **Runtime: 12-min hard cap ≈ 10–12 beats.** Depth bulletproofs on-screen claims + gives cut options ("scholarly behind camera"); the dossier is done when you can *triage*, not when you've collected everything.
- **NotebookLM gotchas** (auth-expiry / borrow-only + Cloudflare + image-PDF ingestion failures / verify with `source_describe` / scope `source_ids`) — see RESEARCH-LOOP.md.

## Four Hard Rules

**Rule 1 — NLM-anchor:** Every verbatim quote filed in `01-VERIFIED-RESEARCH.md` MUST carry an NLM source ID. No exceptions. The anchoring source must **reproduce** the verbatim, not merely *cite or footnote* it — a primary quote (treaty, report, named figure) reached only through a scholar's footnote is **not anchored** (tag `[S→P-FOOTNOTE]`) and fires the same flag until the words are confirmed in a source that reproduces them. On-screen quote cards must match the displayed source character-for-character. Violation fires `[FLAG: NEED SOURCES]` or `[FLAG: LIBRARY ACQUISITION]`. See [WEB-POLICY.md](WEB-POLICY.md). (Footnote-laundering origin: #58 Kurdistan Pike/Kissinger cards.)

**Rule 2 — Tier-discipline:** Every claim must carry [P]/[S]/[S→P] tier + T1/T2/T3 tier-vibe. Single-source claims and [S]-tagged on-screen claims fire a flag. If a named acquisition target exists → `[FLAG: LIBRARY ACQUISITION]`. If no target → `[FLAG: NEED SOURCES]`.

**Rule 3 — Fork-detection:** When two NLM-grounded scholars interpret the same evidence differently AND the framing affects script tone or thesis direction, halt immediately. Fire `[FLAG: DIRECTION NEEDED]` and present both framings to the user.

**Rule 4 — Attribution-anchor (two modes):**
- **(A) Argument attribution.** Any claim of the form "PERSON read / argued / claimed / treats X" — **especially a debunk TARGET** (Hancock, Hapgood, von Däniken…) — must be NLM-anchored to a source showing *that person making that move*, not a source that merely confirms X is independently true. A real verbatim quote does NOT validate the attribution wrapped around it (validated-quote ≠ validated-attribution). Reframe overclaims as an appearance the text debunks, attributed to no named proponent. Violation fires `[FLAG: ATTRIBUTION UNVERIFIED]`. Origin: #57 cağferiye double-misattribution.
- **(B) Expository attribution — predicate drift.** When filing any claim that attributes a convention/theory/legal-or-textual proposition to a named **non-target** authority ("Ptolemy's geography said X", "the treaty established Y", "Roman law held Z"), record the **exact predicate the source supports** and confirm the authority asserts *that* predicate — not an adjacent one. **The non-target named-authority side is not low-risk — it is low-salience.** A claim where loose unnamed phrasing and a named-authority phrasing coexist for the same fact must be **reconciled before script-ready: name only what the source names.** Violation (script-predicate P2 ≠ source-predicate P1) fires `[FLAG: ATTRIBUTION DRIFT]`. Origin: #57 Ptolemy/Ortelius — research pinned Ptolemy to "land encircles water" (P1) but the script welded his name onto "had to exist to balance the globe" (P2, actually the Aristotelian symmetry argument popularized by Ortelius); filmed, fact-check-passed, caught only in editing. See `feedback-attribution-audit.md`.

> **Rule 4 companion — Attribution-tiering as neutrality (CANDIDATE, competitor-derived).** On contested religious/ideological claims, achieve neutrality by *tiering every position to its holder and date* — "most X believe…", "Al-Tabari affirmed…", "proponents of the Y reading point to…" — never by hedging ("some say") and never by adjudicating the doctrine itself. The cleanest model we've found is ReligionForBreakfast (Iblis angel-vs-jin: lays out both camps, then "what if both were right?", resolves to historical complexity, not a verdict). This is the positive, voice-side form of Rule 4: don't just avoid false attributions — bind *every* claim to who holds it. Especially load-bearing for the Claims-on-Trial series (#59) and religion-adjacent topics (#52). Idea, not mandate — test it. See `tools/benchmark/SCRIPT-PATTERN-ANALYSIS-VOTP-RFB-2026-06-03.md`.

## Stop Flags

| Flag | Fires when | Spec |
|---|---|---|
| `[FLAG: NEED SOURCES]` | Verbatim quote has no NLM anchor + no known acquisition target; or single-source [S] on-screen claim | [STOP-FLAGS.md](STOP-FLAGS.md) |
| `[FLAG: LIBRARY ACQUISITION]` | Verbatim quote has no NLM anchor but a specific named source would close the gap | [STOP-FLAGS.md](STOP-FLAGS.md) |
| `[FLAG: DIRECTION NEEDED]` | Two NLM-grounded scholars diverge on framing that affects script tone or thesis | [STOP-FLAGS.md](STOP-FLAGS.md) |
| `[FLAG: ATTRIBUTION UNVERIFIED]` | A "PERSON read/argued/claimed X" claim is backed only by a source confirming X is true, not by that person making the move (strawman risk — esp. debunk targets) | [STOP-FLAGS.md](STOP-FLAGS.md) |
| `[FLAG: ATTRIBUTION DRIFT]` | A named non-target authority/document is said to assert proposition P2, but the source supports only an adjacent P1 (predicate drift — esp. expository "X said/required/established Y") | [STOP-FLAGS.md](STOP-FLAGS.md) |

**When a flag fires:** state the flag text, explain why it fired, halt research output, and wait for user direction. Do NOT continue filing claims past an unresolved flag.

## Stage Transitions

Surface conversationally at natural moments: *"Stage A complete — ready for Stage B?"*

On user confirm, append a `## Historian Stage State` section to `PROJECT-STATUS.md` **below the `<!-- /AUTO:reconcile -->` marker** (not inside the AUTO block). See [STAGE-AUDITS.md](STAGE-AUDITS.md) for pre-transition checklists.

```
## Historian Stage State
**Current stage:** Stage [X] — [Name] (locked [YYYY-MM-DD])
**Next stage:** Stage [Y] — [Name]
**Outstanding flags:** [None / list of unresolved flags]
**Stage A locked:** [date or "pending"]
**Stage B locked:** [date or "pending"]
**Stage C locked:** [date or "pending"]
```

## Migration (existing projects)

For `/research --existing` on projects without stage markers, infer from artifacts:

| Evidence | Inferred stage |
|---|---|
| 20+ ✅ claims in `01-VERIFIED-RESEARCH.md` + notebook ID present | Stage C |
| `00-NOTEBOOKLM-SOURCE-LIST.md` + NLM notebook populated + <5 ✅ claims | Stage B |
| `_research/00-PRELIMINARY-BRIEF.md` exists + no NLM notebook | Stage A |

Surface inference: *"I infer Stage C based on [evidence]. Confirm?"* Write Stage State section only after user confirms.

## Supplementary Files

- [RESEARCH-LOOP.md](RESEARCH-LOOP.md) — the Stage-C iterative research/contemplation loop + behavioral lessons + NotebookLM ops (from Kurdistan #58)
- [STOP-FLAGS.md](STOP-FLAGS.md) — full spec + Piri Reis examples for all three flags
- [STAGE-AUDITS.md](STAGE-AUDITS.md) — stage-boundary audit checklists
- [WEB-POLICY.md](WEB-POLICY.md) — verbatim/paraphrase policy with worked examples
