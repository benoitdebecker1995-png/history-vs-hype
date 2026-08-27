# MORTALITY — the defensible range of excess deaths

**Question:** how many people died, by whose method, and what does the disagreement actually turn on?
**Status of this file:** ✅ **COMPLETE.** Read in full: Dyson & Maharatna 1991 (D1); Maharatna 1994
(D13) incl. Tables 1–2 from page images; Maharatna LSE thesis 1992 Ch. 5 incl. Table 5.4; Sen 1981
Appendix D; FIC *Report on Bengal* Part II. Maharatna 1993 (D6) read for the district-ecology finding
only. Remaining gaps listed at §8.
**Date:** 2026-07-31

---

## THE ANSWER, UP FRONT

**The defensible range is 1.8 to 2.4 million excess deaths, centring on ~2.1 million.** Both bounds
are the *same* study's sensitivity band, and the thing that moves them is not history — it is one
number: **how incomplete was death registration in 1943–44.**

Three findings that change how the script must talk about this:

1. **⚠ The framing in `01-VERIFIED-RESEARCH.md` is backwards.** The note says modern demography
   "revises upward" from the FIC's 1.5M to Dyson & Maharatna's 2.1M. Dyson & Maharatna are not
   revising the FIC upward — **they are revising Sen's 3 million *downward***, and they end up
   endorsing Aykroyd's position that 1.5M was too low and 3M too high (D1 p. 297). Relative to the
   FIC the direction is up; relative to the number everybody actually repeats, the direction is
   emphatically down. The paper is a debunk of 3M, not a debunk of 1.5M.

2. **⚠ The 3.5M "Chattopadhyay" figure is misattributed** — on two counts. See §6.

3. **The declining baseline is real, verified, and NOT the big mover.** It is worth roughly
   +0.2–0.3M. The big mover — worth about −1.0M off Sen — is a **data replacement**, and inside that,
   a single arithmetic error in a 1951 Pakistani census baseline. See §1.

---

## 1 — DYSON & MAHARATNA 1991, IN FULL

**Tim Dyson & Arup Maharatna, "Excess mortality during the Bengal famine: A re-evaluation,"
*Indian Economic and Social History Review* 28:3 (1991), pp. 281–297.**
File: `_research/library/articles/D1-DysonMaharatna-ExcessMortalityReevaluation-IESHR-28-3-1991-pp281-297.pdf`
Both authors, Dept. of Population Studies, LSE. Full text layer; **Tables 1–5 are image-only and did
not extract** — every figure below comes from the running prose, which states them explicitly.

### 1.1 The two aims, in their own framing (p. 282)

> *"First, we review the estimates provided by Sen… we show that major problems attach to the data he
> used… The paper's second aim is to produce new estimates of excess mortality based on the previously
> neglected material for undivided Bengal."*

They state the destination on p. 282: applying Sen's own method to better data "produces estimates of
around 1.9 million," and "even allowing for a much greater degree of death under-registration than
that used by Sen, it is difficult to see that excess mortality could have approached 3 million."

### 1.2 STEP ONE — the data replacement (the big mover: ≈ −1.0M off Sen)

**What Sen used.** Registered deaths for **West Bengal only**, from *Census of India 1951*, Vol. VI
Pt. 1B, *Vital Statistics, West Bengal 1941–50*; plus, for East Bengal, a single figure of **1.714
million** taken from the *Census of Pakistan 1951*, Vol. 3.

**What D&M found.** Registration data for **undivided Bengal, 1941–46**, in the *Annual Reports of the
Public Health Commissioner with the Government of India* for 1943–44, 1945 and 1946, plus the
*Statistical Appendices* for 1940–44 (D1 footnote 10, p. 284). Their claim about it:

> *"So far as we can ascertain, these detailed registration data for undivided Bengal have nowhere
> been used in all that has been written about the famine."* (p. 284, fn. 10)

**Kill #1 — the West Bengal series is not trustworthy (pp. 286–287).** Two defects:
- West Bengal's *share* of all registered deaths in undivided Bengal should be ~⅓ (its population
  share). In the published series it swings from **28.5% in 1942 to 36.2% in 1945** (Table 3). D&M
  judge the instability more likely to sit in the West Bengal numerator than in the all-Bengal
  denominator.
- For 1941–46 the *age distribution* of deaths in *Vital Statistics, West Bengal* is **identical in
  every one of the six years** — a flat pro-ration, "although no warning of this stark pro-ration is
  provided to the unsuspecting reader" (p. 287). **This misled Sen** into concluding the age pattern
  of mortality did not change during the famine (p. 287, fn. 12).

**Kill #2 — the East Bengal 1.714M is built on a broken baseline (pp. 287–288).** This is the single
most consequential correction in the paper. The Pakistan census figure is an arithmetic construction:

    total registered deaths, East Bengal 1942–44  =  3,335,000
    minus 3 × "quinquennial normal average" of      540,000/yr
    =  1,715,000  ("1,714,000" as printed — D1 fn. 14 notes the misprint)

D&M's objection: **there is no valid basis for a 540,000 normal.** Undivided Bengal registered an
average of **1,184,903 deaths a year in 1938–42**; East Bengal was about ⅔ of that, i.e. **≈790,000**.

> *"The origins of the figure of 540,000 may never be known. But it is a gross underestimate, which
> introduces a massive upward bias into the above calculation of 1.714 million excess deaths."* (p. 288)

**Substituting 790,000 gives 965,000 excess deaths for East Bengal 1942–44** (p. 288, fn. 17) — a cut
of ~750,000, i.e. **~44% of Sen's East Bengal component evaporates on one baseline correction.**

**Result of step one.** Running Sen's *own* procedures and *own* stationary norms over the undivided-
Bengal data yields **1.8 million (norm A) and 1.9 million (norm B)** — Table 2, p. 285.
Against Sen's 2.62 / 2.73 / 2.72 / 3.05, that is the whole of the reduction.

### 1.3 STEP TWO — the declining baseline. VERIFIED, and quantified (pp. 291–295)

**The brief's hypothesis is correct.** D&M do replace a flat baseline with a fitted declining trend.
The mechanics, from p. 292:

1. Take the 1931 and 1941 censuses for mid-year populations under registration; assume a constant
   **1.88% p.a.** growth between them; interpolate 1931–42 mid-year populations.
2. Combine with registered deaths → **registered crude death rates (CDRs) for 1931–42**.
3. **Fit a least-squares regression line to the 1931–42 registered CDRs** and extrapolate it to
   1943–46 — i.e. what the death rate *would have been* had the pre-war decline continued.
4. That trend line implies registered CDRs of **19.44 in 1943 and 19.19 in 1944** absent famine
   (p. 292). (≈ −0.25 per mille per year of continuing mortality decline.)
5. Adjust *both* the observed and the counterfactual CDRs upward by a correction factor (CF) for
   under-registration.

**Worked example they give (p. 295), which shows the machinery exactly:**

> 1943 under assumption 2: **1,061,765 excess deaths = (46.47 − 29.35) × 62,019**

