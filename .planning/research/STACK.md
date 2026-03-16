# Technology Stack: v7.0 Packaging & Hooks Overhaul

**Project:** History vs Hype — Packaging & Hooks Overhaul
**Researched:** 2026-03-16
**Milestone:** v7.0 — Better hook generation, title scoring against external benchmarks, metadata optimization

---

## What Already Exists (DO NOT Re-add or Re-research)

| Capability | Location | Status |
|-----------|----------|--------|
| Python 3.11+ | tools/ (~48K LOC) | Working |
| SQLite databases | keywords.db (v29), intel.db (v2), analytics.db | Working |
| YouTube Analytics API v2 | tools/youtube_analytics/ | Working |
| YouTube Data API v3 | tools/intel/competitor_tracker.py | Working |
| OAuth2 auth | tools/youtube_analytics/auth.py | Working |
| title_scorer.py | tools/title_scorer.py | Working — rules-based, own data only |
| Competitor RSS + enrichment | tools/intel/competitor_tracker.py | Working — 15 videos/channel |
| Competitor title classification | tools/intel/competitor_patterns.py | Working |
| Topic vocabulary | tools/intel/topic_vocabulary.py | Working |
| Transcript fetching (1 video) | .claude/tools/get-transcript.py | Working — youtube-transcript-api v1.0+ |
| Transcript analysis (83 files) | tools/youtube_analytics/transcript_analyzer.py | Working |
| feedparser (RSS) | tools/intel/algo_scraper.py | Working |
| requests | tools/intel/algo_scraper.py | Working |
| pyppeteer + stealth | tools/discovery/autocomplete.py | Working |
| scrapetube | tools/discovery/ | Installed |
| trendspyg | tools/discovery/trends.py | Working |
| textstat | pyproject.toml [nlp] | Installed — readability scores |
| spacy >=3.8 | pyproject.toml [nlp] | Installed — NOTE: Python 3.14 incompatible, use 3.11-3.13 |
| imagehash | pyproject.toml [thumbnails] | Installed — perceptual hashing |
| anthropic SDK | notebooklm_bridge.py | Working |
| Playwright MCP | MCP server | Active |
| Context7 MCP | MCP server | Active |

**Key constraint — spaCy on Python 3.14:** Known tech debt. Stay on Python 3.11-3.13 for now.

---

## New Capabilities Needed

### 1. Bulk Competitor Transcript Harvesting

**Problem:** The existing competitor system collects title + view count from RSS (15 videos/channel, no transcript text). Hook research requires the actual opening 60 seconds of top-performing videos. We need transcripts for 20-50 competitor videos, not just metadata.

**What to add:** `youtube-transcript-api` is already installed (used in `get-transcript.py`). It is NOT yet wired into the competitor pipeline. No new library needed — just a new module that calls the existing API for a batch of competitor video IDs.

**Recommended approach:** New `tools/intel/competitor_transcripts.py` using the already-installed `youtube-transcript-api`. Fetch only the first 90 seconds of transcript per video (truncate by timestamp) to minimize storage. Store in intel.db.

**Quota cost:** Zero — youtube-transcript-api uses no YouTube Data API quota. It scrapes the transcript endpoint directly.

**Why not yt-dlp:** yt-dlp.exe is already available at `tools/yt-dlp.exe` for subtitle download, but youtube-transcript-api is cleaner for programmatic batch use and is already integrated. Reserve yt-dlp for edge cases (non-English channels).

**Confidence:** HIGH — youtube-transcript-api v1.0+ fetch() method is confirmed working in get-transcript.py line 126.

---

### 2. YouTube Data API — Unused Capabilities for Title Research

**Problem:** The title_scorer.py scores titles against own-channel CTR data only (33 videos, single snapshot). It has no external benchmark.

**YouTube Data API v3 capabilities already authenticated but NOT used for title research:**

