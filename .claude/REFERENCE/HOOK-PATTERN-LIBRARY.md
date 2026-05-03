# Hook Pattern Library

Collected: 2026-03-23 | Channels: 10 (Atun-Shei Films, CaspianReport, Fall of Civilizations, Historia Civilis, Knowing Better, Kraut, Shaun, Three Arrows, TikHistory, WonderWhy) | Total verified hooks: 85 | Source: `tools/benchmark/TRANSCRIPT-STRUCTURE-ANALYSIS.md`

**Data source:** Real YouTube transcripts extracted via youtube-transcript-api + yt-dlp. All hooks are verbatim — auto-captions where manual not available.
**Usage:** Parsed by hook_scorer.py (Phase 69) and referenced by script-writer-v2 Rules 19 + 27.

**Performance by hook type (normalized views, 85 videos):**
| Hook Type | n | Avg Normalized Views | Confidence |
|-----------|---|---------------------|------------|
| specificity_bomb | 5 | 5.4x subscriber count | LOW |
| cold_fact | 11 | 3.7x subscriber count | MEDIUM |
| myth_contradiction | 1 | 4.6x subscriber count | VERY LOW |
| contextual_opening | 68 | 2.7x subscriber count | HIGH |

---

## Pattern: cold_fact

**Topic type:** territorial, political_fact_check
**Description:** Opens with a specific number, date, or measurement that reframes the scope of the question before any context is provided.
**Hook-to-topic fit:** Highest fit for territorial disputes and historical surveys. Numbers anchor the viewer's attention and signal evidence-based content.
**Performance:** 3.7x subscriber count normalized views (n=11/85, MEDIUM confidence). Second-best performing hook type.

### Examples (from 100K+ sub channels)

1. Channel: Fall of Civilizations | Video: 13. The Assyrians - Empire of Iron | Views: 21,313,326 | First sentence: "In the year 401 BC, at the height of the period known as the Greek Golden Age, a Persian prince named Cyrus the Younger was fighting a bitter civil war against his brother, and was trying to seize the throne of Persia. To help him in this fight, he h"
2. Channel: Fall of Civilizations | Video: 18. Egypt - Fall of the Pharaohs | Views: 11,995,193 | First sentence: "Around the year 1200 AD, the medieval Arab traveler and scholar Abd Al-Latif Al-Baghdadi departed from his hometown of Baghdad and set out on a journey of exploration. As a young man, Al-Baghdadi had studied law, medicine, and philosophy, and was ins"
3. Channel: Fall of Civilizations | Video: 17. Carthage - Empire of the Phoenicians | Views: 11,626,608 | First sentence: "In the year 1858, the French novelist Gustave Flaubert arrived in North Africa hoping to find inspiration for his latest book. Flaubert was a seasoned traveler, and a decade or so earlier had embarked on a grand tour of Cairo, Constantinople, Greece,"
4. Channel: Fall of Civilizations | Video: 18. Egypt - Fall of the Pharaohs | Views: 7,711,456 | First sentence: "around the year 1200 ad the medieval Arab traveler and Scholar ABD Al Latif Al Bagdad departed from his hometown of Baghdad and set out on a journey of exploration as a young man al- bagdadi had studied law medicine and philosophy and was inspired by"
5. Channel: Fall of Civilizations | Video: 11. Byzantium - Last of the Romans | Views: 7,077,101 | First sentence: "in the year 1852 the French writer and translator Te'o Figo ta made a journey to the city then known as Istanbul the capital of the Ottoman Empire thanks to the new technology of the steamship that now Criss crossed the Mediterranean he made the jour"
6. Channel: Knowing Better | Video: If Veterans Ruled the World | Starship Troopers | Views: 2,287,663 | First sentence: "In 1997, I was in middle school and the best movie ever was released – Starship Troopers, an alien war movie with boobs. It instantly became one of my all-time favorites. I’ve made no attempt to hide the fact that in my younger years, I was a liberta"
7. Channel: CaspianReport | Video: Why Zimbabwe wants its ‘white farmers’ back | Views: 2,061,134 | First sentence: "This is a $100 trillion bank note from Zimbabwe. One of the most worthless currencies ever. The paper it's printed on is worth more than the money itself."
8. Channel: Toldinstone | Video: Where Every Roman Emperor was Buried | Views: 303,914 | First sentence: "over the Millennium and a half that separate the rise of Augustus from the fall of Constantinople there were about 150 Roman emperors they reigned on average 11 years living to a median age of 51 not quite half met unnatural ends some Emperors never "
9. Channel: WonderWhy | Video: The Breakup of Yugoslavia | Views: 6,556,972 | First sentence: "for most of the 20th century there existed a country in Southeastern Europe called Yugoslavia today however what used to be Yugoslavia is now six fully independent countries"
10. Channel: Historia Civilis | Video: The Bronze Age Collapse (approximately 1200 B.C.E.) | Views: 4,983,791 | First sentence: "sometime around the year 1200 bce human civilization in the eastern mediterranean and the near east reached a tipping point"
11. Channel: Atun-Shei Films | Video: Holy Horror: A New History of John Brown | Views: 401,148 | First sentence: "in the year 1800 a man named John Brown was born in the state of Connecticut"

