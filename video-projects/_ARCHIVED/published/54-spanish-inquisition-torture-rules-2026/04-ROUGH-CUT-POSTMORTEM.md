# Rough-Cut Post-Mortem — #54 Spanish Inquisition

**Date:** 2026-05-09 (post-mortem) / 2026-05-10 (test reframe)
**Status:** Complete. Findings baked into script-writer-v2 v15.0 + structure-checker-v2 (Constraints BC + BD).
**Salvage decision:** Publish 7:48 rough cut as-is. Add visual fixes for §5 + §2 in post.
**Test reframe (2026-05-10):** Shipping at 7:48 means this is no longer a "5-min Format C compression test." It is now an **8-min Format C close-read test** — what we learn from launch data will be about 8-min Format C performance (retention on document scenes, audience patience for primary-source close-read at this length), not 5-min compression viability. Compression-test conclusion: format does not compress to 5 min at this complexity. Lessons baked into v15.0 Rule 10 Format-Specific WPM Calibration.

---

## Runtime gap

| Metric | Value |
|---|---|
| Target runtime | 5:00 |
| Script estimate | 5:30 |
| **Actual runtime** | **7:48** |
| Overshoot vs target | **+2:48 (+56%)** |
| Overshoot vs estimate | +2:18 (+42%) |
| Spoken WPM (rough cut) | ~154 |
| WPM assumed by script | ~200 |
| Word budget overshoot | ~45% |

**Root cause:** Format C (forensic close-read) delivers slower than standard talking-head because verbatim legal/document quotes need deliberate read pace + pause-before/pause-after to register as evidence. Foreign proper nouns (Compilación, Torquemada, Díaz de Cáceres, conversos), longhand dates, and document-as-evidence beats compound the overhead. Pre-v15 script-writer-v2 used 250 WPM × 1.20x — wrong for document-heavy formats.

**v15 fix:** Format-Specific WPM Calibration in Rule 10. Format C = ~150 WPM, runtime_seconds × 2.5 (5-min Format C ≤ 750 words, not 1100). Structure-checker Constraint BD enforces as BLOCK gate.

---

## Live edits log (12 deltas)

| § | Change | Direction | Inferred reason |
|---|--------|-----------|-----------------|
| 1 | Cut "and they wrote it down" | Trim | redundant |
| 2 | Restructured "The rules for everything" → "It contained the rules for everything" | Smooth | grammar |
| 3 | Cut rhetorical question "And if the prisoner confessed?" | Trim padding | felt artificial |
| **4** | **Replaced "rule and its escape hatch, written together" with "this phrase is cited by historians to conclude torture could only occur once. Why else would you use the word 'repeat' as an exception?"** | **Major rewrite** | **Inverted attribution direction; added missing baseline scaffold** |
| 4 | Cut closing "built in from day one" line | Trim | over-asserting |
| **5** | **"Under §XV" → "Under Inquisition law"** | **Softened over-attribution** | §XV doesn't explicitly say silence=innocence |
| 5 | Cut "Hassner's words" attribution | Trim attribution | gut-punch lands harder bare |
| **6** | **"worse death" → "worse enemy"** | **Quote correction** | script had wrong word vs Kamen p. 232 source |
| 7 | Cut Marina/Díaz name-callback | Trim | recency duplication |
| 7 | "both right" → "both kind of right" | Hedged false symmetry | precision over balance (one-off mood per user) |
| 7 | CTA softened: "I don't just tell" → "I try not to just tell" | Voice softened | one-off mood per user |

---

## Findings (4 root causes, ranked by severity)

### Finding 1 — Loophole-without-rule [CRITICAL]

The script's locked thesis is *"Torquemada wrote the rules. The loophole was in the same paragraph."* But the script never articulates the rule the loophole loopholes. §3 covers procedural rules (personnel, warnings, ratification) but never the "one torture session only" baseline that §XV's final sentence is an exception to. So when §4 declares "rule and escape hatch, written together," the listener has no baseline to map "escape" against. **The thesis half-evaporates on screen.**

User patched live by inserting: *"This phrase is cited by historians to conclude that torture could only occur once. Why else would you use the word 'repeat' as an exception?"* This does three jobs the script skipped: names the default interpretation, anchors it to textual evidence (the word "repeat"), attributes it to historians.

**Same failure recurs at §5 (silence=innocence) and §2 (CIA cold/hot blood frame).** User's fix path for §5+§2 is visual: show the law text, show the CIA reports.

**v15 fix:** Rule 40 Baseline-Before-Exception (Two-Lane Audit). Path A = VO scaffold; Path B = `[ON SCREEN]` visual scaffold. Pick a lane per pivot beat. Format C = MANDATE; Format A/B = default-on relaxable.

### Finding 2 — VO-mono blindness [HIGH]

Script-writer-v2 treats scripts as audio-only. Uses `[ON SCREEN]` cues only for the *featured exhibit* (§XV title page, highlighted clauses) — never for the *baseline rules and counter-evidence* the featured exhibit's twist depends on. For a hybrid talking-head + B-roll evidence channel where "Primary sources ON SCREEN" is a Tier 1 hard rule, this is a category mismatch. The script's job is **lane choreography**, not VO drafting.

**v15 fix:** Rule 41 Lane Choreography. Every rule-assertion VO beat must have paired `[ON SCREEN]` cue OR explicit `<!-- NO VISUAL: reason -->` annotation. Structure-checker Constraint BC enforces.

### Finding 3 — WPM calibration error [HIGH]

