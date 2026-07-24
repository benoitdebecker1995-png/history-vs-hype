# Packaging round — 2026-07-16 (vidIQ coach + repo gates)

## DECISIONS

**TITLE: KEEP — "Zelensky Honored These WWII \"Heroes.\" Poland Calls Them Nazis."**
- vidIQ Optimize: 95/100 (their highest seen on this channel). Repo title_scorer: 67/C (below-median but best of all candidates on our own gate).
- The "safe" de-Zelensky swap (vidIQ 94: "Ukraine's WWII 'Heroes': Poland's Nazi Accusation") scores **32/F on the repo scorer** (colon-pattern base + hedge flag) — NOT a 1-point tie by our filter. Rejected as the launch title.
- **Evergreen hedge = the /retitle workflow, not a weaker launch title:** "Zelensky Poland" carries 3,502/mo NOW; if that lane decays post-news-cycle, swap via /retitle (alt candidates logged below). Matches the channel's A/B-not-ban policy.
- Alt titles logged for retitle/A-B: "Ukraine's WWII 'Heroes': Poland's Nazi Accusation" (vidIQ 94/repo 32) · "Volhynia Massacre: Ukraine's Unburied Past" (86) · "The Volhynia Massacre: A Genocide Denied?" (83).

**THUMBNAIL: Concept 1 — the 1943 Klymchak report scan + overlay "LIQUIDATED ALL POLES".**
- Passes every channel filter: 3-word overlay ✓ (2–4 mandate) · no face ✓ · document-driven ✓ (niche outlier pattern) · verbatim-accurate fragment of a held document ✓ (McBride p. 648 rendering; fragment doesn't distort meaning — cropping guard checked).
- Coach's rationale adopted: it's evidence, not a headline — "says what their title only hints at" vs the main English competitor.
- A/B alternate: Concept 2 — original vs doctored proclamation side-by-side, overlay "HISTORY REWRITTEN" (weaker scroll-stop; strong analytical-audience variant).
- Rejected as primary: "Klym Savur signature / THE MISSING ORDER" — mid-video reveal, not a packaging hook (agree with coach).

**STRATEGY: SPLIT HOOKS (adopted).** Title works the modern-scandal lane ("zelensky poland" 3,502/mo); thumbnail works the massacre lane ("volhynia massacre" 3,326/mo @ only 25.5 competition — clean). Two search intents, one video that genuinely delivers both.

## Keyword table (vidIQ, 2026-07-16)
zelensky poland 3,502/mo comp 50.5 · volhynia massacre 3,326/mo comp 25.5 (overall 61.3 — best lane) · volhynia 5,234/mo comp 58 · upa 41,021/mo comp 58.6 · ukrainian insurgent army 4,678/mo comp 34.2.

## QUEUE (production)
1. Render Concept 1 (+ Concept 2 variant) → `python -m tools.preflight.thumbnail_checker` / thumbnail image audit.
2. Spawn **packaging-adversary** on the locked title+thumbnail vs the live SERP (incl. "Ukraine's Darkest Secret…", the Polish-language shelf).
3. YOUTUBE-METADATA.md: description/tags carry "Volhynia massacre", "UPA", "Ukrainian Insurgent Army" anchors (41K/mo "upa" rides tags/description, not title).
4. Guard note: all vidIQ numbers = enrichment input (ADR-0012/0013); repo filters made the decisions above; vidIQ's fact-claims remain zero-trust (it hallucinated a quote extension this same day).
