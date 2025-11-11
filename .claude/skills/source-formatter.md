# Source List Formatter - History vs Hype

Format source lists for video descriptions. Organize sources by type, verify URLs work, and create copy-paste ready lists.

## Activation

Use when user says:
- "Format my sources for description"
- "Organize source list"
- "Create source citations"
- "/format-sources"

## STEP 1: Get Sources

Ask for:
1. **Source list** (from script, research notes, or manual list)
2. **Citation style** (default: YouTube description format with URLs)

## STEP 2: Categorize Sources

Group sources into categories:

### Category 1: Primary Documents
- Papal bulls, encyclicals, church documents
- Treaties, government documents
- Historical letters, correspondence
- Court rulings, legal documents
- Original archaeological/scientific studies

### Category 2: Founding Documents (if applicable)
- Founding Fathers' writings
- Constitutional documents
- Early American government records

### Category 3: Academic Sources
- Peer-reviewed books
- Academic journal articles
- University press publications

### Category 4: News/Modern Sources (if applicable)
- News articles (for modern relevance)
- Government reports
- Policy documents

### Category 5: Archival/Historical Sources
- Codices, chronicles
- Historical manuscripts
- Archaeological reports
- Period documents

## STEP 3: Format Each Source

### For Primary Documents with URLs:

```
[Document Name] ([Year]): [URL]
```

**Example:**
```
Mirari Vos (1832): https://www.papalencyclicals.net/greg16/g16mirar.htm
```

### For Books:

```
[Author], "[Book Title]" ([Publisher], [Year])
```

**Example:**
```
Samuel Moyn, "Christian Human Rights" (University of Pennsylvania Press, 2015)
```

### For Journal Articles:

```
[Author], "[Article Title]," [Journal Name] ([Year]): [URL if available]
```

**Example:**
```
Brian Levack, "The Witch-Hunt in Early Modern Europe," Journal of Modern History (1987)
```

### For News Articles:

```
[Author/Publication], "[Title]" ([Date]): [URL]
```

**Example:**
```
New York Times, "Florida Education Standards Spark Controversy" (July 2023): [URL]
```

## STEP 4: Verify URLs

For each URL provided:
- Note if URL is accessible
- Flag if URL is paywalled
- Suggest alternative if URL broken
- Provide archive.org alternative if needed

**Output:**
```
✅ URL verified: [URL]
❌ URL broken: [URL] - Suggested alternative: [archive.org link]
⚠️ URL paywalled: [URL] - Note for user
```

## STEP 5: Generate Formatted List

Create copy-paste ready source list:

```markdown
📚 PRIMARY SOURCES CITED:

**[Category 1 Name]:**
- [Source 1]
- [Source 2]
- [Source 3]

**[Category 2 Name]:**
- [Source 1]
- [Source 2]

**Academic Sources:**
- [Source 1]
- [Source 2]

**[Other Categories as needed]**
```

## Output Format

```markdown
# FORMATTED SOURCE LIST - [Video Title]

**Date:** [Date]
**Total Sources:** [Number]

---

## COPY-PASTE READY FORMAT

📚 PRIMARY SOURCES CITED:

**Papal Documents:**
- Mirari Vos (1832): https://www.papalencyclicals.net/greg16/g16mirar.htm
- Syllabus of Errors (1864): https://www.papalencyclicals.net/pius09/p9syll.htm

**Founding Documents:**
- Madison's Memorial and Remonstrance: https://founders.archives.gov/documents/Madison/01-08-02-0163

**Academic Sources:**
- Samuel Moyn, "Christian Human Rights" (University of Pennsylvania Press, 2015)
- Matthew Restall, "Seven Myths of the Spanish Conquest" (Oxford University Press, 2000)

---

## URL VERIFICATION REPORT

✅ **Working URLs:** [Number]
- [List URLs that work]

❌ **Broken URLs:** [Number]
- [List broken URLs with alternatives]

⚠️ **Paywalled Sources:** [Number]
- [List paywalled sources]

---

## MISSING INFORMATION

Sources that need more details:
- [Source name]: Missing [what's missing - year, publisher, URL, etc.]

---

## ALPHABETICAL REFERENCE LIST (Optional)

Full alphabetical list for academic citation if needed:

[Author Last Name, First Name. "Title." Publisher, Year.]
[Continue alphabetically]

---

## NOTES

- Total primary sources: [Number]
- Total academic sources: [Number]
- All URLs verified: [Yes/No]
- Ready for video description: [Yes/No - if no, explain what's needed]
```

## Common Source Templates

### Papal Encyclicals:
```
[Encyclical Name] ([Year]): https://www.papalencyclicals.net/[pope]/[filename].htm
```

### Founding Fathers' Writings:
```
[Title/Letter Name]: https://founders.archives.gov/documents/[Name]/[reference]
```

### Vatican Documents:
```
[Document Name] ([Year]): https://www.vatican.va/archive/hist_councils/[council]/documents/[filename].html
```

### Archaeological/Scientific Studies:
```
[Authors], "[Title]," [Journal Name] [Volume] ([Year]): https://doi.org/[DOI]
```

### Historical Treaties:
```
[Treaty Name] ([Year]): https://avalon.law.yale.edu/[century]/[filename].asp
```

## Source Credibility Notes

Add credibility notes for non-obvious sources:

```
📝 SOURCE NOTES:

**Doctrine of Discovery Project:**
Independent research collaborative documenting papal bulls. Hosted by Syracuse University. Academic peer-reviewed.

**Papal Encyclicals Online:**
Comprehensive archive of papal documents. Widely used by scholars. English translations verified against Latin originals.

**Founders Online:**
National Archives official database. Primary source documents with editorial annotations.
```

## Quality Control Checklist

Before delivering formatted list:

- [ ] All sources grouped by category
- [ ] URLs tested and working
- [ ] Books have full citation (author, title, publisher, year)
- [ ] Primary documents have dates
- [ ] Alternative URLs provided for broken links
- [ ] Paywalled sources flagged
- [ ] Format is copy-paste ready
- [ ] Alphabetical within categories

## Integration with Other Skills

**When to use:**
- After script is finalized
- Before generating YouTube metadata
- When preparing video description

**Works with:**
- youtube-metadata skill (uses this source list)
- fact-checker skill (sources from fact-check reports)
- script-generator skill (sources cited in script)

---

**This skill ensures every source is properly cited and accessible to viewers.**
