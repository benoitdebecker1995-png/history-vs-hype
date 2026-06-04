---
description: Generate a segment-by-segment editing playbook from a rough cut SRT (Post-production Phase 3)
model: opus
---

# /editing-guide — Rough-cut editing playbook

Produces a Tripoli-style editing guide from a filmed rough cut. Cross-references the SRT against the script, maps each segment to planned B-roll shots (if any), suggests period-source fills for talking-head gaps via Gemini Flash, and surfaces re-records, captions, pacing, music decisions.

## Usage

```
/editing-guide                   # Run on current project (auto-discover inputs)
/editing-guide [project]         # Run on a specific project folder
/editing-guide --srt [file.srt]  # Override SRT auto-detection
```

## Output

- `[project]/05-EDITING-GUIDE.md` — the playbook (or `EDITING-GUIDE.md` if project doesn't number files)
- `[project]/_gemini-output/editing-guide-broll-<timestamp>.md` — raw Gemini Flash B-roll research (kept for reference)

---

## Inputs (auto-discovered)

**Required:**
- `*.srt` — prefer files matching `rough*cut*.srt`, fall back to most recently modified `.srt`
- Script — `02-SCRIPT-DRAFT.md` OR `SCRIPT.md` (whichever exists)

**Optional (used if present, gracefully skipped if absent):**
- `B-ROLL-FACSIMILE-SHOT-LIST.md` / `B-ROLL-ASSET-MANIFEST.md` / any `B-ROLL*.md` — pre-planned shots
- `NANOBANA-PROMPTS.md` — visual-language rules (highlight colors, citation tags)
- `03-FACT-CHECK-VERIFICATION.md` — unresolved verification gates
- `*POSTMORTEM*.md` — known re-records, visual fixes
- `_research/documents/` — local PDFs/images (Tier 0 inventory)

**Hard fail if:** no SRT found, OR no script found. Both are required to do the diff.

---

## Procedure

### Phase 1 — Load & parse

1. **Discover inputs** via Glob in active project folder (or specified `[project]`).
2. **Read all required + optional files.** For `_research/documents/`, list filenames only — don't read PDF contents (they're inventory references, not analysis inputs).
3. **Parse SRT into segment-aligned blocks.** Group consecutive subtitle entries into spoken-sentence chunks (~3-8 entries per chunk). Track first-entry IN timecode and last-entry OUT timecode per chunk.
4. **Map chunks to script sections.** Walk script section-by-section (§1 hook, §2 turn, etc., or scene/beat headers if no sections). Each script section gets a list of SRT chunks that fall within it.

### Phase 2 — Diff script vs SRT

Three diffs produced in parallel:

**Diff A — Verbal divergences:**
- For each script section, compare reconstructed SRT text against script paragraph
- Flag: dropped phrases, added phrases (ad-libs), wrong words that change meaning, missing words
- Distinguish: *intentional ad-libs* (richer/better than script — KEEP) vs *verbal stumbles* (jump-cut candidates) vs *factual divergence* (re-record candidates)

**Diff B — Transcription errors (caption pass):**
- Extract every proper noun + Spanish/Latin/foreign term from the script
- Check whether SRT renders each correctly
- Flag every mismatch with: script spelling → SRT spelling
- If >5 mismatches detected: surface a top-level note recommending `/fix` be run before burn-in. **Do NOT attempt corrections.** That's `/fix`'s job.

**Diff C — Pacing:**
- Read total runtime from last SRT timecode
- Compare against script's target runtime (look in script frontmatter or first 20 lines for "Target: X min")
- Compute delta. If actual ±10% of target → "on target." If overshooting → list 2-3 trim candidates from longest sections. If undershooting → flag (rare).

