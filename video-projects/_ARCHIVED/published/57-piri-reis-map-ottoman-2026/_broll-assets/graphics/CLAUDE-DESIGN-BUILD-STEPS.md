# Building the Piri Reis explainer deck in Claude Design — step by step

**Goal:** rebuild/animate the 6 forensic-dossier slides in Claude Design (claude.ai/design), keeping them clean and **not AI-generated-looking**, then hand the result back to Claude Code.
**You'll need:** Claude Pro/Max/Team/Enterprise (Design is in research preview on those plans).
**Inputs to have ready (already in this folder):**
- `piri-explainer-deck.html` — the built deck (carries the full design system)
- `../Piri_reis_world_map_01.jpeg` — the real 1513 map fragment (the ONLY imagery allowed)
- `../Piri_Reis_Map_Translated.svg` — translated map (optional, for watermark/insets)

---

## STEP 0 — The anti-"AI look" rule (state this every session)
The thing that keeps it looking premium and not AI-slop: **no generative imagery, ever.** Real artifact + real typography + hard grid only. Paste this guardrail into Claude Design up front and repeat it if it drifts:

> "Do not generate or illustrate any imagery. The only image allowed is the uploaded Piri Reis map photo. Everything else is typography, rules, and solid color blocks on a dark ground. No gradients-as-decoration, no fake parchment textures beyond a faint film grain, no drop shadows except one subtle card elevation, no icons. Documentary/forensic, calm — not flashy."

---

## STEP 1 — Open and seed the design system
1. Go to **claude.ai/design**.
2. Start a new project. In the composer, **upload `piri-explainer-deck.html`** and the **map JPEG**.
3. First message — lock the brand system (paste):

> "Use the uploaded HTML file as the design system of record — read its `:root` tokens and reuse them exactly. Palette: ink #15120D, paper #EDE4D0, accent (oxidized red) #B0432F, gold #C6A24A, ash #8A8270, card stock #EFE7D4. Type: serif (Iowan Old Style / Palatino / Georgia) for headlines and source text; a clean grotesque (Helvetica Neue / Arial) for labels and verdict lines; monospace (SF Mono / Consolas) for the 'Exhibit' index and citation tags. Every slide: 1920×1080, left-aligned dossier grid, ~120px action-safe margins, a faint film grain, a mono 'EXHIBIT ·' index top-left, a mono citation tag bottom-left, and the red accent used on exactly ONE element. Build six slides matching the HTML, then we refine one at a time."

That's the whole brand kit — Design will inherit it so all six stay consistent.

---

## STEP 2 — Build the six slides (paste each prompt; copy is exact, don't retype)

**Slide 1 — The Source List**
> "Slide 1. Exhibit index: 'INSCRIPTION No. 6'. Eyebrow (mono): 'WHAT PIRI REIS WROTE IN THE CORNER'. Headline (serif, huge): 'The Source List'. Then a 4-row ledger, each row = big gold quantity · serif source · right-aligned mono date-tag:
> 8 · Ptolemaic world maps · 'Greek textbook — reprinted 1400s'
> 1 · Arab map of India · 'medieval'
> 4 · Portuguese charts · 'early 1500s'
> 1 · map by **Christopher Columbus** (Columbus in red) · 'c. 1490s — within living memory'
> Verdict line (sans, bold): 'Every source named. **None of them ancient.**' (second sentence in red). Citation tag: 'Inscription no. 6 · Soucek translation'."

**Slide 2 — The Word**
> "Slide 2. Exhibit: 'THE WORD'. Centered horizontal transform: left group = Arabic 'جغرافيا' large, transliteration 'jughrafiya' in gold, gloss 'ARABIC FOR “GEOGRAPHY”'. A thin arrow labeled 'DROP ONE DOT'. Right group = 'cağferiye' transliteration in red, with 'A WORD THAT MEANS NOTHING' under it. Below, a serif explainer: 'In Arabic, ghayn (غ) and ʿayn (ع) are the same letter — separated by a single dot. Drop the dot, swap one more letter, and “geography” turns into a word no one can translate.' Citation: 'Kahle 1933 · Pinto · McIntosh'. Keep the Arabic accurate and right-to-left."

**Slide 3 — Mistake 1**
> "Slide 3. Exhibit: 'MISTAKE 1 of 2'. A giant red serif numeral '1' beside a stacked label: 'THE WORD' (sans, bold, huge) and 'WHOSE ERROR · CHARLES HAPGOOD, 1966' (mono, Hapgood in gold). Body (serif): 'He read a misspelled word — “cağferiye” (red) — as the name of an ancient, mysterious kind of map.' Then a gold-arrow line: 'It just means “geography.” The eight maps were ordinary Ptolemaic atlases, reprinted across Renaissance Europe.' Citation: 'McIntosh · Kahle, “A Lost Map of Columbus,” 1933'."

