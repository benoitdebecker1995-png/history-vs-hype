#!/bin/bash
# Process all remaining categories

DOWNLOADS="/c/Users/benoi/Downloads"
LIBRARY="/c/Users/benoi/Documents/History vs Hype/library/by-topic"

process_category() {
  local category="$1"
  local pattern="$2"
  echo "Processing $category..."
  
  find "$DOWNLOADS" -maxdepth 1 -type f -name "*.pdf" | \
  grep -iE "$pattern" | \
  while IFS= read -r file; do
    base=$(basename "$file")
    first20=$(echo "$base" | cut -c1-20)
    
    if ls "$LIBRARY/$category/"*"$first20"* 2>/dev/null | grep -q .; then
      continue
    fi
    
    # Clean filename
    cleaned="$base"
    cleaned=$(echo "$cleaned" | sed 's/ - libgen\.li.*\.pdf/.pdf/')
    cleaned=$(echo "$cleaned" | sed 's/_compressed//')
    cleaned=$(echo "$cleaned" | sed 's/ (Z-Library)\.pdf/.pdf/')
    cleaned=$(echo "$cleaned" | sed 's/ -- ( WeLib\.org )\.pdf/.pdf/')
    cleaned=$(echo "$cleaned" | sed "s/ -- .*Anna's Archive.*\.pdf/.pdf/")
    cleaned=$(echo "$cleaned" | sed 's/__*/-/g' | sed 's/  */ /g')
    
    cp "$file" "$LIBRARY/$category/$cleaned"
    echo "✓ $cleaned"
  done
}

# African history
process_category "african-history" "(sahel|mali|niger|senegal|burkina|ivory|ghana|nigeria|cameroon|chad|sudan|ethiopia|somalia|kenya|tanzania|rwanda|burundi|congo|angola|mozambique|zimbabwe|africa.*postcolonial|decoloni|cfa.*franc|africa.*since)"

# Middle East
process_category "middle-east-history" "(ottoman|arab|persian|iran|iraq|syria|lebanon|palestine|israel|jordan|kuwait|saudi|yemen|mandate|sykes|picot|balfour|zion|fateful.*triangle|line.*sand)"

# Crusades-Christianity
process_category "crusades-christianity" "(crusad|templar|hospitaller|saladin|richard.*lion|jerusalem|acre|constantinople|byzantine|orthodox.*christian|jihad|holy.*land|pilgrimage|fulcher|usama)"

# Reference-Methodology
process_category "reference-methodology" "(historiography|historical.*method|holocaust|auschwitz|protocols|paranoid|apocalypse|non.*existent.*manuscript|great.*divergence|myth.*nations|master.*plan)"

echo "All categories processed!"
