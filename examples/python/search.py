"""Live search, paging until a page comes back empty.

Usage: python search.py [source] [make] [max_pages]
"""
import sys
from datetime import datetime, timezone

from salvagealert import call

source = sys.argv[1] if len(sys.argv) > 1 else "copart_us"
make = sys.argv[2] if len(sys.argv) > 2 else "TOYOTA"
max_pages = int(sys.argv[3]) if len(sys.argv) > 3 else 2

for page in range(1, max_pages + 1):
    data, headers = call("POST", "/lots/search", {
        "source": source, "makes": [make], "year_min": 2018, "page": page, "page_size": 25,
    })
    print(f"page {page}: {len(data['lots'])} lots (est. {data['total_estimate']}), "
          f"charged {headers.get('X-Credits-Charged')}, balance {headers.get('X-Credits-Balance')}")
    for lot in data["lots"]:
        ms = lot.get("auctionDateUTC")  # MILLISECONDS
        when = datetime.fromtimestamp(ms / 1000, timezone.utc).strftime("%Y-%m-%d %H:%M") if ms else "not assigned"
        print(f"  {lot['year']} {lot['make']} {lot['model']}  {lot.get('primaryDamage', '')}  sale {when}  {lot.get('detailUrl')}")
    if not data["lots"]:  # a short page is not the end; an empty one is
        break
