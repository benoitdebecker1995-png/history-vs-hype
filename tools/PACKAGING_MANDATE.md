# PACKAGING MANDATE — Tiered Rules (VALIDATED / HEDGE / RETIRED)

**Effective:** 2026-06-10 (Fable Phase 1 forensics) | **Supersedes:** 2026-03-21 hard-reject policy
**Authority:** D1 breakout dossier (`channel-data/fable-digests/D1-breakout-dossier.md`, 57 videos, analytics.db through 2026-06-10 + fresh ctr_tracker snapshot) + niche-wide corpus (388 titles, 85 hooks)
**Enforcement:** `title_scorer.py` (graded penalties + warnings — auto-REJECT retired, see spec `channel-data/fable-digests/PHASE-1-SCORER-SPEC.md`)

> **Governing principle (per rules-hedge-not-prescribe):** Only rules backed by n≥19 own-channel data or niche-wide corpora may gate publication. Everything else is a HEDGE — an idea to weigh and A/B test, not a mandate. A strong keyword/data signal justifies testing against any HEDGE rule (single-variable, judged on the right metric).

---

## THE FUNNEL MODEL (what actually determines outcomes)

Per-video forensics across all 57 videos show three distinct failure/success modes, in funnel order:

**Gate 1 — Topicality/demand (does YouTube test you at all?)**
The 2025 stall cohort died here: A-grade titles (China/Taiwan 100, Kashmir 100, Cyprus 90, S.China Sea 90, Armenia 85) earned ≤5.5K lifetime impressions each. Their CTR, where measured, was fine (2.3–4.1%). Construction wasn't the failure — YouTube never surfaced them. All 4 breakouts had a live contemporary hook at publish (active ICJ case, active oil dispute, sitting-VP statement) plus country-name head terms with real search volume.

**Gate 2 — Impression-test CTR (do you convert the test batch?)**
The 2026 cohort fails HERE, not Gate 1. Fresh snapshot: slave-trade 5,188 impressions → 1.91% CTR; Piri Reis 3,097 → 3.81%; Hijab 1,759 → 1.48%. YouTube IS testing recent uploads — they fail the test and distribution stops. **This is where packaging effort pays right now.** Working target: ≥4% on the first test batch.

**Gate 3 — Retention (does the push sustain?)**
Breakouts held 34–39% avg watch; the channel median is 28.1%. Governed by script rules, not this mandate.

**Traffic reinterpretation (HIGH confidence, arithmetic + API taxonomy):** The "73% of views from subscribers" finding (2026-03-21) misread the Analytics API. The SUBSCRIBER bucket includes home-page feed views. B1 Guatemala logged 23,741 "SUBSCRIBER" views on a ~515-sub channel — impossible as subscriber loyalty. The channel's #1 video was a **homepage algorithmic breakout**. Implication: this channel CAN win Browse pushes; they go to topical, country-anchored, high-test-CTR packaging. `channel-data/patterns/TRAFFIC-SOURCE-ANALYSIS.md` conclusions should be re-read through this lens.

**B1 pocket caveat (2026-06-11, user-verified Studio geography):** B1's audience was largely Belize-national — an underserved demand pocket (real audience, zero quality English coverage), not transferable franchise equity. The Sapodilla Cayes sequel (`sXadwOj8VoA`, 2026-03-30) proved it: 47 views, 7 subscriber/browse views, despite 41.5% avg watch. Pocket subscribers are topic-bound. Pockets are RAIDS (see BREAKOUT-HYPOTHESES H3); the channel's positioning stays method-first.

**Identity guard (overrides all packaging tactics):** The channel is "history through primary sources — showing how history is done" (intro video yt:yMAWJcjo_ug). Any packaging optimization that requires regional positioning or stakes-first geopolitics framing is out of bounds, whatever the data says. Topic selection passes identity first, demand second.

