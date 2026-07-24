# Thumbnail Concepts — #59 Israel/Palestine (Res 181)

---

## 🔒 LOCKED BUILD BRIEF v2 (2026-07-04) — supersedes the /thumbnail concepts below

**Direction:** a clean 1947 UN partition **flag-map** as the single focal point (map + flags + text = recognition; the map itself *answers* the title). Chosen over the document/highlighted-text concepts because the channel's own CTR data rates document-as-focal its **worst** thumbnail category (−0.71) and clean map its **best** (+0.65); and because the live Israel-Palestine SERP is all AI-garbled maps or generic dramatic stock — a clean, accurate map is the differentiation. Validated by: VidIQ (titles 94–97; the "on paper" hook 95–96), a Gemini adversarial pass, and the outlier corpus (WonderWhy territorial exemplar = flag-fill map + visual answer).

**⚠️ Recognition safeguard — MANDATORY on the map concepts (A/B):** the 1947 map is *not* recognizable on its own (Gemini's flagged risk). Recognition must come from big **"ISRAEL vs PALESTINE"** text + the two **flag chips** on their zones. If the map floats without them, it fails. This is what lets A/B override Gemini's "cut them" call.

### Real source assets (creator builds — Claude does NOT render; see `memory/feedback-thumbnail-process.md`)
- **1947 partition map:** Wikimedia Commons *"UN Palestine partition versions 1947.svg"* (public domain) — recolour the two zones to flag colours; or trace flat in MapChart. Official ref: UN Map No. 103.
- **Modern outline (Concept C):** Wikimedia base map of Israel + Palestinian territories.
- **Flags:** Flag of Israel + Flag of Palestine (Wikimedia, PD).
- **Optional bg texture:** UN A/RES/181(II) first page (UN doc, PD) — faint, behind the map only, never the focal.

### Palette / type
- Israel blue `#0038b8` · Palestine green `#007a3d` (red `#ce1126` accent) · Jerusalem = white/checker international dot · background dark `#0b1a2b` **or** parchment `#ece3cf`.
- Overlay font: heavy condensed grotesque (Anton / Bebas Neue / Archivo Black), white with thick black stroke. "ISRAEL vs PALESTINE" same family, smaller.
- ≤3 text elements. Must resolve at ~160px feed size — run `python -m tools.preflight.thumbnail_image_audit <export.png>` before lock.

### Concepts — build all 3 for native A/B rotation (overlays Gemini-validated, plain, gap-not-verdict)

| # | Focal | Overlay | Paired title | Note |
|---|---|---|---|---|
| **A** | Clean partition flag-map, both zones flag-filled, Jerusalem dot | `WHO GOT WHAT?` | *What the 1947 Partition Plan Actually Gave Each Side* (96) | the map **is** the visual answer to the title |
| **B** ⭐ | Same map, the **Arab/Palestinian state highlighted** (glow / faint "never-built" treatment) | `A STATE ON PAPER` | *…Actually Gave Each Side* (96) **or** *The Arab State That Only Existed on Paper* (96) | **PRIMARY** — freshest hook (creator idea), VidIQ-validated 95–96 |
| **C** | Recognizable **modern** outline + 1947 lines **ghosted** (bright dashed) | `THIS WASN'T THE PLAN` (A/B: `NOT THE FIRST MAP`) | *The Document Everyone Cites and Nobody Reads* (94) | recognition-max; **watch ghost-line legibility** at feed size (Gemini + Claude both flag this) |

### A/B EXPERIMENT — 3 full title+thumbnail pairs, OFAT design (2026-07-04)

YouTube rotates 3 full **title+thumbnail pairs** (both vary). This tests the title too — the channel's #1 verified CTR lever (views↔CTR r=0.62) — so it beats holding the title fixed. To keep clean attribution, anchor with one-factor-at-a-time: title+overlay are one coupled **MESSAGE** (they must bridge); the **MAP IMAGE** is the other factor.

| Pair | Title (message) | Map + overlay | Isolates → data point |
|---|---|---|---|
| **1 — anchor** | *…Almost Nobody's Read It* (97) | 1947 **flag-map** + `NOBODY READ IT` | baseline |
| **2** | *…Almost Nobody's Read It* (97) | **modern outline** (1947 partition inside) + `NOBODY READ IT` | **vs 1 = map only** → clean 1947 map vs familiar modern shape (recognition source) |
| **3** | *…The Arab State That Only Existed on Paper* (96) | 1947 **flag-map** + `A STATE ON PAPER` | **vs 1 = message only** → proven "nobody read it" vs fresh "on paper" hook |

Pairs 1 & 3 share the **same map image** (only title+overlay change). Pairs 1 & 2 share the **same message** (only the map changes). Every cell obeys the confirmed rules; the *differences* are the two experiments. Build = **2 base maps** (1947 flag-map, modern outline) + 2 overlays + 2 titles.

**Logging:** pull per-variant CTR from Studio. Only add to the dataset (`CTR-THUMBNAIL-FINDINGS.md` / `thumbnail_features`) if **each variant cleared ~1k+ impressions** — below that it's noise (`feedback-channel-data-too-small.md`). Record BOTH reads: map (P1v2) and message (P1v3).

Optional on any slot: faint Res 181 letterhead as background texture (dossier tone, map stays focal).

---

**Generated:** 2026-06-24
**Title (A, scored 100/100):** Israel vs Palestine. The Document Everyone Cites and Nobody Reads.
**Title (B):** Israel vs Palestine. The Partition Plan Nobody Actually Read.
**Source:** Packaging Intelligence — History vs Hype notebook (grounded, 5 sources)
**Protocol:** THUMBNAIL-RECOMMEND-PROTOCOL.md
**Mandate compliance:** text overlay ✓ (all ≤16 chars) · no face ✓ · map asset for territorial ✓ (Concept 3) · curiosity-gap ✓ (every overlay ≠ title)

---

Based on the **THUMBNAIL-RECOMMEND-PROTOCOL.md** and the provided script thesis, here are three ranked thumbnail concepts for the video on UN Resolution 181.

### Concept 1 (Rank 1: The Forensic Audit)
*   **Visual:** A macro-shot of a manila file folder sitting on a dark, textured desk. The folder is labeled "UN RESOLUTION 181" with a typewriter-style adhesive label. Tucked inside the folder is the 1947 Partition Map, with a physical red "EXHIBIT A" paperclipped to the corner of the document [1, 2].
*   **Text overlay:** "RECOMMENDED ONLY" (16 chars)
*   **(a) Operation:** **TITLE REPETITION + DOSSIER METAPHOR** â€” The overlay echoes the "Nobody Reads" angle of the title while the dossier aesthetic signals "intellectual competence" and forensic depth [1, 3].
*   **(b) Outlier evidence:** 
    *   *What Putin Fears More Than War* (PolyMatter, **6.9x ratio**) â€” used a document_collage and dossier aesthetic to frame the click [3].
    *   *The End of Cheap Chinese Labor* (PolyMatter, **3.7x ratio**) â€” used an aesthetic hook to reinforce a "historical inevitability" thesis [3].
*   **(c) Channel exemplar:** **PolyMatter** â€” Rule: "HvH treaty/legal/diplomatic topics map here. Use DOSSIER METAPHOR aesthetic (folders, classified-document framing, paperclips). Matches 'intellectual competence' subscriber trigger" [1].
*   **Risk:** The "Israel vs Palestine" keyword is highly saturated; if the dossier doesn't look sufficiently "official" or "high-stakes," it may be ignored as generic history.

### Concept 2 (Rank 2: The Mechanism Reveal)
*   **Visual:** A high-contrast macro close-up of the original 1947 UN Resolution text. A modern yellow highlighter "streak" crosses the specific word "Recommends" in the opening paragraph. The rest of the document is slightly desaturated to make the word "Recommends" the primary visual anchor [4, 5].
*   **Text overlay:** "IT WASN'T A LAW" (15 chars)
*   **(a) Operation:** **MECHANISM REFRAME (reveal)** â€” The title bait is the "Document Everyone Cites," while the overlay reveals the actual mechanism/thesis (that it was non-binding) [4, 6].
*   **(b) Outlier evidence:** 
    *   *How Vodka ruined Russia* (Kraut, **7.0x ratio**) â€” overlay names the hidden thesis ("Systemic Addiction") rather than the topic ("Vodka") [3, 6].
    *   *Trump's Biggest Failure* (Kraut, **7.8x ratio**) â€” overlay names the hidden punchline ("Ni Hao") [3, 6].
*   **(c) Channel exemplar:** **Kraut** â€” Rule: "When HvH's title names a topic... but the actual thesis is a mechanism... the overlay should name the thesis, not repeat the topic" [7].
*   **Risk:** This operation requires the viewer to already have the "it was a law" myth loaded in their mind; if they don't, the "It wasn't a law" reveal has no friction and generates no curiosity [8].

### Concept 3 (Rank 3: The Statistical Paradox)
*   **Visual:** A **WonderWhy** style map visual of the 1947 partition blocks (blue and orange). Next to the blue segment (55% land), a stark white label says "33% Pop." Next to the orange segment (representing the 7% ownership), a large "55% Land" label creates a visual mismatch to trigger curiosity [9, 10].
*   **Text overlay:** "THE 7% PARADOX" (15 chars)
*   **(a) Operation:** **COMPRESSION + VISUAL ANSWER** â€” Compresses the "fairness" thesis into a numerical shock while the map visually illustrates the allocation mismatch [9, 11].
*   **(b) Outlier evidence:** 
    *   *Why Ireland Split* (WonderWhy, **6.4x ratio**) â€” long title compressed to 3 words; map answers the split visually [3, 12].
    *   *The Most Complex International Borders* (WonderWhy, **4.8x ratio**) â€” vague title â†’ specific geographies; map color-codes them [3, 12].
*   **(c) Channel exemplar:** **WonderWhy** â€” Rule: "The overlay should compress the title... AND the map should visually answer it. This is the highest-leverage finding for territorial topics" [11].
*   **Risk:** At the current channel size (515 subs), "Visual Answer" maps can sometimes be perceived as dry geography explainers rather than "myth-busting" conflict videos, which have a lower CTR ceiling [13, 14].

***

**Top pick:** **Concept 1.** It best leverages the channel's primary subscriber trigger ("intellectual competence") and uses the **PolyMatter Dossier Metaphor**, which the data identifies as the strongest fit for document-driven forensic audits [1, 2].

**Risk if all 3 fail:** "Israel-Palestine" topics are prone to a **16.7% median intro drop-off** [15]. If the first 5 seconds of the video do not immediately deliver the "Res 181" document on screen to satisfy the packaging promise, retention will collapse regardless of CTR [16, 17].

---

## Build notes (lock before filming)
- **Top pick = Concept 1 (RECOMMENDED ONLY dossier)** — fits the "intellectual competence" trigger + the title's "Nobody Reads" frame; safest on a saturated keyword. Zero-budget: manila folder + printed 1947 partition map + red "EXHIBIT A" tag, shot on a dark desk.
- **Concept 2 (IT WASN'T A LAW)** is the sharpest mechanism reveal but assumes the viewer holds the "it was binding" myth — higher variance. Strong **A/B partner** to Concept 1 (single-variable swap: same map/document, different overlay claim).
- **Concept 3 (THE 7% PARADOX)** is the cleanest territorial-map play; risk = reads as dry geography on a charged topic.
- Recommended path: build **Concept 1**, hold **Concept 2** as the A/B alt. Run `thumbnail_image_audit.py` on the exported PNG for feed-size legibility before locking.
