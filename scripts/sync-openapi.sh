#!/usr/bin/env bash
# Pull the live spec, rebuild the Postman collection and the changelog.
set -euo pipefail
cd "$(dirname "$0")/.."
curl -fsS https://salvagealert.com/api/v1/openapi.json | python3 -m json.tool --indent 2 > openapi/openapi.json
python3 scripts/build-postman.py
python3 scripts/build-changelog.py
echo "spec version: $(python3 -c 'import json;print(json.load(open("openapi/openapi.json"))["info"]["version"])')"