— where 46.47 is the CF-adjusted actual 1943 CDR, 29.35 the CF-adjusted counterfactual, and 62,019
the mid-year population in thousands. Note **29.35 = 19.44 × 1.51**: the counterfactual is the fitted
declining trend, grossed up by Jain's CF. That confirms the mechanism beyond inference.
(Parallel check, p. 295 fn. 24: assumption 1's 1943 CDR = 40.57 = (1.32 × 1,908,622)/62,107.)

### 1.3a THE FULL CALCULATION, RECOVERED — the numbers D1's image-only table would not give

D1's Table 5 did not extract. **But the same table survives as machine-readable text in Maharatna's
LSE thesis as Table 5.4** (`C2thesis…pdf`, PDF p. 230 = printed **p. 228**). It reproduces D1's Panel A
and B exactly, and it recovers the whole apparatus. Everything below is transcribed from it.

**The declining baseline, as an equation** (thesis p. 228, note iii):

> **CDR = 506.098 − 0.25052 × (YEAR)** — least-squares line fitted to registered CDRs, 1931–42.

That is the entire "declining trend" in one line: **registered mortality in Bengal was falling by
0.25 per thousand per year** through the 1930s, and D&M charge the famine with the gap between what
happened and where that line was heading.

**Panel A — registered deaths, registered CDR, and the extrapolated counterfactual:**

| Year | Registered deaths | Registered CDR | Counterfactual CDR (trend) |
|---|---|---|---|
| 1938 | 1,315,886 | 23.05 | — |
| 1939 | 1,090,530 | 18.75 | — |
| 1940 | 1,111,082 | 18.75 | — |
| 1941 | 1,184,850 | 19.62 | — |
| 1942 | 1,222,164 | 19.86 | — |
| **1943** | **1,908,622** | — | **19.44** |
| **1944** | **1,726,870** | — | **19.19** |
| 1945 | 1,238,133 | — | 18.94 |
| 1946 | 1,068,996 | — | 18.69 |

*(Note 1941 → 1942: registered deaths **rise**, 1,184,850 → 1,222,164. Sen's West Bengal series shows a
sharp **fall** across the same two years. That single divergence is what inflates Sen's baseline.)*

**Panel B — excess deaths, year by year, under each correction factor:**

| Year | Assumption 1 (CF 1.32) | Assumption 2 (CF 1.51) | Assumption 3 (CF 1.70) |
|---|---|---|---|
| 1943 | 926,015 | **1,061,765** | 1,194,991 |
| 1944 | 743,373 | **862,852** | 980,520 |
| 1945 | 119,948 | **153,036** | 183,740 |
| 1946 | *(below trend — none)* | *(below trend — none)* | *(below trend — none)* |
| **Total** | **1,789,336 → 1.8M** | **2,077,653 → 2.1M** | **2,359,251 → 2.4M** |

The published totals reproduce exactly. **Two-thirds of the deaths fall in 1943, essentially all the
rest in 1944, and 1945 contributes about 7%.** 1946 is *below* the trend line and contributes nothing.

**This finally lets the declining baseline be priced precisely.** Sen's flat norm B is 1942's registered
CDR of 19.86. The trend counterfactual is 19.44 (1943), 19.19 (1944), 18.94 (1945) — gaps of 0.42,
0.67 and 0.92 per mille. On the relevant mid-year populations and grossed by Jain's CF 1.51, that is
roughly **39,000 + 61,000 + 83,000 ≈ 185,000 additional excess deaths**.

> **The declining baseline is worth about 185,000 deaths — under 9% of the total.** It is a real and
> correct refinement, and it is not what the argument is about.

*(Also from Panel A: registered infant mortality per 1,000 live births ran 155.7 in 1941 and 154.3 in
1942, then **195.4 in 1943 and 207.9 in 1944** — peaking in 1944, not 1943 — before dropping to 143.2
in 1945, marginally *below* the 1931–42 trend. D1 p. 296 treats that last fact as its strongest
independent evidence that famine mortality really did end in 1945.)*

### 1.4 THE ESTIMATE UNDER EACH BASELINE ASSUMPTION — the table the brief asked for

| Baseline for "normal" mortality | Registration correction factor (deaths) | Total excess deaths | Locator |
|---|---|---|---|
| **Flat** — Sen's norm A (avg 1941–42), undivided-Bengal data | Jain 1.51 | **1.8M** | D1 Table 2, p. 285 |
| **Flat** — Sen's norm B (1942 alone), undivided-Bengal data | Jain 1.51 | **1.9M** | D1 Table 2, p. 285 |
| **Declining fitted trend 1931–42** | Chowdhury **1.32** (assumption 1) | **1.8M** | D1 pp. 291, 295–296 |
| **Declining fitted trend 1931–42** | Jain **1.51** (assumption 2) | **≈2.1M** ← preferred | D1 pp. 291, 296 |
| **Declining fitted trend 1931–42** | arbitrary **1.70** (assumption 3) | **2.4M** | D1 pp. 291, 295–296 |
| Declining trend | 2.00 (hypothetical) | 2.8M | D1 p. 297, fn. 30 |
| Declining trend | would need registration **well under 50%** | 3.0M | D1 p. 297 |

**Read the table this way.** Swapping the flat baseline for the declining trend, *holding the
correction factor at Jain's 1.51*, moves the estimate from ~1.9M to ~2.1M — **worth about +0.2M,
roughly 10%.** Swapping the correction factor from 1.32 to 1.70, *holding the baseline fixed*, moves
it from 1.8M to 2.4M — **worth 0.6M, roughly 33%.** So:

> **The declining baseline is real but second-order. The disagreement lives almost entirely in the
> registration correction factor — i.e. in how many deaths were never written down.**

Their verdict on which to use (p. 296):

> *"In our view the rough figure of 2.1 million excess deaths arising from assumption 2 is probably as
> good as any."*

And on the upper end (p. 296): the 2.4M figure "is based upon an arbitrary assumption regarding the
level of registration completeness. We know of no strong grounds for considering that the average
level of death registration in 1943–44 was less than 60 per cent."

### 1.5 The FIC's implied correction factor, reverse-engineered — a genuinely good exhibit

D1 footnote 18 (pp. 288–289) reconstructs what the Famine Inquiry Commission *implicitly* assumed
about its own data quality:

- Registered deaths 1943: **1,873,749** (Bengal Public Health Dept).
- Quinquennial average 1938–42: **1,184,903**. Registered excess: **688,846**.
- FIC rounded 688,846 up to "of the order of one million" → an implied CF on the *excess* of 1.45.
- But that means the FIC believed total 1943 deaths were 1,184,903 + 1,000,000 = **2,184,903** …
- … which implies it thought registration in 1943 was **86% complete (CF ≈ 1.16)**.

**Jain's CF is 1.51 — registration only 66% complete.** That single divergence, 86% vs 66%, is most of
the distance between the 1945 official finding and the modern figure. It is the whole argument in one
comparison and it is fully sourced on both sides.

### 1.6 What D&M concede against themselves (pp. 295, 297)

They list their own soft joints, which is why the paper is usable: the choice of 1931–42 as the trend
window ("use of a different period would alter the results"); the assumption that Bengal grew at its
intercensal rate through mid-1942 in the absence of migration data; whether 1945 and 1946 should count
at all; and the provisional status of the 1946 registration numbers. Their judgement is that these are
"probably relatively minor… in comparison with the fundamental issue of death registration
completeness" and partly offsetting (p. 295).

They also concede that the 1.5M–vs–3M argument does not carry the moral weight people load onto it:

> *"If a lower figure is indicated this in no way alters the fundamental issues of the causes of, and
> responsibilities for, what was undoubtedly a massive crisis."* (p. 297)

And they note something the video should not drop: **there was substantial excess mortality elsewhere
in India in 1943–44 — some of it in Orissa, probably out-migrants from Bengal** (p. 297 and fn. 31).
Bengal-only counting therefore understates the event's death toll, in a direction nobody has measured.

---

## 2 — MAHARATNA 1994 AND THE LSE THESIS

### 2.1 Maharatna 1994 — no revision; it turns to *how* and *when*, not *how many*

**Arup Maharatna, "The demography of the Bengal famine: A detailed study," IESHR 31:2 (1994),
pp. ~169–216.** File: `…/articles/D13-Maharatna-DemographyOfBengalFamineDetailedStudy-IESHR-31-2-1994.pdf`

It **restates 2.1M without amendment** and does not re-run the estimate:

- p. 171: Dyson & Maharatna "arrive at a figure of 2.1 million excess deaths for the whole of undivided
  Bengal. Thus, the Famine Inquiry Commission's *Report on Bengal* almost certainly provides an
  underestimate of famine mortality of only 1.5 million excess deaths."
- p. 211 (Conclusions): *"Excess deaths were probably around 2.1 million."*

**Where it moves the ground instead — the timing envelope (p. 172, p. 211).** Using the undivided-Bengal
data, famine excess mortality **began June 1943 and lasted to the middle of 1945**; the main peak was a
**12-month window, July 1943 – June 1944**; proportional excess mortality peaked in **October 1943**.
This settles a live dispute in Sen's favour on one point and against him on another: Sen was right that
mortality did not stop in June 1944 (the FIC's cut-off), but wrong that it ran to 1946.

**Where 1994 disagrees with Sen, explicitly (p. 173):** on age and sex patterns. Sen concluded from the
West Bengal data that age/sex differentials were much as in normal times; Maharatna says that
conclusion is an artefact of the pro-rated table. On the undivided-Bengal data, the largest
proportional rises were among **older children (10–14) and adults**; infants, young children and the
elderly rose proportionally *least*; male death rates rose more than female in 1943, especially in the
prime reproductive years, with infancy the exception.

**Where the 1994 paper disagrees with the hinge file's framing:** p. 211 calls the famine a "classic
example of what is often termed a 'class famine'" and says "this crisis was not directly caused by a
food shortage as such." That is Maharatna adopting Sen's causal reading in a passing sentence, and it
sits against the settled hinge verdict. It is not a demographic finding and carries no data in this
paper — **do not cite the 1994 conclusion as evidence on the availability question.** Cite it only for
mortality magnitude, timing and cause-composition.

### 2.2 The LSE thesis (1992) — READ. No revision, and it is the better citation

**Arup Maharatna, "The demography of Indian famines: A historical perspective," PhD thesis, LSE, 1992,
425pp.** Bengal mortality is **Chapter 5, printed pp. ~215–232** (PDF pagination = printed + 2).

**It does not revise the figure. It is D1's argument at length, with the same numbers:**
- "Our chief criticism of Sen's estimates relates to the data he used" — printed **p. 218**, the same
  sentence as D1 p. 284.
- The FIC's implied correction factor of **1.16** — printed **p. 226** (the long-form of D1 fn. 18).
- **Table 5.4**, printed **p. 228** — Panels A and B in full, totals 1.8 / 2.1 / 2.4 million (§1.3a).
- "the implied range of famine mortality is between 1.8 and 2.4 million excess deaths" — printed
  **p. 231**, verbatim as D1 p. 296.

**One sentence the thesis adds that the article does not, and it is the best framing available**
(printed p. 231):

> *"…the rough figure of 2.1 million excess deaths arising from assumption 2 **(and embodying precisely
> the same correction factor for death under-registration as was used by Sen)** is probably as good as
> any."*

That parenthesis is the argument's keystone. **D&M do not reach a lower number by assuming better
record-keeping than Sen did.** They use Sen's correction factor, Sen's method, and a *more* generous
(declining) baseline than Sen used — and still land at 2.1M, because the data underneath are different.
It forecloses the obvious objection before it is made, and it is the line to put in front of anyone who
says the lower figure is a whitewash.

**Where the thesis disagrees with nothing:** searched Chapter 5 for any revised total. The only figures
present are 1.8 / 2.1 / 2.4, identical to 1991 and to 1994. **Across three publications spanning
1991–1994, Maharatna's number never moves.**

---

## 3 — SEN'S ~3 MILLION: THE ACTUAL RECONSTRUCTION

**Amartya Sen, *Poverty and Famines* (Clarendon, 1981), Appendix D, "Famine Mortality: A Case Study,"
pp. 195–216.** Read in full text from
`library/by-topic/colonialism-slavery/PovertyAndFaminesEntitlementAndDeprivation-Sen-1981-ClarendonPress.pdf`.

### 3.1 The method, step by step

1. **Data.** Registered deaths, **West Bengal only**, 1941–50, from *Census of India 1951*, Vol. VI
   Pt. 1B (Table D1, p. 200).
2. **Two "normal" baselines**, both flat: **A** = average of 1941 and 1942; **B** = 1942 alone (p. 200).
   Sen chooses these *specifically to improve on the FIC*: because registered deaths fell every year,
   "the Famine Inquiry Commission's procedure of taking the average mortality in the previous
   quinquennium as the 'normal' mortality may understate excess mortality" (p. 200).
   **Note: Sen identified the declining-trend problem himself; he simply did not model it.** He says
   even B understates it "since the relevant comparison is not with the level in the prefamine year,
   but with the level to which the expected death rates would [have fallen]" (p. 200).
3. **Time window.** Summing until excess disappears gives 648,000 (A) / 784,000 (B). To be
   conservative he cuts at 1946 → **601,000 (A) / 673,000 (B)** registered excess (p. 201).
4. **Under-registration.** Jain's reverse-survival method → deaths under-registered by **33.9%** in
   1941–50, so actual mortality is **51% above registered** (p. 199). Applied → **908,000 (A) /
   1.016M (B)** for West Bengal (p. 201).
5. **Scaling to undivided Bengal — two routes** (pp. 201–202):
   - **add** the *Census of Pakistan 1951* East Bengal figure of **1.714M** → **2.622M / 2.730M**;
   - **or multiply West Bengal by 3** (its population and pre-1943 registered-death share were each
     almost exactly ⅓) → **2.724M / 3.048M**.
6. **Then argue three downward biases** and round up (p. 202): the uniform CF understates 1943, when
   registration was worst; the stationary norm ignores the pre-war mortality decline; the East Bengal
   figure stops at 1944 while West Bengal shows excess to 1946.

> *"we may be inclined to pick a figure around 3 million as the death toll of the Bengal famine. (It
> has also the merit of being a 'round' number…)"* — p. 202.

**Sen's own Table D2 (p. 202) — his summary of the field:**

| | Excess mortality 1943 (m) | Total excess (m) |
|---|---|---|
| Famine Inquiry Commission | 1.00 | 1.50 |
| K. P. Chattopadhyaya | 2.20 | 2.70 |
| Assumption A + Pakistan Census | 1.17 | 2.62 |
| Assumption B + Pakistan Census | 1.25 | 2.73 |
| Assumption A blown up ×3 | 1.17 | 2.72 |
| Assumption B blown up ×3 | 1.25 | 3.05 |

### 3.2 Why Sen lands ~50% high — the gap, located precisely

The gap is **not** in the correction factor. Sen and D&M both use Jain's 1.51. It sits in **three
places, in descending order of size**:

| Source of the gap | Size | Which assumption |
|---|---|---|
| **The East Bengal baseline** | ≈ **0.75M** | Sen imports 1.714M whole from the Pakistan census; that figure subtracts a "normal" of 540,000/yr for East Bengal where the registration data imply ~790,000. Correcting it gives 965,000 (D1 p. 288, fn. 17). |
| **The West Bengal series itself** | ≈ **0.2–0.3M** | Sen's 1942 figure is anomalously *low* (28.5% of all-Bengal deaths vs an expected ⅓), which inflates *both* his A and B excesses. The undivided-Bengal data show deaths rising slightly 1941→1942, not falling sharply (D1 p. 285). |
| **The tail to 1946** | ≈ **0.1–0.2M** | Sen counts excess through 1946. D&M find excess ends mid-1945; the all-India Public Health Report for 1945 says the deterioration in Bengal "gradually disappeared by the middle of the year 1945" (quoted D1 p. 285). |
| *(offsetting, in Sen's favour)* | −0.2M | Sen's flat baseline **understates** excess. D&M's declining trend, applied to Sen's data, would have pushed him *higher*, not lower. |

**The one-sentence version for the script:** *Sen's higher number is not a different reading of the
famine. It is one 1951 Pakistani census table with an unexplained normal-mortality figure roughly
250,000 a year too low, compounded over three years.*

### 3.3 What Sen gets right that survives entirely

- **He identified the flat-baseline problem before anyone corrected it** (p. 200) — D&M's headline
  refinement is Sen's own stated third bias, implemented.
- **His "How did they die?" analysis (D.3, pp. 203 ff.) is not touched by any of this.** See §4.
- Sen also catches a **second FIC internal inconsistency**, distinct from the 1.3M/1.5M one already in
  the project file: the FIC's own correction of 688,846 → 1,000,000 is **+45%**, but the report
  describes it as "some 40 per cent" (Sen p. 201, fn. 326, citing FIC p. 109). Two arithmetic
  inconsistencies inside one report is a pattern, not a typo.

---

## 4 — THE DISEASE MECHANISM: IS "STARVED TO DEATH" ACCURATE?

**Short answer: no, not for most of the dead — and the sources say so in the strongest possible terms.
But "died of malaria, not of the famine" is equally wrong, and the same sources say that too.**

### 4.0 THE DEFINITIVE DECOMPOSITION — Maharatna 1994, Table 1, printed p. 181 ⭐

**This is the number the script should use.** Read from the page image (the table has no text layer).
D13 Table 1, "Cause-specific Death Rates and Relative Importance of Different Causes of Death during
Pre-famine and Famine Periods: Bengal," printed **p. 181** (PDF p. 13). Source: *Bengal Public Health
Report*, various years. Rates per 1,000 on a constant 1941-census denominator. **Figures in brackets
are each cause's share of *total average annual deaths* for 1937–41, and its share of *total excess
deaths* for 1943 and 1944.**

| Cause of death | 1937–41 rate (share of all deaths) | 1943 rate (**share of excess**) | 1944 rate (**share of excess**) |
|---|---|---|---|
| Cholera | 0.73 (3.72%) | 3.60 (**23.88%**) | 0.82 (0.99%) |
| Smallpox | 0.21 (1.06%) | 0.37 (1.30%) | 2.34 (**23.69%**) |
| Fever *(excl. malaria)* | 6.14 (31.08%) | 7.56 (11.83%) | 6.22 (0.91%) |
| **Malaria** | 6.29 (31.82%) | 11.46 (**43.06%**) | 12.71 (**71.41%**) |
| Dysentery and diarrhoea | 0.88 (4.47%) | 1.58 (5.83%) | 1.08 (2.27%) |
| Respiratory | 1.52 (7.67%) | 1.30 (**−1.82%**) | 1.39 (**−1.44%**) |
| Injury | 0.37 (1.86%) | 0.33 (−0.33%) | 0.27 (−1.05%) |
| All other | 3.32 (18.32%) | 5.57 (16.26%) | 3.91 (3.23%) |
| **All causes (CDR)** | **19.46** (100%) | **31.77** (100%) | **28.75** (100%) |

**What this table establishes, and it is the strongest evidence in this file for the wording verdict:**

- **Malaria alone: 43% of the excess deaths in 1943, and 71% in 1944.** Not a contributing factor — the
  single largest cause, by a distance, in both years.
- **The famine changed diseases as it went.** 1943 is a cholera-and-malaria year (67% of excess between
  them); 1944 is a malaria-and-smallpox year (**95%** between them). Cholera collapses from 23.88% to
  0.99%; smallpox rises from 1.30% to 23.69%. Whatever killed people in the autumn of 1943 was not what
  killed them in the spring of 1944.
- **"Dysentery and diarrhoea" is only 5.83% / 2.27% of excess deaths.** This constrains Sen's argument
  (§4.3) that starvation deaths hid inside that category — the category is too small to hold them. If
  starvation deaths were relabelled, they went mostly into *malaria*, *fever* and *all other* (16.26%
  in 1943, and D13 p. 185 shows "all other" is exactly where urban destitute deaths landed).
- **Respiratory and injury deaths go NEGATIVE** — *fewer* than normal, in both years. Sen noticed the
  respiratory fall too (D13 p. 185, fn. 48). It is a good detail: the famine did not raise all-cause
  mortality uniformly; it raised the *infectious* causes and suppressed others, which is what makes the
  "they'd have died anyway" line untenable.
- **The registered crude death rate ran 19.46 normal → 31.77 in 1943 → 28.75 in 1944.** Roughly a 63%
  rise, on numbers that everyone agrees are undercounts.

**⚠ Reconciling with the FIC (§4.1):** the FIC gives malaria 41.5% of 1943 excess and 53.0% of
January–June 1944 excess. Maharatna gives 43.06% and 71.41%. They are not in conflict — the FIC's 1944
figure covers only the first half of the year, and Maharatna covers all of it, using a 1937–41 baseline
where the FIC used 1938–42. **Cite Maharatna's; mention the FIC's only if a 1945-dated source is
wanted on screen.**

### 4.0a Public health spending arrived after the dying — D13 Table 2, printed p. 181

Same page, read from the image. Government of Bengal expenditure, in rupees:

| Year | Public Health Establishment | Expenses on epidemic diseases | Total expenditure |
|---|---|---|---|
| 1941–42 | 650,985 | 726,496 | **3,929,486** |
| 1942–43 | 614,585 | 942,122 | **3,595,021** ← *falls* |
| 1943–44 | 626,616 | 2,706,933 | 6,025,472 |
| 1944–45 | 735,977 | **7,146,172** | **10,929,958** |

**Total public health spending fell in 1942–43** — the year the famine developed — and epidemic
spending does not reach its peak until **1944–45**, by which time, on Table 1, most of the dying is
done. Epidemic expenditure in the year *after* the mortality peak is **ten times** the pre-famine level.
This is the same "relief follows deaths" pattern as the grain despatches (§4.4), in a second
independent ledger. **Strong exhibit; the numbers are the Bengal government's own.**

### 4.1 The FIC's own numbers — recorded, and the best-locatable exhibit set

Famine Inquiry Commission, *Report on Bengal*, Part II (1945), §E "Epidemics," printed **pp. 119–120**
(PDF pp. 12–13 of `library/by-topic/colonialism-slavery/FamineInquiryCommissionBengalPartII-Woodhead-1945-GovtOfIndia.pdf`):

| Disease | Recorded deaths | Excess over quinquennial avg | Share of excess mortality | Printed p. |
|---|---|---|---|---|
| **Malaria**, Jul–Dec 1943 | 479,039 | +266,208 (**+125.1%**) | **41.5% of all 1943 excess deaths** | 119 |
| **Malaria**, Jan–Jun 1944 | 400,901 | +223,664 (**+126.1%**) | **53.0% of all Jan–Jun 1944 excess** | 119 |
| **Malaria**, Dec 1943 alone | — | **+202.6%** over average | — | 119 |
| **Cholera**, Jul 1943–Jun 1944 | 218,269 | **+309.7%** over 1938–42 avg | peak Oct–Nov 1943 | 119–120 |
| **Smallpox**, 1943 | 22,005 (avg 7,991) | — | "relatively unimportant" in 1943 | 120 |
| **Smallpox**, Jan–Jun 1944 | 125,471 | +118,841 | **~28% of Jan–Jun 1944 excess** | 120 |

**Malaria alone accounts for over half the excess deaths in the first half of 1944. Malaria plus
smallpox account for roughly four-fifths of it.**

The FIC also flags its own limits here, which matters for honesty on screen (p. 119): malaria figures
"are likely to be inaccurate, and more inaccurate in 1943 than in 1944," because certain diagnosis
needs a blood examination and "the proportion of cases in which this was done was of course
infinitesimal."

### 4.2 The FIC refuses to decompose — and this is the load-bearing quotation

Printed **p. 120** (PDF p. 13), §(ii) "The relation of famine to the epidemics," para 17:

> *"A famine-stricken population is a sick population… We have estimated that there were some 1.5
> million deaths in excess of the average in 1943 and the first half of 1944. **It is impossible to
> separate these into groups and to assign a proportion to starvation and under-nutrition, another
> proportion to epidemic disease, and yet another to non-epidemic disease.** The famine and its effects
> on the life of the people must be held generally responsible for the high excess mortality recorded
> under all the headings in the mortality tables."*

Two things fall out of that sentence and both are usable:
- **⚠ It also fixes the scope of the 1.5M**: "in 1943 and the first half of 1944." That is a *narrower*
  window than the phrase "the famine and the epidemics which followed it" (D1 in the project file,
  p. 110) implies. It is a third internal wobble in the same report.
- The body that produced the official number **declined to say how many starved**, on the record.

### 4.3 Sen on why "starvation" barely appears in the death registers (pp. 203–204)

> *"…it is common to die of starvation through diarrhoea (indeed, 'famine diarrhoea' is a well-known
> phenomenon) as well as dysentery… Clearly, many of the deaths reported under 'dysentery, diarrhoea
> and enteric group of fevers' were, in fact, starvation deaths."*

Starvation was not a registration category. Village registrars used the traditional disease headings,
and a starving person dies with identifiable proximate symptoms that fit those headings. **So the
disease shares in §4.1 are an upper bound on "disease" and a lower bound on "starvation," not a
partition.** Sen's ranking of contributions to excess mortality, excluding the catch-all 'fever'
(p. 204): **malaria, then cholera, then dysentery/diarrhoea/enteric, then smallpox.**

### 4.4 The counterfactual problem — stated at its sharpest

**Sen, p. 203, and this is the single best showable sentence in the whole mortality file:**

> *"In December 1943, Bengal reaped a harvest larger than any in the past. Curiously enough, it was
> also the month in which the death rate in Bengal reached its peak in this century."*

The phase sequence (Sen p. 203; Maharatna 1994 pp. 211–212):

| | Peak |
|---|---|
| Starvation deaths | ~September–October 1943 |
| Cholera | October–November 1943 |
| Overall proportional excess mortality | **October 1943** |
| Malaria | **December 1943**, elevated right through 1944 |
| Smallpox | March–April 1944 (and higher again a year later) |

**What this does to the "would grain in month X have saved the people who died in month Y" question —
and the answer is not the comfortable one for either side:**

Maharatna 1994 pp. 211–212 makes the causal direction explicit and it cuts *against* the exculpatory
reading:

- *"food relief, which provoked significant population movement, followed excess mortality, not vice
  versa. In other words, food relief became significant only after famine mortality was already very
  high."* The district-level correlation between the percentage rise in deaths (July–Dec 1943) and
  the tonnage of food despatched in 1943 is **+0.58 and highly significant** — i.e. grain was sent
  *where people were already dying*, as a response to death rates, not as prevention (p. 212 and fn. 82,
  citing FIC *Report on Bengal* Appendix V, p. 223).
- The FIC itself, quoted at p. 212 (FIC *Report on Bengal* p. 99): *"Distribution of food on a large
  scale was not begun… until September — several months after the need for it had arisen."*
- Tippera: "numerous" starvation deaths and very high excess mortality attributed by the FIC to lack
  of timely relief; Chittagong, with relatively timely supplies, held excess deaths to a moderate level
  (Maharatna 1994 p. 213, citing FIC p. 73). **A within-Bengal natural experiment on timing.**

**The genuinely uncomfortable finding — the refeeding hypothesis (Maharatna 1994 pp. 172–173).**
Dyson raises, as a tentative explanation for the timing, S. P. Ramakrishnan's suggestion that the
extreme malaria mortality of late 1943 / early 1944 *followed* the establishment of feeding
arrangements in September 1943 — latent malarial infections in an undernourished population becoming
manifest and fatal only once nutrition improved from an extreme low. Corroborating evidence exists
from later African famine contexts (Murray et al., *Lancet*, 1975 and 1976, cited at p. 173, fn. 23).

**⚠ Handle this carefully on screen.** It is *tentative* in the source, and Maharatna's own 1993 paper
(D6, printed **p. 8**) raises "some difficulties with this explanation." It does **not** mean feeding people killed them
— it means the malaria peak is not simple evidence that food arrived too late to matter. **The honest
formulation:** the disease phase was *set up* by months of prior starvation, and the diseases that
killed most people were killing them because starvation had removed their capacity to survive
infections that Bengal survived every other year.

### 4.5 Why the disease phase does not exculpate — the ecology finding

**Arup Maharatna, "Malaria ecology, relief provision and regional variation in mortality during the
Bengal famine," *South Asia Research* 13:1 (1993), pp. 1–26** (filename says pp. 1–29; the PDF is 26
printed pages and printed page = PDF page). Read for this section; the finding, printed **p. 13**:

