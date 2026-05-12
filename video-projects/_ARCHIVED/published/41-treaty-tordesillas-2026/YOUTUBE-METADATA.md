# YOUTUBE METADATA — Treaty of Tordesillas

**Video #41**
**Primary Keyword:** treaty of tordesillas (search vol: 2,703/mo, comp: 35)
**Secondary:** why brazil speaks portuguese, colonial borders, portuguese empire
**Duration:** ~12:45
**Rebuilt from SRT:** 2026-03-17

---

## TITLE OPTIONS (ranked by title_scorer.py)

*Audited CTR baselines (2026-03-12): versus ~3.7% (n=2), declarative 3.8% (n=19), how_why 3.3% (n=5). Year penalty -46%, colon penalty -28%.*

1. **Spain vs Portugal. They Split the World in Half.** — 48 chars, 75/B (versus)
   - Versus = best-performing pattern on this channel
   - Clean, searchable, immediately clear stakes
   - No colon, no year

2. **Brazil Spoke a Different Language for 200 Years. Portugal Killed It.** — 68 chars, 75/B (declarative + number bonus)
   - Specific number ("200 Years") + active verb ("Killed") = double bonus
   - Matches the actual video payoff (Tupi → Portuguese via 1757 decree)
   - Highest curiosity gap — most viewers don't know Brazil spoke Tupi
   - Risk: 68 chars is close to mobile truncation (70 max)

3. **Two Countries Split the World in Half. The Line Is Still There.** — 63 chars, 65/B (declarative)
   - Evidence-promise: "The Line Is Still There" = visual proof (economics data payoff)
   - Declarative two-punch

4. **A Pope Gave Two Countries the Entire World. Here's the Map.** — 59 chars, 65/B (declarative)
   - "A Pope" = personality hook + shock value
   - "Here's the Map" = evidence-promise

### Rejected (DO NOT USE)
- ~~Spain vs Portugal: The Treaty That Divided the World~~ — **REJECTED: colon (-28% CTR)**
- ~~The 1494 Line That Split the World (And You Can Still See It)~~ — **DOUBLE REJECTED: year (-46%) + "The X That Y" pattern (worst performer)**
- ~~Treaty of Tordesillas: How Spain and Portugal Divided the World~~ — **REJECTED: colon**

### A/B Test Plan
- **Launch:** Title 1 (versus — safest pattern, highest score)
- **48h:** If CTR < 3.5%, swap to Title 2 (curiosity gap + number + verb)
- **96h:** If still < 3.5%, swap to Title 3 (evidence-promise)

---

## POSTING

- **Day:** Monday (data: 9,689 avg views vs Friday 54)
- **Backup:** Tuesday
- **Time:** 16:00-18:00 UTC
- **Never:** Friday

---

## THUMBNAIL CONCEPTS

**Data note:** No text > text overlays (3.3% vs 2.0% CTR). Map thumbs ~1.7x more views than face thumbs. Checker result: PASS (80/100).
**Build method:** AI-generate the base map/globe, then composite in Photoshop (line, color grading, final polish).

---

### Concept A — The Line (pairs with Title 1: Spain vs Portugal)

**AI prompt base:**
> Satellite view of South America from space, dramatic lighting, dark ocean, continent lit from the side. A single bold glowing line runs perfectly north-to-south through eastern Brazil, splitting the continent. Left side has a warm golden/red tint, right side has a cool green tint. Photorealistic, cinematic, no text, no people, no UI elements.

**Photoshop finishing:**
- Adjust line position to match actual Tordesillas meridian (~49°W)
- Boost color split contrast (Spanish gold left, Portuguese green right)
- Add subtle flag watermark if needed (very low opacity)
- Ensure line reads clearly at phone size (minimum 4px width)

**Why it works:** Immediate visual question — "what is that line?" Map thumbnail, high contrast, no text, no face.

---

### Concept B — The Language Map (pairs with Title 2: Brazil Spoke a Different Language)

**AI prompt base:**
> Clean, stylized map of South America viewed from directly above. Every country is colored in one shade (warm red/orange) except Brazil, which is a completely different color (deep green or blue). The border between Brazil and the rest is sharp and dramatic. Flat design, bold colors, no text labels, no people, dark background.

