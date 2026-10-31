#!/bin/sh
# Build the archive website: Hugo renders the pages from the Markdown and the
# catalogue, then Pagefind builds the static search index.
#
#   scripts/build_site.sh [output-dir]
#
# Uses `hugo` and `pagefind` from PATH, or the HUGO / PAGEFIND variables.
# Versions used and tested: Hugo 0.140.2, Pagefind 1.3.0.
set -eu
ROOT=$(cd "$(dirname "$0")/.." && pwd)
OUT=${1:-"$ROOT/build/site"}
HUGO=${HUGO:-hugo}
PAGEFIND=${PAGEFIND:-pagefind}

# Start from an empty folder so no page from an earlier build survives.
case "$OUT" in
  ""|/|"$ROOT"|"$ROOT/") echo "refusing to use $OUT as output" >&2; exit 1 ;;
esac
rm -rf "$OUT"
"$HUGO" --source "$ROOT/site" --destination "$OUT" --minify --panicOnWarning
"$PAGEFIND" --site "$OUT" --output-subdir pagefind
echo "site built in $OUT"
