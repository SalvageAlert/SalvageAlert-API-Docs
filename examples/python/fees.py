"""All-in cost of a win. Usage: python fees.py [source] [bid] [tax_region]"""
import sys
from urllib.parse import urlencode

from salvagealert import call

source = sys.argv[1] if len(sys.argv) > 1 else "iaai_ca"
bid = sys.argv[2] if len(sys.argv) > 2 else "7500"
params = {"source": source, "bid": bid}
if len(sys.argv) > 3:
    params["tax_region"] = sys.argv[3]

data, _ = call("GET", f"/fees/estimate?{urlencode(params)}")
cur = data["currency"]
print(f"Bid           {data['bid_amount']:>12,.2f} {cur}")
for line in data["fee_lines"]:
    print(f"  {line['label']:<22}{line['amount']:>10,.2f}")
for tax in data.get("tax_breakdown", []):
    print(f"  {tax['label']:<22}{tax['amount']:>10,.2f}  ({tax['rate'] * 100:g}% on {tax['basis']})")
print(f"Total all-in  {data['total_with_taxes']:>12,.2f} {cur}")
