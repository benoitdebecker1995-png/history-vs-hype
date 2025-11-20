#!/bin/bash
# Process colonialism-slavery books

DOWNLOADS="/c/Users/benoi/Downloads"
LIBRARY="/c/Users/benoi/Documents/History vs Hype/library/by-topic"

echo "Processing colonialism-slavery books..."
find "$DOWNLOADS" -maxdepth 1 -type f -name "*.pdf" | \
grep -iE "(slave|slavery|abolition|colonial|empire|imperial|plantation|conquest|encomienda|atlantic.*trade|born.*die|disease.*conquest)" | \
while IFS= read -r file; do
  base=$(basename "$file")

  # Skip if similar file exists
  first20=$(echo "$base" | cut -c1-20)
  if ls "$LIBRARY/colonialism-slavery/"*"$first20"* 2>/dev/null | grep -q .; then
    continue
  fi

  # Clean filename
  if [[ "$base" =~ libgen\.li ]]; then
    cleaned=$(echo "$base" | sed 's/ - libgen\.li.*\.pdf/.pdf/' | sed 's/_compressed//')
  elif [[ "$base" =~ Z-Library ]]; then
    cleaned=$(echo "$base" | sed 's/ (Z-Library)\.pdf/.pdf/')
  elif [[ "$base" =~ WeLib ]]; then
    cleaned=$(echo "$base" | sed 's/ -- ( WeLib\.org )\.pdf/.pdf/' | sed 's/ -- / - /')
  elif [[ "$base" =~ "Anna's Archive" ]]; then
    cleaned=$(echo "$base" | sed "s/ -- .*Anna's Archive.*\.pdf/.pdf/")
  else
    cleaned="$base"
  fi

  cleaned=$(echo "$cleaned" | sed 's/__*/-/g' | sed 's/  */ /g')

  cp "$file" "$LIBRARY/colonialism-slavery/$cleaned"
  echo "✓ $cleaned"
done

echo "Done!"
