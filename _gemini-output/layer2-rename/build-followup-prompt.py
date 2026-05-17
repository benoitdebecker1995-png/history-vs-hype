"""Build a tighter follow-up prompt for files Gemini didn't resolve.
Includes original filename + folder context. Pre-flags likely off-topic."""
import re, os, json

MD_PATH = r"D:\History vs Hype\_gemini-output\layer2-rename\WEB-LOOKUP-PROMPT.md"
ROOT = r"D:\History vs Hype\library\by-topic"

with open(MD_PATH, encoding="utf-8") as f:
    md = f.read()

# Re-derive idx -> (folder, fname) from reference section
ref_pattern = re.compile(r'^\s*(\d+)\.\s+`library/by-topic/([^/]+)/(.+?)`\s*$', re.MULTILINE)
ref_map = {}
for m in ref_pattern.finditer(md):
    ref_map[int(m.group(1))] = (m.group(2), m.group(3))

# Indices that Gemini resolved in the table
resolved_indices = set()
for m in re.finditer(r'^\|\s*(\d+)\s*\|', md, re.MULTILINE):
    try:
        resolved_indices.add(int(m.group(1)))
    except: pass
# Exclude header markers (which aren't numeric)

# Also parse prompt section to get current canonical metadata for each idx
prompt_entries = {}
prompt_pattern = re.compile(r'^\s*(\d+)\.\s+\[([^\]]+)\]\s+(\S+)\s+\|\s+a=(\S+)\s+\|\s+y=(\d{4})\s+\|\s+p=(.+?)\s*$', re.MULTILINE)
for m in prompt_pattern.finditer(md):
    idx = int(m.group(1))
    prompt_entries[idx] = {
        "folder": m.group(2), "t": m.group(3),
        "a": m.group(4), "y": m.group(5), "p": m.group(6).strip()
    }

print(f"Reference map: {len(ref_map)}")
print(f"Resolved by Gemini: {len(resolved_indices)}")
unresolved_idx = sorted(set(ref_map.keys()) - resolved_indices)
print(f"Still unresolved: {len(unresolved_idx)}")

# Pre-flag off-topic patterns
OFFTOPIC_PATTERNS = [
    r'\bD&D\b', r'DungeonsDragons', r'GrimHollow', r'Grimhollow', r'GrimhollowCampaign',
    r'Drakkenheim', r'Etharis', r'RappanAthuk', r'HouseRulesRappan', r'Frostmaiden',
    r'BolComFactuur', r'Calendar', r'ZichtrekeningInvest', r'EuropassDocument',
    r'EnglishCommonEntrance', r'EuropeanYouthProposal', r'TraineeshipsJobs',
    r'GuidebookTEC', r'KSATPPAT', r'EuropeanSolidarityCorps', r'GeneralIntroductionESC',
    r'ExploreSolidarityProjects', r'KreativUngCulturalProject', r'ProgramOutlineMay28',
    r'Ardennendagtocht', r'AlsJeVoorHetEerstDeelneemt', r'KlaprozenlaanDocument',
    r'TransaccionAutorizacion', r'TransactionDocument', r'Toelatingsvoorwaarden',
    r'DeclarationAccessUniversityBachelorProgramme', r'WordSyllabus', r'WordSourDocument',
    r'KMBTC364', r'EuropassDocument', r'Hageprot', r'BlandijnDocument', r'JODEFDocument',
    r'JORFDocument', r'OrdonnanceAllemande',
    # User's own working docs from earlier sweeps
    r'GeminiVidResearch', r'ExtraResearch', r'ResearchPrompt', r'^Research-',
]
OFFTOPIC_RE = re.compile('|'.join(OFFTOPIC_PATTERNS), re.IGNORECASE)

off_topic = []
academic_unresolved = []
for idx in unresolved_idx:
    folder, fname = ref_map[idx]
    pe = prompt_entries.get(idx, {})
    src = os.path.join(ROOT, folder, fname)
    if not os.path.exists(src):
        continue  # already renamed in earlier passes
    slug_or_name = pe.get("t","") + "|" + fname
    if OFFTOPIC_RE.search(slug_or_name):
        off_topic.append((idx, folder, fname, pe))
    else:
        academic_unresolved.append((idx, folder, fname, pe))

