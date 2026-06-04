# Stale Claims Audit — _IN_PRODUCTION Projects

**Date:** 2026-05-17
**Scope:** All 24 projects in `video-projects/_IN_PRODUCTION/`

---

## Summary

| Category | Count | Projects |
|---|---|---|
| No `01-VERIFIED-RESEARCH.md` (pre-research) | 17 | See below |
| Empty research file (shell awaiting work) | 4 | #36, #38, #39, #55 |
| Research in progress — below Gate 1 (< 90% ✅) | 1 | #23 Christmas |
| Research complete — Gate 1 PASS | 1 | #21 Haiti |
| Research complete + script in progress | 1 | #56 Atlantic Slave Trade |
| **True stale ⏳ claims (actual unverified claims in claim rows)** | **0** | None |

---

## Projects with No Research File (pre-research phase — expected)

These are either idea-stage or were created as folder placeholders. Not blocking.

```
11-industrial-revolution-2025
12-guatemala-maya-claims-2025
15-library-alexandria-2025
16-pyramid-builders-merer-2025
2-heritage-protocols-2025
20-guadalupe-hidalgo-2025
25-iran-protests-history-2025
26-czechoslovakia-velvet-divorce-2025
29-format-research-2025
33-greenland-independence-2026
42-why-brazil-speaks-portuguese-2026
46-sabah-dispute-2026
47-operation-legacy-2026
48-hamoodur-rahman-commission-2026
49-code-noir-untranslated-2026
5-netanyahu-map-2025
8-medieval-women-2025
9-communism-definition-2025
```

---

## Projects Requiring Attention

### ⚠️ #23 Christmas Origins — Gate 1 WARN (80% verified)
- 8 ✅, 2 ❌, 0 ⏳
- 80% < 90% threshold — cannot proceed to script
- Action: either verify the 2 remaining claims via NotebookLM or drop them as ❌

### ✅ #21 Haiti Independence Debt — Gate 1 PASS (95% verified)
- 91 ✅, 5 ❌, 0 ⏳
- Ready for script if packaging passes `/greenlight`
- Memory notes: cut script from 18→12 min required before filming (per `MEMORY.md` project state)

### ✅ #56 Atlantic Slave Trade — Gate 1 PASS (script in progress)
- 23 ✅, 1 ❌, 0 stale in claim rows
- Scan false-positive: ⏳ markers only appear in legend/gate header text
- Gate explicitly: "Zero ⏳ on film-ready exhibits"
- Pending: thesis lock via `/thesis-discovery`

### ⬜ #36, #38, #39, #55 — Empty shells (0 claims)
- Research files exist but contain only headers/templates
- Not stale — just not started
- Action: none until packaging passes `/greenlight` for each

---

## Verdict

**No truly stale ⏳ claims exist in any active production project.** The scan found ⏳ symbols only in legend and gate-header text (not claim rows). The pipeline is clean. One project (#23) is below Gate 1 threshold — needs 2 claims resolved before scripting.

---

**Scanned by:** Antigravity Analytics Agent (Sonnet 4.6)
