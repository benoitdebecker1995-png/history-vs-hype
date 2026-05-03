# Workflow Audit Report — 2026-04-14

**Scope:** All files in `.claude/commands/`, `.claude/agents/`, `.claude/REFERENCE/`, plus root `.claude/` files.  
**Method:** Full inventory of 69 files, cross-reference analysis, pipeline mapping, NotebookLM integration assessment.

---

## 1. Broken / Orphaned — Files to Delete or Fix

### Dead File References (10 references across 6 files)

These files reference other files that have been **deleted from disk** (visible in `git status` as `D` entries):

| File with broken ref | Dead reference | Fix |
|---|---|---|
| `REFERENCE/STYLE-GUIDE.md` (line 6) | `scriptwriting-style.md`, `author-style.md`, `USER-VOICE-PROFILE.md` | Header claims "consolidated from" these files but they're deleted. Update to: *"Successor to: scriptwriting-style.md, author-style.md (merged). Voice overrides in VOICE-PROFILE.md. Supplement: NARRATIVE-FLOW-RULES.md."* |
| `REFERENCE/STYLE-GUIDE.md` (lines 1675, 1681-1682) | `VOICE-GUIDE.md`, `USER-VOICE-PROFILE.md`, `author-style.md` | Cross-reference table lists 3 deleted files. Remove those rows. `VOICE-GUIDE.md` → delete row. `USER-VOICE-PROFILE.md` → change to `VOICE-PROFILE.md`. `author-style.md` → delete row (content merged into STYLE-GUIDE). |
| `REFERENCE/creator-techniques.md` (line 1331) | `map-framing-checklist.md` | Gate references non-existent file. Remove the gate entry. |
| `REFERENCE/creator-techniques.md` (line 1341) | `scriptwriting-style.md` | Says "See scriptwriting-style.md". Change to `STYLE-GUIDE.md`. |
| `REFERENCE/SCRIPTWRITING-DEBUNKING-FRAMEWORK.md` (line 407) | `scriptwriting-style.md` | Cross-reference to deleted file. Change to `STYLE-GUIDE.md`. |
| `REFERENCE/CREATOR-PHRASE-LIBRARY.md` (line 290) | `USER-VOICE-PROFILE.md` | Wrong filename. Change to `VOICE-PROFILE.md`. |
| `templates/02-SCRIPT-DRAFT-TEMPLATE.md` (line 44) | `REFERENCE/scriptwriting-style.md` | Says "Choose Opening Pattern (from REFERENCE/scriptwriting-style.md)". Change to `OPENING-HOOK-TEMPLATES.md` or `STYLE-GUIDE.md`. |
| `COMMENT-RESPONSE-STRATEGY.md` (lines 372, 549) | `NOTEBOOKLM-COMMENT-VERIFICATION-TEMPLATE.md` | References deleted template twice. Either inline the guidance or note it's been deprecated. |

### Orphaned Files (not referenced by any command, agent, or INDEX.md)

| File | Status | Recommendation |
|---|---|---|
| `REFERENCE/EXTRACTED-TECHNIQUES.md` | Not referenced by any command or agent in `.claude/`. Only exists as a source uploaded to the Article Workshop NotebookLM notebook. | **Keep** — it's consumed by the NotebookLM notebook, not by Claude Code. Add a comment header: *"This file is a NotebookLM source, not consumed by Claude Code commands."* |
| `.claude/COMPREHENSIVE-OUTLIER-RESEARCH-JAN-2026.md` | Root-level, 45K, not in INDEX.md, dated January 2026 | **Archive** — move to `_ARCHIVE/`. Historical research output, not actively consumed. |
| `.claude/OUTLIER-TOPIC-IDEAS.md` | Root-level, dated Dec 2025, not in INDEX.md | **Archive** — move to `_ARCHIVE/`. Stale topic ideas. |
| `.claude/NOTEBOOKLM-PUBLIC-COMMUNICATION-RESEARCH-PLAN.md` | Root-level, dated Jan 2026, not in INDEX.md | **Archive** — appears to be a one-time research plan that was executed. |
| `.claude/TROUBLESHOOTING.md` | Root-level, dated Nov 2025 (5+ months old), not in INDEX.md | **Review and likely archive** — troubleshooting guide from early project setup. |

### Stale Files (60+ days without update, claiming currency)

| File | Last modified | Issue |
|---|---|---|
| `REFERENCE/NOTEBOOKLM-SCRIPTWRITING-PROMPTS.md` | 2026-01-30 (73 days) | 17 use-case templates — may be out of sync with current NOTEBOOKLM-RESEARCH-PROMPTS.md (updated 2026-03-28). Review for overlap or staleness. |
| `.claude/COMMENT-RESPONSE-STRATEGY.md` | 2025-01-05 (99 days) | References deleted template. Otherwise functional but old. |
| `.claude/VERIFIED-CLAIMS-DATABASE.md` | 2026-03-15 (30 days) | OK for now but approaching threshold. |

