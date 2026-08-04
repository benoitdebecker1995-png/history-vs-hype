---
name: source-command-verify
description: "Fact-checks a script line-by-line against the verified research, extracts claims, and detects oversimplifications. Use when: a draft is written and needs checking, asked to fact-check or verify claims, or filling 03-FACT-CHECK-VERIFICATION.md. Does NOT run the deeper narrative-flow + per-claim NotebookLM pass (→ source-command-verify-flow-nlm)."
---

> **Codex note.** This is the Codex port of `.claude/commands/verify.md`, which stays canonical.
> The procedure below is that file verbatim. While running here: a `/name` reference is the
> `source-command-name` skill in `.agents/skills/`; "the Task tool" means spawning a Codex agent
> from `.codex/agents/`; "Claude" means you.

# /verify - Verification Entry Point

Fact-check scripts, extract claims from transcripts, or run simplification detection. This command consolidates all verification workflows.

## Usage

```
/verify                      # Interactive: fact-check current project
/verify --script [project]   # Fact-check a script
/verify --extract [file]     # Extract claims from transcript
/verify --delta [project]    # Verify only NEW/CHANGED claims (not in verified research)
/verify --simplify [project] # Run simplification detection only
/verify --extract-nlm [file] # Extract citations from NotebookLM output
/verify --translation [project] # Verify translated documents
/verify --nlm [project]         # Notebook-only: Tier 1 claims + citation grounding via MCP
/verify --adversarial [project] # Cross-model skeptic pass (Gemini attacks the script) → NLM-adjudicated findings
/verify --audio [project]       # POST-FILM BACKSTOP: catch narrator ad-libs/misreads that deviate from the fact-checked script
```

## Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `--script` | Full fact-check verification | `/verify --script 19-flat-earth-medieval-2025` |
| `--delta` | Verify only claims not in verified research | `/verify --delta 50-thermopylae-sources-2026` |
| `--extract` | Extract claims from YouTube transcript | `/verify --extract transcript.vtt` |
| `--simplify` | Simplification detection only | `/verify --simplify 19-flat-earth-medieval-2025` |
| `--from-transcript` | Extract + fact-check workflow | `/verify --from-transcript video-url` |
| `--extract-nlm` | Extract citations from NotebookLM output | `/verify --extract-nlm nlm-output.txt` |
| `--translation` | Verify translated documents before filming | `/verify --translation 37-vichy-statute` |
| `--nlm` | Notebook-only pass: verify Tier 1 claims + citation grounding via MCP, skip web sources | `/verify --nlm 56-no-lassos-atlantic-slave-trade-origin-2026` |
| `--adversarial` | Cross-model skeptic pass: Gemini attacks the locked-candidate script for overclaims/strawmen/laundered quotes; each finding is then NLM-adjudicated (Step 7.9) | `/verify --adversarial 58-kurdistan-2026` |
| `--audio` | **POST-FILM BACKSTOP** (secondary to the Step 0 pre-film coverage gate). Diffs the DELIVERED transcript against the fact-checked script to catch narrator ad-libs/misreads that changed a claim/source/number at the mic (#59: script said "the plan *gave* 84%" → tape said "the *annexes show* 84%"). Recommended before `/publish`; not a hard gate | `/verify --audio 59-israel-palestine-partition-offer-2026` |

> **Deeper passes (kept as separate lightweight commands by design — context economy, so you don't load this 47 KB file to run a 5 KB pass; W2 2026-06-12):**
> - **`/verify-flow-nlm`** — narrative-flow verification + NotebookLM claim-query verification. The deeper claim-grounding pass that `--script` skips for context economy. Run when you want every claim NLM-checked, not just the Tier-1/contested ones.
> - **`/script-research-pass`** — full editor + head-of-research pass: paragraph-by-paragraph NLM verification (no context-economy skip), expository/predicate-drift, quote-card provenance, completeness, flow, prose polish, and script↔teleprompter lock discipline. The heaviest pass; use before locking a high-stakes script.

---

## FACT-CHECK WORKFLOW (`--script` or default)

Comprehensive fact-checking using the History vs Hype protocol.

### Step 0: Coverage Completeness Gate (HARD — the #59 fix, run this FIRST)

**Fact-checking is a PRE-FILM gate, and it only counts if it covers the WHOLE script.** The #59 failure (see `_CORRECTIONS-LOG.md`): `03-FACT-CHECK-VERIFICATION.md` was allowed to "pass" on the COLD OPEN only while Beats 2–8 were still a beat-map; the body prose was then written and filmed **without ever being cross-checked**, and two attribution errors (the "84% farmland" provenance, the "India" mis-credit) rode to tape. A fully fact-checked script means there is nothing left to catch after the camera rolls.

**Rule:** a script is NOT film-ready — and this command CANNOT return APPROVED — until **every beat/section of the delivered script has a verdict row in `03-FACT-CHECK-VERIFICATION.md`.** A section marked `PENDING-DRAFT`, `BEAT MAP`, or "prose to draft later" is an **uncovered beat = NOT film-ready**, no matter how clean the cold open is.

**Do this before anything else:**
1. Read the full `SCRIPT.md` (or `02-SCRIPT-DRAFT.md`) — enumerate every beat/section.
2. Read `03-FACT-CHECK-VERIFICATION.md` — which beats actually have verdict rows?
3. Any script beat with no fact-check rows → emit `[COVERAGE-GAP: Beat N unchecked]`. The verdict is **NOT film-ready** until those beats are drafted-to-prose AND run through Steps 2–7 below.

**Gate:** do not proceed to `/prep`, do not return APPROVED, and do not let the folder move to `_READY_TO_FILM/` with any open `[COVERAGE-GAP]`.

### Step 1: Identify the Script

- Read SCRIPT.md from project folder
- Or user pastes script content

### Step 2: Extract All Factual Claims

**Categories:**
- **Statistics & numbers** (dates, percentages, quantities, distances)
- **Direct quotes** (from historical figures, documents, politicians)
- **Historical events** (battles, treaties, laws, decisions)
- **Cause-effect claims** (X led to Y, X caused Z)
- **Attribution claims** (who said/wrote/did what)

### Step 3: Organize by Priority (then → Step 3.5 before checking sources)

**TIER 1 - SMOKING GUN EVIDENCE (Must verify before filming):**
- Primary document quotes
- Key statistics that form the thesis
- Viral quotes from current figures
- Claims that would discredit the video if wrong

**TIER 2 - SUPPORTING CLAIMS (Need 2+ sources):**
- Historical event details
- Timeline/date claims
- Attribution claims
- Academic consensus statements

**TIER 3 - CONTEXTUAL (Should verify):**
- Background information
- Comparative data
- Secondary quotes
- Common knowledge claims

**CONTESTED CLAIMS (Present both sides):**
- Any claim where sources disagree
- Claims that require "some historians argue..."
- Interpretation-dependent statements

### Step 3.5: Notebook Discovery (MCP)

Before running web searches, locate the project's NotebookLM notebook:

1. Call `mcp__notebooklm__notebook_list` — find notebooks matching the project slug or topic keywords (case-insensitive substring).
2. **Notebook found → MCP path** (Step 4A below).
3. **No match / MCP unavailable → Manual path** (Step 4B below).

---

### Step 4A: MCP-First Claim Verification (if notebook found)

For each **TIER 1** claim (and any TIER 2 claims without a clear source), dispatch a targeted `mcp__notebooklm__notebook_query`. Run in parallel — batches of up to 5:

```
CLAIM VERIFICATION — [Claim text]
The script asserts: "[exact wording from script]"
Is this claim supported by sources in this notebook?
Return:
(a) SUPPORTED / PARTIALLY SUPPORTED / NOT SUPPORTED / CONTRADICTED
(b) If supported: exact verbatim quote with author, title, page number
(c) Nuance or context the script is missing
(d) If contradicted: what the sources actually say
```

**Citation grounding scope** (per `feedback-notebook-citation-grounding.md`):
- Every blockquote in the script
- Title's mechanism word
- Central thesis verb
- Named-figure co-protagonist agency claims

**Verdict mapping → report status:**
- SUPPORTED + verbatim + page → ✅ VERIFIED (goes in "Verified Claims")
- PARTIALLY SUPPORTED → NEEDS VERIFICATION with the gap flagged
- NOT SUPPORTED / CONTRADICTED → INCORRECT OR MISLEADING

After MCP pass, run Step 4B only for any claims the notebook couldn't address.

---

### Step 4B: Check Against Source Hierarchy

**Most Reliable (Tier 1):**
- Primary documents (treaties, census data, government archives)
- Peer-reviewed academic publications
- Expert historians specializing in the topic

**Use with Caution:**
- Respected journalists with expertise
- International organization reports
- Declassified government documents (note potential bias)

**Flag These:**
- Opinion pieces without sources
- Claims without attribution
- Statistics without clear methodology
- "Common knowledge" that can't be verified

### Step 5: Run Simplification Detection

**CRITICAL: Scan script for simplification patterns**

Read `.claude/REFERENCE/FACT-CHECK-SIMPLIFICATION-RULES.md` and check for:

| Rule | Pattern | Severity |
|------|---------|----------|
| 1 | Territorial claims without boundaries/percentages | CRITICAL |
| 2 | Present tense for past positions | CRITICAL |
| 3 | Absolutist language without qualifiers | IMPORTANT |
| 4 | Statistics without context | IMPORTANT |
| 5 | Contested claims as facts | IMPORTANT |
| 6 | Quotes without specific attribution | CRITICAL |
| 7 | Complex events oversimplified | RECOMMENDED |
| 8 | Vague timelines | RECOMMENDED |

### Step 6: Generate Fact-Check Report

```markdown
# FACT-CHECK REPORT: [Script Title]

## SIMPLIFICATION FLAGS

### CRITICAL - Fix before filming
[List Rule 1, 2, 6 violations with suggested fixes]

### IMPORTANT - Should fix
[List Rule 3, 4, 5 violations with suggested fixes]

### RECOMMENDED - Improves clarity
[List Rule 7, 8 violations with suggested fixes]

## CULTURAL-ANCHOR & NEGATIVE-FINDING FLAGS (Step 7.6) — Fix before filming
[List any [CULTURAL-ANCHOR] that is CONTRADICTS-RESEARCH, UNSUPPORTED, or DATE-OR-CONTENT-UNVERIFIED, with the research negation quote and a category-accurate rewrite. HARD gate for the cold open.]

## VERIFIED CLAIMS (Source confirmed)
1. [Claim] - Source: [Exact citation]
2. [Claim] - Source: [Exact citation]

## NEEDS VERIFICATION (Missing or weak sources)
1. [Claim] - Issue: [What's missing/unclear]
2. [Claim] - Issue: [What's missing/unclear]

## INCORRECT OR MISLEADING
1. [Claim] - Problem: [What's wrong]
   Correction: [Accurate information]

## CONTESTED CLAIMS (Must acknowledge both sides)
1. [Claim] - Disagreement: [Who says what]
   Recommendation: [How to present fairly]

## MISSING CONTEXT
1. [Claim] - Additional context needed: [What's missing]

## OVERALL ASSESSMENT
- Coverage: every beat has fact-check rows? [YES/NO] (NO = not film-ready, Step 0)
- Ready to film? [YES/NO]
- Critical simplifications: [Number]
- Source issues: [Number]
- Recommendations: [What needs to be fixed/added]
```

### Step 7: Pre-Production Checklist

Before approving for filming:
- [ ] **Coverage completeness (Step 0) — EVERY beat of the delivered script has fact-check rows; no `PENDING-DRAFT`/beat-map section survives (HARD gate — the #59 fix; a cold-open-only pass is NOT film-ready)**
- [ ] Every load-bearing number/quote **classified + routed by KIND** (Step 7.8b) — kind-1 (contested/historical/atrocity/quote) academic-grounded, no `[WEB-NUMBER]` survivors; kind-2 academic-first else `[MODERN-ADMIN]` labeled; kind-3 routed to 7.6
- [ ] Every quote verified from original
- [ ] Contested claims clearly labeled
- [ ] At least 2 sources for each major point
- [ ] No logical fallacies in arguments
- [ ] Counter-evidence acknowledged where relevant
- [ ] **Simplification check complete** (all CRITICAL flags resolved)
- [ ] Territorial claims have specific boundaries/percentages
- [ ] Present-tense statements have temporal accuracy
- [ ] Attributions have specific sources (video timestamp, document, interview date)
- [ ] **Cultural-anchor / negative-finding check complete** (Step 7.6) — no script line asserts what verified research says did NOT happen; every "on [show] in [date]" / "most recently" anchor web-verified for BOTH date AND content; all `[CULTURAL-ANCHOR]` flags resolved (HARD gate for the cold open)
- [ ] **Argument & expository attribution check complete** (Step 7.7) — (A) every "PERSON read/argued/claimed/treats X" sentence (esp. debunk TARGETS) anchored to that person making THAT move, not just a source confirming X is true; (B) every "[Authority]/[the treaty] said/required/established X" expository sentence round-tripped — authority asserts the EXACT predicate (P2), not an adjacent one (no predicate drift); all `[ATTRIBUTION-ARG]` + `[ATTRIBUTION-EXPOSITORY]` flags resolved AND every trigger-grep entry has a row in 03-FACT-CHECK (`[COVERAGE-GAP]` cleared) (HARD gate for debunk-format)
- [ ] **Provenance & quote-card lock complete** (Step 7.8) — every on-screen quote card matches its displayed source character-for-character; no footnote-laundering (cited source reproduces the verbatim, not just footnotes it); every load-bearing on-screen quote re-queried THIS pass (never skipped for context-economy); **cross-checked against `_research/SOURCE-GENEALOGY.md` (verdict + verbatim + page match; no NO-LEDGER-ROW / LEDGER-MISMATCH; no SECONDARY-ONLY card framed as a document)**; all `[PROVENANCE]` flags resolved (HARD gate for on-screen quotes)
- [ ] **Number-grounding tier check complete** (Step 7.8b) — every load-bearing figure/quote classified kind 1/2/3 and routed; no kind-1 `[WEB-NUMBER]` web-only survivors (HARD gate); kind-2 `[MODERN-ADMIN]` labeled with tier; kind-3 `[MEDIA-NUMBER]` cross-checked via 7.6
- [ ] **Adversarial cross-model review complete** (Step 7.9, debunk-format) — Gemini skeptic pass run; every surviving finding routed to its 7.6/7.7/7.8 flag and **NLM-adjudicated** (Gemini raises, NLM confirms); any NLM-confirmed UNSUPPORTED/LAUNDERED/CONTRADICTS finding resolved; false alarms logged. No edit driven by an unadjudicated Gemini finding.

### Step 7.5: Attribution Mandate (for `X named/coined/termed Y` claims)

> See `memory/feedback-notebook-citation-grounding.md` §'verbatim verification ≠ attribution verification' for the why and the Hijab #52 origin.

After the Pre-Production Checklist (Step 7), run an attribution pass on the script. This step catches **cite-selection drift** — when the script names Scholar A for a term that multiple scholars use, and a more authoritative scholar in the sub-field exists.

#### Trigger phrases — grep the script for all of:

- `named` / `was named by` / `named it`
- `coined` / `coined the term`
- `termed` / `termed it`
- `called this` / `called it`
- `labelled this` / `labeled this`
- `the [Name] regime` / `the [Name] system` / `the [Name] framework` / `the [Name] principle` / `the [Name] effect`
- `the [Name] term` / `[Name]'s term`

#### Flag output

For each match, output:

```
[ATTRIBUTION-CHECK]: line N — "<matched-phrase>" — scholar=<Name>, term=<Y> — needs bidirectional NotebookLM round-trip.
```

#### Bidirectional round-trip (the verification step)

For each `[ATTRIBUTION-CHECK]` flag, run TWO NotebookLM queries via `mcp__notebooklm__notebook_query`:

- **Query A (origin direction):** *"Where does the term `<Y>` originate / who introduced it?"*
- **Query B (user direction):** *"Does `<Name>` use / describe / discuss `<Y>` in their work?"*

Both queries must return consistent results. If Query A surfaces a **different** scholar than `<Name>`, the attribution is at risk — either rewrite to the more-authoritative scholar, or downgrade the claim from origination to description.

#### Annotation requirement

Once verified, add an inline annotation to the script line:

- Confirmed originator: `[ATTRIBUTION-VERIFIED: <Name> originated <Y> per <NotebookLM source IDs>]`
- Downgraded: `[ATTRIBUTION-DOWNGRADED: <Name> describes but did not originate <Y>; primary cite is <Other-Name>]`

#### Shared-conceptual-space sub-class

When 2+ scholars work in cognate territory on the same concept (e.g., Geissinger + Llewellyn-Jones on veil-as-social-regulation), use the **most-authoritative-in-subfield** scholar, not just any scholar who uses the term. The bidirectional query surfaces this — it is a judgment call, not an automated rule.

#### Gate behavior

- **Format C (document-led / forensic):** Script cannot reach DRAFT-LOCKED with any `[ATTRIBUTION-CHECK]` lines that lack a corresponding `[ATTRIBUTION-VERIFIED]` or `[ATTRIBUTION-DOWNGRADED]` annotation. Hard gate.
- **Format A/B:** Attribution checks are a recommendation, not a gate. Surface flags; user decides.

---

### Step 7.6: Cultural-Anchor & Negative-Finding Reconciliation (load-bearing — runs before film)

> See `memory/feedback-cultural-moment-verification.md` for the why and the **two** #57 origins: (1) wrong JRE date/content in research; (2) the FILMED cold open asserting "Hancock brought up the Piri Reis map on Lex Fridman" when the same project's `01-VERIFIED-RESEARCH.md` stated twice "Piri Reis NOT named in 2024." A correct verbatim quote sitting next to a wrong script sentence is the failure this step exists to catch.

This step catches **two** drift modes Step 7.5 does not:
- **Cultural-moment decay** — "on [show] in [date]" / "most recently" / "again on" anchors that rot or were hallucinated upstream.
- **Negative-finding contradiction** — the script asserting something the verified research explicitly says did **not** happen.

#### Trigger phrases — grep the script for all of:

- `on [Show/Podcast]` — e.g. `on Lex Fridman`, `on Joe Rogan`, `on JRE`, `on [Capitalized Name] #N`
- `said on` / `told [Host]` / `brought it up` / `brought up` / `made the case on` / `repeated on` / `pushing it on`
- recency framing: `most recently` / `as recently as` / `again on` / `still` + appearance
- a person + a show/episode + `in [Month] [Year]`

#### Two checks per match

**Check 1 — Positive support.** Does `01-VERIFIED-RESEARCH.md` record that `<person>` discussed `<the specific topic/claim>` in `<that appearance>`? Capture the verbatim + source ID.

**Check 2 — Negative-finding contradiction (the new gate).** Search the research for any **negation** tied to that appearance: `NOT named`, `did not mention`, `generalized away from`, `dropped`, `not discussed`, `never says`. If the script asserts `<person>` said/brought up `<specific thing>` in an appearance the research records them **NOT** doing → **CONTRADICTION**.

**Web re-verification (both, always):** independently web-verify (a) the appearance happened on that date, (b) the specific topic was actually discussed there. Do not trust the brief — upstream agents hallucinate plausible cultural anchors.

#### Flag output

```
[CULTURAL-ANCHOR]: line N — "<matched phrase>" — person=<Name>, show=<Show>, date=<date>, claimed-topic=<topic>
  → status: SUPPORTED | UNSUPPORTED | CONTRADICTS-RESEARCH("<research negation quote>") | DATE-OR-CONTENT-UNVERIFIED
```

#### Annotation requirement

- Confirmed: `[CULTURAL-ANCHOR-VERIFIED: <Name> discussed <topic> on <Show> <date> per <source ID> + web]`
- Rewritten: `[CULTURAL-ANCHOR-CORRECTED: was "<old>"; research says <negation>; now states <category-accurate claim>]`

#### Gate behavior

- **Cold open + any modern-relevance / "who pushes this today" beat: HARD gate.** The script cannot be approved for filming with an unresolved `[CULTURAL-ANCHOR]` flag. A script line may **not** assert a person discussed a specific topic in an appearance the research records them **not** discussing. This is the negative-finding rule: research that says "X did NOT do Y" is reconciled against the script the same way positive quotes are.
- **Post-film catch:** if the offending line is already filmed, the fix is a **VO pickup**, never a B-roll patch (the audio actively asserts something false — see `memory/feedback-html-deck-broll.md` decision rule).

---

### Step 7.7: Argument & Expository Attribution Audit (strawman + predicate-drift gate — load-bearing for debunks)

> See `memory/feedback-attribution-audit.md` for the why and the #57 cağferiye + Ptolemy/Ortelius origins. This catches TWO attribution-drift modes that 7.5 (who-coined-a-term) and 7.6 (who-said-it-on-a-show) do not: **(A) who actually holds this argument** (the debunk target), and **(B) does this named authority actually assert this exact proposition** (any expository authority — Ptolemy, Aristotle, a treaty, a legal code).

**The two failures:**
- **(A) Argument attribution (target side).** The script says "PERSON read / argued / claimed / treats X as Y," every component quote is verbatim-true, so it passes the quote-level gate — but no source shows that *person* making that *move*. **Validated-quote ≠ validated-attribution.** On #57, "Hapgood read that word [cağferiye]… and Hancock after him… as the fingerprint of the lost civilization" was false on both men — yet every atom was real. Highest risk is the **TARGET side of a debunk**; misattribution there is a strawman.
- **(B) Expository attribution (named-authority side) — predicate drift.** The script assigns a specific proposition to a named non-target authority ("Ptolemy's geography said one had to exist, to balance the globe"), the name is real and the topic is real — but the source supports an **adjacent** proposition, not that one. On #57 the research pinned Ptolemy to "land encircles water / enclosed Indian Ocean" (P1); the script welded his name onto "had to exist to **balance the globe**" (P2 — actually the Aristotelian symmetry argument, popularized by Ortelius). No source has Ptolemy asserting P2. **The non-target named-authority side is not low-risk — it is low-salience**, so it gets less scrutiny while still asserting falsifiable history on screen.

#### Trigger phrases — grep the script for ALL of (this grep list is also the enumerator for the completeness check below):

**Class A — argument/target:**
- `read [it/that/the …] as` / `reads … as` / `treats … as`
- `argued` / `argues` / `claimed` / `claims` / `says` / `said that` / `believed`
- `to [him/her/them] …` / `for [Name], …` (assigning a position)
- `[Name]'s claim` / `[Name]'s argument` / `the [Name] reading`
- `built [his/the] … on` / `rests on` / `comes down to` (when load-bearing for a named person)

**Class B — expository authority (NEW):**
- `[Authority]'s [geography/work/theory/map/law/text] said / required / held / shows / established / tells us`
- `according to [Authority / the treaty / the document / the code]`
- `[the treaty / the text / the law] says / states / requires X` (where X is **paraphrased**, not a quote card — quote cards go to 7.8)
- `[Authority] said / argued / required …` where Authority is a historical/textual source the script treats as established background (NOT the debunk target)

#### Checks per match

**Check 1 — Person-said-it (Class A).** Does an NLM source show **that person making this move** (ideally verbatim from their own work)?
**Check 2 — Fact-true-only trap (Class A).** Is the only backing a source confirming the CLAIM is independently true (not that the person asserted it)? If yes → **unsupported**, even with a real quote attached.
**Check 3 — Predicate drift (Class B — the welding catch).** Pin the exact proposition the script puts in the authority's mouth (P2). Does a source show **that authority asserting P2** — or only an **adjacent** proposition P1? If research/sources support P1 but the script says P2, it is **ADJACENT-ONLY (drift)** even when both P1 and P2 are independently true. Re-attribute P2 to its real holder, or rewrite to the predicate the source actually supports. (Worked example: Ptolemy P1 "land encircles water" → script P2 "had to exist to balance the globe" → real holder = Aristotelian symmetry / Ortelius.)

#### Round-trip (NLM) — batch by person/authority

Group every Class-A and Class-B hit by the named person/authority and issue **one query per authority** (keeps 15-30 attributions from becoming 30 sequential calls):

> **Class A:** *"Does `<Name>` actually `<verb>` `<X>` in their own work — quote verbatim, or 'NOT FOUND'? Do not infer; do not substitute a source that merely confirms X is true."*
> **Class B:** *"Does `<Authority>` assert each of these exact propositions in their own work — for each, quote verbatim or answer 'NOT FOUND' / 'ADJACENT: <what they actually say>'. Do not infer; do not substitute a source that confirms the proposition is independently true."*

#### Flag output

```
[ATTRIBUTION-ARG]:        line N — "<phrase>" — person=<Name>, claim=<X>
  → status: PERSON-SAID-IT(<src>) | FACT-TRUE-ONLY | UNSUPPORTED
[ATTRIBUTION-EXPOSITORY]: line N — authority=<A>, script-predicate=<P2>, source-supports=<P1 or NONE>
  → status: AUTHORITY-ASSERTS-IT(<src>) | ADJACENT-ONLY(drift) | UNSUPPORTED
```

#### Annotation requirement

- Confirmed (A): `[ATTRIBUTION-ARG-VERIFIED: <Name> <verb> <X> per <NLM src>]`
- Confirmed (B): `[ATTRIBUTION-EXPOSITORY-VERIFIED: <Authority> asserts <P2> per <NLM src>]`
- Rewritten (A): reframe the overclaim as **an appearance the next lines debunk, attributed to no named proponent**. Annotate `[ATTRIBUTION-ARG-CORRECTED: was "<old>"; <Name> never makes this move; reframed as unattributed appearance]`.
- Rewritten (B): re-attribute to the real holder or rewrite to P1. Annotate `[ATTRIBUTION-EXPOSITORY-CORRECTED: was "<A> said <P2>"; source supports only <P1>; re-attributed to <real holder> / rewritten to <P1>]`.

#### Gate behavior

- **Debunk-format — Class A (target attribution): HARD gate.** Cannot lock with a FACT-TRUE-ONLY or UNSUPPORTED attribution to a real person.
- **Debunk-format — Class B (expository authority): HARD gate, NO load-bearing exemption.** **Every** expository attribution round-trips; cannot lock with an ADJACENT-ONLY(drift) or UNSUPPORTED status. (The scholar's *own-analysis* quotes remain low risk — Class B is about propositions put in a named authority/document's mouth, not a scholar describing their own finding.)
- **Post-film:** an unsupported attribution OR a drift on the delivered audio = a **VO pickup** (or cut), never a B-roll patch — the audio asserts something false. Template: #57 `VO-PICKUP-cagferiye.md` + `ATTRIBUTION-AUDIT.md`.
- **Format A/B:** recommendation; surface flags, user decides.

#### Completeness reconciliation (the enabler that hid the Ptolemy line)

The #57 Ptolemy line **never entered `03-FACT-CHECK-VERIFICATION.md` at all** (grep = 0 rows) — so no line-vs-source check ever ran on it. The Class-A + Class-B trigger grep above is the **master enumerator**: **every entry it returns must map to a verdict row in `03-FACT-CHECK-VERIFICATION.md`.** Any grep hit with no corresponding fact-check row is itself a flag (`[COVERAGE-GAP]: line N — attribution sentence not in 03-FACT-CHECK`) and blocks lock in debunk-format until rowed and adjudicated. Manual cross-check, no tooling.

---

### Step 7.8: Provenance & Quote-Card Verbatim Lock (load-bearing for on-screen quotes)

> See `memory/feedback-attribution-audit.md` §provenance and the #58 Kurdistan origin. Where 7.7 asks "did the person make this move," 7.8 asks "**does the cited source actually contain these exact words, on the page claimed?**" — and "**does the on-screen card match the source it displays?**"

**The failure (#58):** three Act-4 quotes were tagged "NLM-grounded, verbatim + p.401 (McDowall)." On re-query the verbatim **wasn't in McDowall at all** — he only *footnoted* the primary source (Village Voice / Vanly). Two were also misquoted ("a uniquely cynical enterprise" — "uniquely" not in the source; "hoped our clients would not prevail" — a paraphrase in quote marks). It passed because the fact-check trusted the grounding tag instead of re-querying. The shortcut "context-economy: C##-tagged, not re-queried, trail exists" is exactly what hid it.

#### Three checks

**A — Footnote-laundering.** For any quote attributed to a primary source (treaty, report, named figure, document), confirm the in-notebook source **reproduces** the verbatim — not merely *cites or footnotes* it. A primary quote reached only through a scholar's footnote is **NOT grounded**; flag `[S→P-FOOTNOTE]` and either acquire a reproducing source or downgrade to paraphrase. (NotebookLM tip: when the answer surfaces footnotes/bibliography rather than body text containing the words, that's the tell.)

**B — Quote-card verbatim lock.** Every **on-screen quote card** must match the source it displays **character-for-character** (wording, ellipses, brackets). Embellishments ("uniquely"), paraphrases-in-quote-marks, and merged sentences all fail. Trim only with honest ellipsis.

**C — Genealogy ledger cross-check.** If `_research/SOURCE-GENEALOGY.md` exists (produced by `/research` Step 8, the `primary-source` skill), it is the single provenance source of truth — **cross-check each on-screen card against its ledger row instead of re-deriving**: the card's verbatim + page + source must match the row's, and the row's verdict (`PRIMARY-GROUNDED` / `PRIMARY-VIA-TESTIMONY` / `SECONDARY-ONLY`) must match how the script frames it (a `SECONDARY-ONLY` claim framed on screen as "the document shows" is a `[PROVENANCE]` fail — re-label to named-scholar attribution). **Any on-screen card with no ledger row is itself a flag** (`NO-LEDGER-ROW`) — run the genealogy for it (spawn `primary-source-hunter`) or add the inline-confirmed row before lock. If the ledger does NOT exist (older project, or genealogy step not yet run), fall back to checks A/B and note that the ledger is absent.

#### No-skip rule (the one that bit #58)

**Load-bearing on-screen quotes are NEVER exempted from re-query for context-economy.** "Already C##-tagged / verified in a prior session / trail exists" is not sufficient for a quote that will appear on screen. Re-query each one against the notebook THIS pass and confirm the source reproduces it.

#### Flag output

```
[PROVENANCE]: line N — "<quote>" — attributed to <source/p.> 
  → status: REPRODUCED(<src, p.>) | FOOTNOTE-LAUNDERED(<scholar only cites it>) | MISQUOTED("<actual verbatim>") | NOT-IN-NOTEBOOK
           | NO-LEDGER-ROW(<on-screen card absent from SOURCE-GENEALOGY.md>) | LEDGER-MISMATCH(<verdict/verbatim/page ≠ ledger row>)
```

#### Gate behavior

- **Any on-screen quote card: HARD gate.** Cannot lock with a FOOTNOTE-LAUNDERED / MISQUOTED / NOT-IN-NOTEBOOK / LEDGER-MISMATCH card, or an on-screen card framed as a document whose ledger verdict is SECONDARY-ONLY. Correct to the reproduced verbatim, re-anchor the citation to the reproducing source, re-label secondary-only claims to named-scholar attribution, or downgrade to paraphrase.
- **NO-LEDGER-ROW** (ledger exists but this on-screen card isn't in it): run the genealogy for it (`/research` Step 8 / spawn `primary-source-hunter`) or add the inline-confirmed row; don't lock an on-screen card that hasn't been traced.
- **Post-film:** a misquoted/ungrounded on-screen card = re-cut the card art (and a VO pickup if it's also spoken). Template: #58 `03-FACT-CHECK` resolution + #57 `VO-PICKUP-cagferiye.md`.

---

### Step 7.8b: Number-Grounding Tier Check (route each figure to the right source tier)

> See `memory/feedback-historical-number-grounding.md`. The #62 origin: a web ("Wikipedia/ENRS") figure was used to ground a number, and a web quote landmine had to be quarantined — the exact failure the "History vs Hype" premise forbids. This step doesn't add a new gate; its **only job is to CLASSIFY each load-bearing number/quote by KIND and route it to the gate that already handles that kind.** Classify by the KIND of fact, not its age (a 1947 admin count and a 2016 vote are both administrative; a recent death toll is still historical).

#### Trigger — grep the script + `01-VERIFIED-RESEARCH.md` for load-bearing figures/quotes:
death tolls, casualty counts, quantities, percentages, distances, dates, and any verbatim quote. (Round background color, not the load-bearing spine numbers.)

#### Classify each into one of three KINDS, then route:

- **Kind 1 — Contested / historical / atrocity figure, or ANY quote.** (death toll, who-killed-whom, verbatim.) → **academic / NLM / primary ALWAYS.** If its only source is web/Wikipedia/news → `[WEB-NUMBER]` **HARD flag** → re-ground via NLM (Step 4A) or quarantine. Routes into the existing provenance machinery (7.8).
- **Kind 2 — Administrative fact of record.** (official count, vote tally, treaty text, event date.) → **academic-preferred**; authoritative-web fallback (ENRS / gov / primary registry) **only when no academic source carries it**, labeled `[MODERN-ADMIN: web-ok — <tier>]`. Try the notebook first even here.
- **Kind 3 — Recent / media number.** (current-events figure too new for academic press.) → route into the **existing Step 7.6 cultural-anchor gate** (attribute to the outlet · cross-check 2+ independent outlets · label "reported" not "established" · re-verify week-of-film). No new gate.

#### Flag output
```
[WEB-NUMBER]: line N — "<figure/quote>" — kind=1 — web-only source <url> → re-ground via NLM or quarantine
[MODERN-ADMIN]: line N — "<figure>" — kind=2 — no academic source; authoritative web <tier> → labeled, OK
[MEDIA-NUMBER]: line N — "<figure>" — kind=3 → routed to Step 7.6 (attributed + cross-checked + reverify-week-of-film)
```

#### Gate behavior
- **Kind 1 web-only = HARD gate** (same as `[PROVENANCE]`): cannot lock. Re-ground or quarantine.
- Kind 2/3 are routing labels, not blocks — but a kind-3 figure that fails the 7.6 cross-check IS blocked by 7.6.

---

### Step 7.9: Adversarial Cross-Model Review (Gemini-as-skeptic → NLM-adjudicated)

> Origin: 2026-06-03, ecosystem "dual-model review" practice (Claude writes → a *different* model reviews → feedback incorporated), adapted to this channel's rigor. Rationale: Claude wrote and self-verified the script, so Claude carries confirmation bias toward its own phrasing. A fresh model with no stake in the wording surfaces overclaims Claude rationalized. This step does **not** replace 7.5–7.8 — it **feeds** them: Gemini *raises suspicion*, NotebookLM *adjudicates*.

**Runs as a flag (`--adversarial`) or automatically before lock on debunk-format scripts.** Advisory on Format A/B.

#### Hard constraint — Gemini raises, NLM confirms (never the reverse)

Per `feedback-historian-mode.md` and `feedback-gemini-cli-down-fallback.md`: **a Gemini finding is a hypothesis, never evidence.** Gemini output may NOT become a script claim, a citation, or a "verified" status. Every adversarial finding that survives triage is converted into an existing 7.5–7.8 flag and **re-queried against NotebookLM** before any edit. Gemini cannot exonerate the script either — "Gemini found nothing" is not a pass.

#### Inputs

- The locked-candidate script (`SCRIPT.md` / `02-SCRIPT-DRAFT.md`).
- `01-VERIFIED-RESEARCH.md` (so Gemini can check script-vs-research negative findings, the 7.6 failure mode).

#### Model

Gemini **Flash** default (`feedback-gemini-model-default.md`). This pass is reasoning-heavy, so for **load-bearing debunk scripts**, offer Pro and ask approval first — do not silently upgrade.

#### The adversarial prompt (target the known failure modes, not generic "fact-check")

```
You are a hostile peer reviewer trying to GET THIS VIDEO RETRACTED. You have the
script and the channel's own verified-research file. Find the script's weakest
attributions and overclaims. Do NOT rewrite. Do NOT confirm anything as true —
only flag what a motivated critic would attack. For each finding give: line/quote,
attack type, and the one question that would expose it.

Attack types to hunt (ignore everything else):
1. STRAWMAN — script says a named TARGET "argued/read/treats X as Y" but that's
   the script's characterization, not a position the target demonstrably holds.
2. OVERCLAIM — absolute/universal wording ("always", "never", "the entire", "all")
   the evidence underneath can't carry.
3. LAUNDERED QUOTE — a primary-source quote that the script likely reached only
   through a scholar who *footnotes* it, not reproduces it.
4. ANCHOR DECAY — "on [show] in [date]" / "most recently" claims that may be stale,
   wrong, or contradicted by the verified-research file.
5. RESEARCH CONTRADICTION — any script line asserting something the attached
   verified-research file says did NOT happen.

Output a numbered list. Each item: [TYPE] line N — "quote" — exposing question.
If you genuinely find nothing in a category, say so. Be ruthless and specific.
```

Invoke (mirror `/editing-guide` Phase 4):
```bash
gemini -m gemini-2.5-flash -p "<prompt + script + research>" --yolo \
  > [project]/_gemini-output/adversarial-review-<timestamp>.md
```

**CLI-down fallback** (`feedback-gemini-cli-down-fallback.md`): if `gemini` errors, output the paste-ready web-UI prompt for the user; never silently swap to another model.

#### Triage → route into existing gates (do NOT trust Gemini's verdicts)

For each Gemini finding:
1. **Discard** if it misreads the script or attacks a non-load-bearing line. (Gemini over-fires; that's fine.)
2. **Convert** surviving findings into the matching existing flag and run that gate's NLM round-trip:
   - STRAWMAN / OVERCLAIM on a named debunk TARGET → `[ATTRIBUTION-ARG]` (Step 7.7 Class A round-trip)
   - PREDICATE DRIFT on a named authority/document ("X said P2" but source supports only P1) → `[ATTRIBUTION-EXPOSITORY]` (Step 7.7 Class B round-trip)
   - LAUNDERED QUOTE → `[PROVENANCE]` (Step 7.8 re-query: does the in-notebook source *reproduce* it?)
   - ANCHOR DECAY → `[CULTURAL-ANCHOR]` (Step 7.6 web + research check)
   - RESEARCH CONTRADICTION → 7.6 negative-finding check
3. The finding's status is whatever **NotebookLM** returns — not what Gemini claimed.

#### Report section (append to 03-FACT-CHECK-VERIFICATION.md)

```markdown
## ADVERSARIAL CROSS-MODEL FINDINGS (Step 7.9)

**Reviewer model:** gemini-2.5-flash | **Raised:** [N] | **Survived triage:** [M] | **Confirmed by NLM:** [K]

| # | Gemini attack | Routed to | NLM verdict | Action |
|---|---------------|-----------|-------------|--------|
| 1 | [TYPE] "quote" | [ATTRIBUTION-ARG] | UNSUPPORTED | reframe per 7.7 |
| 2 | [TYPE] "quote" | [PROVENANCE] | REPRODUCED p.X | no change (false alarm) |
```

#### Gate behavior

- **Debunk-format:** any Gemini finding that NLM **confirms** as UNSUPPORTED / FOOTNOTE-LAUNDERED / CONTRADICTS-RESEARCH inherits that gate's HARD block (via 7.6/7.7/7.8). Gemini findings that NLM clears are logged as false alarms, no edit.
- **Format A/B:** advisory — surface the table, user decides.
- **Never** let an unadjudicated Gemini finding drive an edit, and never let "Gemini found nothing" substitute for the 7.5–7.8 passes.

#### Append the verdict to the judge-verdict ledger

Append one line to `channel-data/calibration/JUDGE-VERDICT-LOG.md` (create it from its header template if it doesn't exist yet) summarizing this 7.5–7.9 attribution/provenance pass — these are real LLM-as-judge calls (Claude's own 7.5–7.8 verdicts, plus the Gemini-raises/NLM-confirms triage at 7.9) that otherwise only exist in the chat transcript:

```
| [today's date] | /verify Steps 7.5-7.9 | [video slug] | raised=[N] survived-triage=[M] nlm-confirmed=[K] | [any HARD gate tripped: yes/no] |
```

Lightweight, no new tooling — an append, matching `/script` Step 4b (`docs/LLM-CRAFT-UPGRADE-PLAN.md` D3). This is what lets attribution-judge drift and false-alarm rate become measurable across videos instead of evaporating each session.

---

### Output Location

`video-projects/[project]/03-FACT-CHECK-VERIFICATION.md`

**Proactive suggestion:** "Fact-check complete. [APPROVED/X issues to fix]. Run `/prep` for filming preparation."

---

## POST-FILM VO DEVIATION BACKSTOP (`--audio`)

> **Secondary to Step 0 — this is a backstop, not the main gate.** The primary control is the pre-film coverage gate (Step 0): a fully fact-checked *complete* script means there is nothing left to catch after filming. This mode covers only the one class Step 0 cannot reach: **narrator deviations at the mic** — ad-libs, misreads, dropped qualifiers between the fact-checked script and the delivered audio. #59 origin: the locked script said "the plan *gave* 84%"; the delivered VO said "the *annexes show* 84%" — a false attribution invented at filming, not in the script. (If a beat reaches filming never fact-checked at all, that is a **Step 0 failure**, not this — fix the pre-film gate.)

**Run:** after filming, on the clean transcript, before `/publish`. Recommended, **not a hard gate** (Step 0 is the hard gate).

### Inputs
- The **cut `.srt`** (the rough-cut caption = what is actually IN the video) — **preferred**. The uncut `CLEAN-AUDIO-TRANSCRIPT-*.txt` has different takes + auto-transcription errors, so never rely on it for delivered wording (the #59 lesson: the uncut heard "annexes" / "India"-only where the cut had "documents and access" / "India, Iran, and Yugoslavia").
- The **locked** `SCRIPT.md` / `TELEPROMPTER.md` (the fact-checked baseline to diff against).
- `01-VERIFIED-RESEARCH.md` for anything that turns out to differ.

### Process
1. **Diff transcript vs locked script — offload to a cheap subagent** (Haiku/Sonnet; keeps main context lean, see `.claude/AGENT-ORCHESTRATION.md`). Bounded task: line up delivered audio against the locked script and return every place the delivered wording **changed a claim, a source, a number, or an attribution verb** ("the plan gave" → "the annexes show"). Ignore filler/retake stumbles. Return: `timestamp | script wording | delivered wording | what changed`.
2. **Adjudicate the deltas — Opus, do NOT offload.** (The #59 India line was rubber-stamped by a review that reasoned from memory — never clear a delta from memory.) For each meaning-changing delta, check against `01-VERIFIED-RESEARCH.md`, and if load-bearing/contested RAW-READ the source (`mcp__notebooklm__source_get_content` → grep, per `reference-nlm-raw-read-verification`). Classify: SOURCE-DRIFT / PREDICATE-DRIFT / MIS-CREDIT / NUMBER-MISMATCH / benign-rewording.
3. **Output** `video-projects/[project]/VO-ATTRIBUTION-AUDIT.md` (table: `ts | delivered sentence | delta type | research says | fix`); feed each into the editing-guide pickup list.

### Gate behavior
- A meaning-changing deviation on load-bearing audio = a **VO pickup (or cut), never a B-roll/caption patch** (`memory/feedback-broll-patch-for-postfilm-slips`) — the audio asserts something false. Benign rewordings pass.
- This is a backstop; it does **not** substitute for Step 0. A script that reaches this stage with un-fact-checked beats has already failed the real gate.

---

## DELTA VERIFICATION (`--delta`)

Verify only NEW or CHANGED claims in a script — not blanket re-verification. Use after collaborative editing rounds where the user has added rough notes, rewritten sections, or integrated new material.

### When to Use

- After `/script --collaborate` rounds where user added unverified material
- After any script revision that introduces new claims
- When a script is mostly verified but sections were rewritten
- **NOT for first-pass verification** — use `--script` for that

### Process

#### Step 1: Load Both Files

Read from the project folder:
- `02-SCRIPT-DRAFT.md` (current script)
- `01-VERIFIED-RESEARCH.md` (verified claims database)

#### Step 2: Diff — Three Categories

Compare every factual claim in the script against verified research. Flag claims in three categories:

**Category A — NEW CLAIMS (not in verified research)**
Claims the user added that have no corresponding entry in 01-VERIFIED-RESEARCH.md. These are the highest risk — often from memory, blog posts, or rough notes.

**Category B — CONTRADICTING CLAIMS**
Claims that conflict with what's in verified research. Often from the user misremembering details (e.g., "god of love" when source says "primordial cosmic force").

**Category C — SECONDARY WHERE PRIMARY EXISTS**
Places where the script quotes a historian's summary, but the primary source they're summarizing is available in the notebook/verified research. The primary source may be more powerful.

#### Step 3: Generate Delta Report

```markdown
# DELTA VERIFICATION: [Project Name]

**Script:** 02-SCRIPT-DRAFT.md
**Verified Research:** 01-VERIFIED-RESEARCH.md
**Date:** [Today]
**Claims checked:** [Total in script]
**Already verified:** [Number matching verified research]
**Flagged for review:** [Number]

## CATEGORY A — NEW CLAIMS (Not in Verified Research)

### Claim A1
**Script says:** "[exact quote from script]"
**Section:** [Act/section where it appears]
**Status:** UNVERIFIED
**Action:** Verify via NotebookLM or cut

### Claim A2
[...]

## CATEGORY B — CONTRADICTIONS

### Claim B1
**Script says:** "[exact quote from script]"
**Verified research says:** "[exact quote from 01-VERIFIED-RESEARCH.md]"
**Source:** [Citation from verified research]
**Action:** Fix script to match verified source

## CATEGORY C — PRIMARY SOURCE AVAILABLE

### Claim C1
**Script says:** "[historian's summary]"
**Primary source available:** "[exact quote from primary source in verified research]"
**Citation:** [Primary source reference]
**Action:** Consider replacing with primary source + interpretation

## SUMMARY

- Category A (new, unverified): [X] claims → verify or cut
- Category B (contradictions): [X] claims → fix now
- Category C (primary available): [X] claims → consider upgrading
- Already verified: [X] claims → no action needed
```

#### Step 4: Targeted NotebookLM Queries (MCP-native)

For Category A claims, call `mcp__notebooklm__notebook_query` directly — one query per claim, run in parallel (batches of up to 5). Use the project's existing notebook (locate via `mcp__notebooklm__notebook_list` first).

```
DELTA VERIFICATION — [Claim text]
The script adds this new claim: "[exact wording]"
Is this claim supported by sources in this notebook?
Return:
(a) SUPPORTED / PARTIALLY SUPPORTED / NOT SUPPORTED / CONTRADICTED
(b) If supported: exact verbatim quote with author, title, page number
(c) If not supported or contradicted: what the sources say instead
```

**Result routing:**
- SUPPORTED + page → move to Category A sub-status "VERIFIED VIA MCP", update `01-VERIFIED-RESEARCH.md`
- PARTIALLY SUPPORTED → flag in delta report with gap described
- NOT SUPPORTED / CONTRADICTED → flag for cut

**Fallback (MCP unavailable):** generate prompts the user can paste into NotebookLM browser, then run `/verify --extract-nlm <output-file>` to extract citations.

#### Step 5: Update Files

- Fix Category B contradictions in the script immediately
- For Category A: update 01-VERIFIED-RESEARCH.md with newly verified claims, or flag for cutting
- For Category C: suggest primary source replacements (user decides)

### Output Location

Terminal summary + `DELTA-VERIFICATION.md` in project folder (not the full 03-FACT-CHECK report — that's for `--script`).

### How It Differs from `--script`

| | `--script` | `--delta` |
|---|-----------|-----------|
| **Scope** | Every claim in script | Only new/changed claims |
| **When** | First verification pass | After collaborative editing |
| **Simplification check** | Full 8-rule scan | No (assumes already done) |
| **Output** | 03-FACT-CHECK-VERIFICATION.md | DELTA-VERIFICATION.md |
| **NotebookLM queries** | Blanket verification | Targeted per-claim |
| **Time** | Full session | Quick pass |

---

## CLAIMS EXTRACTION (`--extract`)

Extract factual claims from YouTube video transcript for systematic fact-checking.

### Input

- YouTube video URL (will fetch transcript)
- Or path to transcript file (.vtt, .srt, .txt)

### Process

1. **Fetch/read transcript**
2. **Extract ALL factual claims:**
   - Dates (when events occurred)
   - Statistics (death tolls, population figures, numbers)
   - Quotes (who said what, with attribution)
   - Cause-effect relationships ("X caused Y")
   - Historical interpretations (contested claims)
   - Geographic claims (territorial boundaries, locations)

3. **Categorize by priority:**
   - **Priority 1:** Major claims central to video's argument
   - **Priority 2:** Supporting claims and context
   - **Priority 3:** Minor details

4. **Note red flags:**
   - Claims without sourcing
   - Contested framing presented as settled
   - Potential misattributions

### Output

```markdown
# Claims Extraction: [Video Title]

**Video:** [Title]
**URL:** [YouTube URL]
**Creator:** [Channel name]
**Duration:** [Length]
**Extraction Date:** [Today]

## PRIORITY 1: Major Claims (Must Fact-Check)

### Claim 1.1: [Category]
**Exact Quote:** "[Verbatim from video]"
**Timestamp:** [MM:SS]

**Factual Elements to Verify:**
- Date: [Specific date claimed]
- Number: [Specific statistic]
- Source attribution: [If they cite a source]

**Verification Needed:**
- [ ] Verify date accuracy
- [ ] Verify number/statistic
- [ ] Check if source cited actually supports claim

**Potential Red Flags:**
- [Any obvious issues]

[Continue for all claims...]

## SUMMARY

**Total Claims:** [Number]
- Priority 1: [X] major claims
- Priority 2: [X] supporting claims
- Priority 3: [X] minor details
```

### Output Location

`video-projects/[project]/CLAIMS-TO-VERIFY.md`

---

## NOTEBOOKLM CITATION EXTRACTION (`--extract-nlm`)

Extract structured citations from NotebookLM chat output using the Python CLI tool.

### Usage

```bash
python tools/citation_extractor.py INPUT_FILE [--output FILE] [--format detailed|compact] [--stats-only]
```

### Process

1. User copies NotebookLM chat response into a `.txt` or `.md` file
2. Tool parses citation markers ([1], [2]) and source references
3. Produces NOTEBOOKLM-EXTRACTIONS.md with claims in VERIFIED-RESEARCH.md format
4. User reviews extractions and copies verified claims to 01-VERIFIED-RESEARCH.md

### Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `input` | Yes | - | Path to file with pasted NotebookLM output |
| `--output` | No | Same dir as input | Output file path |
| `--format` | No | detailed | Output format: detailed (full checklist) or compact (table) |
| `--stats-only` | No | - | Print stats without writing file |

### Output Format

Each extracted citation includes:
- Claim text (cleaned of citation markers)
- Source with page number
- Verification status (starts as NEEDS REVIEW)
- Checklist for verification steps

**Example output:**
```markdown
### Claim 1
**Claim:** Roman literacy rates were approximately 10-15% of the population
**Source:** Harris, William V, Ancient Literacy, p. 22
**Status:** NEEDS REVIEW

**Verification:**
- [ ] Verify claim accuracy against source
- [ ] Confirm page number
- [ ] Update status: VERIFIED / UNVERIFIABLE / PARTIALLY TRUE
- [ ] Copy to 01-VERIFIED-RESEARCH.md when verified
```

### Supported Citation Formats

The tool recognizes multiple NotebookLM output formats:
- **[1], [2] markers** with source legend at bottom (most common)
- **SOURCES:** section with numbered list
- **Inline parenthetical** citations

### Optimized Prompts

For best extraction results, use prompts from `.claude/REFERENCE/NOTEBOOKLM-RESEARCH-PROMPTS.md` — designed to produce extractor-compatible output with [N] citation markers and page numbers.

### Output Location

`NOTEBOOKLM-EXTRACTIONS.md` in same directory as input file (or custom path with `--output`)

---

## TRANSLATION VERIFICATION (`--translation`)

Verify translated documents before filming to catch discrepancies and missing annotations.

### Usage

```
/verify --translation [project]                           # Audit existing translation output
/verify --translation [project] --scholarly-summary FILE  # Compare against scholarly description
/verify --translation [project] --document-name "Name"   # Compare against Claude's knowledge
```

### Modes

**Audit mode (default):** Reads existing translation output and checks completeness.
- Pure Python analysis — no API key needed
- Cross-check results present
- Legal annotations exist
- Surprise detection complete (if enabled)
- No pending placeholders

**Scholarly comparison:** Optional verification against academic descriptions of the document.
- `--scholarly-summary FILE`: User provides file with scholarly description (e.g., "Article 3 establishes X, Article 5 prohibits Y")
- Claude Code (this command itself) executes the LLM comparison natively — no API key needed
- Flags omissions or contradictions
- Uses `TranslationVerifier.build_scholarly_comparison_payload()` to build prompt, then Claude Code executes it

**Knowledge comparison:** Optional verification against Claude's training knowledge.
- `--document-name "Name"`: Claude Code compares translation against known scholarly descriptions
- Uses `TranslationVerifier.build_knowledge_comparison_payload()` to build prompt, then Claude Code executes it

### Process

1. Locate translation output file in project folder (formatted output from /translate)
2. Instantiate TranslationVerifier (no API key or model argument needed):
   ```python
   from tools.translation.verification import TranslationVerifier
   verifier = TranslationVerifier()
   ```
3. Run audit mode (pure Python):
   ```python
   result = verifier.verify_translation(translation_file='[path]', mode='audit')
   ```
4. For scholarly comparison: build payload, execute LLM call natively as Claude Code, pass result back:
   ```python
   payload = verifier.build_scholarly_comparison_payload(translation_text, scholarly_summary)
   # Claude Code executes LLM call using payload['system_prompt'] and payload['user_prompt']
   scholarly_result = verifier.parse_scholarly_comparison_response(claude_response)
   result = verifier.verify_translation(translation_file='[path]', scholarly_result=scholarly_result)
   ```
5. Generate TRANSLATION-VERIFICATION.md with full findings
6. Print condensed summary to terminal

### Output Format

Terminal summary:
```
TRANSLATION VERIFICATION: [Document Name]
VERDICT: GREEN / YELLOW / RED

Top issues:
1. [Issue description]
2. [Issue description]
3. [Issue description]

Full report: video-projects/[project]/TRANSLATION-VERIFICATION.md
```

Full report sections:
- **Verdict:** GREEN/YELLOW/RED with reasoning
- **Completeness Check:** Cross-check status, annotation coverage, surprise detection status
- **Discrepancy Analysis:** HIGH/MEDIUM/LOW severity issues from cross-check
- **Annotation Coverage:** % of legal terms with definitions, missing terms list
- **Scholarly Comparison:** (if --scholarly-summary used) Alignment check, omissions, contradictions
- **Recommendation:** Proceed to filming / Revise translation / Major issues - retranslate

### Verdict Interpretation

| Verdict | Meaning | Next Step |
|---------|---------|-----------|
| GREEN | No significant issues | Proceed to script generation |
| YELLOW | Minor discrepancies or gaps | Review flagged sections, decide if acceptable |
| RED | Significant problems | Revise translation before filming |

### Output Location

`video-projects/[project]/TRANSLATION-VERIFICATION.md`

### After Completion

**When verification returns GREEN:**
> "Translation verified! No significant issues found.
> Next steps:
> 1. `/script --document-mode` - Generate document-structured script
> 2. `/prep --split-screen` - Create split-screen edit guide
>
> Ready to write script? Run `/script --document-mode`"

**When verification returns YELLOW:**
> "Translation verification found minor issues (see TRANSLATION-VERIFICATION.md).
> Review flagged sections and decide if acceptable for filming.
> To proceed: `/script --document-mode`"

**When verification returns RED:**
> "Translation verification found significant problems.
> See TRANSLATION-VERIFICATION.md for details.
> Revise translation before proceeding to script generation."

---

## SIMPLIFICATION DETECTION ONLY (`--simplify`)

Run simplification detection without full fact-check.

**Use when:** Quick scan before filming, or after revisions.

### Process

1. Read SCRIPT.md
2. Apply all 8 simplification rules
3. Generate severity report only

### Output

Quick report with only simplification flags (no verification status).

---

## NotebookLM Integration

**MCP-native (primary path):** Claim verification runs inline via `mcp__notebooklm__notebook_list` + `mcp__notebooklm__notebook_query`. See Steps 3.5 and 4A above. No copy-paste required.

**Fallback (MCP unavailable or no project notebook):** Generate prompts for manual paste into the NotebookLM browser:

```
I need to fact-check these specific claims from my script:

1. CLAIM: "[Claim from script]"
   Script says: "[Exact wording]"
   Verify: Is this accurate? Exact quote with page number if supported.

2. CLAIM: "[Next claim]"
   Script says: "[Exact wording]"
   Verify: [same]
```

After pasting, save the output to a `.txt` file and run `/verify --extract-nlm <file>` to extract structured citations.

---

## Key Principle

**If you can't verify it with 2+ credible sources, it doesn't go in the script.**

Historical integrity is the channel's core value. Better to cut a claim than to include something unverified.

---

## Reference Files

- **Simplification rules:** `.claude/REFERENCE/FACT-CHECK-SIMPLIFICATION-RULES.md`
- **Fact-check template:** `.claude/templates/03-FACT-CHECK-VERIFICATION-TEMPLATE.md`

---

## After Completion

**When verification completes with APPROVED verdict** (valid ONLY if the Step 0 coverage gate passed — no open `[COVERAGE-GAP]`; a cold-open-only check is NOT an APPROVED script):

> "Fact-check complete! Script approved for filming.
> Next steps before filming:
> 1. `/prep` - Generate edit guide and B-roll checklist
> 2. `/publish` - Create YouTube metadata
>
> Ready to prepare for filming? Run `/prep`"

**When verification completes with NEEDS REVISION:**

> "Fact-check found issues requiring revision.
> See 03-FACT-CHECK-VERIFICATION.md for specific corrections needed.
> After fixing, run `/verify` again."

**When claims extraction completes (`--extract`):**

> "Extracted [X] claims from transcript.
> - Priority 1 (critical): [X] claims
> - Priority 2 (supporting): [X] claims
> - Priority 3 (minor): [X] claims
>
> Claims saved to CLAIMS-TO-VERIFY.md. Ready to fact-check? Run `/verify --script`"

---

## Absorbed Commands

This command consolidates functionality from:
- `/fact-check` - Full fact-check verification
- `/extract-claims` - Claims extraction from transcripts

All original functionality preserved through flags.