> **RESTATED 2026-07-29 (owner interview) — the guard was true but too narrow, and the narrowness caused real drift.**
>
> The subject is **access to the historical record**. Something is properly known by people who work on it, and the public can't get to it; the channel goes and gets it. The mission in the owner's words: *"make the historical discipline more accessible… bring history closer to the people and cut through the ideological bullshit."*
>
> **Four barriers block access**, and all four are in scope:
> | barrier | the viewer's problem | precedent |
> |---|---|---|
> | **enclosure** | it's settled scholarship locked in a £95 university-press book | thinly served so far — the NotebookLM workflow is built for exactly this |
> | **language** | the evidence exists, it just isn't in English | #62 Volhynia · #37 Vichy · Wuchale · Recopilación |
> | **ideology** | the record is buried under a story someone invented | Flat Earth (1828) · Sol Invictus · Dark Ages · Fuentes · Vance |
> | **archive** | the document exists and nobody has looked at it | Vichy draft · Condor cable · Piri Reis |
>
> **Territory, treaties and courts are NOT a lane.** They are topics where several barriers happened to stack. The owner's correction, verbatim: *"i dont want the focus to be solely on law or geopolitics… i do want to show why it is relevant but i want to specialize in history."* Relevance is the closing rhyme; history is the subject.
>
> **Deliberately left open:** which barrier carries breakout demand, and how visible the historian's method should be. The owner declined to pre-commit on both and assigned them to measurement (`tools/discovery/gap_hunter.py` barrier axis, `channel-data/gap-hunter/`). **Do not resolve either by assertion.**
>
> **Ideological targets are symmetric** — nationalist myth, pseudo-history, and current political claims about history all qualify, whoever is making them. No period constraint: *"the topic decides."*

---

## 2026-06-27 — COMPLETE-DATA UPDATE (supersedes the 2026-02-23 snapshot for CTR)

> ⚠ **ARCHIVAL — `surface_ctr` and `thumbnail_features` are frozen datasets, verified 2026-07-30.**
> Neither table has a single reader or writer anywhere in `tools/` — nothing refreshes them and
> nothing queries them. Both stop at videos published **2026-06-04** (56 and 47 rows against 58
> live videos). Treat every figure derived from them below as a **dated observation, not current
> data**, and do not cite them as an authority — see the 2026-07-23 section, which supersedes them.
> To revive either one it needs an importer; until then the vintage stands.

> ⛔ **CORRECTED 2026-08-03 (ADR-0024).** The sentence below previously read that Studio
> impressions+CTR are in `videos.impressions/ctr_percent`. **They are not.** Those columns are the
> **collector's trailing snapshot**, stamped `videos.ctr_as_of`; the Studio LIFETIME export lands in
> **`studio_ctr_rows`**. They differ by ~50× — snapshot median 56 impressions vs lifetime median
> 2,923; the breakout reads 3,915 @ 11.03% snapshot and **292,398 @ 7.66% lifetime**. Reading this
> line as written is what produced three false strategy conclusions on 2026-08-03.
> **Read via `AnalyticsStore.lifetime_ctr_by_video()`** — every row carries `grain`, `as_of` and
> `source_table`. Use `snapshot_ctr_by_video()` only when the recent window is what you actually want.

**Data vintage upgrade:** real per-video Studio impressions+CTR for ALL 56 long-form now in
`analytics.db` (**`studio_ctr_rows`** — *not* `videos.impressions/ctr_percent`), plus per-surface CTR (`surface_ctr` —
Browse/Suggested) and full 56-thumbnail visual tagging (`thumbnail_features`). The "22-video
2026-02-23 snapshot" caveat is retired for CTR. Sources: `channel-data/CTR-TITLE-FORMULA-2026-06.md`,
`CTR-THUMBNAIL-FINDINGS-2026-06.md`, `AB-TEST-AND-TRAFFIC-CTR-2026-06.md`, `FLOP-AUTOPSY-PLAN-2026-06.md`.

**Funnel confirmed + quantified (n=56):**
- views↔impressions r=0.92 · views↔CTR r=0.62 · **views↔retention r=0.07**. Cause of death:
  27/56 NOT-CLICKED (CTR<2.5%), 11 NOT-SERVED, only **3 retention**. Retention is NOT a view lever.
