# Opener Playbook — First 30s (fresh prescriptive layer)

## Opener system map (canonical roles)

This is one doc in a set. To stop two-sources-of-truth drift, each file has a fixed role — reach for the right one:

| Doc | Role | Reach for it when |
|---|---|---|
| **OPENER-PLAYBOOK.md** (this) | **Operational quick-reference** — the 5 patterns, the 3 killers, the sentence-1 checklist, the primer rule, the hierarchy | You're writing/checking an opener and want the *what to do* fast |
| **OPENER-CRAFT-BRIEF.md** | "Why" knowledge base — **write** (rules + principles) | Writing a new opener from scratch |
| **OPENER-CRAFT-BRIEF-2.md** | "Why" knowledge base — **diagnose** (structural mechanics) | Diagnosing a specific structural problem (primer too long, gap not sustaining, sentence-1 issues) |
| **OPENER-MASTERY-BRIEF.md** | "Why" knowledge base — **mental models** | You don't know WHICH rule applies — the models tell you what to optimize first |
| **RETENTION-STRUCTURE-MAP.md** | Whole-video gap-sustain (beyond the opener) | Keeping the opener's gains from bleeding out across the 8–12 min body |
| **OPENING-HOOK-TEMPLATES.md** + **HOOK-PATTERN-LIBRARY.md** | Legacy / corpus — cross-referenced, NOT primary | Mining the older fill-in templates or the March 85-hook corpus (freshness-guarded) |

**Operational home:** the `/opener` skill (`.claude/commands/opener.md`) runs this playbook as gates. The primer split is executed in **/opener STEP 0**; the 3 killers in **/opener GATE C**. This doc carries the *rationale* copies of both (below); the skill carries the executable gate — keep them in sync.

---

**Provenance:** vidiq in-app chat synthesis (cites Reddit creators / PrePublish-2026 / Retention Rabbit-2025 — directional, second-hand) + Gemini-in-YouTube-Studio analysis of our own published first-30s retention (Gemini-estimated %). Captured **2026-06-25**.

**Role:** This is the **prescriptive** layer for `/opener` — *what to write* — fresher and more voice-fitted than the stale `HOOK-PATTERN-LIBRARY.md` (March, 85 hooks). It will be deepened by the NotebookLM Opener-Craft brief (`cd9d6d5a-4377-4315-afa3-1c7497ccfc14`). Own-channel numbers below are DIAGNOSTIC (where we bled), not for ranking archetypes.

**Throughline:** *evidence before ego · contradiction before context · artifact before argument.* Fire it in the first **8 seconds**, not the first 90. Every video sits below the generic 70%-at-0:30 "solid" bar (our best opener ≈61%) — clearing that bar is the target.

---

## The 5 cold-open patterns (voice-fitted)

Each maps to our archetype taxonomy + famous-gate method (`[holds]` = audience holds the belief → myth-contradiction; `[cold]` = assumption-first).

### 1. Document Ambush  · maps to `specificity_bomb` `[cold]`
Open ON a primary source. **No narration 3–5s.** Zoom to one sentence, read it aloud, then: "That's X — here's why it contradicts what you've been told."
> "This is Article 11 of the Treaty of Tripoli — signed 1796, ratified unanimously. It reads: 'The Government of the United States is not, in any sense, founded on the Christian religion.' Read aloud on the Senate floor. No one objected. Here's what happened next."

**Why:** the document sells itself before the viewer forms a "do I trust this channel?" judgment. Visual+textual open loop — you can't half-listen. This is the "Exhibit A" rule, moved to the first 8 seconds.

### 2. Inverted Verdict  · maps to `cold_fact` / claim-first `[cold]`
State the **conclusion as sentence one**, then spend the video proving it.
> "In 1526, a Central African king wrote a letter that should have ended the Portuguese slave trade. It didn't. Here's the sentence Portugal ignored for 300 years."

**Why:** payoff up front → viewer watches to understand *why*, not *what*. Unifies thumbnail → title → first 10s (matches the two-sentence declarative-paradox title structure).

