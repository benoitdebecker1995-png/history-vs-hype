# Writer Lessons — bundled from #57 (Piri Reis)

> Captured 2026-05-29 after the v1→v4 rewrite cycle. Everything the assistant got wrong, every pattern the creator surfaced, and every rule that should bind future scripts. Companion to `VOICE-FINGERPRINT.md` (voice layer); this doc adds structure, scope, collaboration, and process.
>
> **For future agents / Claude sessions:** read this before drafting any script. It encodes the corrections from a four-version rewrite — don't make those rewrites necessary again.

---

## 1. The capstone rules (in priority order)

### 1.1 Report the claim — don't sell it
The single biggest recurring error across v1→v4 was *narrating/inflating* the opposing claim instead of stating it flat.
- **Wrong:** *"the only way to draw a map this accurate was from above"* — building von Däniken's argument for him.
- **Right:** *"a spaceship hovering over Cairo helped draw the map."* State the claim plainly and let the document prosecute.
- Fix loose verbs to literal truth: *"the landmass WAS Antarctica"* → *"the bottom DEPICTS Antarctica."* A drawing claimed to show a continent is not the continent.

### 1.2 Digest creator shorthand — never parrot it
When the creator floats a term ("status quaestionis"), a phrase ("there's fingerprints on the map"), or a rough sentence ("like eh.. this version of the story doesn't explain everything…"), that's *thinking out loud*, not the line. Extract the idea and write the publication version in his voice. Two parroting failure modes to avoid:
- Pasting his term verbatim into the script.
- Handing the decision back as an A/B choice ("name it or keep it plain — your call").

Both are reflecting instead of applying. He wants the digested, committed deliverable.

### 1.3 What is the video about?
**Before drafting any beat, restate the title and ask: is this beat actually about what the title promises?** The #57 rewrite consumed hours because the script was a *Hancock debunk* when the title was *"What the Piri Reis Map Actually Says."* The video should be about the map; Hancock is the foil at each stop, not the spine.
- When the title is *"What X says / proves / is,"* the structure should be a guided tour of X, not a sequence of "Y is wrong about A; Y is wrong about B."
- The debunking IS in there — but framed as "what's actually on the document," not as "let me catalogue Y's errors."

### 1.4 Length discipline — pre-trim, don't bloat
Every clarity-fix added concrete detail. Across the read-through, the script grew from ~1,800 to ~3,100 words (over 19 min). Cutting it back required either:
- Killing whole sections (Beat 4 "real mystery" meta, the moving-claim enumeration, the Mallery/Hapgood/USAF origin), or
- Refocusing the structure entirely (what we ended up doing).
**Word-count at length-decision moments.** 12-min hard cap is real (channel data: r=−0.455 duration vs retention). At 163 WPM that's ~1,950 words. Don't pass that.

### 1.5 The read-through is the gate
Abstract line-by-line review catches surface tics. Reading aloud catches:
- Cold pronouns (*"That's slow"* — that's *what?*)
- Buried logic (1528 update never said *why* it mattered)
- Undefined antecedents (*"the answer"* — to *what?*)
- Recap-redundancy (*"For sixty years the claim kept moving — Antarctica, then the Caribbean, then Indonesia"* — already said this in Beat 2)
- Vestigial references (*"don't argue about Antarctica"* — only made sense in a prior structure)

**Don't ship a draft without a read-through.** And during the read-through, accept that earlier-approved phrasings may need to be cut once their context changes.

### 1.6 Don't moralise — credit the believer's enjoyment, not their character
The high-identity-stake move (voice-spec §4.4) is **fan-directed**, not character-defense:
> *"If you like Graham Hancock and the stories he tells, this isn't an attack on the stories. I'm just trying to explain why the scientific community doesn't agree with him."*

NOT *"this isn't about whether Hancock is a good guy. By all accounts, he is."* The fan-directed version separates the fan's enjoyment from the factual claim — and protects the channel's credibility (private take can be sharper than what airs).

### 1.7 Quotes are evidence, not decoration — and they need an NLM source
Every on-screen verbatim needs primary-source grounding (Rule 1). If the source isn't in the project's NLM notebook, **acquire it before placing the quote** — don't paste from web or memory. The Columbus 1494 oath case (acquired via cross-notebook query of the flat-earth notebook's Morison source) is the model:
1. Fact verified in research file (Claim 19) → use the dated fact in VO.
2. Verbatim text not in NLM → fire `[FLAG: LIBRARY ACQUISITION]`, name the candidate source (Morison, Las Casas), don't fabricate.
3. Acquire (cross-notebook is fine if another project has it).
4. Round-trip the quote with page numbers, then place on screen.