> *"The correlation coefficients between the average malaria death rate during 1938–42 and the
> percentage rise in malaria deaths in 1943 and 1944 were respectively **−0.41 and −0.48** (both being
> statistically significant)… The most heavily-hit districts — in terms of famine excess mortality —
> were those which were usually **relatively malaria free**."*

The greatest proportional increases in malaria deaths occurred in districts that were **normally the
*least* malarious**. West Bengal, with lower pre-famine malarial incidence, saw the *greater* rise in
famine mortality. In the worst-hit districts malaria became *more* dominant in the death mix; in the
already-malarious districts its relative share *fell* (D6 p. 13).

That is the signature of an epidemic sweeping a population that had lost its resistance, not of a
malaria year. Bengal was already the most malarial province in British India except Coorg, and the FIC
states plainly (Part II p. 119): *"no epidemic approaching in severity that of 1943–4 has occurred
within its recent history."*

### 4.6 The wording verdict for the script

- ❌ **"Three million people starved to death"** — wrong on both halves.
- ❌ **"They died of malaria, not of the famine"** — the FIC explicitly refuses this move (§4.2) and
  the ecology data refute it (§4.5).
- ✅ **"Most of them did not starve to death in the literal sense. Malaria alone accounts for 43% of
  the excess deaths in 1943 and 71% in 1944 — plus cholera, smallpox, dysentery. These were diseases
  Bengal lived with every single year. They became lethal because starvation had stripped the
  population's ability to survive them. The Famine Inquiry Commission was asked to separate the
  starvation deaths from the epidemic deaths, and said it was impossible."**
