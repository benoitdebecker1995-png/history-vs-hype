const fs = require('fs');
const path = require('path');
const sharp = require('C:/Users/benoi/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');

const project = 'G:/History vs Hype/video-projects/_IN_PRODUCTION/62-volhynia-massacre-untranslated-2026';
const outDir = path.join(project, 'assets/youtube-native');
fs.mkdirSync(outDir, { recursive: true });

const W = 1920;
const H = 1080;
const sources = {
  klymchak: path.join(project, '_research/genealogy/mcbride-p648.png'),
  order11: path.join(project, '_research/exhibits/klym-savur-order11/order11-avr7498-p1.png'),
  order11s2: path.join(project, '_research/exhibits/klym-savur-order11/verify-s2-liquidate.png'),
  kolodzinskyi: path.join(project, '_research/exhibits/kolodzinskyi-doctrine-um20-p266.png'),
  stelmashchuk: path.join(project, '_research/genealogy/katchanovski-photo1-stelmashchuk-protocol-1963.jpeg'),
  litopys: path.join(project, '_research/genealogy/litopys-ns9-p442-massacre-confession.png'),
  map: path.join(project, 'assets/volhynia-1939-base.jpg'),
};

function esc(s) {
  return s.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;');
}

function bugSvg(kicker, source, colour = '#D3A52F') {
  return Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}">
    <defs>
      <linearGradient id="bottom" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.78"/></linearGradient>
    </defs>
    <rect x="0" y="760" width="1920" height="320" fill="url(#bottom)"/>
    <rect x="54" y="914" width="8" height="108" fill="${colour}"/>
    <text x="88" y="952" fill="${colour}" font-family="Arial" font-weight="700" font-size="25" letter-spacing="4">${esc(kicker)}</text>
    <text x="88" y="1002" fill="#FFF" font-family="Arial" font-size="29">${esc(source)}</text>
  </svg>`);
}

async function wide(file, source, kicker, sourceText, colour) {
  const bg = await sharp(source).resize(W, H, { fit: 'cover' }).blur(28).modulate({ brightness: 0.42, saturation: 0.35 }).png().toBuffer();
  const page = await sharp(source).resize({ width: 1500, height: 970, fit: 'inside', withoutEnlargement: false }).png().toBuffer();
  const meta = await sharp(page).metadata();
  const left = Math.round((W - meta.width) / 2);
  const top = Math.round((H - meta.height) / 2) - 18;
  const shadow = Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}"><rect x="${left + 18}" y="${top + 22}" width="${meta.width}" height="${meta.height}" fill="#000" opacity="0.55"/></svg>`);
  await sharp(bg)
    .composite([{ input: shadow }, { input: page, left, top }, { input: bugSvg(kicker, sourceText, colour) }])
    .png({ compressionLevel: 9 })
    .toFile(path.join(outDir, file));
}