**Diff D — Audio loudness (runs only if a rough-cut media file is present):**
- Glob the project for the rough-cut `*.mp4` (the SRT's source media). If none, skip this diff silently.
- Run: `python -m tools.preflight.audio_loudness "<rough-cut.mp4>"`
- This is the earliest point the audio exists — catching a quiet/clipped master here is far cheaper than after upload (where `/publish` Gate 3 is only a backstop).
- Capture the verdict (integrated LUFS / true-peak dBTP / loudness-range LU vs YouTube's −14 target). Feed it into the Phase 5 output's "Audio loudness" section.
- If ffmpeg isn't installed the tool returns `MISSING` — surface the one-line install (`winget install Gyan.FFmpeg`) in the TL;DR and move on. Do NOT block the guide on it.

### Phase 3 — Identify B-roll gaps

1. For each SRT chunk's timecode range, check whether any planned shot from the shot list covers it.
2. Mark each chunk as:
   - ✅ **Planned shot covers** — note shot # and name
   - ⚠️ **Talking-head gap** — no planned shot
3. For talking-head gaps, gather context for Gemini: chunk's spoken text + script section topic + named entities mentioned in the chunk.
4. **Tier 0 inventory:** for each gap, also check `_research/documents/` filenames for matches. If a local file is obviously relevant (e.g., chunk mentions "Hassner" and `hassner-2020-anatomy-of-torture.pdf` is in `_research/`), pre-populate Tier 0 suggestion.

### Phase 4 — Gemini Flash B-roll research (batched, headless)

Build ONE batched Gemini Flash prompt covering all talking-head gaps from Phase 3. Pattern:

```
For a video on [TOPIC OVERVIEW from script frontmatter or first lines], identify
specific public-domain B-roll sources for these talking-head segments.

For each segment, provide 2-3 candidate sources. Format each as:
- Source name (year, author/origin)
- Where to find: archive.org / Wikimedia Commons / HathiTrust / LoC / gallica.bnf.fr — with URL or specific search term
- Why it fits this moment

NEVER suggest AI-generated imagery. Public-domain originals only — engravings, portraits,
primary documents, period maps, scholar book covers.

SEGMENTS:

[TC range] "spoken text"
- Topic: [topic descriptor]
- Mood: [tone setting]

[TC range] "spoken text"
...

Output as markdown with one ## section per segment, each containing the suggested sources.
```

Invoke via Bash:
```bash
gemini -m gemini-2.5-flash -p "<prompt>" --yolo > [project]/_gemini-output/editing-guide-broll-<timestamp>.md
```

After Gemini returns, **read only the parsed structured results** — do NOT pull the full output into Claude's context. Write the parsed list to a temporary working note in your head and reference by segment in Phase 5.

### Phase 5 — Compose the editing guide

Apply Tripoli's 9-section template. Write the final guide to `[project]/05-EDITING-GUIDE.md` (or `EDITING-GUIDE.md` if no numbered files in project).

**Density rule:**
- Hook segment (§1, ~first 60-90s): ~50 lines/min — every beat gets full table treatment
- Mid-video and close: ~25 lines/min — only beats with decisions/issues get tables; clean beats get one-liners

**Section structure:**

```markdown
# Editing Guide — [Project Title]

**Source:** `[srt filename]` vs `[script filename]`
**Region covered:** Full video, [N] minutes [N] seconds
**Generated:** [date]

---

## TL;DR — top 7 actions

1. [most important action]
2. [...]

---

## Segment 1 — [name] ([TC IN] → [TC OUT])

**SRT lines [N–M] — what's on tape:**
> *"[reconstructed spoken text]"*

**vs script said:**
> *"[script paragraph]"*

**Verdict:** [KEEP / FIX / DECIDE]

**Issues:**
| # | Timestamp | Issue | Fix |
|---|---|---|---|
| 1 | [TC] | [issue] | [fix] |

**B-roll for segment:**
- [TC range] [planned shot OR Gemini-suggested source]
- [...]

**Music note:** [optional]

---

[Repeat for each segment]

---

## Pacing assessment

| Marker | Script target | Rough cut actual | Delta |
|---|---|---|---|
| [...] | [...] | [...] | [...] |

**Verdict:** [acceptable / tighten / overshoot warning]

---

## Caption pass — burned-in subtitles

**Recommendation:** Run `/fix` before burn-in — [N] proper-noun/foreign-term mismatches detected:

- Line [N]: "[wrong]" → **"[correct]"**
- [...]

(Do NOT manually correct in this guide — `/fix` handles it programmatically.)

---

## Re-record / pickup checklist

Ranked by impact:

1. **HIGH:** [pickup] — [why, cost-benefit]
2. **LOW:** [...]
3. **OPTIONAL:** [...]

**Don't re-record:**
- [...]

---

## Music & silence beats

| Time | Beat | Recommendation |
|---|---|---|
| [...] | [...] | [...] |

---

## Audio loudness

(From Diff D — omit this section if no rough-cut media file was present.)

| Metric | Measured | YouTube target | Verdict |
|---|---|---|---|
| Integrated | [N] LUFS | −16…−12 (−14 ideal) | [OK / QUIET / LOUD] |
| True peak | [N] dBTP | ≤ −1 | [OK / CLIPPING] |
| Loudness range | [N] LU | 4–15 | [OK / DYNAMIC / FLAT] |

**Action:** [e.g., "Master is −19 LUFS — bring up ~5 dB before export" / "On target, no change" / "ffmpeg not installed — run `winget install Gyan.FFmpeg` to enable this check"]

---

## Done state

When this video is locked, you should have:
- [checklist of locked-state criteria derived from issues + decisions above]
```

---

## Defaults / edge cases

| Case | Behavior |
|------|----------|
| Multiple `.srt` files | Prefer `rough*cut*.srt`; otherwise most recently modified `.srt` |
| No shot list | Treat all segments as B-roll gaps; full Gemini research pass for everything |
| No script | Hard fail — guide is unreliable without script ground truth |
| No fact-check / postmortem | Skip those sources; build guide from SRT + script + shot list only |
| Output filename | Match project's numbered convention if `0X-*.md` files exist; otherwise plain `EDITING-GUIDE.md` |
| Gemini output location | `[project]/_gemini-output/editing-guide-broll-<YYYY-MM-DD-HHMMSS>.md` |
| Long output (>800 lines) | Single file with TOC at top; user splits manually if desired |
| Gemini call fails | Fall back to Tier B suggestions only (described + search hints, no named sources). Surface failure in TL;DR. |

---

## Reminders

- This command does NOT modify the SRT. Subtitle correction is `/fix`'s job.
- This command does NOT alter the shot list or research files. Read-only on inputs.
- Don't pull full Gemini output into context — read parsed sections only, reference by gap.
- Hook density > mid-video density. The first 60-90s carries disproportionate retention weight.
- "Verdict KEEP your version" is real and important — when the rough cut improved on the script, name it.