- ✅ Or, tighter: **"They died of the diseases that always circulated. Starvation is what made those
  diseases fatal."**
- ✅ The strongest single-sentence version, because it forecloses the exculpatory reading in the same
  breath: **"The districts where malaria deaths rose most were the districts that normally had the
  least malaria."**

---

## 5 — THE RANGE, AND THE SENTENCE TO SAY

### 5.1 Recommended public formulation

> **"Nobody knows. The colonial government counted 688,846 excess deaths in 1943 and admitted its own
> figures were unreliable. Its official finding was around a million and a half. The best modern
> demography — Dyson and Maharatna, working from registration data for undivided Bengal that nobody
> had used before — puts it at about 2.1 million, in a range of 1.8 to 2.4. The three-million figure
> you usually hear is Amartya Sen's, and it rests on a 1951 Pakistani census table that used a normal
> death rate roughly 250,000 a year too low. Two to three million people is the honest way to say it,
> and every one of those numbers is an estimate of how many deaths were never written down."**

Shorter, if the beat needs it:

> **"Somewhere between two and three million. The best demographic reconstruction says 2.1 million.
> The gap between the estimates isn't a disagreement about history — it's a disagreement about how many
> deaths went unrecorded."**

### 5.2 Why each bound is where it is

- **Absolute floor — 688,846.** Registered excess deaths, Bengal, 1943 only. Bengal Public Health
  Department, quoted in FIC Part II p. 108. **This is a count, not an estimate.** Everything above it
  is inference about non-recording.
