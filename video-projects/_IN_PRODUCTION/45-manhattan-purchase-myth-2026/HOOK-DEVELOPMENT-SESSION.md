# Hook Development Session — Manhattan Purchase Myth (#45)

**Date:** 2026-04-16
**Status:** Hook locked at Version A (Inwood Hill plaque opener) — pending B-roll confirmation before applying to SCRIPT.md
**Resume here:** "Lock Version A and apply to SCRIPT.md, or test against B/C?"

---

## Context

Video #45 is fact-checked and NLM-audited. Title locked: "The Dutch vs The Lenape. Manhattan Was Never $24." Goal pivoted from subscriber retention to **search + browse acquisition** because channel has 515 subs (no real audience to leverage).

Current SCRIPT.md hook (line 1 of HOOK section): "This is the only document from 1626 that mentions the purchase of Manhattan." → Document/Object Anchor pattern. Competitor data shows this pattern earns 0.65% sub conversion vs 5.4x for specificity bombs. Bad fit for cold-traffic acquisition.

---

## Process Walked Through

### Step 1: Competitor pattern query (Notebook: Competitor Script Structure Analysis — Wave 2)

Found 5 hook patterns ranked by performance. Best for HvH at 515 subs:
- **Specificity Bomb** (5.4x sub conv, 4.27M avg views) — WonderWhy, Historia Civilis
- **Standard Myth Subversion** (KB style, 2.31% conv) — requires loyal audience, NOT a fit yet
- **Document/Object Anchor** (current hook, 0.65%) — fails for search/browse acquisition

Time-to-topic for top performers: WonderWhy 1-15s, Three Arrows 5-15s, Knowing Better 15-60s.

Recommendation: hybrid Specificity Bomb + Myth Contradiction.

### Step 2: First draft

> "We all know the story of the Manhattan Purchase. In 1626, the Dutch bought the island from the Lenape for 60 guilders — about $24 in beads.
> The beads were painted into the story in 1853.
> The $24 figure was made up by a journalist in 1844.
> The Canarsee trickster angle came from a magazine in 1959.
> The only surviving document from 1626 is one sentence in a Dutch cargo manifest. It mentions no scam, no beads, and no $24."

User feedback: "not fluent enough... stiff."

### Step 3: Fluency rewrites (Notebook: The Mind's Eye — Twenty-First Century Style)

Diagnosis: teleprompter flatline (3 middle sentences identical syntax), passive zombies ("were painted into," "was made up by"), missing coherence connective between myth and debunk.

3 rewrites delivered (Frankopan artifact anchor / Pinker Necker Cube Flip / Minto staccato pyramid). Recommended **Pinker Necker Cube Flip**:

> "We all know the legend. In 1626, the Dutch scammed the Lenape out of Manhattan for twenty-four dollars in beads. But that story isn't history. It was assembled backwards over three centuries. A journalist invented the twenty-four dollar receipt in 1844. A painter added the glass beads in 1853. A magazine fabricated the Canarsee trickster in 1959. Look at the only actual witness — a 1626 Dutch cargo manifest called the Schagen letter — and the scam vanishes. No beads. No price tag. Just a single sentence."

User feedback: "want to change the schoolchild thing — there's a play, a movie, a statue. Maybe statue is best."

### Step 4: Pop culture artifact inventory (Notebook: Manhattan Purchase Myth — Phase 2 Research)

Verified artifacts of the myth:
- **Inwood Hill Park rock + plaque** (still standing, photographable) — best
- **Hudson-Fulton parade float** (1909, no surviving photo) — unusable
- **Ranney's painting** (1853) — covered later in script
- **Too Many Girls** Broadway musical (1939) — "Give It Back to the Indians"
- **Manahatta** (2023, Mary Kathryn Nagle) — modern corrective, wrong direction for hook

Notebook frames the plaque as: "physically cementing a historical forgery into the geography of New York City."

### Step 5: Final hook variants (3 tested)

**Version A — Plaque as Antagonist (LOCKED PENDING B-ROLL):**
> "There's a rock in Inwood Hill Park with a plaque on it. The plaque says this is where the Dutch bought Manhattan from the Lenape in 1626 for twenty-four dollars in beads.
> Almost everything on that plaque is a lie.
> A journalist invented the twenty-four dollar price in 1844. A painter added the beads in 1853. A magazine fabricated the trickster angle in 1959. The only surviving record from 1626 is a single sentence in a Dutch cargo manifest. It mentions no beads. No twenty-four dollars. And no Inwood Hill."

**Version B — Three-Artifact Stack:**
> "There's a rock in Inwood Hill Park that marks the spot. There's an 1853 painting that shows the chest of beads. There's a Broadway song from 1939 telling the Lenape to take it back. Three artifacts. One famous story. Almost none of it happened. [...continues...]"

**Version C — Plaque + Tourist Frame:**
> "If you walk to the northern tip of Manhattan, in Inwood Hill Park, you'll find a boulder with a bronze plaque. [...continues...]"

---

## Open Decisions (Resume Here)

1. **B-roll availability for Inwood Hill plaque** — must confirm before locking Version A. Check Wikimedia, Flickr, NYC Parks. If no usable footage exists, fall back to Version B (uses 3 artifacts, more coverage flexibility).
2. **Apply to SCRIPT.md** — replace lines 1-3 of current HOOK section with Version A.
3. **Update YOUTUBE-METADATA.md** — refresh "Stumble Sentences" section with new hook delivery notes.
4. **Hook scorer rerun** — once locked, run `tools/hook_scorer.py` to validate 5.4x specificity bomb classification.

---

## Notebooks Used (for follow-up queries)

- `438186cd-045e-40b1-ae67-9ecf25fcb415` — Competitor Script Structure Analysis Wave 2 (hook patterns)
- `b04802f4-0f8e-436b-b78d-0c5479272885` — The Mind's Eye: Twenty-First Century Style (fluency rewrites)
- `92a51593-8878-4314-a144-bb926ef1584a` — Manhattan Purchase Myth Phase 2 Research (artifact inventory)