function detailOverlay(kicker, sourceText, highlights, captions = [], colour = '#D3A52F') {
  const boxes = highlights.map(h => `<rect x="${h.x}" y="${h.y}" width="${h.w}" height="${h.h}" rx="4" fill="${colour}" fill-opacity="0.18" stroke="${colour}" stroke-width="5"/>`).join('');
  const captionSvg = captions.map((line, i) => `<text x="88" y="${827 + i * 58}" fill="#FFF" font-family="Arial" font-size="${i === 0 ? 44 : 34}" font-weight="${i === 0 ? 700 : 400}">${esc(line)}</text>`).join('');
  return Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}">
    <defs><linearGradient id="v" x1="0" y1="0" x2="0" y2="1"><stop offset="0.58" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.88"/></linearGradient></defs>
    ${boxes}
    <rect x="0" y="560" width="1920" height="520" fill="url(#v)"/>
    ${captionSvg}
    <rect x="54" y="944" width="8" height="82" fill="${colour}"/>
    <text x="88" y="973" fill="${colour}" font-family="Arial" font-weight="700" font-size="22" letter-spacing="4">${esc(kicker)}</text>
    <text x="88" y="1014" fill="#DDD" font-family="Arial" font-size="25">${esc(sourceText)}</text>
  </svg>`);
}

async function detail(file, source, crop, kicker, sourceText, highlights, captions, colour) {
  const srcMeta = await sharp(source).metadata();
  const safe = {
    left: Math.max(0, Math.min(crop.left, srcMeta.width - 2)),
    top: Math.max(0, Math.min(crop.top, srcMeta.height - 2)),
    width: Math.min(crop.width, srcMeta.width - crop.left),
    height: Math.min(crop.height, srcMeta.height - crop.top),
  };
  const base = await sharp(source).extract(safe).resize(W, H, { fit: 'cover', position: 'centre' }).sharpen().png().toBuffer();
  await sharp(base)
    .composite([{ input: detailOverlay(kicker, sourceText, highlights, captions, colour) }])
    .png({ compressionLevel: 9 })
    .toFile(path.join(outDir, file));
}

async function stripDetail(file, source, kicker, sourceText, captions, colour) {
  const bg = await sharp(source).resize(W, H, { fit: 'cover' }).blur(25).modulate({ brightness: 0.3, saturation: 0.25 }).png().toBuffer();
  const strip = await sharp(source).resize({ width: 1840, height: 420, fit: 'inside' }).sharpen().png().toBuffer();
  const meta = await sharp(strip).metadata();
  const top = 238;
  const captionSvg = captions.map((line, i) => `<text x="96" y="${730 + i * 67}" fill="#FFF" font-family="Arial" font-size="${i === 0 ? 47 : 36}" font-weight="${i === 0 ? 700 : 400}">${esc(line)}</text>`).join('');
  const svg = Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}">
    <rect x="40" y="${top - 22}" width="1840" height="${meta.height + 44}" fill="#000" opacity="0.55"/>
    <line x1="78" y1="${top + meta.height + 34}" x2="1842" y2="${top + meta.height + 34}" stroke="${colour}" stroke-width="6"/>
    ${captionSvg}
    <rect x="54" y="944" width="8" height="82" fill="${colour}"/>
    <text x="88" y="973" fill="${colour}" font-family="Arial" font-weight="700" font-size="22" letter-spacing="4">${esc(kicker)}</text>
    <text x="88" y="1014" fill="#DDD" font-family="Arial" font-size="25">${esc(sourceText)}</text>
  </svg>`);
  await sharp(bg).composite([{ input: strip, left: 40, top }, { input: svg }]).png({ compressionLevel: 9 }).toFile(path.join(outDir, file));
}

async function mapFrame(file, poryck = false) {
  const base = await sharp(sources.map).resize(W, H, { fit: 'cover', position: 'centre' }).modulate({ brightness: 0.72, saturation: 0.72 }).png().toBuffer();
  const marker = poryck ? `<circle cx="595" cy="606" r="17" fill="#D52D2D" stroke="#FFF" stroke-width="5"/><circle cx="595" cy="606" r="37" fill="none" stroke="#D52D2D" stroke-width="4" opacity="0.8"/><line x1="620" y1="586" x2="790" y2="486" stroke="#D52D2D" stroke-width="5"/><text x="810" y="478" fill="#FFF" font-family="Arial" font-size="50" font-weight="700">PORYCK</text><text x="810" y="520" fill="#DDD" font-family="Arial" font-size="27">today Pavlivka · 50°41′N, 24°30′E</text>` : '';
  const label = poryck ? 'ONE LOCATION — NOT A COMPLETE ATTACK MAP' : 'VOLHYNIA · SECOND POLISH REPUBLIC · 1939';
  const svg = Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}">
    <defs><radialGradient id="shade"><stop offset="0.48" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.62"/></radialGradient></defs>
    <rect width="1920" height="1080" fill="url(#shade)"/>
    ${marker}
    <rect x="54" y="947" width="8" height="66" fill="#D3A52F"/>
    <text x="88" y="994" fill="#FFF" font-family="Arial" font-size="32" font-weight="700" letter-spacing="2">${label}</text>
    <text x="1830" y="1012" text-anchor="end" fill="#DDD" font-family="Arial" font-size="22">Poeticbent · 2009 · public domain</text>
  </svg>`);
  await sharp(base).composite([{ input: svg }]).png({ compressionLevel: 9 }).toFile(path.join(outDir, file));
}

async function transparentOverlay(file, label, sublabel, colour) {
  const svg = Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}">
    <rect x="46" y="48" width="${Math.min(1040, 90 + label.length * 25)}" height="98" fill="#050505" fill-opacity="0.78"/>
    <rect x="46" y="48" width="9" height="98" fill="${colour}"/>
    <text x="82" y="91" fill="${colour}" font-family="Arial" font-size="23" font-weight="700" letter-spacing="4">${esc(label)}</text>
    <text x="82" y="126" fill="#FFF" font-family="Arial" font-size="23">${esc(sublabel)}</text>
  </svg>`);
  await sharp({ create: { width: W, height: H, channels: 4, background: { r: 0, g: 0, b: 0, alpha: 0 } } }).composite([{ input: svg }]).png().toFile(path.join(outDir, file));
}

