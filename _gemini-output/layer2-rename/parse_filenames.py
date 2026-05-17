
import re
import json

# List of publisher abbreviations
PUBLISHER_ABBREVS = {
    "Cambridge University Press": "CambridgeUP",
    "CambridgeUP": "CambridgeUP",
    "Oxford University Press": "OxfordUP",
    "OxfordUP": "OxfordUP",
    "Yale University Press": "YaleUP",
    "YaleUP": "YaleUP",
    "Princeton University Press": "PrincetonUP",
    "PrincetonUP": "PrincetonUP",
    "Columbia University Press": "ColumbiaUP",
    "ColumbiaUP": "ColumbiaUP",
    "Indiana University Press": "IndianaUP",
    "IndianaUP": "IndianaUP",
    "Edinburgh University Press": "EdinburghUP",
    "EdinburghUP": "EdinburghUP",
    "NYU Press": "NYUPress",
    "NYUPress": "NYUPress",
    "University of California Press": "UCPress",
    "UCPress": "UCPress",
    "Johns Hopkins University Press": "JohnsHopkinsUP",
    "JohnsHopkinsUP": "JohnsHopkinsUP",
    "Hoover Press": "HooverPress",
    "HooverPress": "HooverPress",
    "Pluto Press": "PlutoPress",
    "PlutoPress": "PlutoPress",
    "Routledge": "Routledge",
    "Palgrave Macmillan": "Palgrave",
    "Palgrave": "Palgrave",
    "Bloomsbury Publishing": "Bloomsbury",
    "Bloomsbury": "Bloomsbury",
    "I.B. Tauris": "ITauris",
    "ITauris": "ITauris",
    "Hurst & Co.": "HurstCo",
    "HurstCo": "HurstCo",
    "Zed Books": "ZedBooks",
    "ZedBooks": "ZedBooks",
    "Verso Books": "VersoBooks",
    "VersoBooks": "VersoBooks",
    "Basic Books": "BasicBooks",
    "BasicBooks": "BasicBooks",
    "Random House": "RandomHouse",
    "RandomHouse": "RandomHouse",
    "Penguin": "Penguin",
    "Brill": "Brill",
    "Springer": "Springer",
    "Da Capo Press": "DaCapo",
    "DaCapo": "DaCapo",
    "Free Press": "FreePress",
    "FreePress": "FreePress",
    "Granta": "Granta",
    "Weidenfeld & Nicolson": "WeidenfeldNicolson",
    "WeidenfeldNicolson": "WeidenfeldNicolson",
    "Cornell University Press": "Cornell-UP",
    "Cornell-UP": "Cornell-UP",
    "Stanford University Press": "Stanford-UP",
    "Stanford-UP": "Stanford-UP",
    "Harvard University Press": "Harvard-UP",
    "Harvard-UP": "Harvard-UP",
    "Liverpool University Press": "Liverpool-UP",
    "Liverpool-UP": "Liverpool-UP",
    "FB & C Ltd": "Unknown", # This looks like a reprint publisher, not an academic press. Defaulting to unknown.
    "Forgotten Books": "Unknown", # Same as above
    "Literatura Random House": "RandomHouse", # This should be handled
    "Penguin Random House Grupo Editorial S-A-S": "RandomHouse" # Same as above
}

# Piracy markers to remove from title and publisher
PIRACY_MARKERS = [
    r"\(z-library\.sk.*?\)",
    r"\(1lib\.sk.*?\)",
    r"\(z-lib\.sk.*?\)",
    r"Anna’s Archive",
    r"libgen\.li",
    r"ZLib",
    r"-- \w{32} --", # 32-char hash often found with Anna's Archive
    r"\d{10,}" # ISBN like numbers, also often found near Anna's Archive
]