The Gemini-injection lesson sits behind this. Web verbatim or half-remembered quotes are forbidden on screen.

---

## 2. Voice fingerprint (validated by #57 picks)

See `VOICE-FINGERPRINT.md` for the full catalogue. Headline patterns:

**DO**
- **Enumeration** for lists of provisions / perpetrators / sources — name + date + what they did, in one tight clause.
- **Concrete, immediate openings** — document-first imperative or claim-first colloquial. No meta-framing.
- **"There's just one problem."** — his actual turn phrase.
- **Plain-concrete verbs over jargon** — *"put it together from other maps,"* not *"compiled."*
- **Present tense, contractions throughout.**
- **"We" not "I"** when guiding the viewer — *"we'll come back to it,"* not *"I'm going to."*
- **Person-subject parallel verdicts** — *"They built it."* / *"A free woman who doesn't veil isn't punished. A slave who does veil is mutilated."*
- **"It isn't X, it is Y"** — *"The map hasn't changed. The story keeps changing."*
- **Direct-address imperatives** — *"Look at the punishment."* / *"Read that again."*
- **Plain first-person research authority** — *"So I read it."* / *"I went through the medieval manuscripts."*
- **Quote intro = credential + name + "put it" / "wrote"** — *"As Cambridge historian Paul Cartledge put it, …"*
- **Dry irony when it points at the opponent's own material** — *"the tragically lost Library of Alexandria"*; *"fingerprint of the lost civilization"* (Hancock's book title); *"nobody, that I'm aware of, has argued aliens were involved."*
- **Counter the conspiracy STRUCTURE, not just the fact** — *"it wasn't an official military analysis that got buried"* defuses the framing, not only the claim.
- **Throw the opponent's own number back** — *"A 12,000-year-old relic doesn't do that."*
- **Steelman = "what they actually believe"** — *"I think what the people who believe in a lost civilization actually believe comes down to this one word."* First-person, attributes belief.
- **Understated honesty move** — *"this version of the story doesn't explain everything."* NOT *"the honest version has a weak spot."*
- **Causal "so busy…they…" for irony** — *"They were so busy looking for Atlantis they walked straight past it."*
- **Title-callback close + "didn't read it" bookend** with the cold open.

