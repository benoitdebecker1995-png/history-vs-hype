---
name: Earn-Your-Inclusion / Orphan Quote Test
description: Verified facts from research summaries don't auto-qualify for the article. Every quote must earn its narrative seat or get cut.
type: feedback
originSessionId: 1d752b6d-75c0-42f1-a54d-0f1ea7ada73b
---
# Earn-Your-Inclusion Test (article-writer Rule 5B)

**Rule:** "Verified" + "in research summary" ≠ "must include." Every verified fact in an article must earn its narrative seat. Cut anything that fails the four sub-tests.

**Why:** Crusades article (2026-04-29) had a verified Phillips/JP2 2001 apology quote dropped into the 1204 sack section as a section closer. Real source. Real quote. Survived the fact-check pipeline. But narratively: 800-year time-jump, no setup, no follow-up, then HR divider. The user noticed during layout review and removed it manually with "THE APOLOGY SHOWS UP SUPER RANDOMLY WTF." Verified-source pipelines produce these airdrops because the verification gate only asks "is it true" — not "does it belong here."

**How to apply:** Run the four sub-tests on every candidate quote/fact during draft assembly:

1. **Airdrop test** — single-sentence paragraph introducing a new actor/place/time with no setup before and no follow-up after = cut.
2. **Time-jump test** — paragraph >50 years from surrounding context with no bridge phrase ("centuries later," "the wound persisted") = either write the bridge or cut.
3. **Closer-airdrop test** — last paragraph before HR divider must (a) land the section's argument, (b) bridge to next section, OR (c) deliver a punchline. None of those = cut.
4. **Phillips test** — read the section with the candidate sentence removed. Does the section still land? If yes, the sentence was decoration; cut it. If no, it's load-bearing; keep it.

**Where it lives:** `.claude/agents/article-writer.md` Rule 5B (HARD RULE, Tier 1) — bumped to v5.2. Quality Gate item added. Applies to CONVERT, WRITE, and EDIT modes.

**Detection signal during review:** if a section closer reads as random when scrolling the layout, it's likely an airdrop that survived fact-check. The user's instinct here is correct — trust it.
