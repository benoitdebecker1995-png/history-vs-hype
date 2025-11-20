#!/bin/bash
# Batch process books from Downloads to library

DOWNLOADS="/c/Users/benoi/Downloads"
LIBRARY="/c/Users/benoi/Documents/History vs Hype/library/by-topic"

# Counter
count=0

# Process territorial disputes books
echo "Processing territorial disputes books..."
find "$DOWNLOADS" -maxdepth 1 -type f -name "*.pdf" | \
grep -iE "(belize|guatemala|kashmir|cyprus|essequibo|guyana|venezuela|nagorno|karabakh|armen|azerbaijan|kosovo)" | \
while IFS= read -r file; do
  base=$(basename "$file")

  # Skip if already processed (simple check)
  if ls "$LIBRARY/territorial-disputes/"*"$(echo "$base" | cut -c1-20)"* 2>/dev/null | grep -q .; then
    continue
  fi

  # Simple filename cleaning - extract key parts
  if [[ "$base" =~ libgen\.li ]]; then
    # libgen format: "Author - Title (Year, Publisher) - libgen.li.pdf"
    cleaned=$(echo "$base" | sed 's/ - libgen\.li.*\.pdf/.pdf/' | sed 's/_compressed//')
  elif [[ "$base" =~ Z-Library ]]; then
    # Z-Library format
    cleaned=$(echo "$base" | sed 's/ (Z-Library)\.pdf/.pdf/')
  elif [[ "$base" =~ WeLib ]]; then
    # WeLib format
    cleaned=$(echo "$base" | sed 's/ -- ( WeLib\.org )\.pdf/.pdf/' | sed 's/ -- /- - /')
  elif [[ "$base" =~ "Anna's Archive" ]]; then
    # Anna's Archive - take first two parts only
    cleaned=$(echo "$base" | sed "s/ -- .*Anna's Archive.*\.pdf/.pdf/")
  else
    cleaned="$base"
  fi

  # Further simplify
  cleaned=$(echo "$cleaned" | sed 's/__*/-/g' | sed 's/  */ /g')

  cp "$file" "$LIBRARY/territorial-disputes/$cleaned"
  ((count++))
  echo "✓ $cleaned"

  # Limit to avoid overwhelming
  if [[ $count -ge 50 ]]; then
    echo "Processed 50 books, stopping for review..."
    break
  fi
done

echo "Processed $count territorial disputes books"
