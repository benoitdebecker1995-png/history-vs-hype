# Metadata Execution Plan — Video #52 Hijab

**Prepared by:** Opus 4.7 (planning pass)
**Executor:** Sonnet 4.6 (next session)
**Date:** 2026-05-20
**Scope:** Finalize `YOUTUBE-METADATA.md` + flag fact-check issue. No re-filming. No SRT edits. Metadata-only pass.
**Estimated execution time:** 15-20 min

---

## 0) Read this first

This plan is self-contained. Sonnet should NOT re-query NotebookLM, re-read the SRTs, or spawn sub-agents. All inputs are captured below. Execute Section A, gate-check against Section D, log to Section E target file.

---

## 1) Context dump

### 1.1 SRT changes (rough cut → finished cut)
Same total runtime (~11:26). Substantive content edits, not just transcription fixes:

**Cut from rough cut:**
- Tabari's "Dat Yehud" defense quote (harassers' legal defense) — replaced with cleaner mechanic explanation
- Ibn al-Jawzi's exact quoted reasoning ("if you let an old free woman walk around uncovered…") — now summarized
- "Dat Yehudit" naming in Jewish-law beat

**Fixed (incomplete sentences in rough cut, now resolved):**
- "made the veil mandatory on pain of 74 lashes" (was "made the story…")
- "favorite wife of Muhammad" (was "favorite woman")
- "use her face as the signal" (was cut mid-sentence)
- "baseline across the entire region when Islam arrived" (was a gap)

