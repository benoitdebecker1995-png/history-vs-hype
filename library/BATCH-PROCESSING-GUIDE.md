# Batch Processing Guide - Organizing 395 Remaining Books

**Goal:** Organize 395 remaining books from Downloads → library/by-topic/
**Current Progress:** 21 done, 395 to go
**Estimated Time:** 3-4 hours (with script assistance)

---

## OPTION 1: Semi-Automated (Recommended)

Use the provided bash script to process books by category in batches.

### Step 1: Find Books by Category

```bash
# Crusades & Christianity (find remaining)
find "C:\Users\benoi\Downloads" -type f -name "*.pdf" | grep -iE "(crusad|templar|saladin|richard|muslim|christian|byzantine|holy land)" > crusades-list.txt

# Colonialism & Slavery
find "C:\Users\benoi\Downloads" -type f -name "*.pdf" | grep -iE "(slave|abolition|colonial|empire|plantation|africa)" > colonialism-list.txt

# Middle East History
find "C:\Users\benoi\Downloads" -type f -name "*.pdf" | grep -iE "(ottoman|turk|arab|persia|iran|iraq|syria|lebanon|palestine|israel|jordan)" > middleeast-list.txt

# Territorial Disputes
find "C:\Users\benoi\Downloads" -type f -name "*.pdf" | grep -iE "(belize|guatemala|kashmir|cyprus|essequibo|guyana|venezuela|border|territory|dispute)" > territorial-list.txt

# African History
find "C:\Users\benoi\Downloads" -type f -name "*.pdf" | grep -iE "(sahel|mali|niger|senegal|ivory coast|ghana|nigeria|kenya|ethiopia|rwanda|congo)" > african-list.txt
```

### Step 2: Review Lists

Open each .txt file and review the filenames. Remove any false matches.

### Step 3: Process Each Category

Use the naming script below for each book:

```bash
# Example: Processing a Crusades book
OLD_FILE="Crusades-and-Jihad-Origins-Development-and-Legacy-_-Catlos_-Brian-A_-_2024_-Oxford-UP.pdf"
NEW_FILE="Catlos - Crusades and Jihad Origins and Legacy (2024).pdf"
CATEGORY="crusades-christianity"

cp "C:\Users\benoi\Downloads/$OLD_FILE" "C:\Users\benoi\Documents\History vs Hype\library\by-topic/$CATEGORY/$NEW_FILE"
```

---

## OPTION 2: Manual Processing (Slower but More Control)

Process books one by one with full manual review.

### Workflow:

1. **Open Downloads folder** in File Explorer
2. **Sort by Name** (or Date Modified)
3. **For each book:**
   - Read title/author from filename
   - Decide category
   - Clean filename to format: `Author - Title (Year).pdf`
   - Cut & paste to appropriate folder
   - Add entry to LIBRARY-INDEX.md

**Time estimate:** ~1-2 minutes per book = 6-13 hours total

---

## OPTION 3: Quick Categorization Script

Save this as `organize-books.sh` and run in Git Bash:

```bash
#!/bin/bash

# Set paths
DOWNLOADS="C:\Users\benoi\Downloads"
LIBRARY="C:\Users\benoi\Documents\History vs Hype\library\by-topic"

# Function to clean filename
clean_name() {
    local file="$1"
    local author="$2"
    local title="$3"
    local year="$4"
    echo "${author} - ${title} (${year}).pdf"
}

# Process Crusades books (example)
echo "Processing Crusades books..."
find "$DOWNLOADS" -type f -name "*.pdf" | grep -iE "crusad" | while read -r file; do
    filename=$(basename "$file")

    # Extract author and title (basic pattern matching)
    # This is simplified - you'll need to customize per file

    if [[ $filename =~ \(([^)]+)\).*\(Z-Library\) ]]; then
        author="${BASH_REMATCH[1]}"
        # Continue parsing...
    fi

    # For now, just list files needing manual review
    echo "Review: $filename"
done

echo "Done! Review output and customize script as needed."
```

**Note:** This script needs customization for your specific filename patterns. It's a starting template.

---

## FILENAME CLEANING PATTERNS