| Endpoint | Quota Cost | What It Gives | v7.0 Use |
|----------|-----------|--------------|----------|
| `videos.list` (own videos) | 1 unit/call, 50 IDs/call | Full snippet including actual published title, description, tags, thumbnailUrl | Compare published titles to CTR — already available in analytics.db but not cross-referenced |
| `search.list` | 100 units/call | Videos matching query | **DO NOT USE** — quota cost is prohibitive (established decision, see competitor_tracker.py line 8) |
| `channels.list` | 1 unit | brandingSettings.channel.keywords | Competitor channel keywords/niche tags |
| `videos.list` (competitor IDs) | 1 unit/call, 50 IDs | tags, categoryId, defaultAudioLanguage | Competitor metadata patterns |

**Recommendation:** No new YouTube API integration needed. Use `videos.list` for competitor videos already in intel.db — we have their IDs from the RSS pipeline. A new query module can batch-fetch tags and descriptions for the ~1,000 competitor videos we already have stored.

**What this unlocks:** Competitor tag patterns → identify which tags top-performing edu/history videos use → inform metadata optimization.

**Confidence:** HIGH — google-api-python-client is installed, auth is working, videos.list is already used in competitor_tracker.py line 8.

---

### 3. Title Benchmark Data — External Patterns

**Problem:** title_scorer.py uses only internal CTR data (33 videos, single collection date). It cannot benchmark against what performs in the broader edu/history niche.

**Approach — no new API needed:**

The competitor_patterns.py system already classifies ~1,000 competitor titles by formula (question, how_why, colon_split, quote, list). But it does not correlate formula → outlier view count for the history/edu niche specifically.

**What to add:** New query function in `tools/intel/competitor_patterns.py` (or new `title_benchmark.py`) that:
1. Reads competitor_videos from intel.db (already populated)
2. Filters to edu/history channels (already classified by topic_cluster)
3. Groups by title formula × topic cluster
4. Outputs median views and outlier rate per formula

This is pure SQL + stdlib math — zero new dependencies.

**Result feeds title_scorer.py:** When scoring a title, it can compare "declarative history = 3.8% own CTR" against "declarative history competitors = N median views". The two signals together give a more reliable score.

**Confidence:** HIGH — intel.db competitor_videos table exists (confirmed in competitor_patterns.py), outlier detection already in pattern_analyzer.py.

---

### 4. Hook Pattern Corpus — Structured Storage

**Problem:** Hook generation currently relies on OPENING-HOOK-TEMPLATES.md (6 templates, 1 Rule 19 formula) written by hand. It has no empirical basis from competitor analysis.

**What to add:** New SQLite table in intel.db to store extracted hook patterns from competitor transcripts.

```sql
-- intel.db migration (v2 → v3)
CREATE TABLE competitor_hooks (
    id          INTEGER PRIMARY KEY,
    video_id    TEXT NOT NULL,
    channel_id  TEXT NOT NULL,
    title       TEXT,
    view_count  INTEGER,
    hook_text   TEXT NOT NULL,      -- First 90 seconds of transcript
    hook_type   TEXT,               -- cold_fact, myth_contrast, document_reveal, question, stat_shock
    beat_1      TEXT,               -- Cold Fact text (0-10s)
    beat_2      TEXT,               -- Myth/Setup text (10-20s)
    beat_3      TEXT,               -- Contradiction/Evidence (20-40s)
    beat_4      TEXT,               -- Payoff preview (40-60s)
    parsed_at   TEXT DEFAULT (datetime('now'))
);
```

**Parsing strategy:** Claude API (already available via Claude Code native LLM) classifies the 4-beat structure from raw transcript text. No NLP library needed — the classification is semantic, not statistical, and Claude handles it better than regex or spaCy.

**New module:** `tools/intel/hook_analyzer.py` — fetch transcripts, send first 90s to Claude for 4-beat parsing, store in competitor_hooks table.

**Confidence:** HIGH — Pattern is already established in algo_synthesizer.py which uses Claude for synthesis of scraped text.

---

### 5. Thumbnail Hash Comparison — External Benchmark

**Problem:** thumbnail_checker.py (referenced in PACKAGING_MANDATE.md) exists but the imagehash library is only installed, not wired to competitor data. Thumbnail data confidence is LOW (n=8 total per PACKAGING_MANDATE.md).

