# Phase 69: Hook Quality Upgrade - Context

**Gathered:** 2026-03-18
**Status:** Ready for planning

<domain>
## Phase Boundary

Upgrade `tools/research/hook_scorer.py` with a title-fulfillment check (HOOK-01) and topic-type hook style recommender (HOOK-02). Implement `/script --hooks` command that scores existing hooks and generates LLM-written alternatives. Replace the current 4-beat detection with the user's "Document Reveal" framework (anomaly → stakes → inciting incident).

</domain>

<decisions>
## Implementation Decisions

### Title-Fulfillment Check (HOOK-01)
- **Dual check:** Both entity echo AND promise-type alignment must pass
- **Entity echo:** At least one key entity from the title must appear in the hook's first ~50 words
- **Promise-type match:** Categorize title promise (mechanism, document, conflict, myth-bust) and verify hook delivers the same type — not generic context
- **"Document Reveal" alignment:** The hook's specific anomaly should connect to the title's systemic scope (informed by user's 4-Layer Framework)
- **Title input:** Title is a required parameter for the fulfillment check. Without a title, hook_scorer still works but skips fulfillment dimension
- **Mismatch output:** Name the specific gap AND suggest a fix. E.g., "❌ Title promises Spain vs Portugal conflict, but hook opens with generic South America context. Try: name Spain or Portugal in first sentence, frame as rivalry."

### 4-Layer Framework Integration (REPLACES current beat detection)
- **Replace, don't extend:** Current 4-beat detection (cold_fact, myth, contradiction, payoff_preview) is replaced by the user's "Document Reveal" framework
- **New structure elements:** anomaly (specific document/map/detail), stakes connection (systemic consequence), inciting incident (the "turn" within ~45 seconds)
- **Point mapping:** Claude's discretion on how to map the 3 framework elements to the existing 40-point beat_score budget
- **Library categories preserved:** HOOK-PATTERN-LIBRARY.md categories (cold_fact, specificity_bomb, myth_contradiction, contextual_opening) remain for style recommendation. Framework = scoring structure, library categories = style vocabulary

### /script --hooks Command (SC2)
- **Dual function:** Score existing hook from script AND generate alternative variants
- **Input:** Script path + title (via --title flag). Title required for fulfillment check
- **Existing hook extraction:** Read first ~300 words of script as the current hook
- **Urgency flagging:** Always generate alternatives, but flag urgency level based on existing hook score. Claude's discretion on score thresholds
- **Topic type:** Auto-detect from script content, --topic flag overrides (same pattern as Phase 67 title scorer)

### Hook Variant Generation
- **Method:** LLM-generated from script material (not template-based). Claude reads script + title, extracts key material, writes variants using 4-Layer Framework as generation guidance
- **Variant count:** Claude's discretion based on script material richness (same philosophy as Phase 68 title generation)
- **Style coverage:** Lead with recommended style for the topic type, then include variants in other styles for comparison
- **Variant length:** Claude's discretion based on style — cold_fact might need 3 sentences, myth_contradiction might need a full paragraph
- **Output:** Spoken text only — no [VISUAL] or [AUDIO] cues (those belong in /prep)
- **Every variant auto-scored** against the upgraded hook_scorer

### Style Recommendation (HOOK-02)
- **Display:** Recommendation banner at top of output with 2-3 first-sentence examples from HOOK-PATTERN-LIBRARY.md, shown before the score
- **Format:** "🎯 Topic type: territorial → Recommended style: cold_fact" + real examples with view counts
- **Score impact:** Confidence-based modifier — matching recommended style gives +5 when library has 7+ examples for that pattern, advisory-only when <5 examples. Mismatching gives -5 (high confidence) or no penalty (low confidence)
- **Topic-to-style mapping:** territorial → cold_fact, ideological → myth_contradiction, political_fact_check → specificity_bomb (per HOOK-PATTERN-LIBRARY.md topic distributions)

### Claude's Discretion
- Framework-to-score point distribution (anomaly/stakes/inciting incident within 40-point budget)
- Number of hook variants to generate (proportional to script richness)
- Variant length per style
- Urgency flag score thresholds
- Detection patterns for anomaly, stakes connection, and inciting incident in existing hooks
- Topic auto-detection keyword lists (extending Phase 67 pattern)

</decisions>

<specifics>
## Specific Ideas

- User's 4-Layer Framework for hook generation guidance:
  1. **"Document Reveal" Hook:** Start with specific, localized anomaly (line on map, single telegram, redacted sentence). Connect to massive systemic consequence. Inciting incident within 45 seconds.
  2. **"Human Cog" Characterization:** Define figures by professional background and lack of preparation. Focus on motivations: rushed, exhausted, under pressure.
  3. **Systemic Stakes (Physical Reality):** Translate abstract policy into physical resource consequences (water, food, logistics, movement). If a border moves, explain what valve it shuts off.
  4. **Retention Mechanics:** Setup → Quote/Document → Implication pattern. Pattern interrupts every 90 seconds.

- User's brand voice for generation: "Forensic, intelligent, skeptical. Bureaucratic Horror — high stakes hidden in dry documents, maps, and administrative failures."
- Influences: "Structural depth of Kraut + document-first rigor of Shaun"
- The "Document Reveal" framework should be the primary guidance when Claude generates hook variants

</specifics>

<code_context>
## Existing Code Insights

### Reusable Assets
- `tools/research/hook_scorer.py`: Existing scorer with score_hook(), rank_hooks(), format_hook_ranking(). Beat detection needs replacement; pattern_score, authority_score, gap_score dimensions can be kept/adapted
- `tools/research/hook_scorer.py`: `_detect_beats()` function — will be replaced with framework-based detection (anomaly, stakes, inciting incident)
- `.claude/REFERENCE/HOOK-PATTERN-LIBRARY.md`: 22 verified hooks across 4 patterns from 4 channels (100K+ subs). Structured for programmatic parsing
- `channel-data/niche-hook-patterns.md`: Same data with full first-sentence examples and view counts
- `tools/production/parser.py`: ScriptParser — parses markdown scripts into sections. Reusable for extracting opening hook text
- `tools/production/metadata.py`: EntityExtractor — extracts people, places, documents. Reusable for title entity extraction in fulfillment check
- `tools/title_scorer.py`: `detect_pattern()` — topic type detection via keywords. Same pattern for hook topic detection

### Established Patterns
- Phase 67's topic auto-detection via keyword matching in title_scorer.py — extend to script content
- Phase 68's TitleMaterialExtractor — extracts specific numbers, documents, contradictions from scripts. Same material useful for hook variant generation
- Scoring dimension pattern: beat_score + pattern_score + authority_score + gap_score = total. Fulfillment and style dimensions are additive

### Integration Points
- `/script --hooks` command → calls upgraded hook_scorer → output to terminal
- Title input via --title flag → used for fulfillment check
- HOOK-PATTERN-LIBRARY.md → read at runtime for style recommendation examples and confidence-based scoring
- script-writer-v2 Rule 19 → references hook patterns. Framework replacement should align with Rule 19 update

</code_context>

<deferred>
## Deferred Ideas

- **4-beat completeness check (HOOK-03):** Future requirement for verifying all 4 beats present — may need revisiting after framework replaces beats
- **"Authority stack" hook template (HOOK-04):** Multiple authorities believe myth, all wrong — specific template for future phase
- **[VISUAL]/[AUDIO] cue generation for hooks:** User explicitly deferred to /prep command, not hook generation
- **script-writer-v2 Rule 19 update:** Framework replacement in scorer should trigger corresponding update in script-writer-v2's hook writing guidance — separate task

</deferred>

---

*Phase: 69-hook-quality-upgrade*
*Context gathered: 2026-03-18*
