# Inventory and mirroring

`GET /inventory` pages through the archived catalogue behind [salvagealert.com/lots](https://salvagealert.com/lots): **1.5M+ de-duplicated lots** from every source, continuously crawled. It reads our index, never the live source, and costs **1 credit per call**.

## Two pagination modes

| Mode | Select it with | Use it for |
|---|---|---|
| **Offset** | `page`, `sort` | Showing a page a person will read. Capped at page 500 |
| **Keyset** | `cursor` and/or `updated_since` | Mirroring. Safe while the catalogue changes underneath you |

The crawlers write to the catalogue all the time, so an offset walk skips and duplicates rows as they shift. **Never mirror with `page`.**

### Keyset walk

Results are ordered by `(archived_at, source, lot_key)`. Pass back the `next_cursor` from each response, and stop when it's `null`. If a lot changes mid-walk, it moves to the end of the ordering, so you see it again instead of missing it.

### Incremental sync

`updated_since` (Unix **seconds**, compared with `archived_at`) returns only the lots that changed since then: bid, sale date, photo, identity or sale. Combine it with `cursor` to page through a large delta. **Upsert on `(source, lot_key)`.**

```text
first run:   GET /inventory?cursor=   ... until next_cursor == null
             remember max(archived_at) as HWM
every hour:  GET /inventory?updated_since=HWM&cursor= ... upsert, advance HWM
```

`include_sold=true` adds ended lots, and a delta then also carries the lots that sold, with `sold_at`. Lots deleted from the catalogue aren't reported, so treat a lot you haven't seen for a while as stale.

See [`examples/node/mirror-inventory.mjs`](../examples/node/mirror-inventory.mjs) and [`examples/python/mirror_inventory.py`](../examples/python/mirror_inventory.py).

## Filters

`source`, `q`, `make`, `model`, `year_min`, `year_max`, `max_odometer_km`, `price_min_usd`, `price_max_usd`, `damage`, `body`, `fuel`, `drive`, `transmission`, `seller`, `sale_terms`, `buy_now`, `clean_title`, `title`, `runs_drives`, `has_keys`, `ending_within_hours` (24/48/72/168), `location`, `yard`, `state`, `repair_pct_max` (25/50/75/100), `include_sold`.

Offset-mode `sort`: `ending`, `recent`, `highestBid`, `lowestBid`, `newestYear`, `oldestYear`, `makeAZ`, `lowestMileage`, `bestValue`.

## Freshness

`GET /inventory/sources` (free) returns the live count for each source, plus `newest_lot_at`, `newest_change_at` and `stale`. `stale` is true when nothing from that source has changed for 48 hours. Use it to tell "no changes" apart from "the feed is down".

## One archived lot

`GET /inventory/{source}/{lot_key}` reads one lot by identity, from any source. It costs 1 credit on a hit and nothing on a miss.

## Shape

Inventory rows are the **snake_case** `InventoryLot`. Watch the [boolean split](conventions.md#booleans): `has_keys`, `drives` and `starts` are integers.
