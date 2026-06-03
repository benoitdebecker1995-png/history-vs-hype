# Piri Reis #57 — Script Revision Brief (intent-first pass)

**Trigger:** open this file in a clean session and say *"run the Piri Reis revision brief."*
**Goal:** one disciplined pass over `SCRIPT-v4-teleprompter.txt`, paragraph by paragraph, using the intent-first method the creator validated. Upgrade / trim / restate where needed. Mirror every approved change to `SCRIPT-v4.md`.

---

## ⛔ OPERATING RULE — PROPOSE, DON'T ACT (read this first, obey it all the way through)

**Do not change anything by yourself. Propose every change and ask the creator before doing it. Wait for an explicit yes, then write.**

- Work **one paragraph / beat at a time.** Never batch. Present, get a decision, move on.
- For each change, **show what you'd change and why**, then ask. The creator decides.
- Present options **only when there's a genuine choice** (max 3, different angles not synonyms, mark a recommendation). Otherwise propose one line and ask to confirm. Don't hand back trivial decisions; don't act on non-trivial ones without a yes.
- **Never write a file unprompted, and never rewrite a whole file.** Only edit the specific approved beats. (Last session, unprompted full-file writes were rejected twice — this is the rule that came out of it.)
- "Drive, don't punt" applies to the *thinking* (do the analysis, query the notebook, form a recommendation). It does **not** authorise writing without approval.
- If the creator says keep/cut a specific thing, that's a decision, not a preference — honor it.

---

## Read first (in this order — a clean context has none of last session's calibration)
1. `WRITER-LESSONS.md` — voice, collaboration rules, cringe inventory, document-led-video architecture.
2. `VOICE-FINGERPRINT.md` — delivered-speech DO/DON'T mined from finished cuts.
3. `SCRIPT-v4-teleprompter.txt` — **the live read version (v5). This is what we're revising.**
4. `SCRIPT-v4.md` — master with [SOURCE]/[VISUAL] cues + a header documenting every reframe locked last pass. Mirror all approved edits here too.
5. `01-VERIFIED-RESEARCH.md` — factual ground truth + NLM source IDs.
6. Memory: `~/.claude/projects/D--History-vs-Hype/memory/feedback-scriptcollab.md` → the entries **"Edit-flow continuity check"** and **"Intent-first querying."** Also `MEMORY.md` Production State for #57.

---

## The loop — run on EACH paragraph, in order, one at a time
1. **State the intent plainly** to the creator — one or two sentences: what is this paragraph trying to convey? Do this *before* anything else.
2. **Query the notebook against that intent** — not the topic, the intent. Let the result *confirm or redirect*. This is the highest-yield move (examples below).
3. **Flow-check in + out** — does the opening pronoun/connector still have a clear antecedent from the previous paragraph? Does the ending still set up the next one? Catch cold pronouns and stranded transitions at the seam.
4. **Form a recommendation:** upgrade / trim / restate / leave as-is. State it plainly.
5. **ASK.** Present the proposed change (+ options if a real choice) and wait for the creator's decision. **Do not write yet.**
6. **On explicit approval, write to BOTH files** (teleprompter + master, mirrored). Then move to the next paragraph.

**Length:** currently **1,880 VO ≈ 11.5 min** (under the ~1,950 / 12-min cap, but near the ceiling). This pass should *net-trim*. Word-count after substantive changes: `(words)/163 = minutes`.

---

## How the creator works (collaboration patterns)
- He drives by **reaction**, not generation — give him something concrete to react to, plainly stated.
- **Digest his shorthand; never parrot it.** When he floats a term or rough sentence, extract the intent and write the publication line in his voice. Don't paste his words; don't hand the decision back as "your call."
- He'll revoke earlier-approved phrasings when context changes — flag overrides transparently ("you'd approved X; I'd cut it because Y").
- He reads **too much complexity** as a failure. When he says it "reads complicated" or "too much shit going on," **restate the bare intent in plain words**, then give one simple line.
- **Flag vocabulary:**
  - *"doesn't make sense" / "huh?"* → cold pronoun, buried logic, or vague antecedent. Find and fix it.
  - *"cringey"* → performative metadiscourse, slang, or sanctimony. **Cut it — don't soften.**
  - *"random"* → missing bridge or a beat that doesn't belong. Fix the connection or cut the beat.
  - *"what is the video we're making"* → scope drift. Restate the title; rebuild around it.
  - *"too much prose"* → strip explainer prose; trust the evidence + the turn.
- He dislikes **staccato fragment triplets** ("Hot. Serpents. Cold.") — reads as AI cringe. Full sentences or a dash clause. (One kept staccato in a prior cut is the exception, not the target.)

## Voice quick-reference (headlines — full lists in VOICE-FINGERPRINT.md)
**DO:** enumeration (name + date + what they did); concrete immediate openings; "There's just one problem."; plain-concrete verbs over jargon; present tense + contractions; "we" not "I" to guide; short person-subject verdicts; "it isn't X, it is Y"; direct-address imperatives ("Read that again."); plain first-person research authority ("So I read it."); credential + name + "put it"; dry irony aimed at the *opponent's own material*; counter the conspiracy *structure*, not just the fact; fan-directed concession (not character defense).
**DON'T:** performative metadiscourse ("here's what nobody will tell you"); slang/coinage ("the receipt," "mystery-sellers"); self-clever wordplay with no referent; sanctimonious takeaways; "let's" as an empty transition; overselling research; moralising about the person.

