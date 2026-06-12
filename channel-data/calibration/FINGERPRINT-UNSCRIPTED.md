# FINGERPRINT-UNSCRIPTED.md — deep linguistic fingerprint of the gold standard

> **Source:** `yt:yMAWJcjo_ug` — the creator's first, fully unscripted video (channel intro). Transcript: `transcripts/voice-analysis-unscripted.en.vtt`, cleaned (rolling-caption overlap-join) as preserved in `channel-data/fable-digests/D2-voice-triad.md` SAMPLE A. Re-tokenized and measured 2026-06-12 (UPGRADE-PLAN S5).
>
> **Status per VOICE-PROFILE.md:** this video is the canonical voice gold standard ("MORE explanatory than the SRTs/spec"). This file goes BELOW the profile's top-level rules into quantitative distributions, to feed voice_lint thresholds (S11).
>
> **Sample-size caveat (read first):** ONE video, **741 words, 39 sentences**. Every number below is a single-sample point estimate, not a stable rate. Treat thresholds derived here as starting values to tune, never hard gates. Also: this is his *nervous first recording* in pure conversational register — scripted-delivery comparisons must go through VOICE-PROFILE, which supersedes on conflict.
>
> **ASR artifacts (do not fingerprint these):** "Brainard" = *brainrot*; "statethood" = *statehood*; "le lesson" = *lesson*; "u"/"re reality" = ASR stutter-splits. The 77-word max "sentence" is an ASR punctuation gap, not a real syntactic unit.

---

## 1. Sentence-length distribution

| Metric | Value |
|---|---|
| Sentences | 39 |
| Mean length | 19.0 words |
| Median length | 13 words |
| Max | 77 (ASR run-on artifact — real ceiling nearer ~40) |

Histogram (words per sentence):

| Bucket | Count | Share |
|---|---|---|
| 1–5 | 5 | 13% |
| 6–10 | 8 | 21% |
| 11–15 | 10 | 26% |
| 16–20 | 6 | 15% |
| 21–30 | 5 | 13% |
| 31+ | 5 | 13% |

**Reading:** broad, flat distribution — modal 11–15 but a real quarter of sentences run 21+ words. He is NOT a short-sentence speaker. Confirms the VOICE-PROFILE reversal (flowing/explanatory, clipped-gavel was over-applied). Short sentences (1–5 words) exist but are sparse (~13%) and functional ("So, here I am…", "See you."), not dramatic fragments.

## 2. Connector inventory (frequencies, per 741 words)

| Connector | Count | /100w | Note |
|---|---|---|---|
| and | 26 | 3.5 | dominant chainer; also sentence-initial ×6 |
| so | 9 | 1.2 | his #1 causal; sentence-initial ×6 of 9 |
| but | 7 | 0.9 | pivot of choice, often "But just because…" |
| because | 4 | 0.5 | in-clause cause |
| the reason why | 1 | 0.1 | heavier causal frame, rare |
| which is why | 0 | 0 | **absent** in unscripted speech |
| and that meant | 0 | 0 | **absent** in unscripted speech |
| consequently / thereby | 0 | 0 | absent (as the style guide predicts) |

**Reading:** the spoken-register causal stack is `so` ≫ `because` > `the reason why`. The style guide's "which is why / and that meant" connectors are *writer's tools* — fine, but they are not his unscripted defaults; over-density of them would be a tell.

## 3. Fillers, hedges, intensifiers

| Item | Count | /100w | Lint relevance |
|---|---|---|---|
| uh | 27 | 3.6 | speech-only; baseline comfort marker, never scripted |
| um | 25 | 3.4 | speech-only |
| like (filler/approx) | 11 | 1.5 | survives in his scripted ad-libs at low rate |
| I guess | 3 | 0.4 | clause-FINAL hedge ("…I guess") — signature placement |
| I think | 3 | 0.4 | verdict-softener |
| kind of / some kind of | 3 + 2 | 0.7 | approximator family ("some kind of counterbalance") |
| basically | 3 | 0.4 | confirmed HIS word (VOICE-PROFILE "basically OK") |
| you know | 1 | 0.1 | rare — NOT a habit |
| very | 9 | 1.2 | **his intensifier** ("very first," "very little basis," "very good reason") |
| really | 0 | 0 | **zero** — "really" as intensifier is not him |

## 4. How he opens a thought

Sentence-initial words (after stripping uh/um): **I/I'm (8)**, **So (6)**, **And (6)**, But (3), then content-first. Patterns:
- **First-person launch:** "I'm passionate about…", "I know that…", "I hope to be…" — he enters through his own stance, not through "Here's" or "Now".
- **"So" as resumption**, not conclusion: "So, here I am doing something…", "So, this is what I'm going to try and combat, I guess."
- **"And"-chaining** across sentence boundaries when extending a case.
- Zero instances of "Here's", "Now,", "Look,", "Listen" — the YouTuber-opener set is absent.

