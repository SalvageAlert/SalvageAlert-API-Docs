"""Mirror the archived catalogue with the keyset cursor, then pull deltas.

State goes in ./mirror-state.json and rows in ./lots.ndjson. A real mirror
would upsert into a database on (source, lot_key).

Usage: python mirror_inventory.py [source] [max_pages]
"""
import json
import os
import sys
from urllib.parse import urlencode

from salvagealert import call

source = sys.argv[1] if len(sys.argv) > 1 else "copart_de"
max_pages = int(sys.argv[2]) if len(sys.argv) > 2 else 5
STATE = "mirror-state.json"
state = json.load(open(STATE)) if os.path.exists(STATE) else {"hwm": None, "cursor": ""}

pages = 0
while True:
    params = {"source": source, "page_size": 100, "cursor": state.get("cursor") or ""}
    if state.get("hwm"):
        params["updated_since"] = state["hwm"]
    data, headers = call("GET", f"/inventory?{urlencode(params)}")

    with open("lots.ndjson", "a") as out:
        for lot in data["lots"]:
            out.write(json.dumps(lot) + "\n")
            state["next_hwm"] = max(state.get("next_hwm") or 0, lot.get("archived_at") or 0)  # SECONDS
    state["cursor"] = data.get("next_cursor")
    print(f"+{len(data['lots'])} lots, balance {headers.get('X-Credits-Balance')}")

    if not data.get("next_cursor"):
        state["hwm"], state["cursor"] = state.get("next_hwm") or state.get("hwm"), ""
        json.dump(state, open(STATE, "w"), indent=2)
        print(f"up to date; next run uses updated_since={state['hwm']}")
        break
    json.dump(state, open(STATE, "w"), indent=2)
    pages += 1
    if pages >= max_pages:
        print("page budget reached; rerun to resume")
        break
