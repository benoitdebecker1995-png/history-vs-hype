# Assets — Tripoli Article 11

Modern graphic assets for the Tripoli video. Designed to be **clearly modern** — no faux-period typography, no fake aging, no AI-generated imagery. They sit alongside real document scans and portraits (sourced per `B-ROLL-ASSET-MANIFEST.md`), not as substitutes for them.

---

## Files

| File | Purpose | Script anchor |
|---|---|---|
| `_shared.css` | Shared design system (typography, color, spacing). All HTML files link this. | — |
| `quote-card-1-hurgronje-371.html` | Hurgronje's "no equivalent whatever in the Arabic" line, page 371 | Beat 4 reveal |
| `quote-card-2-hurgronje-secretary.html` | Hurgronje's "stupid secretary"/"bombastic words" passage, page 371 | Beat 4 (immediately after the missing-Article-11 reveal) |
| `quote-card-3-miller-384.html` | Miller's "most extraordinary (and wholly unexplained)" comment, page 384 | Beat 6 closing buildup |
| `quote-card-4-spellberg.html` | Spellberg's "he probably never knew" — Joel Barlow attestation | Beat 5 (Barlow couldn't read Arabic) |
| `quote-card-5-crane-405.html` | Crane's "wielded as often by Christian nationalists as by militant secularists" | Beat 6 closing |
| `timeline-133-years.html` | The 133-year silence visualization — broken timeline, three events 1796-97, gap, three events 1930-2020 | Beat 6 closing setup |
| `side-by-side-frame.html` | Split-screen English Article 11 vs Arabic letter. Optional "MISSING IN ARABIC" overlay. | Beat 3→4 transition |
| `arabic-annotation-overlay.html` | Real Arabic scan + modern callout box + annotation label ("where Article 11 should be") | Beat 4 reveal |

---

## How to render and screenshot

### Step 1 — Open in a browser
Just double-click any `.html` file, or drag-drop into Chrome/Firefox/Edge. Files use Google Fonts (EB Garamond, Inter, JetBrains Mono) loaded via CDN — needs internet on first render. Browser caches after that.

### Step 2 — Set viewport to 1920×1080
The CSS fixes the frame at 1920×1080 (16:9 1080p). For consistent screenshots:

**Chrome / Edge — DevTools method (recommended, gives clean 1920×1080 PNG):**
1. Open file in browser
2. F12 to open DevTools
3. `Ctrl+Shift+M` to toggle device toolbar
4. Set dimensions to `1920 × 1080` (custom)
5. `Ctrl+Shift+P` → type "screenshot" → select **"Capture full size screenshot"**
6. Saves as PNG at exact 1920×1080 — no browser chrome, no scaling artifacts

**Browser full-screen method (faster, lower quality):**
1. F11 for full-screen
2. OS screenshot tool (Win+Shift+S, or whatever you use)
3. Crop to remove any browser chrome bleeding through

### Step 3 — Want 4K (3840×2160)?

**Option A — DevTools 2x zoom:**
1. In DevTools device toolbar, set dimensions to `1920 × 1080`
2. Set DPR (Device Pixel Ratio) to `2.0`
3. Capture full size screenshot → 3840×2160 PNG

**Option B — Edit `_shared.css`:**
- Change `width: 1920px; height: 1080px;` to `width: 3840px; height: 2160px;`
- Double the font sizes in the same file (`64px → 128px`, etc.)
- Re-render and screenshot
- (Slower; only do this if Option A fails for some reason)

---

## Swapping in the real scans

Two of the files (`side-by-side-frame.html`, `arabic-annotation-overlay.html`) reference image placeholders. Replace them once you've captured the HathiTrust scans per `B-ROLL-ASSET-MANIFEST.md` Section 1.1.

**Where to put scan files:**
Recommended path: `_research/documents/scans/`. Create the folder if it doesn't exist.

**What to swap:**

In `side-by-side-frame.html`, find the two placeholder blocks and replace each:

```html
<!-- BEFORE -->
<div class="placeholder">
  Drop English Article 11 scan here<br>
  <span style="font-size:13px;color:#5A4F3F;">(HathiTrust Hunter Miller Vol. 2, Tripoli section)</span>
</div>

<!-- AFTER -->
<img src="../_research/documents/scans/miller-vol2-english-article-11.jpg" alt="Article 11, English text">
```