**DON'T**
- Performative metadiscourse — *"Here's what almost no video about it will tell you,"* *"Let's play their game,"* *"Let's do what nobody does,"* *"If there's anything you remember from this video, let it be this."*
- Slang/coinage — *"the receipt,"* *"hot take,"* *"mystery-sellers."*
- Self-clever wordplay with no referent — *"signed by the man they call the mystery."* (Callbacks to the *opponent's* material are fine; clever for its own sake is cut.)
- Cold pronouns — *"That's slow, and it's boring, and it works"* with no clear antecedent.
- Recap inside the close — restating the moving-claim enumeration when the body already covered it.
- Vague nouns at the end — *"He wrote the answer down"* with no referent for "answer."
- Vestigial references — *"don't argue about Antarctica"* from a prior structure.
- Knowing Better snark or Shaun irony — wrong register; we're the referee, not the dunker.

**Nuances that override the spec:**
- *"let's"* is natural for him in some constructions ("So let's check the part we can"). Don't eradicate — only kill empty "Now let's talk about…" transitions.
- *"basically"* is OK as a natural softener (he kept *"It's basically a bibliography"*).
- Declarative superlative openers are fine — don't force the imperative open every time.

---

## 3. Structural preferences

### 3.1 Scope-check at the start
**Before drafting:** state the video's promise (the title) in one sentence and write the beat structure around fulfilling that promise. Re-check during every read-through pass.

### 3.2 Beat structure for document-led videos
When the title is *"What X says / proves"* and the video is about a primary document:
- **Open on the document/inscription/artifact** (matches thumbnail).
- **Tour the document by section/region** — "the corner," "the western coast," "the southern coast" (#57's final structure).
- The opposing claim appears at each stop as a brief foil (*"Hancock points to this and says X"*), not as a separate debunk beat.
- The structural verdict comes from *what the document actually says*, not from cataloguing the opponent's errors.
- Close on title-callback + the bookend phrase from the cold open.

### 3.3 Beats that are usually filler
- **"Real research vs fake research" meta beats** (the cut Beat 4 in #57). They read as preaching, and the lesson is already delivered by the body of the video.
- **Moving-claim arcs** that enumerate the opponent's revisions across decades. Strong on paper, recap-feel in delivery. Use one-line framing instead.
- **Origin-of-the-claim history** (Mallery 1956 radio show / Hapgood book / USAF letters). The map's own labels do the debunking; the claim's family history is bonus.
- **Antarctica glaciology numbers / multi-pronged backup arguments.** When the primary-document evidence is overwhelming, multiple corroborating arguments dilute it. One nail per debunk is usually enough.

### 3.4 The Calm Prosecutor architecture
- **Anchor word** repeated identically across beats (Rule 37). #57 used *"the source list"* in Beat 1, 3, 5, 8. #52 used *"free woman."* One drumbeat anchor per script.
- **Single thesis, mechanism-over-narrative.** ≤12 words. (#57: *"the map is a source list. Read it, and the mystery dies."*)
- **Primary source on screen with verbatim quote + page number** — the channel's core differentiator. Every load-bearing claim has a sourced quote.

### 3.5 Identity-stake awareness
When the topic is tied to group identity (lost-civilization fans, nationalist myths, religious narratives):
- Self-affirmation first (fan-directed concession, see §1.6).
- Procedural fairness — show you read both sides' evidence.
- Source transparency — make methodology visible.
- Never mock the believer; critique the evidence.

### 3.6 Length budget by section type
For a 10-min map-led debunk targeting ~1,800 words:
- Cold open: 200-220
- Each "region of the document" section: 200-450 (the densest one carries the etymology/typo, others lighter)
- Survival/rediscovery context: 200-280
- Close: 150-200

---

## 4. Collaboration patterns (how the creator works)

### 4.1 He drives by reaction, not generation
He processes faster by reacting to options than by writing from a blank. For phrasing questions, present 2-3 candidates with a recommendation. But also:
- He'll write his own variant in chat when the options don't fit. *Digest his intent,* don't paste his words.
- He'll keep earlier picks if they hold up in context; revoke them if they don't.
- He doesn't want options/punts when a decision can be made on craft grounds — drive it and flag transparently.

### 4.2 What his flags mean
- **"doesn't make sense"** — usually a pronoun antecedent or buried logic issue. Find the cold pronoun or the missing inference and fix it.
- **"what answer??" / "huh?"** — abstract noun with no referent. Name the concrete referent.
- **"cringey"** — performative metadiscourse, slang, or sanctimony. Cut it. Don't try to soften it — kill it.
- **"random"** — beat doesn't connect to the surrounding flow. Either fix the bridge or cut the beat.
- **"awkward sentence — write what you actually mean"** — the prose is contorted around an idea that has a plain expression. State the idea plainly.
- **"more phrases"** — more 2-3 option checkpoints; he's using them to teach the voice profile.
- **"keep [X] in VO"** — when he tells you a detail should stay in the spoken VO rather than only on screen, that's a content decision, not preference. Honor it.

### 4.3 When he says "query the notebook"
He usually means:
- The competitor notebook (`438186cd`) for prose patterns and how-to-say-it models.
- Or the project's research notebook for factual grounding/quotes.
Disambiguate which by what he's asking about. If he says "non-cringey way to say this" → competitor notebook. If he says "verify this fact" → project notebook (or cross-notebook).

### 4.4 He'll often signal scope drift
Watch for phrases like *"what is the video that we're trying to make"* — that's a reset signal. Restate the title, rebuild the structure around it.

### 4.5 He values transparency about overrides
When you cut a phrasing he earlier approved (because the context changed), **flag it**. *"You'd approved X earlier; I cut it because Y."* He'll either accept or push back — both are fine. Silent overrides erode trust.

---

## 5. Phrasings library (validated)

### 5.1 Approved on-channel verdicts/lines (from #57 picks)
- *"It's a spelling mistake."* — blunt one-line verdict; preferred over *"It's a typo"* (which read as too modern/slangy).
- *"becomes proof of a lost civilization"* — preferred over *"Atlantis"* (more accurate to what Hancock actually claims).
- *"the tragically lost Library of Alexandria"* — dry irony, allowed because it points at the believers' own claim.
- *"the fingerprint of the lost civilization"* — kept as deliberate callback to Hancock's book *Fingerprints of the Gods.*
- *"Notice what's going on here."* — preferred attention cue over *"Look at what just happened."*
- *"Nobody hid the map. The people who owned it just didn't think it mattered."* — mechanism stated as mental state, not apathy.
- *"They were so busy looking for Atlantis they walked straight past it."* — causal "so busy…they…" for missed-treasure irony.
- *"a continent that was never there"* — preferred over *"isn't even there"* (drops the filler "even").
- *"this version of the story doesn't explain everything"* — understated honesty move.
- *"this isn't about whether Graham Hancock is a good guy"* → REPLACED with the fan-directed version (see §1.6). The character-defense version reads as sycophantic.
- *"If you like Graham Hancock and the stories he tells, this isn't an attack on the stories"* — locked. The fan-directed concession.
- *"We just didn't read it."* — closing-line bookend with cold open's *"almost nobody has read it."*
- *"That's what I'm trying to do with this channel. If you like this content, subscribe."* — CTA in plain personal-mission framing. No "quick thing," no clever sell, own paragraph.
- *"the Porte, the Sultan and his ruling circle"* — define-on-first-use for jargon.
- *"California, for example, was drawn as an island for two hundred years — and nobody, that I'm aware of, has argued aliens were involved."* — dry-humor analogy with the "that I'm aware of" hedge.
- *"That leaves Antarctica."* / *"Back to the Caribbean."* — section openers as direct reset.
- *"Soucek calls it — 'a strange map whose mutilated remains lay forgotten in the library of Topkapı Palace.'"* — clean quote intro.

### 5.2 The cringe inventory (assistant introduced; all stripped)
These were inserted across v1-v4 and all cut. Don't reintroduce them.
- *"Here's what almost no video about it will tell you."* — performative metadiscourse.
- *"signed by the man they call the mystery."* — clever-clever wordplay, no referent.
- *"let's play their game for a second."* — performative + "let's" overuse.
- *"he gave you the receipt."* / *"what's not on the receipt."* — off-register slang.
- *"none of this is some hot take of mine."* — online-cringe slang.
- *"keep that test in your pocket."* — cute filler.
- *"the mystery-sellers never do."* — coinage / sneer.
- *"the one that refuses to die… let's end it properly."* — drama + "let's."
- *"Let's do what nobody does — let's read…"* — performative self-congratulation.
- *"If there's anything you remember from this video, let it be this."* — sanctimonious takeaway framing.
- *"don't argue about Antarctica."* — vestigial reference from earlier structure (Antarctica was just one of several claims; singling it out made no sense).
- *"That's a Rorschach test. You see whatever you walked in with."* — label without substance; the pattern-description does the work the label doesn't.
- *"For sixty years the claim about this map kept moving — Antarctica, then the Caribbean, then Indonesia"* in the close — recap of Beat 2.

### 5.3 Edits the creator made that revealed structural rules
- *"hancocks claim is a bit vague. not really sure what we are debunking"* → ALWAYS make the debunk's logical chain explicit. State the test, name the evidence, draw the conclusion.
- *"What date? huh?"* → state the PURPOSE of each evidentiary detail. The 1528 map exists to DATE the 1513 map to Columbus's lifetime; say so.
- *"inscription 6 doesn't explain everything"* → don't over-narrow the answer to one source when the debunk relies on multiple.
- *"this is very cringey"* → check for sanctimonious framings ("if there's anything you remember…") and vestigial references.
- *"better, but still, i think we should either ask the question or mention it before the last sentence"* → emotional closing lines need a setup (a question or a brief mention) so they don't land cold.
- *"there's too much wrong, please see what you want to say and then query the notebook"* → when revising, first state what you're trying to convey in plain words, then find non-cringey models, then write.

---

## 6. Process disciplines

### 6.1 Packaging-first
Lock title + thumbnail before writing any beat (channel mandate). Beat 1 fulfills the thumbnail's promise in 5s.

### 6.2 Voice-fingerprint mining (one-time, durable)
For voice calibration, diff the creator's **delivered SRTs** (finished cuts) against **scripts** for format-matched videos. The ad-libs are the real voice. #57 used #52 hijab + #56 slavery + #19 flat earth + #50 Thermopylae. Save to `VOICE-FINGERPRINT.md`.

### 6.3 Two-stage gate
- Gut-pick first (creator's call).
- Tool/critic if unsure (`thumbnail-critic`, `title_scorer`, the notebook).
- Don't override gut with scorer points when the gut pick is clearly on-brand (creator rejected scorer-pushed titles that read as clickbait).

### 6.4 Quote acquisition
- Check the project notebook first.
- If not there, check sister-project notebooks (cross-notebook is fine for verification).
- If not in any NLM, fire `[FLAG: LIBRARY ACQUISITION]`, name a specific source candidate, acquire, round-trip.
- Never paste web verbatim or half-remembered quotes on screen.

### 6.5 Read-through cadence
- Present each beat for read aloud, one at a time.
- Fix flags inline (apply to both master `SCRIPT-vN.md` and the read-version `.txt` to keep in sync).
- Word-count at section breaks if length feels off.
- After all beats, regenerate the clean read version.

### 6.6 Length gates
- Hard cap: 12 min recorded ≈ 1,800–1,950 VO words at 163 WPM.
- Pre-trim aggressively before showing read version. Don't show bloat.
- If projected length exceeds cap before read-through, refocus the structure (don't just trim — check that the video is doing what the title promised).

### 6.7 Scope check
At any reset signal ("what is the video that we are trying to make"), STOP and restate the title's promise. Rebuild the structure around it. The #57 refocus cut ~870 words by reframing from "Hancock debunk" to "guided tour of the map."

---

## 7. The #57-specific architectural lesson (transferable)

When the title is *"What X says / proves / actually is"*:

- **Structure = guided tour of X**, in 3-5 regions/sections of the document/artifact.
- The opposing claim appears at each stop as a one-line foil (*"Hancock says this is the Bimini Road"*), and the document's own labels/text deliver the answer (*"It says: Porta ghande, Columbus's name for Guantánamo"*).
- The debunking is implicit in showing what's actually on the document. Don't structure as a debunk-list.
- Close with title-callback + the bookend phrase from the cold open.
- Cut: moving-claim arcs, opposing-claim history (Mallery / Hapgood / etc.), corroborating-science nails after the primary-source nail, "real vs fake mystery" meta beats.

Applies to: any video framed as "what X says," "what X proves," "what was actually in the document," "untranslated evidence," etc.

---

## 8. Phase 5 — enshrine after lock

After the creator's read-aloud locks v4 → SCRIPT.md, these get propagated:
1. **`VOICE-FINGERPRINT.md`** is already current; copy its **DO / DON'T / cringe inventory** sections into the `script-writer-v2` agent definition.
2. Add the **cringe-inventory phrasings (§5.2)** to `WRITING-VOICE-AND-STYLE.md` §1.3 forbidden list.
3. Update memory `feedback-script-voice-calibration.md` with the meta-rules from §1 of this doc.
4. Consider adding §7 (the document-led-video architecture) to `WRITING-VOICE-AND-STYLE.md` PART 3 as a new structural template.
5. Save §4 (collaboration patterns) as a behavioral memory file.

Until then, this doc is the single source of truth. Future script-writer-v2 invocations should read this before drafting.
