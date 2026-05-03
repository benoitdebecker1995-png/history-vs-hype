# History vs Hype — Strategic Audit

**Date:** 2026-03-29
**Data sources:** analytics.db (48 videos, 43,757 total views), 40+ pattern analyses, 14-channel niche benchmark (650 videos), 85-transcript competitor analysis, 47 NotebookLM notebooks, full catalog metadata review
**Channel state:** 515 subs, 218K views, ~800 views/day, ~21 net subs/month

---

## EXECUTIVE SUMMARY

The channel produces excellent content (30-35% avg retention, proven academic depth, zero-competition primary source format) but has two compounding problems that prevent growth:

1. **Algorithmic scatter** — No coherent identity for YouTube to recommend
2. **Packaging structure** — Strong titles (swaps done), but script structure still chronological when myth-first works better

Title swaps and catalog optimization have been executed. Newsletter launching 2026-03-29. The remaining growth blockers are structural: how the algorithm sees the channel, and how scripts are built.

---

## STATUS: EXECUTION ITEMS (Updated 2026-03-29)

| Plan | Status |
|------|--------|
| Catalog optimization: Tier-1 title swaps | DONE (confirmed via API) |
| Gibraltar → "34,000 People Can't Decide..." | DONE |
| Tordesillas → "Two Countries Split a Continent..." | DONE |
| Berlin Conference → "They Split 229 Ethnic Groups..." | DONE |
| Newsletter launch | LAUNCHING TODAY (2026-03-29) |
| Description CTA additions | Check status |
| Analytics DB refresh | STALE — needs update (last: Mar 16) |

---

## PROBLEM 2: PACKAGING MISMATCH (Fix This Month)

### The Core Contradiction

**Your strength:** Academic depth no competitor can match (page numbers, primary sources, cross-archive verification, clause-by-clause translations)

**Your packaging:** Looks like every other mid-tier history channel (generic titles, chronological structure, delayed payoffs)

### Evidence

| Metric | You | Competitors (outliers) | Gap |
|--------|-----|----------------------|-----|
| Scale words in titles ("every," "all," "entire") | 12% | 36% | -24% |
| Authority framing in titles | 31% | 12% | +19% (overusing) |
| Two-sentence declarative titles | Rare | 11% outlier rate | Not using proven pattern |
| Turn moment placement | 42% of runtime | 15-35% of runtime | 20% too late |
| Years in titles | Present (-46% CTR) | Absent | Free penalty to remove |
| "The X That Y" pattern | Present (1.2% CTR) | Absent | Free penalty to remove |

### The 5 Videos Bleeding Views Right Now

These videos have PROVEN content (retention 35%+) trapped behind broken packaging:

| Video | Retention | Views | CTR | Problem | Ready Replacement |
|-------|-----------|-------|-----|---------|-------------------|
| South China Sea | 49.6% | 91 | 1.83% | Year + "The X That" | "6 Countries Claim the Same Sea. One Map Started It All." |
| NATO Expansion | 45.7% | 47 | 2.47% | Generic | "Putin Lied About a NATO Promise. 1,000 Documents Exposed Him" |
| KGB Palestine | 41.5% | 288 | 5.51% | Good CTR, low impressions | Leave — needs time, not a swap |
| Turkey/Greece | 39.0% | 925 | 3.10% | Working | Leave |
| Stalin | 36.2% | 121 | 1.55% | Generic question | "Stalin Purged His Own Army. Then Hitler Invaded" (DONE) |

**South China Sea is the clearest case:** Best retention on the entire channel. 91 views. New title ready since March 16. Not swapped.

### The Structural Quality Fixes (IMPLEMENTED 2026-03-29 in script-writer-v2 v8.0 + structure-checker-v2)

**Fix 1: Hard 12-min duration cap (Rule 32) — IMPLEMENTED**
- Data: r=-0.455 between duration and retention (n=47). 8-12 min = 29.6% avg, 12-20 min = 24.7% avg.
- script-writer-v2: Rule 32 added. Max 5,400 words. Cut priority order defined. Exception criteria documented.
- structure-checker-v2: Constraint T added. Flags CRITICAL if over 12 min without exception.
- CLAUDE.md: Updated from "as long as needed" to "8-12 minutes hard cap."

**Fix 2: Myth-first structure mandatory for non-territorial videos (Rule 33) — IMPLEMENTED**
- Data: Myth-first = 30.3% avg retention. Chronological colonial = 22.4%. Gap = 8pp.
- script-writer-v2: Rule 33 added. Requires `<!-- STRUCTURE: MYTH-FIRST -->` tag. Chronological only for pure territorial.
- structure-checker-v2: Constraint U added. Flags CRITICAL if non-territorial uses chronological.
- Quality checklist updated with structure tag and turn placement checks.

