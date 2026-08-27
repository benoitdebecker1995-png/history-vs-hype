const path = require('path');
const sharp = require('C:/Users/benoi/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');

const project = 'G:/History vs Hype/video-projects/_IN_PRODUCTION/62-volhynia-massacre-untranslated-2026';
const outDir = path.join(project, 'assets');

function svgBuffer(width, height, content, background = 'none') {
  return Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}"><rect width="${width}" height="${height}" fill="${background}"/>${content}</svg>`);
}

async function evidenceCard(filename, sourcePath, panelSvg) {
  const document = await sharp(sourcePath)
    .resize(2220, 1920, { fit: 'contain', background: '#E8DFC9' })
    .png()
    .toBuffer();
  const panel = svgBuffer(1200, 1920, panelSvg, '#14243A');
  await sharp({ create: { width: 3840, height: 2160, channels: 4, background: '#0A1628' } })
    .composite([
      { input: document, left: 120, top: 120 },
      { input: panel, left: 2520, top: 120 },
    ])
    .png({ compressionLevel: 9 })
    .toFile(path.join(outDir, filename));
}

async function thumbnail() {
  const scanPath = path.join(project, '_research/exhibits/klym-savur-order11/order11-avr7498-p1.png');
  const document = await sharp(scanPath)
    .resize(1040, 1300, { fit: 'cover', position: 'centre' })
    .rotate(5, { background: { r: 10, g: 22, b: 40, alpha: 0 } })
    .png()
    .toBuffer();
  const base = svgBuffer(2560, 1440, `
    <circle cx="560" cy="650" r="1040" fill="#203854"/>
    <text x="108" y="500" fill="#FFFFFF" font-family="Impact, Arial Black, sans-serif" font-size="210">READ THE</text>
    <text x="108" y="850" fill="#D2A23A" font-family="Impact, Arial Black, sans-serif" font-size="280">ORDER</text>
    <rect x="110" y="936" width="1000" height="20" fill="#C84A46"/>
    <text x="120" y="1060" fill="#D7DFE8" font-family="Arial, sans-serif" font-size="60" letter-spacing="10">WHAT DOES IT ACTUALLY SAY?</text>
    <rect x="108" y="1200" width="1040" height="116" rx="12" fill="#14243A" stroke="#536174" stroke-width="5"/>
    <text x="628" y="1276" text-anchor="middle" fill="#FFFFFF" font-family="Arial, sans-serif" font-size="52" letter-spacing="8">UNTRANSLATED EVIDENCE</text>
  `, '#0A1628');
  const overlay = svgBuffer(2560, 1440, `
    <rect x="1450" y="630" width="1050" height="145" transform="rotate(5 1975 702)" fill="#C84A46"/>
  `);
  await sharp(base)
    .composite([
      { input: document, left: 1440, top: 40 },
      { input: overlay, left: 0, top: 0 },
    ])
    .png({ compressionLevel: 9 })
    .toFile(path.join(outDir, '12-thumbnail-dossier.png'));
}

