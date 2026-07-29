# THUMBNAIL CRAFT RECIPE — how to make a clickable thumbnail (evidence-grounded)

**Built:** 2026-06-14. **Status:** canonical thumbnail *craft* reference. Companion docs: `tools/benchmark/PER-CHANNEL-THUMBNAIL-PLAYBOOK.md` (picks the *operation* by topic shape) and `tools/benchmark/OUTLIER-THUMBNAIL-CORPUS.md` (the outlier evidence). This doc is the *execution* layer — turning a chosen operation into pixels that get the click.

---

## The core truth (read first)

**There is no pre-publish "clickability score."** Clickability is decided in the wild — by live CTR, not any pre-publish number. (Two distinct live signals, don't conflate: native **Test & Compare** = the *variant* winner; reach-window `ctr_snapshots` = the CTR *trend*. At this channel's traffic A/B isn't viable yet, so the operative verdict is the reach-window trend + SINGLE-VARIABLE before/after swaps.) Everything before publish is either a **necessary-condition FILTER** (clarity, legibility, no-duplication — kills broken thumbnails) or an **operation prior** (copy what demonstrably earned 3x). A tool that rates a thumbnail "100/100 clickable" before publish (the old CLIP-differentiation audit) is lying — *differentiation ≠ clickability* (a low-info blob is "differentiated").

The pipeline:
**clarity + curiosity-gap + 160px legibility (filters)** → **operation from real outliers (prior)** → **live CTR (the only verdict — Test & Compare variant winner / reach-window trend)** → feed the winner back into the proven-recipes appendix below.

Every rule is tagged by evidence strength: **[T1 proven]** (rely on it) · **[T2 heuristic]** (directional, confounded) · **[T3 hedge]** (opinion — A/B-test it, don't enforce).

---

## The rules

### [T1] 1. Clarity — ONE focal point, ≤3 elements, reads in ~1 second
The single most-supported principle in the field ("if you have to explain it, it fails"). Busy ≈ −23% CTR. **One subject or one clear two-side conflict.** Our own hijab loser (1.5%) failed *only* here: three co-equal panels = the eye has nowhere to land.

### [T1] 2. Curiosity gap — the overlay must NOT duplicate the title
Title and thumbnail divide labor: the title says what it is; the thumbnail raises the question / shows the result / names the charge. "THEIR COINS" over a coin, under a title that already says "…Minted Their Own Coins," is pure duplication — zero gap. A charged, *specific* word beats an abstract one ("BORDER ON TRIAL" wins; "DEPOPULATED" — abstract, no gap — lost at 1.9%).

### [T1] 3. 160px legibility floor — design at 1280×720, JUDGE at 160px
Physics of the mobile feed. If the subject + the words don't resolve at 160px, it isn't done. This is a *filter*, not a predictor. Both our losers collapse at 160px; all three winners survive.

### [T1] 4. Single focal point: 40–60% of frame, cut out + separated, high contrast
The subject fills 40–60%, sits off-center (rule of thirds), and is **cut out from its background** with rim-light / drop-shadow / darkened-blurred BG — the biggest "looks designed vs flat" lever. Edge vignette + saturation pop on the subject. De-emphasize the background.

### [T3] 5. One high-contrast accent at the focal point — but NOT because red is proven
All three winners put one red element at the focal point: the CLASSIFIED stamp (KGB), the red disputed zone
(ICJ), the red contested strip (Guatemala).
⚠ **Downgraded T2 → T3, 2026-07-28.** Across all 47 tagged videos "red pop" is **−0.67** and was formally
killed as over-fit in `CTR-THUMBNAIL-FINDINGS-2026-06.md`; restricted to the 13 meaningfully-served videos
it collapses to −0.28. Red is on 29 of 47 thumbnails, most of them cluttered-document flops, so the n=3
winners are a selection of the survivors, not evidence.
**Keep the practice, drop the claim:** one saturated accent at the single focal point is sound contrast
craft. It is not a validated channel signal, and nothing should be prescribed *because it is red*.
See `CTR-THUMBNAIL-RECOMPUTE-2026-07-28.md`.

### [T2] 6. Text — ≤3 words, ≥~100px tall, heavy stroke, ONE accent color
Bold condensed sans (Anton/Bebas/Impact/Oswald), white + 8–10px black stroke + soft shadow; one accent color (your yellow `#FFD23F` or red) on the payoff word only. Keep text ≥40–60px off edges and **out of the bottom-right** (duration badge). Short text (<4 words) ≈ +30% CTR.

### [T2] 7. The SUBJECT must be real — no AI-generated figures (AI *polish* of real material is fine)
The evidentiary subject (the face / document / artifact) must be a **real** photo or illustration, not AI-generated. Our two weak thumbnails leaned on AI-generated PEOPLE (the "DEPOPULATED" man, the "TODAY" hijab woman — both confirmed AI, 2026-06-14): a fake person on an evidence channel undermines the authenticity moat (and ~52% disengage when they suspect AI). **Fine:** AI for *invisible polish* of real source (relight, cut-out, upscale, composite real photos) and *atmospheric backdrop stylization* (a film-grade behind real elements, cf. Thermopylae A/B). **Not fine:** AI generating the subject the thumbnail asks the viewer to believe. The governing test — *does it read as AI, or fake the evidence?* Free real subjects: Wikimedia Commons / Unsplash / Pexels. (Supersedes the old "hard no-AI-image" overstatement; see ADR 0007 + `memory/feedback-thumbnail-process.md`.)

### [T3 hedge] 8. Calm/audit over dramatic — default, but A/B-test it
For educational content the guidance is "clear/calm beats dramatic" (trust + clarity) — *opinion, not proven research*, but it aligns with the channel's Calm-Prosecutor voice and the anti-RealLifeLore identity guard. **Default to the audit framing** (document, contradiction, legal/dossier charge, recognizable subject); **allow one A/B arm** to test a more dramatic/number variant, judged on real CTR (per *data-overrides-rules-for-testing*). Educational CTR of **3–6% is healthy** — don't chase MrBeast's 10%+. Hard floor regardless: the *voice gate* below.

### Voice gate (hard — overrides craft, from `VOICE-PROFILE.md`)
No RealLifeLore scale-comparison ("the size of Texas"); no culture-war / polemic signal; no verdict words (the title can declare, the thumbnail shows). The thumbnail sells **the audit** — a document, a contradiction, an evidence object, a recognizable subject + a charge. The emotion is *curiosity of the reveal*, not outrage.

---

## Operation-by-topic (which job the thumbnail does — from the playbook)

| Topic shape | Operation | What it looks like | Channel proof |
|---|---|---|---|
| Ideological / myth-bust | **COMPRESSION on a recognizable subject** | one face/subject + one charged word | Saladin draft A; (KB exemplar) |
| Treaty / legal / intelligence | **DOSSIER METAPHOR** | document/redaction/CLASSIFIED stamp aesthetic | **KGB EXPOSED 18.4%** |
| Territorial / border | **VISUAL ANSWER (simple map)** | 2–3 big color zones + **one red contested area**, ≤3 text | **ICJ 12.1%, Guatemala 8.5%** |
| Mechanism / "HOW" | **MECHANISM REFRAME** | overlay names the *thesis*, not the topic | (Kraut/Asianometry exemplar) |

**Map rule (hard-won):** a winning map is **simple — two/three big zones + one red disputed area** (ICJ, Guatemala). A *fragmented* region-blob across grey with many country labels (Kurdistan draft C) is the anti-pattern — it smears at 160px and reads "boring lecture."

---

## Proven winner recipes (reverse-engineered from real `ctr_snapshots`, 2026-06-10)

| Video | CTR | Operation | Why it works (the skeleton) |
|---|---|---|---|
| KGB EXPOSED (`UH2PddfaaR8`) | **18.41%** | Dossier + two-side conflict | 2 cut-out real faces in a clear ☭-vs-Palestine split + red **CLASSIFIED** stamp + 2-word charged overlay. Intellectual-competence trigger. |
| ICJ 2027 / 3 CASES (`XbGl1Kcspt4`) | **12.11%** | Simple map, visual answer | 2 big color zones + **one red hatched disputed area** + numbered 1-2-3 (structured-promise). Clean, high-contrast, reads at 160px. |
| Guatemala vs Belize / Border on Trial (`Y21EjQ0v9W4`) | **8.49%** | Versus + visual answer + legal charge | one **red contested strip** + two framing text blocks + "ON TRIAL" mechanism. |

### Loser autopsies (what the filter must catch)
| Video | CTR | Failed rule(s) |
|---|---|---|
| DEPOPULATED (`aSfZtrgGjwA`, slave trade) | **1.91%** | #2 curiosity-gap (abstract overlay, no charge) · #7 AI-looking figure · weak focal/illegible doc texture |
| 1200 BCE / 600 CE / TODAY (`mCR5f_ZcB5k`, hijab) | **1.48%** | #1 clarity (3 co-equal panels = no focal point) · #3 (tiny at 160px) · voice gate (polemic modern-hijab read) |

**The pattern:** winners = one focal conflict + red accent + a charged legal/dossier overlay + real materials + high contrast. Losers break #1 or #2 (and lean synthetic). A filter built on rules #1–#3 separates them.

---

## Build checklist (mechanical — for the render)
1. Pick the **operation** (table above) from the topic shape.
2. **One** hero subject/conflict, 40–60% of frame, off-center, cut out + drop-shadow/rim separation.
3. **One red accent** at the focal point (contested zone / stamp / marker).
4. Overlay: **≤3 words**, charged + specific, **not** the title's words; ≥100px; heavy stroke; one accent color; out of bottom-right.
5. Edge vignette; saturation pop on subject; high subject-to-background contrast (the shelf is black — pop *out* of it, don't match it).
6. **Shrink to 160px** — subject + words must read instantly. If not, enlarge (don't add).
7. Voice gate: audit not stakes; no scale-comparison; no polemic; no verdict words.
8. Build **3 variants** for native A/B; ship together; let `ctr_snapshots` pick the winner; add the winner here.

*Pre-publish checks (`thumbnail_checker`, `thumbnail_image_audit`) verify rules #1–#4 + voice as FILTERS — they do not predict the winner. A/B does.*
