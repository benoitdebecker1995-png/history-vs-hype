# Stale Projects — 2026-08-27

14 of 15 `_IN_PRODUCTION/` folders are past the 7-day line. Only #62 Volhynia (editing, touched
today) is live. **Nine are real projects; five are leftover thumbnail folders from published
videos** (grouped at the bottom — those are an archive decision, not work).

Three blocked projects share one blocker: **NotebookLM auth is expired.** One `nlm login` unblocks
#63, #64 and #65 at once.

---

## 63-leopold-congo-cobalt-2026 — 35 days untouched

**Stage:** Pre-research (packaging gate cleared, Phase 2 never started)
**Last touched:** 2026-07-22
**Blocking issue:** NotebookLM auth expired — recorded in the status doc *and* in the packaging lock
(`NLM P5: not queried — packaging notebook auth-expired`). Phase 2 cannot start without it.
**Next action:** Run `nlm login`, create the topic notebook, upload the 5 already-owned sources
(Casement, Morel, CFS gazette, Hochschild, Ewans) from `_research/00-NOTEBOOKLM-SOURCE-LIST.md`.
**Estimated time:** 2h

---

## 61-spanish-colonization-black-legend-2026 — 35 days untouched

**Stage:** Research complete — Stage C locked 2026-06-18, awaiting title lock
**Last touched:** 2026-07-22
**Blocking issue:** The status doc's step 1 is still marked **(IN PROGRESS)** — the packaging-driver
scan of the top ~5 comps was started and never closed, and the title lock sits behind it.
Secondary: `⚠️ page in-source verification` of new-source verbatims is outstanding before any
on-screen card (only Clayton + Villacañas returned confirmed NLM `sources_used`).
**Next action:** Finish the packaging-driver scan on the top 5 comps and lock the title (lead C:
"The Black Legend Is Half True. So Is the Legend That Replaced It.").
**Estimated time:** half-day

---

## 60-guadalupe-hidalgo-dispossession-2026 — 35 days untouched

**Stage:** Script draft (SCRIPT.md v1, ~1,970 words, explicitly **not locked**)
**Last touched:** 2026-07-22
**Blocking issue:** The script header says "pending creator read-aloud" — it has been pending since
2026-06-13. `03-FACT-CHECK-VERIFICATION.md` is still the locked placeholder, so nothing downstream
can move. Carried flag: the "40 years" span in the retired title is loose (honest span ~50yr).
**Next action:** Creator read-aloud (T1) on `SCRIPT.md`, then `/verify`.
**Estimated time:** 2h

---

## 55-falklands-malvinas-2026 — 30 days untouched

**Stage:** Research — Stage A locked 2026-07-26, Stage B (source criticism) pending
**Last touched:** 2026-07-28
**Blocking issue:** Two, one of them a contradiction inside the status doc. (a) The `### Next`
section says `/script`, but Historian Stage State says Stage B is still pending — those disagree
and someone has to decide which is true. (b) The cold open must be re-decided: the 1844 arbitration
quote it currently specifies was demoted to a single-source claim (C36 → C49e). Non-blocking:
Goebel (1927, Yale UP) is the load-bearing acquisition for 4 T2 claims.
**Next action:** Pick the replacement cold-open exhibit — McNeil, HC 16 Feb 1948 (C47a) or the
4 May 1955 pairing (C44a + C49a) — then settle the Stage B vs `/script` question.
**Estimated time:** half-day

---

## 36-panama-canal-deconcini-2026 — 29 days untouched

