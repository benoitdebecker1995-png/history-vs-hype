# Skill Library Index

> Built 2026-07 as a knowledge-transfer library: everything a cold session (any model class)
> or a new engineer needs to debug, extend, validate, and advance this project at standard.
> Build record + review trail: `docs/SKILL-LIBRARY-BUILD-2026-07.md`.
> House rule for these files: skills own only knowledge written nowhere else — they route to
> ADRs/REFERENCE/commands for everything that has an authoritative home. If you change a fact
> a skill states, grep the library for it (facts are cross-referenced deliberately).

**Cold session? Read `project-onboarding` first. It routes to everything below.**

| Situation | Skill |
|---|---|
| New here / unsure where to look / "how is this organized?" | **project-onboarding** |
| Where does X live · what depends on Y · how do I run tool Z | **codebase-atlas** |
| Querying/citing analytics.db, keywords.db, intel.db · stale data · AUTO zones | **data-stores** |
| Something broke, failed, stale, or "didn't run" · weird task result codes | **debugging-playbook** |
| Scheduled tasks · hooks · MCP servers · re-auth (NLM/VidIQ/YouTube) | **automation-ops** |
| About to change code · new module/command/skill · committing · spawning agents | **extending-safely** |
| Writing/editing a SKILL.md, command, or agent · a skill reads vague or won't fire | **authoring-skills** (craft; defers the should-it-exist gate to extending-safely) |
| Running tests · "is this done/verified?" · building a checker or gate | **validation-standards** |
| Video pipeline: which command next · packaging gates · "I uploaded X" / "script locked" | **production-map** |
| Active historical research: NLM queries, filing claims, source discipline | **historian** (pre-dates the library) |
| What document goes ON SCREEN · trace a claim's provenance · genealogy-before-filing · /verify 7.8 | **primary-source** (routes deep single-claim traces to the `primary-source-hunter` agent) |

Domain skills defer to each other along declared lanes (see each skill's `## Related skills`).
Two files per skill max: `SKILL.md` (≤250 lines, scannable) + one supplementary depth file
(`SCHEMAS.md`, `FAILURE-MODES.md`) where the domain demanded it.
