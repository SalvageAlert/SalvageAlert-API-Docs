# Sources

| ID | Marketplace | Currency | Notes |
|---|---|:-:|---|
| `copart_us` | Copart USA | USD | Full VINs. Make and year are applied at the source |
| `copart_ca` | Copart Canada | CAD | Full VINs |
| `copart_uk` | Copart UK | GBP | Full VINs, `ukCategory` (A/B/S/N), regions from `/yards` (`UK-ENG`…) |
| `copart_de` | Copart Germany | EUR | Full VINs, regions from `/yards` (`DE-BY`…). No photos endpoint |
| `iaai_us` | IAA USA | USD | Single-make filter applied at the source |
| `iaai_ca` | IAA Canada | CAD | Year, damage, title and price applied at the source. Regions `QC`, `ON`, `AB`, `BC`, `ATL`, `PRAIRIES` and branch ids |
| `iaai_uk` | IAA UK (SYNETIQ) | GBP | One national catalogue (`UK-ALL`). Single-lot reads through `/inventory/{source}/{lot_key}` |
| `govdeals_us` | GovDeals | USD | US government surplus. Often no title status. Single-lot reads through `/inventory` |

## What every source supports

| | Copart US/CA/UK | Copart DE | IAA US/CA | IAA UK | GovDeals |
|---|:-:|:-:|:-:|:-:|:-:|
| `/lots/search` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `/lots/{source}/{lot_key}` | ✅ | ✅ | ✅ | — | — |
| `/lots/…/images(.zip)` | ✅ | — | ✅ | — | — |
| `/inventory` and `/inventory/{source}/{lot_key}` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `/fees/estimate` | ✅ | ✅ | ✅ | ✅ | ✅ |

Live counts and freshness: `GET /inventory/sources`.

SalvageAlert is independent and isn't affiliated with IAA, Copart or GovDeals.