Same swap for the Arabic side. And same swap in `arabic-annotation-overlay.html`.

**Annotation overlay — adjust callout position after swap:**
The `.callout` box in `arabic-annotation-overlay.html` is positioned at approximate coordinates (top: 28%, left: 18%, width: 64%, height: 22%). Once the real scan is in, open the file in browser and tweak those four values in the inline CSS until the callout box exactly outlines the area where Article 11 "should be." It's four numbers; takes 2 minutes.

---

## Design notes (so you can keep the system intact if you add more)

**Color palette:**
- Background: `#14110F` (warm charcoal — not pure black, reads better against video)
- Body text: `#F4EDE0` (cream — not pure white)
- Accent: `#E8D9A8` (warm gold for emphasized words)
- Muted: `#B8A88E` for attribution, `#8A7B66` for eyebrow labels
- Hairlines: `#5A4F3F`
- Annotation accent (callouts): `#E8B547` (saturated gold for the markup overlay color — clearly modern intervention)

**Typography:**
- Quote display: EB Garamond 64px regular (medium 56px and large 72px variants available)
- Eyebrow / category labels: Inter 16px 500 weight, 0.22em tracking, uppercase
- Attribution: EB Garamond 24px italic
- Page citation footer: Inter 14px regular, 0.12em tracking, uppercase
- Date stamps (timeline): JetBrains Mono 18px

**Why these choices:**
- EB Garamond is a digital revival of Claude Garamont's 16th-century types — period-appropriate without being a faux-period gimmick. It's a respected modern academic typeface (used in scholarly publishing). It signals "rigorous" without signaling "old."
- Inter for UI text reads as cleanly modern. The contrast between EB Garamond and Inter is what tells the viewer "this is a modern presentation of a historical quote," not "this is a fake old document."
- Cream text on warm charcoal beats white on black for video — less harsh, blends with footage temperature.

**What this design system avoids:**
- No faux-parchment textures, no torn-paper edges, no sepia gradients
- No blackletter (Old English, Cloister Black, etc.) — that's for medieval, not 1797
- No "vintage" filter overlays
- No drop shadows that mimic an old book
- No decorative initial caps or flourishes
- No icons, no decorative dividers (the single 80px hairline is the only line element)

If you build more cards in this style, follow the same template: dark background, single eyebrow, single quote, single thin divider, two-line attribution. Don't add ornament.

---

## Shot list integration

Per script `02-SCRIPT-DRAFT.md` v5-FINAL, suggested placement of these assets in the edit:

| Time (script) | Beat | Asset to cut to |
|---|---|---|
| ~1:13–1:16 | Beat 2 end → Beat 3 start | Real Arabic manuscript scan (HathiTrust); hold for 2s into silence before Article 11 reveal |
| ~1:30–1:50 | Beat 3 (Article 11 read) | Real English Article 11 scan (HathiTrust) — full-screen with key clause highlighted |
| ~1:50–2:00 | Beat 4 reveal — "the Arabic does not contain Article 11" | `side-by-side-frame.html` (with overlay) OR `arabic-annotation-overlay.html` |
| ~2:00–2:20 | Beat 4 — Hurgronje's verbatim line | `quote-card-1-hurgronje-371.html` |
| ~2:20–2:30 | Beat 4 — "stupid secretary" passage | `quote-card-2-hurgronje-secretary.html` |
| ~2:30–3:00 | Beat 5 — "he probably never knew" | `quote-card-4-spellberg.html` |
| ~4:30–4:45 | Beat 6 closing — "most extraordinary, wholly unexplained" | `quote-card-3-miller-384.html` |
| ~4:45–5:15 | Beat 6 — the 133-year silence | `timeline-133-years.html` |
| ~5:15–5:30 | Beat 6 — Crane's reading | `quote-card-5-crane-405.html` |

Treat these as canonical text overlays. The real document scans, portraits, and period maps from `B-ROLL-ASSET-MANIFEST.md` Section 1 cover the remaining B-roll.
