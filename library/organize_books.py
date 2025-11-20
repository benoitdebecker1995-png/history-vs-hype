#!/usr/bin/env python3
"""
Batch process PDFs from Downloads to library/by-topic folders
Handles filename cleaning and categorization
"""

import os
import re
import shutil
from pathlib import Path

# Paths
DOWNLOADS = Path(r"C:\Users\benoi\Downloads")
LIBRARY = Path(r"C:\Users\benoi\Documents\History vs Hype\library\by-topic")

# Category keywords
CATEGORIES = {
    "territorial-disputes": [
        "belize", "guatemala", "kashmir", "cyprus", "essequibo", "guyana",
        "venezuela", "nagorno", "karabakh", "armenia", "azerbaijan", "kosovo",
        "border.*dispute", "territorial.*dispute", "ararat"
    ],
    "colonialism-slavery": [
        "slave", "slavery", "abolition", "colonial", "empire", "imperial",
        "plantation", "triangular.*trade", "atlantic.*slave", "bengal", "raj",
        "apartheid", "settler", "indigenous", "encomienda", "conquest",
        "new.*world", "disease.*conquest"
    ],
    "african-history": [
        "sahel", "mali", "niger", "senegal", "burkina", "ivory.*coast",
        "ghana", "nigeria", "cameroon", "chad", "sudan", "ethiopia",
        "somalia", "kenya", "tanzania", "rwanda", "burundi", "congo",
        "angola", "mozambique", "zimbabwe", "south.*africa", "decoloni",
        "independence.*africa", "cfa.*franc"
    ],
    "middle-east-history": [
        "ottoman", "turk", "arab", "persian", "iran", "iraq", "syria",
        "lebanon", "palestine", "israel", "jordan", "kuwait", "saudi",
        "yemen", "mandate", "sykes", "picot", "balfour", "zion", "fateful.*triangle"
    ],
    "crusades-christianity": [
        "crusad", "templar", "hospitaller", "saladin", "richard.*lion",
        "jerusalem", "acre", "constantinople", "byzantine", "orthodox",
        "catholic", "jihad", "holy.*land", "pilgrimage", "saracen",
        "islamic.*conquest"
    ],
    "reference-methodology": [
        "historiography", "historical.*method", "sources", "evidence",
        "archive", "primary.*source", "oral.*history", "bias",
        "interpretation", "holocaust", "auschwitz", "protocols.*elders",
        "genocide.*studies", "paranoid"
    ],
}

def clean_filename(filepath):
    """Extract author, title, year from various naming patterns"""
    filename = filepath.stem

    # Pattern 1: Z-Library format: "Title (Author) (Z-Library)"
    z_lib = re.match(r"(.+?)\s+\((.+?)\)\s+\(Z-Library\)", filename)
    if z_lib:
        title, author = z_lib.groups()
        # Try to extract year from title if present
        year_match = re.search(r"(\d{4})", title)
        year = year_match.group(1) if year_match else "n.d."
        # Clean author name (Last, First or First Last)
        if "," in author:
            last, first = author.split(",", 1)
            author = last.strip()
        else:
            parts = author.strip().split()
            author = parts[-1] if parts else "Unknown"
        return f"{author} - {title.strip()} ({year}).pdf"

    # Pattern 2: Anna's Archive format: "Title -- Author -- ...hash... -- Anna's Archive"
    anna = re.match(r"(.+?)\s+--\s+(.+?)\s+--\s+.+?--\s+Anna'?s Archive", filename)
    if anna:
        title, author = anna.groups()
        year_match = re.search(r"(\d{4})", filename)
        year = year_match.group(1) if year_match else "n.d."
        # Extract last name
        parts = author.strip().split(",")
        if len(parts) > 1:
            author = parts[0].strip()
        else:
            parts = author.strip().split()
            author = parts[-1] if parts else "Unknown"
        return f"{author} - {title.strip()} ({year}).pdf"

    # Pattern 3: WeLib format: "Title -- Author -- ( WeLib.org )"
    welib = re.match(r"(.+?)\s+--\s+(.+?)\s+--\s+\(\s*WeLib", filename)
    if welib:
        title, author = welib.groups()
        year_match = re.search(r"(\d{4})", filename)
        year = year_match.group(1) if year_match else "n.d."
        parts = author.strip().split(",")
        if len(parts) > 1:
            author = parts[0].strip()
        else:
            parts = author.strip().split()
            author = parts[-1] if parts else "Unknown"
        return f"{author} - {title.strip()} ({year}).pdf"

    # Pattern 4: libgen format: "Author - Title (Year, Publisher) - libgen.li"
    libgen = re.match(r"(.+?)\s+-\s+(.+?)\s+\((\d{4}),?\s+.+?\)\s+-\s+libgen", filename)
    if libgen:
        author, title, year = libgen.groups()
        parts = author.strip().split()
        author = parts[-1] if parts else "Unknown"
        return f"{author} - {title.strip()} ({year}).pdf"

    # Pattern 5: Already clean "Author - Title (Year)"
    clean = re.match(r"(.+?)\s+-\s+(.+?)\s+\((\d{4})\)", filename)
    if clean:
        return filename + ".pdf"

    # Default: return as-is
    return filename + ".pdf"

def categorize_file(filepath):
    """Determine category based on keywords"""
    filename_lower = filepath.name.lower()

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if re.search(keyword, filename_lower):
                return category

    return "general-history"

def process_books():
    """Main processing function"""
    pdfs = list(DOWNLOADS.glob("*.pdf"))
    total = len(pdfs)
    processed = 0
    skipped = 0
    errors = []

    print(f"Found {total} PDFs in Downloads")
    print("Processing...\n")

    for pdf_path in pdfs:
        try:
            # Skip if already processed (check if exists in library)
            if any((LIBRARY / cat).glob(f"*{pdf_path.stem[:20]}*") for cat in CATEGORIES.keys()):
                skipped += 1
                continue

            # Categorize
            category = categorize_file(pdf_path)

            # Clean filename
            new_name = clean_filename(pdf_path)

            # Destination
            dest_folder = LIBRARY / category
            dest_folder.mkdir(parents=True, exist_ok=True)
            dest_path = dest_folder / new_name

            # Copy (don't move, for safety)
            if not dest_path.exists():
                shutil.copy2(pdf_path, dest_path)
                processed += 1
                print(f"✓ [{category}] {new_name}")
            else:
                skipped += 1

        except Exception as e:
            errors.append((pdf_path.name, str(e)))
            print(f"✗ Error: {pdf_path.name} - {e}")

    print(f"\n{'='*60}")
    print(f"SUMMARY:")
    print(f"  Total PDFs: {total}")
    print(f"  Processed: {processed}")
    print(f"  Skipped: {skipped}")
    print(f"  Errors: {len(errors)}")

    if errors:
        print(f"\nErrors:")
        for filename, error in errors[:10]:
            print(f"  - {filename}: {error}")

if __name__ == "__main__":
    process_books()
