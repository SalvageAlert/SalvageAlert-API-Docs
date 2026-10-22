#!/usr/bin/env bash
# Every auction lot a VIN has appeared as. 1 credit, 0 if the VIN is unknown.
# Usage: ./vin-history.sh 1HGCM82633A004352
set -euo pipefail
VIN="${1:?usage: $0 <17-char VIN>}"
curl -sS "https://salvagealert.com/api/v1/vin/$VIN/history" \
  -H "Authorization: Bearer ${SALVAGEALERT_KEY:?set SALVAGEALERT_KEY}"
echo
