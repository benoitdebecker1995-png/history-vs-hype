# NotebookLM MCP Tools — Implementation Plan

**Created:** 2026-03-29
**Status:** APPROVED — waiting for prioritization against other channel initiatives
**Trigger:** NotebookLM MCP server connected (notebooklm-mcp-cli v0.5.11)

---

## What We Have

- 47 NotebookLM notebooks with 800+ academic sources
- MCP integration: can query, create, add sources, generate artifacts programmatically
- Cross-notebook query capability (tested — works across 4+ notebooks simultaneously)
- Pipeline automation (ingest-and-podcast, research-and-report, multi-format)

## 3 Tools to Build (in `tools/notebooklm/`)

### Tool 1: Cross-Notebook Intelligence (`cross_query.py`)

**Purpose:** Query across all 47 notebooks to find cross-topic connections, shared documents, and recurring legal patterns.

**Commands:**
```
python -m tools.notebooklm.cross_query "What legal precedent connects these colonial treaties?"
python -m tools.notebooklm.source_reuse --topic "Falklands Malvinas"
```

**Use cases:**
- Find which existing notebook sources apply to a new topic (saves weeks of PDF re-downloading)
- Generate "connection briefs" showing how topics link across centuries
- Feed meta-content format: "Every Colonial Treaty Uses the Same 3 Legal Tricks"

**Content unlock:** Videos pulling verified quotes from 6+ notebooks with page numbers. No competitor can do this.

### Tool 2: Automated Phase 2 Verification (`verify.py`)

**Purpose:** Semi-automate the NotebookLM Phase 2 research workflow.

**Command:**
```
python -m tools.notebooklm.verify --project 44-bakassi-peninsula-2026
```

**Process:**
1. Reads Phase 1 preliminary research (claims marked ❓)
2. Identifies the corresponding NotebookLM notebook
3. Runs battle-tested verification prompts from NOTEBOOKLM-RESEARCH-PROMPTS.md
4. Outputs draft 01-VERIFIED-RESEARCH.md with citations and page numbers
5. Flags claims that couldn't be verified

**Time savings:** Phase 2 from 1-2 weeks → 1-2 days of human review.

### Tool 3: Untranslated Document Finder (`untranslated_finder.py`)

**Purpose:** Scale the "Untranslated Evidence" series by systematically finding documents.

**Command:**
```
python -m tools.notebooklm.untranslated_finder --scan-all
```

**Process:**
1. Queries all notebooks for untranslated/under-translated primary documents
2. Cross-references with discovery DB search demand
3. Ranks by: (a) never translated on YouTube + (b) search demand exists
4. Feeds into /greenlight gate

---

## Integration Points

- Wire `verify` into `/research` command for Phase 2 automation
- Wire `cross_query` into `/script` for cross-topic connection suggestions
- Wire `untranslated_finder` into `/greenlight` for series episode selection

## Proven Test

Cross-notebook query tested 2026-03-29: pulled connections between Haiti, Doctrine of Discovery, Africa, and Bakassi notebooks — returned structured results with source citations across 3 notebooks successfully.

## Strategic Value

The competitive moat is the interconnected academic graph. Individual videos are well-researched but isolated. The cross-notebook capability reveals patterns:
- Same "effective occupation" doctrine in Berlin 1884, Bakassi, Belize, AND Tordesillas
- Same Vienna Convention articles in every ICJ ruling covered
- Same French legal structure in Haiti debt, Code Noir, AND Vichy laws

Meta-content from this graph = the "intellectual competence" that VidIQ data says drives subscriptions.