- **1.5M** — the FIC's finding. Sits where it does because the Commission implicitly assumed **86%**
  registration completeness (§1.5) and stopped counting at June 1944 (§4.2).
- **1.8M — the defensible lower bound.** D&M assumption 1 (Chowdhury CF 1.32, registration ~76%
  complete). Also, coincidentally, what Sen's own flat baseline yields on the better data.
- **2.1M — the centre.** D&M assumption 2: Jain's CF 1.51 (registration ~66%) plus the declining
  1931–42 trend. The authors' own preference, restated unchanged in 1994.
- **2.4M — the defensible upper bound.** D&M assumption 3, CF 1.70 (registration ~59%) — which they
  label *arbitrary*, chosen to represent worse under-registration than any study supports.
- **~3M — reachable but unsupported.** Requires registration to have fallen "well under 50 per cent"
  in 1943–44 (D1 p. 297). D&M: "This is not impossible. But it would be hard to justify."
- **Above 3M — not defensible on the registration data.** See §6 for what the 3.5M figures actually are.

**⚠ One-sided error the script should name:** every bound above is Bengal-only. D1 p. 297 records
substantial excess mortality elsewhere in India in 1943–44, "some of it, in Orissa, probably reflecting
deaths of out-migrants from Bengal," and calls the neglect of it inadequate. Nobody has quantified it.
The true toll of the event is therefore biased *upward* from all of these figures by an unmeasured amount.