### Trigger mechanism
The brain interprets specific numbers as evidence rather than assertion. A precise number in the first sentence forces the viewer to update their mental model before engaging their existing narrative.

---

## Pattern: specificity_bomb

**Topic type:** territorial, ideological
**Description:** Opens with a hyper-specific named detail — a place, person, date, or document — that signals the creator has done research others haven't.
**Hook-to-topic fit:** Highest fit for document-based videos and long-form historical narratives. Fall of Civilizations uses this pattern exclusively in their outlier videos.

### Examples (from 100K+ sub channels)

1. Channel: CaspianReport | Video: The Israel-Iran War just changed everything | Views: 3,268,872 | First sentence: "The Cold War has turned hot overnight. In the early hours of June 13th, Israel launched preemptive strikes on Iran. Multiple explosions were heard across Thran with online footage showing blasts lighting up the capital."
2. Channel: Kraut | Video: The Mexican American Border | A Tale of two Colonies | Views: 1,930,770 | First sentence: "in arizona's southern county of santa cruz you will find the city of nogales at first glance an average american city with a population of slightly over twenty thousand most of these are families of which the median income lies at almost thirty thous"
3. Channel: Toldinstone | Video: How did the Egyptians forget Hieroglyphs? | Views: 690,177 | First sentence: "Here in the temple of Isis at Fel is the last hieroglyphic inscription ever written. It reads, "Before Mandulus, son of Horus, by the hand of Nesmetar, son of Nesmet, the second priest of Isis for all time and eternity. Words spoken by Mandulus, Lord"
4. Channel: Toldinstone | Video: Why isn't Roman Concrete used today? | Views: 330,401 | First sentence: "I'm Garrett Ryan this is toen Stone Roman concrete redefined architecture it allowed towering apartment blocks to rise with Incredible speed it made break Waters that defied the waves it supported the Colossal vaults of the Imperial bads and the Dome"

5. Channel: Historia Civilis | Video: The Longest Year in Human History (46 B.C.E.) | Views: 7,244,648 | First sentence: "in the summer of the year 46 BCE Julius Caesar found himself in a very precarious situation"
6. Channel: WonderWhy | Video: Why Ireland Split into the Republic of Ireland & Northern Ireland | Views: 6,159,559 | First sentence: "this is the island of Ireland the island is split into two countries Northern Ireland which is part of the United Kingdom and the Republic of Ireland"
7. Channel: TikHistory | Video: Where do our modern ideologies come from? (Timeline Map) | Views: 539,587 | First sentence: "this is the map we're going to talk about today a map showing all the major ideologies and their evolution from the 17th century"
8. Channel: Shaun | Video: Stellar Blade: The Fake Outrage | Views: 2,032,108 | First sentence: "hello everyone imagine if you can the following scenario"

**Sample size note:** 8 verified examples across 85 videos (9.4%). Highest normalized views (5.4x) but LOW confidence due to small n. Treat as promising signal, not proven rule.

### Trigger mechanism
Specificity signals primary source access. The viewer implicitly reasons: 'If they know that detail, they've done research I haven't.' Creates instant authority transfer.

---

## Pattern: myth_contradiction

**Topic type:** ideological, political_fact_check
**Description:** States the standard answer most viewers hold, then immediately contradicts or qualifies it. The gap between belief and reality keeps the viewer engaged.
**Hook-to-topic fit:** Highest fit for ideological myth-busting and revisionist history. Works when the audience has a pre-existing belief that can be named.

