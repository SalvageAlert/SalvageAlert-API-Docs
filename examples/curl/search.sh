#!/usr/bin/env bash
# Live search on one source. 1 credit, or 0 on a cache hit.
# Usage: ./search.sh [source] [make]
set -euo pipefail
SOURCE="${1:-copart_us}"
MAKE="${2:-TOYOTA}"
curl -sS -X POST https://salvagealert.com/api/v1/lots/search \
  -H "Authorization: Bearer ${SALVAGEALERT_KEY:?set SALVAGEALERT_KEY}" \
  -H "Content-Type: application/json" \
  -D /dev/stderr \
  -d "{\"source\":\"$SOURCE\",\"makes\":[\"$MAKE\"],\"year_min\":2018,\"page_size\":10}"
echo
