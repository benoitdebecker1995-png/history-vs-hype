# Requirements: History vs Hype Workspace

**Defined:** 2026-04-14
**Core Value:** Every video shows sources on screen — viewers see the evidence themselves

## v8.0 Requirements — Pipeline Quality Gates

Close 3 critical silent-failure gaps + bridge test + NotebookLM auto-queries. Based on WORKFLOW-AUDIT-2026-04-14.md findings.

### Verification Gates

- [ ] **GATE-01**: `/script` reads `01-VERIFIED-RESEARCH.md`, counts checkmark vs pending/failed markers, and BLOCKS with clear message if <90% verified
- [ ] **GATE-02**: `/script` displays verification summary (X/Y claims verified, Z%) before proceeding when >= 90%

### Structure Validation

- [ ] **STRUCT-01**: After `/script` generates a script, `structure-checker-v2` agent auto-runs against the output and reports CRITICAL/WARNING/INFO findings
- [ ] **STRUCT-02**: CRITICAL structure findings block progression (user must acknowledge or fix before `/verify`)

### Fact-Check Enforcement

- [ ] **FACT-01**: `/prep` reads `03-FACT-CHECK-VERIFICATION.md` and BLOCKS if verdict is not APPROVED
- [ ] **FACT-02**: `/prep` displays the verdict and any outstanding revision items when blocking

### Bridge Test

- [ ] **BRIDGE-01**: During `/publish`, auto-run bridge test scoring title + thumbnail concept against the script's first 30 seconds (hook alignment)
- [ ] **BRIDGE-02**: Bridge test flags WEAK alignments (title promises something the hook doesn't deliver) as warnings

### NotebookLM Auto-Queries

- [ ] **NLM-01**: After `/script` generation, auto-query Competitor notebook via MCP for structure comparison (hook pattern, turn placement, evidence pacing, closing type). Falls back to ready-to-paste prompt if MCP unavailable
- [ ] **NLM-02**: During `/greenlight` title evaluation, auto-query Competitor notebook via MCP for title pattern matching against outlier patterns. Falls back to ready-to-paste prompt if MCP unavailable
- [ ] **NLM-03**: For high-stakes videos (user-flagged or ideological topics), auto-query Article Workshop notebook via MCP for prose critique. Falls back to ready-to-paste prompt if MCP unavailable

## Future Requirements

None deferred from this milestone.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Metadata consistency auto-check | 73% subscriber-driven traffic — SEO not the growth bottleneck |
| `/patterns` to `/publish` integration | Optimization, not quality gate — defer to future |
| SRT validation | Medium priority friction, not failure |
| Full NLM automation without fallback | MCP primary, paste fallback ensures reliability |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| GATE-01 | TBD | Pending |
| GATE-02 | TBD | Pending |
| STRUCT-01 | TBD | Pending |
| STRUCT-02 | TBD | Pending |
| FACT-01 | TBD | Pending |
| FACT-02 | TBD | Pending |
| BRIDGE-01 | TBD | Pending |
| BRIDGE-02 | TBD | Pending |
| NLM-01 | TBD | Pending |
| NLM-02 | TBD | Pending |
| NLM-03 | TBD | Pending |

**Coverage:**
- v8.0 requirements: 11 total
- Mapped to phases: 0
- Unmapped: 11 (roadmap pending)

---
*Requirements defined: 2026-04-14*
*Last updated: 2026-04-14 after initial definition*