- **FAME is the #1 validated CTR driver: +0.87 blended, +2.23 on Browse** (famous-topic Browse
  CTR 5.65% vs 3.41%). This is Gate-1 demand expressed as a packaging lever.
- **Packaging only pays once the topic is famous** (interaction): within famous topics, a
  document-focal thumbnail costs −2.11% and clutter −1.05%; within obscure topics packaging is
  flat (~0). → Sequence is FIXED — famous topic first (precondition), THEN clean packaging.

**NEW VALIDATED TACTIC — topical CLUSTERS (4–7× on Suggested):** the Guatemala×2 +
Venezuela-Guyana border-dispute cluster pulls 4–7% Suggested CTR; isolated one-offs 0.5–1%.
Ship 2–3 in the SAME dispute family within ~2–4 weeks so they feed each other's Suggested
traffic. Isolated topics get suggested next to unrelated content and die.

**Surfaces:** Browse CTR healthy (7.5% aggregate), Search 6.73%, **Suggested weak (3.07%)**.
The low per-video blended median (2.51%) is an impressions-distribution artifact, not a
thumbnail-quality failure — confirms the Browse-breakout reinterpretation above.

**Thumbnail — validated on all 56 (filters, not predictors):** document-AS-FOCAL-POINT hurts
(−0.71 overall, −2.11 within famous); clutter hurts (−0.52); clean map mild + (proxy for
famous territorial); blank creator face doesn't help (emote or omit). Enforced in
`thumbnail_checker.py` RULE 6 (document-focal = REVIEW flag).
**OVER-FIT KILLS (do NOT prescribe):** "red pop" (−0.67; on 29/47 thumbs, confounded with the
cluttered-document style) and title "visceral predicate" (+0.08) both looked like winners in a
12-extreme pre-analysis and evaporated on the full set.

**Overlay wording (A/B = watch-time-share, individually inconclusive but cross-test):**
"FACT CHECKED" beat its synonyms ("Myths Busted"/"Reality Check"/"The Real Evidence") in 2
independent tests; an existential question ("DOES BELIZE EXIST?") beat flat framings. Default
verdict-overlay direction; confirm via forward A/B (A/B power itself is gated on fame→impressions).

---

## 2026-07-23 — FORWARD-VIDEO FINDINGS (July-23 Studio LIFETIME import, verified)

**Data authority:** the July-23 Studio lifetime export (57 videos, `studio_ctr_imports`/`studio_ctr_rows`, schema v5) is now the freshest CTR truth. ⚠ **`surface_ctr` is a Feb-2026 legacy export and is missing #59 — directional only; do NOT cite it as current.** Every result below was reproduced by the main thread against the live DB; queries in `tools/youtube_analytics/_research/CODEX-FUTURE-VIDEOS-2026-07-23.md`. All Guatemala-sensitive results computed with `Y21EjQ0v9W4` excluded.

**These are FORWARD (at-creation) rules for the NEXT video, not patches for old ones. Tagged so nothing reads as law that isn't.**