print(f"Pre-flagged off-topic: {len(off_topic)}")
print(f"Academic unresolved:   {len(academic_unresolved)}")

# Build follow-up prompt for academic entries
lines = []
lines.append("# Web Lookup Prompt — Round 2 (harder cases)")
lines.append("")
lines.append("**Paste the prompt below into Gemini / ChatGPT / Perplexity.**")
lines.append("")
lines.append("```")
lines.append("Round 2 lookup. These academic library files weren't resolved in round 1.")
lines.append("Each entry shows: (1) current canonical filename, (2) folder topic, (3) extracted metadata, (4) original filename.")
lines.append("")
lines.append("Use the original filename as the strongest hint — it often contains author, year, DOI, or publisher fragments that were missed during slug extraction.")
lines.append("")
lines.append("OUTPUT FORMAT: markdown table:")
lines.append("| file_index | title (verified) | author_surname | year | publisher_abbrev | source_url |")
lines.append("")
lines.append("Publisher abbreviations: CambridgeUP, OxfordUP, YaleUP, PrincetonUP, ColumbiaUP, IndianaUP,")
lines.append("EdinburghUP, NYUPress, UCPress, JohnsHopkinsUP, HooverPress, PlutoPress, Routledge, Palgrave,")
lines.append("Bloomsbury, ITauris, HurstCo, ZedBooks, VersoBooks, BasicBooks, RandomHouse, Penguin, Brill,")
lines.append("Springer, DaCapo, FreePress, Granta, WeidenfeldNicolson, CornellUP, StanfordUP, HarvardUP,")
lines.append("LiverpoolUP, MacmillanUK, NortonCo, ChicagoUP, MITPress, SyracuseUP, DukeUP, UCLAUP, UNCPress,")
lines.append("WileyBlackwell, SAGEPub, TaylorFrancis, OneWorldPubs, NewPress, ZED, OUPIndia, McGrawHill.")
lines.append("")
lines.append("If still unresolved, output 'UNRESOLVED' in that row's title cell.")
lines.append("If it appears to be a personal document, government form, course material, or non-academic content, output 'OFF-TOPIC' in title cell.")
lines.append("")
lines.append("---")
lines.append("")

for idx, folder, fname, pe in academic_unresolved:
    t = pe.get("t","?")
    a = pe.get("a","?"); y = pe.get("y","?"); p = pe.get("p","?")
    lines.append(f"### {idx}")
    lines.append(f"- canonical: `{fname}`")
    lines.append(f"- folder: {folder}")
    lines.append(f"- known: title-slug=`{t}` a=`{a}` y=`{y}` p=`{p}`")
    lines.append("")

lines.append("```")
lines.append("")
lines.append("---")
lines.append("")
lines.append(f"## Stats")
lines.append(f"- Total in round 2: **{len(academic_unresolved)}** academic entries")
lines.append(f"- Skipped as likely off-topic (separate stash decision): {len(off_topic)}")
lines.append("")
lines.append("## Pre-flagged as likely off-topic (NOT in prompt above)")
lines.append("")
lines.append("These look like personal docs / D&D / EU youth program / govt forms. Review whether to stash them:")
lines.append("")
for idx, folder, fname, pe in off_topic:
    lines.append(f"- `[{folder}] {fname}`")

with open(r"D:\History vs Hype\_gemini-output\layer2-rename\WEB-LOOKUP-PROMPT-ROUND2.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

# Save off-topic list as JSON for one-click stash later
with open(r"D:\History vs Hype\_gemini-output\layer2-rename\round2-offtopic-candidates.json", "w", encoding="utf-8") as f:
    json.dump([{"idx":idx,"folder":folder,"fname":fname} for idx,folder,fname,_ in off_topic],
              f, indent=2, ensure_ascii=False)

print()
print(f"Wrote WEB-LOOKUP-PROMPT-ROUND2.md")
print(f"  Academic entries in prompt: {len(academic_unresolved)}")
print(f"  Off-topic candidates listed separately: {len(off_topic)}")