**Stage:** Script v2 — fact-check APPROVED, not locked
**Last touched:** 2026-07-28
**Blocking issue:** `BREAKOUT-VERSION-2026-07.md` (2026-07-28) prescribes three changes that were
written and never applied — change 1 is that the title must name the Panamanian pocket, not just
the topic. The currently-locked packaging title ("America Took the Panama Canal With a Treaty.
Panama Took It Back.") does not name it, so the lock and the breakout memo disagree.
**Next action:** Apply the three BREAKOUT changes, starting with the pocket-naming title rewrite +
re-run `packaging_lock.py`. Then the heavy gate → creator read-aloud (T1) per
`VOICE-DRILL-RESUME.md`.
**Estimated time:** half-day

---

## 64-ancient-dna-aryan-weaponised-2026 — 28 days untouched

**Stage:** Greenlit, pre-research (Phase 1 brief only — `_research/PRELIM-BRIEF-2026-07-29.md`)
**Last touched:** 2026-07-29
**Blocking issue:** NotebookLM auth expired (`NLM P5: not queried`). Folder has no
`01-VERIFIED-RESEARCH.md` yet. Standing guard: the Orbán/Árpád strand did **not** survive sourcing —
do not reinstate without a dated, attributable source.
**Next action:** `nlm login`, then Phase 2 verification of every §4 source.
**Estimated time:** 2h to unblock; research itself is a multi-day job

---

## 65-enigma-polish-cipher-bureau-2026 — 27 days untouched

**Stage:** Pre-research — packaging gate cleared on demand/whitespace, title **LOCK PENDING owner
choice**
**Blocking issue:** Waiting on Benoit. Two sub-blockers: `topMarkets` for the primary anchor
("enigma code", 6,198/mo) is unresolved (pocket gate), and the title lock is his pick from three.
NLM auth also blocks the research that follows.
**Last touched:** 2026-07-30
**Next action:** Resolve `topMarkets` for "enigma code" via vidIQ (30 min, unattended) — then the
title choice is Benoit's, and `packaging_lock.py` stamps it.
**Estimated time:** 30 min for the pocket check; the title lock is an owner decision

---

## 67-donation-constantine-forgery-2026 — 12 days untouched

**Stage:** Script draft v4, not locked (three-file shape)
**Last touched:** 2026-08-14
**Blocking issue:** Fifteen `[CL]` passages still need Benoit's own language — this is talk-first
work that only he can do. The old fact-check file was an uncompleted template, so the draft has not
passed a claim-and-exhibit check either. No thumbnail selected.
**Next action:** One creator read-through focused on the `[CL]` passages, especially the Act 5→6
contrast and the bridge into circulation; preserve spontaneous wording verbatim.
**Estimated time:** half-day

---

## 37-untranslated-vichy-statut-juifs-2026 — 10 days untouched

**Stage:** ⚠️ **Cannot determine — the folder has no status file.** It is now only
`_research/documents/` (22 PDFs and page scans: the JORF issues, Paxton, Marrus & Paxton, Poznanski,
Rousso, Weisberg, Semelin, plus Chirac/Macron speeches). No `PROJECT.md`, `PROJECT-STATUS.md`,
`SCRIPT.md`. Memory carries it as "ready to film", which the folder does not support.
Note: several documents in there are Volhynia-side (`Fascism_or_ustashism_Ukrainian_integral.pdf`,
`Polshcha-Tekstartykuu.pdf`), so it may be serving as a shared source pool rather than a project.
**Blocking issue:** State is unrecoverable from the folder alone.
**Next action:** Decide what this folder is — live project or shared source library. If it is a
project, restore a `PROJECT.md` before it decays further.
**Estimated time:** 30 min

---

## Not projects — leftover thumbnail folders (32 days each)

These five contain **only `.psd` thumbnail files**, no research, script, or status doc. Their videos
are published. They inflate the `_IN_PRODUCTION/` count and the §3 table.

| Folder | Contents | Last touched |
|---|---|---|
| `10-dark-ages-2025` | 6 × `Thumnbnail *.psd` (sic) | 2026-07-25 |
| `23-christmas-origins-2025` | 3 × `Thumbnail *.psd` | 2026-07-25 |
| `27-peru-2025` | 3 × `Thumbnail *.psd` | 2026-07-25 |
| `35-gibraltar-treaty-utrecht-2026` | 3 × `Thumbnail *.psd` | 2026-07-25 |
| `Tariffs` | `Thubnail redo.psd` (sic) — also violates the numbering convention | 2026-07-25 |

**Next action:** Move all five to `_ARCHIVED/published/` alongside their video folders (the other
seven published projects already live there). Owner call — this routine does not move folders.
**Estimated time:** 15 min

---

## Escalation note

The routine's >21-day rule fires on **eight of the nine real projects** — everything except #67 and
#37. That is not eight independent stalls: #62 Volhynia has been the committed next upload since
23 August ("Do not surface alternative topics"), and the pipeline behind it stopped moving on
2026-07-30. Expect these to unfreeze in order once #62 ships, not to need individual rescue.