- **[CONFIRMED, null, n=56] Nothing measurable post-publish predicts distribution.** Impressions vs: CTR ρ=+0.18, retention ρ≈0, like-rate **−0.26**, age ≈0. You cannot earn a push with retention/engagement tuning. **The only at-creation distribution levers are TOPIC and PACKAGING.** This confirms the Gate-1/funnel model above with the current data.
- **[CONFIRMED, null, n=56] No topic FORMULA in the data.** Topic-type vs impressions Kruskal–Wallis **p=0.18** (not significant). Territorial runs a higher median (3,330 vs 2,240) — a weak directional hint, NOT a law. Fame/recognizability/live-relevance are not stored, so the data can't test the stronger idea. **→ V1 demand gate is the rule; territorial is one presentation, not the formula.** Do not build a "make territorial disputes" doctrine.
- **[CONFIRMED, n=55] Structure: the 5–10% post-hook seam is where holds are won or lost.** r20 top vs bottom retention quartile 48.7% vs 27.8%; the beat right after the cold open loses a mean **12.7 pp** vs 4.7 pp for the next band. **→ at SCRIPT stage: no welcome, methodology preamble, recap, or roadmap in the first 5–10%; go straight into substance.** This is a HOLD/watch-time lever (Gate 3), not a distribution lever — see `WRITING-VOICE-AND-STYLE` and the opener docs for where it's actioned.
- **[HYPOTHESIS, n=8] Evidence-promise titles run higher CTR.** Median 3.28% vs 2.41% (mean 3.92% vs 3.04%). Supports V3's evidence-promise punch. Small cohort, JD-Vance-influenced — a default-to-test, not a gate.
- **[CONFIRMED concentration] Search demand is entity-led.** 47% of non-Guatemala search views come from 5 exact named terms; some titles omit the searched entity (`operation sig`, `treaty of tripoli`). **→ reinforces V2: name the exact searched person/treaty/operation/case in the title, or the first description line at upload.**
- **[HYPOTHESIS, n=46] Thumbnail: document-as-focal-object negative** (2.39% vs 3.11%), busy weak-negative, **red is not a lever** (2.48% vs 3.16%). Confirms the "OVER-FIT KILLS" note above from the fresh data. One clear focal object, few elements.
- **[CONFIRMED, null, n=47] Length is not a lever in 5–13 min** (duration↔body-retention r=−0.12). Let the argument decide runtime.

---

## TIER 1 — VALIDATED (publication gates)

### V1: Topic demand gate
- VidIQ search volume >500/mo **or** a verifiable live news hook (active dispute, ruling, public claim by a notable figure).
- Evidence: every breakout had one; the impression-starved 2025 cohort had neither. Binding constraint at Gate 1.
- Enforced by `/greenlight` + `demand_checker.py`. Hard stop, no exceptions.

### V2: Search-anchored head term (keyword-ladder GATE)
- A country/region/entity head term with real search volume must **begin** within the first 40 characters of the title (it may run past that edge — the breakout "The Country That Might Disappear: Guatemala vs Belize" anchors at char 34). **Enforced as a `/greenlight` Step-4 PASS/FAIL gate** (2026-06-15), not just the `title_scorer` `SEARCH_ANCHOR_BONUS (+12)`: anchor a famous parent keyword, deliver the obscure entity as the *reveal*. Recognizer: `title_scorer.has_search_anchor`.
- **A FAIL means one of two things — decide which before touching the title** (ADR-0023). Either the title genuinely leads with something obscure (rewrite it), or the lead term is famous and its demand has never been measured (record it). The recogniser accepts a term on a curated list *or* on a verified search volume ≥1,000/mo in `keywords.db`; the second is what keeps it from going stale. Repair the second case with one command — the FAIL message prints it:<br>`python -m tools.title_scorer --record-anchor "<term>" --volume <n/mo> --anchor-source vidiq-YYYY-MM-DD`<br>Never trade a title down for a vaguer one to clear a gap in the list: that is what #67 did before the mechanism was fixed (five candidates regenerated away from "Constantine", 113,206/mo). Inspect any title's verdict with `python -m tools.title_scorer --anchor "<title>"`.
- Evidence: all 4 breakouts front-load country names ("Guatemala vs Belize", "Venezuela vs Guyana", "Turkey Claims 152 Greek Islands", "JD Vance"). The stall cohort is dominated by document/myth-first titles with zero-volume head terms ("The Lenape…", "Treaty of Tripoli:…", "38 Dead Over 4.6 Square Kilometers"). Confirms feedback-starting-channel-search-anchored (515 subs = every title needs a keyword anchor).
- Channel-DNA note: the document-forensic identity stays **in the video** (doc on screen). The title front-loads the searched subject; the primary-source reveal is the second punch ("…The Documents Disagree"). NOT stakes-first geopolitics framing — that's the RealLifeLore lane (anti-voice).