**What to add:** Use imagehash (already installed via `[thumbnails]` extra) to compare own thumbnail hashes against competitor high-performers. Download competitor thumbnails via the maxresdefault URL pattern (no API quota):
```
https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg
```

**Recommended approach:** New `tools/intel/thumbnail_analyzer.py` that:
1. Downloads thumbnails for top competitor videos (outliers already flagged in intel.db)
2. Computes perceptual hashes with imagehash
3. Clusters similar thumbnails (map-based vs face-based vs document-based)
4. Reports which cluster correlates with outlier view counts

**New dependency required:** `Pillow>=10.0.0` — imagehash depends on it for image loading. It is NOT currently in pyproject.toml. Must add to `[thumbnails]` extras.

```toml
thumbnails = [
    "imagehash>=4.3.0",
    "Pillow>=10.0.0",   # ADD: required by imagehash for image loading
]
```

**Confidence:** MEDIUM — imagehash + PIL integration is straightforward and well-documented. The YouTube thumbnail URL pattern is public and stable (confirmed in YouTube oEmbed responses). Pillow version compatibility with Python 3.11-3.13 is HIGH confidence.

---

### 6. Readability Scoring for Titles and Hooks (textstat)

**textstat is already installed** (pyproject.toml `[nlp]` extra). It is NOT currently used in title_scorer.py or hook generation.

**What to add:** Wire textstat into title_scorer.py for two new signals:
- `textstat.flesch_reading_ease(title)` — titles scoring <60 (hard to read) get a small penalty
- `textstat.syllable_count(title)` — titles over 20 syllables tend to be truncated awkwardly

**No new dependency.** Just a new import in title_scorer.py and two additional scoring signals.

**Why textstat over rolling our own:** It handles edge cases (contractions, hyphens, abbreviations) correctly and is already installed. Confidence: HIGH.

---

### 7. Metadata Tag Analysis — stdlib Only

**Problem:** The `/publish` metadata command generates tags, but there is no benchmark for which tags the top-performing edu/history videos actually use.