**Fix 3: Turn placement at 15-25% of runtime (Rule 26 enforced) — IMPLEMENTED**
- Data: Competitor analysis 85 videos — 15-25% = 3.2x views, 25-35% = 2.1x (dead zone), channel avg = 42% (too late).
- structure-checker-v2: Constraint U checks `<!-- TURN MOMENT -->` position. Flags WARNING if >25%.
- Quality checklist: Updated from "within first 3 minutes" to "at 15-25% of runtime."

**Credential chains performed verbally (Shaun technique) — already in Rule 25:**
- Current: You cite page numbers in text overlays
- Fix: Also READ the full credential chain aloud: "[Full name] + [Title] + [Why they're relevant] + [Direct quote]"

**First 5 seconds must deliver on title promise:**
- Current: 29/31 videos have 16.7% avg drop at the 2% mark (first 5-10 seconds)
- Fix: If title says "The Document That..." → show the document in second 1, not second 90
- This is NOT a hook quality problem — it's a thumbnail/title MISMATCH problem

---

## PROBLEM 3: ALGORITHMIC SCATTER (Fix This Quarter)

### The Identity Problem

YouTube's algorithm needs to categorize your channel to recommend it. Right now:

- **Kraut** = deep geopolitical analysis (consistent format, consistent audience)
- **Fall of Civilizations** = civilizational collapse (2-4 hours, consistent format)
- **WonderWhy** = geographic explainers (consistent 12 min, consistent map thumbnails)
- **History vs Hype** = ??? (4 min to 31 min, territorial + ideological + colonial + political + medieval, different audiences every video)

### The Traffic Source Data Confirms This

- 73% of views come from subscribers (healthy = 30-50%)
- Only 14% from Suggested/Related (should be 30-50%)
- Only 3.4% from YouTube Search

YouTube isn't recommending you alongside Kraut/Knowing Better/Shaun because it can't figure out who your audience IS. Your Bakassi viewers (Nigerian) won't click your Manhattan video (American). Each video fragments the audience signal.

### The Rapid-Fire Problem

The current plan tests 6 completely different geographic audiences in 6 weeks:
1. Bakassi (Nigeria)
2. Manhattan (US)
3. Sabah (Philippines)
4. Operation Legacy (Kenya)
5. Hamoodur Rahman (Pakistan)
6. Code Noir (global)

This maximizes topic diversity but MINIMIZES algorithmic coherence. Each new audience segment tells YouTube "this channel's viewers don't watch the next video" — which kills the session continuation signal.

### The Fix: Two Buckets, Not Six

Instead of scattering, pick 2 related content buckets and alternate:

**Bucket A: "Document Autopsy"** (your unique moat)
- Bakassi (1913 treaty)
- Code Noir (1685 law)
- Manhattan (1626 Schagen letter)
- Operation Legacy (destroyed files)
- All share: a physical document examined on camera, clause-by-clause

**Bucket B: "Country vs Country"** (your proven view-getter)
- Sabah (Philippines vs Malaysia)
- Falklands (Argentina vs UK)
- Kashmir follow-up (India vs Pakistan)
- All share: map thumbnail, versus title, territorial stakes

Both buckets serve the SAME viewer type: someone interested in evidence-based geopolitical analysis. A viewer who watches Bakassi (document autopsy of 1913 treaty in a territorial dispute) WILL click Sabah (document autopsy of 1878 treaty in a territorial dispute). YouTube learns: "people who watch one of these watch the next one."

### The Conversion Data Supports This

| Topic Type | Avg Views | Sub Conversion | Best Use |
|-----------|-----------|----------------|----------|
| Territorial | 2,317 | 0.58% | Views/impressions |
| Ideological myth-bust | 179 | 2.88% | Subscriber growth |
| Colonial | 612 | 0.67% | Neither (pause) |
| Political fact-check | 1,132 | 1.41% | Both (best ceiling) |

**The ideal video combines territorial search demand + ideological framing:**
- "Nigeria Lost Oil-Rich Territory. A Court Explains Why." (territorial demand + legal document = Bakassi)
- "France Wrote a Law Making People Property. Here's What It Says." (ideological framing + untranslated document = Code Noir)

---

## THE PRIORITY STACK

### This Week (2 hours total)

