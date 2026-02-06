---
description: Source recommendations, NotebookLM prompts, and citation formatting (Pre-production Phase 2)
model: haiku
---

# /sources - Source Management Entry Point

Get source recommendations, generate NotebookLM prompts, or format citations. This command consolidates all source-related workflows.

## Usage

```
/sources                     # Interactive: asks what you need
/sources --recommend [topic] # Get academic source recommendations
/sources --prompts [topic]   # Generate NotebookLM research prompts
/sources --format [sources]  # Format source list for video description
```

## Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `--recommend` | Get 20-30 academic source recommendations | `/sources --recommend "Library of Alexandria"` |
| `--prompts` | Generate NotebookLM verification prompts | `/sources --prompts 19-flat-earth-medieval-2025` |
| `--format` | Format sources for YouTube description | `/sources --format` |
| `--all` | Full workflow: recommend → prompts → format | `/sources --all [topic]` |

---

## SOURCE RECOMMENDATIONS (`--recommend`)

Generate 20-30 authoritative sources (up to 50 if essential) organized by tier.

### Output Structure

**Tier 1: Recent Comprehensive Works (2010-present)**
- Modern consensus scholarship
- Prioritized for currency

**Tier 2: Primary Source Collections**
- Critical editions with scholarly apparatus
- Timeless evidentiary value

**Tier 3: Classic Works (pre-2010)**
- Foundational scholarship
- Flag: "Verify against recent scholarship"

**Tier 4: Contemporary Analysis**
- Modern relevance connections (2023-2026)
- News hooks, current events

**Tier 5: Counter-perspective**
- Strongest academic rebuttals
- Specific scholars and page numbers
- Steel-manned opposing views

**Tier 6: Historical Context**
- Background reading
- Broader context sources

### For Each Source

- **Title and author** with credentials
- **Why essential:** What research gap it fills
- **Publication date:** 2010+ prioritized
- **Page ranges:** For key claims (needed for YouTube citations)
- **Acquisition:** University library / purchase / interlibrary loan
- **Preview link:** If available

### Academic Quality Standards

**MANDATORY (from NOTEBOOKLM-SOURCE-STANDARDS.md):**
- University press publications ONLY (Cambridge, Oxford, Chicago, Harvard, Yale)
- Top-tier scholars (leading authorities, endowed chairs)
- Critical editions for primary sources
- **Budget is UNLIMITED** - recommend best sources regardless of price

### ⛔ QUALITY GATE: Academic Source Verification

**BEFORE generating any source list, Claude MUST verify:**

| Check | Requirement | Fail Action |
|-------|-------------|-------------|
| Primary Sources | 3+ treaties/court rulings/official documents | Add more before proceeding |
| Academic Sources | 3+ university press books OR peer-reviewed articles | Add more before proceeding |
| Wikipedia/News | NOT listed as academic citations | Remove or move to "Reference Only" |
| Think tanks | Listed as "Expert/Policy" NOT "Academic" | Reclassify |

**Source list header MUST include this table:**

```markdown
## SOURCE QUALITY CHECK

| Requirement | Status |
|-------------|--------|
| 3+ Primary Sources | ✅/❌ [count] identified |
| 3+ University Press Academic Sources | ✅/❌ [count] identified |
| Total 10+ Sources | ✅/❌ [count] sources |
| Wikipedia/News as citations | ❌ Excluded (reference only) |
```

**If any check fails:** Do NOT proceed. Add required sources first.

**Acceptable Academic Publishers:**
- Cambridge University Press
- Oxford University Press
- University of Chicago Press
- Harvard University Press
- Yale University Press
- Princeton University Press
- Palgrave Macmillan (academic imprint)
- Routledge (academic titles)
- Cornell University Press
- University of [State] Press
- Museum Tusculanum Press (Nordic)

**NOT Academic Sources (move to Expert/Policy or Reference):**
- CSIS, Brookings, Atlantic Council, CFR → "Expert/Policy Sources"
- DIIS → "Research Institute" (acceptable but not primary academic)
- Wikipedia, news articles → "Reference Only - NOT for NotebookLM"
- Library of Congress blogs → "Government Analysis"

### Output Location

`video-projects/[project]/_research/00-NOTEBOOKLM-SOURCE-LIST.md`

