# VidIQ MCP — Full Capability Map

**Generated:** 2026-07-01 (full-capability sweep) · **Server:** `mcp__vidiq__*` (`https://mcp.vidiq.com/mcp`, OAuth) · **Plan:** Boost
**Governs:** every VidIQ MCP tool, classed by fit with the channel's identity + gate model.
**Companion docs:** `docs/VIDIQ-MCP-SETUP.md` (setup/auth) · `docs/adr/0013-vidiq-mcp-scope-and-competitor-source-of-truth.md` · ADR-0012 (packaging-lock authority).

> **Why this exists.** The setup doc was written when VidIQ MCP was a small read-only surface. The
> live server exposes ~55 tools, including a **generation suite** (AI video, voiceover clone, b-roll,
> thumbnails, motion graphics, clips) that *spends credits and produces assets*. This map inventories
> everything and fixes each tool's verdict so "it exists" never silently drifts into "we use it."

## The two constraints that decide every verdict

1. **Enrichment, never a gate** (ADR-0012). VidIQ output lands on the ENRICHMENT line of the
   packaging lock. It is recorded, never decides. The four pass/fail filters decide. A confident
   VidIQ score (e.g. "title 95/100") is exactly the failure mode that ADR-0012 was written for.
2. **Identity guard** (PACKAGING_MANDATE; intro `yt:yMAWJcjo_ug`): "history through primary sources —
   showing how history is done." Any tool that fabricates a **real source, figure, historical
   footage, or the narrator's voice** is out of bounds regardless of convenience.

**Verdict legend:** **WIRE** = research/data we lack or do via a fragile scraper; extends the
enrichment role, safe. **GUARDED** = usable but bounded (enrichment-only, clickbait/identity-guarded,
never a decider). **REJECT** = collides with the identity guard or the anti-clickbait moat; off-limits
with the reason stated.

---

## Credits (Boost tier, as of 2026-07-01)

`vidiq_balance`: 3,326 total = 1,471 renewable (of 2,000, resets 2026-07-17) + 1,855 bonus (non-renewing).
Standard research/scoring calls cost **5 credits**; **Video Watch 10**; utility (balance, channels,
competitors, trend categories) **0**. Generation tools cost far more and drain the same pool — the
identity guard fences them off before cost is even a factor. Watch the renewable-vs-bonus split:
bonus credits don't refill, so treat them as a one-time reserve.

---

## Research / data tools — WIRE / GUARDED

| Tool | Cost | Verdict | Use |
|---|---|---|---|
| `vidiq_balance`, `vidiq_user_channels`, `vidiq_list_competitors`, `vidiq_trend_categories` | 0 | WIRE | Free utility. Balance-watch, auth check, competitor introspection. |
| `vidiq_outliers` | 5 | **WIRE** | Official-API competitor breakout mining. Replaces the scraped `intel.db` path in `packaging_intel` (bot-walled). Keyed on the synced competitor set. **Centerpiece.** Output: `videoTitle/viewCount/breakoutScore/videoTopics/videoPublishedAt`. |
| `vidiq_keyword_research` | ~5 | **WIRE** | Real YouTube search volume + competition + Overall score (+ per-country). Feeds the V1 demand *enrichment* and TOPIC-RUBRIC "30% VidIQ Overall" (was a manual in-app paste). Modes: `research` / `country_search` / `country_top`. |
| `vidiq_channel_search` (breakout filter) | 5 | GUARDED | Niche/competitor **channel** discovery (supersedes `vidiq_breakout_channels`). Feeds `/greenlight --scan`; candidates reconciled against `competitor_channels.json`. |
| `vidiq_breakout_channels` | 5 | GUARDED | **Deprecated** alias of the above. Don't wire new calls to it. |
| `vidiq_similar_channels` | 5 | GUARDED | "Channels like X" — competitor-set expansion candidates. |
| `vidiq_trending_videos`, `vidiq_youtube_search` | 5 | GUARDED | Trend / live-hook discovery; Step-0 + `--scan` enrichment. |
| `vidiq_video_watch` | 10 | GUARDED | Frame-by-frame retention diagnostic — no repo equivalent. Wired in `/retitle` Step 3 to sharpen the packaging-vs-content call. Enrichment only. |
| `vidiq_channel_stats` / `_analytics` / `_performance_trends` / `_videos` | 0–5 | GUARDED | Competitor channel forensics; ad-hoc research. |
| `vidiq_video_stats` / `_comments` / `_transcript` | 0–5 | GUARDED | Per-video forensics. `video_comments` = audience-demand / sentiment mining (complements `/comment-mine`). |
| `vidiq_get_channels_by_ids`, `vidiq_get_videos_by_ids` | 5 | GUARDED | Resolve IDs → metadata (used this session to audit the tracked set). |
| `vidiq_ig_profile` / `_ig_profile_reels` / `_ig_outlier_reels_search` / `_ig_reel_watch` / `_ig_accounts_from_outliers` | 5 | GUARDED | Instagram cross-platform outlier/trend spotting (public data). Low priority; no identity conflict. |
| `vidiq_update_competitors` | 0 | GUARDED (**write**) | The **one** write call we use: sync VidIQ's tracked competitors to `competitor_channels.json`. See `tools/intel/vidiq_competitor_sync.py`. |
| `vidiq_submit_feedback` | 0 | GUARDED | Send feedback to VidIQ; incidental. |

