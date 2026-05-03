# Retention Curve Shape Analysis
**Generated:** 2026-03-21
**Videos analyzed:** 42

## Classification Rules

| Shape | Criteria |
|-------|----------|
| cliff | Retention at 10% mark < 50% of start, then drops < 30% more |
| slow_burn | No 10-point segment drops > 15%, linear R² > 0.85 |
| bump | After 15% mark, retention increases >= 3% over previous 10 points |
| plateau | After 20% mark, retention stdev < 0.03 (nearly flat) |
| other | Does not clearly fit any category |

## 1. Shape Distribution

| Shape | Count | % | Avg Views | Avg Retention |
|-------|------:|--:|----------:|--------------:|
| cliff | 9 | 21% | 255 | 22.2% |
| slow_burn | 0 | 0% | 0 | 0.0% |
| bump | 17 | 40% | 49 | 28.3% |
| plateau | 1 | 2% | 11 | 25.1% |
| other | 15 | 36% | 742 | 32.8% |

## 2. Shape × Traffic Source

| Shape | Search % | Suggested % | Subscriber % | Total Views |
|-------|--------:|-----------:|-------------:|------------:|
| cliff | 6.1% | 9.5% | 67.8% | 2,091 |
| slow_burn | 0.0% | 0.0% | 0.0% | 0 |
| bump | 23.0% | 19.9% | 22.0% | 792 |
| plateau | 0.0% | 9.1% | 0.0% | 11 |
| other | 4.7% | 26.3% | 57.8% | 11,107 |

## 3. Shape × Topic Type

| Topic | cliff | slow_burn | bump | plateau | other | Total |
|-------|------:|------:|------:|------:|------:|------:|
| colonial | 0 | 0 | 3 | 0 | 1 | 4 |
| factcheck | 0 | 0 | 1 | 0 | 0 | 1 |
| general | 0 | 0 | 4 | 0 | 2 | 6 |
| ideological | 2 | 0 | 3 | 0 | 5 | 10 |
| legal | 0 | 0 | 0 | 0 | 1 | 1 |
| territorial | 7 | 0 | 6 | 1 | 6 | 20 |

## 4. Bump Analysis

Where do mid-video recoveries happen?

| Video | Position | Timestamp | Zone | Magnitude |
|-------|--------:|-----------|------|----------:|
| Why a 1908 Map is Still Killing People: Thailand v... | 50% | 3:41 | mid | +12.9% |
| Putin Says NATO Promised Not to Expand. The Docume... | 33% | 1:52 | early | +10.4% |
| "Putin Copied Serbia's Playbook. Here's the Origin... | 76% | 9:15 | late | +10.0% |
| Spain vs Peru. 300 Years of Colonial Lies Exposed | 88% | 11:03 | late | +8.9% |
| Iran vs the CIA. Two Coups the West Wants You to F... | 62% | 12:33 | mid | +8.6% |
| How 3 Coups Ended 60 Years of French Control in Af... | 87% | 11:46 | late | +6.9% |
| | Britain Expelled 2,000 Islanders. The Memo Prove... | 49% | 5:12 | mid | +6.9% |
| The CIA Document That Proved Operation Condor | 43% | 2:03 | mid | +5.9% |
| Russia vs Georgia. The Rehearsal for Ukraine | 34% | 2:02 | early | +5.0% |
| The 1713 Document That Still Controls Gibraltar's ... | 78% | 10:59 | late | +4.9% |
| 1,000 Years of Ukraine: The History Putin Erased | 64% | 6:20 | mid | +4.8% |
| JD Vance vs History: Who Invented Human Rights? | 68% | 7:45 | late | +4.6% |
| Iran vs Its Own Democracy. 120 Years of Failed Rev... | 35% | 4:48 | mid | +4.6% |
| Was Lagertha Real? DNA Says Female Viking Warriors... | 55% | 5:33 | mid | +4.2% |
| The 1922 Treaty Loophole That Ended the USSR | 57% | 2:45 | mid | +3.8% |
| Britain Promised the Same Land to Three Different ... | 50% | 5:33 | mid | +3.1% |
| The CIA Knew Cyprus Would Be Invaded. They Let It ... | 32% | 2:57 | early | +3.0% |

**Bump zone distribution:**
- early: 3 videos
- mid: 9 videos
- late: 5 videos

## 5. Best-Performing Shapes

**Highest avg views:** other (742 avg, n=15)
**Highest Suggested traffic:** other (26.3% of traffic)
**Highest avg retention:** other (32.8%, n=15)

## Interpreted Findings