Or if standalone: `research/[topic]-SOURCE-RECOMMENDATIONS.md`

---

## NOTEBOOKLM PROMPTS (`--prompts`)

Generate customized prompts for NotebookLM verification.

### What You Get

**Core Research Prompts:**
1. **Topic-Specific Organization** - Extract evidence for exact thesis
2. **Smoking Gun Evidence** - Find quotes/documents that prove the case
3. **Counter-Evidence Analysis** - Strongest scholarly rebuttals (steel-manned)
4. **Modern Relevance Mapping** - Connect history to current impact
5. **Pattern Recognition** - Identify 3+ interconnected incidents
6. **Script Hook Generation** - Most compelling opening hooks

**Fact-Checking Prompt:**
- Customized for script's specific claims (once written)

**B-Roll Shot List Prompt:**
- Visual evidence needs for the topic

### Prompt Requirements

Each prompt is:
- Copy-paste ready for NotebookLM
- Optimized for length limits
- Designed to extract specific evidence
- Requests page numbers (required for YouTube)
- Prioritizes 2010-present sources
- Requests counter-evidence

### NotebookLM Features to Leverage

**Gemini 2.0 Flash capabilities:**
- 2M token context window (50 sources, 25M words)
- Customized Audio Overviews (click "Customize" before generating)
- Interactive Mode (talk with podcast hosts)
- Citation grounding (clickable page numbers)
- Study guides for dense academic texts

### Input Needed

1. **Topic and thesis:** What myth are you debunking?
2. **Sources uploaded:** What's in NotebookLM? (Or use `/sources --recommend` first)
3. **Specific questions:** Any particular aspects to focus on?

### Output Location

`video-projects/[project]/_research/02-NOTEBOOKLM-PROMPTS.md`

---

## SOURCE FORMATTING (`--format`)

Format source list for YouTube video description.

### Process

1. **Get sources:** From script, research, or manual list
2. **Categorize:** Group by type
   - Primary Documents (treaties, census, archives)
   - Academic Monographs
   - Peer-reviewed Articles
   - News/Contemporary Analysis
3. **Verify URLs:** Test each link
   - ✅ Working
   - ❌ Broken (provide alternative)
   - ⚠️ Paywalled (note it)
4. **Format:** Copy-paste ready for YouTube description

### Output Format

```markdown
SOURCES:

**Primary Documents:**
- [Document Name] ([Year]) - [Archive/Location]
  Link: [URL]

**Academic Sources:**
- [Author], *[Title]* ([Year]), pages [X-Y]
  Link: [URL or "Available via university library"]

**News & Contemporary:**
- "[Article Title]" - [Publication] ([Date])
  Link: [URL]
```

### Output Location

`video-projects/[project]/[topic]-SOURCES.md` or added to `YOUTUBE-METADATA.md`

---

## FULL WORKFLOW (`--all`)

Run complete source workflow:

1. Generate source recommendations
2. User downloads and uploads to NotebookLM
3. Generate NotebookLM prompts
4. User runs prompts and collects responses
5. Format final source list

**Best for:** Starting a new topic from scratch

---

## Integration with Research Workflow

### Typical Sequence

```
/research --new [topic]     # Creates project, preliminary research
/sources --recommend        # Gets academic sources to download
[User downloads sources, uploads to NotebookLM]
/sources --prompts          # Generates verification prompts
[User runs prompts, updates 01-VERIFIED-RESEARCH.md]
/script                     # Ready when 90%+ verified
```

### Quality Gate Connection

Sources feed into 01-VERIFIED-RESEARCH.md which must be 90%+ verified before scripting. The `/sources` command provides the tools to reach that verification threshold.

---

## Reference Files

- **Source standards:** `.claude/REFERENCE/NOTEBOOKLM-SOURCE-STANDARDS.md`
- **NotebookLM prompts guide:** `.claude/REFERENCE/NOTEBOOKLM-SCRIPTWRITING-PROMPTS.md`
- **Research template:** `.claude/templates/01-VERIFIED-RESEARCH-TEMPLATE.md`

---

## Absorbed Commands

This command consolidates functionality from:
- `/suggest-sources` - Academic source recommendations
- `/notebooklm-prompts` - NotebookLM prompt generation
- `/format-sources` - Source citation formatting

All original functionality preserved through flags and workflow stages.
