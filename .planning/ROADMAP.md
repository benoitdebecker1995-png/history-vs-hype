# Roadmap: v1.1 Analytics & Learning Loop

**Created:** 2026-01-23
**Milestone:** v1.1
**Depth:** Comprehensive

## Overview

Build a feedback system that helps learn what works from each video. YouTube Analytics API integration provides automated data pulls (CTR, retention, watch time). Post-publish analysis captures lessons in structured format. Pattern recognition surfaces cross-video insights monthly.

## Phases

### Phase 7: API Foundation

**Goal:** YouTube Analytics API is configured and secure, ready for data scripts.

**Dependencies:** None (fresh start)

**Requirements:**
- INTEG-01: Google Cloud project set up with YouTube Analytics API enabled
- INTEG-02: OAuth2 flow implemented for channel authorization
- INTEG-06: Credentials stored securely (not in git)

**Success Criteria:**
1. Google Cloud Console shows YouTube Analytics API enabled for project
2. Running OAuth2 flow opens browser, user authorizes, token is saved
3. Credentials file exists in secure location (gitignored, not in repo)
4. Token refresh works without re-authorization

**Plans:** 2 plans

Plans:
- [ ] 07-01-PLAN.md — Infrastructure setup + Google Cloud Console configuration (human checkpoint)
- [ ] 07-02-PLAN.md — OAuth2 Python implementation + connection verification

---

### Phase 8: Data Pull Scripts

**Goal:** Scripts can pull all key metrics from YouTube Analytics API on demand.

**Dependencies:** Phase 7 (API must be configured)

**Requirements:**
- INTEG-03: Script pulls CTR data per video
- INTEG-04: Script pulls retention/audience data per video
- INTEG-05: Script pulls watch time and engagement metrics

**Success Criteria:**
1. Running script with video ID returns CTR percentage for that video
2. Running script with video ID returns retention curve data (drop-off points visible)
3. Running script with video ID returns watch time, likes, comments, shares
4. Script handles API errors gracefully (quota exceeded, invalid video ID, expired token)
5. Output format is structured (JSON or Markdown) for downstream consumption

---

### Phase 9: Post-Publish Analysis Command

**Goal:** User can run a single command to get comprehensive analysis of any video's performance with lessons logged.

**Dependencies:** Phase 8 (data pull scripts must exist)

**Requirements:**
- ANALYSIS-01: Command to trigger post-publish analysis
- ANALYSIS-02: CTR comparison vs. channel average
- ANALYSIS-03: Retention drop-off points identified
- ANALYSIS-04: Comments pulled and categorized (questions, objections, requests)
- ANALYSIS-05: Lessons captured in structured format
- ANALYSIS-06: Analysis linked to video project folder

**Success Criteria:**
1. Running `/analyze <video-id>` produces a complete analysis report
2. Report shows CTR as percentage and comparison to channel average (above/below/by how much)
3. Report identifies specific timestamps where retention drops occur
4. Report includes comment summary with categories (questions viewers asked, objections raised, content requests)
5. Report ends with "Lessons Learned" section in structured format
6. Analysis file is saved in the video's project folder (e.g., `video-projects/_ARCHIVED/1-somaliland-2025/POST-PUBLISH-ANALYSIS.md`)

---

### Phase 10: Pattern Recognition

**Goal:** User can see cross-video patterns that reveal what's working and what's not.

**Dependencies:** Phase 9 (need accumulated analysis data from multiple videos)

**Requirements:**
- PATRN-01: Cross-video comparison by topic type vs. performance
- PATRN-02: Monthly summary generation
- PATRN-03: Title/thumbnail patterns correlated with CTR

**Success Criteria:**
1. Running pattern analysis shows performance breakdown by topic type (territorial vs. ideological vs. myth-busting)
2. Monthly summary command generates insights across all videos published that month
3. Title patterns (length, keywords, structure) are correlated with CTR data
4. Thumbnail characteristics (map vs. face, text amount) correlated with CTR data
5. Insights are actionable ("Territorial topics average 2.3x more views than ideological")

---

## Progress

| Phase | Name | Requirements | Status |
|-------|------|--------------|--------|
| 7 | API Foundation | INTEG-01, INTEG-02, INTEG-06 | Planned (2 plans) |
| 8 | Data Pull Scripts | INTEG-03, INTEG-04, INTEG-05 | Not Started |
| 9 | Post-Publish Analysis | ANALYSIS-01 through ANALYSIS-06 | Not Started |
| 10 | Pattern Recognition | PATRN-01, PATRN-02, PATRN-03 | Not Started |

## Coverage

| Requirement | Phase |
|-------------|-------|
| INTEG-01 | Phase 7 |
| INTEG-02 | Phase 7 |
| INTEG-03 | Phase 8 |
| INTEG-04 | Phase 8 |
| INTEG-05 | Phase 8 |
| INTEG-06 | Phase 7 |
| ANALYSIS-01 | Phase 9 |
| ANALYSIS-02 | Phase 9 |
| ANALYSIS-03 | Phase 9 |
| ANALYSIS-04 | Phase 9 |
| ANALYSIS-05 | Phase 9 |
| ANALYSIS-06 | Phase 9 |
| PATRN-01 | Phase 10 |
| PATRN-02 | Phase 10 |
| PATRN-03 | Phase 10 |

**Total:** 15/15 requirements mapped

---

*Roadmap created: 2026-01-23*
*Phase 7 planned: 2026-01-24*
