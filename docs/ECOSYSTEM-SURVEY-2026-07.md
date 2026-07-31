# Community ecosystem survey — what's worth merging into this repo

**Date:** 2026-07-31 · **Status:** survey only, nothing installed · **Scope:** GitHub skills,
agents, plugins and tooling for Claude Code, assessed against this repo's verified gaps.

---

## The headline finding

**The Claude Code ecosystem is large and almost entirely irrelevant to this channel.**

That is not a shrug — it's the result, and it saves re-running this search. The biggest curated
collection, [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)
(~1000+ skills, including official sets from Anthropic, Google, Stripe, Microsoft, Figma,
Cloudflare), was checked directly for research, fact-checking, citation, historical/academic,
and document-evidence coverage. Verbatim result:

> Research, Fact-Checking, Citations: **Not found.** No dedicated skills for academic citation
> management, fact-verification, or research workflows.
> Historical/Academic Work: **Not present.** The collection focuses on development and operations
> rather than humanities scholarship.

Everything downstream follows from that. The ecosystem optimises for software teams. This repo is a
history channel's evidence pipeline that happens to be built in Python, and it is already further
along in its own domain than anything on offer — 11 skills, 13 agents, 34 commands, 21 ADRs, a
golden-set eval harness, enforced storage seams.

So: **three** candidates are worth anything, and one of those is a packaging format rather than
content.

---

## Adoption criteria

Applied to every candidate below.

1. Does it serve **evidence-on-screen**, **packaging**, or **research verification** — the three
   things that actually move this channel? If not, reject regardless of star count.
