# Phase 54: External Intelligence Synthesis - Context

**Gathered:** 2026-02-26
**Status:** Ready for planning

<domain>
## Phase Boundary

Automate the VidIQ/Gemini metadata workflow: prompt generation from script analysis, response intake parsing, synthesis into ranked metadata packages with moderation scoring, and Photoshop-ready thumbnail blueprints. Manual workflow for Gibraltar (#35) and Vichy (#37) took ~2 hours each — this phase automates the repeatable parts.

</domain>

<decisions>
## Implementation Decisions

### Prompt Generation Style
- **Hybrid approach:** Deep script analysis for VidIQ keyword prompts (needs specificity), template-based for Gemini creative prompts (works better with less constraint)
- **Channel context:** Frame as a channel with no audience yet — avoid advice calibrated for established channels
- **VidIQ target:** All VidIQ prompts target the **VidIQ Pro Coach chat function** (not Keyword Inspector or other tools separately)
- **Gemini scope:** Claude's discretion on what Gemini is best at — use it for whatever it excels at (likely creative ideation, hook angles, audience psychology)
- **Competitor context:** Include competitor data from `/intel` (intel.db) to ground prompts in what works in the niche
- **Don't include:** Channel's own proven patterns — let tools give fresh perspective without bias
- **Auto-detect script length:** If script fits VidIQ char limit → include full hook/intro text. If too long → auto-generate topic summary with key entities and claims
- **Sequenced workflow:** Numbered steps with clear order — each prompt builds on previous response. Copy-paste ready with instructions (e.g., "Paste this into VidIQ Pro Coach. Copy the full response.")
- **VidIQ prompt count:** Claude's discretion on number and focus areas based on VidIQ Pro Coach capabilities
- **Focused for VidIQ, single for Gemini:** Multiple focused prompts for VidIQ, one comprehensive creative brief for Gemini
- **Output saved to:** `EXTERNAL-PROMPTS.md` in the video project folder
- **Prompt versioning:** Automatic from intake quality — system infers prompt effectiveness from how much of the response was parseable/useful. No manual rating.

### Intake Parsing
- **Input method:** Copy-paste raw text directly into `/publish --intake`
- **Auto-detection:** Parser identifies whether pasted text is keyword data, title suggestions, thumbnail concepts, etc. based on content patterns (no manual labeling)
- **Session flow:** One paste at a time with confirmation — system parses, confirms what it extracted, then prompts for next paste
- **Storage:** JSON file (`EXTERNAL-INTELLIGENCE.json`) in the video project folder — structured data for synthesis engine

### Synthesis Ranking
- **Conflict resolution:** Weigh each source by what it's good at, present recommendations with reasoning, let user decide
- **Primary output:** 3 distinct title+thumbnail pairings designed for A/B testing
- **Variant labeling:** Each variant labeled by test hypothesis (e.g., "Variant A: Keyword-optimized", "Variant B: Curiosity gap", "Variant C: Authority angle")
- **Full metadata package:** 3 title+thumbnail pairings PLUS one optimized description and one tag set — complete publish-ready package
- **Integration:** Complements existing `/publish --titles` workflow — adds external intelligence as additional input, doesn't replace it
- **Cross-project learning:** None for now — each project independent. Too early (462 subs) for meaningful pattern data from synthesis specifically.

### Content Moderation Scoring
- **Scope:** Full metadata moderation — titles, description, tags, AND thumbnail concepts
- **Inline with blueprints:** Each thumbnail variant includes moderation risk notes (e.g., "Variant B uses Holocaust imagery: high demonetization risk")
- **Safe alternatives:** Flag trigger words/imagery and suggest alternatives

### Thumbnail Blueprints
- **Detail level:** Concept + composition guide — describes concept, visual layout (thirds, focal points), color palette, text overlay suggestions, asset types needed
- **Matched to variants:** Each of the 3 thumbnail blueprints matched to its paired title variant (same angle, coherent A/B test)
- **No asset sourcing:** Just describe what's needed, don't source specific URLs
- **Text overlay guidance:** Include text placement, approximate word count, font style direction, and contrast approach per variant
- **Mobile considerations:** Claude's discretion
- **Channel patterns:** Don't enforce (e.g., map-focused) — treat each project fresh

### AI Thumbnail Generation
- **Per-element guidance:** Each blueprint element tagged as AI-generatable or manual Photoshop work
- **Available tools:** VidIQ image generator + Napkin AI (Nanobanna)
- **AI element scope:** Claude's discretion per project based on topic sensitivity (e.g., Holocaust topics may need real photos only)
- **Copy-paste prompts:** Include ready-to-paste image generation prompts for VidIQ/Napkin for each AI-generatable element

</decisions>

<specifics>
## Specific Ideas

- VidIQ Pro Coach has a character limit — prompts must be aware of this and auto-adapt (full script text for short hooks, topic summaries for long scripts)
- User tests 3 titles paired with 3 thumbnails to gather data — synthesis output must produce exactly 3 coherent pairings
- Prompt versioning is automatic: track which prompt templates produce more parseable/useful responses over time, evolve templates accordingly
- The whole point is reducing the ~2 hour manual metadata workflow to a streamlined prompt-paste-synthesize flow

</specifics>

<deferred>
## Deferred Ideas

- Cross-project learning from synthesis recommendations vs actual CTR/view performance — revisit when channel has more data
- Photoshop Generative Fill integration — user doesn't currently use it
- Screenshot/OCR intake from VidIQ — copy-paste is sufficient for now

</deferred>

---

*Phase: 54-external-intelligence-synthesis*
*Context gathered: 2026-02-26*
