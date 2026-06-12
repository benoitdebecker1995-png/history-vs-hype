# WORKSPACE_RULES.md — Antigravity Rules Panel

> Load this file in Antigravity's **Rules** panel. Every agent (Content/Script, Fact-Check, Packaging, Asset, Analytics) inherits these constraints. Do not duplicate per-agent.

---

## 1. Identity & Scope

- **Project:** History vs Hype — evidence-based, myth-busting YouTube channel.
- **Audience:** Males 25–44, UK / DE / CA / US. Subscriber trigger = "intellectual competence" — explain *systems*, not narratives. HOW > WHY. Mechanism > politics.
- **Channel DNA:** History-first with modern relevance (60–80% historical, 20–40% modern hook). NOT geopolitics with historical background. Test every angle against: *"Will this matter in 10 years regardless of who is in power?"*
- **Format:** 8–12 minute hybrid talking-head + B-roll evidence. **Hard cap 12 minutes** (channel data: r = –0.455 duration↔retention, n=47).
- **Voice:** *"Calm Prosecutor"* — emotionally low, intellectually high. Evidence-based referee, never a partisan.

---

## 2. Hard Rules (never violate)

1. **PACKAGING-FIRST.** No research, scripting, or asset work begins until a topic passes `/greenlight`. Demand < 1K searches/mo = hard stop.
2. **Two-Phase Research is mandatory.** Phase 1 (internet landscape, marked ❓) and Phase 2 (NotebookLM academic verification, marked ✅) — never skip Phase 2. Phase 2 = the channel's competitive advantage.
3. **Academic sources only** for verification. University presses (Cambridge, Oxford, Chicago, Harvard, Yale), peer-reviewed (2010+), critical editions, primary documents. No Wikipedia in final script. No commentary YouTubers.
4. **Real quotes with page numbers.** *"Wickham, The Inheritance of Rome, p. 147"* — never *"historians say."* Paraphrase only if no primary source exists.
5. **Primary documents ON SCREEN.** Treaty page, manuscript, court ruling — visible to the viewer. This is the *auditor's edge.*
6. **No unverified claims in script.** If you cannot cite the source with page/timestamp, the claim does not enter `02-SCRIPT-DRAFT.md`. Hold it as ⏳ in `01-VERIFIED-RESEARCH.md` or drop it.
7. **Quality gates are blocking, not advisory:**
   - Gate 1 (Research → Script): ≥ 90% claims marked ✅
   - Gate 2 (Script → Film): 100% claims cross-checked in `03-FACT-CHECK-VERIFICATION.md`
8. **Title rules.** No year tokens (–46% CTR, n=47), no colons (–28%). Front-load search-anchor keyword. Mechanism word required (see `CONTEXT.md` → *Mechanism word*).
9. **Thumbnail rules.** Text overlay mandatory (2–4 words, not full title; verdict overlays *forbidden* — titles can declare, thumbnails must invite). No face on territorial videos. Maps for border/territorial topics. Real-material aesthetic > AI render.
10. **Folder lifecycle is law.** `_IN_PRODUCTION/` → `_READY_TO_FILM/` → `_ARCHIVED/published/`. Never create loose folders under `video-projects/`. Naming: `[number]-[slug]-[year]/`.

---

## 3. Content Safety & Editorial Constraints

- **No conspiracy framing** without primary-document support. If documentation is thin, the claim does not appear.
- **Acknowledge the opposing side's strongest point** before refuting (intellectual-honesty gate — Calm Prosecutor voice depends on this).
- **No absolutist language:** avoid *"X destroyed the culture,"* *"Z is occupying Y,"* *"the truth they don't want you to know."* These trigger demonetization risk and break the prosecutor voice.
- **Politically charged topics** (Israel/Palestine, Iran, Russia/Ukraine, China) require: (a) primary-source citation for every contested claim, (b) named-scholar attribution on screen, (c) modern stakes framed as state behavior, not ethnic/religious essentialism.
- **Define every technical term immediately** ("estoppel — a legal rule that…"). No jargon stranded.
- **Define-before-use** on first occurrence of any abbreviation, document title, or named figure.

---

## 4. Voice & Style (script-side)

