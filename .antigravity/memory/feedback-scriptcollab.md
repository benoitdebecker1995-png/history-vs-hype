---
name: Script Collaboration Workflow
description: User prefers collaborative script editing over generated scripts — draft first, refine together, verify changes
type: feedback
originSessionId: 8f9dbbcd-4784-479f-b2ca-3a31f442573e
---
## Collaborative Scripting > Generated Scripts

The user writes better scripts when they draft first and Claude refines, versus Claude generating from scratch. The Thermopylae session (2026-03-31) proved this — the result felt more personalized and authentic.

**Why:** The user's voice, instincts, and personal takes ARE the product. Generated scripts sound like summaries; collaborative edits sound like a person who read the books.

**How to apply:**
- When user pastes a draft or says "read my changes," enter collaborative mode (not revision mode)
- Parse inline comments: anything in parentheses, "??", incomplete sentences, "why", "how"
- Answer factual questions from 01-VERIFIED-RESEARCH.md
- Identify 5-6 patterns in their rewrites (voice, cadence, precision, structure) — tell them what they're doing well so they can do more of it
- Ask 3-5 personal take questions focused on their REACTION to the material (not logistics/filming/on-screen stuff)
- Integrate answers but AUDIT every addition against verified research
- Flag claims not in verified research → targeted NotebookLM verification (not blanket)
- When secondary source makes a claim, check if primary source says it more powerfully
- Small iterative edits, one round at a time
- **Voice-pass sections: pause after EACH section for user review.** Never batch multiple sections. After rewriting one section, stop and show the user. They read it, give directional phrasing notes ("I'd say X here"), then I integrate their shorthand as publishable prose (per VOICE-PROFILE §8). **Why:** The user's voice is the product; my rewrite is a draft for them to correct, not a final. Streamrolling forward wastes both our time if section 1's voice was wrong.

## User Draft Patterns