- [ ] Swap 5 Tier-1 penalty titles (20 min YouTube Studio) — CATALOG-OPTIMIZATION-PLAN.md has copy-paste replacements
- [ ] Fix 3 critical errors: "Gemini said" description, leading pipe, missing quote (2 min)
- [ ] Add CTA to 22 descriptions (30 min)
- [ ] Rewrite 4 description first-lines (10 min)
- [ ] Run analytics backfill to get current data
- [ ] Publish newsletter issue #1 (Tordesillas article, ready to go)

### This Month

- [ ] Monitor swapped titles at 48h and 1-week marks for CTR changes
- [ ] Publish Bakassi as first rapid-fire test (territorial + document + geographic monopoly)
- [ ] Publish Manhattan as second test (myth-busting + anniversary + American audience)
- [ ] Publish newsletter issues #2-3 (Haiti, Crusades — both ready)
- [ ] Create 3 playlists: "Document Autopsies," "Country vs Country," "Myths Debunked"

### This Quarter

- [ ] Evaluate rapid-fire results: which BUCKET works, not just which topic
- [ ] If Document Autopsy bucket wins → commit to "Untranslated Evidence" as THE series identity
- [ ] If Country vs Country wins → commit to versus-format territorial content
- [ ] Build NotebookLM tools (cross-query, Phase 2 automation) — plan saved in NOTEBOOKLM-TOOLS-PLAN.md
- [ ] Establish weekly "YouTube Studio hygiene" routine (title monitoring, description updates, CTA checks)

---

## WHAT TO STOP DOING

1. **Stop building tools before executing the plans those tools produced.** The catalog optimization, newsletter launch, and analytics refresh are all ready to go. They've been ready for days to weeks.

2. **Stop publishing to 6 different geographic audiences in sequence.** Pick 2 related buckets and alternate. The algorithm needs coherence.

3. **Stop chronological script structure for myth-busting videos.** State the myth first, THEN dismantle it. Move the turn to 15-25% of runtime (currently at 42%).

4. **Stop making pure colonial history without a modern news hook.** Colonial topics average 12.1% retention and 6.36 comments/1K views. Unless attached to an active legal case or political debate, they underperform.

5. **Stop publishing on Friday.** 54 avg views vs 304 on Thursday, 931 on Sunday. Hard embargo.

---

## WHAT TO DOUBLE DOWN ON

1. **Untranslated Evidence format** — zero competition, proven engagement (22% like ratio on Vichy pilot), unique moat
2. **Territorial + document hybrid** — combines the view-getter (territorial) with the converter (ideological/document-first)
3. **Ad-lib filming style** — data shows ad-libs outperform scripted content by +0.102 retention delta. Write looser scripts.
4. **Geographic monopoly targeting** — Belize proved it (29K views from a 400K population). Bakassi (220M English speakers) and Sabah (113M Filipino YouTube users) are the next tests.
5. **The newsletter as a parallel growth channel** — Substack has its own discovery algorithm. Your niche (primary source translation + academic myth-busting) has zero competition on the platform.

---

## THE SUCCESS FORMULA (Data-Backed)

**Belize worked because it had ALL FOUR:**
1. Search demand (people searching "Belize Guatemala dispute")
2. Map thumbnail (88% of geo channels use maps)
3. Territorial dispute (proven view-getter)
4. Active legal case (ICJ advisory — urgency)

**Bakassi has all four:** Nigeria-Cameroon searches + map + ICJ ruling + separatist insurgency.

**Manhattan has three of four:** "Manhattan $24" myth searches + American audience + 400th anniversary. Missing: no active legal case (but anniversary compensates).

**The test:** If Bakassi replicates Belize's pattern (geographic monopoly + territorial + ICJ + zero competition), that's the formula. Scale it: Sabah, Falklands, Kashmir, South Africa.

If it doesn't replicate, the Belize breakout was topic-specific luck, and the channel should pivot harder toward ideological myth-busting (2.88% sub conversion, proven JD Vance 9.46% CTR ceiling).

---

## METRICS TO TRACK

| Metric | Current | Target (3 months) | Target (6 months) |
|--------|---------|-------------------|-------------------|
| Subscribers | 515 | 800 | 1,200+ (YPP eligible) |
| Suggested/Related traffic | 14% | 25% | 35% |
| Subscriber-driven traffic | 73% | 55% | 45% |
| Avg CTR (new videos) | ~2.5% | 4%+ | 5%+ |
| Views/month | ~24K | 40K | 80K |
| Newsletter subscribers | 0 | 200 | 500 |
| Net subs/month | 21 | 50 | 100+ |

---

*This audit supersedes all previous strategy documents. Execute the "This Week" checklist before reading anything else.*
