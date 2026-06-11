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

---

## TIER 1 — VALIDATED (publication gates)

### V1: Topic demand gate
- VidIQ search volume >500/mo **or** a verifiable live news hook (active dispute, ruling, public claim by a notable figure).
- Evidence: every breakout had one; the impression-starved 2025 cohort had neither. Binding constraint at Gate 1.
- Enforced by `/greenlight` + `demand_checker.py`. Hard stop, no exceptions.

### V2: Search-anchored head term
- A country/region/entity head term with real search volume must appear in the first ~40 characters of the title.
- Evidence: all 4 breakouts front-load country names ("Guatemala vs Belize", "Venezuela vs Guyana", "Turkey Claims 152 Greek Islands", "JD Vance"). The stall cohort is dominated by document/myth-first titles with zero-volume head terms ("The Lenape…", "Treaty of Tripoli:…", "38 Dead Over 4.6 Square Kilometers"). Confirms feedback-starting-channel-search-anchored (515 subs = every title needs a keyword anchor).
- Channel-DNA note: the document-forensic identity stays **in the video** (doc on screen). The TITLE leads with country stakes; the document is the payoff, not the marquee.

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
> **Gate-2 addendum (2026-06-10):** the thumbnail carries at least half the test-batch CTR burden. Rendered thumbnail must pass `thumbnail_image_audit.py` SERP differentiation (<0.70 CLIP vs target query top results) — this is now the thumbnail's Gate-2 check.

---

## PRE-PUBLISH CHECKLIST

- [ ] Topic passes V1 demand gate (>500/mo VidIQ **or** verified live news hook)
- [ ] Title front-loads a search-anchored head term (V2)
- [ ] Title scores 65+ on title_scorer.py (V4) — style warnings reviewed, not auto-fatal
- [ ] Pattern chosen deliberately (declarative default; versus for bilateral disputes; how/why for evergreen search)
- [ ] Thumbnail concepts via `/thumbnail`; rendered image passes `thumbnail_image_audit.py` differentiation
- [ ] Final-cut audio: -16 to -12 LUFS, true peak ≤ -1 dBTP (`audio_loudness.py`)
- [ ] 48h swap protocol armed (V5): know your swap candidates BEFORE publish

---

## ENFORCEMENT TOOLS

| Tool | What it checks | Command |
|------|---------------|---------|
| `title_scorer.py` | Title construction, anchors, graded penalties | `python -m tools.title_scorer "Title Here"` |
| `outlier_title_dissector.py` | Outlier pattern analysis (scale words, two_sentence, specificity) | `python -m tools.benchmark.outlier_title_dissector --score "Title Here"` |
| `thumbnail_checker.py` | Concept TEXT checks | `python -m tools.preflight.thumbnail_checker --project PATH [--territorial]` |
| `thumbnail_image_audit.py` | Rendered IMAGE: compliance, legibility, SERP differentiation | `python -m tools.preflight.thumbnail_image_audit THUMB.jpg --serp-ids id1,id2` |
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

*This mandate overrides all previous title guidance. Data vintage: lifetime CTR = 2026-02-23 POST-PUBLISH snapshot (22 videos); fresh CTR = 2026-06-10 ctr_tracker reach-window (compare within snapshot only).*