### 5.3 What cannot be recovered, and why — sourced, not asserted

The single best statement of this is the **Census of Pakistan 1951**, quoted in full by D&M at p. 287:

> *"The Birth and Death Registration system, which is normally operated by the village chowkidars who
> are often illiterate and irresponsible, is notoriously unsatisfactory, but during the famine year,
> even this defective machinery practically collapsed as the chowkidars themselves became victims of
> the famine. People left their homes, families and children died here and there. Women and children
> whose feeble legs could not carry them far, perished unnoticed in the recesses of the villages."*

**⚠ Attribution discipline:** that passage is the *Pakistan census's* self-description, and **D&M
dispute its central claim.** They say (p. 289) "there seems to be no good basis for the sweeping view
that the registration system 'practically collapsed'," citing the FIC's own inquiries and the fact that
the monthly *pattern* of deaths in undivided Bengal during the famine closely tracked the normal
seasonal distribution. **Present the quotation as the contemporary claim, and say the demographers who
re-ran the data think it overstates the collapse.** That is a better beat than either half alone.

The categories that are genuinely irrecoverable:

| What was missed | Evidence it was missed |
|---|---|
| **Roadside deaths of migrants** | Aykroyd, who *made* the FIC estimate: it was an underestimate "especially in that it took too little account of roadside deaths" (*The Conquest of Famine*, 1974, p. 77, quoted D1 p. 281). FIC Part II p. 111 also refers to "unrecorded road-side deaths." |
| **Deaths of the destitute in Calcutta** | Public Health Commissioner for India, 1943–44 report: bodies "disposed of by public arrangement" — **3,000 (June 1942–May 1943) rising to 19,000 (June 1943–May 1944)**, a six-fold rise (Maharatna 1994 p. 185). Migrants recorded, if at all, in the town they died in and not the district they left. |
| **Women and children disproportionately** | FIC Part II p. 111: omissions "may not have been equally distributed in the different age and sex groups. We have referred to unrecorded road-side deaths. It is not unlikely that these included more women and children than men." |
| **Village watchmen (chowkidars) dead or unpaid** | Census of Pakistan 1951 (above) — contested as to degree, not as to direction. |
| **Migrants counted twice or not at all** | Maharatna 1994 p. 211: out-migration "may have both lowered registered birth and death rates in sending districts and raised registered birth and death rates in receiving districts." Nets out at province level; destroys district-level attribution. |
| **Bengalis who died outside Bengal** | D1 p. 297 (Orissa). Not in any estimate. |

### 5.4 Claim status