### Examples (from 100K+ sub channels)

1. Channel: WonderWhy | Video: The Breakup of Yugoslavia | Views: 6,556,972 | First sentence: "for most of the 20th century there existed a country in Southeastern Europe called Yugoslavia today however what used to be Yugoslavia is now six fully independent countries plus one more self- declared independent country but more than that later so"
2. Channel: Knowing Better | Video: The Part of History You've Always Skipped | Neoslavery | Views: 6,026,235 | First sentence: "This video is going to look and sound a little different from my usual content because this topic is serious, complex, and infuriating. It’s also incredibly long, as you’ve probably noticed, but it is necessary to understand the full picture. As we’r"
3. Channel: WonderWhy | Video: The Most Complex International Borders in the World - Part 2 | Views: 4,671,178 | First sentence: "international borders can be very complicated I showed this in a previous video of Maine but there are still plenty more complex international borders in the world lake last time I'm going to start by looking in Cleaves and eights Cleaves the first c"
4. Channel: WonderWhy | Video: What's the Difference Between Latino and Hispanic? | Views: 3,913,052 | First sentence: "have you ever wondered what's the difference between the terms Latino and Hispanic most people use these words interchangeably but there is actually a difference there is a huge overlap I.E most people who are Latino are also Hispanic and vice versa "
5. Channel: Knowing Better | Video: American Exceptionalism but as a Religion | Mormons | Views: 2,569,419 | First sentence: "We should all know the American creation myth, but for the two or three of you that don’t. It all started when a group of religious conservatives who didn’t think the Church of England was Protestant enough were kicked out of a number of European cou"
6. Channel: CaspianReport | Video: Pakistan, Afghanistan, and Iran heading to war? | Views: 1,877,901 | First sentence: "this is where the Triad of Iran Afghanistan and Pakistan lies it is a region full of activity though often for the wrong reasons here communal life is broken International borders are breached daily and both militants and militaries Carry Out secret "
7. Channel: Kraut | Video: America's foreign Entanglement | Views: 1,654,449 | First sentence: "pacifism is objectively pro-fascist this is elementary common sense if you hamper the war effort of one side you automatically help out that of the other nor is there any real way of remaining outside such a war as the present one in practice he that"
8. Channel: Toldinstone | Video: Why Roman Cities were Abandoned in the Middle Ages | Views: 796,349 | First sentence: "London, Paris, Milan, and hundreds of other cities founded by the Romans are still thriving today, but hundreds more in every part of the former classical world have been abandoned. I'm standing in the ruins of Tsus in what is now southern Turkey. Th"

### Trigger mechanism
Cognitive dissonance exploitation. Stating the viewer's belief triggers recognition; contradicting it creates discomfort only the video can resolve.

---

## Pattern: contextual_opening

**Topic type:** territorial, ideological
**Description:** Opens with a broad philosophical question or observation that sets the conceptual frame before narrowing to specifics.
**Hook-to-topic fit:** Used by Kraut for grand-narrative videos. Less hook-optimized but effective for loyal audiences who expect depth.

### Examples (from 100K+ sub channels)