**New SRT typos in finished cut (will be fixed later via `/fix` skill — NOT this pass's job):**
- "Gast of your veil" → should be "Cast off your veil"
- "must fail in public" → "must veil in public" (whisper "veil"/"fail" artifact throughout)
- "Aisha Bintalha" → "Aisha bint Talha"
- "all three women" → "all free women"
- "Gita Palahani" → "Kitāb al-Aghānī"

### 1.2 Confirmed thesis (from project NotebookLM, 28 sources)
The veil is a **state mechanism for marking the legal boundary between protected and unprotected women.** Across 3,200 years — Assyria → Greco-Roman → Byzantium → Jewish law → early Islam → medieval jurists → Iran 1936 → Iran 1983 → Afghanistan 2024 → France 2010 — the constant is state control of cloth, not religion. Quran exegesis is evidence, not the argument.

### 1.3 Scholar-grounded mechanism phrases (verbatim)
| Scholar | Phrase | Citation |
|---|---|---|
| Mernissi | "political weapon" / "sacred divide" | The Veil and the Male Elite, pp. 20:860, 21:1006 |
| Ahmed | "privilege of rank" / "marker of status" | Women and Gender in Islam, p. 23:1151 |
| Lerner | "mark of status" / "institutionalized split" / "legal classification" | Creation of Patriarchy, ch. 5-6 |
| Llewellyn-Jones | "portable seclusion" | Aphrodite's Tortoise, p. 5 |
| El Cheikh | "imperial brand" | Women, Islam, and Abbasid Identity, p. 15:481 |
| Katz | "visual distinction" | Women in the Mosque, p. 25:1206 |
| Geissinger | "scopic regime" (borrowed from Martin Jay) | Gender and Muslim Constructions of Exegetical Authority, p. 216, fn. 25 |

### 1.4 Hard constraints from Thumbnail Inspiration notebook (650-thumb dataset)
- **12-character HARD LIMIT** on overlay text. Failure case: "ELIMINATE SALIENT" (17 chars) failed comprehension; "MOVED" (5 chars) passed.
- **2-4 words** is niche standard (87% of n=650).
- **0% talking-head face.** Historical subject photos OK (27% of closest matches).
- **Two-sentence title formula** = 11% outlier rate (3x+ views, strongest structural pattern).
- **Scale words** ("every," "all," "entire," "century") = 1.33x lift.
- **Primary-source overlay** = +10 points on channel rubric.
- **Documentary aesthetic** — muted colors, bold sans-serif (Montserrat/Oswald/Impact), white/yellow on dark.
- **Closest precedent in corpus:** "Iran vs Its Own Democracy. 6 Revolutions in 120 Years" scored 85/A.

### 1.5 ⚠️ Critical fact-check finding (already filmed)
Script attributes "Scopic Regime" to "Historian Lloyd Jones" at ~01:02:19. **Actual attribution:** "scopic regime" is **Aisha Geissinger's** term (borrowed from Martin Jay via Christian Metz). Llewellyn-Jones's actual coinage is "**portable seclusion**" — a different concept (veil as wearable home). This is an Auditor's Edge violation. See Section A2 for remediation.

---

## 2) Section A — File edits

### A1) `YOUTUBE-METADATA.md`

#### A1.1 — Replace Title Variant 3

**Current** (lines 28-34):
```
### Variant 3 — Doorway B (forensic invitation)
*"The Hijab Wasn't Made Mandatory by the Quran. Three Medieval Scholars Did."*
- **Length:** 76 chars
- **Front-loaded keyword:** "hijab"
- **Promise:** named-mechanism reveal, three scholars angle
- **Audience selected:** mechanism-curious (PolyMatter / Asianometry overlap)
```

**Replace with:**
```
### Variant 3 — Doorway B (thesis reveal)
*"The Hijab Wasn't Modesty. It Was a Property Law."*
- **Length:** 50 chars
- **Front-loaded keyword:** "hijab"
- **Promise:** thesis-level reveal — state mechanism, not religious doctrine
- **Pattern:** Two-sentence formula (11% outlier rate, 3x+ views — strongest structural pattern in 650-thumb dataset)
- **Audience selected:** mechanism-curious (PolyMatter / Asianometry overlap)
- **Scholar-grounded:** Echoes Lerner's "legal classification" and Ahmed's "privilege of rank" framings
```

**Reason for change:** The "three medieval scholars" promise is unfulfilled in the finished cut — only Ibn al-Jawzi is named. Replacement uses the two-sentence outlier formula, is fully defensible against the script's actual thesis, and pairs with the Tight-Bridge Variant 1 thumbnail.

#### A1.2 — Replace all three Thumbnail Concepts

**Delete** lines 39-59 (the three current concepts).

**Replace with:**
```markdown
## THUMBNAIL CONCEPTS (paired with title variants)

### Variant 1 (PRIMARY) — Evidence Anchor — paired with V3 title
- **Title pairing:** "The Hijab Wasn't Modesty. It Was a Property Law."
- **Overlay:** **"PROPERTY LAW"** (12 chars, 2 words — at hard limit)
- **Focal point:** Macro close-up of the Middle Assyrian Law 40 tablet (cuneiform).
- **Treatment:** High-res cuneiform texture, dark navy/charcoal background. Subtle yellow glow around the specific section of the tablet that names the law. Bold sans-serif overlay (Impact/Oswald), white text with thin dark stroke for mobile legibility.
- **2-second comprehension:** "Ancient stone document... PROPERTY LAW." Reads as a legal/origin reveal, not an opinion piece.
- **Bridge:** TIGHT. The first 30 seconds of the hook introduces this exact tablet — "a law from 1200 BCE from the Middle Assyrian Empire."
- **Score estimate:** 95/100 (40 evidence + 25 text + 20 composition + 10 tension).
- **Source:** British Museum digital collection / Driver & Miles 1935 edition photographs.

### Variant 2 — Visual Paradox — paired with V1 title
- **Title pairing:** "The Veil Was Forbidden for Slaves 2,000 Years Before Islam Made It Mandatory."
- **Overlay:** **"FORBIDDEN"** (9 chars, 1 word)
- **Focal point:** Split-frame contrast.
  - LEFT (muted grey): Astarte hierodule ivory (unveiled figure, British Museum, imported from Phoenicia to Nimrud).
  - RIGHT (warm gold museum lighting): Ashurbanipal feast relief detail showing the veiled Queen Ašur-šurrat (BM WA 124920, c. 645 BCE).
- **Treatment:** Red "FORBIDDEN" stamp angled across the unveiled figure on the left. Documentary palette, no editorial overlay on the queen.
- **2-second comprehension:** "Two ancient women... wait, being unveiled was the forbidden state?" Visual paradox.
- **Bridge:** ADEQUATE. Relief and ivory illustrate the Assyrian/early-Islamic mechanism described in the first 2 minutes.
- **Score estimate:** 85/100 (30 evidence + 25 text + 15 composition + 15 tension).
- **Source:** British Museum holdings, both objects in public domain photographs.

### Variant 3 — Status Reveal — paired with V2 title
- **Title pairing:** "The Hijab Was a Status Symbol Before Islam Adopted It."
- **Overlay:** **"ELITE ONLY"** (10 chars, 2 words)
- **Focal point:** Zoomed cutout of the veiled Queen Ašur-šurrat from the Ashurbanipal feast relief (BM WA 124920), right side of frame.
- **Treatment:** Queen cutout right, bold yellow "ELITE ONLY" left. Background desaturated, clarity/structure boost on the veil's cloth texture so it reads as a luxury item, not generic costume.
- **2-second comprehension:** "Ancient royal woman... veiling was for the elite." Class-based mechanism signal.
- **Bridge:** ADEQUATE. Connects to "changes the frame entirely" in the hook and pays off in the cross-civilization sweep.
- **Score estimate:** 75/100 (25 evidence + 20 text + 20 composition + 10 tension).
- **Source:** British Museum WA 124920.

**Channel rule:** Real materials > AI. No generated faces. No clickbait selfies. All three concepts use authenticated museum-collection imagery in public domain.

**Primary slot rationale:** Variant 1 is the only Tight Bridge — the tablet appears on screen in the first 30 seconds, so click → first-frame retention is mechanically guaranteed. Variants 2 and 3 rotate as B-tests.
```

**Reason for change:** Earlier concepts violated the 12-char hard limit ("POLITICAL WEAPON" 16, "BANNED → MANDATORY" 18). New concepts all pass the limit, have a human/historical-subject element (channel rule), are paired explicitly to specific title variants, and the primary concept achieves a Tight Bridge to the literal opening of the video.

#### A1.3 — Compress chapter list in description

**Current chapters block** (lines 84-93, 9 entries that don't match the finished cut runtime):
```
0:00 Three governments, opposite rules, same move
1:07 Five civilizations, one rule (Assyrian, Greek, Talmudic, Byzantine, Sasanian)
2:37 What Islam inherited — and what it changed
2:52 The verse that wasn't about modesty (Q. 33:59)
3:52 Two scholars, four hundred years later (al-Tha'labi, al-Biqa'i)
4:52 Ibn al-Jawzi closes the last exemption
6:52 The logic collapsed when slavery ended. The rule didn't.
7:22 How the ruling survived into the modern state
7:52 France, Iran, and the eight-hundred-year argument
```

**Replace with:**
```
0:00 The veil before Islam — a law from 1200 BCE
1:18 Five civilizations, one mechanism
2:50 What the Quran actually says
4:31 Caliph Umar enforces the class line
7:11 Medieval jurists close every loophole
9:19 A note on personal faith vs state law
9:46 Iran, Afghanistan, France — same mechanism, different states
```

**Reason:** 7 chapters covers major structural pivots, each ≥ 60 seconds (YouTube minimum). Drops noisier sub-beats. Old chapters had wrong timestamps (ended 7:52, actual video runs 11:26) and referenced cut content (al-Tha'labi, al-Biqa'i no longer in finished cut).

#### A1.4 — Fix description body

**Current** (description block, lines 65-99) has two problems:
1. Dangling fragment: *"required free women to —"* (sentence never completes)
2. False promise: *"three named medieval Muslim scholars"* (only Ibn al-Jawzi is named in finished cut)

**Replace the description code block (between the triple backticks at line 65 and the closing backticks at line 99) with:**

```
Hijab debates always come back to one question: is it a religious obligation, or isn't it?

The answer is on a stone tablet from 1200 BCE — three thousand years before Islam existed.

This video traces the actual mechanism. How a 2,000-year-old class marker — one that flogged slaves for wearing the veil and required free women to wear it as a sign of legal protection — was inherited by Islam, universalized by medieval jurists, and now sits at the center of every modern veil law from Iran's morality police to France's 2010 ban to Afghanistan's 2026 criminal code. Same mechanism, different states.

ACADEMIC SOURCES (full citations):
• Ahmed, Leila. Women and Gender in Islam. Yale University Press, 1992.
• Mernissi, Fatima. The Veil and the Male Elite. Basic Books, 1991.
• Bauer, Karen. Gender Hierarchy in the Quran. Cambridge University Press, 2015.
• Geissinger, Aisha. Gender and Muslim Constructions of Exegetical Authority. Brill, 2015.
• Katz, Marion Holmes. Women in the Mosque. Columbia University Press, 2014.
• El Cheikh, Nadia Maria. Women, Islam, and Abbasid Identity. Harvard University Press, 2015.
• Llewellyn-Jones, Lloyd. Aphrodite's Tortoise: The Veiled Woman of Ancient Greece. Classical Press of Wales, 2003.
• Lerner, Gerda. The Creation of Patriarchy. Oxford University Press, 1986.
• Heath, Jennifer (ed.). The Veil. University of California Press, 2008.

CHAPTERS:
0:00 The veil before Islam — a law from 1200 BCE
1:18 Five civilizations, one mechanism
2:50 What the Quran actually says
4:31 Caliph Umar enforces the class line
7:11 Medieval jurists close every loophole
9:19 A note on personal faith vs state law
9:46 Iran, Afghanistan, France — same mechanism, different states

ABOUT THE CHANNEL:
History vs Hype is evidence-based mythbusting on geopolitics, colonial history, and ideological narratives. Every claim verified against academic primary sources, with page numbers in the description.

Disagree with something? Comment below — I read every comment and respond when I can be useful.
```

**Source-list changes vs current:**
- Added: Geissinger (cited in script — must be credited per Auditor's Edge)
- Added: Lerner (the foundational class-marker analysis — heavily used in notebook synthesis)
- Removed: Reda & Amin (no quote from this volume appears in finished cut)
- Removed: Secunda's Talmud's Red Fence (Jewish law beat tightened in finished cut — Secunda no longer load-bearing)

#### A1.5 — Update tags

**Current tag block** (lines 114-140). Keep all existing tags. **Append** at the end (before closing backtick):
```
scopic regime
assyrian law 40
caliph umar
taliban hijab law
aisha bint talha
property law history
```

Confirm total tag count still under YouTube's 500-char limit. If over, drop weakest tags from current list: "religious history" and "gender history" (too generic, low search anchor value).

#### A1.6 — Update A/B Rotation Hypothesis

**Current paragraph** (line 172, "Hypothesis: Doorway B…").

**Replace with:**
```
**Hypothesis:** Variant 1 ("PROPERTY LAW" + Assyrian tablet, paired with V3 "Hijab Wasn't Modesty" title) wins on raw CTR — it's the only concept with a Tight Bridge to the literal opening 30 seconds of the video, and the closest match to the corpus's highest-scoring precedent ("Iran vs Its Own Democracy" 85/A). Variant 2 ("FORBIDDEN" + split paradox, paired with V1 grenade title) wins on visual-paradox CTR but bridges adequately, not tightly. Variant 3 ("ELITE ONLY" + Queen Ašur-šurrat, paired with V2 status-symbol title) is the conservative fallback — single-subject Knowing-Better model, lower variance, brand-recognition slot.
```

### A2) `04-ROUGH-CUT-POSTMORTEM.md`

**Append at end of file** (check for existing Finding numbering — find the last `## Finding #N` and use N+1):

```markdown
## Finding #N — Scopic Regime Attribution Error (Auditor's Edge)

**Severity:** HIGH — already in filmed audio
**Source of finding:** NotebookLM query 2026-05-20, project notebook 322e3b05-5960-4036-8dac-02e2377db07c

The script attributes "Scopic Regime" to "Historian Lloyd Jones" at timestamp ~01:02:19.

**Actual attribution per sources in the notebook:**
- "Scopic regime" originates with Christian Metz (French film theorist), via Martin Jay, brought into Islamic studies by **Aisha Geissinger** (Gender and Muslim Constructions of Exegetical Authority, Brill 2015, p.216, fn.25). Verbatim definition: "A way of seeing that has been molded by human beings, and has changed and developed through time."
- **Lloyd Llewellyn-Jones** writes about veils as social regulation in Aphrodite's Tortoise but his term is "**portable seclusion**" — a different concept (the veil as wearable home / spatial technology, p. 5).

**Remediation options (decide before publish):**
1. **Edit cut:** Remove the "Historian Lloyd Jones named this entire architecture the Scopic Regime" line (~3 sec). Keep the concept sentence that follows ("a system in which visibility itself functions as a social regulation"). Cleanest fix.
2. **Pinned correction comment:** Acknowledge in pinned comment post-publish. Lower edit cost; on-brand for the channel; satisfies Auditor's Edge by surfacing the correction rather than hiding it.

**Default recommendation:** Option 2 (pinned correction comment). Lower-risk; doesn't require re-editing; aligns with channel's transparency positioning. User can override to Option 1 if they want the cleaner cut.
```

### A3) New file: `06-METADATA-EXECUTION-LOG.md`

Create this file in the same project folder. Sonnet fills the checkboxes as it goes:

```markdown
# Metadata Execution Log — Video #52
**Executed:** [date Sonnet runs the plan]
**Executor:** Sonnet 4.6
**Plan source:** `06-METADATA-EXECUTION-PLAN.md` (Opus planning pass 2026-05-20)

## Changes applied
- [ ] YOUTUBE-METADATA.md — A1.1 Title Variant 3 swapped to "Property Law"
- [ ] YOUTUBE-METADATA.md — A1.2 Thumbnail concepts replaced (3 new, all ≤12 char overlay)
- [ ] YOUTUBE-METADATA.md — A1.3 Chapter list compressed (9 → 7, timestamps corrected to finished cut)
- [ ] YOUTUBE-METADATA.md — A1.4 Description dangling-fragment fix + source list updated
- [ ] YOUTUBE-METADATA.md — A1.5 Tags appended
- [ ] YOUTUBE-METADATA.md — A1.6 A/B hypothesis paragraph rewritten
- [ ] 04-ROUGH-CUT-POSTMORTEM.md — Finding #N (Scopic Regime attribution) appended

## Verification gate results
- [ ] All three thumbnail overlays confirmed ≤ 12 chars
- [ ] No years in titles
- [ ] No colons in titles
- [ ] Chapter timestamps end at or before 10:59 (last beat in finished cut)
- [ ] No new claims added that aren't in finished cut SRT
- [ ] No edits to script files (SCRIPT.md, FINAL-SCRIPT-TELEPROMPTER.txt)

## Open decisions for user (post-execution)
- [ ] Scopic regime attribution: edit cut vs pinned comment (default pinned)
- [ ] Final approval of Variant 3 title ("Property Law")
- [ ] Thumbnail PNG production (use `/thumbnail` skill or hand-design)

## Diff summary
[Sonnet fills in: which lines changed in which files, with line ranges]
```

---

## 3) Section B — Decision points

These are gray-area calls. Defaults specified; Sonnet uses the default unless user has overridden in conversation.

| Decision | Default | Override condition |
|---|---|---|
| **B1** Title Variant 3 wording | *"The Hijab Wasn't Modesty. It Was a Property Law."* | User picks an alternative from prior conversation |
| **B2** Scopic Regime remediation | Pinned correction comment (Option 2) | User explicitly requests edit cut |
| **B3** Thumbnail primary slot | Variant 1 (PROPERTY LAW + tablet) | User picks different primary |

If any decision is ambiguous and there is NO conversational override, Sonnet should AskUserQuestion ONCE with all three decisions in a single multi-question block.

---

## 4) Section C — Execution order

1. **Read in parallel:** This plan + `YOUTUBE-METADATA.md` + `04-ROUGH-CUT-POSTMORTEM.md` (3 Read calls in one message).
2. **Resolve decisions:** Check conversation context for B1/B2/B3. If unresolved, single AskUserQuestion block. Otherwise proceed with defaults.
3. **Apply edits in order:** A1.1 → A1.2 → A1.3 → A1.4 → A1.5 → A1.6 via Edit tool calls. Each as a discrete Edit (no batching of unrelated sections).
4. **Append A2** to `04-ROUGH-CUT-POSTMORTEM.md`. Find next Finding number first.
5. **Write A3** (`06-METADATA-EXECUTION-LOG.md`) with all checkboxes filled per actual execution.
6. **Report back** with a one-paragraph summary: which files changed, which decisions used defaults, anything that needed user input.

---

## 5) Section D — Verification gates

Sonnet must confirm these before reporting done:

- [ ] All three thumbnail overlays ≤ 12 chars (verify by counting)
- [ ] Description first 150 chars front-load the hook question
- [ ] No years in any title variant
- [ ] No colons in any title variant
- [ ] Chapter timestamps land within the finished cut runtime (≤ 11:26)
- [ ] Chapter count = 7 (not the previous 9)
- [ ] No new claims added that aren't in finished cut SRT
- [ ] No edits to script files (SCRIPT.md, FINAL-SCRIPT-TELEPROMPTER.txt, SCRIPT-v3.1-locked.md, SCRIPT-TELEPROMPTER.txt)
- [ ] No edits to SRT files (`finsihed cut.srt`, `rough cut.srt`)
- [ ] Tag list still under 500 chars (YouTube limit)

---

## 6) Section E — Do-NOT list

Sonnet must NOT:
- Generate or rewrite any portion of the script
- Re-render any SRT or generate captions
- Create thumbnail PNG files (those are produced separately via `/thumbnail` skill or hand-design after this metadata pass)
- Run `/fix` on the SRT (separate post-publish workflow)
- Re-query NotebookLM (all needed queries already done; results captured in Section 1)
- Spawn sub-agents
- Edit `PROJECT-STATUS.md` (lives outside metadata scope; reconciled separately via `/reconcile` at publish time)
- Edit `01-VERIFIED-RESEARCH.md`, `02-SCRIPT-DRAFT.md`, `03-FACT-CHECK-VERIFICATION.md` (locked source-of-truth files)
- Touch the `_research/` subfolder or anything in `_gemini-output/`

---

## 7) Handoff signal

When Sonnet completes execution and verification, it reports:

```
✅ Metadata execution complete for #52.
   Files modified: YOUTUBE-METADATA.md, 04-ROUGH-CUT-POSTMORTEM.md
   File created: 06-METADATA-EXECUTION-LOG.md
   Decisions used: B1 default, B2 default, B3 default [or list overrides]
   Outstanding: thumbnail PNG production (user's job)
```

Then stop. Do not proceed to publish-day checklist, thumbnail rendering, or any downstream task.