2. Does an existing surface already carry it? (`extending-safely`'s three-grep test.)
3. Licence and provenance — adoptable at all, and is the source credible?
4. Maintenance cost, and who is the named caller?

---

## ADOPT — 1 candidate

### `dougwyu/claude-zotero-skills` — Apache 2.0

The only candidate found that directly serves the channel's stated competitive advantage ("real
quotes with page numbers"). Three skills:

| Skill | What it does |
|---|---|
| `zotero-skill` | Queries the Zotero SQLite DB — author/year/keyword, collections — **verifies citation faithfulness by opening the cited PDF and checking the claim is actually supported**, surfaces annotations |
| `zotero-notes-import` | Imports structured reading notes into Zotero, matched on author + year |
| `manuscript-audit-skill` | Four-pass review: citation faithfulness, gap detection, logical consistency, copyediting |

**Why it matters here.** Faithfulness verification is currently manual, done through NotebookLM
query-by-query. This is the same discipline, automated, against a local library — and it reads the
PDF rather than trusting an index. `manuscript-audit-skill`'s four passes map closely onto `/verify`
and `03-FACT-CHECK-VERIFICATION.md`.

**The honest catch:** it assumes a Zotero library, and this workflow is NotebookLM-based. Adopting
it wholesale means adopting Zotero. **The technique is separable from the tool** — SQLite-backed
source index + `pdfplumber` open-and-check + a faithfulness pass is implementable against the
existing sources without Zotero at all. That is the recommended read: **adapt the method, don't
install the skill**, unless the owner wants a reference manager anyway.

Requirements if adopted as-is: Zotero 6/9, Python 3.11+, `pdfplumber`. Licence is clean.

---

## ADAPT (reference only — licence blocks copying)

### `anthropics/skills` — the `pdf` skill

Extract text and tables, OCR scanned pages, handle form fields, create PDFs. It maps onto a
**verified gap**: `grep` finds **zero** modules in `tools/` importing any PDF library, while
on-screen primary-source documents are the channel's non-negotiable. All of the Bengal exhibit work
(OCR of the Famine Commission report, page rendering, 25 exhibit PNGs) was done ad hoc and left
nothing reusable behind.

> ⚠ **Licence:** most of `anthropics/skills` is Apache 2.0, but the document skills — `docx`, `pdf`,
> `pptx`, `xlsx` — are explicitly **source-available, NOT open source**. Readable as reference;
> not copy-paste. The repo also states they are "for demonstration and educational purposes only."

**Recommendation:** read it as a design reference for a small in-repo `tools/production/exhibits.py`
(render page N of a PDF at a given DPI, extract text with a locator, emit an exhibit PNG + caption).
That closes the gap with code this repo owns, under this repo's conventions, with no licence
question. Named caller: `/prep` and the `primary-source-hunter` agent.

---

## CONSIDER — packaging, not content

### Plugin + marketplace format ([official docs](https://code.claude.com/docs/en/plugin-marketplaces))

There is **no `.claude-plugin/`** here; the 11 skills / 13 agents / 34 commands are local-only and
sync between machines by committing the whole repo. The supported alternative:

```
my-marketplace/
  .claude-plugin/marketplace.json        # registry: name, owner, plugins[] with source
  plugins/<name>/.claude-plugin/plugin.json
  plugins/<name>/skills/<skill>/SKILL.md
```

A plugin can bundle skills, agents, hooks, MCP servers and LSP servers together; sources may be a
relative path (`"./plugins/x"`) or a git repo. Installed plugins are cached at
`~/.claude/plugins/cache`.

**Verdict: real but not urgent.** git-based sync already works and the owner deliberately relies on
it. The case for packaging is portability and versioning, not a current problem — and it would add
a second place where skills live, which is the failure mode `extending-safely` warns about. Worth
doing only if the skills are ever shared outside this repo.

---

## ADOPT (as a source, not a tool) — the anti-AI-slop cluster

**Added 2026-07-31 after the owner asked why this wasn't covered. He was right — the first pass
searched research/infrastructure and missed the cluster aimed at the channel's actual #1 content
problem ("scripts feel AI").**

There is a whole genre here: [xr0zv/no-ai-slop](https://github.com/xr0zv/no-ai-slop),
[jalaalrd/anti-ai-slop-writing](https://github.com/jalaalrd/anti-ai-slop-writing),
[adewale/anti-slop-writing](https://github.com/adewale/anti-slop-writing),
[hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop),
[conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing),
[petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop),
[realrossmanngroup/no_ai_slop_writing_rules](https://github.com/realrossmanngroup/no_ai_slop_writing_rules),
[Byk3y/no-slop](https://github.com/Byk3y/no-slop).

### Do NOT adopt their rule lists wholesale — architecture forbids it

`tools/voice_lint.py` carries ~40 rules and says so explicitly: *"This tool does NOT invent voice
rules — it mechanizes the profile's hard 'no' list."* Rules derive **from**
`.claude/REFERENCE/VOICE-PROFILE.md` (527 lines, built from the owner's own rejections, each rule an
approved line plus a rejected counter-example), never the reverse — that is ADR-0006. Bulk-importing
a stranger's banned-word list inverts the arrow and would corrupt a personal fingerprint with
generic advice.

Two claims also failed inspection, which is why the whole genre gets judged as a *source* not a tool:

- The Rossmann repo is widely described as carrying "a data-driven voice profile built from corpus
  analysis of 513,683 words." **Its actual SKILL.md documents no such thing** — reading it directly:
  no corpus methodology, no training-data source, no derivation. It is 24 rules and banned-word
  lists. It also **specifies no licence**, so it is not adoptable regardless.
- Most of the others are constraint prompts, not runnable linters, and emit no machine-readable
  findings — so they cannot gate anything the way `voice_lint` does.

### The genuinely valuable find: Wikipedia's *Signs of AI writing*

[`Byk3y/no-slop`](https://github.com/Byk3y/no-slop) (MIT, 13 patterns, 40+ banned words) is the only
one that names a real, checkable provenance: every rule derives from
[**Wikipedia:Signs of AI writing**](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing),
maintained by WikiProject AI Cleanup from patterns observed across thousands of AI-generated texts.
Verified directly: seven categories (content, language/grammar, style formatting, communication
patterns, markup, citations, edit summaries), citing peer-reviewed 2025 detection studies and
tracking how tells shift between LLM versions.

That is a **collaboratively maintained, evidence-based, citable catalogue** — the same standard this
channel demands of its historical sources. It is a far better input than any one developer's list.

**Recommendation.** `voice_lint`'s 40 rules cover the tells the owner *noticed and rejected*. Tells
he never had to reject — because they never survived to reach him, or he never named them — are
invisible to it by construction. So:

1. Mine *Signs of AI writing* for tells absent from `VOICE-PROFILE.md`.
2. Put the survivors **into the profile first**, as a clearly separate "generic LLM tells" tier
   distinct from his personal fingerprint, so ADR-0006's arrow still points the right way.
3. Re-derive `voice_lint` from the profile. Ship them **WARN**, never HARD — the existing
   fingerprint-derived thresholds already ship WARN because they are single-sample, and generic
   rules deserve no more authority than that.

Named caller: `/polish`, which already exists for exactly this pass.

**One caveat worth stating plainly:** several of these lists ban the em dash outright, and blanket
bans are how a voice gets flattened. `VOICE-PROFILE.md` records that his lines get "eaten by
tidying, not by bad writing" — a generic tidy-up list is precisely that failure mode. Import the
tells, not the aesthetics.

---

## REJECT — and why, so this isn't re-researched

| Candidate | Reason |
|---|---|
| Any community **eval harness** | The repo is ahead of them. `EVAL-RUBRIC.md`, `EVAL-GOLDEN-SET.md`, `EVAL-JUDGE-PROTOCOL.md`, `EVAL-BASELINE.md` plus `tests/unit/test_eval_harness.py` run golden-set assertions against locked scripts. Nothing found improves on that. |
| [`VoltAgent/awesome-agent-skills`](https://github.com/VoltAgent/awesome-agent-skills) | ~1000+ skills, **zero** research/fact-check/citation/humanities coverage. Video: only `remotion` (programmatic React video) and an AI video editor — neither fits a talking-head + B-roll workflow. |
| [`VoltAgent/awesome-claude-code-subagents`](https://github.com/VoltAgent/awesome-claude-code-subagents), [`0xfurai`](https://github.com/0xfurai/claude-code-subagents), [`rshah515`](https://github.com/rshah515/claude-code-subagents) (100–133 agents each) | Generic SDLC roles — `backend-architect`, `code-reviewer`, `devops`. Wrong domain. Adopting them would dilute a 13-agent set where every agent has a named caller and a return contract. |
| [`rohitg00/awesome-claude-code-toolkit`](https://github.com/rohitg00/awesome-claude-code-toolkit), [`jeremylongshore/claude-code-plugins-plus-skills`](https://github.com/jeremylongshore/claude-code-plugins-plus-skills) | Aggregators of the above. Volume, not fit. |
| `Galaxy-Dawn/claude-scholar`, `imbad0202/academic-research-skills` | Aimed at producing papers — ideation → experiments → publication. This channel consumes scholarship, it doesn't publish it. `notebook-researcher` + `primary-source-hunter` already cover the consuming half, and better, because they enforce on-screen provenance. |
| Anthropic `docx` / `pptx` / `xlsx` | No workflow need, and the same source-available licence limit. |

---

## What this actually points at

The two real gaps found are **not** things to install — they're things to build small and own:

1. **A PDF/exhibit module.** The single clearest gap: zero PDF tooling behind a workflow whose
   whole claim is documents on screen. ~150 lines, modelled on the Anthropic `pdf` skill's approach,
   in `tools/production/`.
2. **A faithfulness pass that opens the source.** The Zotero skill's core move — don't trust the
   index, open the PDF and check the claim is on the page — is exactly the discipline
   `.claude/skills/primary-source/` describes in prose but nothing enforces in code. This is the
   natural successor to `claim_status.py`'s ladder: `INSPECTED` could become machine-checkable.

Both are extensions of surfaces that already exist, which is the outcome `extending-safely` asks for.

---

## Sources

- [anthropics/skills](https://github.com/anthropics/skills)
- [dougwyu/claude-zotero-skills](https://github.com/dougwyu/claude-zotero-skills)
- [Zotero Research Agent](https://mcpmarket.com/tools/skills/zotero-research-agent)
- [Claude Code plugin marketplace docs](https://code.claude.com/docs/en/plugin-marketplaces)
- [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)
- [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)
- [rohitg00/awesome-claude-code-toolkit](https://github.com/rohitg00/awesome-claude-code-toolkit)
- [jeremylongshore/claude-code-plugins-plus-skills](https://github.com/jeremylongshore/claude-code-plugins-plus-skills)
- [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)
- [Galaxy-Dawn/claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar)
- [imbad0202/academic-research-skills](https://github.com/imbad0202/academic-research-skills)
- [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [Byk3y/no-slop](https://github.com/Byk3y/no-slop) · [xr0zv/no-ai-slop](https://github.com/xr0zv/no-ai-slop) · [jalaalrd/anti-ai-slop-writing](https://github.com/jalaalrd/anti-ai-slop-writing) · [adewale/anti-slop-writing](https://github.com/adewale/anti-slop-writing) · [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) · [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) · [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop) · [realrossmanngroup/no_ai_slop_writing_rules](https://github.com/realrossmanngroup/no_ai_slop_writing_rules)