### 3. Map Contradiction  · maps to `cold_fact` / territorial `[cold]`
Open on a map; reveal a second map that contradicts it; let the mismatch **sit visually for a beat** before speaking.
> [Map A: "Spanish Sahara" 1975] — 3s pause — [Map B: "Morocco" 1976] — "Both are official UN maps, one year apart. Here's what happened in between."

**Why:** visual contradictions register faster than verbal; the viewer feels they *discovered* the problem → far stickier than being told.

### 4. Audio Artifact  · maps to `specificity_bomb` / Untranslated Evidence `[cold]`
Open with **5–8s of a recording / primary text read aloud**, zero narration, then: "That was X — here's what it actually meant."
> [crackling 1940s radio reading a treaty clause in French] — "That was Article 8 of the 1940 Armistice. The English translation published next day omitted that clause. Here's why."

**Why:** purest "evidence referee" — artifact speaks first. Active listening kills the passive-scroll state.

### 5. Single-Sentence Contradiction  · maps to `myth_contradiction` `[holds]`
One flat sentence — the "calm bomb" — between what everyone knows and what the record says. No fireworks.
> "Everyone knows the Berlin Conference of 1884 divided Africa. What no one mentions is that the conference's own Final Act explicitly banned the slave trade — and every signatory kept trading slaves for another 30 years."

**Why:** calm delivery + destabilising content signals authority ("they have the receipts"). Fits skeptical 25–44 men who distrust hype merchants.

---

## Per-pattern execution (dos & don'ts)

Source-grounded micro-mechanics from `OPENER-CRAFT-BRIEF-2.md` §3.

