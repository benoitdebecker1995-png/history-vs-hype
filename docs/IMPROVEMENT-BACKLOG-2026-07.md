# Improvement Backlog — 2026-07-01 full-project audit

> Scope (user-picked): channel results + tooling/repo health + workflow/AI quality; audit the three
> multi-session plans AND hunt new gaps; mix of quick wins + structural, ranked by ROI.
> Evidence gathered live 2026-07-01. Execute top-down; P2 items are opt-in, not a new mega-plan.
>
> **Pipeline context (user, 2026-07-01):** #59 Palestine is in EDIT now; #62 Ukraine/Volhynia is the
> next build; Panama (and its pre-registered v18 KPI read) comes after those. The proven data loop
> behind packaging decisions = **periodic Studio CSV exports** — the hijab/SCS swaps came from that
> data, per the creator. Frame every CTR read below around a fresh CSV pull, not ad-hoc pastes.

---

## Verified healthy — no action needed

- **UPGRADE-PLAN: 23/24 done.** Only R4 remains and it is blocked BY DESIGN (R3 verdict NOTEBOOK-SUFFICIENT, notebook 10/10 vs graph 0/10). The plan is effectively complete; the real KPI test (Panama passes-to-lock + H2 CTR ≥4%) is pre-registered and Panama scripting is underway.
- **Calibration loop is live and fed.** #59 lock deltas mined (corpus entries 59-01..22, 51 read-aloud deltas), EVAL-BASELINE ledger + INTERVIEW-AGENDA updated at lock (2026-06-24). S14 standing loop works.
- **Analytics freshness:** `analytics.db` refreshed today 09:59; `intel.db` today 15:02. Routines 4/5 producing dated outputs through 06-29/30. `HvH-Reconcile` exited 0 today.
- **Topic pipeline stocked:** Tier A has Brest-Litovsk (63 Overall/5,008 mo, weak shelf) and Unequal Treaties China (61/4,554, near-zero direct coverage) ready behind Panama.
- **Test suite: 670 passed / 13 skipped / 2 failed** — both failures in `tools/tests/test_swap_ledger.py` (see P0-1).

---

## P0 — broken and blocking (this week)

### 1. Close the overdue swap-loop read — the CTR growth loop is stalled ⏰
The channel's #1 verified lever (CTR) has a live experiment nobody can read:
- **Experiment #1** (Slave Trade `aSfZtrgGjwA`, thumbnail-only, shipped 06-14) was due for its read **2026-06-29** — still PENDING (`channel-data/SWAP-LEDGER.md`, last regenerated 06-15).
- **Blocker A:** `ctr_snapshots` max date = **2026-06-15** (16 days stale). The read needs a fresh **Studio CSV export** (the loop the creator already runs and credits for the hijab/SCS swap decisions) — one export refreshes the snapshots and closes this read; the same pull repeated ~07-25 reads the hijab/SCS swaps.
- **Blocker B:** the read path itself looks broken — `test_read_computes_lift` / `test_read_computes_drop` fail with `KeyError: 'verdict'`, i.e. `read_experiment()` (tools/swap_ledger.py:202) hits an early error-return instead of computing a verdict. Root-cause before trusting a real read.
- **Then:** ingest the export → `ctr_quick_add --swap-read 1` → verdict (LIFT ≥+0.5pp / FLAT / DROP) → if LIFT, run the loop on the next dying-but-impressed video.

### 2. Repair the morning routine chain — freshness failures are silent
Today's evidence (schtasks + `.brain/_inbox/`):
- `HvH-Reconcile` **aborted this morning**: analytics.db was 48.9h stale at run time (`reconcile-stale-db-2026-07-01.md`) — the 07:45 GrowthRefresh hadn't run for ~2 days; the catch-up storm fired all tasks at 09:17 and the refresh only landed at 09:59, after reconcile had already given up.
- `HvH-GrowthRefresh` last result **267014** (SCHED_S_TASK_TERMINATED), `HvH-ChannelHealth` + `HvH-StaleProjects` **−2147020576** (0x800710E0, start refused), `HvH-BrainHygiene` **exit 1** (06-30 22:00).
Root cause: the 07:45 → 08:00 → 08:30 chain is TIME-coupled on a laptop that is often asleep at trigger time; wake-up catch-up runs them simultaneously in the wrong order, and task conditions refuse some starts.
Fix direction:
- (a) Make consumers **self-healing**: reconcile/channel-health should check DB freshness and invoke `growth_data --refresh` inline instead of aborting (event-driven, not clock-faith).
- (b) Task conditions: `StartWhenAvailable` + allow-start-on-batteries on all HvH-* tasks.
- (c) Diagnose BrainHygiene exit 1 from `brain-hygiene-run-2026-06-30.log`.
- (d) Add the still-pending `AtLogOn` trigger for HvH-Reconcile (needs an elevated shell).
- (e) Refresh the stale W3 routine-health table in `docs/AUDIT-COMMANDS-2026-06.md` (still says HvH-Reconcile "not scheduled").