**What to add:** New query function in existing tools that reads competitor tags from youtube API enrichment (videos.list already fetches tags into intel.db's enrichment fields) and produces a ranked tag frequency table per topic cluster.

**New dependencies:** None. This is SQL aggregation on existing data.

**Integration point:** `tools/intel/metadata_optimizer.py` (new) reads intel.db, outputs top-N tags per topic cluster as a reference table. The `/publish` command then reads this table when generating metadata.

---

## Libraries NOT to Add

| Temptation | Why Not |
|-----------|---------|
| BeautifulSoup / lxml | Already decided against in algo_scraper.py — LLM synthesis handles messy HTML better. Existing regex approach works. |
| NLTK | Overkill. textstat covers readability. Claude API covers semantic classification. spaCy already installed if NLP needed. |
| sentence-transformers / embeddings | No similarity search needed. Patterns are explicit rules, not vector clusters. Would require PyTorch (heavy). |
| Selenium / Playwright Python | Playwright MCP is already available and active. The Python Playwright package would duplicate it. |
| SerpAPI / BrightData | Paid APIs. No budget allocated. Existing autocomplete scraper + RSS pipeline covers search data needs. |
| VidIQ API | Confirmed no public API exists (PROJECT.md, Out of Scope). |
| Pandas | Overkill for this dataset size (< 10K rows). stdlib statistics module + sqlite3 is sufficient. |
| aiohttp / httpx | requests is already installed and sufficient for synchronous batch fetching of thumbnails and transcripts. |
| pytrends | Archived/unreliable. trendspyg is already the replacement and installed. |
| OpenAI / Gemini APIs | Anthropic SDK (Claude) is already the LLM of record. No reason to add competing provider. |
| youtube-dl | Superseded by yt-dlp.exe which is already in tools/. |

---

## pyproject.toml Changes

**Only one new dependency:**

```toml
# [thumbnails] extra — ADD Pillow
thumbnails = [
    "imagehash>=4.3.0",
    "Pillow>=10.0.0",    # ADD: imagehash requires PIL for image loading
]
```

**All other v7.0 features use existing dependencies or stdlib.**

---

## New Modules Summary

| Module | Dependencies | Purpose | Where |
|--------|-------------|---------|-------|
| `tools/intel/competitor_transcripts.py` | youtube-transcript-api (existing) | Batch-fetch first 90s of competitor video transcripts | intel.db → competitor_hooks table |
| `tools/intel/hook_analyzer.py` | Claude Code native LLM (existing) | Parse 4-beat structure from transcript text | competitor_hooks table population |
| `tools/intel/title_benchmark.py` | sqlite3 stdlib (existing) | Compute formula × view-count correlations from intel.db | Feeds title_scorer.py |
| `tools/intel/thumbnail_analyzer.py` | imagehash + Pillow (Pillow is new) | Cluster competitor thumbnails, correlate with outlier views | intel.db |
| `tools/intel/metadata_optimizer.py` | sqlite3 stdlib (existing) | Extract top tags per topic cluster from competitor data | Feeds /publish |

**DB migrations required:**
- intel.db: v2 → v3 (add `competitor_hooks` table)
- keywords.db: No changes anticipated (v29 sufficient)

---

## YouTube Data API — Unused Endpoints Worth Using

**Currently unused, worth adding for v7.0:**

| Endpoint | Module to Add It To | What It Adds |
|----------|---------------------|-------------|
| `videos.list` with `part=snippet,tags` for competitor IDs | `competitor_tracker.py` enrichment pass | Competitor tags array → metadata_optimizer.py |
| `videos.list` own channel with `part=snippet,statistics` | `title_intelligence.py` | Cross-reference published title → actual CTR from analytics.db |

**Currently used and sufficient:**
- `videos.list` with `part=contentDetails,statistics` — view counts, duration (competitor_tracker.py)
- YouTube Analytics API v2 reports — CTR, retention, impressions (ctr.py, ctr_tracker.py)
- YouTube RSS feeds — last 15 videos per channel (competitor_tracker.py, algo_scraper.py)

**DO NOT add:** `search.list` — 100 quota units per call, established hard rule in codebase.

---

## Integration Points for Existing Systems

| Existing System | v7.0 Addition | How They Connect |
|----------------|--------------|-----------------|
| `title_scorer.py` | title_benchmark.py | `score_title()` gains optional `benchmark_db` parameter; queries intel.db for niche-level formula performance |
| `tools/intel/competitor_patterns.py` | competitor_transcripts.py + hook_analyzer.py | `get_pattern_report()` gains hook pattern section |
| `/publish` command | metadata_optimizer.py | Metadata generation references top-N tags table per topic cluster |
| `OPENING-HOOK-TEMPLATES.md` | hook_analyzer.py output | New Part 10 in STYLE-GUIDE.md with empirically-derived hook patterns from competitor analysis |
| `script-writer-v2` agent | Updated STYLE-GUIDE.md Part 10 | Rule 19 supplemented with competitor hook evidence |

---

## Confidence Assessment

| Area | Confidence | Basis |
|------|------------|-------|
| youtube-transcript-api for batch use | HIGH | Already working in get-transcript.py, v1.0+ API confirmed |
| videos.list for competitor tags | HIGH | Same client/auth already used in competitor_tracker.py |
| textstat for title readability | HIGH | Already installed, well-documented |
| imagehash + Pillow for thumbnails | MEDIUM | imagehash installed, Pillow not yet in pyproject.toml but standard |
| Claude for 4-beat hook parsing | HIGH | Established pattern (algo_synthesizer.py uses same LLM synthesis approach) |
| intel.db schema extension | HIGH | PRAGMA user_version migration pattern well-established (v1→v2 done) |
| title benchmark from intel.db | HIGH | Data already exists, pure SQL aggregation |
| spaCy for hook NLP | NOT RECOMMENDED | Overkill; Claude does better semantic work; Python 3.14 incompatibility risk |

---

## Installation

```bash
# Only one new package — Pillow for thumbnail analysis
pip install "Pillow>=10.0.0"

# Or add to pyproject.toml and reinstall:
pip install -e ".[thumbnails]"
```

All other v7.0 capabilities use the existing installed stack.

---

*Researched: 2026-03-16 for v7.0 Packaging & Hooks Overhaul milestone*
