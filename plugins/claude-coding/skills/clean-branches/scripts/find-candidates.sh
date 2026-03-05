#!/usr/bin/env bash
# find-candidates.sh — Find merged and stale git branches
# Usage: find-candidates.sh [pattern]
# Output: Two labeled sections (MERGED / STALE), one branch per line.
#         Empty section = no candidates of that type.
# Exit 0 always; downstream decides what to do with empty output.

set -euo pipefail

PATTERN="${1:-}"

# Detect main branch name (prefer main, fall back to master)
if git rev-parse --verify main >/dev/null 2>&1; then
  BASE="main"
elif git rev-parse --verify master >/dev/null 2>&1; then
  BASE="master"
else
  echo "ERROR: no main or master branch found" >&2
  exit 1
fi

# --- Merged branches ---
echo "=== MERGED ==="
MERGED=$(git branch --merged "$BASE" 2>/dev/null | grep -v "^\*" | sed 's/^[ ]*//' | grep -vE '^(main|master|develop)$' || true)
if [ -n "$PATTERN" ]; then
  MERGED=$(echo "$MERGED" | grep "$PATTERN" || true)
fi
echo "$MERGED"

# --- Stale branches (no commits in 30+ days) ---
# Unix timestamps used for accurate threshold — git relative dates miss edge cases
echo "=== STALE ==="
CUTOFF=$(python3 -c "import time; print(int(time.time()) - 30*86400)")
git for-each-ref --sort=-committerdate \
  --format='%(refname:short) %(committerdate:unix) %(committerdate:relative)' \
  refs/heads/ | while read -r branch ts reldate; do
  # Skip protected branches
  case "$branch" in main|master|develop|release/*) continue ;; esac
  # Apply pattern filter if provided
  if [ -n "$PATTERN" ] && [[ "$branch" != $PATTERN ]]; then
    continue
  fi
  if (( ts < CUTOFF )); then
    echo "$branch ($reldate)"
  fi
done