async function main() {
  await wide('01-klymchak-page-wide.png', sources.klymchak, 'PUBLISHED REPRODUCTION', 'Jared McBride · Slavic Review 75:3 (2016) · p. 648', '#D3A52F');
  await detail('02-klymchak-quote-detail.png', sources.klymchak, { left: 145, top: 125, width: 980, height: 550 }, 'SCHOLARLY REPRODUCTION — ORIGINAL FOLIO NOT IN HAND', 'McBride (2016), p. 648 · report dated 30 August 1943', [{ x: 92, y: 260, w: 1735, h: 210 }], [], '#D3A52F');

  await wide('03-order11-page-wide.png', sources.order11, 'PRIMARY DOCUMENT REPRODUCTION', 'Order No. 11 · 4 September 1943 · AVR 7498 / HDA SBU fol. 200', '#5CA8E8');
  await stripDetail('04-order11-language-detail.png', sources.order11s2, 'GRAMMATICAL OBJECT MUST REMAIN VISIBLE', 'Order No. 11 §2 · AVR 7498 · CC BY-ND 3.0', ['“If possible—liquidate him.”', '“This applies to the Germans as well as to the Bolshevik partisans.”'], '#5CA8E8');
  await detail('05-order11-signature-detail.png', sources.order11, { left: 100, top: 1760, width: 1740, height: 520 }, 'SIGNED RECORD', 'Klym Savur and Col. Honcharenko · 4 September 1943', [{ x: 1320, y: 720, w: 560, h: 230 }], [], '#5CA8E8');

  await wide('06-kolodzinskyi-page-wide.png', sources.kolodzinskyi, 'PREWAR DOCTRINE', 'Kolodzinskyi manuscript reproduced in Ukraina Moderna 20 (2013) · p. 266', '#D3A52F');
  await detail('07-kolodzinskyi-quote-detail.png', sources.kolodzinskyi, { left: 160, top: 1010, width: 1120, height: 630 }, 'DOCTRINE — NOT A 1943 OPERATIONAL ORDER', 'Ukraina Moderna 20 (2013), p. 266 · English: Himka (2021), p. 154', [{ x: 65, y: 170, w: 1785, h: 650 }], [], '#D3A52F');

  await wide('08-stelmashchuk-page-wide.png', sources.stelmashchuk, 'ARCHIVAL COPY', 'HDA SBU Sprava 372 vol. 89 ark. 33 · reproduced by Katchanovski (2020)', '#D52D2D');
  await detail('09-stelmashchuk-directive-detail.png', sources.stelmashchuk, { left: 135, top: 230, width: 920, height: 518 }, 'TESTIMONY UNDER SOVIET INTERROGATION', '1963 archival copy · copy status, duress and authenticity remain material', [{ x: 78, y: 130, w: 1765, h: 390 }], [], '#D52D2D');

  await wide('10-litopys-page-wide.png', sources.litopys, 'PUBLISHED INTERROGATION RECORD', 'Litopys UPA · New Series 9 · p. 442', '#D52D2D');
  await detail('11-litopys-oleh-detail.png', sources.litopys, { left: 70, top: 350, width: 900, height: 506 }, 'A DIFFERENT INTERROGATION RECORD', 'Litopys UPA · New Series 9 · p. 442 · reliability/duress caution', [{ x: 72, y: 215, w: 1775, h: 325 }, { x: 72, y: 585, w: 1775, h: 245 }], [], '#D52D2D');

  await mapFrame('12-volhynia-map-fullscreen.png', false);
  await mapFrame('13-poryck-map-fullscreen.png', true);

  await transparentOverlay('overlay-primary-document.png', 'PRIMARY DOCUMENT', 'Archive reference stays visible', '#5CA8E8');
  await transparentOverlay('overlay-reproduced-source.png', 'REPRODUCED IN SCHOLARSHIP', 'Original archival folio not in hand', '#D3A52F');
  await transparentOverlay('overlay-interrogation.png', 'UNDER SOVIET INTERROGATION', 'Testimony · duress and reliability caution', '#D52D2D');
  await transparentOverlay('overlay-original-unavailable.png', 'ORIGINAL FILE UNAVAILABLE', 'Do not reconstruct or imply that it was located', '#D52D2D');

  process.stdout.write('Rendered YouTube-native source frames and transparent overlays.\n');
}

main().catch(error => {
  process.stderr.write(`${error.stack || error}\n`);
  process.exitCode = 1;
});
