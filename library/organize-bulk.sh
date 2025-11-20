#!/bin/bash
# Bulk process remaining books

DOWNLOADS="/c/Users/benoi/Downloads"
LIBRARY="/c/Users/benoi/Documents/History vs Hype/library/by-topic"
count=0

find "$DOWNLOADS" -maxdepth 1 -type f -name "*.pdf" | \
grep -vE "\.(download|tmp|crdownload)$" | \
while IFS= read -r file; do
  base=$(basename "$file")
  first20=$(echo "$base" | cut -c1-20)
  
  # Skip academic paper codes
  if [[ "$base" =~ ^[0-9]+\.pdf$ ]] || [[ "$base" =~ ^10\.[0-9]+.*\.pdf$ ]] || [[ "$base" =~ ^[A-Z]_[0-9]+.*\.pdf$ ]]; then
    continue
  fi
  
  # Check all categories
  skip=false
  for cat in territorial-disputes colonialism-slavery african-history middle-east-history crusades-christianity reference-methodology general-history; do
    if ls "$LIBRARY/$cat/"*"$first20"* 2>/dev/null | grep -q .; then
      skip=true
      break
    fi
  done
  
  if [ "$skip" = true ]; then
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
  
  cp "$file" "$LIBRARY/general-history/$cleaned" 2>/dev/null
  ((count++))
  
  if ((count % 20 == 0)); then
    echo "Processed $count books..."
  fi
  
  # Process in batches of 150
  if ((count >= 150)); then
    echo "Batch complete: $count books processed"
    break
  fi
done

echo "Total: $count books processed"
