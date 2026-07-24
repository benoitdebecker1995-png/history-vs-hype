# Stop-Flag Specifications

Flags that halt active research. Each fires during live work, not in cleanup. (Five: NEED SOURCES, LIBRARY ACQUISITION, DIRECTION NEEDED, ATTRIBUTION UNVERIFIED, ATTRIBUTION DRIFT.)

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

---

## `[FLAG: ATTRIBUTION UNVERIFIED]` — argument attribution (Rule 4 mode A)

### Trigger conditions

- A claim of the form "PERSON read / argued / claimed / treats X as Y" is being filed and the only backing is a source confirming **X is independently true**, not a source showing **that person making that move**.
- Highest risk: the claim characterizes a **debunk TARGET** (Hancock, Hapgood, von Däniken…). A real verbatim quote attached to the sentence does NOT validate the attribution wrapped around it.

### Flag text to output

```
[FLAG: ATTRIBUTION UNVERIFIED]
Claim: "[PERSON] [read/argued/treats] [X]"
Problem: Backing source confirms X is true, but no source shows [PERSON] making this move.
Options:
  (a) Re-source to a work where [PERSON] actually makes the move (verbatim) → flag clears
  (b) Reframe as an appearance the text debunks, attributed to no named proponent
  (c) Cut
Halting until resolved.
```

### Piri Reis #57 example

**cağferiye double-misattribution** — "Hapgood read that word [cağferiye]… and Hancock after him… as the fingerprint of the lost civilization." Every component was verbatim-true (Kahle's quote, Hancock's "4th century BC," Hapgood-as-Alexandria-originator) — but Hapgood never names the word and Hancock never engages it. A strawman welded from two true facts. Caught only when the user opened Hapgood's physical book. → `[FLAG: ATTRIBUTION UNVERIFIED]`; resolution = VO pickup (filmed). See `VO-PICKUP-cagferiye.md`.

---

## `[FLAG: ATTRIBUTION DRIFT]` — expository attribution / predicate drift (Rule 4 mode B)

### Trigger conditions

- A named **non-target** authority or document is said to assert proposition **P2** ("Ptolemy's geography said one had to exist to balance the globe"; "the treaty established Y"; "Roman law held Z"), but the source supports only an **adjacent** proposition **P1** — even when both P1 and P2 are independently true.
- The same fact appears in research once with **loose unnamed phrasing** ("ancient geographic theory required…") and once **pinned to an authority** ("Ptolemy's theory…") and the two were never reconciled. (This double-entry is the welding seed.)
- A "[Authority] said/required/established X" sentence with X paraphrased (quote cards go to `/verify` Step 7.8 provenance instead).

### Flag text to output

```
[FLAG: ATTRIBUTION DRIFT]
Claim: "[Authority] [said/required/established] [P2]"
Source supports: [P1, verbatim or paraphrase] — NOT P2
Problem: Predicate drift — the authority asserts P1; the script puts P2 in their mouth.
Options:
  (a) Re-attribute P2 to its real holder (who actually asserts it)
  (b) Rewrite the line to P1 (what the source supports)
  (c) Drop the named attribution; state the convention unattributed
Reconcile any loose-vs-named double-entry before script-ready: name only what the source names.
Halting until resolved.
```

### Piri Reis #57 example

**Ptolemy / Ortelius** — research carried the southern-continent fact two ways: "ancient geographic theory required a southern continent to **balance**" (unnamed, correct) AND "it's **Ptolemy's** 2nd-century theory that land must **encircle water**" (named, but the enclosed-Indian-Ocean predicate). The script welded them: "**Ptolemy's geography said one had to exist, to balance the globe**" — a proposition no source attributes to Ptolemy (it's the Aristotelian symmetry argument, popularized by **Ortelius**, 1570). Filmed, fact-check-passed; caught in editing and re-attributed on-screen to Ortelius. → `[FLAG: ATTRIBUTION DRIFT]`; post-film resolution = re-attribute the on-screen card (+ VO pickup if the drift is also spoken).
