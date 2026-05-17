"""Build Gemini publisher-lookup batch: author+year known, publisher unknown."""
import os, re, json

ROOT = r"D:\History vs Hype\library\by-topic"
targets = []
for folder in sorted(os.listdir(ROOT)):
    p = os.path.join(ROOT, folder)
    if not os.path.isdir(p): continue
    for f in os.listdir(p):
        if not os.path.isfile(os.path.join(p, f)): continue
        m = re.match(r'^(.+?)-(.+?)-(\d{4})-(.+?)(?:-v\d+)?\.[a-z0-9]+$', f)
        if not m: continue
        t, a, y, pub = m.groups()
        if a.lower() == 'unknown': continue
        if y == '0000': continue
        if pub.lower() not in ('unknown','zlib','libgen','annaarchive','z-library'): continue
        targets.append({"folder":folder,"f":f,"t":t,"a":a,"y":y})

print(f"Targets: {len(targets)}")

prompt = """You will receive a numbered list of academic books with KNOWN author, year, and title slug. Your job: identify the PUBLISHER using your training knowledge.

OUTPUT FORMAT: JSON array, NO markdown fences, JSON only.
[{"i":N,"p":"PublisherAbbrev"}]

PUBLISHER ABBREVIATIONS (use these — match closest):
CambridgeUP, OxfordUP, YaleUP, PrincetonUP, ColumbiaUP, IndianaUP, EdinburghUP, NYUPress, UCPress (= UC Press), UCLAUP, UNCPress, JohnsHopkinsUP, HooverPress, PlutoPress, Routledge, Palgrave, PalgraveMacmillan, Bloomsbury, ITauris (= I.B.Tauris), HurstCo (= Hurst), ZedBooks, VersoBooks, BasicBooks, RandomHouse, Penguin, Brill, Springer, DaCapo, FreePress, Granta, WeidenfeldNicolson, CornellUP, StanfordUP, HarvardUP, LiverpoolUP, MacmillanUK, NortonCo, ChicagoUP, MITPress, WileyBlackwell, SAGEPub, TaylorFrancis, Greenwood, Lexington, Brookings, RFFPress, AsiaSocietyPress, CUNYPress, OneWorldPubs, NewPress, ZED, OUPIndia

If you don't know with reasonable confidence, output "Unknown".

ENTRIES (i. title | author | year):
"""
for idx, t in enumerate(targets, 1):
    prompt += f"\n{idx}. {t['t']} | {t['a']} | {t['y']}"

with open(r"D:\History vs Hype\_gemini-output\layer2-rename\publisher-lookup-input.txt", "w", encoding="utf-8") as f:
    f.write(prompt)
idxmap = {idx: t for idx, t in enumerate(targets, 1)}
with open(r"D:\History vs Hype\_gemini-output\layer2-rename\publisher-lookup-idxmap.json", "w", encoding="utf-8") as f:
    json.dump(idxmap, f, indent=2, ensure_ascii=False)
print(f"Wrote publisher-lookup-input.txt")
