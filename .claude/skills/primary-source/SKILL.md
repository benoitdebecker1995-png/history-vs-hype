---
name: primary-source
description: On-screen-provenance discipline for the History vs Hype channel — the rule that every claim going ON SCREEN carries a genealogy verdict (traced to the most-primary showable source), the two-layer model (on-screen primaries vs behind-camera scholarship), and when to spawn the primary-source-hunter agent. Use when: deciding what document/verbatim to put on screen, filing an on-screen claim in a project, reaching the Stage C → script-ready boundary in /research, running /verify Step 7.8 (provenance/quote-card lock), or whenever a claim's provenance ("who actually said/measured/wrote this?") is load-bearing. Owns the SOURCE-GENEALOGY.md ledger. DEFERS filing/tiering discipline to `historian`; routes deep single-claim traces to the `primary-source-hunter` agent.
---

# Primary-Source Mode

The channel's product is *demonstrated provenance* — we opened the document ourselves. A single mis-sourced on-screen claim is self-refuting: it makes the referee guilty of the hype the channel exists to expose. This skill institutionalises the standard so it never rides on a lucky deep-dive.

**This skill owns the DISCIPLINE and the LEDGER; the `primary-source-hunter` agent owns the METHOD.** Don't re-derive the citation-ladder climb, the access-route repertoire, or the render commands here — those live in `.claude/agents/primary-source-hunter.md`. This skill decides *what needs a trace, what verdict it must carry, and when to spawn the agent*.

---

## The two-layer model (hold as a model, not a taxonomy)

| Layer | What it is | Where it appears | Provenance bar |
|---|---|---|---|
| **ON-SCREEN primary** | The document a careful historian would put on screen — treaty, UN verbatim record, gov memo/telegram, census, diary, court ruling, map. Mostly free (gov/UN/archival). | Quote cards, chyrons, document push-ins | **Must be showable + traced to bedrock.** Gets a genealogy verdict. |
| **BEHIND-CAMERA scholarship** | The monographs and articles that inform the read — often paywalled, world-class. | The citation tag / description, spoken attribution ("Benny Morris — Israeli historian") | Tier-tagged (defer to `historian` Rule 2). No full down-ladder trace required. |

The point is never three buckets — it's **report the best rung reached and the move up.** A claim can be primary-grounded, primary-via-testimony, or honestly secondary-only; say which.

---

## The on-screen standard (the non-negotiable)

**Every claim that goes ON SCREEN carries a genealogy verdict before the project is script-ready:**

- **PRIMARY-GROUNDED** — a real primary document exists and is showable (with char-exact verbatim + exact page/locator). Includes S→P where a scholar's footnote carries a genuine archival primary.
- **PRIMARY-VIA-TESTIMONY** — participant recollection only (memoir, oral history, diary). Primary-ish but relayed; label it as such.
- **SECONDARY-ONLY** — the trail bottoms out at scholars. **Attribute to historians by name — NEVER "documents show" / "the record proves."** This is a legitimate on-screen state for the channel's voice, but it must be *labelled as a scholar's reading*, not dressed as a document. **Chase-the-footnote rule (two halves):** (1) a footnote that merely *points* to another scholar is a rung to climb, not a bottom — this verdict is honest only after the *reachable* chain is exhausted; but (2) "chase" means *locate and name* the rung and pursue **free primaries** to the end — a **gated/unowned secondary** book (wanted only for its footnote) is an **ACQUISITION ASK, not a grind**: one quick reachability check, then name it (title + page → `SOURCE-ACQUISITION-QUEUE.md`) and report the verdict as *"SECONDARY-ONLY, pending acquisition of [work p.X]"*. The agent locates + names; the user acquires and re-invokes. Never burn effort scraping around a paywall for secondary scholarship. See `feedback-chase-the-footnote-chain`.

Load-bearing **spoken** claims that never appear on screen get tier-tagging only (`historian` Rule 2: [P]/[S]/[S→P] + T1/T2/T3). Decoration stays scholar-cited. **The gate is scoped to what's on screen — not every sentence.**

---

## Routing: spawn the agent, or confirm inline?

The core decision this skill makes:

| Situation | Action |
|---|---|
| On-screen claim whose provenance is **non-obvious / load-bearing / contested** (the trail runs through a scholar, or the number/quote carries the beat) | **Spawn `primary-source-hunter` (`model: opus`).** It climbs the ladder, raw-reads, renders the document, returns a Source Genealogy + upserts the ledger row. |
| On-screen claim **already primary-grounded in the notebook** (you've raw-read the reproducing source this pass; page confirmed) | Confirm **inline**; write the ledger row yourself. |
| Behind-camera scholarship (tag only) | No trace. Tier-tag per `historian`. |
| Provenance is fine but a claim's **wording** may drift from the primary | Run the attribution-mismatch check (below) inline; spawn the agent only if the primary needs re-reading. |

Invocation (return contract + rate-limit rule: `.claude/AGENT-ORCHESTRATION.md`):
```
Task(subagent_type="primary-source-hunter", model="opus",
  prompt="Find the most-primary showable source for: '[claim]'. Currently cited to [src/p.] in [slug]. Notebook: '[name]'.")
```

---

## The ledger — `_research/SOURCE-GENEALOGY.md`

The per-project roll-up this skill produces and `/verify` Step 7.8 consumes. **One row per on-screen claim.** The agent upserts a row when it finishes a trace; you write rows for inline-confirmed claims. #59's `ON-SCREEN-CARDS.md` is the worked prototype the schema distils.

```markdown
# Source Genealogy Ledger — #NN <topic>
> One row per ON-SCREEN claim. Verdict ∈ {PRIMARY-GROUNDED, PRIMARY-VIA-TESTIMONY, SECONDARY-ONLY}.
> `Detail` links the hunter's per-claim source-genealogy-<slug>-<date>.md.

| On-screen claim | Verdict | Primary reached (doc · cite · page) | Showable file/URL | Rung + route | Mismatches | Detail |
|---|---|---|---|---|---|---|
| Philippines pressure | PRIMARY-GROUNDED | FRUS 1947 v5 d910, Lovett→Truman, 10 Dec 1947, 501.BB Pal/12-1047 | history.state.gov/…/d910 | left notebook → FRUS | VO "US officials" → ten US senators | [detail](_research/source-genealogy-philippines-2026-07-04.md) |
| Liberia rubber-freeze | SECONDARY-ONLY | none — Sachar thesis + Henderson interview + Urofsky | — | Cohen p.297 fn99 | attribute to historians, not "documents show" | [detail](…) |
```

The ledger is the **single provenance source of truth**: `/research` writes it before script-ready; `/verify` 7.8 reads it instead of re-deriving. Keep it current — a card with no ledger row is a `/verify` flag.

---

## The channel's two hard cases (stated as discipline)

- **Foreign-language primary = a STRENGTH, not a dead end.** This channel's edge is *untranslated evidence* (#62 Volhynia). Retrieve the document in its **original language**; quote the verbatim **in-language, char-exact** (the owner source-verifies FR/ES/DE/Dutch/Latin/Greek per `user-languages`). **Never present a translation as the original** — translation is a separate step → route to `/translate` (clause-by-clause + cross-check + surprise detection). On screen = original document + a clearly-labelled verified translation. The ledger row records the original-language verbatim and flags translation as pending.
- **Gated primary = separate the DOCUMENT from its CONTAINER.** When the primary is reproduced only in a paid volume/journal/archive (e.g. a 1947 telegram in *Political Documents of the Jewish Agency*): FIRST hunt a **free reproduction of the same document** — a public-domain gov/UN/legal record trapped in a paid edition usually also sits in FRUS, a national archive, or the paper of record; show *that* and cite it to its archival origin. Only if no free reproduction exists is it an owned-library / legitimate-access problem. Mark **GATED** and note whether the underlying record is itself public-domain (older gov/legal/archival records usually are, even when the edition isn't).

**Boundary:** locate + legitimately access + organize. Shadow-library downloads stay the owner's manual call — never automated.

---

## Stop-flags (provenance-specific; siblings of `historian`'s)

| Flag | Fires when | Action |
|---|---|---|
| `[FLAG: PROVENANCE — SECONDARY-ONLY]` | An on-screen claim's trail bottoms out at scholars/testimony but the script/card frames it as a document ("the record shows", "the annexes prove") | Re-label to named-scholar attribution, or find a real primary. HARD for on-screen. |
| `[FLAG: ATTRIBUTION MISMATCH]` | The claim's wording drifts from what the primary says — **SOURCE-DRIFT** (wrong document), **PREDICATE-DRIFT** (stronger/different proposition), **MIS-CREDIT** (right event, wrong actor), **NAME/NUMBER-ERROR** (source itself errs, e.g. Cohen's "Rojas" for Roxas) | Fix the wording to what the primary supports; don't launder or propagate. Validated fact ≠ validated attribution. |

**When a flag fires:** state it, explain why, halt on that claim, and resolve before it reaches the ledger as cleared. Defers to `historian`'s `[S→P-FOOTNOTE]` / `[FLAG: ATTRIBUTION DRIFT]` for the filing-side versions — this skill's flags are the *on-screen showability* layer on top.

---

## Where this fires in the workflow

- **`/research` — genealogy-before-filing** (Stage C → script-ready boundary): before `01-VERIFIED-RESEARCH.md` flips to `READY TO WRITE SCRIPT`, every projected on-screen claim must have a ledger verdict. Surface unresolved ones as a checklist; spawn the hunter for the non-obvious load-bearing ones. (Skill-enforced/conversational this slice; a `genealogy_lock.py` hard code-gate is deferred.)
- **`/verify` — Step 7.8** (Provenance & Quote-Card Verbatim Lock): cross-check each on-screen card against its ledger row (verdict + verbatim + page); flag any card with no row.
- Reuses, never replaces, the existing owned-first machinery (`/research` Step 8.5 library grep, Step 6.6 acquisition queue).

## Related skills

- **historian** — filing/tiering/NLM-anchor discipline, the Stage A/B/C research loop, and the [P]/[S]/[S→P] + T-vibe tags. This skill sits *on top* for the on-screen showability layer; it defers all filing discipline there.
- **`primary-source-hunter` agent** (`.claude/agents/primary-source-hunter.md`) — the deep method: citation-ladder climb, raw-read, access-route repertoire, render, per-claim Source Genealogy output. This skill routes single-claim traces to it.
- **production-map** — which pipeline command comes next; where /research and /verify sit.
- **`/translate`** — the destination for every foreign-language primary's translation step.
