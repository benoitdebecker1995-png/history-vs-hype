# Live Thumbnail Field Scan — #57 / #58 / #59

**Date:** 2026-06-03 · **Method:** pulled the live top-SERP YouTube thumbnails for each video's target query (i.ytimg.com maxres), read every image directly. 22 competitor thumbnails across 3 topics. This is the *current* competitive field, not the month-old corpus — the goal is to find the visual cliché each field has converged on, so our thumbnail can break it.

> Differentiation logic (from `PER-CHANNEL-THUMBNAIL-PLAYBOOK`): you don't win by executing the niche template better — you win by being the one thumbnail that doesn't look like the other nine. For each topic: (1) what the field converged on, (2) the gap, (3) the play.

---

## #57 Piri Reis — `query: "Piri Reis map"`

**The field converged on (8/8):** aged-parchment map background + red arrow/circle + pseudo-archaeology claim. Every single one.
- "ANCIENT CIVILIZATION MAPPED THE WORLD FIRST?" + red arrow (ubkM)
- "ANTARCTICA!?" red circle, map + Suleiman portrait (wxbq)
- AI-slop fake news desk, "ALIEN BASE / PYRAMIDS", "THIS IS NOT POSSIBLE!" (PYm3)
- "Inner Earth" guy, "Shatters our Understanding of History" (pjpW)
- a REACTION video reacting to ubkM's thumbnail (ddY6)

**The gap:** the **entire field is the conspiracy/Antarctica frame.** Not one thumbnail represents the historical-truth or Ottoman angle. The parchment-map-with-red-arrow is so universal it's invisible — if we use it, we ARE the field.

**The play (our angle = "What Hancock Gets Wrong / the Ottoman text nobody reads"):**
- **Do NOT lead with the parchment map.** It's the single most saturated visual in the field.
- Route to **Three Arrows partial-transfer** (per playbook): recognizable **Graham Hancock face** + a charged debunk term (`ACTUALLY MEDIEVAL`, `NOT ANTARCTICA`, `THE TEXT SAYS…`). Hancock is the known figure with the checkable claim — the face anchors, the term creates the gap.
- Alternative: **Knowing Better COMPRESSION** — tight crop on the actual **Ottoman script** on the map (the text nobody reads) with a 2-word overlay. Makes the *document* the hero, which is literally the thesis. No red arrow.
- Either inverts a field that is 100% sensation. **This is the easiest differentiation of the three** — the field has left the entire "sober debunk" lane empty.

---

## #58 Kurdistan — `query: "Kurds / Kurdistan history"`

**The field converged on:** Kurds as **stateless / forgotten / divided / victim**, in flag colors (red-green-yellow).
- "THE MILITARY HISTORY OF A STATELESS NATION" (jWYs)
- "WHY IS KURDISTAN DIVIDED?" flag-colored map (kJuG)
- "THE FORGOTTEN NATION" + war/refugee photo (Her4)
- "SOLD OUT" — dark betrayal silhouette, handshake over glowing Kurdistan (4hy8)
- WonderWhy-style map + arrow + historical figure (T6uW)
- AI traditional-dress portrait, no text (dagq)
- Two standouts that break flag-color: WaPo **forensic B&W archival collage** (-O5P) and the dark **"SOLD OUT" dossier** (4hy8)

**The gap:** **every thumbnail frames Kurds as powerless** — stateless, divided, forgotten, sold out, refugees. **Nobody frames them as having HAD states/power.** That is exactly our locked angle ("The Kurds Had Their Own States for 300 Years").

**The play:**
- **Invert the victimhood monopoly — show power, not loss.** A Kurdish *ruler/dynasty* (Saladin is in our research, C1) or a map of the Kurdish **states** that existed — not the modern divided-victim shape everyone uses.
- Two playbook routes: **Knowing Better historical-photo** (Saladin / a dynasty figure + COMPRESSION `THEY HAD STATES`) OR **WonderWhy map-as-answer** (map showing the historical Kurdish states, title compressed to 3–5 words).
- **Avoid the red-green-yellow flag palette** — it's the field's wallpaper. The two thumbnails that stand out (WaPo B&W, "SOLD OUT" dark) both *drop* the flag colors. A desaturated/archival or dark-dossier treatment will pop against the flag-color wall.

---

## #59 Israel/Palestine — `query: "Israel Palestine partition"`

**The field converged on:** the **blue/orange UN partition map** + "1947" + B&W 1947–48 archival.
- Navy/cream partition map, "1947", "UN PARTITION PLAN / A TURNING POINT" (wIyh)
- Blue/orange satellite partition map + B&W founder portrait (9bYn)
- Al Jazeera B&W Nakba refugee photo (tbKQ)
- The Hindu podcast, two talking heads, B&W 1947 assembly bg (Rb4J)
- countryball "WHY DOES GAZA EXIST?" (GrUR)
- whiteboard animation (of_m8)

**The gap:** the field shows the **map** (the partition lines) and the **outcome** (refugees, the divide). **Nobody shows the *document* — the offer itself — as a readable object.** Our angle is literally "The Offer Nobody Actually Read" + Claims-on-Trial doc-on-screen.

**The play (this is the cleanest fit to a playbook exemplar of all three):**
- **PolyMatter DOSSIER METAPHOR** — make **Resolution 181 / the partition offer** the hero: the actual document, highlighted/annotated/redaction-bar aesthetic, overlay `THE OFFER` or `NOBODY READ IT`. Matches our "intellectual competence" trigger and the Claims-on-Trial series identity.
- **Be the document, not the map.** The map is the field's wallpaper (and a search-skim signal, so optionally keep a *small* partition-map reference in-corner — but the document is the hero).
- Caveat: most crowded + most sensitive field of the three. The dossier/document frame is also the *safest* — it signals forensic neutrality (referee, not partisan), which the flag/refugee/countryball thumbnails do not.

---

## Cross-topic takeaways
1. **All three fields have left our exact lane empty** — sober/forensic/document-first. The channel's differentiator (intellectual competence, primary source on screen) is *also* the thumbnail differentiator in all three SERPs.
2. **The document-as-hero move recurs** (#57 Ottoman script, #59 Resolution 181) — and no competitor in either field does it. That's the PolyMatter dossier operation, our most underused.
3. **Drop the field's house palette:** parchment (#57), flag-colors (#58), navy/B&W partition (#59). Standing out is partly just *not* using the wallpaper color.
4. **Re-run the proper audit** (`thumbnail_image_audit.py --serp-ids …`) once each thumbnail is rendered — it'll CLIP-score our actual image against these exact competitor IDs (open_clip is installed). IDs are in `D:/tmp/thumb-field-scan/<topic>/`.

### Competitor IDs scanned
- **#57:** ubkM4U8BWfQ, wxbq67Odqjs, PYm3b4KpXA0, pjpWidpBQDw, Fk3HVcMVFTQ, 90BWEWnU31c, ddY6CbRcdXk
- **#58:** dagq_vokQ2E, T6uWgqE70yI, jWYslKbs01A, rv4Mb5QmWo8, -O5PEwU8bg4, kJuGlPEIHV4, 4hy8aVU1y9c, Her4F_XZ2dc
- **#59:** tbKQ5g8GCBc, wIyhnnpN5K0, of_m8l-6HKQ, 9bYnp9WP0cY, GrURIaTzYUs, Rb4J61GZGYA
