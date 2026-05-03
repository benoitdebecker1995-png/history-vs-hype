# CLAUDE.md

## Repository Overview

**History vs Hype** — YouTube channel: evidence-based myth-busting about geopolitics, colonial history, border disputes, and ideological narratives. Academic research + primary sources to debunk historical myths.

**Stats:** 515 subs, 219K+ views, 47 long-form, 28.1% median retention | **Audience:** Males 25-44 (UK, DE, CA, US)
**Format:** 8-12 min hybrid talking head + B-roll evidence | **Hard cap 12 min** (r=-0.455 duration-retention, n=47)

**Subscriber trigger:** "intellectual competence" — proving you understand SYSTEMS, not narratives. HOW > WHY. Mechanism > politics. Logistics/legal/admin angles win. RealLifeLore/Wendover overlap audience.

**Growth bottleneck:** Packaging, not content. Only 3/47 broke 2K views. Content that gets impressions performs well. `/greenlight` BEFORE any research.

---

## Core Principles

1. **Historical integrity** — every claim verified with credible sources
2. **Real quotes with page numbers** — word-for-word from academic sources (the competitive advantage)
3. **Modern relevance** — connect history to 2024-2026 developments
4. **Academic balance** — present multiple perspectives, acknowledge counter-evidence
5. **Deep causal chains** — explain WHY (consequently, thereby, which meant that)
6. **No oversimplification** — maintain nuance while accessible

---

## Quick Start Commands

**Pre-production:** `/greenlight` (FIRST) → `/research` → `/sources`
**Production:** `/script` → `/verify` → `/prep` → `/thumbnail`
**Post-production:** `/publish` → `/fix` → `/engage`
**Navigation:** `/status` | `/help` | `/next` | `/intel`
**Article writing:** `article-writer` agent (CONVERT / WRITE / EDIT / WORKSHOP modes — invoke directly)
**Analytics:** `/analyze` | `/patterns` | `/growth` | `/retitle`

---

## File Organization (CRITICAL)

**Lifecycle folders (MANDATORY):**
- `video-projects/_IN_PRODUCTION/` → `_READY_TO_FILM/` → `_ARCHIVED/`
- **NEVER** create loose folders in `video-projects/` root
- Naming: `video-projects/[lifecycle]/[number]-[topic-slug-year]/`

**Before creating any file:** Read `PROJECT_STATUS.md` → Glob for existing folder → confirm lifecycle stage

**Standard project files:**
- `01-VERIFIED-RESEARCH.md` — single source of truth for verified facts
- `02-SCRIPT-DRAFT.md` — production-ready script
- `03-FACT-CHECK-VERIFICATION.md` — final quality gate
- `YOUTUBE-METADATA.md` — title, description, tags, timestamps
- `PROJECT-STATUS.md` — track progress

See: `.claude/FOLDER-STRUCTURE-GUIDE.md`

---

## Research: Two-Phase Approach (CRITICAL)

**Phase 1: Internet research** — map landscape, identify claims to verify (Wikipedia, news, Google Scholar). All findings marked ❓. Free, 2-4 hours.

**Phase 2: NotebookLM academic verification** — university press books ONLY (Cambridge, Oxford, etc.), top scholars, critical editions. Budget UNLIMITED. Upload 10-20 sources, use citation grounding for exact page numbers. Output: verified quotes ready for script.

**NEVER skip Phase 2.** That's the competitive advantage. See: `.claude/REFERENCE/NOTEBOOKLM-SOURCE-STANDARDS.md`

---

## Verified Workflow (3-Phase Quality Gates)

1. **Research + Verify** → `01-VERIFIED-RESEARCH.md` — mark each fact ✅/⏳/❌. Gate: 90%+ verified before writing.
2. **Script from verified facts ONLY** → `02-SCRIPT-DRAFT.md` — if fact isn't verified, STOP and verify first.
3. **Cross-check** → `03-FACT-CHECK-VERIFICATION.md` — every script line vs verified research. Verdict: ✅ APPROVED or ❌ REVISION.

---

## Script Writing

**Authoritative reference:** `.claude/REFERENCE/WRITING-VOICE-AND-STYLE.md` — READ BEFORE WRITING ANY SCRIPT (PARTS 1-5 script-side).

**Voice:** "Calm Prosecutor" — emotionally low, intellectually high. Evidence-based referee.

**Key rules:** Real quotes with page numbers | Primary sources ON SCREEN | Define every term immediately | Contractions ("it's" not "it is") | Dates spoken ("On June 16th, 2014") | "Here's" max 2-4/script

