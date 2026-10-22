#!/usr/bin/env bash
# Free call: your plan, balance and rate limit.
set -euo pipefail
curl -sS https://salvagealert.com/api/v1/me \
  -H "Authorization: Bearer ${SALVAGEALERT_KEY:?set SALVAGEALERT_KEY}"
echo
