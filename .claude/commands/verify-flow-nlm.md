---
description: Run narrative-flow verification + NotebookLM claim-query verification on a script (the deeper pass /verify --script skips for context-economy)
model: opus
---

# /verify-flow-nlm — Flow check + NotebookLM claim verification on a script

Two passes on a finished `SCRIPT.md`: (A) narrative-flow / structure verification, and (B) live NotebookLM claim-query verification via MCP. Use after `/script` when you want the deeper, notebook-grounded check — not just the simplification/attribution scan.

## Usage
```
/verify-flow-nlm [project]            # both passes
/verify-flow-nlm [project] --flow     # narrative-flow pass only
/verify-flow-nlm [project] --nlm      # NotebookLM claim-query pass only
```

## Context-economy (Sonnet has NO 1M context — mandatory)
- Do NOT re-query claims already grounded in `01-VERIFIED-RESEARCH.md` (claim IDs `C##`/`M#` ARE the trail). Query only: blockquotes, the thesis verb, the title's mechanism word, named-figure agency claims, and any claim with no `[SOURCE: … / C##]` tag.
- Batch `notebook_query` calls ≤5 in parallel. Large results persist to a file — Read it.
- If the run is getting heavy, do `--flow` and `--nlm` in separate invocations.

---

## PASS A — NARRATIVE-FLOW VERIFICATION (`--flow`)

Read `SCRIPT.md`. Apply the 10 narrative-flow rules (`WRITING-VOICE-AND-STYLE.md` §3.2) + the structure checks. For each finding give `line N → issue → concrete fix`.

**Check:**
1. **Terms before use** — every technical/foreign/named term defined in-breath at first mention (emirate, hükûmet, Anfal, etc.). Flag any term used before it's introduced.
2. **Bridges** — every section transition has a "why we're here now" sentence. Flag topic-jumps.
3. **Quote integration (3-step)** — Setup → Quote → Implication. Flag any quote dropped without a "so what."
4. **Implication after major facts** — after each big fact, the "which meant…" payload. Flag orphaned facts.
5. **Meta-commentary budget** — "I read/found" ≤1; "here's where it gets interesting" ≤1; performative metadiscourse = 0.
6. **No repetition** — same fact restated in different words. Flag.
7. **Stumble test / rhythm** — read each line as speech; flag compressed-prose fragments (telegraph nouns), sentences >25 words that don't build, 4+ consecutive same-length sentences, "So/Now" paragraph-opener stack (≤2–3), rhetorical-question pile-up (reserve 1 payoff question).
8. **Forbidden phrases** — grep the §1.3 list (delve, tapestry, buckle up, here's the thing, pivotal, "it's worth noting" as filler, etc.).
9. **The turn** — lands at 15–25% of runtime (not the 25–35% dead zone). State where it lands.
10. **Modern-relevance gaps** — note any stretch >90s with no modern bridge. *(For history-anchored videos this may be a deliberate deviation — state it, don't auto-fail.)*

**Output:**
```
--- FLOW VERIFICATION ---
CRITICAL (fix before film):  [line → issue → fix]
WARNING:                     [line → issue → fix]
INFO:                        [line → issue → fix]
Turn lands at: [m:ss / %]   Forbidden phrases: [none / list]
[If no CRITICAL: "Flow clean — proceed."]
---
```
(For a fuller structural read, also apply `.claude/agents/structure-checker-v2.md` natively.)

---

## PASS B — NOTEBOOKLM CLAIM-QUERY VERIFICATION (`--nlm`)

**Step 1 — locate notebook.** `mcp__notebooklm__notebook_list` → match the project slug/topic. If `UNAUTHENTICATED` / "Authentication expired": tell the user to run `! nlm login` (the `✓` UnicodeEncodeError on Windows is cosmetic — it authed), then `mcp__notebooklm__refresh_auth`. (Disk-cache refresh alone will NOT revive an expired token.)

**Step 2 — select claims to query** (per context-economy above): blockquotes, thesis verb, title mechanism word, named-figure agency claims, and any untagged claim. Skip already-grounded `C##` claims unless a quote's exact wording needs re-confirming.

**Step 3 — dispatch (batches ≤5), one query per claim, scoped with `source_ids` where known:**
```
CLAIM VERIFICATION — [short label]
The script says: "[exact wording / blockquote from SCRIPT.md]"
Is this supported by sources in this notebook? Return:
(a) SUPPORTED / PARTIALLY SUPPORTED / NOT SUPPORTED / CONTRADICTED
(b) if supported: exact verbatim quote + author, title, page
(c) any nuance/context the script is missing
(d) if contradicted: what the sources actually say
```

**Step 4 — map verdicts:**
- SUPPORTED + verbatim + page → ✅ (annotate the script line `[NLM-VERIFIED: <source id> p.X]`)
- PARTIALLY → flag with the gap named
- NOT SUPPORTED / CONTRADICTED → flag for cut/rewrite; quote what the source says instead

**Step 5 — attribution round-trip** (only for `Scholar X coined/named term Y` claims, per `/verify` Step 7.5): Query A "who originated term Y?" + Query B "does X use Y?" — both must agree, else downgrade to "describes, didn't originate."

**Step 6 — flag source-tier:** mark any claim resting on web/journalism (T2) rather than the academic notebook; mark fast-moving modern facts to re-verify at film-time.

**Output → `03-FACT-CHECK-VERIFICATION.md`** (append a `## NLM CLAIM-QUERY PASS (date)` section): a table of `claim → verdict → verbatim+page → action`, plus any inline `[NLM-VERIFIED]` / `[ATTRIBUTION-DOWNGRADED]` annotations added to `SCRIPT.md`.

---

## Verdict
End with: `FLOW: clean/N issues · NLM: X verified / Y flagged / Z contradicted · VERDICT: film-ready / fix-then-film`. If anything is CONTRADICTED, that's a hard blocker — fix before `/prep`.
