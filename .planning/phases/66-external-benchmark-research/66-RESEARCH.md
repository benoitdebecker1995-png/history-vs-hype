# Phase 66: External Benchmark Research - Research

**Researched:** 2026-03-16
**Domain:** YouTube niche benchmarking — competitor CTR proxies, hook pattern extraction, structured data authoring
**Confidence:** MEDIUM (CTR proxy methodology is sound; exact per-channel CTR inaccessible without channel-owner API access)

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- 500K+ subscribers only — large enough for reliable CTR pattern data
- Format-matched channels: talking head + evidence B-roll, document-based, maps (Kraut, Knowing Better, Shaun, History Matters style)
- No animation-heavy or high-production channels whose CTR norms reflect unreplicable formats
- Claude discovers channel candidates; user approves final list
- 5-8 channels — Claude picks count based on data availability, minimum 5 per roadmap success criteria
- Benchmark JSON granularity: range + median per pattern: `{min_ctr, max_ctr, median_ctr, sample_count, example_titles}`
- Two dimensions: title pattern AND topic type as separate axes (enables BENCH-03)
- Metadata header: `{collected_date, channels_sampled, total_videos_analyzed, refresh_after}` for automated staleness detection
- Outlier identification via views-to-subscriber ratio (3x+ typical views) — not VidIQ-estimated CTR
- Hook analysis: rhetorical move classification (cold_fact, myth_contradiction, authority_challenge, specificity_bomb) with exact first sentence
- Library structure: separated by topic type (territorial, ideological, political fact-check)
- 8-10 examples per pattern type
- Hybrid execution: Claude gathers programmatically, user manually verifies and adds any CTR proxy data from VidIQ
- ctr_tracker.py run included as Phase 66 deliverable (success criteria #4)

### Claude's Discretion
- Exact channel count (5-8 based on data availability)
- Transcript extraction method (auto-captions vs manual)
- JSON field naming conventions
- How to handle channels with inconsistent upload formats
- Whether to include a "confidence" field per benchmark entry based on sample size

### Deferred Ideas (OUT OF SCOPE)
- None identified during discussion phase
</user_constraints>

---

## Summary

Phase 66 is a research-only deliverable: no code written, no existing tools modified. The output is four artifacts consumed by Phases 67-70 — a JSON benchmark file, a hook patterns markdown file, a hook pattern library for agent consumption, and a fresh CTR snapshot run.

The core challenge is that YouTube does not expose competitor CTR publicly. The methodology therefore relies on views-to-subscriber ratio as a CTR proxy: videos where a channel dramatically outperforms its own average on views represent cases where both packaging (title + thumbnail) and hook retention worked together. This is directional, not precise — which is exactly what the CONTEXT.md specifies ("advisory, not a hard gate").

The planner must account for the hybrid execution model: Claude will do the programmatic gathering pass (channel discovery, YouTube Data API public stats, web search for outlier video identification), but the user must manually verify and supply any VidIQ-sourced CTR proxy data. The tasks should be split accordingly, with a clear handoff point between Claude's autonomous work and the user review gate.

**Primary recommendation:** Structure tasks so Claude produces a complete draft of all four artifacts in one pass, then a single user-review task approves/adjusts the channel list and any manually-verifiable data before the artifacts are finalized.

---

## Standard Stack

### Core (existing — no new installs required)
| Tool | Version | Purpose | Why Standard |
|------|---------|---------|--------------|
| Python (tools/) | 3.11-3.13 | All scripting | Project-wide constraint (spaCy requires <=3.13) |
| json (stdlib) | — | Write niche_benchmark.json | No dependency, stable |
| yt-dlp | Latest | Auto-caption extraction from YouTube | Most reliable open tool for YT transcripts |
| tools.youtube_analytics.ctr_tracker | Existing | Run CTR snapshot refresh (success criterion #4) | Already integrated into ctr_snapshots table |

### Supporting (may need install)
| Tool | Purpose | When to Use |
|------|---------|-------------|
| yt-dlp | Transcript extraction if manual review needed | If auto-captions available on target channel videos |
| youtube-transcript-api | Python library for transcript extraction | Lighter alternative to yt-dlp when only transcripts needed |

**yt-dlp install (if not present):**
```bash
pip install yt-dlp
pip install youtube-transcript-api
```

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| yt-dlp for transcripts | Manual copy-paste from YouTube | Manual is slower but 100% reliable for 8-10 videos |
| views/subscriber ratio proxy | VidIQ-estimated CTR | VidIQ is more accurate but requires user manual lookup; ratio is automatable |

---

## Confirmed Channel Candidates

Research confirmed subscriber counts and format compatibility for the following channels (as of early 2026):

| Channel | Subs (approx) | Format Match | Notes |
|---------|--------------|--------------|-------|
| Kraut | ~600K | HIGH — talking head, animated maps, long-form 12-120 min | Exact style model per CLAUDE.md |
| Knowing Better | ~952K | HIGH — talking head, maps, source-heavy | Core style model per CLAUDE.md |
| Shaun | ~760K | HIGH — document-first, talking head, no animation | Core style model; low upload frequency (6 in 2 years) |
| History Matters | ~1.88M | MEDIUM — animated, not talking head | Formerly "Ten Minute History"; 3-5 min animated shorts, format mismatch with talking head but high volume of title pattern data |
| WonderWhy | Unconfirmed >500K | MEDIUM — animated geography/history | Animation-heavy, may fail format filter |
| Toldinstone | ~617K | HIGH — talking head, primary source focus, ancient history | Format matches; topic is ancient vs. modern — may limit territorial/ideological pattern applicability |

**Recommendation for channel count:** 5 confirmed format-matched channels (Kraut, Knowing Better, Shaun + 2 more to confirm). History Matters and WonderWhy are animation-heavy — use only if format-matched channels yield insufficient title pattern samples.

**Channels to investigate further during execution:**
- Fall of Civilizations (Paul Cooper) — cinematic documentary, talking head narration, likely 500K+
- Histocrat — smaller history channel, may be below 500K threshold
- RealLifeLore — geography/geopolitics, 5M+ subs, mostly animated but high volume of title pattern data

---

## Architecture Patterns

### Pattern 1: CTR Proxy Methodology (views/subscriber ratio)

**What:** For each candidate channel, identify videos that outperform the channel's own typical views by 3x or more. These are the outlier packaging successes.

**How to calculate:**
```
channel_typical_views = median(recent 20 videos, view_count)
outlier_threshold = channel_typical_views * 3
outlier_videos = [v for v in channel_videos if v.view_count >= outlier_threshold]
```

**Data source:** YouTube Data API v3 `videos.list(part='statistics,snippet')` — public, no auth required for read-only.

**Confidence label per entry:**
- HIGH: sample_count >= 10 outlier videos analyzed
- MEDIUM: sample_count 5-9
- LOW: sample_count < 5

**Why 3x threshold:** Accounts for algorithm spikes from recommendations; a 3x outlier is unlikely to be purely algorithmic luck without packaging contribution.

### Pattern 2: niche_benchmark.json Structure

The JSON must use the same pattern names as `title_scorer.py` (PATTERN_SCORES keys) and topic type names already in use across the codebase:

```json
{
  "metadata": {
    "collected_date": "2026-MM-DD",
    "channels_sampled": ["Kraut", "Knowing Better", "Shaun", "..."],
    "total_videos_analyzed": 0,
    "refresh_after": "2026-06-16"
  },
  "by_pattern": {
    "versus": {
      "min_ctr": 3.5,
      "max_ctr": 6.2,
      "median_ctr": 4.8,
      "sample_count": 12,
      "confidence": "HIGH",
      "example_titles": ["X vs Y: ...", "..."],
      "note": "proxy CTR from views/subscriber ratio — directional only"
    },
    "declarative": { "..." : "..." },
    "how_why": { "..." : "..." },
    "question": { "..." : "..." },
    "colon": { "..." : "..." }
  },
  "by_topic_type": {
    "territorial": {
      "proxy_ctr_range": [2.8, 5.5],
      "median_proxy_ctr": 3.8,
      "sample_count": 18,
      "confidence": "MEDIUM"
    },
    "ideological": { "..." : "..." },
    "political_fact_check": { "..." : "..." }
  }
}
```

**Critical constraint for Phase 67:** The `metadata.collected_date` and `metadata.refresh_after` fields are specifically required by the planned `benchmark_store.py` for automated staleness detection. These MUST be present.

### Pattern 3: Hook Pattern Library Structure for Agent Consumption

`HOOK-PATTERN-LIBRARY.md` must be machine-parseable by `hook_scorer.py` (Phase 69). This means consistent heading structure and fenced code blocks for examples, not prose paragraphs.

Recommended structure:
```markdown
## Pattern: cold_fact

**Topic type:** territorial
**Description:** Opens with a specific number, date, or measurement that reframes the question.
**Hook-to-topic fit:** High for territorial disputes (map-and-number framing)

### Examples (from 100K+ sub channels)
1. Channel: Kraut | Video: [Title] | First sentence: "[exact text]"
2. Channel: Knowing Better | Video: [Title] | First sentence: "[exact text]"
...

### Trigger mechanism
[1-2 sentences on why this works for the topic type]
```

**Why this structure:** `hook_scorer.py` currently uses regex pattern matching (`_detect_beats`, `_detect_beats`). Phase 69 will add external pattern matching by scanning first-sentence examples in this library for linguistic patterns, not prose descriptions.

### Pattern 4: Execution Model — Two-Stage Hybrid

**Stage A (Claude autonomous):**
1. Discover and confirm channel candidate list with subscriber counts
2. Query public YouTube API for recent video lists + view counts per channel
3. Compute views/subscriber ratio to identify outlier videos (3x+ threshold)
4. Extract first sentences from those videos via yt-dlp auto-captions or youtube-transcript-api
5. Draft all four deliverable files with `[NEEDS USER VERIFICATION]` flags where manual lookup needed

**Stage B (User review gate):**
1. Review and approve/modify channel list
2. Add any VidIQ-sourced CTR estimates for flagged outlier videos
3. Approve final artifact content before Phase 67 begins

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| YouTube video stats | Custom scraper | YouTube Data API v3 `videos.list` | Public API, free, 10K quota/day |
| Transcript extraction | Custom caption parser | yt-dlp `--write-auto-subs` or youtube-transcript-api | Both handle YouTube's auto-caption format reliably |
| JSON schema validation | Custom validator | Python dataclass or TypedDict + json.dumps | Phase 67's benchmark_store.py will validate on read; no pre-validation needed |
| CTR data for competitors | Any scraping | views/subscriber ratio proxy | Actual CTR is not publicly accessible; proxy is the correct approach |

---

## Common Pitfalls

### Pitfall 1: Animation-Heavy Channel Contamination
**What goes wrong:** Including Kurzgesagt, WonderWhy, History Matters (post-2018) inflates benchmark CTR because high-production animation achieves CTR through visual spectacle not replicable with talking head format.
**Why it happens:** These channels have 500K+ subs and appear in "history YouTube" searches.
**How to avoid:** Filter on format before sampling. Talking head + evidence B-roll only. If a channel's median video is animated, exclude from title pattern benchmarks.
**Warning signs:** Channel has 2M+ subs but videos are 4-8 minutes — likely animation-optimized, not long-form documentary.

### Pitfall 2: Proxy CTR Conflation With Real CTR
**What goes wrong:** Treating views/subscriber ratio as equivalent to actual CTR percentage. A video with 3x typical views might have achieved that via browse/suggested (where CTR is irrelevant) not search (where CTR drives distribution).
**Why it happens:** Proxy methodology is easier to compute but conflates multiple traffic sources.
**How to avoid:** Add a `note` field in every JSON entry: `"proxy only — not actual CTR"`. Ensure Phase 67's benchmark_store.py surfaces this note in scorer output.
**Warning signs:** Proxy CTR values appear suspiciously high (>8%) — flag as outlier, reduce confidence to LOW.

### Pitfall 3: JSON Structure Drift From Phase 67 Contract
**What goes wrong:** Phase 66 authors `niche_benchmark.json` with field names that Phase 67's `benchmark_store.py` doesn't expect, causing silent None returns.
**Why it happens:** Phase 66 produces the file without seeing Phase 67's implementation.
**How to avoid:** The CONTEXT.md explicitly names the required fields. Treat the JSON structure in this research as a contract. The planner should include a verification task: "Confirm JSON field names match benchmark_store.py expectations before closing phase."
**Warning signs:** benchmark_store.py returns None on first Phase 67 test.

### Pitfall 4: Hook Examples Without First Sentences
**What goes wrong:** Documenting hook "patterns" without including exact first-sentence text from real videos. Phase 69 needs literal examples for the external pattern matching feature.
**Why it happens:** First sentences require transcript access, which takes time. Researchers fall back to paraphrased descriptions.
**How to avoid:** Every hook example entry must include the exact verbatim first sentence (or first two sentences if the rhetorical move spans both). Flag entries without exact text as `[NEEDS TRANSCRIPT VERIFICATION]`.

### Pitfall 5: CTR Snapshot Staleness Blocking Phase 67
**What goes wrong:** Phase 67 starts but ctr_tracker.py hasn't been run since 2026-02-23 (the last confirmed collection date per STATE.md), meaning scorer recalibration is anchored to 3-week-old data.
**Why it happens:** ctr_tracker.py is success criterion #4 for Phase 66 but easy to forget when focused on external channel research.
**How to avoid:** Make ctr_tracker.py the FIRST task in Phase 66 execution. Confirm snapshot date is >= 2026-03-01 before any other work begins.

---

## Code Examples

### Public YouTube API — Get Channel Video List
```python
# No auth required for public channel data
# Source: YouTube Data API v3 docs
import googleapiclient.discovery

youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=API_KEY)

# Get channel uploads playlist ID
channel_resp = youtube.channels().list(
    part='contentDetails',
    forHandle='KrautYT'  # or forUsername, or id=CHANNEL_ID
).execute()

uploads_playlist = channel_resp['items'][0]['contentDetails']['relatedPlaylists']['uploads']

# List videos in playlist (50 at a time)
playlist_resp = youtube.playlistItems().list(
    part='snippet',
    playlistId=uploads_playlist,
    maxResults=50
).execute()
```

### yt-dlp Auto-Caption Extraction
```bash
# Download auto-generated English captions only (no video download)
yt-dlp --write-auto-subs --sub-lang en --skip-download --sub-format vtt \
  "https://www.youtube.com/watch?v=VIDEO_ID"
```

### youtube-transcript-api (Python)
```python
# Source: pypi.org/project/youtube-transcript-api
from youtube_transcript_api import YouTubeTranscriptApi

transcript = YouTubeTranscriptApi.get_transcript('VIDEO_ID', languages=['en'])
first_sentences = ' '.join([t['text'] for t in transcript[:10]])  # first ~90 seconds
```

### views/subscriber ratio outlier detection
```python
# Pseudocode for outlier identification
import statistics

def find_outliers(video_stats: list[dict], channel_subs: int) -> list[dict]:
    """Identify videos with 3x+ typical views/subscriber ratio."""
    ratios = [v['view_count'] / channel_subs for v in video_stats]
    median_ratio = statistics.median(ratios)
    threshold = median_ratio * 3
    return [v for v, r in zip(video_stats, ratios) if r >= threshold]
```

### CTR snapshot freshness check
```bash
# Run from project root — success criterion #4
python -m tools.youtube_analytics.ctr_tracker

# Verify result date in output (should be >= 2026-03-01)
# If already run today, re-running is safe (idempotent via existing_check)
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Own-channel CTR only as scoring anchor | Own-channel primary + niche percentile as context | Phase 66 (now) | Prevents false "passing" scores when own CTR baseline is artificially low |
| Static PATTERN_SCORES in title_scorer.py | DB-enriched scores via title_ctr_store | Phase 53-54 era | Already in place; Phase 67 extends further |
| Hook scoring internal-only (Rule 19 beats) | Hook scoring + external pattern matching | Phase 69 (future) | Phase 66 provides the external pattern library |

**CTR benchmarks context (verified, MEDIUM confidence):**
- Education/history YouTube channels: 3-7% CTR range (Miraflow, 2026)
- Platform-wide average: 4-5% across all creators (Miraflow, 2026)
- "Good" for educational content: 4-6% (stripo.email research, 2025)
- History vs Hype own-channel data: declarative 3.8%, versus 3.7%, how_why 3.3%, colon 2.3%
- Own-channel data sits at the low end of the 3-7% educational range — confirms external benchmarks are needed to avoid self-referential baseline trap

---

## Open Questions

1. **Fall of Civilizations subscriber count**
   - What we know: Cinematic documentary format, talking head narration, high production — strong format match
   - What's unclear: Current subscriber count (last confirmed data not found in search results)
   - Recommendation: Check directly on YouTube during execution; include if 500K+

2. **Shaun upload frequency impact on sample size**
   - What we know: Only 6 videos in last 2 years (760K subs); most are essay-style videos 40-90 min
   - What's unclear: Whether 6 videos is enough to establish a reliable views/subscriber ratio baseline
   - Recommendation: Use Shaun for hook pattern extraction (high quality examples) but flag as LOW confidence for title pattern benchmarking (n too small)

3. **WonderWhy format qualification**
   - What we know: Animated geography/history, format may not match talking head requirement
   - What's unclear: Current subscriber count, proportion of talking head vs pure animation
   - Recommendation: Check during execution; exclude if primarily animated

4. **yt-dlp availability on project machine**
   - What we know: Not confirmed installed; project uses Python 3.11-3.13
   - What's unclear: Whether yt-dlp is already in the environment
   - Recommendation: First task should check `yt-dlp --version`; if absent, fall back to youtube-transcript-api or manual extraction for the ~10-15 target videos

5. **niche-hook-patterns.md vs HOOK-PATTERN-LIBRARY.md distinction**
   - What we know: Success criteria #2 calls for `niche-hook-patterns.md` (analysis document) and #3 calls for `HOOK-PATTERN-LIBRARY.md` (agent-consumable)
   - What's unclear: Whether these should be two completely separate files or one file with two sections
   - Recommendation: Two separate files. `niche-hook-patterns.md` is human-readable analysis (used for research review); `HOOK-PATTERN-LIBRARY.md` is structured for machine parsing by hook_scorer.py and script-writer-v2

---

## Validation Architecture

> nyquist_validation key is absent from .planning/config.json — treating as enabled.

### Test Framework
| Property | Value |
|----------|-------|
| Framework | None applicable — Phase 66 is research only, zero code |
| Config file | N/A |
| Quick run command | N/A |
| Full suite command | `python -m tools.youtube_analytics.ctr_tracker --report-only` (verifies snapshot freshness) |

### Phase Requirements → Test Map

| Deliverable | Behavior | Verification Type | Verification Command |
|-------------|----------|-------------------|---------------------|
| niche_benchmark.json | File exists with required fields | File existence + JSON parse | `python -c "import json; d=json.load(open('channel-data/niche_benchmark.json')); assert 'metadata' in d and 'by_pattern' in d and 'by_topic_type' in d"` |
| niche-hook-patterns.md | File exists, non-empty | File existence + line count | Manual review |
| HOOK-PATTERN-LIBRARY.md | File exists with correct heading structure | File existence + grep for required sections | `grep -c "## Pattern:" .claude/REFERENCE/HOOK-PATTERN-LIBRARY.md` (expect >= 4 sections) |
| CTR snapshot fresh | Snapshot date >= 2026-03-01 | ctr_tracker.py report output | `python -m tools.youtube_analytics.ctr_tracker --report-only` (check date in output) |
| channels_sampled >= 5 | metadata.channels_sampled array has 5+ entries | JSON parse | `python -c "import json; d=json.load(open('channel-data/niche_benchmark.json')); assert len(d['metadata']['channels_sampled']) >= 5"` |
| Hook examples >= 50% from 100K+ channels | Success criterion #3 | Manual review against channel list | User review gate task |

### Sampling Rate
- **Per task commit:** Spot-check relevant output file exists and is non-empty
- **Per wave merge:** Run all JSON validation checks above
- **Phase gate:** All 4 success criteria confirmed TRUE before `/gsd:verify-work`

### Wave 0 Gaps
None — no test files needed. This phase produces data files, not code. Verification is file-existence checks and manual review.

---

## Sources

### Primary (HIGH confidence)
- CONTEXT.md (66-CONTEXT.md) — locked decisions on methodology, structure, execution model
- STATE.md — confirmed last CTR snapshot date (2026-02-23), pending todos
- tools/title_scorer.py — confirmed pattern names (versus, declarative, how_why, question, colon, the_x_that) and topic types
- tools/research/hook_scorer.py — confirmed beat classification system (cold_fact, myth, contradiction, payoff_preview)
- tools/youtube_analytics/ctr_tracker.py — confirmed snapshot mechanism, idem potency behavior

### Secondary (MEDIUM confidence)
- Miraflow (2026): education/history CTR range 3-7%, platform average 4-5% — [YouTube CTR Benchmarks 2026](https://miraflow.ai/blog/youtube-ctr-benchmarks-2026)
- stripo.email research (2025): "good" educational CTR 4-6% — [YouTube Benchmarks by Niche](https://research.stripo.email/youtube-benchmarks)
- Socialblade/search: Kraut ~600K subs, Knowing Better ~952K subs, Shaun ~760K subs, History Matters ~1.88M subs, Toldinstone ~617K subs — confirmed format-qualified channels

### Tertiary (LOW confidence)
- WonderWhy format qualification: animated, subscriber count unconfirmed above 500K
- Fall of Civilizations subscriber count: format matches but count not confirmed from search results
- Shaun title pattern sample size reliability: 6 videos in 2 years is likely too few for reliable CTR proxy statistics

---

## Metadata

**Confidence breakdown:**
- Channel candidate list: MEDIUM — 4 of 6 candidates confirmed format-matched and above 500K threshold; 2 need execution-time verification
- CTR proxy methodology: HIGH — views/subscriber ratio is sound and matches CONTEXT.md specification exactly
- JSON structure: HIGH — field names and axes confirmed against existing codebase (title_scorer.py, hook_scorer.py, benchmark_store.py plans)
- External CTR benchmarks (3-7% for edu/history): MEDIUM — two independent sources agree; no history-specific sub-niche breakdown available
- Hook pattern classification system: HIGH — directly maps to existing hook_scorer.py beat taxonomy

**Research date:** 2026-03-16
**Valid until:** 2026-06-16 (90 days; channel subscriber counts may shift but methodology is stable)