**Structure:** Myth-first for non-territorial (30.3% vs 22.4% retention) | Turn at 15-25% runtime (3.2x, not 25-35% dead zone at 2.1x) | Modern relevance every 90s | Pattern interrupt every 2-3 min | Deep causal chains throughout

**Language to avoid:** "X is occupying Y" | "Z destroyed the culture" | absolutist language | conspiracy framing without documentation

**Templates:** `.claude/REFERENCE/OPENING-HOOK-TEMPLATES.md` | `.claude/REFERENCE/CLOSING-SYNTHESIS-TEMPLATES.md`

---

## Fact-Checking

**Source hierarchy:** See `.claude/REFERENCE/fact-checking-protocol.md`
- Tier 1: Primary documents, peer-reviewed (2010+), expert historians
- Tier 2: Journalists, intl org reports, declassified docs
- Tier 3: News sources (verify multiple), documentary evidence

**Red flags requiring immediate verification:**
- "The court ruled X..." → Which paragraph? Exact quote?
- "The treaty says..." → Which article? Exact language?
- Any quote without page number → Verify with primary source

**NEVER include unverified claims.** If you can't verify: don't include it, flag it, or ask user for source.

See: `.claude/FACT-CHECK-SIMPLIFICATION-RULES.md` for 8 anti-oversimplification rules

---

## Packaging-First Workflow

1. **Search demand** — <1K/mo = hard stop
2. **Title generation** — `title_scorer.py`. No years (-46% CTR), no colons (-28%). Front-load keyword. Declarative = default (3.8% CTR).
3. **Thumbnail concept** — text overlay MANDATORY (87% niche), no face (0% niche), maps for territorial. `thumbnail_checker.py`
4. **THEN research** — only after `/greenlight` passes

See: `tools/PACKAGING_MANDATE.md` | `.claude/REFERENCE/TITLE-GENERATION-PROTOCOL.md`

**Channel DNA:** History channel with modern relevance, NOT geopolitics with historical background. Test: "Will this matter in 10 years regardless of who's in power?"

---

## Working Style

- **Be direct and efficient** — no pleasantries, get to the point
- **Read first, ask later** — use Glob/Read to find info, don't ask user
- **Parallel tool calls** — when multiple independent reads needed
- **Don't ask for info in files you can read** — find it yourself
- See: `.claude/USER-PREFERENCES.md` for complete guide

---

## Critical Reminders

1. **PACKAGING FIRST** — `/greenlight` before ANY research
2. **NEVER skip Phase 2** (NotebookLM) — that's the competitive advantage
3. **ACADEMIC SOURCES ONLY** — university presses, top scholars. Budget UNLIMITED
4. **REAL QUOTES with page numbers** — not summaries
5. **Primary sources ON SCREEN** — non-optional
6. **Read WRITING-VOICE-AND-STYLE.md before scripts** — voice, delivery, patterns, checklist (PARTS 1-5)
7. **Write for spoken delivery** — contractions, natural phrasing
8. **Deep causal chains** — explain WHY (consequently, thereby, which meant that)
9. **Intellectual honesty** — acknowledge what opposing side gets right
10. **Single source of truth** — 01-VERIFIED-RESEARCH.md only
11. **Quality gates** — 90% verified → write; 100% cross-checked → film
12. **HOW > WHY** for subscriber growth — mechanisms/logistics, not politics
13. **No years/colons in titles** — -46% / -28% CTR penalty
14. **Text overlay on thumbnails** — 2-4 words, not full title. Maps for territorial.
15. **AGENT ORCHESTRATION** — Read `.claude/AGENT-ORCHESTRATION.md` before spawning sub-agents — return contract, tiers, rate-limit rule

---

## Agent skills

### Issue tracker

Issues live in GitHub Issues for `benoitdebecker1995-png/history-vs-hype`, accessed via `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Default canonical labels: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context layout — `CONTEXT.md` and `docs/adr/` at repo root. See `docs/agents/domain.md`.

---

## Key References

- **Style:** `.claude/REFERENCE/WRITING-VOICE-AND-STYLE.md` (authoritative)
- **Commands:** `.claude/commands/` | **Agents:** `.claude/agents/`
- **Reference index:** `.claude/REFERENCE/INDEX.md`
- **Packaging:** `tools/PACKAGING_MANDATE.md`
- **Performance data:** See memory files (patterns, analytics, competitor findings)
- **Topic pipeline:** `channel-data/TOPIC-PIPELINE.md`

**Start:** `/greenlight` → `/research --new`
