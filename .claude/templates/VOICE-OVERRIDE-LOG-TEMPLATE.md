# VOICE-OVERRIDE-LOG — [project-slug]

> Per-project log of voice rules the **creator overrode during read-aloud**. The
> read-aloud is the T1 voice gate; when he changes a line away from what
> `VOICE-PROFILE.md` / the linter predicted, record it here. Over time these
> overrides sharpen the canonical profile (and the linter) — they are the
> use-and-correct loop's raw data.
>
> **How to use:** during/after the read-aloud pass, append one row per override.
> Keep the creator's exact replacement wording. When a pattern recurs across
> projects, promote it to `.claude/REFERENCE/VOICE-PROFILE.md` (and, if literal,
> to `tools/voice_lint.py`). Do NOT automate — this is a hand-kept ledger.

| Date | Rule / linter id | What it predicted | What he changed it to | Keep as one-off or promote? |
|------|------------------|-------------------|-----------------------|-----------------------------|
|      |                  |                   |                       |                             |

## Notes

- Link the canonical rule each override touches, e.g. `VOICE-PROFILE.md` "Transitions" or linter rule `staccato-triplet`.
- A one-off override (topic-specific) stays here. A pattern seen 2+ times across projects = promote to the profile.