### V3: Declarative two-punch as default pattern
- Statement + evidence promise, two sentences. n=19 own-channel (largest sample, 3.8% avg CTR) + niche-wide two-sentence outlier rate 5.3x (n=9 outliers).
- Scale words ("every," "all," "entire," "century") = 1.33x outlier lift (niche-wide n=138).

### V4: Title scoring gate — 65+ on `title_scorer.py`
- Retained as a floor. The scorer no longer auto-REJECTs on style rules (see RETIRED); it grades construction + anchors + demand. If no candidate scores 65+, generate new titles — don't lower the bar.

### V5: Test-batch CTR reaction (48h swap protocol)
- CTR <2% at 48h on >500 impressions → swap title + thumbnail; 2–4% → swap title; >4% → hold. Always swap to a different pattern. See `tools/SWAP-PROTOCOL.md`. This is the Gate 2 recovery mechanism and stays mandatory.

---

## TIER 2 — HEDGE (ideas, A/B-testable, never auto-reject)

Each entry lists the n-size and the contradicting evidence. Per feedback-data-overrides-rules-for-testing, any of these may be deliberately tested against.

| Rule | Original claim | n | Contradicting evidence | Current stance |
|---|---|---|---|---|
| No colons | -28% CTR | 9 vs 26 | The #1 (29.7K views), #2 (5.4K, fresh 12.1% CTR) and #3 (2.0K, 4.31% CTR) videos ALL have colons. Measurement confounded: colon titles clustered on low-demand topics. | Mild style preference (-10 in scorer). "X vs Y: Stakes" colon = no penalty. A/B candidate (see BREAKOUT-HYPOTHESES H5). |
| No years | -46% CTR | 6 vs 27 | "Invented in 1828" year-as-hook scored 3.7% CTR. n too small for HARD. | Year-as-topic-label discouraged (-15); year-as-hook ok (-10→0 case-by-case). A/B-testable on search impressions. |
| No "The X That Y" | 1.2% CTR historically | 0 current | "The CIA Document That Proved Operation Condor": fresh 4.91% CTR, above channel median. | Discouraged (-15), warn not reject. |
| No questions | -36% CTR | 3 vs 32 | Single-digit sample. | Soft penalty, passes at 65+. |
| Versus > all patterns | ~3.7% CTR best | 2 verified | Breakout advantage is plausibly the TOPIC (bilateral conflict), not the syntax. | Preferred for territorial disputes; not mandated elsewhere. |
| How/Why = search pattern | 2x search traffic share | 5 | "How the KGB Weaponized…" = highest fresh CTR on channel (18.4%) — supports it; "How 3 Coups…" = worst retention — against. | Use for evergreen/search topics; pair with strong head term. |

---

## TIER 3 — RETIRED

- **The hard-reject policy itself** (auto-disqualification on colon/year/The-X-That-Y). The scorer REJECTED the channel's #1 and #3 videos. A style rule that rejects your best performers is measuring the wrong gate. Penalties stay (the CTR cost where real is honest); the auto-REJECT and "DO NOT PUBLISH" verdicts are retired.
- **"No exceptions" language** on any n<10 channel-derived rule (violates rules-hedge-not-prescribe).
- **-46% / -28% as causal claims.** They are confounded correlations from a single 2026-02-23 snapshot. Cite as "observed in early catalog, confounded with topic demand."
- **"73% subscriber loyalty" interpretation** of traffic mix (see Funnel Model — it was largely Browse).
- 26x map multiplier (already removed in v4; actual ~1.7x).

---

## THUMBNAIL MANDATE

> **Retired 2026-04-26.** Thumbnail rules live in `tools/benchmark/PER-CHANNEL-THUMBNAIL-PLAYBOOK.md` and `tools/benchmark/OUTLIER-THUMBNAIL-CORPUS.md` (text overlay is a floor, not a predictor; face/map usage channel-anchored). Use `/thumbnail` for per-video concepts.
> **Gate-2 addendum (2026-06-10, corrected 2026-06-14 per ADR 0007):** the thumbnail carries at least half the test-batch CTR burden — but no pre-publish number predicts the click. Rendered thumbnail must pass `thumbnail_image_audit.py`'s **feed-size legibility + tech gate** (a mushy/illegible thumbnail is the one image-computable click-killer). CLIP **differentiation is informational only** (differentiation ≠ clickability). The real Gate-2 verdict is native A/B / reach-window CTR, never a pre-publish score.

