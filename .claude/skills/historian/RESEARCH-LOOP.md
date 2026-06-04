# Stage-C Research / Contemplation Loop

The engine that runs *inside* Stage C (Corroboration). Distilled from the Kurdistan #58 session. Stages 0/A/B and the three Hard Rules still govern; this is *how you iterate* once sources are in the notebook.

## The loop (repeat until the angle's acts are continuous + honesty-guarded, then triage)

1. **ASSESS** — read `01-VERIFIED-RESEARCH.md` as a claim ledger. Against the locked angle/spine, where are the *narrative holes* (a 60-yr jump?), the *un-verified load-bearing claims*, the *over-claims*, the *missing emotional peak*?
2. **SYNTHESIZE (chief-coordinator move)** — integrate the three "departments" before deciding anything:
   - **Competitor gap** — what every competitor does vs. the white space (see Competitor re-check below).
   - **Comment-mine** — the loudest reflex + the #1 *unanswered* question (that's the demand).
   - **Audience/packaging** — channel DNA (HOW>WHY, mechanism, primary docs on screen), searchable entity/mechanism terms.
3. **DECIDE** — name the angle (or the specific gaps) explicitly and write it at the TOP of `01-VERIFIED-RESEARCH.md` as `🎯 ANGLE LOCKED`. Prioritize gaps (Tier 1 = before scripting).
4. **EXECUTE** — NLM query (always: *verbatim + page + tier; flag if a source doesn't support it; flag single-source*), OR tell the user exactly what to acquire/upload. File each finding as `C##` with [P]/[S] + T-tier + NLM source ID.
5. **PRESSURE-TEST** — before locking a thesis, run a verification query: *"is this defensible? quote the strongest SUPPORTING and any CONTRADICTING passages."* Keep the contradiction in the doc as the honesty guard.
6. **LOOP / don't declare "complete" early** — re-assess against the angle each pass. There is almost always another seam (a *bridge* between acts, a *near-miss*, the deeper *why*, a human anchor, the shareable gem). Stop when the acts run continuous and every claim is guarded — **then flip to triage**, not before.

## Operator instincts (how the channel-owner steers research — internalize, don't wait to be told)

These are the moves the user made repeatedly in #58. They ARE the loop's driving logic — anticipate them; when running autonomously, apply them yourself.

- **Push the gravity deeper than the obvious start.** The user's reflex was "go back *further*." Competitors begin where the topic seems to begin (here: 1916); the differentiated, on-brand story is almost always *older*. Default to interrogating the deep past before accepting a modern framing.
- **Hold the angle loosely; let evidence lead.** Lock a *working* spine, but stay genuinely open to a better one the sources surface ("maybe a different interesting evidence comes to light"). Evidence-led, not thesis-protective — be willing to re-lock and to bust your own earlier claims.
- **Distrust "done."** The user rejected "research complete" more than once. Never accept it at face value — re-ask "what are we missing?" against the angle AND against what competitors cover. Completeness is something you *interrogate*, not declare.
- **Decide by examining the decision process, not just the answer.** When choosing (e.g. the spine), the user asked "how would a historian actually decide this?" — reason on explicit axes (sources / surprise / scope / on-screen / searchable), show the reasoning, then pick. Don't hand back a verdict without the method.
- **Synthesize across roles before deciding.** The user thinks as the coordinator integrating distinct departments — competitor research, comment-mine demand, "what people actually want to watch." Triangulate all three; never decide from a single lens.
- **Separate the analytical spine from the emotional hook.** "Give me something people will LOVE" is its own question. The shareable gem ≠ the thesis — hunt it deliberately and let it compete for the cold open.
- **Protect the channel's identity above the interesting tangent.** Guard the throughline (history, not geopolitics); fascinating modern material earns a place only as payoff.
- **Treat the format limit as a forcing function.** The user asks "how long is this?" to force the shift from collecting to triage. Inputs are chosen for quality/breadth, never convenience — but output is ruthlessly bounded.

## Behavioral lessons (this session's feedback — apply by default)

- **Source selection = breadth + quality + RECENCY, never "free."** Sweep for recent (2018+) monographs; access status is a footnote. Lead with the best + broadest (incl. foreign-language + archival collections). See memory `feedback-source-selection-breadth`.
- **Angle is a synthesis decision, then LOCK it.** Don't drift. Title direction is deferred to `/greenlight`. Re-locking is allowed when research surfaces something better — but say so.
- **History-anchored is a STANDING CONSTRAINT.** Gravity in the deep past; modern material is the closing *rhyme/payload only*, never a current-affairs explainer. If a beat explains present-day politics for its own sake, cut it. (User reaffirmed this 3×.)
- **Competitor re-check uses FULL TRANSCRIPTS, run AFTER deep research.** `yt-dlp --skip-download --write-auto-sub --sub-lang en` → strip VTT → read. Purpose: (a) confirm white space, (b) catch audience-EXPECTED beats you lack (e.g. the genocide/atrocity peak, the famous proverb), (c) **turn their saturated thesis into your SETUP, not your thesis** ("they end at X; we explain *why* X").
- **Hunt the gem.** Explicitly sweep for the "I have to tell someone this" fact (the shareable payload). It may become the hook. Hold the honesty caveat (don't anachronize a medieval figure into a nationalist).
- **Auditor's-edge / honesty guards are mandatory, not optional.** Prefer myth-bust beats (popular-claim vs what-the-document-says); de-risk overclaims (check *timing* — e.g. the resource wasn't proven until after the decision; claim "states" not "a nation"); always carry the scholarly complication so a historian can't catch you. Bust your own Phase-1 brief claims when sources contradict them.
- **Runtime reality.** Channel hard cap = **12 min** (~1,400–1,600 spoken words ≈ **10–12 beats**). A deep dossier holds 3–4× that. Depth is for *bulletproofing on-screen claims + giving cut options* ("scholarly behind the camera, accessible in front") — not for putting all of it on screen. The dossier is done when you can *triage*, not when you've collected everything.

## Source-availability probe = the Stage A→B bridge
To choose the spine, don't do open-ended "general research." Run a **bounded probe with a stop rule**: for each candidate spine, test whether its *load-bearing PRIMARIES* are accessible AND on-screen-able. The spine whose primaries you can actually put on screen wins. Two of three historian axes (sources / surprise / scope) are usually already known from Stage A; the probe closes the third.

## NotebookLM operational gotchas
- **Auth expires constantly — auto-recover, don't punt.** On a REAL auth failure (`UNAUTHENTICATED` on an actual call): (1) **Claude runs `nlm login` directly via Bash** (authorized — non-interactive, reusing the saved Google session in a dedicated auth-Chrome profile, not the user's browsing window; add `--force` to bypass the "already valid" short-circuit and rewrite the token); (2) retry the failed call. Only ask the user if `nlm login` itself blocks on a Google sign-in prompt.
  - **⚠ 0.6.14 BUG — `refresh_auth`/`server_info` lie.** They report `"expired"`/`"stale"` even when the cookies authenticate fine, and `nlm login --force` does NOT clear the false verdict. **Do NOT treat `refresh_auth: expired` as ground truth and do NOT loop on `nlm login` because of it** (you'll just pop Chrome for nothing). Ground-truth test = an actual authenticated call (`notebook_list` / `notebook_get`); if that returns data, auth is fine — proceed.
  - NOTE: `PYTHONIOENCODING=utf-8` is set (user env var), so the old `✓` UnicodeEncodeError traceback on Windows is gone — validated on the real `nlm login --force` success path.
- **URL ingestion silently fails on:** borrow-only archive.org pages (gets metadata only), Cloudflare-walled PDFs ("Verifying your browser…"), and image-only PDFs (no text layer → grabs only Google-Books boilerplate). **Fixes:** use the archive.org `_djvu.txt` / a clean `.txt`; file-upload the real PDF; or have the user download via a real browser then upload.
- **VERIFY every new source** with `source_describe` (or a scoped query) before trusting it — don't assume ingestion took.
- **Scope queries with `source_ids`** to force the right sources and avoid contamination from stray/off-topic uploads.
- Large query outputs persist to a file — Read it.
