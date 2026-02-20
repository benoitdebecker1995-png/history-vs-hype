# Phase 42: Pipeline Hardening & Research Ingestion - Context

**Gathered:** 2026-02-20
**Status:** Ready for planning

<domain>
## Phase Boundary

Two capabilities: (1) Make the translation CLI reliable with proper credential management, error handling, and a smoke test, and (2) build a NotebookLM-to-verified-research ingestion flow that extracts claims, lets the user review them, and writes approved claims to 01-VERIFIED-RESEARCH.md.

Requirements: PIPE-01, PIPE-02, PIPE-03, RES-01, RES-02, RES-03

</domain>

<decisions>
## Implementation Decisions

### Credential Management
- Single .env file at project root (G:/History vs Hype/.env), all tools read from there
- Anthropic API key is the only credential needed (translation pipeline uses Claude API only)
- When API key is missing, show step-by-step fix instructions (e.g., "Missing ANTHROPIC_API_KEY. Add it to .env: echo ANTHROPIC_API_KEY=sk-... >> .env")
- Auto-create .env.example with commented placeholders on first run if no .env exists

### Error Messaging
- Actionable error messages with step-by-step fix instructions (not stack traces)
- Cover: missing API key, network failure, rate limiting — each with specific remediation steps

### NLM Ingestion Input
- Support both copy-paste and file input depending on size (small = paste, long sessions = file path)
- NLM output is a mix of structured (bullet points with inline citations) and freeform paragraphs — parser must handle both
- Integrate as a slash command (/research --ingest or similar) rather than standalone script

### Claim Extraction
- Categorize extracted claims by type (statistics, quotes, events, etc.) to help organize verified research sections

### Claim Review UX
- Show full list of claims, user marks which to approve (checklist style, not one-at-a-time)
- Review happens via generated markdown file with checkboxes — user edits, tool reads back approvals
- Include edit option: approve as-is, reject, or edit wording/citation before writing
- Require existing project folder — error if 01-VERIFIED-RESEARCH.md path doesn't exist (user sets up via /research --new first)

### Claude's Discretion
- Exact NLM output parsing strategy (regex, LLM-based, hybrid)
- Claim categorization taxonomy
- Smoke test implementation details
- Error retry strategy for network failures
- Markdown file format for claim review

</decisions>

<specifics>
## Specific Ideas

- Claim review via markdown checkboxes aligns with the existing VERIFIED-RESEARCH.md workflow — user is already comfortable editing markdown files
- The ingestion flow should feel like a natural extension of the existing two-phase research workflow (Phase 1: internet, Phase 2: NotebookLM)
- Error messages should assume a non-technical user who just wants to get the translation running

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 42-pipeline-hardening-research-ingestion*
*Context gathered: 2026-02-20*
