# History vs Hype — Skill Workflow (v2, built around your actual loop)

## What changed from v1

v1 was a generic pro-team blueprint. After your answers, here's what the plan actually needs to do — and what it must *not* do.

**Your real loop:**
```
Mixed topic intake (VidIQ + scholarship + backlog + opportunistic)
        ↓
Comment mining (competitors' channels + source-topic articles)
        ↓
NotebookLM: dump sources, query via Claude Code, extract notes  ← PAIN: sources not exhaustive enough
        ↓
You write full word-for-word teleprompter script in YOUR voice  ← PAIN: research → script is heavy lifting
        ↓
Thumbnail ideation  ← PAIN: concept/angle, not execution
        ↓
Film + DaVinci edit  ← OFF LIMITS
        ↓
Publish
```

**Hard rules from your answers:**
1. **No skill writes prose for the script.** Voice/tone is yours. Skills prepare material; you write.
2. **Filming and DaVinci stay untouched.** No EDL exports, no edit suggestions.
3. **NotebookLM is the research hub.** Skills feed it (upstream) and query it (downstream). They don't replace it.
4. **Thumbnail skills do ideation, not design.** You handle execution.

**What that kills from v1:**
- `script-drafter` — gone. You write.
- Most of the "script editor" role — reduced to a flagging-only pass.
- All thumbnail design/layout skills — only concept generation remains.

**What that adds:**
- `source-deepening` — fixes the upstream pain (NotebookLM under-fueled).
- `comment-miner` — formalizes what you already do manually.
- `research-to-brief` — the critical bridge from NotebookLM output to a script-ready brief you can write straight from.

---

## The Priority 3 (build these first, in this order)

These directly attack the three pains you named.

### 🥇 `source-deepening`
**Pain it fixes:** "I need more exhaustive sourcing in the notebook to write a better script."

**What it does:** given a topic + format, hunts primary and scholarly sources *before* you load NotebookLM. Output is a download/link bundle ready to drag into NotebookLM.

**Process:**
1. Reads `00_brief.md` (topic, format, claims to test).
2. Searches in priority order: original-language primary sources (FR/ES/EN — leveraging your trilingual advantage) → peer-reviewed scholarship (JSTOR/Google Scholar/archive.org) → reputable secondary → reference. Calls Firecrawl/web for archive sites; for known repositories (Gallica, BNE, Internet Archive, JSTOR open) hits them directly.
3. For each source, captures: full citation, what it proves, the relevant passage with page number, language, accessibility (open / paywalled / archive-only), credibility note.
4. Flags coverage gaps: "you have nothing on X — without it, the script will have to hedge."
5. Produces `sources-package/` with PDFs/links + a `manifest.md` summarizing what's in the package and what's still missing.

**Output:** a folder you drag into NotebookLM in one shot.

**Stop condition:** at least 3 primary sources per load-bearing claim, OR an explicit "couldn't find — here's why" note.

---

### 🥈 `research-to-brief`
**Pain it fixes:** "Turning research into a watchable script."

**What it does:** queries NotebookLM (via your existing Claude Code setup) and outputs a *script-ready brief* — not a script. The brief contains every fact, quote, translation, and source ordered the way the script will need them, so when you sit at the teleprompter you're translating structure into your voice, not still researching mid-sentence.

**The brief has six sections, fixed:**
1. **The Hook Material** — 3–5 candidate cold-open facts (a name, a number, a specific date) that pay off the title within 8 seconds. Sourced.
2. **The Stakes** — why this myth matters / who believes it / where it circulates. Pulled from comment mining + scholarship.
3. **The Evidence Beats** — 3–5 ordered beats. Each beat: one claim, one or two sources, the exact quote (in original language + translation if non-EN), the page reference. *No prose. Just the load-bearing material.*
4. **The Strongest Counter** — the steelman of the myth (from `counterframe-builder`) + the rebuttal material.
5. **The Synthesis** — the 2–3 facts you want viewers to remember 24h later.
6. **Citation Block** — full bibliography formatted for the description.

**Critical constraint:** the brief is *materials*, not prose. You write the words. Every claim has a citation; every quote is verbatim with provenance.

**Process:**
1. Queries NotebookLM with structured prompts ("give me the strongest 3 primary-source quotes proving X").
2. Validates each pull against `claim-auditor` rules before including.
3. Orders the evidence beats for narrative flow (chronological, escalating, or contrast — picks based on format).
4. Drops the brief in `02_script/brief.md`. You write `final.md` from it.

---

### 🥉 `thumb-concept-forge`
**Pain it fixes:** "Thumbnail ideation — figuring out the concept/angle."

**What it does:** generates thumbnail *concepts*, not designs. Output is enough for you to know what to make in your design tool.