def clean_filename(filename):
    # Remove category prefix like "[african-history] "
    filename = re.sub(r"^\[.*?\]\s*", "", filename)
    # Remove file extension
    filename = re.sub(r"\.pdf$", "", filename, flags=re.IGNORECASE)
    # Remove common separators and excessive spaces
    filename = re.sub(r"-\s*$", "", filename) # remove trailing dash
    return filename.strip()

def extract_author(text):
    author = "Unknown"
    # Try to find author in parentheses at the end or within the string
    match = re.search(r"\(([^)]+?)\)", text)
    if match:
        potential_author = match.group(1).strip()
        # If it looks like a person's name (contains comma or two words capitalized)
        if "," in potential_author or len(potential_author.split()) > 1 and all(w.istitle() or w.isupper() for w in potential_author.split() if w not in ["and", "&"]):
            author_parts = potential_author.split(",")
            if len(author_parts) > 1: # Last name, First name
                last_name = author_parts[0].strip()
                author = last_name.replace(".", "").replace("Jr", "").strip().split()[-1] # take last word as last name for cases like "Williams Jr."
            else: # First name Last name
                author = potential_author.strip().split()[-1] # take last word as last name
            author = author.upper()
            if len(author) > 25:
                author = author[:25]
        # Check for known organizations/treaties
        elif potential_author.upper() in ["UN", "ICJ", "UK", "US", "EU", "AU", "NATO"]:
            author = potential_author.upper()
    
    # Fallback to look for author-like patterns outside parentheses, e.g. "Cook, Noble David"
    if author == "Unknown":
        # Look for "Lastname, Firstname" pattern
        match = re.search(r"([A-Za-z\s'\.-]+),\s+([A-Za-z\s'\.-]+)", text)
        if match:
            author = match.group(1).strip().upper()
            if len(author) > 25:
                author = author[:25]
        else:
            # Look for "Firstname Lastname" as part of the title but try to identify if it's an author
            # This is tricky and might pick up title words. More specific checks are needed.
            # For now, let's keep it simple and rely more on parentheses.
            pass
            
    return author


def extract_year(text):
    # Look for a four-digit year, possibly in parentheses or after a dash
    match = re.search(r"(\(?\d{4}\)?)", text)
    if match:
        year = re.sub(r"[()]", "", match.group(1))
        return year
    return "0000"

def extract_title(text):
    # Remove author and year in parentheses first to get a cleaner title string
    text = re.sub(r"\([^)]*\d{4}[^)]*\)", "", text) # remove (Author, YYYY) or (YYYY)
    text = re.sub(r"\(.*?\)","", text) # remove any remaining parentheses content, assuming it's not part of the title

    # Remove piracy markers
    for marker in PIRACY_MARKERS:
        text = re.sub(marker, "", text, flags=re.IGNORECASE)
    
    # Remove publisher info if present at the end
    for pub_name, pub_abbrev in PUBLISHER_ABBREVS.items():
        text = re.sub(r"-\s*{}\s*(,|\d{{4}}|$)".format(re.escape(pub_name)), "", text, flags=re.IGNORECASE)
        text = re.sub(r"-\s*{}\s*(,|\d{{4}}|$)".format(re.escape(pub_abbrev)), "", text, flags=re.IGNORECASE)
    
    # Remove common descriptive words or phrases that aren't part of the core title
    text = re.sub(r"vol \d", "", text, flags=re.IGNORECASE)
    text = re.sub(r"new approaches to the americas", "", text, flags=re.IGNORECASE)
    text = re.sub(r"cambridge new york", "", text, flags=re.IGNORECASE)
    text = re.sub(r"paperback edition london", "", text, flags=re.IGNORECASE)
    text = re.sub(r"the church and the non-christian world", "", text, flags=re.IGNORECASE)
    text = re.sub(r"a history and source book", "", text, flags=re.IGNORECASE)
    text = re.sub(r"classic reprint", "", text, flags=re.IGNORECASE)
    text = re.sub(r"studies in antisemitism", "", text, flags=re.IGNORECASE)
    
    text = re.sub(r"\s*--\s*.*", "", text) # remove anything after '--'
    
    # Clean up and format
    title_words = re.findall(r"[A-Za-z0-9]+", text)
    title = "".join(word.capitalize() for word in title_words)
    
    # Remove "The", "A", "An" prefixes
    if title.startswith("The") and len(title) > 3:
        title = title[3:]
    elif title.startswith("A") and len(title) > 1:
        title = title[1:]
    elif title.startswith("An") and len(title) > 2:
        title = title[2:]
        
    title = title.replace("978", "").replace("979", "").strip() # remove ISBN-like numbers
    title = re.sub(r"\d{10,}", "", title) # remove long numbers that might be ISBNs
    title = re.sub(r"[^\w]", "", title) # remove any remaining non-alphanumeric chars
    
    if len(title) > 45:
        title = title[:45]
    
    return title if title else "Untitled"


