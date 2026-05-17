# Launch Checklist — Stream 3 (Toolkit)

Sequential steps to take the bundle from "files on disk" to "first $49 in your bank account." Estimated total time: 8-10 hours over 5-7 days.

## Day 1 — Polish bundle (2h)

- [ ] Read `PACKAGING-SYSTEM.md` end-to-end. Catch typos, fix any claim that no longer matches reality.
- [ ] Replace placeholder `[Your Name]` and `{your-email}` in `GUMROAD-LISTING.md` and `MARKETING-COPY.md`.
- [ ] Run `title_scorer_standalone.py` on 5 of your own real titles. Confirm scores match your intuition. Adjust word lists if not.
- [ ] Convert `PACKAGING-SYSTEM.md` to PDF. Free options:
  - VS Code + "Markdown PDF" extension (one click)
  - Pandoc: `pandoc PACKAGING-SYSTEM.md -o PACKAGING-SYSTEM.pdf --pdf-engine=xelatex`
  - Or paste into Google Docs → File → Download → PDF
- [ ] Create cover image. Canva free template: title, subtitle, "47 Videos. 173% Growth in 90 Days. Calibrated CTR data." Export 1200x630 (Gumroad cover spec).

## Day 2 — Set up Gumroad (1.5h)

- [ ] Sign up for Gumroad (free, no fees on first $1k of sales).
- [ ] Create new product. Paste fields from `GUMROAD-LISTING.md`.
- [ ] Upload bundle ZIP:
  ```
  history-youtube-packaging-system-v1.zip/
    PACKAGING-SYSTEM.pdf
    PACKAGING-SYSTEM.md       (source markdown for buyers who prefer it)
    LICENSE.txt
    CHANGELOG.md
    scripts/
      title_scorer_standalone.py
      README.md
  ```
- [ ] Set price: $49 base.
- [ ] Add second product "Loom Title Review (Add-On)" at $50 with a description like: *"Send 5 of your titles + your channel link. You'll receive a 60-min async Loom video applying the methodology to your specific channel within 5 business days. Only available with the main Packaging System purchase."*
- [ ] Configure post-purchase email (template in `GUMROAD-LISTING.md`).
- [ ] Add the License + Changelog as visible files on the product page (transparency builds trust).
- [ ] Test purchase path with your own card or a friend's. Refund the test purchase.

## Day 3 — Build cold-email list (2h)

- [ ] Open YouTube. Search for terms in your niche: "history documentary", "geopolitics explained", "border dispute", "treaty history", whatever sub-niches overlap with yours.
- [ ] Use "Channels" filter + sort by relevance.
- [ ] For each channel, check sub count. Target 1K-50K range. Skip <1K (they can't afford $49) and >50K (they probably already have an in-house process).
- [ ] Build a spreadsheet with columns: Channel name | URL | Sub count | Top video URL | Top video title | Email/contact | Notes
- [ ] Public emails are usually in:
  - Channel "About" tab → "View email address"
  - Linked Twitter/X bio
  - Linked Instagram/website contact form
- [ ] Stop at 30 channels. Quality > quantity.

## Day 4 — Send first batch of cold emails (3h)

- [ ] For each channel, run their top 5 titles through `title_scorer_standalone.py`. Save the output.
- [ ] Identify the most interesting scoring observation per channel (different for each — that's the personalization).
- [ ] Personalize the email template from `MARKETING-COPY.md`. Send 5-7 emails Tuesday morning their time.
- [ ] Track in your spreadsheet: Sent date | Subject variant | Open (if you can track) | Reply (Y/N) | Reply content | Sale (Y/N).

## Day 5 — Reddit case-study post (1h)

- [ ] Post the r/NewTubers case-study from `MARKETING-COPY.md` Wednesday 9-10am ET.
- [ ] Reply to comments for the next 3-4 hours. Score titles publicly when asked. Don't sell — just demonstrate.
- [ ] Move post to r/PartneredYoutube the next day with the slight reframe.

## Day 6-7 — Twitter thread (optional, 1h + ongoing)

- [ ] Only do this if you'll commit to 2-3 follow-up threads over the next week. Otherwise skip — single threads die.
- [ ] Post Friday 9-11am ET.
- [ ] Pin to profile.
- [ ] Score titles in replies.

## Week 2+ — Iterate

- [ ] Send 5-10 more cold emails per day, Tue-Thu.
- [ ] Post one new Reddit comment-friendly insight per week (different angle: thumbnail rules, then 48h protocol, then retitle decision tree).
- [ ] Track sales weekly. Compare which channel/sub drove which sale.
- [ ] After 50 sales: raise price to $69. After 100 sales: $89.
- [ ] After 5 Loom buyers: raise Loom tier to $149.

## Red flags / things that mean "stop and rethink"

- **2+ weeks, 100+ emails, 0 sales:** Subject lines or pitch is wrong. Try variant B for 50 more emails. If still 0 sales, the product isn't matching the market — pivot to selling the *consulting* version (1-on-1 channel review at $200 instead of the productized PDF).
- **Multiple refunds in week 1:** PDF doesn't deliver on the promise. Read the refund reason carefully. Probably means the PDF needs more concrete "rewrite this BAD title to this GOOD title" examples.
- **High open rate, low reply rate:** Subject line is good, body is weak. Strengthen the personalization line.
- **High reply rate, low sale rate:** People want to talk shop, not buy. That's fine — turn 2-3 of them into paid 1:1 consultations at $100/h instead.

## Success markers (week 4 check-in)

- [ ] 5+ sales = product-market fit signal. Continue.
- [ ] 10+ sales = early traction. Start v2 refactor on the side (1-2h/day).
- [ ] 1+ Loom upsell = high-value tier validated. Raise price.
- [ ] 0 sales after 4 weeks = pivot. The methodology likely belongs in the Substack instead.