### 3. Commit sweep — 176 dirty paths, 73 untracked, real data-loss exposure
Working tree on a single laptop with no push holds, uncommitted:
- **Canonical infra the ADRs already document:** `tools/video_projects/` (ADR-0008), `tools/title_features.py` (ADR-0009), `tools/subtitles.py` (ADR-0010) — all UNTRACKED.
- **The entire 06-27 analytics wave:** CTR-TITLE-FORMULA, CTR-THUMBNAIL-FINDINGS, FLOP-AUTOPSY-{PLAN,TABLE}, CHANNEL-PERFORMANCE-DATA, LONGFORM-FAILURE-DIAGNOSIS, AB-TEST-AND-TRAFFIC-CTR, calibration/OPENER-*.
- **Whole project folders** #61 and #62; #36/#59 production files (SCRIPT.md, TELEPROMPTER, metadata).
- **3 new commands** (referee-retrofit, voice-clickdrill, voice-readthrough) + OPENER briefs + VIDIQ-MCP-CAPABILITY-MAP.
- **Half-applied moves:** sykes-picot → `_ARCHIVED/published/` (deletions unstaged, destination untracked); `test_pacing.py` move (old path staged-deleted, new path modified).
Action: series of logical commits (infra / channel-data / commands+reference / video-projects / moves). Optional: add a `.gitattributes` to stop the LF↔CRLF churn warnings (see P2-10).

---

## P1 — cheap, high value

### 4. Apply the 5 pending retitles (shortlist ready since 06-10, zero applied)
`channel-data/RETITLE-SHORTLIST.md` proposals for `xODFE2Pyubo` (Thailand–Cambodia), `QgDJSu0Y5K0` (Western Sahara), `499YLd1BHZ4` (NATO), `mg6ujk6rDVE` (Manhattan), `P6yalauLDic` (Mexico island) were never applied — only hijab + SCS (separate pair, reads ~07-25) went live. Each is a dead-or-dying video, so parallel swaps are safe; open a `swap_ledger` record with baseline per swap. Caveat the shortlist itself notes: #1/#2 want matching overlay changes = 2-variable; either accept the attribution loss (lottery re-tests) or swap title-only first.

### 5. Fix CLAUDE.md coverage-query guidance — it contradicts the R3 measurement
CLAUDE.md § Knowledge Graphs still routes "have we covered scholar/treaty/topic Z" to `graphify-research`; the R3 pilot scored the `HvH-coverage-corpus` notebook **10/10 vs graph 0/10** on exactly those queries. Point coverage questions at the notebook (via notebook-researcher), demote the research graph to a footnote, mark R4 permanently closed, and declare UPGRADE-PLAN complete — which frees `/refactor` for whatever gets defined after Panama's KPI read.

### 6. Voice-corpus + archive hygiene (two known misfiles, flagged 06-12, still present)
- `transcripts/Kraut/` still contains RealLifeLore ("Why is Russia So DAMN BIG?" — the anti-voice) and a Finnish-language interview. Any future voice mining ingests the anti-voice as a positive ref. Move both out.
- `35-gibraltar-treaty-utrecht-2026/POST-PUBLISH-ANALYSIS.md` actually analyzes `TYNaIu28LeU` (Belavezha/USSR video) — refile to the correct project so `/patterns` and S4-style mappings stop mis-joining.

---

## P2 — structural (opt-in; don't open all at once)

### 7. Make CTR-snapshot staleness self-announcing
The swap loop's weak link is that nothing prompts the next Studio CSV pull: `ctr_snapshots` went 16 days stale WITH an experiment due and nothing surfaced it (P0-1 only got caught by this audit). Wire a "swap read due — pull a fresh Studio CSV" line into session start (`tools/hooks/session_context.py`) — `packaging_autopilot` already computes SWAP EXPERIMENTS DUE, so this is plumbing, not new logic. Standing read dates to surface: hijab/SCS ~07-25, plus any ledger row past `planned_read_date`.

### 8. Retire the three completed multi-session plans from active memory
UPGRADE-PLAN (23/24, R4 closed), packaging overhaul (round 2 executed), claudebase overhaul (11/11) are all effectively done, yet memory still advertises them as active plans. Mark their memory files completed and slim MEMORY.md's Active Plans section. Deliberately do NOT define the next big plan until Panama's passes-to-lock + first-28-day CTR read — that decision point is pre-registered, and Panama is now two videos out (#59 edit → #62 build → Panama), so this stays parked for a while.

### 9. Command-sprawl follow-through (W1 leftovers)
30 active commands; the W1 audit shortlisted overlap candidates (`polish`, `script-research-pass`, …). W2's decision log exists — verify every shortlist item was consciously kept/merged, not silently forgotten. Also: 3 new commands shipped since the audit (referee-retrofit, voice-clickdrill, voice-readthrough) are outside it.

### 10. Line-ending normalization
Add `.gitattributes` (`* text=auto` + explicit binary entries for `*.db`) so every git operation stops emitting dozens of LF/CRLF warnings and diffs stay clean. Do it in the same session as the P0-3 sweep to avoid double-touching files.

---

## Suggested execution order

1. P0-3 commit sweep first (protects everything else), with P2-10 folded in.
2. P0-1 swap read: fix `swap_ledger` bug → user pastes fresh Studio CTR → read experiment #1 → open next swap (can fold P1-4 baselines into the same paste session).
3. P0-2 routine chain repair (one focused session; needs one elevated shell moment).
4. P1-5 + P1-6 doc/hygiene fixes (30 min combined).
5. P2 items as separate deliberate picks.
