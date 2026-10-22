"""Relisting trail for a VIN. Usage: python vin_history.py 1HGCM82633A004352"""
import sys

from salvagealert import SalvageAlertError, call

vin = sys.argv[1]
try:
    data, _ = call("GET", f"/vin/{vin}/history")
except SalvageAlertError as e:
    if e.status == 404:
        sys.exit("No auction history for this VIN (not billed).")
    raise

print(f"{data['count']} lot(s) for {data['vin']}")
for l in data["lots"]:
    print(f"  {l['source_label']} #{l['lot_key']}  {l.get('year')} {l.get('make')} {l.get('model')}  "
          f"{l.get('primary_damage') or ''}  {l.get('title_type') or ''}  {l.get('listing_url')}")