1. Channel: Kraut | Video: Trump's Biggest Failure | Views: 5,375,616 | First sentence: "somewhere more less close to you there's a prison and in that prison a business transaction took place today with the currency use being anything from ramen noodles to cigarettes prison economies are frowned upon that justice systems mostly tried to "
2. Channel: Kraut | Video: How Vodka ruined Russia | Views: 4,779,695 | First sentence: "when you search through history books you will find many anecdotes on the role that alcohol and other addictive substances played in shaping societies throughout human history the Pharaohs of ancient Egypt paid their farm laborers in bread and beer G"
3. Channel: Kraut | Video: The Turkish Century | From Hittites to Atatürk | Views: 3,223,249 | First sentence: "what ties a people to their land what makes land yours how can land even be yours the idea of the nation-state is barely 200 years old and before that idea the notion of land as a collective property of a cultural or national construct didn't exist t"
4. Channel: Kraut | Video: India & Pakistan - A continuing Story | Views: 2,715,073 | First sentence: "cars dominate the world of personal transport the industry sectors built around them are so large that they are their own category of geopolitical power players for the first half of the 20th century the americans dominated that market they invented "
5. Channel: Knowing Better | Video: They Were Just in the Way | Indian Removal | Views: 2,541,338 | First sentence: "Well, it’s that time of year again, the kids are back in school and are learning about Columbus, the Pilgrims, and the founding of our nation. Growing up in the United States and then becoming a high school history teacher, I’ve both learned and taug"
6. Channel: Knowing Better | Video: Temporary Residents in this World | Jehovah's Witnesses | Views: 1,871,615 | First sentence: "Youtube gurus like to- [Clears throat] Youtube gurus often target smaller channels with promises of exponential channel growth. [Skype ringtone] Who even uses Skype anymore? What?... Hello?"
7. Channel: Kraut | Video: The Origins of Russian Authoritarianism | Views: 1,847,881 | First sentence: "nomadic empires were some of the most fascinating entities in human history originating from the steps of central asia most lived in isolation unbothered by neighbouring empires who saw their lands as worthless this isolation allowed many nomadic tri"
8. Channel: Knowing Better | Video: God's Alternative Medicine | Christian Science | Views: 1,728,976 | First sentence: "Over the course of this channel’s existence, I’ve become something of a scholar of American-born religions, and one in particular seems to keep popping up in those discussions. So, today – Hey! The people have spoken, it’s time for another religion v"

### Trigger mechanism
Appeals to intellectual curiosity rather than information gap. Works when the question itself is inherently interesting.

---

## Pattern: authority_challenge

**Topic type:** ideological, political_fact_check
**Description:** Names an established authority or expert consensus and promises to show why it's wrong or incomplete.
**Hook-to-topic fit:** High-risk, high-reward. Effective with 25-44 male demographic valuing intellectual independence.

### Examples (from 100K+ sub channels)

**No verified examples in current sample.** Expand channel set to find examples.

### Trigger mechanism
Activates the viewer's independence instinct. The explicit naming of authority before undermining it positions the video as speaking truth to power.

---

## Usage Notes for hook_scorer.py (Phase 69)

Pattern sections formatted for programmatic parsing:
- `## Pattern: {name}` — section delimiter (grep target)
- `**Topic type:**` — topic fit annotation
- `### Examples (from 100K+ sub channels)` — example block start
- Numbered list format: `N. Channel: {name} | Video: {title} | Views: {count} | First sentence: "{text}"`
- `### Trigger mechanism` — human reference block

```
grep "^## Pattern:" .claude/REFERENCE/HOOK-PATTERN-LIBRARY.md
```

**Integration with script-writer-v2 Rule 19 (4-beat hook formula):**
- `cold_fact` provides Beat 1 (Cold Fact) examples
- `myth_contradiction` provides Beat 2 (Myth) + Beat 3 (Contradiction) combined
- `specificity_bomb` enhances Beat 1 with document-anchor variation
- `authority_challenge` provides alternative Beat 2 framing for named-figure topics

**Data quality:** All hooks are verbatim from real YouTube transcripts. No paraphrases, no training-data guesses.

---

## CRITICAL: Title-Content Alignment Rule (2026-03-25, Tordesillas retention data)

**Hook pattern matters less than title-hook alignment.** A well-crafted hook will still hemorrhage viewers if the title creates a different expectation.

**Evidence:** Tordesillas (16.7% avg retention). Title: "A 530-Year-Old Treaty Still Affects Brazilians Today." Hook: contextual_opening with geography → 1494 date → contradiction. The hook was well-written — but 37% of viewers left at 0:18 when "1494" landed because the title promised modern Brazil.

**Rule:** Before selecting a hook pattern, check: does the title promise modern relevance, a mystery, a mechanism, or historical evidence? The hook's first 15 seconds must deliver a TASTE of whatever the title promised. If the title says "Today" or "Still," open with today — not with history.

**Title-hook alignment matrix:**

| Title Promises | Hook Must Open With | Example |
|---|---|---|
| Modern impact ("Still," "Today") | Modern fact, then historical cause | GDP map → "because of a line drawn in 1494" |
| Mystery ("One Letter," "Nobody Knows") | The mystery object/question | Document on screen → quote → "but someone is ignoring it" |
| Mechanism ("How," "Why") | The mechanism in action | "The British didn't rule. They cut." |
| Historical evidence ("The Document") | The document | Document zoom → quote → stakes |