- **Document Ambush** — the document must *act* in the sentence it appears in (McKee: "convert exposition to ammunition"), never be introduced ("X is a document that states…" = McKee's "table-dusting" failure). Open with the document's most surprising *content*, not its title. The hook is the gap the document opens, not the document itself.
- **Inverted Verdict** — give the contradiction/"gag" within ~10s (Kane/Shareability), but reveal only the **verdict** ("we have the historical record"), NOT the evidence — the evidence is the *sustain* mechanism for the body. Failure mode = "hiding the ball": if the viewer can't tell within 10s what you'll disprove, there's no gap, just confusion.
- **Single-Sentence Contradiction** — aim for proverb density (Made to Stick): one ≤10-word sentence, maximally simple + maximally surprising, that implies a mechanism ("X is wrong because of Y you've never heard"). Failure mode = the "wolves" problem: a surprise unrelated to the thesis is worthless; the schema you break must be the one the video debunks.
- **Map Contradiction** — geographic specificity is a concreteness anchor (a "big red X" — Made to Stick). One named place + one contradicted assumption. Don't pre-load full geography (cartographic table-dusting). *(Visual timing — map on screen at word 1 vs word 10 — not addressed in sources.)*
- **Mystery Figure / Audio Artifact** — the named actor must *act* in sentence 1 ("Snouck Hurgronje examined the Arabic original", not "was a scholar who studied…"); behavior reveals character (Yorke), and one named person beats a category (Made to Stick "Mother Teresa principle"). Best when the action *contradicts* the figure's apparent role (a king who *hires* rather than sells).

## Primer calibration (how long before you open the gap)

> **Operational gate:** `/opener` STEP 0 (famous-gate method switch) executes this split. The text below is the **rationale/diagnostic** copy — edit the skill, not just this, when the rule changes.

The gap should be named by **sentence 3**; if sentence 3 has no gap, the primer has become exposition.
- **Known topic** (audience holds a belief to contradict): 1–2 sentence belief-primer → gap by ~0:08. (The primer IS the schema activation Loewenstein requires.)
- **Unknown topic** (no existing frame): 3–4 sentences of grounding, but each must be a **named concrete landmark** (person/place/date/document), never abstract context → gap by ~0:12.
- Bakassi (31%) failed not because its primer was long but because it contained **no schema the viewer holds** ("Most border disputes are about…") — no reference point, so no gap can fire.

## Sentence-1 checklist (run before filming any opener)

From `OPENER-CRAFT-BRIEF-2.md` §4 (McKee / Kane / Made to Stick / Kahneman). Several items are **borrowed from canonical homes** (annotated so they can't drift — fix the canonical source, not just this copy):
```
[ ] ≤13 words (≈5s spoken)        [ ] active voice, no "is/are/there is"  → WRITING-VOICE-AND-STYLE-P1-CORE-VOICE.md §1.7
[ ] every noun photographable      [ ] no subordinate clauses (1 subject/verb/object)
[ ] no hedging ("some argue…")  → §1.6      [ ] no creator framing ("today we're looking at")
[ ] ≥1 of: named person / date / place / violated claim  → hook_scorer anomaly (year/number/named-document in first 30 words)
[ ] reads aloud without stumbling (rhythm = cognitive ease)  → WRITING-VOICE-AND-STYLE-P1-CORE-VOICE.md §1.4 Stumble Test
```

**Word-limit scope (disambiguated — three different limits, don't conflate):**
- **≤13 words** applies to **sentence 1 only**.
- It is NOT `voice_lint.py`'s **10-22-word median** (`scan_sentence_band`), which is a *whole-script* band.
- The **Single-Sentence Contradiction** pattern's **≤10 words** *overrides* ≤13 for that archetype only.

First paragraph: gap by sentence 3 · clues not MapQuest · stikomythia variety (short/medium/short, never 3 longs or 3 shorts) · no floating tail-words.

## The 3 killers (auto-flag in /opener lint)

> **Operational gate:** `/opener` GATE C (Killer scan) auto-rejects on these. The entries below are the **rationale/diagnostic** copy — the executable gate lives in the skill.

1. **Context Dump** — "To understand X, we first need to go back to…" Front-loads a prologue nobody asked for. This is the #1 history-explainer killer and the documented Tordesillas failure (37% drop at 0:18). **Fix:** verdict first, context second. If they need 1492 to grok 1494, give 1494 first.
2. **Logo / Greeting / Channel Intro** — "[logo] Hey everyone, welcome back to…" Burns 8–10s before any value. At ~559 subs nobody tunes in for *you*. **Validated by our own data:** our worst-retaining opener literally opens "Hi, my name is Benoît" (Ukraine, 46% first-30s drop). **Fix:** cut entirely. Cold open → evidence → then contextualize.
3. **Stakeless Question** — "Have you ever wondered what happened at the Congress of Vienna?" A question the viewer hasn't asked → easy "no" → they leave. **Fix:** don't ask, state the contradiction.

---

## Own-data diagnostic (Gemini / YT Studio, first-30s, estimated)

**Leaderboard (retain@0:30 · opening type):**
- America's Founding Secular Quote ≈ **61%** · Mystery/unexplained evidence
- They Didn't Just Buy Slaves ≈ **58%** · Direct confrontation of online claims
- Myths of Thermopylae ≈ **52%** · Direct myth-busting
- $24 Manhattan Myth ≈ **50%** · Setting the scene (location)
- Spanish Inquisition ≈ **45%** · Common misconception
- **Worst:** Nigeria vs Cameroon → ~31% by 1:00 · academic/theory-heavy, payoff too slow

**What our best openers share:**
1. **Immediate conflict** — name the "common knowledge" within 10s and label it the myth/problem.
2. **Fast pacing (3-second rule)** — change visual context every 3–4s; lingering >7s on one static idea = sharper drop.
3. **"Discovery" first sentence — declarative mystery, NOT a question.** Best: *"In 1930, a Dutch scholar found something the US government still can't explain."* (61%) beats *"Everyone thinks they know what the Spanish Inquisition was."* (45%).

**3 changes to bake into every opener:**
1. **Front-load the counter-intuitive claim** — Claim → Correction in the first 5s ("the records show the opposite").
2. **Tighten the explanation gap** — name the specific document/person by 0:15 (e.g., "Middle Assyrian Law 40").
3. **Show visual proof earlier** — primary source on screen within the first 5s.

---

*Convergence: this triangulates with `channel-data/patterns/HOOK-RETENTION-CORRELATION.md` (document/myth-first beats context dump), the `opener_retention` table (abstract/intro-cold openers bleed worst), and the generic 70/80 benchmark (we're under the solid bar everywhere). Three independent sources agree → high confidence.*
