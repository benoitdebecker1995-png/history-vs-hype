# PACKAGING MANDATE — Hard Reject Policy

**Effective:** 2026-03-12
**Authority:** Channel CTR data (~33 videos measured, single snapshot)
**Enforcement:** `title_scorer.py` auto-rejects violations

> **⚠️ Data Confidence Note (audit 2026-03-12):**
> - Year penalty (-46% CTR) and colon penalty (-28% CTR) are **HIGH confidence** (n=5-9 vs n=26-30)
> - Title pattern CTR averages are **MEDIUM confidence** (n=2-19 per pattern, directional only)
> - Thumbnail data is **LOW confidence** (mixed ~1.7x vs document, n=8 total)
> - All CTR from single collection date. Use for direction, not precision.

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
- Examples: "Two Countries Split the World in Half. The Line Is Still There."
- Best for: Myth-busting, document reveals, surprising facts

### Tier 3: How/Why (3.3% avg CTR)
- "How [Entity] [Active Verb] [Stakes]"
- Examples: "How France Drained Haiti for 122 Years"
- Best for: Mechanism explainers, causal chains

---

## THUMBNAIL MANDATE

### Map-First Policy
- **Data:** Map/mixed thumbnails avg ~1.7x more views than document-only (n=4 vs n=4 — LOW confidence)
- **Data:** No text overlay (3.3% CTR) > text overlay (2.0% CTR) — ⚠️ small sample
- **Data:** No face (3.3% CTR) > face (1.9% CTR) — ⚠️ small sample
- **Rationale:** Even with low sample confidence, map thumbnails communicate "this is about a place/conflict" instantly, which matches the channel's territorial dispute niche

### Required Elements
1. **Geographic element** — Map, border, territory, or satellite view
2. **Color contrast** — Two distinct colors showing opposing sides/claims
3. **Clean composition** — No text overlay, no face, no busy backgrounds

### Forbidden Elements
- Face/person thumbnails (unless the video IS about a specific person)
- Text overlays (title does the work, not the thumbnail)
- Document-only thumbnails (pair with map context)
- Stock photography or generic historical images

### Blueprint Template
For every video, create 3 thumbnail concepts:
- **A:** Split-map showing the territorial/conceptual divide
- **B:** Animated border/line overlay on geographic context
- **C:** Document fragment placed ON TOP of geographic context

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
- [ ] Thumbnail scores 80+ on thumbnail_checker.py
- [ ] Thumbnail is map-based with color contrast
- [ ] Thumbnail has NO text overlay, NO face
- [ ] Topic has verified search demand (VidIQ keyword volume > 500/month)

---

## ENFORCEMENT TOOLS

| Tool | What it checks | Command |
|------|---------------|---------|
| `title_scorer.py` | Title pattern, hard rejects, score | `python -m tools.title_scorer "Title Here"` |
| `thumbnail_checker.py` | Map-first, no face, no text, contrast | `python -m tools.preflight.thumbnail_checker --project PATH` |
| `demand_checker.py` | Search volume, comparable videos | `python -m tools.preflight.demand_checker "topic"` |
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
