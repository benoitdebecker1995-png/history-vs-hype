# Comment replies: sources named in prose, not a citation block

**Date:** 2026-07-07
**Status:** accepted

This ADR exists because it **reverses a documented default**. The prior `youtube-comment-response-guide.md` mandated a formal shape on *every* reply: `state the myth → correct → (Sources: …) → CTA ("Full breakdown on YouTube")`. A future reader — or a future `/improve` pass — will find the new `comment-responder` agent deliberately *omitting* the sources block on discussion replies and reasonably ask "did someone forget the citation rule?" No. It was removed on purpose, for the reasons below.

## The decision

Comment replies split by **posture** (see CONTEXT.md "Reply posture"):

- **Interlocutor / Question** (engaged discussion, genuine ask): sources are **named in prose**, only where the claim would be doubted or naming adds weight ("Khalidi dates it to the 1920s"). **No `(Sources: …)` block. No CTA.**
- **Drive-by claim** (a wrong assertion from a low-investment stranger): the formal **sources line + CTA is retained** — a skeptic scanning past wants the receipt, and the CTA legitimately drives a first-time viewer to the video.

Behind every reply, regardless of posture, the agent keeps a **full sourced audit trail** for the owner (CONTEXT.md "Audit trail"). "Honest about sources" is satisfied by the *research* being fully sourced, not by the *reply* carrying a bibliography.

## Why reverse the old mandate

The owner repeatedly rejected the templated replies as **"artificial and fake."** The `(Sources: …)` + "Full breakdown on YouTube" bolt-on is the single loudest tell: on a good-faith back-and-forth with an already-engaged viewer, it reads as a press release, not a person. Two independent evidence sources converged:

1. **Empirical** — a YouTube-API pull of 23 real creator replies on comparable history channels: median length ~38 characters, max ~305, sources woven into the sentence when named at all, never a citation block. A bibliography-terminated reply does not occur in the wild for discussion comments.
2. **Owner feedback** — logged in `memory/feedback-comment-reply-natural-voice.md`: the Sources+CTA template "belong[s] to *myth-debunk* replies aimed at a drive-by stranger, not to a nuanced back-and-forth." The memory explicitly called for a "discussion reply vs debunk reply" split in the guide. This ADR is that split.

The academic-rigor concern (AskHistorians cites its sources) is answered by the *two-layer model*, not by a citation block: do the comprehensive, sourced work behind the scenes; deliver it in the register a creator actually types. Naming a scholar in-sentence when the claim would be doubted is honest sourcing; a formal apparatus on a bar-talk reply is theater.

## Considered alternatives

- **Keep the Sources+CTA mandate everywhere** (status quo). Rejected — it is the specific thing the owner rejects, and it contradicts how every comparable creator actually writes.
- **Drop sources from replies entirely**, keep them only in the audit. Rejected — it fails the "honest about sources" half of the brief; naming Khalidi or Hourani in-sentence is exactly what makes the reply credible *and* human.
- **Always attach a compact sources line** (a lighter receipt on every reply). Rejected — still reads as apparatus on a discussion reply; the median real reply carries none.
- **One reply mode for all comments.** Rejected — a drive-by false claim and a 500-word good-faith rebuttal need different shapes; collapsing them is what produced the one-size template in the first place. Hence the posture taxonomy.

## Consequences

- The `comment-responder` agent and the rewritten `youtube-comment-response-guide.md` implement this split; `/engage --respond` routes through the agent.
- **Re-litigation guard:** a future pass that surfaces "the comment guide dropped its citation rule — restore it" should be answered with this ADR. The rule was not dropped; it was scoped to Drive-by corrections. If the split ever proves wrong, supersede this ADR rather than silently re-adding the block.
- The drive-by CTA remains the one place comment replies still drive traffic to the video — that funnel is intact, just no longer misapplied to discussion threads.
