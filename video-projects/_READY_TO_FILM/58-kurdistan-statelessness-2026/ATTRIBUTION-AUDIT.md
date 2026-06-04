# ATTRIBUTION AUDIT — #58 Kurdistan (pre-film, expository pass)

**Date:** 2026-06-04
**Trigger:** retro-application of the new `/verify` Step 7.7 **Class B (expository authority / predicate drift)** gate — origin #57 Ptolemy/Ortelius. See `memory/feedback-attribution-audit.md` §third check.
**Scope:** every "[Authority]/[the treaty]/[the document] said/required/established/protects X" sentence in `SCRIPT.md` (Class B), plus a confirmatory sweep of Class A (named-person argued X). Run **before filming** — drift caught here is a script edit; after filming it's a VO pickup.
**Method:** extract → pin script-predicate P2 → identify what the source actually supports P1 → classify. NLM round-trips against the #58 notebook are RECOMMENDED to adjudicate the flagged items (per the gate's Gemini-raises/NLM-adjudicates discipline; the suspicions below are hypotheses, not verifications).

**Verdict key:** ✅ authority-asserts-it (grounded) · ⚠️ round-trip recommended · ❌ predicate drift (P2 ≠ P1).

---

## Result: 1 drift flag (load-bearing), 2 round-trip recommendations. Resolve before film.

### ❌ FLAG — `[ATTRIBUTION-EXPOSITORY]` — Lausanne Article 39 "by name"

| Field | Value |
|---|---|
| **Line** | L84 |
| **Script (P2)** | "It protects 'non-Moslem minorities.' Greeks, Armenians, Jews — **protected by name**. The Kurds are Muslims. Which means they fall outside the category completely." |
| **Source likely supports (P1)** | The Lausanne minority articles (≈Art. 37–44) protect the **category** "non-Moslem minorities." They do **not**, on the standard reading, enumerate Greeks / Armenians / Jews **by name** in the protective articles — those three were the *de facto* non-Muslim minorities, but the treaty's wording is the generic category. |
| **Why flagged** | "protected **by name**" is a predicate the document may not support. If the articles say only "non-Moslem minorities" (no enumerated list), the line overstates the treaty's text. **The load-bearing point survives either way** — Kurds-as-Muslims fall outside "non-Moslem minorities" regardless of whether the three groups are named. So the fix is cheap: drop "by name," or re-attribute the naming to a source that lists them. |
| **Action** | NLM round-trip: *"Does the Treaty of Lausanne name Greeks, Armenians, and Jews in its minority-protection articles, or does it use only the category 'non-Moslem minorities'? Quote the relevant article verbatim."* |
| **RESOLVED** | **2026-06-04 (user-authorized script edit).** L84 rewritten in `SCRIPT.md` + `SCRIPT-TELEPROMPTER.txt`: "It protects 'non-Moslem minorities.' **In practice that meant** Greeks, Armenians, Jews. The Kurds are Muslims…" — keeps the concrete groups as illustration, drops the unsupported "protected by name" (which implied the treaty enumerates them). The rewrite is correct **whether or not** the treaty names them, so it needs no round-trip; run the round-trip only if you want to restore stronger naming language. Definition-not-accident beat intact. |

### ⚠️ Round-trip recommended (low suspicion, likely fine)

| # | Line | Document / authority | Script predicate (P2) | Note |
|---|------|----------------------|------------------------|------|
| R1 | L78/80 | **Treaty of Sèvres** (C6/C19) | independence was "conditional, ran on a one-year clock, and hinged on a League panel deciding the Kurds were 'capable'" | Matches the standard reading of Sèvres Art. 62–64 (one-year application window to the League Council; "capable of" language). Confirm "one-year clock" + "capable" against the treaty text verbatim. `"capable"` is a quote → also a 7.8 card check. |
| R2 | L84 | **Article 39** quoted phrase "non-Moslem minorities" | on-screen quote card | 7.8 provenance: confirm the card matches the treaty's exact wording (e.g. "non-Moslem minorities" vs "non-Muslim minorities" — spelling/casing as the displayed source). |

---

## Class A + already-grounded (out of scope / low risk)

These are verbatim-grounded quote cards or hedged scholar paraphrase — **already verified** (most re-anchored in the 2026-06-02 provenance pass). Listed for completeness; not re-queried this pass.

| Line | Attribution | Status |
|------|-------------|--------|
| L22 | Eppel: "the most powerful Kurdish dynasty…" (C1) | ✅ quote card |
| L44 | Ateş / Ottoman paperwork: "separated from the pen…" (C37) | ✅ `[S→P]` grounded |
| L48 | Fraser 1834 via van Bruinessen: "were any man to see a purse of gold…" (C37) | ✅ |
| L52 | Posch via Cambridge: "never united under one political unit named Kurdistan" (C33) | ✅ |
| L60 | "historians call it a second Ottoman conquest" (C23) | ✅ hedged (no single name) |
| L64 | Ateş / Ottoman officers: "dreamt of establishing an independent state" (C33) | ✅ `[S→P]` grounded |
| L66 | van Bruinessen: "rapid devolution" (C23) | ✅ |
| L68 | Sheikh Ubeydullah 1880: "We are a nation apart…" (C32) | ✅ primary-via-Cambridge |
| L76 | MacMillan: Lloyd George "forgot Kurdistan"; "a Parisian pamphleteer" (C22) | ✅ paraphrase + quote, MacMillan's account |
| L82 | Curzon "ought to be an autonomous race" p.357; İnönü "a single unit in respect of race, religion and manners" p.343 (C15) | ✅ NLM-VERIFIED (7d37c3f5) |
| L94 | Pike Committee + Kissinger "covert action…not…missionary work" | ✅ re-anchored 2026-06-02 (Vanly 75e966ef / Gibson 01a62b01) — see SCRIPT.md annotation |
| L98 | McDowall: West supplied the gas "knowingly" (C35) | ✅ scholar quote |

---

## Completeness reconciliation (Step 7.7)

The Class A + Class B trigger grep above is the master enumerator. Before lock, confirm **each** of the lines listed here has a corresponding verdict row in `03-FACT-CHECK-VERIFICATION.md` (the #57 failure was a load-bearing line with **zero** fact-check rows). Spot-check the Sèvres/Lausanne document claims (L78/80/84/86) specifically — paraphrased document assertions are the ones most likely to be missing a row.

## Filming gate
- **L84 "by name" flag must be resolved (round-trip + edit-or-clear) before film.** The other items are round-trip-and-confirm; none currently blocks if the round-trips come back clean.