**Slide 4 — Two Ptolemys (split)**
> "Slide 4. Exhibit: 'TWO MEN, ONE NAME'. Headline (serif): 'There are two famous Ptolemys.' Then a 3-column split: LEFT — role 'THE MAPMAKER' (gold mono), name 'Claudius Ptolemy' (serif), 'c. 150 AD' (mono), desc 'Wrote the Geographia — the atlas reprinted across Renaissance Europe.' CENTER — a vertical divider with a big red '300' and 'YEARS APART' (mono). RIGHT — role 'THE GENERAL', name 'Ptolemy I Soter', 'd. 282 BC', desc 'One of Alexander the Great’s generals. Founded the dynasty, not the maps.' Footer (sans bold): 'Piri Reis **confused the two.**' (confused the two in red). Citation: 'McIntosh · Gaspar'."

**Slide 5 — Mistake 2**
> "Slide 5. Same layout as Slide 3. Exhibit: 'MISTAKE 2 of 2'. Giant red '2'. Label 'THE DATE' + 'WHOSE ERROR · PIRI REIS HIMSELF' (himself in gold). Body (serif): 'He thought his maps reached back to Ptolemy I (red) — to Alexander’s day. They didn’t.' Gold-arrow line: 'That one slip is the only place “the time of Alexander” on the source list comes from — the line Hapgood built his Library of Alexandria on.' Citation: 'McIntosh, p. 18 · Inscription no. 6'."

**Slide 6 — The Ledger (payoff)**
> "Slide 6. Exhibit: 'THE LEDGER'. Headline (sans bold): 'Two mistakes, **not one.**' (not one in red). A 2-column table, ruled: LEFT cell — 'MISTAKE 1 · the word · Hapgood' (mono, 1 in red), 'cağferiye misread' (serif), 'A misspelling of jughrafiya — geography. The 8 maps were ordinary atlases.' RIGHT cell — 'MISTAKE 2 · the date · Piri Reis' (2 in red), 'two Ptolemys confused', 'Produced “the time of Alexander” — read by Hapgood as deep antiquity.' Close line (serif): 'Stacked, they look like a lost civilization. **Separately, neither is evidence of anything.**' (second sentence red). Citation: 'Kahle 1933 · McIntosh · Soucek'."

---

## STEP 3 — Ground it in the real artifact (the non-AI move)
> "On slides 1 and 2, place the uploaded Piri Reis map photo as a very faint left-edge watermark (≈5% opacity, fading to nothing by mid-frame). Do not stylize or regenerate it — use the photo as-is, desaturated. This proves we hold the primary source."

---

## STEP 4 — Refine (use Design's native controls, not just chat)
- **Inline comments:** click any element, drop a comment ("make this 10% smaller", "tighten leading", "move red marker to the dot only").
- **Direct edits:** drag/retype text on canvas.
- **Adjustment controls:** use the per-element sliders for size/weight/spacing.
- Refinement prompts that keep it clean: *"reduce to one accent per slide"*, *"increase contrast for mobile — assume 160px tall in a feed"*, *"align everything to the left margin, no centered blocks except slide 2"*.

---

## STEP 5 — Add motion (only thing worth doing here vs the static HTML)
> "Add restrained motion: Slide 1 ledger rows type/fade in top to bottom on a beat; Slide 2 the dot visibly drops and the word morphs jughrafiya → cağferiye; Slide 4 the red '300 YEARS APART' snaps in last. No bouncing, no easing flourishes — documentary timing, ~0.3s holds."

---

## STEP 6 — Export & hand back to Claude Code
- For **B-roll you screen-record**: export **standalone HTML** (animated) or **PNG/PDF** stills at 1920×1080.
- For **editing in your NLE**: PNGs with transparent or solid #15120D background, one per slide.
- To bring it back here for tweaks: click **"Send to local coding agent"** (or "Send to Claude Code Web") — that ships the handoff bundle, and I wire/adjust it in the repo.

---

## Reality check
The static HTML deck already in this folder is finished and render-verified. Claude Design only earns its keep here for **motion** (Step 5) and easy **PPTX/Canva** exports. If you're filming tomorrow, the HTML is the safe path; do the Design pass only if you want the animated word-morph and ledger build-ons.
