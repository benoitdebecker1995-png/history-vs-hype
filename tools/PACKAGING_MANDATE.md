# PACKAGING MANDATE — Hard Reject Policy

**Effective:** 2026-03-12 | **Updated:** 2026-03-21 (traffic source data confirms mandate)
**Authority:** Channel CTR data (~33 videos) + traffic source analysis (48 videos)
**Enforcement:** `title_scorer.py` auto-rejects violations

> **⚠️ Data Confidence Note (audit 2026-03-12):**
> - Year penalty (-46% CTR) and colon penalty (-28% CTR) are **HIGH confidence** (n=5-9 vs n=26-30)
> - Title pattern CTR averages are **MEDIUM confidence** (n=2-19 per pattern, directional only)
> - Thumbnail data is **LOW confidence** (mixed ~1.7x vs document, n=8 total)
> - All CTR from single collection date. Use for direction, not precision.
>
> **Traffic source confirmation (2026-03-21):**
> - 73% of views come from subscribers. Only 14% from Suggested/Related (healthy = 30-50%).
> - YouTube Search = only 3.4%. Packaging is the #1 growth bottleneck — confirmed by data.
> - See: `channel-data/patterns/TRAFFIC-SOURCE-ANALYSIS.md`

---

## HARD REJECT RULES

Any title matching these patterns is **automatically disqualified**, regardless of script quality or research depth.

### Rule 1: NO YEARS
- **Data:** Years in titles = -45.6% CTR (n=6 vs n=27)
- **Reject:** "The 1494 Line That Split the World"
- **Accept:** "Two Countries Split the World in Half"
- **Exception:** None. Move the year to the description.

### Rule 2: NO COLONS
- **Data:** Colon structure = -28.1% CTR (n=9 vs n=26)
- **Reject:** "Haiti's Debt: 122 Years of French Extraction"
- **Accept:** "Haiti Paid France for 122 Years. Here's Every Receipt."
- **Exception:** None. Use periods, em-dashes, or two sentences.

### Rule 3: NO "THE X THAT Y"
- **Data:** Historically worst pattern (1.2% CTR). All retitled away.
- **Reject:** "The Treaty That Divided the World"
- **Accept:** "Spain vs Portugal. The Treaty That Divided the World" (versus framing supersedes)
- **Exception:** None.

### Rule 4: NO QUESTIONS (Caution)
- **Data:** -36.3% CTR (n=3 vs n=32) — ⚠️ small sample, directional only
- **Reject:** "Did France Really Bankrupt Haiti?"
- **Accept:** "France Bankrupted Haiti. The Documents Prove It."
- **Soft rule:** Questions can pass if they score 65+ on title_scorer.py through other bonuses.

---

## MANDATORY PATTERNS (Use One)

### Tier 1: Versus (~3.7% avg CTR, n=2 verified)
- "[Country/Entity] vs [Country/Entity]: [Stakes]"
- Examples: "Spain vs Portugal", "Turkey vs Greece", "Venezuela vs Guyana"
- Best for: Territorial disputes, bilateral conflicts, competing claims

### Tier 2: Declarative (3.8% avg CTR)
- Two-punch sentences. Statement + evidence promise.
- **Two-sentence formula** has 11% outlier rate (3x+ views) — the strongest proven structural pattern.
- **Scale words** (e.g., "every," "all," "entire," "century") provide 1.33x lift in outlier videos.
- Examples: "Two Countries Split the World in Half. The Line Is Still There."
- Best for: Myth-busting, document reveals, surprising facts

### Tier 3: How/Why (3.3% avg CTR)
- "How [Entity] [Active Verb] [Stakes]"
- Examples: "How France Drained Haiti for 122 Years"
- Best for: Mechanism explainers, causal chains
- **Traffic insight:** How/Why titles get 2x search traffic (26.4% from search vs 12.7% for declarative). Use for evergreen/search-optimized topics.

---

## THUMBNAIL MANDATE

> **Retired 2026-04-26.** Thumbnail rules now live in `tools/benchmark/PER-CHANNEL-THUMBNAIL-PLAYBOOK.md` and `tools/benchmark/OUTLIER-THUMBNAIL-CORPUS.md`. The averaging-based rules previously in this section have been retired — see `tools/benchmark/THUMBNAIL-AUDIT-FINDINGS-2026-04-26.md` for why (text overlay is a floor at 90-96% in BOTH outliers and losers, not a winning predictor; face/map usage is channel-anchored, not niche-wide). Use `/thumbnail` for per-video concept generation grounded in the per-channel playbook + outlier corpus.

