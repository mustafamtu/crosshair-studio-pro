#!/usr/bin/env bash

# watch_review.sh – monitor review.md for new entries and apply simple code fixes.
# Assumes entries in format: <file_path>:<line_number> – <description>
# Supports description pattern: "replace \"OLD\" with \"NEW\""
# Stores last processed line count in .claude/watch_state.txt

STATE_FILE="$(dirname "$0")/.claude/watch_state.txt"
REVIEW_FILE="$(dirname "$0")/review.md"

# Initialize state file if missing
echo 0 > "$STATE_FILE"

while true; do
  # Get total line count of review file
  TOTAL_LINES=$(wc -l < "$REVIEW_FILE")
  LAST_PROCESSED=$(cat "$STATE_FILE")

  if (( TOTAL_LINES > LAST_PROCESSED )); then
    # Process new lines
    NEW_LINES=$((TOTAL_LINES - LAST_PROCESSED))
    tail -n $NEW_LINES "$REVIEW_FILE" | while IFS= read -r line; do
      # Trim leading/trailing whitespace
      line=$(echo "$line" | sed 's/^\s*//;s/\s*$//')
      # Skip empty or comment lines
      [[ -z "$line" ]] && continue
      # Parse entry
      if [[ "$line" =~ ^([^:]+):([0-9]+)\s*–\s*(.*)$ ]]; then
        FILE_PATH="${BASH_REMATCH[1]}"
        LINE_NUM=${BASH_REMATCH[2]}
        DESC="${BASH_REMATCH[3]}"
        # Handle replace directive
        if [[ "$DESC" =~ replace\s+\"([^\"]+)\"\s+with\s+\"([^\"]+)\" ]]; then
          OLD="${BASH_REMATCH[1]}"
          NEW="${BASH_REMATCH[2]}"
          # Use sed to replace only on the specific line
          sed -i "${LINE_NUM}s/${OLD}/${NEW}/" "$FILE_PATH"
          echo "Replaced \"$OLD\" with \"$NEW\" in $FILE_PATH at line $LINE_NUM"
        else
          echo "Unsupported description: $DESC"
        fi
      else
        echo "Malformed entry: $line"
      fi
    done
    # Update state file
    echo "$TOTAL_LINES" > "$STATE_FILE"
  fi

  # Sleep 15 seconds before next check
  sleep 15
done
