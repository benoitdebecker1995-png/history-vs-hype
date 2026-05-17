# Marketing Copy — Three Channels

Three zero-budget marketing assets to drive Gumroad traffic. Use them in this order: cold email first (highest conversion, smallest audience), Reddit case-study second (medium effort, medium reach), Twitter thread third (lowest effort, but only works if you're consistent on Twitter).

---

## 1. COLD-EMAIL TEMPLATE (priority — highest conversion)

**Target:** History/geopolitics YouTubers with 1K-50K subs. Hand-build a list of 30-50 channels using YouTube search + the "Channels" filter. Save channel URL + a public email/contact-form/Twitter DM in a spreadsheet.

**Personalization (5 minutes per email):** Run their top 5 titles through `title_scorer_standalone.py`. Drop the scored output into the email. This makes every email feel hand-written and non-spammy.

**Send pattern:** 5-7 per day, Tue-Thu mornings (their time). Don't blast — Gmail will flag.

### Subject line A/B test these two

- A: `Quick title score for {channel name}'s top 5 videos`
- B: `Why your {top video title fragment} hit X% CTR — pattern analysis`

Subject A converts better cold; Subject B converts better warm.

### Email body

```
Hey {first name},

I run a niche history channel (History vs Hype, 515 subs but growing 173% in 90 days). I built a title-scoring methodology calibrated against 47 of my own videos with measured CTR data, and I ran your top 5 through it this morning.

Here's what came back:

#1 — "{their #1 title}"
Score: {X}/100 ({grade})
Pattern: {pattern}
{1-line on what's working or what's hurting it}

#2 — "{their #2 title}"
Score: {X}/100 ({grade})
{1-line}

#3 — "{their #3 title}"
Score: {X}/100 ({grade})
{1-line}

(I'll skip #4-5 unless you ask — same format.)

The interesting one is #{N}, where {specific pattern observation — e.g., "the colon costs 28% CTR by my data, and your CTR pattern matches that — your colon titles consistently underperform your declarative ones"}.

I packaged the full methodology + the Python scorer as a $49 product on Gumroad. The 40-page PDF has all the calibration data, the hard-reject rules, and 12 worked examples. Link if you want it: {gumroad-link}

But honestly — if you want to talk shop instead, I'm happy to compare notes. I think we're solving the same packaging problem and you're 5x my size.

— {your name}
{your channel link}

P.S. The PDF refund policy is 14 days, no questions. The methodology either applies to your channel or it doesn't — I'd rather you find out cheaply.
```

**Why this email works:**

- **Personalization is real, not template-fake.** You actually scored their titles. They can verify.
- **Free value before ask.** They get insight into their own performance before any sale pitch.
- **The P.S. neutralizes refund anxiety.** Removes a friction point.
- **Soft "talk shop" alternative.** Some won't buy but will reply. Each reply is a relationship in a small niche.
- **Specific scoring observation in #N.** This is the line that converts. Make it specific to *their* channel, not generic.

**Realistic conversion math:**
- 50 cold emails sent → 8-15 opens (15-30% rate, depending on subject line)
- 8-15 opens → 2-4 replies (15-25% reply-to-open)
- 2-4 replies → 1-2 sales (40-60% reply-to-sale, because the personalization filters tire-kickers)
- = ~$50-100 from 50 emails (1 sale at $49 + maybe 1 Loom upsell)
- At 5h to scale (research + score + send), that's $10-20/h. Not great alone, but compounds via word-of-mouth.

---

## 2. REDDIT CASE-STUDY POST (medium effort, medium reach)

**Target subreddits:** r/NewTubers (1.8M, lower bar but more spam), r/PartneredYoutube (200K, monetized creators only — higher quality), r/youtubers (general).

**Posting strategy:** Post the same content with slightly different framing to two subs over 7 days. Don't cross-post the same hour — Reddit auto-detects.

**Why a case-study post (not a sales post):** Reddit hates sales posts. A genuine "here's what I learned, here's the data" post that *happens* to mention a Gumroad link at the bottom converts 3-5x better than a "buy my thing" post.

### r/NewTubers version

**Title:** `Reverse-engineered my top-CTR videos. Found 3 hard-reject patterns costing me 28-46% CTR. (47-video methodology, with data)`

**Body:**

```
I run a niche history/geopolitics channel (515 subs, growing 173% in 90 days). About 18 months ago I started logging CTR + pattern + impressions for every video I published. Yesterday I finished reverse-engineering it into a system that scores titles before I publish them.

Sharing the three biggest findings here because they're niche-agnostic:

**1. The "Topic: Subtitle" colon costs 28% CTR.**

Across my data set (n=4 colon titles vs 19 non-colon declarative), colons averaged 2.3% CTR vs 3.8%. That's a 28% drop. Same content, same thumbnails — just the colon.

The fix is dumb: replace `:` with `—` (em-dash) or split into two sentences.

Bad: "Operation Condor: The CIA's Secret War"
Good: "The CIA Helped Run a Death Squad Network. The Documents Are Now Public."

**2. The "The X That Y" pattern is the worst structural pattern I've measured.**

"The Country That Disappeared" / "The Treaty That Divided The World" / "The Empire That Fell Overnight" — all underperform. My data shows ~1.2% CTR for this pattern. Below the algorithm-survival threshold.

Why I think it fails: it's a curiosity gap with no anchor. Viewers can't tell what they're getting. Replace with declarative or versus framing.

**3. "Evidence promise" is the strongest single bonus signal.**

Phrases like "Here's the evidence", "The documents prove", "Primary sources show", "Word for word" — every one of my top-5 CTR videos has one.

My top video (9.5% CTR — highest in my data set): "JD Vance Claims Christians Found Child Sacrifice. Here's the Evidence."

Pattern: declarative + named entity + controversy frame + evidence promise + two-sentence formula. That's 4 stacked bonuses. Anything less than 2 stacked bonuses underperforms.

---

I built a Python title scorer that automates this. Posting it because someone DM'd me and asked for it: it's a single standalone file, no dependencies, runs anywhere with Python 3.10+. Code's free; the methodology PDF (with all the calibration data, sample sizes, and 12 worked examples) is on my Gumroad at $49 if anyone wants it.

But honestly — the three findings above are 80% of the value. Use them, calibrate to your own channel, and you'll see CTR move within 30 days.

Happy to score titles in the comments if anyone wants to drop their top 3.
```

**Why this post works:**

- **Three concrete findings with data.** Reddit respects measured data.
- **Free value first** — anyone can apply the three findings without buying.
- **Honest about the data set size** — n=4, n=19. No "I have 10 million data points." Smart Reddit users smell hype.
- **The Gumroad mention is mid-post, soft, with a "but honestly" qualifier.** Reduces sales-resistance.
- **"Happy to score titles in the comments"** — turns the comment section into demos. Every score-reply is a public proof of concept that drives DMs.

**Posting tip:** Schedule for Tuesday or Wednesday 8-10am ET. r/NewTubers peaks then. Don't reply to your own post for 30 minutes — let it accumulate engagement organically.

### r/PartneredYoutube version

Same body but adjust the opening:

> *"Posting in r/PartneredYoutube because the methodology is more directly useful to monetized channels — the 48-hour swap protocol I describe at the end is what saved 3 of my last 6 videos from sub-2% CTR."*

This frames it for an audience that's past the "how do I get my first 1K subs" question and into "how do I optimize CTR." Different pain.

---

## 3. TWITTER/X THREAD (lowest effort, only works with consistency)

**Target:** YouTuber Twitter is small (~5K active accounts in this niche). One thread won't do much. **Don't run this campaign unless you're willing to post 2-3 threads/week for a month.** Otherwise skip Twitter.

**Posting strategy:** Tuesday or Friday 9am-2pm ET. Pin to profile. Quote-tweet your own thread once 24 hours later with one extra finding.

### Thread (10 tweets max — Twitter's algorithm penalizes longer)

```
[1/10]
I run a niche history YouTube channel.

515 subs. Grew 173% in 90 days.

Reverse-engineered my top-CTR videos. Found 3 patterns costing me 28-46% CTR every time I used them.

Thread:

[2/10]
**Hard reject #1: YEAR as topic label**

5 videos with years in titles vs 30 without.

Years averaged 45.6% lower CTR.

"The 1494 Treaty That Divided the World" vs "Spain and Portugal Divided the World With One Line"

Same video. 2x CTR difference.

[3/10]
**Hard reject #2: COLON as "Topic: Subtitle"**

Colon titles: 2.3% CTR (n=4)
Non-colon declarative: 3.8% CTR (n=19)

That's a 28% drop. Same content. Same thumbnails. Just the colon.

The fix takes 5 seconds: replace `:` with `—` or a period.

[4/10]
**Hard reject #3: "The X That Y" pattern**

"The Country That Disappeared"
"The Treaty That Divided the World"
"The Empire That Collapsed Overnight"

Worst pattern in my data set. ~1.2% CTR.

Curiosity gap with no anchor. Viewers can't tell what they're getting.

[5/10]
On the other side of the ledger — six bonus signals that show up in every top-CTR video I've published.

The strongest single one: **evidence promise**.

"Here's the evidence."
"The documents prove."
"Word for word."

[6/10]
My top video (9.5% CTR, highest in my data set):

"JD Vance Claims Christians Found Child Sacrifice. Here's the Evidence."

Pattern: declarative
Bonuses: named entity + controversy frame + evidence promise + two-sentence

4 stacked bonuses = top of niche.

[7/10]
**Two-sentence formula** is the strongest structural pattern I've measured.

Across 650 competitor titles I analyzed, two-sentence titles hit outlier status (3x channel avg) at 11% — the highest rate of any structural feature.

Setup. Payoff.

That's it.

[8/10]
**The 48-hour rule**:

Below 2% CTR at 48h + 500 impressions = swap title AND thumbnail
2-4% CTR = swap title only
Above 4% = hold

Most creators I know wait too long to swap. The algorithm decides in 48-72 hours. Past that, it's hard to recover.

[9/10]
I packaged this into a 40-page PDF + a working Python title scorer.

$49 on Gumroad: {link}

But these three hard rejects + three of the bonus signals are 80% of the value. Use them free.

[10/10]
If you run a history, geopolitics, or fact-checking YT channel and want me to score your top 3 titles — drop them in the replies. Public scoring all day.

(Calibrate the methodology to your own channel as you accumulate CTR data — Section 8 of the PDF covers that.)
```

**Why this thread works:**

- **Tweet 1 establishes authority with specific numbers** (515 subs, 173% growth, 28-46% CTR).
- **Tweets 2-4 are the Reddit-style hard rejects** with measured data.
- **Tweets 5-7 are the bonus signals** — proves the system isn't just "what to avoid."
- **Tweet 8 is the 48h protocol** — useful even without buying.
- **Tweet 9 is the soft pitch** with a free-value caveat.
- **Tweet 10 turns replies into proof-of-concept demos.**

**Don't run this thread alone.** Twitter rewards consistency. Pair with 2-3 follow-ups over the next week:

- Day 3: "Scored 5 viewer titles in this thread. Here's what I found." (Quote-tweet the original.)
- Day 5: "The single line of code that detects all 3 hard rejects." (Code screenshot from `title_scorer_standalone.py`.)
- Day 7: "Day 7 update — X sales since the original thread. Here's the conversion data." (Transparency post; YT-Twitter loves these.)

If you're not willing to do the follow-ups, skip Twitter and focus on email + Reddit.

---

## Sequencing: when to send what

**Week 1, Day 1:** Build the cold-email list (30-50 channels). Score their top titles. Send 5-10 emails Tuesday morning.

**Week 1, Day 2:** Continue cold emails (5-10/day). Post r/NewTubers case-study Wednesday morning.

**Week 1, Day 4:** Post r/PartneredYoutube case-study Thursday morning.

**Week 1, Day 5:** Post Twitter thread Friday morning.

**Week 1, Days 6-7:** Reply to all comments/DMs. Score titles publicly. Convert engaged commenters via DM.

**Week 2:** Repeat with a different angle (e.g., "the 48h swap protocol" instead of "the three hard rejects"). New audiences see new framing as new content.

**Realistic week 1 outcome:** 100-200 emails sent + 2 Reddit posts + 1 Twitter thread = 5-15 sales = $250-750 in week 1. The compounding part is the public scoring — every public score creates a portfolio of "look, this works on real channels" examples that future buyers can verify.

---

## A/B test framework (don't skip this)

Track every cold email + every Reddit post + every Twitter thread with this format:

- **Channel/sub:** {channel | r/NewTubers | Twitter}
- **Date:** YYYY-MM-DD
- **Variant:** {subject A | subject B | thread style 1 | etc.}
- **Sent/posted:** count
- **Opens/views:** count
- **Replies/comments:** count
- **Sales:** count
- **Conversion %:** sales / sent

After 200 emails sent, you'll know which subject line converts. After 4 Reddit posts, you'll know which subreddit + framing works. Don't optimize prematurely — collect data first, optimize at week 4.