- **Spoken delivery first.** Contractions (*it's*, not *it is*). Ordinal dates (*"On June 16th, 2014,"* not *"June 16, 2014."*). Lists with commas, not periods, when reading aloud.
- **Causal chains over assertions.** *Consequently, thereby, which meant that…* Explain WHY mechanically, not rhetorically.
- **No staccato fragment triplets.** *"Britain. France. Egypt."* fails the read-aloud test. Use connectors.
- **No filler "Here's"** beyond 2–4 uses per script.
- **Pattern interrupt every 2–3 minutes.** Visual document reveal, location shift, or numerical anchor.
- **Myth-first structure** for non-territorial videos (30.3% retention vs 22.4% for context-first, n=47).
- **Turn beat at 15–25% runtime** (3.2× lift). Avoid the 25–35% dead zone (2.1× — channel data).
- **Modern relevance touch every 90 seconds.**
- **Authoritative reference:** `.claude/REFERENCE/WRITING-VOICE-AND-STYLE.md` — read before any script work.

---

## 5. Tech Stack & Tooling Context

### Runtime
- **Python ≥ 3.11**, managed via `pyproject.toml` (hatchling). Install: `pip install -e .[all]`.
- **PowerShell** is the default shell (Windows 11). Bash available via Antigravity terminal. Use PowerShell syntax for env vars (`$env:VAR`) and null device (`$null`).
- **Working directory:** `d:\History vs Hype\`.

### Internal Python modules (`tools/`)
| Module | Purpose | Owner agent |
|---|---|---|
| `tools.discovery` | Topic demand, autocomplete mining, opportunity scoring | Packaging |
| `tools.production.title_generator` | Title scoring, mechanism-word enforcement | Packaging |
| `tools.production.broll`, `editguide` | B-roll planning, edit guides | Asset |
| `tools.script_checkers` | Pacing, flow, repetition, stumble, scaffolding | Script |
| `tools.research.nlm_ingest` | NotebookLM output → VERIFIED-RESEARCH | Research |
| `tools.citation_extractor` | Claim extraction from transcripts | Fact-Check |
| `tools.youtube_analytics` | Channel metrics, retention, CTR, comments | Analytics |
| `tools.intel` | Competitor patterns, algorithm synthesis | Analytics |
| `tools.translation.translator` | Untranslated-Evidence series clause-by-clause | Research |
| `tools.reconcile` | Folder-state drift detection | Analytics |
| `tools.routines` | Scheduled daily/weekly jobs | Analytics |

### External APIs / Tools
- **NotebookLM** (Gemini 2.0 Flash, 2M context) — academic verification. **MCP server operational (2026-05-18)** — use `mcp__notebooklm__*` tools in-session for Phase 2 verification; browser fallback and `tools/notebooklm_bridge.py` no longer needed for standard queries. Use `notebook-researcher` agent for structured research briefs.
- **VidIQ Pro** — keyword search volume + competition only. Other VidIQ features ignored.
- **YouTube Data API + Analytics API** — read-only. Credentials in `.env` (see `.env.example`).
- **Anthropic API** — used by `notebooklm_bridge.py` and select agents. Required dep.
- **Gemini CLI** — bulk reads (transcripts, source digestion). Flash by default; Pro requires explicit approval.
- **DaVinci Resolve** — editing (external). **Photoshop** — thumbnails (external).
- **analytics.db** — SQLite, source of truth for publish status. **Real path: `tools/youtube_analytics/analytics.db`** (143KB, 56 videos as of 2026-05-17). The root-level `analytics.db` is a 0-byte ghost — do not reference it. CTR is NOT in analytics.db; lives in `_ARCHIVED/published/<slug>/POST-PUBLISH-ANALYSIS.md`.

### Model routing (default to cheapest capable model)
- **Opus 4.7** — script lock, polish pass, newsletter writing, thesis discovery, complex reasoning chains.
- **Sonnet 4.6** — iterative drafting, slash-command execution, fact-check, lookups.
- **Haiku 4.5** — short structured passes (title scoring, claim extraction batches).
- **Gemini Flash** — bulk reads (transcripts, multi-document scans, NotebookLM-style triage).

---

## 6. Data Flow (canonical)

```
   /greenlight  ──►  passes? ──►  /research --new
       │                              │
       │ fails                        ▼
       └─► drop or reframe       01-VERIFIED-RESEARCH.md  (Phase 1: ❓)
                                      │
                          NotebookLM Phase 2 (academic)
                                      ▼
                                 01-... marked ✅ (≥90%)
                                      │
                                      ▼
                                 /script ──► 02-SCRIPT-DRAFT.md
                                      │
                                      ▼
                                 /verify ──► 03-FACT-CHECK-VERIFICATION.md
                                      │
                                  100% pass?
                                      ▼
                                 FINAL-SCRIPT.md  +  YOUTUBE-METADATA.md
                                      │
                                      ▼   (move folder)
                          _READY_TO_FILM/<slug>/
                                      │
                                  filming + edit (DaVinci)
                                      ▼
                                 /editing-guide  /fix  /publish
                                      ▼   (on upload — user says "I uploaded X")
                                  /reconcile <slug>
                                      ▼
                          _ARCHIVED/published/<slug>/
                                      │
                                analytics.db updated
                                      ▼
                            /analyze  /patterns  /growth
```

**Single source of truth per project:** `01-VERIFIED-RESEARCH.md`. Anything not in it cannot appear in the script.

---

## 7. Multi-Agent Coordination (Antigravity-specific)

- **Parallel agents must not write to the same file simultaneously.** Use the agent-ownership table in `ANTIGRAVITY_MIGRATION.md` § 4. Lock = file ownership, not Git lock.
- **Cross-agent handoff is via Artifacts.** When Agent A finishes a phase, emit an Antigravity Task List entry with `OUTPUT: <absolute-path>` as the final line of the artifact summary. The next agent picks up by reading that path.
- **Memory is per-workspace, not per-agent.** Memory directory: `C:\Users\Benoi\.claude\projects\d--History-vs-Hype\memory\`. All agents read `MEMORY.md` (index) on cold start.
- **No agent silently spawns a sub-agent.** If you need delegation, declare it in the Implementation Plan first.

---

## 8. Reconciliation (folder-state drift)

- **Truth sources:** filesystem (lifecycle stage), `analytics.db` (publish status), per-folder `PROJECT-STATUS.md` (narrative).
- **Trigger phrases:** user says *"I uploaded X" / "X is live" / "X went up"* → run `/reconcile <slug>` immediately. The utterance IS the write trigger — do not assume project files are current.
- **AUTO blocks:** top of each `PROJECT-STATUS.md` between `<!-- AUTO:reconcile -->` and `<!-- /AUTO:reconcile -->` is machine-managed. Anything below is hand-written, never overwritten.
- **Daily backstop:** Routine 6 runs 08:30, archives newly-published videos missed by conversation. Routine 6 NEVER touches memory snapshots — lessons-promotion stays gated on interactive `/reconcile`.

---

## 9. Coding Style (for `tools/` Python work)

- **Stdlib + typed.** Type-hint every public function. No `Any` without justification.
- **No new dependencies without updating `pyproject.toml`** and the relevant optional-extra group.
- **Tests live in `tests/`.** New modules ship with at least one happy-path test. Use `pytest`.
- **No silent fallbacks.** If an API key is missing, raise with a clear remediation message. Mocks belong in tests, never in production paths.
- **PowerShell-safe paths.** Use `pathlib.Path` and forward slashes in source; never hard-code `C:\` paths outside of `.env`.
- **No new code in `_DEPRECATED/`, `_ARCHIVE/`, `_tmp_*`, `.pre-diff`** files. Treat as read-only.

---

## 10. What NOT to do (anti-patterns from prior incidents)

- Do not generate titles with year tokens or colons.
- Do not skip Phase 2 NotebookLM verification "because the topic is obvious."
- Do not analyze Shorts with `/analyze` — the tool is long-form only.
- Do not apply channel-specific patterns where n < 30 as hard constraints. They are informational. Niche-wide patterns (n=42+) are actionable. See memory: *Channel Data Not Actionable*.
- Do not paraphrase blockquotes in script — must be word-for-word from primary source with page number.
- Do not write CTAs from generic templates — must reference this video's specific value.
- Do not call NotebookLM Phase 2 "verified" without round-tripping the exact blockquote text and page number.
- Do not act on a memory record without verifying the underlying file/state still exists.
- Do not run destructive Git operations (`reset --hard`, `push --force`, branch deletion) without explicit user confirmation.

---

## 11. References (load on demand, not into every context)

- `CLAUDE.md` — legacy Claude Code instructions (still source of truth for editorial rules).
- `AGENTS.md` — legacy multi-tool agent doc.
- `CONTEXT.md` — domain glossary (terminology lockdown).
- `.claude/REFERENCE/WRITING-VOICE-AND-STYLE.md` — authoritative style.
- `.claude/REFERENCE/THESIS-DISCIPLINE.md` — 9-step throughline procedure.
- `.claude/REFERENCE/fact-checking-protocol.md` — source-tier hierarchy.
- `.claude/REFERENCE/NOTEBOOKLM-SOURCE-STANDARDS.md` — Phase 2 source bar.
- `.claude/REFERENCE/TITLE-GENERATION-PROTOCOL.md` — packaging rules.
- `tools/PACKAGING_MANDATE.md` — packaging-first enforcement.
- `channel-data/CONTENT-TIMELINE-2026.md` — release cadence.
- `ANTIGRAVITY_MIGRATION.md` — this workspace's handoff plan.

---

**Last updated:** 2026-05-18 (NotebookLM MCP operational)
