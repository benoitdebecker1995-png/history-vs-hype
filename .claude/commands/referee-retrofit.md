# /referee-retrofit — retrofit an existing video to the document-led referee standard

Apply the #61 Black Legend research method to an existing `_IN_PRODUCTION` project: **$ARGUMENTS**
(e.g. `/referee-retrofit 58-kurdistan`, `/referee-retrofit 59-israel-palestine`, `/referee-retrofit 36-panama`)

Invoke the **historian** skill first; this command runs Stage-C discipline (`.claude/skills/historian/RESEARCH-LOOP.md` — the verification protocol and the "Referee-format research process" section are the spec; do not duplicate, follow them). Honor `feedback-document-led-referee-franchise`, `feedback-script-revision-grounding` (Kurdistan), and the no-moralizing voice (`VOICE-PROFILE.md`).

Goal: turn a debunk-format / single-thesis project into a **referee** that names the camps, grounds every mechanism, verifies every quote, and lets the documents carry the verdict — OR conclude the topic doesn't fit the format and say so plainly.

## Step 0 — Load
Read the project's `01-VERIFIED-RESEARCH.md`, `PROJECT-STATUS.md`, any `02-SCRIPT*`/`SCRIPT.md`, and the NotebookLM notebook id. Confirm auth with a real call (ignore `refresh_auth` false "stale").

## Step 1 — FORMAT-FIT GATE (do not force it)
Is there a genuine conflict where **two or more camps crop the SAME evidence** (not merely an under-told story)? And are the **primaries gettable on screen**?
- If NO → STOP. Report that this topic is a different (weaker for-referee) format; recommend keeping its existing frame. Don't bolt a referee frame onto a one-sided story.
- If YES → continue.

## Step 2 — DEMAND + COMPETITOR PASS (run/refresh — don't assume it exists)
This is the front-end research, not an optional input. If the project lacks these or they're stale, generate them:
- **Competitor gap on FULL TRANSCRIPTS** (`competitor-gap` agent + the RESEARCH-LOOP "Competitor re-check": `yt-dlp --skip-download --write-auto-sub`). Find the white space, catch audience-EXPECTED beats you lack, and turn each camp's saturated thesis into your SETUP. ⚠ Verify whitespace/"nobody covers X" against the ACTUAL transcript, never a subagent summary (`feedback-no-definitive-claims-without-verification`).
- **Comment-mine** (`/comment-mine` across the big videos): the loudest reflex + the #1 UNANSWERED question = the demand; and *which camp the audience actually holds by default* (sets what you're breaking).
- **Packaging-driver scan** (the #61 method): pull the popularity landscape (view counts + titles from each `.info.json`), the winners' HOOKS (first ~40s of their auto-subs), and **download + visually inspect** their thumbnails (no fabricating visuals); score titles with `title_scorer`. This is what makes the title keyword-anchored and the thumbnail document-split.
Feed all three into Steps 3 (camps), 7 (re-rank), and 8 (packaging).

## Step 3 — CAMP + PROPONENT MAP (the neutrality engine)
List each camp and tier it to **named, dated proponents** (e.g. for I/P: the "generous offer rejected" camp vs the "offer nobody could accept" camp — who argues each, when). Draft the 1–2 line **referee anchor** (the "equivalent distortions of a single truth" / "the opposite of a falsehood is a contrary falsehood" equivalent for THIS topic, sourced). Never assert a camp as truth; never "some say."

## Step 4 — SOURCE RECENCY AUDIT
For each load-bearing beat, is the anchor a **modern synthesis (2018+)** or a dusty standard? Produce an ACQUIRE list that (a) modernizes the dusty anchors and (b) steelmans EACH camp with its best living voice + its academic critic. Access status is a footnote; budget unlimited. (Output a shopping list for the user to drop in Downloads → text-check → upload.)

## Step 5 — MECHANISM GROUNDING (Kurdistan rule — before any rewrite)
List every causal/legal/process beat the script explains (treaties, legal instruments, demographic/economic mechanisms, institutional terms). For each: **query the notebook to understand it**, write a **MECHANISM NOTES** block into the structure doc, build a one-line clarity device, and flag any adjacent-concept conflation to avoid. Never explain a mechanism from your head.

## Step 6 — VERIFICATION GATE (run BEFORE drafting — catches NLM fabrications)
For every on-screen quote/claim, run the RESEARCH-LOOP verification protocol: check `sources_used`; raw-grep (`source_get_content` → Python phrase search) any source returning empty `sources_used`; flag NLM paraphrases-dressed-as-quotes; mark page numbers as PDF-eyeball-pending. Drop or reattribute anything unconfirmed. Output a verify-status list.

## Step 7 — RESTRUCTURE to crop-test + demand re-rank
Rebuild the beat sheet in crop-test shape (EVIDENCE → camp-A crop → camp-B crop → DOCUMENT → qualification). Re-rank acts against the **Step-2 demand×gap data**; promote the highest-demand beat, cut low-demand, lead the cold open on the least-loaded high-demand beat. Mark a triage cut-zone for the 12-min cap.

## Step 8 — PACKAGING (Calm Prosecutor)
From the Step-2 packaging-driver scan: keyword-anchored, two-sentence, **non-cringe** title (`title_scorer` + paste-ready VidIQ chat prompts for volume/competition/Overall). Document-split thumbnail, no face. Open on the document; modern culture-war → close only.

## Output
- A `REFEREE-RETROFIT-DELTA.md` in the project folder: format-fit verdict, camp/proponent map + anchor, ACQUIRE list, MECHANISM NOTES, verify-status, restructured beats, packaging direction.
- Update `PROJECT-STATUS.md` and the Historian Stage State.
- Do NOT draft the script. Stop at a verified, mechanism-grounded, restructured outline + an acquisition/verification to-do for the user.

## Caveat
Steps 4–6 may surface that a beat can't be sourced to the modern/neutral standard, or that a camp has no gettable primary. Surface those as flags (`[FLAG: LIBRARY ACQUISITION]` / `[FLAG: NEED SOURCES]` / `[FLAG: DIRECTION NEEDED]`), don't paper over them. If the format-fit gate (Step 1) fails, that's a valid and useful outcome — report it.