## Core principle that drove the whole last pass
**Report the claim — don't sell it.** State the opposing claim flat and let the document prosecute. Never inflate it to make a bigger target. And **don't strawman** — represent the claim as its strongest proponent actually makes it (the creator polices this hard, and turns it on *our own* claims too: "is this the logic historians actually use, or are we using a weaker one?").

---

## Notebook usage
- **Project notebook:** `ac914976-51bc-4723-b983-f7e283af0da4`. **Invoke the `historian` skill** first (project is Stage C). Every on-screen verbatim needs an NLM source ID (historian Rule 1) — no web verbatim, no half-remembered quotes.
- **Auth quirk:** if expired, run `nlm login` in terminal — the Windows ✓-crash is cosmetic (cookies extract before it), then `refresh_auth`.
- **Competitor notebook** (how-to-say-it / non-cringe phrasing models): `438186cd-045e-40b1-ae67-9ecf25fcb415`. Use when the question is "how do good channels say this," not "is this true."
- **Bermeja / phantom-maps notebook:** `540d20b0-17f5-48b6-96bb-af7cb8bc0ef3` (Mountains of Kong, Sandy Island, etc.).
- **Why intent-first querying wins (worked examples from last pass):** stating the intent turns "tell me about X" into a falsifiable question, and the notebook then *redirects* you when the real picture differs — "translation was wrong" → *it's fine, the error is Piri's own*; "inscription 10 proves Brazil" → *toponyms + cartometry do; inscription 10 only debunks ice*; "they chose this map" → *they use a stack and cherry-pick*; "Hapgood made it up" → *he read it off the map and misread it*; "nobody argues aliens" → *von Däniken did, but Hancock rejects aliens*.

---

## LOCKED — do NOT undo (all creator-approved + notebook-grounded last session)
- **Cold open** opens on the real escalating claims (accurate map → lost civ → aliens), not "star witness." Aliens = von Däniken / "people," **never Hancock** (he rejects aliens for a lost *human* civ). Map authenticity is undisputed — never imply hoax.
- **Alexandria beat:** state Hancock's *real* claim (map *descends from* Alexandria). Name **Hapgood (1966)** as originator. The claim is read into the source list's "time of Alexander" + Ptolemy — McIntosh's own account (p.18). NOT "Alexandria isn't on the list" (the strawman we killed).
- **Translation is not the error** — Piri's own two slips are: cağferiye = *jughrafiya* (geography) misspelled; the two-Ptolemys confusion (Claudius 150 AD vs Ptolemy I) → "time of Alexander." Authority = Kahle could read the Ottoman; Hapgood couldn't. Verdict scoped to "every scholar who can read the original" (philology, not general history).
- **Southern coast:** Brazil identified by **toponyms** (Cabo Frio / Rio de Janeiro / Cananéia) + cartometry — the scholars' real positive ID. Inscription 10 only debunks the ice reading. The "Antarctica" shape = real Brazil coast + speculative *terra australis* (the balancing continent every 1500s mapmaker drew). The names (Brazil, sailed) and inscription 10's "Portuguese didn't land" (the empty southern tail) sit on **different parts** — no contradiction.
- **Cherry-pick beat** (replaced California/Kong in VO): Hapgood used a *stack* of maps; among many differently-shaped imaginary southern continents they kept the few resembling Antarctica → "it's shopping for it." California/Kong/Sandy Island = B-roll captions only.
- **Beat 5** framed as a **paradox** (ignored = survived), NOT a "mystery." "Not hidden, not suppressed, just ignored" defuses the suppression-conspiracy framing.
- **Kahle discovery:** "the one man who could read it" was an overclaim and is cut — uniqueness = his prior Bahriye work, not literacy. Deissmann compressed out of VO.
- **Closer bridge:** "That's where the man's story ends. The map's was only beginning."
- **CTA** at ~70% (end of Beat 3), value-anchored + forward-tease ("there's still the bottom of the map").

## Open flags to resolve in the pass (propose + ask)
1. **Beat 2 "So where did Hancock get that?"** — "that" is a slightly cold pronoun across the rebuttal. Candidate: "So where did Hancock get the Library of Alexandria?"
2. **Kahle appears twice** (Beat 2 intro 1933 + Beat 5 discovery 1929) — mildly non-linear. Decide on read-aloud whether Beat 5 needs a one-word callback or reads fine.
3. **Length margin** — trim candidates if the read runs long: the two-Ptolemys explainer and the cherry-pick beat are the densest additions.

## Output protocol
- Mirror every approved change to **both** files; keep them line-for-line in sync.
- Tag any new on-screen quote with its NLM source ID in `SCRIPT-v4.md`.
- Word-count after substantive changes; report runtime.
- **Never** write without an explicit yes. **Never** rewrite a whole file.
