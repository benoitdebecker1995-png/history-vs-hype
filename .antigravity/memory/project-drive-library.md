---
name: Google Drive source library plan
description: 3-layer plan to consolidate, rename, and Drive-mirror the ~2000 academic PDFs scattered across the project
type: project
originSessionId: 6bc1f95b-8b40-4cfb-ac86-08d5fdaab657
---
Consolidate all academic PDFs into a single Drive-mirrored library. **Layer 2 quality audit COMPLETE (2026-05-15).** Library: 997 active files across 7 topic folders + 91 off-topic stash + 132 duplicate stash. Naming convention: `Title-Author-Year-Publisher.ext`, retrieval-tested both human-scannable and grep-friendly. Publisher slugs canonicalized (OxfordUP, CambridgeUP, PrincetonUP, etc — no more 3-4 variants per house). 14 mid-word title truncations restored (Kinzer "Terror", Lambert "World", Doumani "Jabal Nablus", Akcam "Genocide", etc).

**Why:** Re-downloading sources already owned, can't check "do I have X" without opening files, NLM upload friction every video.

**Layer 1 — Consolidate ✅ DONE (2026-05-10):**
- Moved 201 PDFs/EPUBs from video-projects to topic folders (keyword-based classification)
- Moved 183 academic files from Downloads root (libgen/z-lib/anna's archive pattern)
- 11 Downloads dups skipped (already in library from project moves)
- 453 Downloads root files remain — non-channel (fiction, work docs, random)
- 1 dup remains in video-projects/37-vichy (identical copy already in general-history)
- Formats covered: .pdf, .epub, .mobi, .azw3

**Layer 2 quality audit ✅ DONE (2026-05-15):**
- Three-pass audit run after the residual cleanup, addressing pre-existing naming inconsistencies in the older bulk-pipeline files.
- **Pass 1 — Dedup**: 120 dupe clusters identified by (author, year, title-word-overlap≥3), with format-aware grouping so `.pdf` + `.epub` of same book are kept separately. 132 files moved to `_stash-duplicates/`. Heuristic winner picker ranks by: canonical publisher > non-Unknown year > no -v2/-v3 suffix > specific topic folder over general-history > longer title > file size. Catches like `AbolitionHistorySlaveryAntislavery-Drescher` (full title kept, three other Drescher variants stashed), `OurTimeIsNowRaceModernityPostcolonialGuatemal-Gibbings` (Cambridge canonical kept over Palgrave + verbose-slug variants), and cross-folder duplicates (e.g. Stannard *American Holocaust* was in 3 folders).
- **Pass 2 — Publisher slug normalization**: 267 distinct raw slugs collapsed via canonical-overrides map. 203 files renamed. Examples: `Cambridge` / `Cambridge-UP` / `Cambridge-University-Press` / `CambridgeUniversityPress` → `CambridgeUP` (98 files unified); `Oxford` / `Oxford-UP` / `Princeton-University-Press` / `PalgraveMacmillan` / `VersoBooks` / `BasicBooks` → canonical short forms. Piracy slugs (ZLib, AnnaArchive, Libgen) retained as-is so they signal provenance.
- **Pass 3 — Mid-word truncation fixes**: 14 real cuts repaired via manual map. Examples: `AllShahsMenAmericanCoupRootsMiddleEastTe` → `...Terror-Kinzer-2013-Wiley`; `BarbaryWarsAmericanIndependenceAtlanticW` → `...AtlanticWorld-Lambert-2007-ZLib`; `RediscoveringPalestineMerchantsPeasantsJ` → `...JabalNablus17001900-Doumani-1995-UCalifUP` (also corrected year from 1700 → 1995, period-vs-pubyear misparse); `YoungTurksCrimeAgainstHumanityArmenianGe-Akcam-1815` → `...Genocide-Akcam-2012` (year + truncation both fixed); `ModernIran10129879780300194739LibgenLi-Kagan` → `ModernIran-Kagan-2018-YaleUP` (stripped libgen ID hash). False positives intentionally preserved: `MedievalPhilosophyVol2` (legitimate volume marker), `VikingWarriorWomenReassessingBirkaGraveBj581` (Bj.581 is the famous Birka grave reference).
- One missed dupe caught manually after retrieval test: corrupted-name `15501750JonathanIrvineIsraelOxfordNewYor-mercantilism-1550-OxfordUP` was the same Jonathan Israel "European Jewry in the Age of Mercantilism" book as the clean-named `EuropeanJewryMercantilism-Israel-1989-OxfordUP`. Dedup logic clusters by author field, and the corrupted file's author parsed as "mercantilism" — so it didn't group. **LESSON for future audits: also run a title-word-only dedup pass that ignores the author field, to catch files where the parse pipeline put the author in the wrong slot.**
- **Retrieval test post-audit**: 5/5 scenarios pass cleanly. "1953 Iran coup" → 3 hits (Kinzer/Rahnema/Gasiorowski) all readable. "Drescher abolition" → 2 hits (down from 4 dupes). "Bakassi" → 8 distinct sources. "Spanish Inquisition" → 7 distinct sources incl. fixed Zafra 1667 primary doc.
- All artifacts in `_gemini-output/layer2-rename/`: audit-01-inventory.py → library-inventory.json (1,129 records, 0 unparseable); audit-02-analysis.py → audit-publisher-slug-map.json, audit-dupe-clusters.json, audit-truncation-candidates.json; audit-03-consolidate.py → audit-execution-plan.json/.tsv; audit-04-truncation-fixes.py → audit-truncation-fixes-map.json (manual 16-entry map); audit-05-execute.py → audit-execute-report.txt (full audit trail).

**Layer 2 cleanup pass ✅ DONE (2026-05-14):**
- Hit residual 177 Unknown/Unknown/0000 files after prior Layer 2 closure. Pipeline: PyMuPDF page 1-2 extract (192 targets after broader regex) → Gemini Flash classification (148 text-extractable, 44 image-only+errored) → manual page-1 PNG read for 14 needs_ocr cases.
- Results: 78 rename + 28 move+rename + 5 move + 15 noop + 66 stash. Zero errors.
- Big recoveries: `Unknown-Unknown-2022` was Einsatzgruppen Operational Sit Rep USSR #17 (July 1941 primary Holocaust doc); `UnidentifiableDocument-Unknown-0000` was Barton's *The Hebrew Bible: A Critical Companion* (Princeton); `MiscellaneousWorksRemains-Hall` was actually Rebecca Earle *The Body of the Conquistador* (CUP); `UnknownDocument-2007-Oxford` was Kenny *Medieval Philosophy* Vol 2 OUP; `WorldHistory-Unknown-2010` was Smil *Energy in World History* (Westview 1994); `Unknown-Unknown-0000-Unknown` in african-history was the 1892 *Bulletin officiel de l'État indépendant du Congo* from Gallica/BnF.
- Cross-folder reroutes: 18 misfiled general-history files moved to territorial-disputes (Western Sahara, Belize-Guatemala, Thai-Cambodian, Guyana-Venezuela ICJ); 11 to colonialism-slavery (Body of Conquistador, Mission to Civilize, Black Legend, Recopilación Leyes Indias); 9 to african-history (Sahel coup/intervention papers); plus moves to reference-methodology + middle-east-history.
- Stash sweep removed: user's personal docs (BenoitDeBecker, EuropassCV, TESOL cert, bol.com invoice, Belgian energy/bank/transaction docs), D&D content (Grim Hollow, Drakkenheim, Rappan Athuk, Wildemount masquerading as "IntermediateText-Fearenside"), EU youth/ESC program docs, Ghent University admin paperwork, Appen transcription style guide, and 4 channel working drafts that had crept into colonialism-slavery as "sources".
- One override caught pre-execution: `HolsteinPapers-Holstein-AnnaArchive` was flagged stash by Gemini due to PyMuPDF returning scanner noise, but page 2 showed "Westminster Public Libraries" stamp — kept as `HolsteinPapers-Rich-1955-CUP.pdf`. LESSON: scanned books fool text-extraction-only classifiers; always cross-check low-conf stash decisions.
- Library after pass: **1,129 active + 91 stash = 1,220**. Residuals: 177 → 53 (33 in general-history, mostly missing year/publisher only, recoverable via future title+author web-lookup batch). 70% reduction.
- All artifacts in `_gemini-output/layer2-rename/`: residual-extracts-v3.json, classify-results.json (148), imgonly-results.json (44), ocr-results-manual.json (14), rename-plan-v3.json/.tsv (192), execute-report-v3.txt.
- Model routing confirmed: Gemini Flash for bulk PDF content reading + classification (148 in one call). Multimodal OCR fell back to Claude Code Read tool on rendered PNGs after `gemini @file.pdf` hung — `google-genai` SDK not installed locally; could be added for future multimodal-at-scale jobs. **Opus not used**, per [Model Selection]: Opus is for script polish, not bulk metadata.

**Layer 2 — Rename ✅ DONE (2026-05-12):**
- Canonical format: `ShortTitle-Author-Year-Publisher.ext` (title-first per user preference)
- 1,220 files canonical across all 7 folders. 100% coverage.
- Lookup pipeline: Gemini Flash (filename parse) → Gemini Flash / Haiku (year+publisher lookup for unknowns) → PyMuPDF regex fallback
- ICJ documents preserved with doc-number suffix (e.g., `CameroonNigeriaJudgment-0104-ICJ-2002-ICJ.pdf`)
- territorial-disputes (final batch, 2026-05-12): 115 → 101 files. Overnight RemoteTrigger fired but produced no output — completed manually in same-day session.
- Cross-folder outlier sweep (2026-05-12 followup): 55 stragglers parsed via Haiku subagent (Gemini Flash 429'd), 51 renamed, 4 dedup-deleted, 0 errors.
- 4 off-topic files moved to `library/_stash-offtopic/` (2x Belgian regional gov + 2x D&D guides ~54MB).
- Residual after all cleanup passes (incl. round 1+2 Gemini web-lookup): 21 title=Unknown, 130 author=Unknown, 120 year=0000, 481 publisher=Unknown. Acceptable.
- Web-lookup round 1 (user pasted Gemini answers): 52 entries resolved, all renamed cleanly.
- Web-lookup round 2 (harder cases with full filename context): 137 Gemini responses → 67 renamed + 2 dedup + 4 disambig + 26 flagged off-topic (all stashed) + 29 truly unresolved.
- Stash folder `library/_stash-offtopic/` now has 25 files for user manual review.
- User round-trip (2026-05-12): user pulled 15 files from stash to `library/real/` with hand-corrected names + Gemini metadata.txt → 14 PDFs canonicalized and routed to topic folders (general-history 9, middle-east 2, territorial 2, african 1). `library/real/` retains metadata.txt for reference.
- Library final: **1,195 files** across 7 topic folders.
- **PDF metadata pass (2026-05-12)** — should have been step 1, not step N. Ran PyMuPDF `doc.metadata` on all 1,148 readable PDFs. v1 had false positives: "oup" matched inside "Group" (iText producer), "Microsoft Print to PDF" auto-fills Author = user's Windows username "Benoit De Becker". v2 fixed with word-boundary regex + user-name blocklist + year cap ≤2016 (PDF creationDate often = scan date not pub date). 55 upgrades applied (9 pub + 30 year + 4 title + 12 author). 11 author candidates rejected as junk (system handles like "Dufp001-lap", "Unicafpc", "Zmfr"; org words like "Games", "Service", "States"; initials like "Lr"). LESSON: PDF metadata first ALWAYS — free, fast, often resolves what filename parsing can't.
- Content-ID pass (2026-05-12): PyMuPDF first-2-pages → Gemini Flash. 57 text-extractable scanned. 40 renamed with content-derived names (26 high-conf, 16 medium-conf). 3 academic low-conf renames applied. 10 off-topic surfaced via content extraction + stashed.
- Publisher-lookup pass (2026-05-12): Haiku batched 348 author+year-known entries → 230 publishers resolved (66% hit rate). All 230 renames applied cleanly.
- Year-lookup pass (2026-05-12): Haiku batched 270 author-known year-unknown entries → 173 years resolved (64% hit rate). All applied.
- 33 image-only PDFs detected (scanned books, no OCR) — listed in `image-only-pdfs.json`. Would need OCR pipeline for full ID.
- **WEB-LOOKUP-PROMPT.md** built for user — 244 files needing web-search resolution (paste into ChatGPT/Perplexity). Covers all `author=Unknown` and `title=Unknown` entries.
- All scripts + reports in: `D:\History vs Hype\_gemini-output\layer2-rename\`

**Layer 3 — Drive mirror + NLM integration (one session):**
- Google Drive MCP is already configured (auth needed — see project-claudebase-overhaul.md)
- Upload renamed library to Drive mirroring `by-topic/` structure
- Wire `source_sync_drive` into `/research` Phase 2 so it checks Drive before asking user to find file

**How to apply:** Each layer is independently useful. Start with Layer 1 when user says "organize sources" or "library cleanup". Layer 3 requires Drive MCP auth first.

**Existing structure to preserve:**
```
library/by-topic/
  african-history/
  colonialism-slavery/
  crusades-christianity/
  general-history/
  middle-east-history/
  reference-methodology/
  territorial-disputes/
```