### Z-Library Format:
```
Before: "God's War A New History of the Crusades (Christopher Tyerman) (Z-Library).pdf"
After:  "Tyerman - Gods War A New History of the Crusades (2006).pdf"

Pattern: Extract author from parentheses, remove Z-Library suffix, add year
```

### Anna's Archive Format:
```
Before: "A line in the sand the Anglo-French struggle for the Middle East, 1914-1948 -- James Barr -- hash123 -- Anna's Archive.pdf"
After:  "Barr - A Line in the Sand (2011).pdf"

Pattern: Extract from " -- " separators, remove hash and suffix, add year
```

### WeLib Format:
```
Before: "Africa Since 1940- The Past Of The Present -- Frederick Cooper -- ( WeLib.org ).pdf"
After:  "Cooper - Africa Since 1940 (2002).pdf"

Pattern: Similar to Anna's Archive, remove WeLib suffix
```

### Academic Papers (DOI/Journal):
```
Before: "10.1515_soeu-2021-0059.pdf"
After:  Move to separate "academic-papers/" folder, research proper citation

Pattern: These need manual research to get author/title
```

---

## CATEGORIZATION DECISION TREE

### Is it about Crusades/Christian-Muslim relations?
→ `crusades-christianity/`
- Keywords: crusad, templar, saladin, jerusalem, pilgrimage, jihad, islamic conquests

### Is it about colonialism/slavery/empire?
→ `colonialism-slavery/`
- Keywords: slave, abolition, colonial, empire, plantation, imperial

### Is it about Middle East history (non-Crusades)?
→ `middle-east-history/`
- Keywords: ottoman, arab, persian, sykes, picot, mandate, lebanon, syria

### Is it about territorial disputes/borders?
→ `territorial-disputes/`
- Keywords: border, territory, dispute, conflict, kashmir, belize, essequibo, cyprus

### Is it about African history (post-colonial)?
→ `african-history/`
- Keywords: sahel, decolonization, african independence, rwanda, congo, apartheid

### Is it general historical methodology?
→ `reference-methodology/`
- Keywords: historiography, sources, evidence, research methods

### Everything else?
→ `general-history/`

---

## QUICK REFERENCE: TOPIC KEYWORDS

### crusades-christianity/
`crusad, templar, hospitaller, saladin, richard lion, jerusalem, acre, constantinople, byzantine, orthodox, catholic, muslim, christian, jihad, holy land, pilgrimage, saracen`

### colonialism-slavery/
`slave, abolition, colonial, empire, imperial, plantation, triangular trade, atlantic, east india, bengal, raj, apartheid, settler, indigenous`

### middle-east-history/
`ottoman, turk, arab, persian, iran, iraq, syria, lebanon, palestine, israel, jordan, kuwait, saudi, yemen, mandate, sykes, picot, balfour`

### territorial-disputes/
`belize, guatemala, kashmir, cyprus, essequibo, guyana, venezuela, nagorno karabakh, azerbaijan, armenia, border, territory, dispute, conflict, icj, arbitration`

### african-history/
`sahel, mali, niger, senegal, burkina, ivory coast, ghana, nigeria, cameroon, chad, sudan, ethiopia, somalia, kenya, tanzania, rwanda, burundi, congo, angola, mozambique, zimbabwe, south africa, decolonization, independence`

### reference-methodology/
`historiography, historical method, sources, evidence, archive, primary source, oral history, bias, interpretation`

---

## BATCH PROCESSING WORKFLOW

### Session 1 (1 hour): Crusades Books
1. Run find command to list Crusades books
2. Process ~20-30 books
3. Update LIBRARY-INDEX.md with new entries

### Session 2 (1 hour): Colonialism Books
1. Run find command to list Colonialism books
2. Process ~20-30 books
3. Update LIBRARY-INDEX.md

### Session 3 (1 hour): Middle East Books
1. Run find command to list Middle East books
2. Process ~20-30 books
3. Update LIBRARY-INDEX.md

### Session 4-6 (3 hours): Remaining Categories
- Territorial disputes
- African history
- General history
- Reference books
- Academic papers (separate workflow)

**Total: 6 hours across multiple sessions**

---

## ACADEMIC PAPERS WORKFLOW (Separate)

Academic papers need different handling:

### Create separate folder:
```
library/
└── academic-papers/
    ├── by-author/
    ├── by-topic/
    └── by-year/
```

