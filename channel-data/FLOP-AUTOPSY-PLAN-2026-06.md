# Flop Autopsy + Iteration Plan — Working SOP (2026-06-27)

**Goal:** answer "why did each long-form video flop" mechanically, then decide what
History vs Hype should BE (the "MiniMinuteMan-for-history" hypothesis), then ship a
tested iteration plan. Run like an analytics team: each phase has fixed inputs → outputs.

**Creator intent (constraint, not negotiable):** NOT "become a geopolitics channel."
Target identity = passionate, rigorous history myth-buster (MiniMinuteMan energy, history
not archaeology). The autopsy is identity-agnostic; the lane decision (Phase 3) respects
this constraint.

---

## PHASE 0 — Data ingestion  [BLOCKED ON CREATOR]
- **Input:** `channel-data/imports/studio-reach-export.csv` (Studio Advanced-mode export:
  impressions, impressions CTR, views, AVD, AVP per video) + 6-video velocity figures.
- **Action:** write a header-tolerant ingester (EN/FR), join on video_id, fill
  `videos.impressions` + `videos.ctr_percent` (currently NULL for all 57).
- **Output:** complete funnel per video in `analytics.db`. Gate: ≥50/57 rows matched.

## PHASE 1 — Funnel decomposition (per-video autopsy)
- **Input:** completed `analytics.db`.
- **Action:** for each video compute the chain `Impressions → CTR → Views → AVP/AVD`, then
  CALIBRATE thresholds from the data itself (channel median impressions, median CTR, the
  winner as benchmark — no hardcoded numbers). Tag each video with its PRIMARY failure:
  - **NOT SERVED** — impressions far below channel median → algorithm never distributed it
    (topic has no suggested-parent / no demand). Fix = topic/lane, not packaging.
  - **NOT CLICKED** — impressions OK, CTR below median → packaging (title/thumb).
  - **NOT HELD** — CTR OK, AVP low or steep early drop → hook/script.
  - **DEMAND-CAPPED** — served + clicked + held, but absolute ceiling low → topic too small.
- **Output:** a 57-row table, every video tagged with its failure stage. THIS is the
  "why did it flop" deliverable. Saved to `channel-data/FLOP-AUTOPSY-TABLE.md`.

## PHASE 2 — Pattern extraction + "luck" test
- **Input:** Phase 1 table.
- **Action:**
  - Which failure stage dominates? (Is the channel mostly NOT-SERVED, or NOT-CLICKED?)
  - Does failure stage cluster by lane — geopolitics vs pseudohistory-debunk vs ideology?
  - **Guatemala luck test:** decompose its win — abnormal impressions (algo push = topic
    had a parent, replicable) vs abnormal CTR (packaging) vs abnormal retention (luck).
- **Output:** the dominant bottleneck, named, with evidence; verdict on the luck question.

## PHASE 3 — Identity / demand validation (the MiniMinuteMan-for-history question)
- **Input:** Phase 2 verdict + creator intent.
- **Action:** I supply demand-research prompts (competitor outlier videos in
  history-debunk / pseudohistory / "grifter takedown" lanes; browse/suggested adjacency;
  search demand). Cross with how the creator's OWN videos in that lane scored in Phase 1.
- **Output:** is the history-debunk lane SERVED + WANTED? Which sub-lane is both unique and
  in-demand? Go/no-go on the identity, with evidence.

## PHASE 4 — Iteration plan (the experiments)
- **Input:** Phases 2–3.
- **Action:** spec the next 5 videos — each a single-variable experiment designed to fix
  the dominant failure stage, inside the chosen identity. Define the metric that judges
  each (native A/B for CTR; impressions for served; AVP for held).
- **Output:** `channel-data/ITERATION-PLAN.md` — 5 specced videos + how each is measured.

---

## Status
- [x] Phase 0 — ingested real Studio CSV (impressions+CTR, 56/57) into analytics.db
- [x] Phase 1 — autopsy table → `channel-data/FLOP-AUTOPSY-TABLE.md`
- [x] Phase 2 — bottleneck + luck verdict (below)
- [ ] Phase 3 — identity/demand go-no-go
- [ ] Phase 4 — iteration plan

---

## FINDINGS (Phases 1–2, 2026-06-27, REAL impressions/CTR)

**Funnel math (56 videos, 576,035 impressions, 46,871 views):**
- views ↔ impressions **r=0.92**; views ↔ CTR **r=0.62**; views ↔ retention **r=0.07**.
- CTR earns impressions (r=0.29); retention does NOT (r=0.05). CTR & retention independent (r=0.11).
- Median video: **2,876 impressions, 2.51% CTR, 28% AVP.** Healthy CTR band is 4–6%, so the
  channel is click-starved.

**Cause of death (56 videos):**
| count | diagnosis | meaning |
|---:|---|---|
| **27** | NOT CLICKED (CTR<2.5%) | dies at thumbnail/title — the dominant failure |
| 11 | NOT SERVED (impr<3k) | topic too obscure, never tested broadly (small pool) |
| 10 | CAPPED | got served + clicked but topic ceiling low |
| 5 | WON (≥900 views) | — |
| **3** | NOT HELD (AVP<24%) | retention almost NEVER kills a video here |

**Verdict — the bottleneck is the CLICK, then the POOL. Retention is a red herring.**
~48% of videos die unclicked; only ~5% die on retention. Packaging (CTR) is now VERIFIED as
the #1 lever, not assumed. Topic choice sets the size of the impression pool; CTR decides
whether you scale inside it.

**"Guatemala = luck?" — NO, mostly repeatable.** It won on **7.62% CTR** (3× channel median)
× a **huge territorial impression pool** (50% of all channel impressions). Proof it's a recipe
not a fluke: the follow-up Guatemala-2 also hit **9.11% CTR / 42,871 impressions**. Two-for-two
in one cluster. The lucky part is only the *magnitude*; the recipe (high-CTR packaging on a
big-pool topic, shipped as a cluster) is repeatable.

**MiniMinuteMan/pseudo-debunk lane (n=14) — viable but mis-executed.** Median CTR 2.42% (the
channel's weakest lane as run). BUT the lane's CTR splits hard on TARGET FAME:
- Famous targets click: JD Vance "child sacrifice" **9.37%**, Crusades **5.48%**, Hancock/Piri
  Reis 3.97%, Flat Earth 3.67%.
- Obscure targets die: Sol Invictus 2.47%, Lagertha 2.36%, Inquisition 1.51%, Medieval literacy
  1.12%, $24 Manhattan **0.48%**.
- → The lane works ONLY with recognizable myths/grifters (which is exactly MiniMinuteMan's
  model — he takes on famous targets: Hancock, Joe Rogan, ancient-aliens). Your flops in this
  lane were obscure = small pool + no name recognition = no click.

**Lane medians are similar (CTR 2.4–2.7%, views 83–133); territorial's total-view lead is
almost entirely Guatemala.** So "go territorial" is NOT the lesson — the lesson is FAME +
CTR-craft within whatever lane, and territorial just happens to have the biggest pools.