---

## PRE-PUBLISH CHECKLIST

- [ ] Topic passes V1 demand gate (>500/mo VidIQ **or** verified live news hook)
- [ ] Title front-loads a search-anchored head term (V2)
- [ ] Title scores 65+ on title_scorer.py (V4) — style warnings reviewed, not auto-fatal
- [ ] Pattern chosen deliberately (declarative default; versus for bilateral disputes; how/why for evergreen search)
- [ ] Thumbnail concepts via `/thumbnail`; rendered image passes `thumbnail_image_audit.py` **feed-size legibility + tech** (differentiation is informational only — ADR 0007)
- [ ] Final-cut audio: -16 to -12 LUFS, true peak ≤ -1 dBTP (`audio_loudness.py`)
- [ ] 48h swap protocol armed (V5): know your swap candidates BEFORE publish

---

## ENFORCEMENT TOOLS

| Tool | What it checks | Command |
|------|---------------|---------|
| `title_scorer.py` | Title construction, anchors, graded penalties | `python -m tools.title_scorer "Title Here"` |
| `outlier_title_dissector.py` | Outlier pattern analysis (scale words, two_sentence, specificity) | `python -m tools.benchmark.outlier_title_dissector --score "Title Here"` |
| `thumbnail_checker.py` | Concept TEXT checks | `python -m tools.preflight.thumbnail_checker --project PATH [--territorial]` |
| `thumbnail_image_audit.py` | Rendered IMAGE filter: tech compliance + **feed-size legibility** (hard); CLIP differentiation informational only | `python -m tools.preflight.thumbnail_image_audit THUMB.jpg` |
| `audio_loudness.py` | Final-cut loudness | `python -m tools.preflight.audio_loudness FINAL-CUT.mp4` |
| `demand_checker.py` | Search volume, comparables | `python -m tools.preflight.demand_checker "topic"` |
| `news_hook_monitor.py` | Live news hooks (now a V1 input, not just discovery) | `python -m tools.discovery.news_hook_monitor --scan` |
| `/greenlight` | Combined pre-work gate | `/greenlight "topic"` |
| `/preflight` | Full scorecard before filming | `/preflight --project PATH` |

---

## WORKFLOW (Demand-First, unchanged shape)

```
/greenlight "topic"          ← V1: demand or news hook? Can I title it with a head term?
    ↓ GO
/research --new "topic"      ← Creates project, demand gate + title pre-gen
    ↓ Research + Script
/preflight --project PATH    ← Scorecard before filming
    ↓ READY (70+)
Film → Edit → Publish
    ↓ 48 hours
SWAP-PROTOCOL.md             ← V5: react to the impression test
```

---

## Feedback Loop (Phase 61) — unchanged

1. Update `channel-data/patterns/CROSS-VIDEO-SYNTHESIS.md` with 48h CTR
2. `python -m tools.ctr_ingest`
3. Verify: `python -m tools.title_scorer "Test Title" --db`

Pattern scores from real CTR averages; min 3 videos per pattern before DB overrides static constants; 65-point threshold is policy, not data.

---

## Active experiments

Ranked, falsifiable packaging hypotheses for the next 5 uploads: `channel-data/BREAKOUT-HYPOTHESES.md`. Back-catalog retitle queue: `channel-data/RETITLE-SHORTLIST.md` (feeds `/retitle`).

*This mandate overrides all previous title guidance. Data vintage: **CTR = complete per-video
Studio export, all 56 videos, 2026-06-27** (in `analytics.db` videos.impressions/ctr_percent +
surface_ctr + thumbnail_features) — see the 2026-06-27 COMPLETE-DATA UPDATE section above. Older
vintages (2026-02-23 22-video snapshot; 2026-06-10 ctr_tracker reach-window) are superseded for CTR.*
