# Newsletter Metadata Checklist

**Pre-publish checklist for every Substack article. Based on Substack SEO research and history niche data (2026-03-26).**

---

## Per-Article Checklist

### 1. Subject Line (email open rate = your CTR equivalent)

- [ ] **6-10 words** (highest open rates)
- [ ] **36-50 characters** (sweet spot — no truncation on any client)
- [ ] **No "How to" opener** (-57% fewer opens — move to subtitle)
- [ ] **No colon** (kills curiosity gap, signals generic formatting)
- [ ] **No year in first third** (front-load the mystery, not the date)
- [ ] **Curiosity gap present** (+19% lift: "not," "actually," "never," "wrong," "myth")
- [ ] **Specific number if possible** (+12-15% lift, but NOT a year)
- [ ] **Calm Prosecutor voice** (verdict or contrarian statement, not clickbait)
- [ ] **Run scorer:** `python -m tools.newsletter.subject_line_scorer "Subject Here"`
- [ ] **A/B test** (available at 200+ subscribers — test 4 variants, 50% of list, 1 hour)

**Niche patterns that work (from Substack top history newsletters):**
| Pattern | Example | Why it works |
|---------|---------|-------------|
| Contrarian verdict | "The Dark Ages Were a Lie" | Calm Prosecutor voice + curiosity gap |
| Specific number + mystery | "14 Islands Worth Billions" | Data + unresolved question |
| Familiar made strange | "This Treaty Was About Wind, Not Land" | Inverts assumption |
| Evidence reveal | "I Translated the Law Nobody Reads" | Personal authority + curiosity |

**Patterns to AVOID at <1K subscribers:**
| Pattern | Why it fails |
|---------|-------------|
| Date-only ("March 22, 2026") | Trust play — only works at 100K+ (Richardson) |
| Long academic ("Chartbook 437: Unseasonal war (2)...") | Needs existing reputation (Tooze) |
| "How to" anything | -57% fewer opens — education niche included |
| Brand prefix with colon ("History vs Hype: Topic") | Wastes characters, splits attention |

### 2. Subtitle (shows below subject in email preview + Substack app)

- [ ] **One sentence, under 100 characters**
- [ ] **Complements subject, doesn't repeat it** (subject = curiosity hook, subtitle = context/payoff)
- [ ] **Contains the keyword you're targeting for SEO** (if subject line doesn't have it)
- [ ] **Tells the reader what they'll GET** (the evidence, the document, the data)

**Formula:** "[What the article proves] using [what kind of evidence]"
- "How a 1913 letter from Honduras proves Britain owned the Sapodilla Cays"
- "The income data that still traces a line drawn by the Pope in 1494"

### 3. SEO Fields (Google indexing — Substack posts indexed within 1-3 hours)

- [ ] **SEO title set** (can differ from email subject line — optimize for search intent)
  - Include target keyword
  - Under 60 characters (Google truncates at ~60)
  - If subject line is curiosity-based, SEO title should be keyword-explicit
  - Example: Subject "The Treaty Nobody Read" → SEO title "Treaty of Tordesillas Explained: How the Pope Divided the World"

- [ ] **Meta description set** (under 155 characters)
  - If not set, defaults to first ~10 words of article — usually too short
  - Include target keyword naturally
  - Write as a complete sentence that works as a Google snippet
  - Example: "The 1494 Treaty of Tordesillas didn't just divide the world between Spain and Portugal. Its economic impact is still measurable in Brazilian income data today."

