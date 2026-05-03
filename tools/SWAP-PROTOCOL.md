# 48-Hour Swap Protocol

**Purpose:** Systematic reaction to underperforming videos within the critical first 48 hours.

**Trigger:** Run at 48 hours post-publish for EVERY video. Use `/analyze [video-id]` to get performance data, then apply this protocol.

---

## Important: 48h Velocity Does NOT Predict Lifetime Views

**Source:** VELOCITY-ANALYSIS.md (2026-03-21, n=48 videos)
**Finding:** Pearson r=0.163 — no meaningful correlation between 48h views and lifetime views.
Delayed-push videos average 1,917 lifetime views vs 544 for front-loaded (3.5x).
"The Country That Might Disappear" got only 73 views in 48h but reached 29,011 lifetime (397x).

**Implication:** The 48h swap trigger should focus on **CTR and impressions**, not raw view count. A video with low views but decent CTR (>4%) may simply be waiting for an algorithm push. Only swap when CTR is poor (<2%) WITH sufficient impressions (>500), confirming YouTube tested and viewers rejected the packaging.

## Step 1: Pull 48h Metrics

From YouTube Studio (manual) or `/analyze`:
- **CTR** (click-through rate)
- **Impressions** (how many times YouTube showed the thumbnail)
- **AVD** (average view duration)
- **Views**

## Step 2: Diagnose

| CTR | Impressions | Diagnosis | Action |
|-----|-------------|-----------|--------|
| <2% | >500 | **Bad packaging** — YouTube tested it, viewers rejected it | SWAP TITLE + THUMBNAIL |
| <2% | <500 | **Bad topic or suppressed** — YouTube didn't push it | Check search volume. If low, this was a bad topic choice. |
| 2-4% | >500 | **Mediocre packaging** — performing below potential | SWAP TITLE only (test against backup) |
| 2-4% | <500 | **Early — wait** | Re-check at 7 days |
| >4% | Any | **Good packaging** — hold steady | No swap needed |

## Step 3: Generate Swap Candidates

### Title Swap

1. Run existing title through `title_scorer.py` — identify why it's underperforming
2. Check backup titles in YOUTUBE-METADATA.md — score those too
3. Generate new candidates with `retitle_gen.py` logic:
   - Extract thesis from script opening
   - Slot into versus/declarative patterns
   - Score all candidates
4. Pick the highest-scoring candidate that:
   - Contains the primary search keyword
   - Uses a DIFFERENT pattern than the failing title
   - Scores 65+ on title_scorer.py

### Thumbnail Swap

1. Run current thumbnail concept through `thumbnail_checker.py`
2. If current concept fails any rule → fix the violation
3. If current concept passes → change the STYLE, not the rules:
   - Currently split-map? → Try arrow/flow map
   - Currently document-on-map? → Try pure split-map
   - Always keep text overlay, no talking-head face
   - Map-based for territorial topics; historical/document visual for myth-busting

### Description Swap

4. If the title changes, update first 3 lines of description to match
5. Ensure primary search keyword appears in first sentence

## Step 3b: (PREFERRED) Use YouTube Native A/B Testing

Before manual swapping, use YouTube's built-in Test & Compare:
1. YouTube Studio → Content → Select video → Thumbnail section → "Test & Compare"
2. Upload up to 3 thumbnail+title combinations
3. YouTube splits traffic and measures watch time per variant
4. Let test run — YouTube declares winner automatically

**Why this is better than manual swaps:**
- Statistical significance testing (not raw 48h CTR snapshots)
- Larger sample, no guessing about swap readiness
- Tests run simultaneously, not sequentially

**Use manual 48h swap ONLY if:**
- Test & Compare unavailable (older video)
- Urgent creative failure (CTR < 1% with high impressions)

## Step 4: Execute Swap (Manual Fallback)

1. Change title in YouTube Studio
2. Upload new thumbnail
3. Update YOUTUBE-METADATA.md with swap history:
   ```
   ### SWAP LOG
   - **Original (published DATE):** "Old Title" — CTR X.X%, Y impressions
   - **Swap 1 (DATE):** "New Title" — Reason: [diagnosis]
   ```
4. Update POST-PUBLISH-ANALYSIS.md with swap details
5. Re-check at 48h post-swap

## Step 5: Learn

After 7 days post-swap:
- Compare pre-swap vs post-swap CTR
- If improved: note what changed (pattern type? keyword placement? thumbnail style?)
- If not improved: the problem may be deeper (topic demand, retention, content quality)
- Update `channel-data/patterns/TITLE-PATTERNS.md` with the learning

---

## SWAP SCHEDULE

| Timing | Action |
|--------|--------|
| Publish | Monitor first 2 hours for obvious issues |
| 48 hours | Run full swap protocol (this document) |
| 48h post-swap | Re-check swapped videos |
| 7 days | Final assessment, log learnings |
| 30 days | Bulk retitle review (all videos <100 views) |

---

## NEVER SWAP

- Videos performing >4% CTR (don't fix what's working)
- Videos less than 24h old (insufficient data)
- Videos during a current-events spike (wait for organic to settle)

---

*This protocol replaces "hope and wait." Every video gets a 48h checkpoint.*