| Claim | Status |
|---|---|
| D&M 1991 method and its 1.8/2.1/2.4 band | **SETTLED** — read in full from the primary text; every figure quoted from running prose |
| The declining baseline is worth ~+0.2M, not the main driver | **CORROBORATED** — arithmetic reproduced from the paper's own worked example, p. 295 |
| Sen's gap lives in the East Bengal 540,000 baseline | **CORROBORATED** — D&M p. 288 fn. 17, cross-read against Sen p. 201 |
| Maharatna 1994 does not revise 2.1M | **SETTLED** — pp. 171, 211 |
| Malaria = **43.06% (1943) / 71.41% (1944)** of excess deaths | **CORROBORATED** — D13 Table 1 p. 181 (read from page image), independently consistent with FIC Part II p. 119 (41.5% / 53.0% for H1 1944) on a different baseline and window |
| Public health spending fell in 1942–43 and peaked in 1944–45 | **INSPECTED** — D13 Table 2 p. 181, read from page image; Bengal government's own accounts |
| Maharatna's figure never changed across 1991 / 1992 / 1994 | **SETTLED** — all three read |
| "Starvation" understated in registers | **CORROBORATED** — Sen pp. 203–204; FIC p. 120 refusal to decompose |
| Refeeding hypothesis | **CONTESTED** — tentative in Dyson; D6 raises difficulties. Do not state as fact |
| Maharatna's thesis position | **UNREAD** — see §2.2 |
| FIC's rejection of Chattopadhyaya as "statistically unsound" | **NOT FOUND** — see §6 |

---

## 6 — EVERY ESTIMATE, AND THE ONE ASSUMPTION THAT DRIVES IT

| Figure | Producer | Method | The single driving assumption | Verdict on the project's current attribution |
|---|---|---|---|---|
| **688,846** (1943) | Bengal Public Health Dept, via FIC Part II p. 108 | Registered deaths 1943 (1,873,749) minus quinquennial avg 1938–42 (1,184,903) | **None** — it is a count. Assumes registration is the universe, which it is not. | ✅ **Correct as stated.** |
| **~1.0M** (1943) | Famine Inquiry Commission, Part II pp. 108–109 | 688,846 grossed up for under-registration | **Registration was ~86% complete** (implied CF 1.16, reverse-engineered by D1 p. 289) | ✅ Correct. |
| **~1.5M** (total) | Famine Inquiry Commission, Part II p. 110 | ~1.0M for 1943 + the 1944 excess | Same CF; **and a window ending June 1944** (explicit at Part II p. 120) | ✅ Correct — but the FIC gives **1.3M** at printed p. ~121 and describes its own +45% correction as "some 40 per cent" (Sen p. 201 fn. 326). **Three inconsistencies, not one.** |
| **"well over 3.5M"** | **Anthropology Dept, University of Calcutta** — press release **21 Feb 1944** | Sample survey, 8 districts, 816 family units / 3,880 people; 386 deaths in two 2-month windows of 1943 → 10% per 6 months; subtract 1.5% normal; apply the resulting 8.5% to **two-thirds of Bengal's population** | **That the surveyed districts represent two-thirds of Bengal.** Sen: "a piece of pure guesswork — and an illegitimate one at that, since the sample that was surveyed was chosen from the worst affected areas" (p. 197) | ❌ **MISATTRIBUTED.** It is not "Chattopadhyay's estimate." It is a **February 1944 university press release**, issued before the FIC even existed. Reprinted in Ghosh (1944), App. G. |
| **2.2M (1943) / 2.7M total** | **K. P. Chattopadhyaya** — his actual, revised position | Chattopadhyaya "himself pointed out limitations" of the 3.5M and proposed 2.2M for 1943; plus the FIC's 0.5M for 1944 = a **"minimum"** total of 2.7M | **That his sample can be re-weighted at all** | ❌ **The project file has the wrong number against his name.** Source: Chattopadhyaya & Mukherjea (1946), p. 5, via Sen pp. 197–198 and Sen's Table D2 p. 202. D&M p. 281 independently give "2.2 million [in] 1943 alone." |
| **~3M** | **Amartya Sen**, *Poverty and Famines* (1981) App. D pp. 195–216 | West Bengal registration × Jain CF 1.51, flat 1941/42 baseline, window to 1946; either + the Pakistan census 1.714M or ×3; then rounded **up** for three stated downward biases | **That the *Census of Pakistan 1951*'s East Bengal figure is sound.** It is not — its 540,000 "normal" should be ~790,000 | ✅ Correct attribution. ⚠ But "3 million" is Sen's *rounded-up judgement*, not his computed result. His computed range is **2.62–3.05M**; the ×3 variant of assumption B is the only one that reaches 3.05. |
| **1.8M / 1.9M** | Dyson & Maharatna 1991, Table 2 p. 285 | **Sen's exact method**, run on undivided-Bengal registration data | Flat baseline (Sen's A / B) | ✅ Underused. This is the cleanest apples-to-apples number in the literature: *same method, better data.* |
| **~2.1M (range 1.8–2.4)** | **Dyson & Maharatna 1991**, pp. 291–297; restated Maharatna 1994 p. 211 | Undivided-Bengal registration; least-squares CDR trend 1931–42 extrapolated as the counterfactual; three CF assumptions | **Jain's CF 1.51 — registration ~66% complete** | ✅ Correct. ⚠ Reframe: it is a **downward** revision of Sen, not an upward revision of the FIC. |
| **3.5–3.8M** | **Paul Greenough**, *Prosperity and Misery in Modern Bengal* (OUP, 1982), p. 309 | — | — | ⚠ **Attribution correct, independence false.** D1 p. 282 fn. 6: "Greenough's sometimes-cited estimate of between 3.5 and 3.8 million excess deaths is **itself largely based on Sen's calculations**." It is not a second witness; it is Sen's number with a further gross-up. **Never cite Greenough and Sen as two sources agreeing.** |
| **"3 to 4 million"** | unnamed contemporary critics of the FIC | — | — | Recorded only via Aykroyd 1974 p. 77. Not a study. |
| **"between two and two and a half million"** (East Bengal alone) | "popular belief," per *Census of Pakistan 1951* p. 30 | — | — | Quoted by both Sen (p. 201 fn. 328) and D&M (p. 287). **Not an estimate** — the census reports it as rumour and does not adopt it. |

**⚠ Could not verify: "rejected by the FIC as statistically unsound."** Direct check: searched the full
text of FIC *Report on Bengal* Part II (124 pp.) for `chattopadhyay`, `3,500,000`, `3.5 million`,
`three and a half`. **The only hit is a witness-list entry** — "99. Prof. K. P. Chattopadhyaya /
Representatives of the People's Relief Committee / 11-9-1944." Part II contains no named rejection of
his figures; the nearest thing is the general "We have found no valid reason for accepting estimates in
excess of this figure" (p. 110). **Part I was not searched — it is not in this library folder.** Either
soften the claim to the general rejection, or check Part I before using it.

---

## 7 — SHOWABLE EXHIBITS (verified locators)

### Exhibit 1 — the referee's own disclaimer ⭐ recommended lead
**FIC, *Report on Bengal*, Part II (1945), printed p. 111** (PDF p. 4 of the library copy), §16.
**⚠ Page correction: the brief expected p. 112. It is p. 111** — the paragraph closes that page; the
running head "112 DEATH AND DISEASE IN THE BENGAL FAMINE" begins the next.

> *"The quotation of recorded mortality figures, including digits down to the tens and hundreds, and
> the tabulation of percentages to one place of decimals, tends to give a **false air of accuracy**. We
> must again emphasize that all the figures given are inaccurate and should not be regarded as
> indicating more than general trends in mortality."*

Why it works: the body that produced 1,873,749 and 688,846 says on the record that the precision is
theatre. It licenses the whole range-not-a-number approach in one sentence, in the source's own voice.
Pairs directly with D3 already in the project file.

