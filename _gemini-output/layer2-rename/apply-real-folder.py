"""Canonicalize files from library/real/ using the metadata in gemini metadata.txt and move them to the correct topic folder."""
import os, re, shutil, hashlib

REAL = r"D:\History vs Hype\library\real"
ROOT = r"D:\History vs Hype\library\by-topic"

# Mapping: real filename (lowercase, no ext) keyword -> (canonical_name, target_folder)
# Based on gemini metadata.txt
MAPPING = [
    {
        "real_match": "sapodilla",
        "canonical": "LetterSapodillaCayesBelizeDispute-Unknown-1913-Unknown.pdf",
        "folder": "territorial-disputes",
    },
    {
        "real_match": "morocco",
        "canonical": "ConcludingObsMoroccoCESCRReport-UNCESCR-2015-UN.pdf",
        "folder": "general-history",  # Western-Sahara cluster lives here
    },
    {
        "real_match": "bertot triana",
        "canonical": "ControversiaEsequiboLaudoArbitral1899-BertotTriana-2023-Redalyc.pdf",
        "folder": "territorial-disputes",
    },
    {
        "real_match": "ps4024",
        "canonical": "NurembergDocumentPS4024JodlsDiary-Jodl-1945-HarvardLaw.pdf",
        "folder": "general-history",
    },
    {
        "real_match": "friluftsliv",
        "canonical": "FriluftslivScandinavianPhilosophyOutdoorLife-Gelter-2000-Unknown.pdf",
        "folder": "general-history",
    },
    {
        "real_match": "infanticide",
        "canonical": "InfanticideSacrificesArchaicBabies-Claassen-2013-Routledge.pdf",
        "folder": "general-history",
    },
    {
        "real_match": "lessons from french",
        "canonical": "LessonsFrenchMilitaryInterventionsAfrica-Powell-2017-Routledge.pdf",
        "folder": "african-history",
    },
    {
        "real_match": "balakirsky",
        "canonical": "ProtocolsEldersZionJewishPress-BalakirskyKatz-2012-NYUPress.pdf",
        "folder": "middle-east-history",
    },
    {
        "real_match": "trials of warcriminals",
        "canonical": "TrialsWarCriminalsNurembergVol1-USGPO-1949-DaCapo.pdf",
        "folder": "general-history",
    },
    {
        "real_match": "draft status",
        "canonical": "LoiStatutJuifsDraft-Unknown-1940-Legifrance.pdf",
        "folder": "general-history",
    },
    {
        "real_match": "sykes picot",
        "canonical": "SykesPicotAgreementFODocuments-Unknown-1916-Unknown.pdf",
        "folder": "middle-east-history",
    },
    {
        "real_match": "operation situation",
        "canonical": "EinsatzgruppenOperationalSitRepUSSR17-RSHA-1941-JVL.pdf",
        "folder": "general-history",
    },
    {
        "real_match": "statu des juifs translated",
        "canonical": "LawStatusJewsEnglishTranslation-Unknown-1940-Unknown.pdf",
        "folder": "general-history",
    },
    {
        "real_match": "western sahara",
        "canonical": "QuestionWesternSaharaUNSpecialCommittee-UN-1975-UN.pdf",
        "folder": "general-history",
    },
]

# Build plan
plan = []
real_files = [f for f in os.listdir(REAL) if f.lower().endswith(".pdf")]
unmapped = []
for f in real_files:
    f_low = f.lower()
    matched = None
    for m in MAPPING:
        if m["real_match"].lower() in f_low:
            matched = m; break
    if not matched:
        unmapped.append(f); continue
    src = os.path.join(REAL, f)
    dst = os.path.join(ROOT, matched["folder"], matched["canonical"])
    plan.append({"src": src, "dst": dst, "real": f, "canonical": matched["canonical"], "folder": matched["folder"]})

print(f"Mapped: {len(plan)}")
print(f"Unmapped: {len(unmapped)}")
for u in unmapped: print(f"  UNMAPPED: {u}")
print()
print("=== Plan ===")
for op in plan:
    print(f"  [{op['folder']}] {op['canonical']}")
    print(f"    <- {op['real']}")

# Execute
print()
print("=== Executing ===")
moved = 0; collisions = 0; errors = []
for op in plan:
    if not os.path.exists(op["src"]):
        errors.append(f"MISSING SRC: {op['real']}")
        continue
    if os.path.exists(op["dst"]):
        # Hash compare
        try:
            with open(op["src"],"rb") as fh: h1 = hashlib.md5(fh.read()).hexdigest()
            with open(op["dst"],"rb") as fh: h2 = hashlib.md5(fh.read()).hexdigest()
            if h1 == h2:
                os.remove(op["src"])
                print(f"  DUP-DELETED (identical hash): {op['real']}")
                continue
            base, ext = os.path.splitext(op["canonical"])
            n = 2
            while os.path.exists(os.path.join(ROOT, op["folder"], f"{base}-v{n}{ext}")):
                n += 1
            new_dst = os.path.join(ROOT, op["folder"], f"{base}-v{n}{ext}")
            shutil.move(op["src"], new_dst)
            print(f"  MOVED-v{n}: {op['real']} -> {os.path.basename(new_dst)}")
            collisions += 1
            moved += 1
        except OSError as e:
            errors.append(str(e))
        continue
    try:
        shutil.move(op["src"], op["dst"])
        moved += 1
        print(f"  MOVED: {op['real'][:50]} -> [{op['folder']}] {op['canonical']}")
    except OSError as e:
        errors.append(str(e))

print(f"\nMoved: {moved}, Disambig collisions: {collisions}, Errors: {len(errors)}")
for e in errors: print(f"  {e}")
print(f"\nFiles remaining in library/real/: {len([f for f in os.listdir(REAL) if f.lower().endswith('.pdf')])}")