async function main() {
  await thumbnail();
  await evidenceCard('14-klymchak-report-card.png', path.join(project, '_research/genealogy/mcbride-p648.png'), `
    <rect x="0" y="0" width="14" height="1920" fill="#D2A23A"/>
    <text x="90" y="120" fill="#D2A23A" font-family="Arial" font-size="44" letter-spacing="6">EXHIBIT 1</text>
    <text x="90" y="220" fill="#FFFFFF" font-family="Arial" font-size="70" font-weight="700">UPA AFTER-ACTION</text>
    <text x="90" y="302" fill="#FFFFFF" font-family="Arial" font-size="70" font-weight="700">REPORT</text>
    <text x="90" y="420" fill="#9EB0C5" font-family="Arial" font-size="34" letter-spacing="4">30 AUGUST 1943</text>
    <line x1="90" y1="475" x2="1110" y2="475" stroke="#536174" stroke-width="4"/>
    <text x="90" y="580" fill="#E8DFC9" font-family="Georgia" font-size="52">“I liquidated all Poles</text>
    <text x="90" y="648" fill="#E8DFC9" font-family="Georgia" font-size="52">from young to old…”</text>
    <text x="90" y="760" fill="#D2A23A" font-family="Arial" font-size="34" letter-spacing="4">STATUS</text>
    <text x="90" y="824" fill="#FFFFFF" font-family="Arial" font-size="44" font-weight="700">REPRODUCED PRIMARY</text>
    <text x="90" y="918" fill="#C9D2DC" font-family="Arial" font-size="34">The underlying HDA SBU folio</text>
    <text x="90" y="964" fill="#C9D2DC" font-family="Arial" font-size="34">was not available to McBride.</text>
    <text x="90" y="1056" fill="#D2A23A" font-family="Arial" font-size="34" letter-spacing="4">DO NOT LABEL</text>
    <text x="90" y="1120" fill="#FFFFFF" font-family="Arial" font-size="40">Not a signed original scan.</text>
    <text x="90" y="1704" fill="#9EB0C5" font-family="Arial" font-size="29">Alexander J. McBride, Slavic Review 75:3</text>
    <text x="90" y="1750" fill="#9EB0C5" font-family="Arial" font-size="29">(2016), p. 648 · publisher copyright</text>
  `);
  await evidenceCard('15-order11-card.png', path.join(project, '_research/exhibits/klym-savur-order11/order11-avr7498-p1.png'), `
    <rect x="0" y="0" width="14" height="1920" fill="#D2A23A"/>
    <text x="90" y="120" fill="#D2A23A" font-family="Arial" font-size="44" letter-spacing="6">SIGNED RECORD</text>
    <text x="90" y="220" fill="#FFFFFF" font-family="Arial" font-size="78" font-weight="700">ORDER NO. 11</text>
    <text x="90" y="320" fill="#9EB0C5" font-family="Arial" font-size="34" letter-spacing="4">4 SEPTEMBER 1943</text>
    <line x1="90" y1="375" x2="1110" y2="375" stroke="#536174" stroke-width="4"/>
    <text x="90" y="478" fill="#D2A23A" font-family="Arial" font-size="34" letter-spacing="4">WHAT IT IS</text>
    <text x="90" y="548" fill="#E8DFC9" font-family="Arial" font-size="42">An anti-German village-defence</text>
    <text x="90" y="602" fill="#E8DFC9" font-family="Arial" font-size="42">and logistics order.</text>
    <text x="90" y="728" fill="#E7A4A2" font-family="Arial" font-size="34" letter-spacing="4">CROP LANDMINE</text>
    <text x="90" y="798" fill="#FFFFFF" font-family="Arial" font-size="41" font-weight="700">“Liquidate” applies to Germans</text>
    <text x="90" y="852" fill="#FFFFFF" font-family="Arial" font-size="41" font-weight="700">and Bolshevik partisans.</text>
    <text x="90" y="930" fill="#C9D2DC" font-family="Arial" font-size="34">Keep the grammatical object visible.</text>
    <rect x="90" y="1040" width="1010" height="128" rx="10" fill="#281C29" stroke="#C84A46" stroke-width="4"/>
    <text x="595" y="1093" text-anchor="middle" fill="#E7A4A2" font-family="Arial" font-size="29" letter-spacing="4">DOES NOT ORDER</text>
    <text x="595" y="1138" text-anchor="middle" fill="#FFFFFF" font-family="Arial" font-size="36">the killing of Polish civilians</text>
    <text x="90" y="1704" fill="#9EB0C5" font-family="Arial" font-size="28">AVR 7498 · HDA SBU f.13 spr.376</text>
    <text x="90" y="1750" fill="#9EB0C5" font-family="Arial" font-size="28">vol.60 fol.200 · CC BY-ND 3.0</text>
  `);
  await evidenceCard('16-kolodzinskyi-card.png', path.join(project, '_research/exhibits/kolodzinskyi-doctrine-um20-p266.png'), `
    <rect x="0" y="0" width="14" height="1920" fill="#D2A23A"/>
    <text x="90" y="120" fill="#D2A23A" font-family="Arial" font-size="44" letter-spacing="6">PREWAR DOCTRINE</text>
    <text x="90" y="220" fill="#FFFFFF" font-family="Arial" font-size="68" font-weight="700">KOLODZINSKYI</text>
    <text x="90" y="304" fill="#FFFFFF" font-family="Arial" font-size="50">“the Polish element”</text>
    <line x1="90" y1="370" x2="1110" y2="370" stroke="#536174" stroke-width="4"/>
    <text x="90" y="468" fill="#9EB0C5" font-family="Arial" font-size="31" letter-spacing="4">PUBLISHED ENGLISH — HIMKA</text>
    <text x="90" y="548" fill="#E8DFC9" font-family="Georgia" font-size="42">“The Polish element that actively</text>
    <text x="90" y="604" fill="#E8DFC9" font-family="Georgia" font-size="42">puts up resistance must fall in the</text>
    <text x="90" y="660" fill="#E8DFC9" font-family="Georgia" font-size="42">struggle, and the rest must be</text>
    <text x="90" y="716" fill="#E8DFC9" font-family="Georgia" font-size="42">terrorized and forced to flee…”</text>
    <rect x="90" y="826" width="1010" height="146" rx="10" fill="#263A55"/>
    <text x="595" y="884" text-anchor="middle" fill="#D2A23A" font-family="Arial" font-size="29" letter-spacing="4">CONTEXT GUARD</text>
    <text x="595" y="934" text-anchor="middle" fill="#FFFFFF" font-family="Arial" font-size="38">Doctrine—not a 1943 operational order</text>
    <text x="90" y="1055" fill="#C9D2DC" font-family="Arial" font-size="33">Preserve “Polish element,” not</text>
    <text x="90" y="1101" fill="#C9D2DC" font-family="Arial" font-size="33">“population,” and the two-part program.</text>
    <text x="90" y="1704" fill="#9EB0C5" font-family="Arial" font-size="28">Manuscript reproduced in Ukraina Moderna</text>
    <text x="90" y="1750" fill="#9EB0C5" font-family="Arial" font-size="28">20 (2013), p. 266 · copyrighted reproduction</text>
  `);
  await evidenceCard('17-stelmashchuk-card.png', path.join(project, '_research/genealogy/katchanovski-photo1-stelmashchuk-protocol-1963.jpeg'), `
    <rect x="0" y="0" width="14" height="1920" fill="#C84A46"/>
    <text x="90" y="120" fill="#E7A4A2" font-family="Arial" font-size="40" letter-spacing="5">TESTIMONY UNDER SOVIET INTERROGATION</text>
    <text x="90" y="224" fill="#FFFFFF" font-family="Arial" font-size="62" font-weight="700">STELMASHCHUK</text>
    <text x="90" y="304" fill="#FFFFFF" font-family="Arial" font-size="45">1963 archival copy</text>
    <line x1="90" y1="370" x2="1110" y2="370" stroke="#536174" stroke-width="4"/>
    <text x="90" y="468" fill="#D2A23A" font-family="Arial" font-size="32" letter-spacing="4">WHAT THIS COPY SAYS</text>
    <text x="90" y="538" fill="#FFFFFF" font-family="Arial" font-size="40" font-weight="700">Stelmashchuk stated that “Klym Savur”</text>
    <text x="90" y="590" fill="#FFFFFF" font-family="Arial" font-size="40" font-weight="700">gave him an oral, secret directive.</text>
    <text x="90" y="718" fill="#D2A23A" font-family="Arial" font-size="32" letter-spacing="4">NUMBER LOCK</text>
    <text x="90" y="788" fill="#E8DFC9" font-family="Arial" font-size="39">“Over 15,000” is this testimony’s</text>
    <text x="90" y="840" fill="#E8DFC9" font-family="Arial" font-size="39">claimed operational figure—</text>
    <text x="90" y="892" fill="#E8DFC9" font-family="Arial" font-size="39">not the total Volhynia estimate.</text>
    <rect x="90" y="1010" width="1010" height="150" rx="10" fill="#281C29" stroke="#C84A46" stroke-width="4"/>
    <text x="595" y="1072" text-anchor="middle" fill="#E7A4A2" font-family="Arial" font-size="29" letter-spacing="4">EVIDENTIARY LIMIT</text>
    <text x="595" y="1112" text-anchor="middle" fill="#FFFFFF" font-family="Arial" font-size="35">Testimony is not the missing written order.</text>
    <text x="595" y="1150" text-anchor="middle" fill="#FFFFFF" font-family="Arial" font-size="31">Copy status, duress and authenticity remain material.</text>
    <text x="90" y="1704" fill="#9EB0C5" font-family="Arial" font-size="27">HDA SBU Sprava 372 vol.89 ark.33</text>
    <text x="90" y="1750" fill="#9EB0C5" font-family="Arial" font-size="27">reproduced by Ivan Katchanovski (2020)</text>
  `);
  await evidenceCard('18-litopys-p442-card.png', path.join(project, '_research/genealogy/litopys-ns9-p442-massacre-confession.png'), `
    <rect x="0" y="0" width="14" height="1920" fill="#C84A46"/>
    <text x="90" y="120" fill="#E7A4A2" font-family="Arial" font-size="39" letter-spacing="5">A DIFFERENT INTERROGATION RECORD</text>
    <text x="90" y="224" fill="#FFFFFF" font-family="Arial" font-size="63" font-weight="700">LITOPYS UPA</text>
    <text x="90" y="304" fill="#FFFFFF" font-family="Arial" font-size="45">New Series 9 · p. 442</text>
    <line x1="90" y1="370" x2="1110" y2="370" stroke="#536174" stroke-width="4"/>
    <text x="90" y="468" fill="#D2A23A" font-family="Arial" font-size="32" letter-spacing="4">ATTRIBUTION LOCK</text>
    <text x="90" y="538" fill="#FFFFFF" font-family="Arial" font-size="40" font-weight="700">This text attributes the alleged</text>
    <text x="90" y="590" fill="#FFFFFF" font-family="Arial" font-size="40" font-weight="700">operation to “Oleh”—not Klym Savur.</text>
    <text x="90" y="718" fill="#D2A23A" font-family="Arial" font-size="32" letter-spacing="4">NUMBER LOCK</text>
    <text x="90" y="788" fill="#E8DFC9" font-family="Arial" font-size="39">“Over 15,000” is claimed for the</text>
    <text x="90" y="840" fill="#E8DFC9" font-family="Arial" font-size="39">29–30 August 1943 operation—</text>
    <text x="90" y="892" fill="#E8DFC9" font-family="Arial" font-size="39">not the total Volhynia estimate.</text>
    <rect x="90" y="1010" width="1010" height="176" rx="10" fill="#281C29" stroke="#C84A46" stroke-width="4"/>
    <text x="595" y="1068" text-anchor="middle" fill="#E7A4A2" font-family="Arial" font-size="29" letter-spacing="4">EVIDENTIARY LIMIT</text>
    <text x="595" y="1111" text-anchor="middle" fill="#FFFFFF" font-family="Arial" font-size="32">Soviet-interrogation testimony:</text>
    <text x="595" y="1152" text-anchor="middle" fill="#FFFFFF" font-family="Arial" font-size="32">duress and reliability must stay visible.</text>
    <text x="90" y="1704" fill="#9EB0C5" font-family="Arial" font-size="27">Litopys UPA, New Series 9, p. 442</text>
    <text x="90" y="1750" fill="#9EB0C5" font-family="Arial" font-size="27">published interrogation record · copyrighted scan</text>
  `);
  process.stdout.write('Rendered thumbnail and five evidence cards.\n');
}

main().catch((error) => {
  process.stderr.write(`${error.stack || error}\n`);
  process.exitCode = 1;
});