## 5. How he closes a thought

- **Trailing hedge:** "…I guess." ×3, "…to reach as many people as possible. And um yeah…" — closes soften, they don't punch.
- **"yeah" as paragraph-final exhale:** "And um yeah, basically…", "Um so yeah, there will be a time lapse, I hope".
- **Scope-back qualifier at the end:** "…at least in the historical community, to be false."
- He does NOT close on aphorisms or mirrored binaries (consistent with 56-12's lock-stage cut of exactly that).

## 6. Question frequency

**Zero questions in 39 sentences.** The unscripted register is entirely declarative — even invitations are imperatives ("please send it my way," "ask me to debunk something"), not rhetorical questions. Squares with 56-16 (stagey rhetorical questions get cut at lock) and refines 57-28: the *one* question type he produces under pressure is a genuine setup-question he immediately answers; free-floating rhetorical questions have a true baseline of ~0.

## 7. Self-correction patterns

16 immediate-repetition events in 741 words (~2.2/100w): "the the the", "to to see", "that that are known", "market market them", "I I I try". Mechanism: he **stutter-repeats the function word and pushes forward** — he never abandons and re-casts the sentence, never says "let me rephrase," never apologizes mid-thought. Restarts preserve the original syntactic plan. (Speech-only marker; script implication is rhythm, not transcription: his delivery absorbs imperfection without resetting.)

## 8. Idiolect phrases (recurring/distinctive word choices)

- **"counterbalance"** ×2 — "provide some kind of counterbalance" (the channel mission noun).
- **"sick and tired of seeing… misinformation"** — indignation formula, mild not hot.
- **"rot your brain" / "brainrot"** — internet-native vocabulary deployed casually.
- **"send them my way"** ×2 — audience-as-collaborators.
- **"You don't have to take my word for it, but please look into these things"** — the empowerment move that later became the channel method line ("go to the document and read it," #57 CTA).
- **"figure things out for yourself"**, "means to…" — agency vocabulary.
- **Latinate singletons embedded in plain speech:** "propagate," "fantastical," "misinterpreted" — one elevated word per plain sentence, never clusters.
- **"turn you into a parrot"** — concrete-image mockery of bad pedagogy; dry, not sneering.
- **"cool and edgy and flashy"** — triple-adjective dismissal-by-listing, polysyndeton with "and".
- **Politeness bookends:** "Hello everybody" / "thank you very much" / "I hope you stick around" (×2 — opening and final line).

## 9. voice_lint threshold candidates (S11 input — starting values, single-sample)

| Proposed check | Threshold (start) | Basis |
|---|---|---|
| `really` as intensifier | WARN at ≥1 per script if `very` available | really=0 vs very=9 here |
| Free-floating rhetorical question (no immediate answer) | WARN each | baseline 0/39 sentences |
| Sentence-length profile | WARN if median <10 or >22 words per beat | median 13, mean 19; protects flowing register from clipped-gavel AND from run-on |
| Fragment share | WARN if 1–5-word sentences >20% of script | 13% baseline, functional not dramatic |
| "which is why"/"and that meant" density | WARN if combined >2 per script | 0 baseline; writer's tools, ration them |
| YouTuber-opener set (Here's/Now,/Look,/Listen) | existing "here's" cap stands; add Now,/Look, at WARN | absent in gold |
| Clause-final hedge presence on verdict beats | INFO if a verdict paragraph has zero hedge (I think/I guess/kind of) | hedge family ~1.5/100w is constitutive |
| Intensifier "very" | do NOT flag — it's him | very=1.2/100w |

## 10. The ten strongest fingerprint markers

Mirrored as corpus entries GS-01..GS-10 in `CALIBRATION-CORPUS.md` (tier VALIDATED — it IS him; scope: unscripted conversational register, VOICE-PROFILE supersedes on conflict).

1. Flat, wide sentence-length distribution centered 11–15w with a real 21+w tail — flowing, not clipped.
2. Causal stack = so ≫ because; "which is why"/"and that meant" are absent in natural speech.
3. Zero rhetorical questions; invitations are imperatives.
4. First-person stance openers (I/I'm/I know/I hope) over presentational openers.
5. Clause-final hedging ("…I guess") and "yeah"-exhale closes; never aphoristic closes.
6. "very" is the intensifier; "really" doesn't occur.
7. One Latinate word per plain sentence; elevation never clusters.
8. Audience-as-collaborator imperatives ("send them my way") — the engagement register.
9. Dry concrete-image mockery ("turn you into a parrot"), triple-adjective dismissals.
10. Push-through self-correction — repeats the function word, never re-casts the sentence.
