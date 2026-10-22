#!/usr/bin/env bash
# All-in cost of a CA$7,500 win at IAA Canada in Quebec. 0.2 credits.
set -euo pipefail
curl -sS "https://salvagealert.com/api/v1/fees/estimate?source=iaai_ca&bid=7500&tax_region=QC" \
  -H "Authorization: Bearer ${SALVAGEALERT_KEY:?set SALVAGEALERT_KEY}"
echo