- [ ] **URL slug set** (before publishing — can't change after)
  - Under 60 characters
  - Include focus keyword, use hyphens
  - Skip stop words (the, a, of, and)
  - Example: `treaty-tordesillas-pope-divided-world` not `the-treaty-nobody-read`

### 4. Social Preview Image

- [ ] **Custom image set** (1200x630px — shows on Twitter/Facebook/Substack app)
- [ ] **Readable at phone size** (same principle as YouTube thumbnails)
- [ ] **Not just the article header image** — design specifically for social sharing
- [ ] **Text overlay if used:** 2-4 words max, high contrast

### 5. First Paragraph (does triple duty)

- [ ] **Google snippet fallback** (if meta description not set, Google uses this)
- [ ] **Email preview text** (shows after subject line in inbox)
- [ ] **Reader hook** (determines whether they keep reading)
- [ ] **Contains target keyword** naturally
- [ ] **Under 155 characters for first sentence** (meta description safe)

### 6. Internal Linking

- [ ] **Link to 1-2 previous articles** where relevant (keeps readers on Substack, boosts SEO)
- [ ] **Link to YouTube video** if article is a script conversion (cross-platform flywheel)
- [ ] **Don't link externally in first paragraph** (keeps readers in your ecosystem)

### 7. Tags / Categories

- [ ] **Add 1-3 Substack tags** (helps Substack's recommendation algorithm surface your posts)
- [ ] **Use tags that match Substack's category system** (History, Education, Politics — not custom tags)

### 8. CTA (Call to Action)

- [ ] **Subscribe CTA in article** (Substack embeds these automatically, but add one manually mid-article)
- [ ] **"Share" prompt at end** (critical at <1K — word of mouth is #1 growth driver)
- [ ] **No begging** — Calm Prosecutor voice: "If this kind of research is useful, share it."

---

## One-Time Setup (Before First Publish)

### About Page

- [ ] **Photo of you** (builds trust — Substack data shows higher conversion with photo)
- [ ] **3-sentence description** (what you do, how it's different, what readers get):
  1. What: "Primary sources and academic research to challenge historical myths"
  2. Different: "Every claim sourced. Every quote real. Documents translated from 6 languages."
  3. Get: "Free to read, always."
- [ ] **Credentials** (relevant only: "I've produced 47 evidence-based videos on [topics]")
- [ ] **Two CTAs** (one above fold, one at bottom — Substack best practice)
- [ ] **NO external links** (keep visitors on your Substack page)
- [ ] **Mention paid tier plan** even if not active yet ("Paid subscribers will get full annotated translation PDFs")

### Publication Settings

- [ ] **Custom domain** (optional but helps Google Search Console verification)
- [ ] **"Allow search engines to index paywalled content"** = ON (lets Google show preview text)
- [ ] **Recommendation network** enabled (drives 50% of new free subscriptions on Substack)
- [ ] **Welcome email** set up (auto-sends to new subscribers — include your best article link)

---

## Cold-Start Growth Priorities (0-500 subscribers)

**Ranked by effectiveness for a YouTube creator starting from zero:**

### Priority 1: YouTube → Substack Pipeline (your existing 515 subs)
- [ ] Add Substack link to YouTube channel "About" section
- [ ] Add to every video description (after sources, before tags)
- [ ] Mention in 1-2 videos per month: "I write about this in more depth on my newsletter"
- [ ] Pinned comment on relevant videos linking to corresponding article
- [ ] Expected conversion: 5-10% = 25-50 Substack subscribers immediately

### Priority 2: Substack Notes (free, daily)
- [ ] Post 2-5 Notes per day (short insights, quotes from research, questions)
- [ ] Engage with other history writers' Notes (comment, restack)
- [ ] Notes are the #1 organic discovery tool on Substack in 2026
- [ ] Algorithm surfaces Notes to non-followers based on engagement
- [ ] Inside-Substack readers convert 4x better than external traffic

### Priority 3: Cross-Recommendations
- [ ] Build relationships FIRST (comment on their posts for 2-3 weeks before pitching)
- [ ] Target similar-size newsletters (don't pitch 100K+ newsletters at launch)
- [ ] A single cross-promotion can deliver 50-100 new subscribers in one day
- [ ] Reciprocal recommendations are the norm — be ready to recommend back
- [ ] Start with: Age of Invention (Howes), Dead Language Society (Gorrie), similar academic-tone writers

### Priority 4: Reddit (high-risk, high-reward)
- [ ] Contribute genuinely to r/history, r/AskHistorians, r/geopolitics for 2+ weeks
- [ ] Then share article as discussion, not self-promotion
- [ ] One good Reddit post can bring 100+ subscribers
- [ ] Reddit users WILL check your post history — don't spam

### Priority 5: SEO (long game, compounds over time)
- [ ] Every article optimized per checklist above
- [ ] Substack posts indexed within 1-3 hours
- [ ] Educational content with search demand brings steady organic traffic
- [ ] Focus on keywords your YouTube videos already rank for

---

## Cross-References

- **Subject line scoring:** `python -m tools.newsletter.subject_line_scorer "Subject Here"`
- **Article quality gate:** `python -m tools.newsletter.article_scorer path/to/article.md`
- **Article writing style:** `.claude/REFERENCE/WRITING-VOICE-AND-STYLE-P6-ARTICLE.md` + `-P7-NEWSLETTER.md`
- **YouTube metadata (for cross-linking):** `.claude/REFERENCE/METADATA-CHECKLIST.md`
- **Launch roadmap:** `NEWSLETTER-LAUNCH-ROADMAP.md`
