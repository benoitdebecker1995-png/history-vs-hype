# YouTube Metadata — #56

**Status:** TITLE + THUMBNAIL CANDIDATES DRAFTED (overnight 2026-05-12); locked after exhibit decision + `title_scorer.py` / `thumbnail_checker.py` runs.

---

## Title candidates (overnight draft, all ladder-anchored)

Vance-Pt-1 shape (claim-led + evidence-promise). Each candidate contains *atlantic slave trade*, *african slave trade*, or a clear topic-anchor head term. No colons. No current-year references (historical dates like 1453/1455/1694 are OK — they're the hook). Streamer names NOT in title (zero search volume + dates the video).

Candidates are **exhibit-conditional** — pick after NotebookLM grounding locks the exhibit.

### Exhibit: ZURARA (1453 chronicle) — front-runner pre-NLM

1. *The Atlantic Slave Trade Didn't Start With Trade. It Started With a Raid.*
2. *Africans Sold Their Own? The 1453 Chronicle the Buyer's Own Court Wrote Says Otherwise.*
3. *What Henry the Navigator's Own Chronicler Wrote About the First Atlantic Slave Raids*

### Exhibit: ROMANUS PONTIFEX (1455 papal bull)

4. *The Atlantic Slave Trade Was Licensed in 1455 — By the Pope, In Latin, Before It Began.*
5. *Africans Sold Their Own? Europe Wrote the License to Enslave Them in 1455.*

### Exhibit: PHILLIPS JOURNAL (1694 corporate log)

6. *Africans Sold Their Own? Here's What the British Slave Captain Wrote in His Own Journal.*

### Scoring plan

Run `title_scorer.py` on all 6 once exhibit is locked. Promote top 2 per exhibit for `thumbnail_checker.py` pairing test.

---

## Thumbnail concepts (overnight draft)

All concepts: **primary document on screen + 2-4 word overlay**. No face (0% niche). No streamer faces. Document occupies dominant ~60-70% of frame; overlay top or bottom.

### Concept A — Zurara exhibit (front-runner)

- **Background:** Beazley/Prestage facsimile page (Vol. 1, raid chapter) OR a stylized illustration of a 15th-century chronicle with visible Gothic script
- **Overlay (2-4 words):** *"NO LASSOS?"* / *"THE 1453 CHRONICLE"* / *"HENRY'S CHRONICLER"* — A/B test the three
- **Color:** sepia / manuscript-aged with red accent on the key word
- **Differentiation:** zero competitors use Zurara as a thumbnail document — visual white space

### Concept B — Romanus Pontifex exhibit

- **Background:** Latin manuscript page (papal-bull style with seal) — Davenport scan or stylized facsimile
- **Overlay:** *"1455 / LICENSED"* OR *"PERPETUAL SLAVERY"* (Latin: *PERPETUA SERVITUTE*)
- **Color:** parchment + papal red wax-seal accent
- **Differentiation:** religious-document visual signals legal-licensing argument before video plays

### Concept C — Phillips Journal exhibit

- **Background:** open ship's log / 17th-century corporate ledger with Phillips' handwriting facsimile (cited Donnan Vol. 1)
- **Overlay:** *"BARBAROUS / 1694"* OR *"THE SLAVER'S OWN WORDS"*
- **Color:** sepia ink, red overlay
- **Differentiation:** captain-log visual signals "from inside the apparatus" — buyer's-own-document moat

### Decision plan

1. Lock exhibit after NotebookLM grounding
2. Run `thumbnail_checker.py` on the matching concept variants
3. 2-stage gate (gut → critic if unsure) per `feedback-thumbnail-process.md`

---

## Description (drafted shell)

Will be filled after script lock. Must include:

- Streamer names (Asmongold, Destiny) for tag-spillover algorithm
- Primary-source citations (exhibit archive location, page numbers — pin in top comment)
- Scope note: *Atlantic* slave trade focus; the Arab/Trans-Saharan trade is a separate forthcoming video (responds to comment-mine V2 unmet demand — 7 signals)
- Standard channel CTA
- Link to companion newsletter

---

## Tags (preliminary)

Streamer names live HERE, not in title:

- asmongold
- destiny
- atlantic slave trade
- african slave trade
- history of slavery
- transatlantic slave trade
- portuguese empire *(if Zurara)*
- henry the navigator *(if Zurara)*
- papal bulls *(if Romanus Pontifex)*
- royal african company *(if Phillips)*

---

## Timestamps

TBD post-edit.