- **other** curves average 742 views vs **plateau** at 11 views (67.5x difference).
- **bump** curves get the most Search traffic (23.0%), suggesting these videos rank well for their target keywords.
- **other** curves get the most Suggested/Related traffic (26.3%), indicating the algorithm recommends these videos more.
- 17 videos show mid-video recoveries (avg +6.4%), most commonly in the **mid** section. Investigate what content triggers these recoveries.
- **ideological** videos are predominantly **other** (50%, n=10).
- **general** videos are predominantly **bump** (67%, n=6).
- **colonial** videos are predominantly **bump** (75%, n=4).

## Appendix: Per-Video Classifications

| Video | Shape | Views | Retention |
|-------|-------|------:|----------:|
| Guatemala vs Belize Dispute: What 3 ICJ Cases Show | other | 5,120 | 38.4% |
| Venezuela vs Guyana: The Oil War Over Essequibo | other | 1,964 | 34.5% |
| JD Vance Claims Christians Found Child Sacrifice. Here'... | other | 1,132 | 26.4% |
| Why TURKEY and GREECE Can't Agree on these islands. | other | 925 | 39.0% |
| Primary Sources Destroy the 'Awesome Crusades' Narrativ... | cliff | 674 | 26.8% |
| 5 Big Myths About Israel and Palestine Busted! | other | 627 | 31.0% |
| Somaliland's Legal Independence Problem | cliff | 394 | 23.6% |
| How the KGB Weaponized Palestinian Resistance | other | 288 | 41.5% |
| China vs Taiwan. 4 Historical Claims Exposed by Scholar... | cliff | 255 | 27.7% |
| India vs Pakistan. Britain Sold Kashmir for 7.5 Million... | cliff | 224 | 19.5% |
| They Split 229 Ethnic Groups. Here's the Map They Ignor... | cliff | 207 | 16.8% |
| The Flat Earth Myth Was Invented in 1828. Here's Who Di... | cliff | 207 | 12.1% |
| Did Pagans Actually Copy Christmas? | other | 194 | 22.8% |
| Fact-Checking Nick Fuentes: Why His Claims Are Dangerou... | cliff | 168 | 25.6% |
| Why Trump Walked Back the Armenian Genocide | other | 159 | 26.4% |
| Stalin Purged His Own Army. Then Hitler Invaded | other | 121 | 36.2% |
| London's Stock Exchange Funded a Genocide | other | 118 | 31.4% |
| The "Dark Ages" Never Happened. Here's the Proof. | other | 110 | 29.5% |
| The Hidden Pattern Behind the Armenia Conflict | other | 110 | 29.5% |
| The 200‑Year‑Old Tariff Myth That Drains Your Wallet | other | 105 | 28.4% |
| Morocco's 1,700-Mile Wall (And the Vote That Never Happ... | cliff | 105 | 26.5% |
| The CIA Knew Cyprus Would Be Invaded. They Let It Happe... | bump | 99 | 33.5% |
| Britain Promised the Same Land to Three Different Group... | bump | 96 | 35.7% |
| China Claims the Entire South China Sea. A Court Said N... | other | 91 | 49.6% |
| 1,000 Years of Ukraine: The History Putin Erased | bump | 85 | 24.1% |
| Why Egypt and Sudan Both Reject Bir Tawil | cliff | 69 | 20.9% |
| Vichy France: The Anti-Jewish Law Nobody Translated | other | 67 | 27.0% |
| Iran vs Its Own Democracy. 120 Years of Failed Revoluti... | bump | 64 | 24.9% |
| "Putin Copied Serbia's Playbook. Here's the Original | bump | 60 | 34.1% |
| Was Lagertha Real? DNA Says Female Viking Warriors Exis... | bump | 48 | 28.3% |
| Putin Says NATO Promised Not to Expand. The Documents D... | bump | 47 | 45.7% |
| Spain vs Peru. 300 Years of Colonial Lies Exposed | bump | 46 | 28.0% |
| JD Vance vs History: Who Invented Human Rights? | bump | 44 | 32.5% |
| Russia vs Georgia. The Rehearsal for Ukraine | bump | 40 | 22.5% |
| The 1713 Document That Still Controls Gibraltar's Borde... | bump | 39 | 28.1% |
| Iran vs the CIA. Two Coups the West Wants You to Forget | bump | 35 | 21.8% |
| The CIA Document That Proved Operation Condor | bump | 34 | 19.6% |
| Why a 1908 Map is Still Killing People: Thailand vs. Ca... | bump | 31 | 24.7% |
| How 3 Coups Ended 60 Years of French Control in Africa | bump | 28 | 16.7% |
| | Britain Expelled 2,000 Islanders. The Memo Proves It | bump | 27 | 32.1% |
| The 1922 Treaty Loophole That Ended the USSR | bump | 26 | 28.3% |
| Mexico's Missing Island: The Map Error That Cost $22 Bi... | plateau | 11 | 25.1% |
