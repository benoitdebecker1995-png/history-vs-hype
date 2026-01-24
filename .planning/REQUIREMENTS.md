# Requirements: History vs Hype Workspace

**Defined:** 2026-01-23
**Core Value:** Every video shows sources on screen — viewers see the evidence themselves

## v1.1 Requirements

Requirements for Analytics & Learning Loop milestone.

### API Integration

- [x] **INTEG-01**: Google Cloud project set up with YouTube Analytics API enabled
- [x] **INTEG-02**: OAuth2 flow implemented for channel authorization
- [ ] **INTEG-03**: Script pulls CTR data per video
- [ ] **INTEG-04**: Script pulls retention/audience data per video
- [ ] **INTEG-05**: Script pulls watch time and engagement metrics
- [x] **INTEG-06**: Credentials stored securely (not in git)

### Post-Publish Analysis

- [ ] **ANALYSIS-01**: Command to trigger post-publish analysis
- [ ] **ANALYSIS-02**: CTR comparison vs. channel average
- [ ] **ANALYSIS-03**: Retention drop-off points identified
- [ ] **ANALYSIS-04**: Comments pulled and categorized (questions, objections, requests)
- [ ] **ANALYSIS-05**: Lessons captured in structured format
- [ ] **ANALYSIS-06**: Analysis linked to video project folder

### Pattern Recognition

- [ ] **PATRN-01**: Cross-video comparison by topic type vs. performance
- [ ] **PATRN-02**: Monthly summary generation
- [ ] **PATRN-03**: Title/thumbnail patterns correlated with CTR

## Out of Scope

| Feature | Reason |
|---------|--------|
| Predictive analytics | Can't guarantee video performance — focus on learning, not prediction |
| VidIQ integration | No API available — YouTube Analytics API is the path |
| Automated publishing | Out of scope — this milestone is about learning, not automation |
| Thumbnail A/B testing | YouTube handles this natively — focus on analyzing results |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| INTEG-01 | Phase 7 | Complete |
| INTEG-02 | Phase 7 | Complete |
| INTEG-03 | Phase 8 | Pending |
| INTEG-04 | Phase 8 | Pending |
| INTEG-05 | Phase 8 | Pending |
| INTEG-06 | Phase 7 | Complete |
| ANALYSIS-01 | Phase 9 | Pending |
| ANALYSIS-02 | Phase 9 | Pending |
| ANALYSIS-03 | Phase 9 | Pending |
| ANALYSIS-04 | Phase 9 | Pending |
| ANALYSIS-05 | Phase 9 | Pending |
| ANALYSIS-06 | Phase 9 | Pending |
| PATRN-01 | Phase 10 | Pending |
| PATRN-02 | Phase 10 | Pending |
| PATRN-03 | Phase 10 | Pending |

**Coverage:**
- v1.1 requirements: 15 total
- Mapped to phases: 15
- Unmapped: 0

---
*Requirements defined: 2026-01-23*
*Last updated: 2026-01-24 after Phase 7 completion*
