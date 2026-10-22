#!/usr/bin/env bash
# Register a webhook, save a watch, then send a test delivery. All free.
# Usage: ./watch.sh https://example.com/hooks/salvagealert
set -euo pipefail
URL="${1:?usage: $0 <https webhook url>}"
API=https://salvagealert.com/api/v1
AUTH="Authorization: Bearer ${SALVAGEALERT_KEY:?set SALVAGEALERT_KEY}"

echo "== webhook (store the secret: it is shown once)"
HOOK=$(curl -sS -X POST "$API/webhooks" -H "$AUTH" -H "Content-Type: application/json" \
  -d "{\"url\":\"$URL\",\"events\":[\"lot.matched\",\"lot.updated\",\"lot.sold\"],\"format\":\"generic\",\"label\":\"example\"}")
echo "$HOOK"
HOOK_ID=$(printf '%s' "$HOOK" | python3 -c 'import json,sys; print(json.load(sys.stdin)["id"])')

echo "== watch"
curl -sS -X POST "$API/watches" -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"source":"copart_us","label":"Tacoma 2018+","filters":{"makes":["TOYOTA"],"models":["TACOMA"],"year_min":2018}}'
echo

echo "== test delivery"
curl -sS -X POST "$API/webhooks/$HOOK_ID/test" -H "$AUTH"
echo