**Process — for each chosen title, generates 5 concepts varying on:**
- **Subject:** historical face / object / document / map / contrast pair.
- **Emotional read:** intrigue / defiance / "wait, what" / authority / unease.
- **Anchor element:** the one thing the eye lands on first.
- **Headline word(s):** ≤3 words, what overlays.
- **Tension:** what visual *contradiction* makes the click — e.g. famous quote crossed out, two flags in a frame that "shouldn't" be together, a document next to its mistranslation.

For each concept, also notes:
- What it promises (must match script payoff)
- Mobile-legibility risk
- A reference image style (photo / painting / document scan / map)

**Output:** `04_packaging/thumb-concepts.md` — 5 concepts, you pick one, you design it.

**Stop condition:** rejects any concept whose promise the script doesn't deliver. That's the credibility moat.

---

## The Full Skill Set

Organized by your actual loop, not a generic team.

### Phase 0 — Always-loaded

`channel-memory` — voice, audience, benchmarks (CTR/AVD floors), banned phrases, "won't cover" list. Read by every skill.

`style-guide` — citation format, quote handling (original language first), hook conventions, CTA placement rules.

`project-init` — spins up the per-video folder:
```
videos/YYYY-MM-DD_slug/
  00_brief.md
  01_research/
    sources-package/          ← from source-deepening
    notebooklm-export.md      ← from research-to-brief
    claims.md
    counterframe.md
  02_script/
    brief.md                  ← what research-to-brief produces
    final.md                  ← what YOU write
  03_broll/
  04_packaging/
  05_qa/
  06_post/
  state.json
```

---

### Phase 1 — Topic & Demand

#### `topic-intake`
Handles your mixed funnel rather than pretending it's one channel.

**Process:** maintains three input streams — VidIQ pulls, your manual backlog, and an opportunistic "in the news this week" capture. Weekly, merges them and scores each candidate on: hype-gap, evidence-density, your language advantage, competition, and *demand signal from comment mining*. Ranks top 10. You pick.

**Output:** `topic-candidates.md`.

---

#### `comment-miner`
Formalizes what you do manually: pulls comment threads from competitors covering the topic *and* from the source-topic articles (news pieces, popular history posts) the myth circulates in.

**Process:**
1. Given a topic + a list of competitor video URLs and/or article URLs, scrapes top-engagement comments via YouTube MCP + Firecrawl.
2. Classifies each: demand signal ("I want to know X") / objection ("but actually Y") / received wisdom (the myth being repeated) / good question (script seed) / source request.
3. Surfaces: top 5 demand signals, top 5 objections you'll face, top 3 angles competitors missed.

**Output:** `01_research/comment-mining.md`. Feeds into both `topic-intake` (validates demand) and `counterframe-builder` (pre-builds rebuttals).

---

#### `format-router`
Decides which of your 3 formats fits.
- Single quote being debunked → **Quote Check**
- Core evidence is a non-EN document → **Untranslated Evidence**
- Structural myth needing multiple sources → **Long-form**

Writes `00_brief.md` (topic, format, working angle, the specific claim, target runtime).

---

### Phase 2 — Research (NotebookLM-centric)

#### `source-deepening` 🥇
*(spec above)*

#### `notebook-querier`
Wraps your existing Claude Code → NotebookLM workflow into a repeatable skill. Given a list of claims to test, runs structured queries ("strongest 3 primary quotes proving X", "any sources contradicting Y", "translation of [exact passage]"). Returns structured answers with source citations.

This is the input layer to `research-to-brief`.

#### `claim-auditor`
Tries to break the work. For each claim:
- Is the primary source in context? Date correct? Translation accurate?
- Is the scholar's interpretation contested? Active search for refuting sources on the weakest 2.
- Verdict: ✅ solid / ⚠️ defensible with caveat / ❌ pull or strengthen.

Loops back to `source-deepening` if anything is ❌.

#### `translation-checker`
Specific to Untranslated Evidence format. Given an original-language passage and a popular English rendering, flags translation choices that load the meaning (omitted clauses, false cognates, period-loaded vocabulary, deliberate softening/hardening).

#### `counterframe-builder`
Steelmans the myth. Lists the top 3 hostile-commenter objections. Drafts the source-backed response material (not prose). Feeds `research-to-brief` and `comment-triage`.

---

### Phase 3 — Script PREP (no prose written)

#### `narrative-architect`
Picks the skeleton, no words written. Format templates:

- **Long-form:** Hook (≤8s payoff) → Stakes → Evidence Beat 1 → Beat 2 → Strongest Counter + Rebuttal → Synthesis → CTA.
- **Quote Check:** The Quote → Where You've Seen It → Earliest Real Source → What They Actually Said → Why The Misquote Stuck.
- **Untranslated Evidence:** The Claim → The Document → Clause-by-Clause Translation → What Changes When You Read The Original.

Assigns retention beats (pattern interrupt every ~45–60s), word budgets per section, target total runtime.

**Output:** `02_script/outline.md` — structure only.

