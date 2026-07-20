# REFERENCE Index

**Which files to read for each task. Don't read all — read only what your task needs.**

> **2026-05-02 consolidation:** 9 voice/style files merged into `WRITING-VOICE-AND-STYLE.md`. Source files archived at `.claude/_ARCHIVE/voice-consolidation-2026-05-02/`. See PART-mapping at the bottom of `WRITING-VOICE-AND-STYLE.md`. **2026-07-20 split (LLM-CRAFT-UPGRADE-PLAN C3):** the consolidated file is now split by PART into `WRITING-VOICE-AND-STYLE-P1..P7-*.md` sibling files; `WRITING-VOICE-AND-STYLE.md` is a lean index that points to them. **2026-07-20 split (LLM-CRAFT-UPGRADE-PLAN C3):** the consolidated file is now split by PART into `WRITING-VOICE-AND-STYLE-P1..P7-*.md` sibling files; `WRITING-VOICE-AND-STYLE.md` is a lean index that points to them.

---

## Scriptwriting (read these 4)
1. **WRITING-VOICE-AND-STYLE.md** (index) — PARTS 1-5 are script-side, split into sibling files: `-P1-CORE-VOICE.md` (voice), `-P2-EVIDENCE.md`, `-P3-STRUCTURE.md`, `-P4-DEBUNKING.md`, `-P5-TECHNIQUES.md`. AUTHORITATIVE.
2. **THESIS-DISCIPLINE.md** — Universal 9-step throughline-finding methodology (script-writer Rule 36, article-writer Rule 21).
3. **OPENING-HOOK-TEMPLATES.md** — Hook patterns with retention data (deep template library; cross-references PART 5.2).
4. **CLOSING-SYNTHESIS-TEMPLATES.md** — Close patterns (cross-references PART 5.5).

## Newsletter / Article Writing (read this 1)
1. **WRITING-VOICE-AND-STYLE.md** (index) — PARTS 1, 2, 6, 7 are article-side: `-P1-CORE-VOICE.md`, `-P2-EVIDENCE.md`, `-P6-ARTICLE.md` (10 rules, SCQA, verdict sentences, anti-slop, CRIBS, first-person modes), `-P7-NEWSLETTER.md` (workshop toolkit). AUTHORITATIVE.

## Fact-Checking (read these 2)
1. **fact-checking-protocol.md** — Source hierarchy (Tier 1/2/3), verification process.
2. **FACT-CHECK-SIMPLIFICATION-RULES.md** — 8 anti-oversimplification rules.

## Research / NotebookLM (read these 3)
1. **NOTEBOOKLM-SOURCE-STANDARDS.md** — Academic source quality standards.
2. **NOTEBOOKLM-RESEARCH-PROMPTS.md** — Chat prompts for verification.
3. **NOTEBOOKLM-SCRIPTWRITING-PROMPTS.md** — Prompts for script material (includes Use Case 18 Thesis Articulation Check).

## Visual / Filming (read this 1)
1. **HYBRID_TALKING_HEAD_GUIDE.md** — When to show face vs B-roll.

## YouTube / Publishing (read these 3)
1. **METADATA-CHECKLIST.md** — Title, thumbnail, description checklist.
2. **TITLE-GENERATION-PROTOCOL.md** — Title generation rules + scoring.
3. **VIDIQ-CHANNEL-DNA-FILTER.md** — Filter VidIQ suggestions.

## Newsletter Publishing (read this 1)
1. **NEWSLETTER-METADATA-CHECKLIST.md** — Subject lines, subtitles, SEO metadata.

## Comments / Engagement (read these 2)
1. **youtube-comment-response-guide.md** — Response voice and templates.
2. **`/comment-mine` command** (`.claude/commands/comment-mine.md`) — Mine competitor comments via yt-dlp to lock thesis angle. Always yt-dlp route; never WebFetch or Playwright for comments.

## Untranslated Evidence Series (read this 1)
1. **UNTRANSLATED-EVIDENCE-FORMAT-GUIDE.md** — Format for translation episodes.

## Formats & Templates (read this 1)
1. **FORMAT-TEMPLATES.md** — 10 signature series structures (Three-Case Braid, Synchronic Interpretive Contest, etc.).

## Thesis Workflow (read this 1)
1. **THESIS-DERIVATION-WORKFLOW-PROMPT.md** — Multi-round candidate audit prompt for thesis derivation.

## Script Support (read as needed)
1. **SCRIPT-TO-DELIVERY-LESSONS.md** — Pre-filming polish lessons (32 lessons through Tripoli).
2. **SCRIPTWRITING-EXAMPLES.md** — Competitor §1-§20 examples (separate corpus seam — kept independent of WRITING-VOICE-AND-STYLE.md).
3. **HOOK-PATTERN-LIBRARY.md** — Same scope as OPENING-HOOK-TEMPLATES.md (deep template library).
4. **coverage-audit.md** — Coverage matrix by video type.
5. **breakout-retention-audit.md** — Retention data from breakout videos.

## Data Files (consumed by tools, not for human reading)
1. **GAP-DATABASE.md** — Gap analysis data.
2. **THUMBNAIL-EVALUATION-FRAMEWORK.md** — Thumbnail scoring.

## Other
1. **channel-values.md** — Brand DNA.
2. **primary-sources.md** — Primary source handling.
3. **FOLDER-STRUCTURE-GUIDE.md** — Folder system rules.
4. **CODE-MAP.md** — Project code structure crib sheet (from graphify AST run, 2026-05-25). Load for "where does X live" / "what depends on Y" questions instead of grepping. Includes god nodes, real communities, noise to ignore, worktree-duplication caveat.
5. **RESEARCH-CONCEPT-MAP.md** — Cross-video concept/entity/quote index for the 15 published research files (Gemini Flash bulk-read, 2026-05-25). Load for "have I cited X before?" / "which videos invoke Y?" discovery questions. **Verify slugs before citing** — ~2 quote attributions are wrong; this is T3 synthesis, not primary research. Pairs with CODE-MAP.md to cover the doc-content side graphify's AST run missed.
6. **RESEARCH-GRAPH.json** — Structured-JSON companion to RESEARCH-CONCEPT-MAP. 88 entities, 22 scholars, 55 edges, 22 citations, 2 bridges across 15 videos. Schema: `videos[]/entities[]/scholars[]/edges[]/citations[]/bridges[]`. Query with Python (cheatsheet in concept-map footer). Same verification rule applies — stub entities flagged as `[stub:...]` in role field.
7. **graphify-out/research/** (not in REFERENCE/, separate dir) — interactive graphify build of the research graph. Contains `graph.html` (open in browser), `graph.json` (graphify-schema, 110 nodes/55 edges/2 hyperedges), `GRAPH_REPORT.md`, `query.py` (BFS subgraph helper — THE token-saving entry point for "tell me about X" questions), `build.py` + `extract-prompt.txt` (regenerate). See concept-map footer for query examples.
8. **GRAPHIFY-OPS.md** — Operating manual + session handoff for the graphify setup (built 2026-05-25/26). Read first when picking up graphify work later: current state, health-check commands, workflow patterns, open work, recovery, known caveats. References everything in 4-7 above.