**Photoshop finishing:**
- This is basically a language map: Spanish = one color, Portuguese = another
- Make the color contrast as extreme as possible (the "one of these is not like the others" effect)
- Optional: add a faint dotted line showing the original Tordesillas meridian cutting through Brazil — shows the line doesn't match the modern border
- NO country labels, NO text overlay

**Why it works:** The video literally opens with "Open a language map of South America. Almost the entire continent speaks Spanish. One country doesn't." This thumbnail IS that opening frame. Viewer clicks expecting to learn why.

---

### Concept C — The Old Map (backup / documentary feel)

**AI prompt base:**
> Aged parchment world map in the style of a 1500s Portuguese nautical chart (portolan style), with compass roses, sea monsters faintly visible, and a single bold red line drawn vertically through the Atlantic Ocean and South America. The map should look hand-drawn and historical, slightly yellowed, with ink splotches. No text, no modern elements.

**Photoshop finishing:**
- Overlay actual treaty text fragment (from your treaty.pdf) at very low opacity as texture
- Make the red line the focal point — thick, slightly rough-edged like drawn with a quill
- Vignette edges dark
- This reads as "old document" = documentary authority signal

**Why it works:** Targets the Shaun/Fall of Civilizations audience who click on document-aesthetic thumbnails. Lower CTR ceiling than map concepts but strong subscriber conversion signal.

---

### Title-Thumbnail Pairing Guide

| If launching with... | Use thumbnail... | Swap to... |
|---|---|---|
| Title 1 (Spain vs Portugal) | **Concept A** (satellite + line) | Title 2 + Concept B |
| Title 2 (Brazil Spoke a Different Language) | **Concept B** (language map) | Title 1 + Concept A |
| Title 3/4 (fallbacks) | **Concept A or C** | — |

**Always swap BOTH title and thumbnail together.** A title-thumbnail mismatch kills CTR.

---

## DESCRIPTION

```
Open a language map of South America. Almost the entire continent speaks Spanish — except the biggest country. Brazil.

That border between Spanish and Portuguese isn't a mountain range or a river. It's a treaty. Signed in 1494. Two countries drew a line through a world they'd never mapped, using a measurement that didn't exist yet.

But the treaty only gave Portugal a foothold. What turned it into half a continent was 60 years of shared monarchy, settlers who pushed west for slaves and gold, and a legal principle that said: you keep what you possess.

And for 200 years, Brazil didn't even speak Portuguese. The dominant language was Tupi. It took a government decree in 1757 to kill it.

In 2023, economists drew the old treaty line through modern Brazil. Income inequality is still measurably higher on one side. 530 years later.

CHAPTERS:
0:00 - The Language Map
1:00 - A Wind Pattern and a Pope
3:56 - The Treaty of Tordesillas
5:57 - Portugal Claims Brazil
7:08 - 60 Years Without a Border
8:44 - You Keep What You Possess
9:34 - Brazil Didn't Speak Portuguese
11:59 - The Line Is Still There

SOURCES:
- Laudares & Valencia Caicedo, "Tordesillas, Slavery and the Origins of Brazilian Inequality" (Journal of Development Economics, 2023)
- Anthony R. Disney, A History of Portugal and the Portuguese Empire, Vol. 2 (Cambridge UP, 2009)
- Patricia Seed, Ceremonies of Possession in Europe's Conquest of the New World (Cambridge UP, 1995)
- C.R. Boxer, The Portuguese Seaborne Empire, 1415-1825 (Penguin, 1969)
- Treaty of Tordesillas (1494) — full text at Yale Avalon Project

#history #tordesillas #brazil #portugal #spain #colonialism #whybrazilspeaksportuguese
```

---

## TAGS

```
treaty of tordesillas, tordesillas, why brazil speaks portuguese, spain portugal, brazil history, portuguese empire, spanish empire, inter caetera, pope alexander vi, borgia pope, volta do mar, tupi language, lingua geral, pombal, iberian union, bandeirantes, pedro cabral, uti possidetis, treaty of madrid 1750, brazilian inequality, colonial borders, line of demarcation, colonial history, history documentary, south america history
```

---

## PUBLISHING DAY

**Day:** Monday
**Data:** Monday avg 9,689 views (23x more than Thursday). Friday avg 54 — never publish Friday.
**Time:** 16:00-18:00 UTC
**Backup:** Tuesday