See "Runtime gap" above. v15 fix: Rule 10 Format-Specific WPM Calibration + Constraint BD Word Budget Gate.

### Finding 4 — Citation Grounding gap [MEDIUM]

The §6 Toledo converso quote went to film with `⏳ Confirm verbatim` status in row 90 of `03-FACT-CHECK-VERIFICATION.md`. Script wrote *"continual fear is a worse **death** than a sudden demise"*; user spoke *"worse **enemy**"* in the rough cut. The fact-check explicitly noted the verbatim verification was deferred — and the script went to film anyway.

**Root cause:** Article-writer has Rule 5C (NotebookLM Citation Grounding — mandatory round-trip). Script-writer-v2 had no equivalent. Memory file `feedback-notebook-citation-grounding.md` (origin: 2026-04-29 Berlin Conference Anghie paraphrase incident) flagged the gap for article-writer but was not ported to script-writer-v2.

**v15 fix:** Rule 42 Citation Grounding. Mandatory NotebookLM round-trip for every blockquote before script lock. ⏳ rows block DRAFT-LOCKED status. Memory file scope extended to script-writer-v2.

---

## Retroactive audit results (pattern check)

Spawned subagent to audit Tripoli #51 + Manhattan #45 + Hijab #52 scripts for the same baseline-before-exception failure mode.

| Script | Beats audited | PASS | Notes |
|---|---|---|---|
| Tripoli #51 | 7 | 7/7 | Visual Chekhov's gun ("It looks like this. We'll come back to it.") plants every baseline before pivot |
| Manhattan #45 | 12 | 12/12 | Schagen letter as recurring deictic anchor; every "actually" beat preceded by ON SCREEN quote or narrated baseline |
| Hijab #52 | 14 | 14/14 | Strongest Path B specimen; primary-led rewrites (2026-05-09 v2) stack 2-3 primary documents ON SCREEN before each universalisation/loophole-closure pivot |
| **Total** | **33** | **33/33** | **No retroactive v15 work needed** |

**Verdict:** v15.0 rules are correct but not retroactively needed. Failure mode is **Format C-specific** — Format C is uniquely vulnerable because argumentative density tempts the writer to compress baselines into VO subordinate clauses, and the rule-being-subverted is often treated as common knowledge. Other formats already pass naturally because format itself forces primary-evidence visibility.

Audit report: `_research/baseline-audit-2026-05-09.md`.

---

## Action items remaining

- [x] **Verify §6 ground-truth quote** — RESOLVED 2026-05-09 via NotebookLM round-trip. Kamen p. 232 verbatim: *"Bit by bit many rich people leave the country for foreign realms, in order not to live all their lives in fear and trembling every time an officer of the Inquisition enters their house; for continual fear is a worse **death** than a sudden demise."* **Script was correct; user misspoke "enemy" during recording.**
- [ ] **Re-record §6 line** — DECIDED 2026-05-09. B-roll of the verbatim quote (with "death") was always going up; audio/visual mismatch would be a self-inflicted credibility hit on a channel whose edge is "I show you the sources." Single-line pickup, ~5 seconds. Replace the "enemy" take with "death."
- [ ] **Visual fixes in post** — add `[ON SCREEN]` for §5 silence-rule law text + §2 CIA chaos reports. Doesn't change runtime. §6 B-roll of Kamen quote was already planned.
- [ ] **Publish ~7:48 rough cut as vibes-test data** — log runtime overshoot as Format C compression-test result. Re-recorded §6 swap may shave 1-2 seconds; runtime still ~7:48.

**Note on Rule 42:** The script happened to be correct on §6, but the verification gate had been left at ⏳ "Confirm verbatim" — meaning the gate caught nothing because the script was lucky, not because the gate was reliable. Rule 42 still mandatory: round-trip every blockquote pre-lock, regardless of whether memory-file confirmation looks plausible.

---

## v15 changes summary

**`.claude/agents/script-writer-v2.md`:** v14.9 → v15.0
- New Rule 40 (Baseline-Before-Exception, Tier 1)
- New Rule 41 (Lane Choreography, Tier 1)
- New Rule 42 (Citation Grounding, Tier 1)
- Rule 10 extended with Format-Specific WPM Calibration

**`.claude/agents/structure-checker-v2.md`:** Wave 10
- Constraint BC (Lane Choreography Audit — Format C BLOCK / Format A/B WARNING)
- Constraint BD (Word Budget Gate — Format C BLOCK / Format A/B WARNING)

**Memory:**
- NEW `feedback-baseline-before-exception.md`
- EXTENDED `feedback-notebook-citation-grounding.md` to cover script-writer-v2

**What did NOT change:**
- Voice calibration. Per user, §7 softenings ("both kind of right", humbler CTA) were one-off mood. Calm Prosecutor voice stays as-is.
- The 12 minor trims are not patterns worth ruleifying.

---

## Lessons for future Format C scripts

1. **Word budget at lock:** count spoken-only words. Compare against runtime_seconds × 2.5. Cut before recording, not during.
2. **Pivot beat audit:** for every "but actually" / "loophole" / "exception" beat, commit to Path A (VO scaffold) or Path B (visual scaffold). Don't assume the listener brings the baseline.
3. **Baseline visuals:** plan `[ON SCREEN]` cues for supporting rules, not just the featured exhibit. The featured exhibit's twist depends on the baseline rules being legible.
4. **NotebookLM round-trip before lock:** every blockquote, every time. ⏳ Confirm verbatim is not a status; it's a TODO that blocks lock.
5. **Pacing math:** 5-min Format C = 750 words. Not 1000. Not 1100. 750.