## Scoring tools — GUARDED (enrichment, clickbait-guarded)

| Tool | Cost | Verdict | Use |
|---|---|---|---|
| `vidiq_score_title` | 5 | GUARDED | Second-opinion CTR score on the ENRICHMENT line only. **Rejected + logged** if it trips `title_scorer`'s brand gate / CTR kill-list. Never the decider (the "VidIQ 95/100" failure ADR-0012 exists for). |
| `vidiq_score_thumbnail` | 5 | GUARDED | *New* — no thumbnail scorer was wired before. Still informational only (ADR-0007: no pre-publish number predicts the click). Records, never gates. |

## Generation suite — REJECT (identity guard), one narrow GUARDED exception

| Tool | Verdict | Reason |
|---|---|---|
| `vidiq_generate_video`, `vidiq_compose` | **REJECT** | Full AI video = the opposite of "primary sources on screen." Fabrication destroys the auditor's-edge moat. |
| `vidiq_generate_broll`, `vidiq_generate_clips` | **REJECT** | AI-generated footage of historical events = fabricated evidence. Violates "real subject, NO AI-generated figure." |
| `vidiq_generate_thumbnail`, `vidiq_refine_thumbnail` | **REJECT** | AI figures are banned on thumbnails (`/greenlight` Step 3 / `thumbnail_checker`): "invisible polish of real material only." |
| `vidiq_voiceover_generate`, `vidiq_voiceover_clone`, `vidiq_voiceover_clone_start`, `vidiq_voiceover_list_voices` | **REJECT** | Channel is talking-head in the creator's real voice; the **read-aloud pass is a T1 QA gate** (catches logic errors — `feedback-read-aloud-catches-logic`). An AI voice removes the gate *and* the authenticity. |
| `vidiq_generate_titles` | **REJECT (as a generator)** | Titles are generated FROM the locked script — the channel's moat. A generic clickbait factory is anti-voice. (Its sibling `vidiq_score_title` stays GUARDED.) |
| `vidiq_motion_graphics` | **GUARDED (narrow)** | Non-figurative kinetic text / abstract animation (NOT fabricated footage or figures) could be a zero-budget aid — but it overlaps the in-repo **HTML-Deck B-Roll pipeline** (`feedback-html-deck-broll`), which is controllable + Playwright-verified. Prefer HTML-deck; evaluate once; never use it to depict a "real" source/figure. |
| `vidiq_generate_video`'s async helpers `vidiq_job_poll`, `vidiq_jobs_list` | INFRA | Poll/list async generation jobs; relevant only if a generation tool is ever used. |

---

## Where the WIRE tools plug in

- `vidiq_outliers` → `tools/packaging_intel.py` (cache-refresh into `competitor_videos`) → `/greenlight` Step 0D.
- `vidiq_keyword_research` → `/greenlight` Step 1/1b demand enrichment + `tools/TOPIC-RUBRIC.md`.
- `vidiq_video_watch` → `/retitle` Step 3 retention diagnostic.
- `vidiq_update_competitors` → `tools/intel/vidiq_competitor_sync.py` (repo → VidIQ, manual re-sync).

## Competitor set (the outlier lens)

VidIQ's tracked competitors = the repo's `style-match` + `broad-history` tiers (18 channels), synced
from `tools/intel/competitor_channels.json`. The `geopolitics` tier (stakes-first anti-voice lane) is
**excluded** from the standing default. `vidiq_outliers` accepts arbitrary `channelIds`, so scans can
pass category-filtered subsets: **broad-history** for topic-demand ("is this hot for viewers like
mine"), **style-match** for craft/differentiation ("has a peer covered this, and how"). See ADR-0013.