---

## 2. Contradictions — Conflicting Rules Across Files

### Contradiction 1: "It's important to note that..." — FORBIDDEN vs ALLOWED

| File | Line | Rule |
|---|---|---|
| **STYLE-GUIDE.md** | 73 | **FORBIDDEN** — listed as "Filler" in Forbidden Phrases table |
| **VOICE-PROFILE.md** | 122-125 | **ALLOWED** — "Allow 'It's important to mention/note that...' when it genuinely flags a paradigm-shifting fact" |

**Resolution:** VOICE-PROFILE.md is correct (line 7: "Where this conflicts with STYLE-GUIDE.md, this file wins for voice/phrasing choices"). But STYLE-GUIDE.md doesn't acknowledge the exception. **Fix:** Add to STYLE-GUIDE.md line 73: `"It's important to note that..." | Filler — EXCEPT when flagging paradigm-shifting facts (see VOICE-PROFILE.md §4)`

### Contradiction 2: Cross-reference table lists non-existent authority files

STYLE-GUIDE.md lines 1675-1682 directs readers to 3 deleted files (`VOICE-GUIDE.md`, `USER-VOICE-PROFILE.md`, `author-style.md`) as if they're supplementary resources. Anyone following these pointers hits dead ends.

**Resolution:** Remove deleted rows, add `VOICE-PROFILE.md` if not already listed.

### No other direct contradictions found

Checked: hook guidance across 3 files (consistent), title rules across 2 files (duplicated but not contradictory), thumbnail rules (single source), fact-checking across 2 files (complementary). **No conflicts.**

### Duplication Risk (not contradictions yet, but drift-prone)

| Rule | File A | File B | Risk |
|---|---|---|---|
| Title penalties: -46% year, -28% colon | `TITLE-GENERATION-PROTOCOL.md` (line 29) | `METADATA-CHECKLIST.md` (lines 13-14) | If one is updated, other goes stale. **Fix:** Cross-reference both files to each other. |
| NotebookLM guidance | `NOTEBOOKLM-SOURCE-STANDARDS.md` | `NOTEBOOKLM-RESEARCH-PROMPTS.md` | Cross-referenced to each other ✓ |
| NotebookLM guidance | `NOTEBOOKLM-SCRIPTWRITING-PROMPTS.md` | Neither of the above | **No cross-references.** Writer using only SCRIPTWRITING-PROMPTS won't know about source standards. **Fix:** Add header cross-references. |
| Fact-checking | `fact-checking-protocol.md` | `FACT-CHECK-SIMPLIFICATION-RULES.md` | Complementary but not cross-linked. **Fix:** Cross-reference both. |

---

## 3. Workflow Gaps — Stages with No Quality Gate