---

#### `research-to-brief` 🥈
*(spec above)*

---

#### `script-doctor` (post-your-draft only)
Runs after **you** write `final.md`. Flags only — never rewrites.

Checks:
1. Hook test: does the first 8 seconds contain a concrete payoff?
2. Pacing: any 90s without a beat shift?
3. Open loops: every hook promise closed?
4. Jargon: any term that loses a smart-but-non-specialist viewer?
5. CTA placement: sub-ask after the payoff lands?
6. Citation completeness: every load-bearing claim cited inline?

**Output:** marked-up file with `[ISSUE: ...]` annotations. You decide what to fix.

---

#### `broll-mapper`
After `final.md` is locked. Line-by-line shot list with timecodes. Each visual marked: ✅ have / 🔎 need to source / 🎨 need to create / ⚠️ rights risk. Builds the prioritized hunt list.

---

### Phase 4 — Packaging

#### `title-forge`
Generates ≥12 titles across angles (curiosity, contrarian, named-figure, number, question, primary-source flex). Scores each on clarity at thumb size, keyword presence, CTR potential, and authenticity. **Hard rule:** rejects titles the script doesn't deliver.

#### `thumb-concept-forge` 🥉
*(spec above)*

#### `metadata-builder`
Description (hook → summary → chapters → sources block → boilerplate), chapters from script timings, tags (VidIQ + manual), end-screen recommendations (prefer same-niche cluster), pinned-comment draft.

#### `packaging-qa`
One job: verify title ↔ thumbnail ↔ hook all promise the same thing. The #1 retention killer. ✅ ship or ❌ specific mismatch.

---

### Phase 5 — Film & Edit
**Off limits.** No skills here. Production tracker just records "filmed" and "edited" timestamps.

---

### Phase 6 — Publish & Post

#### `production-tracker`
`state.json` is the single source of truth per video. Every skill updates it. You can ask "status across all in-flight videos" anytime.

#### `pre-publish-qa`
Hard-blocks publish until: citations in description ✅, thumb tested at mobile size ✅, captions uploaded ✅, end screen set ✅, pinned comment drafted ✅, cards added ✅, title↔hook re-verified ✅, IP/legal check on non-EN doc reproductions ✅.

#### `post-publish-monitor`
T+1h, T+6h, T+24h pulls of CTR, AVD %, traffic source mix. Compares against your baselines. If CTR underperforms >25% at T+6h, suggests title/thumb swap from runners-up. If AVD underperforms, queues a retrospective `script-doctor` pass to learn for next time.

#### `comment-triage`
Lightweight (you didn't flag this as a pain). Classifies your channel comments: question / correction / praise / source-request / bad-faith / spam. Drafts replies for legit ones using your `sources.bib`. You approve. Bad-faith gets flagged, not engaged.

#### `correction-log`
Maintains channel-level `corrections.md`. When a real correction is accepted, queues a pinned-comment update and annotates the original `claims.md` so the mistake doesn't recur. For an evidence channel, this *is* the brand.

---

## Build Order (revised against your pains)

**Week 1 — kill the biggest pain:**
1. `channel-memory` + `style-guide` + `project-init` (foundation, half a day)
2. `source-deepening` 🥇
3. `research-to-brief` 🥈

You can already feel the impact: NotebookLM is fuller, the bridge to script is paved.

**Week 2 — kill the second-biggest pain:**
4. `thumb-concept-forge` 🥉
5. `title-forge`
6. `packaging-qa`

**Week 3 — quality and credibility lift:**
7. `claim-auditor`
8. `counterframe-builder`
9. `comment-miner`
10. `translation-checker` (if you're doing Untranslated Evidence soon)
11. `script-doctor`

**Week 4 — narrative scaffolding:**
12. `narrative-architect`
13. `broll-mapper`
14. `metadata-builder`

**Week 5 — operationalize:**
15. `topic-intake`
16. `format-router`
17. `production-tracker`
18. `pre-publish-qa`

**Week 6+ — the flywheel:**
19. `post-publish-monitor`
20. `comment-triage`
21. `correction-log`

---

## MCP Mapping

You already prioritized TubeFlow, Firecrawl, YouTube MCP. They map cleanly:
- **Firecrawl** → `source-deepening` (web/archive scraping), `comment-miner` (article comments)
- **YouTube MCP** → `comment-miner` (competitor videos), `comment-triage`, `metadata-builder`, `post-publish-monitor`
- **TubeFlow** → `topic-intake`, `post-publish-monitor`
- **NotebookLM** → no MCP today, but you're already piping it via Claude Code; `notebook-querier` formalizes that.

---

## What this leaves you doing manually

The script. The film. The edit. The thumbnail design. The publish click.

Everything else gets prepped so when you sit down to do those five things, you're never blocked on missing research, missing translations, missing angles, missing source citations, or missing concept direction.