### Exhibit 2 — the man who made the number, disowning it
**W. R. Aykroyd, *The Conquest of Famine* (London, 1974), p. 77.** Quoted verbatim at **D1 p. 281**
and again at **Sen p. 197**; the second half quoted at **Sen p. 201 fn. 321**. Aykroyd was the
Commission member responsible for the mortality estimate.

> *"it was an under-estimate, especially in that it took too little account of roadside deaths, but not
> as gross an under-estimate as some critics of the Commission's report, who preferred 3 to 4 million,
> declared it to be."*

and, on his own method:

> *"at all events, the figure of 1.5 million deaths is in the history books, and whenever I come across
> it I remember the process by which it was reached."*

Why it works: it is the author of the official figure telling you it is both too low and arbitrary —
and simultaneously refusing the 3–4M number. He is the perfect witness because he indicts both sides.
**⚠ Provenance note: we hold this only at second hand,** verbatim and consistently in two independent
sources (Dyson & Maharatna 1991; Sen 1981). Aykroyd 1974 is **not** in the project library — **direct
check: searched `_research/library/articles/` and `library/by-topic/colonialism-slavery/`; absent.**
Acquire before putting it on screen as a document card; safe now as an attributed spoken quotation.

### Exhibit 3 — the sentence that breaks the simple story
**Sen, *Poverty and Famines* (1981), p. 203**, opening D.3 "How Did They Die?"

> *"In December 1943, Bengal reaped a harvest larger than any in the past. Curiously enough, it was
> also the month in which the death rate in Bengal reached its peak in this century."*

Why it works: it is one sentence, it is from the most-cited author in the field, and it forces the
video's actual question — if the grain was there in December and the dying peaked in December, then
the thing to explain is not the harvest, it is the eight months before it and the destroyed bodies of
the people who did not survive them. It sets up §4 without the script having to argue.

### Exhibit 4 — the cause-of-death table itself ⭐ recommended for the disease beat
**Maharatna 1994, Table 1, printed p. 181.** A clean academic table, already rendered at 300 dpi to
`…/scratchpad/D13-Table1.png`. Put two rows on screen and let them do the work:

    Malaria — share of Bengal's excess deaths:   1943: 43.06%   1944: 71.41%
    Cholera — share of Bengal's excess deaths:   1943: 23.88%   1944:  0.99%

Why it works: it is a real table from a real journal with a visible source line (*Bengal Public Health
Report*), it is legible at thumbnail size, and the cholera row collapsing while malaria climbs shows
the audience — without narration — that this was not one event but a sequence. It also pre-empts the
"they starved" simplification and the "it was just malaria" deflection in a single frame.

### Exhibit 5 (spare) — the two correction factors, side by side
A built graphic rather than a document, but every input is sourced:

    Famine Inquiry Commission, 1945 — implied: registration 86% complete  →  1.5 million
    S. P. Jain, reverse survival, 1954 — registration 66% complete        →  2.1 million
    (would be needed to reach 3 million: registration under 50%)

Locators: FIC's 86% reverse-engineered at **D1 pp. 288–289 fn. 18**; Jain's 33.9% under-registration
at **Sen p. 199**, CF 1.51 at **D1 p. 291**; the sub-50% requirement at **D1 p. 297**.
Why it works: it shows the audience that the entire 1.5-vs-3-million argument is one number about
paperwork, which is the channel's exact register.

---

## 8 — OPEN ITEMS

1. ~~Maharatna LSE thesis~~ — **DONE.** Chapter 5 read; no revision; Table 5.4 recovered (§1.3a, §2.2).
2. **⏳ D6 Maharatna 1993 (malaria)** — the district-ecology finding read and page-verified (p. 13);
   the refeeding caveat located (p. 8). **Not read end to end** — the relief-provision regressions
   (pp. 9–12, 14–20) and Tables 1–6 were not worked through. Nothing in §4 depends on them.
3. **❌ Aykroyd, *The Conquest of Famine* (1974)** — not held. Direct check: absent from both library
   paths. Needed to promote Exhibit 2 to a document card.
4. **❌ Chattopadhyaya & Mukherjea (1946)** — not held. Currently at second hand via Sen p. 198.
5. **❌ FIC *Report on Bengal* Part I** — not in `library/by-topic/colonialism-slavery/`. Needed to
   settle the "rejected as statistically unsound" attribution (§6).
6. **❌ Greenough (1982) p. 309** — not held. D1 characterises it; we have not read it. Do not cite
   Greenough's figure directly, only D&M's characterisation of it.
7. **Image-only tables — status.** Every number in this file comes from running prose that states it
   explicitly, from the thesis's machine-readable Table 5.4, or from a table read directly off a
   rendered page image. **Nothing was inferred.**
   - ✅ D1 Table 5 — recovered via thesis Table 5.4, printed p. 228 (§1.3a).
   - ✅ D13 Tables 1 and 2 — read from the rendered page image of printed p. 181 (§4.0, §4.0a).
     Render cached at `…/scratchpad/D13-Table1.png` (300 dpi).
   - ❌ **Still unread:** D13 Tables 3, 4, 5, 8, 10 and Figures 1–7; D6 Tables 1–6 and Figures 1–2;
     D1 Tables 1–4. Of these, the one worth rendering next is **D13 Table 4** (rural/urban split of
     causes of death, printed ~p. 184) if the script wants the Calcutta destitute story quantified.

---

## 9 — WHAT TO CHANGE IN `01-VERIFIED-RESEARCH.md`

- **§D1 note.** Replace "Modern demography revises upward (Maharatna ~2.1M)" with: *Modern demography
  puts it at ~2.1M (range 1.8–2.4M) — which is above the FIC but well below the 3M figure usually
  quoted. Dyson & Maharatna 1991 is a downward revision of Sen, not an upward revision of the
  Commission.*
- **§D4.** Add the two further inconsistencies: the FIC calls its own +45% correction "some 40 per
  cent" (Sen p. 201 fn. 326), and Part II p. 120 scopes the 1.5M to "1943 and the first half of 1944."
- **Add to the estimates table:** the 3.5M figure is a **February 1944 University of Calcutta
  Anthropology Department press release**, not Chattopadhyaya's estimate; his own figures are 2.2M
  (1943) and 2.7M (total). Greenough's 3.5–3.8M is derived from Sen and is not independent corroboration.
- **Add:** all figures are Bengal-only; excess deaths of Bengali out-migrants in Orissa and elsewhere
  in India in 1943–44 are unmeasured and excluded (D1 p. 297).
- **Add a new graded claim — the cause decomposition.** Malaria 43.06% of 1943 excess deaths and
  71.41% of 1944; cholera 23.88% then 0.99%; smallpox 1.30% then 23.69% (Maharatna 1994, Table 1,
  printed p. 181). This is load-bearing for the script's wording and currently absent from the file.
- **Add the FIC's refusal to decompose** (Part II printed p. 120) alongside D3 — it is the same
  argument as D3 applied to causes rather than counts, and it scopes the 1.5M to "1943 and the first
  half of 1944."
- **⚠ Correct the exhibit locator:** the "false air of accuracy" passage is at Part II printed
  **p. 111**, not p. 112.