### For papers with DOI/journal codes:
1. Look up DOI online to get full citation
2. Rename to: `Author - Article Title (Year) [Journal].pdf`
3. Example: `Hedenstierna-Jonson - Female Viking Warrior Confirmed (2017) [Am J Phys Anthro].pdf`

### For anonymous PDFs (722380.pdf, etc.):
1. Open PDF
2. Check first page for title/author
3. Research if needed
4. Rename appropriately

---

## DUPLICATION HANDLING

### Found multiple versions of same book?

**Example:** Armenian People book has 3 copies:
```
..._compre-1.pdf
..._compre.pdf
...Anna's Archive.pdf
```

**Action:**
1. Compare file sizes
2. Keep largest (usually best quality)
3. Delete duplicates
4. Rename and move the best version

**Check for duplicates:**
```bash
# Find potential duplicates (similar names)
find "C:\Users\benoi\Downloads" -name "*Armenian*people*.pdf"

# List them with sizes
find "C:\Users\benoi\Downloads" -name "*Armenian*people*.pdf" -exec ls -lh {} \;
```

---

## PROGRESS TRACKING

Create a simple progress tracker:

```bash
# Count total PDFs in Downloads
echo "Total in Downloads: $(find 'C:\Users\benoi\Downloads' -name '*.pdf' | wc -l)"

# Count organized books
echo "Crusades: $(ls -1 'C:\Users\benoi\Documents\History vs Hype\library\by-topic\crusades-christianity' | wc -l)"
echo "Colonialism: $(ls -1 'C:\Users\benoi\Documents\History vs Hype\library\by-topic\colonialism-slavery' | wc -l)"
echo "Middle East: $(ls -1 'C:\Users\benoi\Documents\History vs Hype\library\by-topic\middle-east-history' | wc -l)"
echo "General: $(ls -1 'C:\Users\benoi\Documents\History vs Hype\library\by-topic\general-history' | wc -l)"

# Calculate total organized
# Add more categories as you create them
```

---

## TROUBLESHOOTING

### Problem: Filename too long for Windows
**Solution:** Shorten title in cleaned filename, keep essential words only

### Problem: Special characters in filename (', ", :, etc.)
**Solution:** Remove or replace with hyphen

### Problem: Can't determine author from filename
**Solution:**
1. Open PDF, check cover/title page
2. Google the title
3. If still unknown, use "Unknown - Title (Year).pdf"

### Problem: Can't determine publication year
**Solution:**
1. Check PDF copyright page
2. Google the title + author
3. If unknown, use (n.d.) for "no date"

### Problem: Book fits multiple categories
**Solution:**
- Put in primary category
- Add cross-reference note in LIBRARY-INDEX.md
- Example: Crusades book that's also about colonialism → Put in crusades, note in colonialism section

---

## COMPLETION CHECKLIST

When you've processed all books:

- [ ] All PDFs moved from Downloads to library/
- [ ] All books renamed to clean format
- [ ] LIBRARY-INDEX.md updated with all books
- [ ] Duplicates removed
- [ ] Academic papers separated
- [ ] for-notebooklm/ folders created for active projects
- [ ] README created in each topic folder
- [ ] Downloads folder cleared (or archived)

---

## MAINTENANCE GOING FORWARD

### When downloading new books:
1. Don't let them pile up in Downloads
2. Categorize immediately
3. Rename to standard format
4. Move to appropriate topic folder
5. Add to LIBRARY-INDEX.md

### Monthly review:
- Update LIBRARY-INDEX.md stats
- Check for new duplicates
- Reorganize if categories get too large

---

## NEED HELP?

If you get stuck or want automation help:
1. Ask Claude Code to process a specific category
2. Provide the category name and let AI do the bulk processing
3. You review and approve the categorizations

**Example request:**
```
"Process all Crusades books in my Downloads folder:
- Find all PDFs matching crusades keywords
- Clean filenames to Author - Title (Year) format
- Move to library/by-topic/crusades-christianity/
- Update LIBRARY-INDEX.md"
```

---

**Good luck organizing your library!** 📚

Start with one category (Crusades recommended since you just used those books), process 20-30 books, take a break, repeat. You'll have everything organized in a few sessions.