---

## TITLE SCORING GATE

**No title may be published unless it scores 65+ on `title_scorer.py`.**

- Run ALL title candidates through the scorer before finalizing
- If no candidate scores 65+, generate new titles — do not lower the bar
- The scorer now applies -50 HARD PENALTY for years, colons, and "The X That Y"
- Any title triggering a hard penalty displays "REJECTED" status

---

## PRE-PUBLISH CHECKLIST

Before publishing any video:

- [ ] Title scores 65+ on title_scorer.py
- [ ] Title contains NO year, NO colon, NO "The X That Y"
- [ ] Title uses versus, declarative, or how/why pattern
- [ ] Thumbnail concepts generated via `/thumbnail` (grounded in per-channel playbook + outlier corpus)
- [ ] Rendered thumbnail passes `thumbnail_image_audit.py` — SERP differentiation not "BLENDS IN" (<0.70 CLIP) against the target query's top results
- [ ] Final-cut audio passes `audio_loudness.py` — integrated in the -16 to -12 LUFS band, true peak <= -1 dBTP
- [ ] Topic has verified search demand (VidIQ keyword volume > 500/month)

---

## ENFORCEMENT TOOLS

| Tool | What it checks | Command |
|------|---------------|---------|
| `title_scorer.py` | Title pattern, hard rejects, score | `python -m tools.title_scorer "Title Here"` |
| `outlier_title_dissector.py` | Outlier pattern analysis (scale words, two_sentence, entity specificity) | `python -m tools.benchmark.outlier_title_dissector --score "Title Here"` |
| `thumbnail_checker.py` | Concept TEXT: text overlay, no talking head, topic-appropriate visual | `python -m tools.preflight.thumbnail_checker --project PATH [--territorial]` |
| `thumbnail_image_audit.py` | Rendered IMAGE: tech compliance, mobile legibility, SERP differentiation (CLIP vs competitors) | `python -m tools.preflight.thumbnail_image_audit THUMB.jpg --serp-ids id1,id2` |
| `audio_loudness.py` | Final-cut audio vs YouTube -14 LUFS (loudness, true-peak, range) | `python -m tools.preflight.audio_loudness FINAL-CUT.mp4` |
| `demand_checker.py` | Search volume, comparable videos | `python -m tools.preflight.demand_checker "topic"` |
| `news_hook_monitor.py` | Google News RSS scan for timely topic hooks | `python -m tools.discovery.news_hook_monitor --scan` |
| `/greenlight` | All three combined — single pre-work gate | `/greenlight "topic"` |
| `/preflight` | Full 5-gate scorecard (topic+script+title+thumb+duration) | `/preflight --project PATH` |

---

## WORKFLOW (Search-Demand-First)

```
/greenlight "topic"          ← FIRST: Is there demand? Can I title it?
    ↓ GO
/research --new "topic"      ← Creates project, demand gate + title pre-gen
    ↓ Research + Script
/preflight --project PATH    ← LAST: 5-gate scorecard before filming
    ↓ READY (70+)
Film → Edit → Publish
    ↓ 48 hours
SWAP-PROTOCOL.md             ← If CTR < 3%, generate swap candidates
```

---

## 48-HOUR SWAP PROTOCOL

See `tools/SWAP-PROTOCOL.md` for the systematic post-publish reaction system.

Key rules:
- CTR < 2% at 48h + >500 impressions → SWAP TITLE + THUMBNAIL
- CTR 2-4% at 48h + >500 impressions → SWAP TITLE only
- CTR > 4% → Hold steady
- Always swap to a DIFFERENT pattern than the failing title

---

## Feedback Loop (Phase 61)

The title scoring system learns from real CTR data. After each publish, the loop closes automatically.

### After Publishing a Video

1. Update `channel-data/patterns/CROSS-VIDEO-SYNTHESIS.md` with the video's CTR from YouTube Studio (48h post-publish snapshot)
2. Run ingestion: `python -m tools.ctr_ingest`
3. Verify: `python -m tools.title_scorer "Test Title" --db` — output should show "DB-enriched"

### How Scores Update

- Pattern scores come from averaging real CTR across all videos using that pattern
- Minimum 3 videos per pattern before DB scores override static constants
- Static fallback scores (from 2026-02-23 audit) remain when DB has insufficient data
- The 65-point minimum threshold is a policy constant, not data-derived

### Convenience Shortcut

Run ingest directly from the title scorer:

```
python -m tools.title_scorer --ingest
```

---

*This mandate overrides all previous title/thumbnail guidance in project files.*