def extract_publisher(text):
    for pub_name, pub_abbrev in PUBLISHER_ABBREVS.items():
        if re.search(re.escape(pub_name), text, re.IGNORECASE) or re.search(re.escape(pub_abbrev), text, re.IGNORECASE):
            return pub_abbrev
    
    # Check for piracy markers indicating no valid publisher
    for marker in PIRACY_MARKERS:
        if re.search(marker, text, re.IGNORECASE):
            return "Unknown"
            
    # Generic "Press" check for names not explicitly listed but common.
    # This needs to be carefully handled to avoid false positives.
    # For now, stick to the explicit list.
    
    return "Unknown"

def parse_filename_entry(entry_num, full_filename):
    original_filename_no_prefix = re.sub(r"^\d+\.\s*\[.*?\]\s*", "", full_filename)
    cleaned_name_for_parsing = clean_filename(full_filename)

    author = extract_author(cleaned_name_for_parsing)
    year = extract_year(cleaned_name_for_parsing)
    publisher = extract_publisher(cleaned_name_for_parsing)
    title = extract_title(cleaned_name_for_parsing)

    return {
        "i": entry_num,
        "f": original_filename_no_prefix,
        "a": author,
        "y": year,
        "t": title,
        "p": publisher
    }

# Input data (this will be replaced by actual input)
input_filenames = """
1. [african-history] 2024-Coupvolution-Terrorism-Sahel-Springer-142-159.pdf
2. [african-history] Africas Last Colonial Currency The CFA Franc Story (Fanny Pigeaud Ndongo Samba Sylla).pdf
3. [african-history] Bulletin_officiel_de_l'État_indépendant_[...]Congo_(République_bd6t53484301.pdf
4. [african-history] Coloniality of power in postcolonial Africa myths of decolonization (Ndlovu-Gatsheni, Sabelo J.).pdf
5. [african-history] Conflicted colonialisms multi-dimensional violence in the Western Sahel.pdf
6. [african-history] Dis utilities of Force in a Postcolonial Context Explaining the Strategic Failure of the French-Led Intervention in Mali.pdf
7. [african-history] French-interventionism-in-the-Sahel.pdf
8. [african-history] Imperialism, Sovereignty and the Making of International Law (Antony Anghie) (z-library.sk, 1lib.sk, z-lib.sk).pdf
9. [african-history] The Sahel- A Cognitive Mapping -- Rahmane Idrissa -- 01bc973ea2fde3cab83c55c82db4a642 -- Anna’s Archive.pdf
10. [african-history] Villalón - Oxford Handbook of African Sahel (2021).pdf
11. [african-history] Villalón - The Oxford Handbook of the African Sahel (2021).pdf
12. [colonialism-slavery] A History of Portugal and the Portuguese Empire, from Beginnings to 1807, Vol 2) - The Portuguese Empire (Anthony R. Disney) (z-library.sk, 1lib.sk, z-lib.sk).pdf
13. [colonialism-slavery] Born to Die- Disease and New World Conquest, 1492–1650 (New -- Cook, Noble David -- New approaches to the Americas, Cambridge, New York, -- Cambridge -- 9780521622080 -- 9c96325f074d0f778a49d4b401200735 -- Anna’s Archive.pdf
14. [colonialism-slavery] First Manhattans A History of the Indians of Greater New York (Robert S. Grumet) (z-library.sk, 1lib.sk, z-lib.sk).pdf
15. [colonialism-slavery] History of New Netherland or, New York under the Dutch (Edmund Bailey OCallaghan) (z-library.sk, 1lib.sk, z-lib.sk).pdf
16. [colonialism-slavery] How the Incas Built Their Heartland - State Formation and the Innovation of Imperial Strategies in the Sacred Valley, Peru… (R. Alan Covey).pdf
17. [colonialism-slavery] Hugh Kennedy - The Great Arab Conquests- How the Spread of Islam Changed the World We Live In (2008, Da Capo Press).pdf
18. [colonialism-slavery] Lauren Benton - A Search for Sovereignty_ Law and Geography in European Empires, 1400-1900 (2009, Cambridge University Press) - libgen.li.pdf
19. [colonialism-slavery] Lenape Country Delaware Valley Society Before William Penn (Jean R. Soderlund) (z-library.sk, 1lib.sk, z-lib.sk).pdf
20. [colonialism-slavery] Lords of all the world ideologies of empire in Spain, Britain and France c. 1500-c. 1800 (Pagden, Anthony) (z-library.sk, 1lib.sk, z-lib.sk).pdf
21. [colonialism-slavery] Narratives of New Netherland, 1609-1664 (Various, J. Franklin Jameson) (z-library.sk, 1lib.sk, z-lib.sk).pdf
22. [colonialism-slavery] Popes, Lawyers, and Infidels The Church and the Non-Christian World, 1250-1550 (James Muldoon) (z-library.sk, 1lib.sk, z-lib.sk).pdf
23. [colonialism-slavery] Stannard - American Holocaust (1992).pdf
24. [colonialism-slavery] Taner Akçam - The Young Turks' Crime Against Humanity- The Armenian Genocide and Ethnic Cleansing in the Ottoman Empire (2012, PrincetonUP).pdf
25. [colonialism-slavery] The American Indian in Western Legal Thought The Discourses of Conquest (Robert A. Williams Jr.) (z-library.sk, 1lib.sk, z-lib.sk).pdf
26. [colonialism-slavery] The Colony of New Netherland A Dutch Settlement in Seventeenth-Century America (Jacobs, Jaap) (z-library.sk, 1lib.sk, z-lib.sk)-1.pdf
27. [colonialism-slavery] The Colony of New Netherland A Dutch Settlement in Seventeenth-Century America (Jacobs, Jaap) (z-library.sk, 1lib.sk, z-lib.sk)-2.pdf
28. [colonialism-slavery] The Colony of New Netherland A Dutch Settlement in Seventeenth-Century America (Jacobs, Jaap) (z-library.sk, 1lib.sk, z-lib.sk).pdf
29. [colonialism-slavery] The grandfathers speak (Hìtakonanulaxk.) (z-library.sk, 1lib.sk, z-lib.sk).pdf
30. [colonialism-slavery] The Lenape or Delaware Indians the original people of New Jersey, southeastern New York State, eastern Pennsylvania, northern… (Kraft, Herbert C, Kraft etc.) (z-library.sk, 1lib.sk, z-lib.sk).pdf
31. [colonialism-slavery] The Portuguese seaborne empire 1415-1825 (Boxer, C. R. (Charles Ralph), 1904-) (z-library.sk, 1lib.sk, z-lib.sk).pdf
32. [colonialism-slavery] Tinniswood--Adrian-Pirates-of-Barbary--Corsairs--Conquests-and-Captivity-in-the-17th-Century-Mediter.pdf
33. [crusades-christianity] Emon - Religious Pluralism and Islamic Law (2012).pdf
34. [general-history] 1 - Article · March 2013 (n.d.).pdf
35. [general-history] El país de la canela -- Ospina William -- Literatura Random House, Primera edición, 1a- reimpresión, -- Penguin Random House Grupo Editorial S-A-S -- 9789585820777 -- e9d19101d3a028b159286a52bc270f05 -- Anna’s Archive.pdf
36. [general-history] Göttsche - An Integrated Approach to Nuclear Archaeology (2019).pdf
37. [general-history] Israel - a history -- Anita Shapira; Anthony Berris -- W & N paperback, Paperback edition, London, 2015 -- Weidenfeld & Nicolson -- 9781780227399 -- 675a2a02dfdf24bad435035d17c30848 -- Anna’s Archive.pdf
38. [general-history] Lines-Drawn-on-an-Empty-Map-Iraq-s-Borde.pdf
39. [general-history] McMahon–Hussein-Correspondence-1.pdf
40. [general-history] Misha Glenny - The Balkans, 1804–2012 (2012, Granta Publications).pdf
41. [general-history] Peter Hayes- John K. Roth - The Oxford Handbook of Holocaust Studies (2010, Oxford University Press).pdf
42. [general-history] Schneer - The Balfour Declaration (2010).pdf
43. [general-history] The Cousins Wars- Religion, Politics, Civil Warfare, And -- Phillips, Kevin P..pdf
44. [general-history] the early cultures of north-west europe -- Sir Cyril Fox and Bruce Dickins -- 1950 -- 5fb35db5e8f4a4a584d974b63819e1c1 -- Anna’s Archive.pdf
45. [general-history] The Island at the Center of the World (Shorto Russell) (z-library.sk, 1lib.sk, z-lib.sk).pdf
46. [general-history] The Myth of Nations- The Medieval Origins of Europe- -- Geary, Patrick J-, 1948- -- Princeton paperbacks, 2- print-, 1- paperback print, -- Princeton, -- 9780691090542 -- a1bfcabeb85d3995592c59ff974aea11 -- Anna’s Archive.pdf
47. [general-history] The Persian Revolution of 1905-1909 (Classic Reprint) -- Edward G_ Browne -- FB & C Ltd, London, 2018 -- Forgotten Books -- 9780259728894 -- db8a657678d140c752cd51d2d1dc1c5d -- Anna’s Archive.pdf
48. [general-history] Women and Weapons in the Viking World Amazons of the North (Leszek Gardeła).pdf
49. [general-history] Women in the Viking Age (Judith Jesch).pdf
50. [middle-east-history] Geissinger, Aisha - Gender and Muslim Constructions of Exegetical Authority __ (2015, BRILL) [10.1163_9789004294448] - libgen.li.pdf
51. [middle-east-history] IslamicInterpretiveTraditionGenderJustic-(editor)-0000-ZLib.pdf
52. [middle-east-history] Norman Cohn - Warrant for Genocide- The Myth of the Jewish World Conspiracy and the Protocols of the Elders of Zion (2005, Serif).pdf
53. [middle-east-history] The Jews of Arab lands - a history and source book -- Norman A Stillman; Mazal Holocaust Collection.pdf
54. [middle-east-history] The Plot. The secret story of The Protocols of the Elders of Zion (Will Eisner).pdf
55. [reference-methodology] The Non-existent Manuscript- A Study Of The Protocols Of The -- Cesare G De Michelis; Richard Newhouse; Vidal Sassoon -- Studies in antisemitism, -- 9780803217270 -- b29396f9d808955034615c4942c8a73e -- Anna’s Archive.pdf
"""

if __name__ == "__main__":
    results = []
    for i, line in enumerate(input_filenames.strip().splitlines()):
        if line.strip():
            # Extract the original filename without the leading number and category prefix
            match = re.match(r"^\s*\d+\.\s*(.*)", line)
            if match:
                original_full_filename = match.group(1).strip()
                results.append(parse_filename_entry(i + 1, original_full_filename))
    
    print(json.dumps(results, indent=None))
