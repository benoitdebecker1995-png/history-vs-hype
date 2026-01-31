# Project Research Summary

**Project:** History vs Hype v1.3 - Niche Discovery
**Domain:** YouTube niche research and topic validation
**Researched:** 2026-01-31
**Confidence:** HIGH

## Executive Summary

This research evaluates adding niche discovery capabilities to an existing YouTube content production workspace. The channel (197 subs, 82K views) has strong retention (30-35%) but needs help finding high-potential topics with low competition that fit production constraints (no animation, academic sources required, solo creator).

**Recommended approach:** Build tools that filter for YOUR capabilities, not generic "opportunity" scores. The key insight from research: LOW COMPETITION ≠ OPPORTUNITY. True opportunity = high search demand + low *quality* content supply + fits your production format.

**Critical constraint:** No animation capability. This is a STRENGTH — it filters out 80% of "opportunities" that generic tools suggest, leaving document-heavy topics where your primary-source-on-screen approach is a differentiator.

## Key Findings

### Stack Additions (from STACK.md)

**Add 3 new libraries:**
- **trendspyg 0.3.0+** — Google Trends data (replaces archived pytrends)
- **python-youtube 0.9.8+** — Cleaner YouTube Data API wrapper
- **scrapetube** — Quota-free YouTube scraping fallback

**Extend existing:**
- SQLite keywords.db with 5 new tables (trends, competitors, competitor_videos, opportunities, validations)
- tools/discovery/ module with 4 new Python files

**Cost:** $0/month (all free tools, within existing API quotas)

### Expected Features (from FEATURES.md)

**Table Stakes (must have):**
- Search volume estimation (demand proxy from autocomplete position)
- Competition analysis (video count, channel count, quality filtering)
- Keyword research expansion (autocomplete → related queries)
- Competitor channel tracking (monitor 5-10 similar channels)
- Topic categorization and export

**Differentiators (competitive advantage for this channel):**
- **Production constraint filtering** — Auto-reject animation-required topics
- **Channel DNA filtering** — Auto-reject clickbait language, news-first framing
- **Content gap detection** — Find topics NO ONE has covered WELL (quality gap, not quantity)
- **Competition ratio scoring** — Demand/supply quantification (>4.0x = opportunity)
- **Academic source availability check** — Validate NotebookLM research feasibility

**Anti-features (do NOT build):**
- AI auto-generated topic lists (generic, violates channel voice)
- Clickbait title generators (violates documentary tone)
- Viral prediction scores (educational content different from entertainment)
- Real-time trending alerts (can't respond fast with academic workflow)

### Architecture Approach (from ARCHITECTURE.md)

**Integration strategy:**
- Extend keywords.db schema (don't create parallel databases)
- Follow error dict pattern (`{'error': 'msg'}` on failure)
- CLI + Python API dual interface for all modules
- Create `/discover` orchestrator matching `/analyze` pattern
- Generate Markdown reports for human review

**Build order recommendation:**
1. Database schema extension
2. Demand research (trendspyg integration)
3. Competition analysis (YouTube Data API + scrapetube fallback)
4. Format filtering (document-friendly detection)
5. Opportunity scoring (combine all factors)
6. Orchestrator + reports
7. Post-publish validation loop

### Critical Pitfalls (from PITFALLS.md)

**Top 5 to prevent:**

1. **Ignoring Production Constraints** — Discovery surfaces topics requiring animation you can't produce. Prevention: Filter by format BEFORE scoring. Hard block animation-required topics.

2. **Data Staleness** — Topic identified as "low competition" in January has 5 competitors by April publish. Prevention: Weekly refresh of queued opportunities, competition growth tracking.

3. **Invisible Filter Errors (False Negatives)** — Overly conservative filters eliminate long-tail winners. Prevention: Log ALL candidates before filtering, track why eliminated, smoke test with known winners.

4. **Competitor Analysis Without Context** — "Kraut covered this" doesn't mean NO opportunity. His 2-hour animation is different from your 12-minute document focus. Prevention: Track competitor format/angle, not just binary covered/uncovered.

5. **Discovery-Publish Disconnect** — Topics discovered sit in spreadsheets, forgotten. Prevention: Integrate with `/research --new`, track lifecycle from DISCOVERED → PUBLISHED.

## Implications for Roadmap

**Suggested 4-5 phase structure:**

### Phase 15: Database & Demand Foundation
- Extend keywords.db schema with new tables
- Integrate trendspyg for Google Trends data
- Add production constraint filtering schema

### Phase 16: Competition Analysis
- YouTube Data API integration for competitor search
- scrapetube fallback for quota management
- Competitor format/angle tracking (not just binary coverage)

### Phase 17: Format Filtering & Scoring
- Document-friendly vs animation-required detection
- Academic source availability checking
- Opportunity scoring formula (demand × gap × fit / effort)

### Phase 18: Orchestrator & Integration
- `/discover` command wrapping all components
- Markdown opportunity reports
- Integration with `/research --new` workflow

### Phase 19: Validation Loop (optional, requires 3+ published videos)
- Compare predictions to actual performance
- Calibrate scoring weights
- Filter accuracy tracking

**Phase ordering rationale:**
- Database first (foundation for everything)
- Demand + Competition can be built independently
- Format filtering uses both demand and competition data
- Orchestrator wraps everything
- Validation loop needs real video data to calibrate

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack additions | HIGH | trendspyg actively maintained, python-youtube official wrapper |
| Features | HIGH | Table stakes vs differentiators clearly categorized |
| Architecture | HIGH | Follows established workspace patterns |
| Pitfalls | HIGH | Web-verified + channel-specific context |
| Phase structure | MEDIUM | May need adjustment based on actual complexity |

**Overall confidence:** HIGH

Research based on web-validated 2026 tool landscape, official API documentation, and analysis of existing codebase patterns. Feature complexity estimates are conservative.

## Sources

### Primary (from research agents)
- STACK.md — Technology recommendations (trendspyg, python-youtube, scrapetube)
- FEATURES-NICHE-DISCOVERY.md — Feature landscape and categorization
- ARCHITECTURE.md — Integration patterns and build order
- PITFALLS-NICHE-DISCOVERY.md — Prevention strategies for common mistakes

### Web Sources (verified 2026-01-31)
- [trendspyg GitHub](https://github.com/flack0x/trendspyg) — Google Trends library
- [python-youtube PyPI](https://pypi.org/project/python-youtube/) — YouTube API wrapper
- [scrapetube GitHub](https://github.com/dermasmid/scrapetube) — YouTube scraper
- [OutlierKit - Best YouTube Niche Finder Tools 2026](https://outlierkit.com/blog/best-niche-finder-tools-for-youtube)
- [VidIQ vs TubeBuddy Comparison 2026](https://thumbnailtest.com/guides/vidiq-vs-tubebuddy/)
- [YouTube Content Gap Analysis - Subscribr](https://subscribr.ai/p/youtube-content-gap-analysis)

---

*Research completed: 2026-01-31*
*Ready for requirements: YES*
