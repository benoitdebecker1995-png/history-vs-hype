# Stop-Flag Specifications

Three flags that halt active research. Each fires during live work, not in cleanup.

---

## `[FLAG: NEED SOURCES]`

### Trigger conditions

- A verbatim quote is being filed in `01-VERIFIED-RESEARCH.md` with no NLM source ID AND no identifiable acquisition target (no specific named book/article that would close the gap).
- A claim is tagged [S] (secondary source only) AND it is marked or implied as on-screen evidence AND no corroborating second source is identifiable.
- A claim carries a single source and the tier-vibe is T3 (scholar interpretation only) with no path to a primary.

### Flag text to output

```
[FLAG: NEED SOURCES]
Quote/claim: "[text]"
Problem: Verbatim text has no NLM anchor and no known acquisition target.
Options:
  (a) Convert to paraphrase ("Historian X argues that...") — allowed without NLM anchor
  (b) Supply a source URL (freely-accessible web) — see WEB-POLICY.md
  (c) Identify a specific acquisition target → flag upgrades to [FLAG: LIBRARY ACQUISITION]
Halting until resolved.
```

### Piri Reis #57 example

**Mallery 1956 Georgetown radio broadcast dialogue** — Claim 15 included the verbatim exchange: *"Walters: 'These maps go back 5,000 years and even earlier.'"* This text appeared in the Gemini output as a direct quote from the August 26, 1956 Georgetown University forum. The Mallery broadcast is NOT in the NLM notebook. No specific book or journal that reproduces this transcript verbatim is identifiable from the current corpus. → `[FLAG: NEED SOURCES]` fires. Resolution: convert to paraphrase ("Mallery claimed in a 1956 Georgetown forum that...") OR locate an archived transcript with URL.

---

## `[FLAG: LIBRARY ACQUISITION]`

### Trigger conditions

- A verbatim quote is being filed with no NLM source ID AND a specific named book, article, or manuscript is identifiable that would close the gap.
- A claim is tagged [S→P] (secondary points to a primary) and the primary document is a known, acquirable source.
- Gemini/Grok/WebFetch produced text presented as verbatim from a book not in the NLM notebook — and the book title is known.

### Flag text to output

```
[FLAG: LIBRARY ACQUISITION]
Quote/claim: "[text]"
Missing source: [Book/Article title, Author, Year]
Problem: Verbatim text from a source not in the NLM notebook. Cannot file as verified quote.
Proposed action: Add "[source]" to SOURCE-ACQUISITION-QUEUE.md (Step 6.6 schema).
Confirm to append acquisition entry? (y/n)
Halting until resolved.
```

On user confirm (`y`): append to `SOURCE-ACQUISITION-QUEUE.md` using the existing Step 6.6 schema (TARGETED status, priority based on load-bearing-ness). Do NOT write the verbatim text to `## VERIFIED QUOTES`. Move it to `## Candidate Quotes (Not Yet NLM-Verified)` as a holding pen.

On user decline (`n`): convert to paraphrase or cut.

### Piri Reis #57 examples

**Hancock verbatim passages (6 quotes, Claim 15)** — Gemini output produced six verbatim passages from *Fingerprints of the Gods* (1995): "bombshell," "Galileo-type figure," "6,000 years ago," "true enigma," "fingerprints of a vanished civilization," "irrefutable evidence." These are from a published book. Hancock's books (Fingerprints, Magicians, Underworld, America Before) are NOT in the NLM notebook. Acquisition target is identifiable. → `[FLAG: LIBRARY ACQUISITION]` fires for each. Resolution: add Hancock 1995 to SOURCE-ACQUISITION-QUEUE.md; move six verbatim passages to `## Candidate Quotes`.

**Von Däniken *Chariots of the Gods* passages** — same pattern. Book not in NLM; specific title and year known; verbatim text produced by Gemini. → `[FLAG: LIBRARY ACQUISITION]`.

**Verbatim Hancock 2002 *Underworld* passage** engaging McIntosh + Soucek — NLM notebook does NOT contain Underworld; this passage was produced by Gemini. → `[FLAG: LIBRARY ACQUISITION]`.

---

## `[FLAG: DIRECTION NEEDED]`

### Trigger conditions

- Two NLM-grounded scholars interpret the SAME evidence in ways that lead to DIFFERENT script framings.
- The framing choice is load-bearing: it affects scene structure, script tone, or which mechanism the video advances.
- Both framings have comparable NLM-confidence — this is not a credibility judgment but a narrative-direction decision only the user can make.

### Flag text to output

```
[FLAG: DIRECTION NEEDED]
Evidence at stake: [description of shared evidence]
Framing A — [Scholar A, source]: [what framing A says + script implication]
Framing B — [Scholar B, source]: [what framing B says + script implication]
These are not mutually exclusive claims of fact, but they lead to different script architectures.
Which framing should this video advance?
Halting until user picks.
```

After user picks: record the chosen framing in PROJECT-STATUS.md under `## Historian Stage State` > `**Outstanding flags:**` as RESOLVED.

### Piri Reis #57 example

**Gaspar 2008 vs McIntosh + Soucek** — same Scene 4 evidence (the "impossible" longitudinal accuracy of the Piri Reis map):

- **Framing A — Gaspar 2008** (NLM-grounded): magnetic declination and a coordinate rotation matrix explain the apparent longitudinal accuracy; no lost civilization required. Script implication: Scene 4 is a mechanism-explanation beat — "here's the actual science that makes the map accurate."
- **Framing B — McIntosh + Soucek** (NLM-grounded): the cartometric identification via unique Columbus place-names (Porta ghande = Guantanamo, Kaw Punta Orofay = south Cuba) establishes the map is a copy of Columbus's 1495-96 charts, making "impossible accuracy" moot — the accuracy is just Columbus's. Script implication: Scene 4 is a source-identification beat — "the accuracy is explained by whose map it copies."

Both are NLM-grounded. They don't contradict each other but they compete for Scene 4's primary frame. → `[FLAG: DIRECTION NEEDED]`.

**Additional Piri Reis example — Claim 10 single-source** (borderline NEED SOURCES vs LIBRARY ACQUISITION):

The Spanish prisoner chain-of-custody for Columbus's charts rests on Porta ghande and Kaw Punta Orofay as unique place-names — cited by McIntosh alone in the current NLM corpus. This is a single-source [S] claim being used as load-bearing evidence. Soucek accepts the Columbus identification but does not independently document these specific place-names. → `[FLAG: NEED SOURCES]` (no second NLM-grounded source for the specific place-names) OR surface as `[FLAG: LIBRARY ACQUISITION]` if the user identifies another cartographic scholar who independently documented these. McIntosh's own caveat ("a certain amount of uncertainty and hesitancy must enter into the discussion") should be reflected in the script regardless of flag resolution.
