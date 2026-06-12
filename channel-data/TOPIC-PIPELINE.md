# Topic Pipeline — Ranked Through Rubric v2

**Generated:** 2026-06-11 (Fable Phase 4) · **Updated same day:** VidIQ chat batch ingested (18/22 keywords scored; the 30% demand dimension is now REAL data for all Tier A/B clusters)
**Method:** `tools/TOPIC-RUBRIC.md` v2 — gates (identity, V1 demand) → 30% VidIQ Overall / 20% topicality / 25% whitespace / 10% title CTR / 10% rankability / 5% source access + POCKET flag
**Data vintage:** VidIQ Overall + volumes 2026-06-11 (source `vidiq-chat-2026-06-11` in keywords.db) · D4 whitespace map 2026-06-10 · SERP studies 2026-06-03/06-10 · publish list through #57

> **Whitespace dimension: SCANNED 2026-06-11** — five Tier A SERP title studies in `channel-data/serp-studies/titles/*-2026-06-11.md`. Cross-shelf constant: **two-sentence "Claim. Evidence." = 0% and evidence-promise ≈0% on ALL five shelves** — the channel's brand formula is open whitespace everywhere. **Remaining gap before any lock:** hook web-verification (topicality scores marked VERIFY).
>
> **Index-conflict flags (don't treat as truth either way):** `ethiopia never colonized` 3,600→0, `treaty of wuchale` 1,200→0, `panama canal treaty` 1,900→0 between the 2026-03 manual pulls and the 2026-06-11 chat batch — likely exact-match/index differences. Cluster demand rides on the anchors regardless.

---

## In the pipeline already (rubric N/A — editorial commitments)

- **#59 I/P partition pilot** — IN PRODUCTION. "Claims on Trial" series locked; British Mandate cluster (2,200 + 1,800 + 1,200/mo) backs the series lane. H1-tag: HOOK.
- **#58 Kurdistan** — READY TO FILM. kurdistan history 65 Overall / comp 16.4; kurdistan map 64 / 21.6; treaty of sevres 58.2 / 36.
- **1-sykes-picot-2025** — READY TO FILM but **flagged for a decision**: user judged the lane saturated during #58 (beat cut from that script for this reason). Re-run `/greenlight` whitespace before filming.

## TIER A — greenlight next (ranked; VidIQ dimension now confirmed)

### 1. Panama Canal — the treaty no Panamanian signed ⭐ ✅ GREENLIT 2026-06-11 (full composite GO; H4 title arms pre-registered in BREAKOUT-HYPOTHESES; next: pull `_BACKLOG/36-panama-canal-deconcini-2026` → `_IN_PRODUCTION` via `/research`)
- **Demand (30%):** anchor `panama canal history` **63 Overall / 8,995/mo** — highest-scoring keyword in the entire db after Kurdistan. Beneath it, two ultra-low-competition document terms: `hay bunau varilla treaty` (36 Overall, **comp 10.3**) and `torrijos carter treaty` (36, **comp 9.3**).
- **Structure note:** VidIQ's "ladder" pitch = exactly our V2 two-punch — title front-loads the searched anchor ("Panama Canal…"), the document term is the evidence promise ("…the treaty no Panamanian signed"). Sub-11 competition on the doc terms means the channel can OWN those queries outright.
- **Topicality: 100 — ✅ WEB-VERIFIED 2026-06-11.** Active legal-geopolitical drama, multi-sourced and current: Panama Supreme Court ruled the CK Hutchison ports concession unconstitutional (early Feb 2026, FDD/Al Jazeera); Panama voided the contracts and handed interim control to Maersk/MSC (2026-02-23/24, Bloomberg + CNBC); CK Hutchison's PPC filed an ICC lawsuit ≥$2B (Feb-Mar 2026, HKFP); deal block + Beijing retaliation still running as of **2026-05-31** (Newsroom Panama). Drawn-out multi-jurisdiction fight predicted — the hook has months of runway. Modern-relevance beat writes itself: a 2026 court voiding a canal-ports contract on sovereignty grounds ↔ the 1903 treaty no Panamanian signed and the 1977 DeConcini intervention reservation.
- **Whitespace: 50 (scanned).** Shelf = engineering-build megaprojects (HISTORY, TED-Ed, Geographics; "built/engineering" saturate) + news takes. Closest legal touch is a 3-min History Matters animation (1.97M). Treaty-forensic angle (who signed 1903, DeConcini text) unserved; evidence-promise 0%, two-sentence 0%.
- **Banked:** `_BACKLOG/36-panama-canal-deconcini-2026`. Identity: clean. POCKET: NO.

### 2. Treaty of Brest-Litovsk — Russia signed away Ukraine once (PROMOTED from Tier B)
- **Demand:** **63 Overall / 5,008/mo** — tied for top score; 3.3x the volume the stale db showed.
- **Topicality: 0 — ✅ checked 2026-06-11.** No formal contemporary invocation found in Russia-Ukraine negotiation coverage; only cautionary-parallel commentary. Scores as evergreen (volume 5,008 > 1K clears H1's evergreen bar). March 3 anniversary = annual timing lever.
- **Whitespace: 50 (scanned), with a WEAK shelf:** top video only 657K, most under 200K — 5,008/mo of demand served by WWI-week narrative content (The Great War ×3, HistoryPod date-videos). Years saturate 50% → yearless two-sentence title doubly differentiates. Sovereignty-document angle unserved. No banked folder.

### 3. Unequal Treaties China — sovereignty erosion on paper (NEW ENTRANT)
- **Demand:** **61 Overall / 4,554/mo**. D4 whitespace candidate (Treaty of Nanking, Boxer Protocol — legal mechanisms of concession).
- **Topicality:** evergreen 0 unless tied to a live Taiwan/HK beat (VERIFY case-by-case).
- **Whitespace: ~75-100 (scanned) — best of the batch.** The shelf COLLAPSES after position 2: 1.04M and 566K (both Opium War *narratives*, not treaty content), then #3 is 2,285 views and the rest is sub-2.3K classroom material. A 4,554/mo query with effectively zero quality direct coverage — demand currently funnels into adjacent Opium War videos. The treaty-text angle isn't just unserved, the topic is.
- No banked folder. Caveat: channel's China/Taiwan + South China Sea videos (2025 evergreen cohort) died at Gate 1 with no hook — adjacent lane, same H1 risk; volume (4.5K > 1K) is the compensating factor.

### 4. Ethiopia — the treaty that said two different things (Wuchale Art. 17)
- **Demand:** anchor shifts to `battle of adwa` **61 Overall / 4,268/mo** (`ethiopia never colonized` and `treaty of wuchale` returned 0 in the new index — conflict flagged above; Adwa carries the cluster).
- **Topicality:** evergreen; Adwa anniversary March 1 = timing lever for a Feb/Mar publish.
- **Whitespace: 50 (scanned) — but the MOST crowded shelf of the five.** "Why wasn't Ethiopia Colonized?" is directly served at scale (History Matters 2M, Knowledgia 1.85M, PassportHeavy 782K, Nas Daily 309K, Extra History series). The Wuchale Article 17 two-texts forensic is unserved, but differentiation must be total — the `/translate` side-by-side format IS the video, not a beat in it.
- **Banked:** `_BACKLOG/39-adwa-wuchale-2026`. Source access mid (T2 via scholars). POCKET: NO.

### 5. Suez 1956 — the protocol they denied existed (PROMOTED: demand confirmed)
- **Demand:** **59 Overall / 3,381/mo** (3.4x the stale figure — clears V1 comfortably, not marginal after all).
- **Topicality:** **70th anniversary Oct–Nov 2026** = dated lever, scores 50 within the window → strongest publish slot is autumn.
- **Whitespace: 50 (scanned), heavy shelf:** Epic History 4.7M all-parts, History Matters 1.9M, Kings & Generals 1M, BBC doc. Sèvres Protocol document angle unserved (evidence-promise 8% = one "Here's Why" title). Years saturate 58% → yearless two-sentence differentiates. `protocol of sevres`: 0 volume — pure second-punch term.

## TIER B — viable, weaker profile

- **Monroe Doctrine — text vs invocation:** 51 Overall, comp ~48-54 → rankability 0-50. Decent volume (1,245×3) and the doc-forensic angle is open (D4: interventions-catalogs over-served), but the score says crowded. Pairs as thematic follow-on to Panama/Greenland.
- **Greenland — legal paper trail (DEMOTED from Tier A):** raw volume is big (8,100 + 2,900) but **50 Overall with comp 51-54 → rankability 0**, the shelf is flooded, and it carries the highest anti-voice risk (RealLifeLore lane). `kauffmann agreement greenland`: no VidIQ index. Only viable doc-first with a verified hook; otherwise park.
- **Falklands/Malvinas:** `falklands malvinas dispute` returned NO DATA in the new index (old db: 1,400/mo — conflict). Needs broader anchor terms re-scored before it can claim a slot. Backlog folder banked.

## TIER C — gated down (unchanged 2026-06-11)

- **Crimea** (4,400 + 1,528/mo): shelf saturated since 2022; only resurfaces if a SERP scan shows the doc angle (1954 transfer decree, Budapest Memorandum) genuinely open.
- **Library of Alexandria** (1,017×6, comp 30): ancient-era lane over-served (D4).
- **Antarctic Treaty 2048** (800): below band without a hook.
- **Iron curtain / French Revolution terror:** no doc-forensic spine identified; framing over-served.

## H3 POCKET-RAID slot — Sabah/Sulu now HOOK-PATH ONLY

VidIQ: `sabah dispute`, `sulu sultanate claim`, `north borneo dispute` all **0 search volume** → the V1 volume path is dead. The pocket thesis (B1 profile: English-speaking national audience + zero quality coverage + active legal drama) survives only via a **verified live hook** — an active beat in the Sulu-award annulment saga or a Manila/KL flare-up. Park `_BACKLOG/46-sabah-dispute-2026` until `news_hook_monitor` or a manual check verifies one; don't spend research before that.

## VidIQ shopping list — ✅ COLLECTED 2026-06-11

18/22 scored, in keywords.db. No-data (need broader anchors if ever revisited): `anglo-irish treaty border`, `geneva accords vietnam`, `kauffmann agreement greenland`, `falklands malvinas dispute`. Zero-volume doc terms recorded as second-punch vocabulary, not anchors: terra nullius, protocol of sevres, hay bunau varilla, torrijos carter, wuchale.

## Already published — demand pools belong to /retitle, not new videos

Berlin Conference (11,648/mo on an underperforming published video), Tordesillas (2,703), Western Sahara cluster (~11,800 across 7 variants — published as the landmine-wall video, title never named it), Gibraltar/Utrecht (~2,400), Kashmir/partition, Chagos, Operation Condor, Vichy, crusades, vikings, dark ages → `channel-data/RETITLE-SHORTLIST.md` is the vehicle.

---

## Next actions (in order)

1. ~~SERP title scans~~ ✅ DONE 2026-06-11 — five studies in `serp-studies/titles/`.
2. ~~Hook verification~~ ✅ DONE 2026-06-11 — Panama VERIFIED-LIVE (topicality 100, runway into H2 2026); Brest-Litovsk no invocation (topicality 0).
3. **`/greenlight --full "panama canal"`** — all rubric dimensions now real, and Panama wins the board: demand 63/8,995 + topicality 100 verified + whitespace 50 + doc-term competition 9.3/10.3 + banked `_BACKLOG/36-panama-canal-deconcini-2026`. This is also the natural **H1-tag: HOOK** upload for the BREAKOUT-HYPOTHESES pre-registration log. Runner-up stays Unequal Treaties (best whitespace ~75-100, evergreen).

*Refresh trigger: after each upload's 28-day window, or when a Tier A hook verifies — whichever first.*