Ranked by impact (what breaks if this gap isn't closed).

### CRITICAL — Silent failure likely

**Gap 1: Research verification % not enforced before scripting**
- **Stage:** `/research` → `/script`
- **Problem:** `/research` documents "90%+ verified before script" but nothing checks this. `/script --new` runs regardless of verification state. User could script from 40% verified research.
- **Impact:** Script built on unverified claims → `/verify` catches it later → full rework cycle. Worst case: unverified claim survives to publication.
- **Fix:** `/script` reads `01-VERIFIED-RESEARCH.md`, counts ✅ vs ⏳/❌ markers, BLOCKS if <90%.

**Gap 2: Script output has zero structural validation**
- **Stage:** `/script --new` → `/verify`
- **Problem:** `/script` generates a complete script but runs no check on coherence, structure, evidence placement, hook quality, or pacing. The script could be fundamentally broken (front-loaded evidence, weak hook, no turn, no close pattern). `/verify` only checks *facts*, not *structure*.
- **Impact:** Structurally weak script passes fact-check, gets filmed, underperforms on retention. Structure issues only caught if user manually runs `/preflight --gate script`.
- **Fix:** Auto-run structure check (via `structure-checker-v2` agent constraints) immediately after `/script` generation. Flag CRITICAL structural issues before `/verify`.

**Gap 3: Fact-check verdict not enforced before filming prep**
- **Stage:** `/verify` → `/prep`
- **Problem:** `/prep` doesn't check whether `03-FACT-CHECK-VERIFICATION.md` verdict is APPROVED. User could film with NEEDS-REVISION script.
- **Impact:** Errors flagged by `/verify` get filmed anyway → post-filming discovery → reshoot or publish with known errors.
- **Fix:** `/prep` reads `03-FACT-CHECK-VERIFICATION.md`, BLOCKS if verdict ≠ APPROVED.

### HIGH — Quality degradation likely

**Gap 4: Metadata consistency check is optional**
- **Stage:** `/publish` → YouTube upload
- **Problem:** `/discover --check` validates metadata consistency (primary keyword in title/description/tags, no stuffing) but it's optional. User can skip it.
- **Impact:** Suboptimal SEO → lower discovery → fewer impressions. Given packaging is the #1 growth bottleneck, this matters.
- **Fix:** Auto-run `/discover --check` at end of `/publish --metadata`. BLOCK on HIGH priority issues.

**Gap 5: Bridge test not automated**
- **Stage:** `/publish` thumbnail generation → upload
- **Problem:** Title-thumbnail-hook alignment ("bridge test") is documented as critical but runs manually. User decides if thumbnail matches title matches hook. Could publish misaligned packaging.
- **Impact:** Loose bridge → viewer expectations don't match content → early drop-off.
- **Fix:** Auto-run bridge test during `/publish` thumbnail generation. Score each title+thumbnail pairing against the script's first 15 seconds.

**Gap 6: Pattern insights not consumed by /publish**
- **Stage:** `/patterns` → (gap) → `/publish`
- **Problem:** `/patterns` extracts winning formulas (topic angles, title structures, format correlations). `/next` uses these for topic ranking. But `/publish` generates titles fresh — never references what patterns are working.
- **Impact:** Each video's metadata is optimized in isolation, not against proven channel patterns.
- **Fix:** `/publish` reads `FEEDBACK-PATTERNS.md` and uses winning patterns as a scoring modifier for title candidates.

### MEDIUM — Friction, not failure

**Gap 7: SRT not validated before upload**
- `/fix` corrects transcription errors but doesn't validate timestamps or structural integrity.

**Gap 8: Competitor intelligence staleness**
- `/intel` can be 30+ days stale. Commands reading it get outdated competitor landscape.

**Gap 9: /analyze doesn't feed back to intel.db**
- Performance data exists but doesn't enrich competitor intelligence. Feedback loop is open.

---

## 4. NotebookLM Integration Map

For each workflow gap, assessment of whether a NotebookLM query would add value.

### HIGH ROI — Worth the friction

**Integration 1: Post-/script structure validation via Competitor Notebook**
- **Stage:** After `/script --new`, before `/verify`
- **Notebook:** Competitor video notebook (85 transcripts + 55 sources)
- **Query:** *"Compare this script's structure against the top 10 performing videos in the notebook. Check: (1) hook pattern — does it match a proven opener type? (2) turn placement — is it in the 15-25% or 45-55% sweet spot? (3) evidence pacing — is evidence distributed every 60-90s or front-loaded? (4) closing type — does it match what retains viewers?"*
- **What it catches:** Structural weaknesses the `structure-checker-v2` agent misses because it checks against *rules*, not against *what actually performs*. The notebook has real retention data baked into the transcripts.
- **Friction:** Medium — requires pasting script into notebook chat, reading response, acting on it. ~5 minutes.
- **Verdict:** **HIGH ROI.** This is the biggest gap in the pipeline. Structure-checker catches rule violations; competitor notebook catches "technically correct but boring" scripts.

**Integration 2: /greenlight title validation via Competitor Notebook**
- **Stage:** During `/greenlight` Step 2 (title scoring)
- **Notebook:** Competitor video notebook
- **Query:** *"Here are 5 title candidates for a video about [TOPIC]. Which patterns from the top-performing titles in the notebook do these match? Which patterns are they missing? Suggest modifications based on what actually worked."*
- **What it catches:** `title_scorer.py` checks structural rules (no years, no colons, keyword placement). Notebook checks against *real outlier patterns* — the difference between a 65-score title and a breakout title.
- **Friction:** Low — can be run during greenlight's existing NotebookLM step (P1-P4 prompts already exist).
- **Verdict:** **HIGH ROI.** Title scoring is rule-based; this adds pattern-matching against what actually works. Already partially implemented via Packaging Notebook prompts (P1-P4), but not formalized as a gate.

### MEDIUM ROI — Worth it for important videos

**Integration 3: Post-/verify prose quality via Article Workshop Notebook**
- **Stage:** After `/verify` APPROVED, before filming
- **Notebook:** Article Workshop notebook (3ccc9c87 — 19 articles, critique/rewrite notes, EXTRACTED-TECHNIQUES.md)
- **Query:** *"Read this script and critique the prose using the standards from the 19 articles in this notebook. Flag: (1) sentences that are too long for spoken delivery, (2) transitions that feel like AI wrote them, (3) places where the argument could be tighter, (4) opportunities for the 'one killer sentence' technique."*
- **What it catches:** `/verify` checks facts. `/humanify` checks voice. Neither checks *prose quality at the argument level* — whether the writing is compelling, tight, and persuasive vs. merely accurate.
- **Friction:** Medium — requires pasting full script. But this is a pre-filming polish step, worth 10 minutes on important videos.
- **Verdict:** **MEDIUM ROI.** Not every video needs this. Use for videos targeting >10K views or topics where argument quality matters more than evidence density (ideological topics with 2.31% sub rate).

**Integration 4: /publish metadata via Competitor Notebook**
- **Stage:** During `/publish --metadata` description/tag generation
- **Notebook:** Competitor video notebook
- **Query:** *"What description structures and tag strategies do the top-performing videos in this notebook use? Given this video's topic [X] and primary keyword [Y], suggest a description structure and tag list modeled on what actually ranks."*
- **What it catches:** `/publish` generates descriptions from templates. Notebook could surface patterns from videos that actually rank well in search — real SEO patterns vs. template-following.
- **Friction:** Medium — requires querying notebook during publish flow.
- **Verdict:** **MEDIUM ROI.** Descriptions matter less than titles/thumbnails for this channel (73% subscriber-driven traffic). Worth it once search traffic becomes a growth priority.

### LOW ROI — Not worth the friction

**Integration 5: /engage comment fact-check via Research Notebooks**
- **Stage:** During `/engage --respond` for academic challenges
- **Notebook:** Per-project research notebooks
- **Query:** Verify commenter's claim against sources in the video's research notebook.
- **What it catches:** Comments citing academic sources that contradict the video.
- **Friction:** High — requires opening the specific project's notebook, pasting the comment, reading response.
- **Verdict:** **LOW ROI.** `/engage` already fact-checks responses via web search. NotebookLM adds marginal value for rare academic challenges. Only worth it for comments citing specific page numbers.

**Integration 6: /sources quality validation via Competitor Notebook**
- **Stage:** During `/sources --recommend`
- **Notebook:** Competitor video notebook
- **Query:** Check if recommended sources are the same ones competitors use (indicates commodity research).
- **Verdict:** **LOW ROI.** Source selection is already governed by NOTEBOOKLM-SOURCE-STANDARDS.md (university press only). The competitive advantage is *depth*, not *different sources*.

### Summary Table

| Stage | Notebook | Query type | ROI | Add? |
|---|---|---|---|---|
| Post-`/script`, pre-`/verify` | Competitor (85 transcripts) | Structure comparison against performers | **HIGH** | Yes — formalize as optional gate |
| `/greenlight` title eval | Competitor (85 transcripts) | Title pattern matching against outliers | **HIGH** | Yes — extend existing P1-P4 prompts |
| Post-`/verify`, pre-filming | Article Workshop (3ccc9c87) | Prose critique against best articles | **MEDIUM** | Yes — for high-stakes videos only |
| `/publish` metadata | Competitor (85 transcripts) | Description/tag pattern from top performers | **MEDIUM** | Later — when search traffic matters |
| `/engage` academic challenges | Per-project research | Claim verification | **LOW** | No — existing fact-check sufficient |
| `/sources` recommendations | Competitor (85 transcripts) | Source commodity check | **LOW** | No — depth > differentiation |

---

## Appendix: File Inventory Summary

| Category | Total files | Healthy | Issues found |
|---|---|---|---|
| REFERENCE | 35 | 28 | 7 (dead refs, orphaned, stale) |
| Agents | 9 | 9 | 0 |
| Commands | 25 + 1 deprecated README | 25 | 0 (commands themselves are clean) |
| Root .claude | 8 | 3 | 5 (orphaned/archivable) |
| Templates | ~5 | 4 | 1 (dead ref in script template) |
| **Total** | **~82** | **69** | **13 files need attention** |

### Priority Action List

1. **Fix 10 dead references** — 15 minutes, prevents confusion
2. **Add STYLE-GUIDE.md exception note** for "important to note" phrase — 2 minutes
3. **Cross-link duplicated rules** (title penalties, NotebookLM files, fact-check files) — 10 minutes
4. **Archive 4 root-level orphans** — 5 minutes
5. **Implement verification % gate in /script** — prevents the #1 silent failure mode
6. **Auto-run structure check after /script** — closes the biggest quality gap
7. **Enforce fact-check verdict in /prep** — prevents filming with known errors
8. **Formalize post-script NotebookLM structure query** — highest ROI integration