From Thermopylae session, the user's natural editing reveals:
- **First person over "we"** — "I haven't mentioned" not "we haven't mentioned"
- **Precision over cleverness** — "randomly inventing a large number" not "making up a round number" (1.7M isn't round)
- **Spoken cadence** — adds small words for flow: "A Greek physician working at" not "Greek physician at"
- **Cutting dead weight** — drops redundant phrases, unnecessary "But" pivots, adds "only" for emphasis
- **Declarative structure** — full subject-verb-object sentences, not fragments for information
- **Earning claims** — every assertion needs its evidence shown, not just stated

## Accuracy Audit Rule

User said: "sometimes I write based on feeling but I still want to make sure what ends up in the script is accurate — sometimes I remember wrong, sometimes I am biased."

**How to apply:** When integrating user's rough notes into a script:
1. Cross-check every claim against 01-VERIFIED-RESEARCH.md
2. If claim is NOT in verified research, flag it — don't silently include it
3. Run targeted NotebookLM queries for flagged claims only
4. If a claim can't be verified, say so and suggest cutting it or verifying it
5. Never assume user's rough notes are accurate — they're ideas to be checked

## Primary Source Preference

The channel aims to show people how historians work. If a primary source is available, prefer showing it with historian interpretations alongside — not just the historian's summary.

**Example:** Instead of quoting Cartledge saying "100% of their hoplite body," use Herodotus 9.30 (1,800 Thespians at Plataea "not wearing armor") and let the audience do the math. Primary source + interpretation > interpretation alone.

## Bakassi Session Lessons (2026-04-12)

**Structural contradiction detection:** When script sections cover the same time period from different angles, they can read as contradictions. Bakassi Act 3 said "Nigeria gave it away" while Act 4 said "Nigeria ran it" — user caught this as structurally broken. Fix: explicit "two realities existed at the same time" bridging. Now codified as Rule 27E in script-writer-v2.

**Attribution chains:** "According to Ezeilo, 73%..." was wrong — the figure came from Omoigui (2006) via Baye (2010). Ezeilo cited it secondarily. Always verify who originated a statistic before attributing. Now in Rule 8.

**Latin/technical terms are stumble risks:** User recorded "intertemporal" 8+ times and couldn't land it. Plain language always wins for spoken delivery. Now in Rule 7.

**Pronunciation guide saves filming time:** Foreign names (Ahmadou Ahidjo, Akwayafe, pacta sunt servanda) cause re-takes. Script-writer now generates a pronunciation table with every script. Now in Rule 7 + output template.

---

## Script-pass methods (added 2026-05-08, Video #54)

These are TECHNIQUES, not mandates. Apply when the situation fits.

### Pre-frame audit (before quoted sources)
When a quote has BOTH a pre-frame setup AND a post-quote decoder, audit whether the pre-frame is doing redundant work. Cut to question + quote + decoder if pre-frame is restating what decoder will say. Keep pre-frame if it's priming for legalese, introducing source, or doing emotional setup the decoder doesn't cover.
**Don't reflex-cut.** Audit each case. Source: Video #54 §3 ratification rule — original had pre-frame + quote + decoder all saying the same thing; cutting the pre-frame tightened the section without losing meaning.

### Category-match in scale transitions
When bridging from individual case to aggregate scope, the categories must match. Don't transition "torture case" → "executions count" without naming the shift. The listener's brain tries to map and slips.
**How to apply:** When writing a scale transition, name the bridging category explicitly. Source: Video #54 §6 fix — "His friends and family weren't the only ones" replaced "His case was one of many" because Díaz wasn't executed (he was tortured and cleared), so the original line slipped from torture-category to executions-category.

### Cut > adjust default
When a line is doing weak or ambiguous work, default to cutting rather than rewording. Multiple lines cut from #54 (§5 "the inquisitors proceed — the rules, and the loophole" + others) all improved the section.
**Why:** If a line needs three rewrites to land, it's probably doing redundant work or promising something the section doesn't deliver.

### CTA guardrail (no template)
CTAs are vibe — what value did THIS video deliver that viewers might want more of. Don't generate generic templates ("subscribe and hit the bell") or boilerplate channel taglines. Ground in the specific video's value. Ask user if unsure what the video's distinct value was. Source: Video #54 §7 close — the working CTA "Subscribe — I don't just tell the story, I show you the sources" was reached after the user explicitly named the channel value prop ("I don't only talk about history but show you how it is done"). Don't generate the formula; ask for the value first.

### "In other words" softened
Allowed when a quote needs unpacking — either translation (inaccessible language: legalese, archaic, foreign) OR explication (significance isn't obvious from the quote alone). NOT allowed as filler before a paraphrase that's already accessible. Source: Video #54 §3 ratification decoder — "In other words, a confession under torture couldn't convict you on its own..." legitimately translated dense legal text.

---

## Script-pass methods (added 2026-05-08b, Video #54 user read-through)

These surfaced from the user's read-through after the Sonnet+Opus polish pass. The user's question-pattern ("on what?", "why does this matter?", "what was his crime?", "where's this from?") revealed a small set of recurring archetypes that the AI had been missing.

### User-question audit (final pass before lock)
For each section, run four checks:
1. **Specificity** — Any term/person/document introduced? Is its definition or charge in the same paragraph?
2. **Significance** — Any claim of "X is true / X happened"? Does the next sentence land WHY this matters?
3. **Sourcing** — Any quote, statistic, dramatic claim? Is the source visible (in prose or citation)?
4. **Decoding** — Any primary-source quote? Is its significance immediately clear, or does it need a decoder?

These four checks encode the user's actual question-archetypes. Mechanical, fast, runnable in one final pass. Don't expand into "anticipate every possible question" — that's an infinite checklist.

### Charge specification for case studies
When a person gets a multi-paragraph block or >30 seconds of listener investment, name the charge/accusation in the same paragraph. Procedural placeholders (one-line illustrations of a rule) don't need it. Scope by depth of treatment.
**Source:** Video #54 §5 — Díaz de Cáceres needed "Judaizing" charge spelled out (case study, 45+ seconds). Marina González in §3 didn't (procedural example illustrating §XV personnel rule).

### Notebook verification for emotional beats
Verify timeline / isolation / dramatic claims via notebook before locking. Don't let dramatic narrative outpace verification.
**Source:** Video #54 §5 — the December 1596 collision (arrested same month family was killed) came from a notebook query during the user read-through. The notebook produced BETTER material than what we would have invented; the original gut-punch line was weak by comparison. Lesson: emotional beats also benefit from source verification, not just factual claims.

---

## Voice-Pass Patterns (added 2026-05-14, Video #52 Hijab)

A codified voice pass was run before filming on #52. One candidate at a time, user confirmed/cut/adjusted. Patterns identified:

### What the user flags as "cringy" / "typical AI writing"
- **Decorative metaphors with no informational content.** "Walking into a building that's already been standing for two thousand years" → cut, replaced with plain statement. Rule: if the metaphor can be removed and nothing is lost except the image, it's decorative and should go.
- **Internet-era phrases.** "History has receipts" → cut. Applies to anything that sounds like a Twitter/blog voice rather than a documentary voice.
- **Staccato fragments as rhetorical flourish — AI fingerprint.** User: "AI really likes these staccato bullshit things." Applies to: couplets ("Same instrument. Different uniforms."), triplets ("Three states. Three opposite rules. The same move."), and standalone sentence fragments ("Not permanent obligations.") used as closing punches. These get cut or folded into the preceding sentence every time. The rule is absolute — do not generate staccato fragment sequences as rhetorical beats. If the content needs emphasis, use a single complete sentence or a dash clause, not a run of fragments.
- **"Almost in passing"** — hedging adverbials that soften factual claims without adding nuance → cut.

### Redundancy detection
User flags lines that restate the previous line in different words. Two patterns caught:
- "The class logic is the substrate. The religion is the surface." came right after a sentence that said the same thing. Cut.
- "Same instrument. Different uniforms." came right after "The garment doesn't change. The states using it do." — same redundancy risk.
**Rule:** If you can cut the line and the paragraph still lands, cut it.

### Attribution framing (scholar vs. presenter)
User distinguishes sharply between what the presenter concludes and what scholars conclude. "Not our conclusion, it's the scholars'" was explicitly stated. When a function-analysis conclusion (what a ruling *actually does* vs what it *says*) comes from a scholar's reconstruction, frame it explicitly: "as X shows" or "X's analysis reveals." Never let a scholarly reconstruction sound like presenter's own reading.

### Theological scope
When a topic touches theology directly (e.g., whether veiling is religiously correct), user prefers a scope statement over naming a theological opponent. Pattern: "The question of whether women should cover — I'll leave that to the theologians. This is the question of where the mandatory rule came from." — draws the line clearly without engaging the theological argument.

### Contractions throughout
User expects a contractions pass as part of the voice check. "it is" → "it's", "the argument is not" → "the argument isn't", "her wearing of it" → "her choice to wear it" (also: more active/intentional). Run this check on every static block of VO.

### Voice-pass workflow
Run AFTER all factual grills (not before). One candidate at a time — never batch. User reads, gives directional note, Claude integrates. The pass has four priority checks:
1. **Contractions** — any formal "it is / does not / are not" constructions
2. **Decorative metaphors** — flag any spatial/architectural/biological metaphor; ask if it's earning its place
3. **Redundancy** — any line that says what the previous line already said
4. **Attribution framing** — any "he/she argues" or scholar-conclusion presented as presenter-conclusion

---

## Voice-Pass Patterns (added 2026-05-15, Video #52 Hijab — /polish second pass)

A second `/polish` pass on #52 surfaced three patterns not in the 2026-05-14 set. All three relate to *how rewrites get proposed and evidenced* during polish, not what gets cut.

### Verb-noun affordance check (when proposing rewrites)
**User reaction:** *"the sentence is awkward. a system can not start."*
**Example:** "And Islam isn't where it started" — a *system* doesn't *start*; it gets built, inherited, or set up.
**Rule:** When proposing a rewrite, audit verb-noun coherence. The verb must match what the noun can actually do. Abstract nouns ("system," "architecture," "logic") need verbs of construction/inheritance/operation, not action verbs that apply to events or rules. Most common slip: action verbs applied to abstract system-nouns.

### Freestanding historical-scope claims need inline evidence
**User reaction:** *"c but i hope we are providing some proof/evidence for this claim."*
**Example:** "The rule, as the early community understood it, applied to *free women* in Medina." — assertion about how a historical community interpreted a text, made without inline citation. The surrounding section's citations don't auto-cover this claim.
**Rule:** When a script makes a claim about *how a historical community understood* a tradition's text or rule (community-interpretation claims, not just primary facts), it needs either (a) an inline citation tag OR (b) a primary-evidence anchor in the same beat. Ambient citations of the surrounding section don't carry community-understanding claims by default. This sits adjacent to [[feedback-research-audit]] (which covers research-stage gap detection) but fires during polish, not research.

### Primary-evidence anchor > scholar name-drop, even in polish
**User reaction:** *"i would like to cite the arguments or sources and only if it's not clear or hard to put on screen rely on name dropping."*
**Example:** Offered choice between (a) bare "[SOURCE: Ahmed p. 55]" tag and (b) primary-document on-screen anchor (*darabat al-hijab* idiom). User wanted (b) and asked for the underlying scholarly arguments to surface a primary anchor.
**Rule:** When citation is needed during polish, the default move is to *find and surface the primary evidence the scholar is reasoning from* — not to add a bare name-drop tag. Bare citation tags are the fallback only when primary evidence is unavailable or unviewable on screen. This is [[feedback-auditors-edge]] applied specifically to polish-pass citation decisions. **Workflow implication:** when adding inline evidence during polish, query the notebook first for the primary anchors the scholar uses, then choose between primary-on-screen vs. bare-tag based on what survives "viewable on screen" test.
