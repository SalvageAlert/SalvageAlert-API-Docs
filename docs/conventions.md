# Field conventions

These four rules are worth reading before you write a deserializer.

## Timestamps

| Representation | Fields |
|---|---|
| Unix **seconds** (the default) | every `*_at`, `archived_at`, `last_seen_utc`, `first_seen_utc`, `sold_at`, `created_at`, `enrolled_at`, and the `since` / `until` / `updated_since` params |
| Unix **milliseconds** | exactly two: `sale_date_utc` (snake_case objects) and `auctionDateUTC` (camelCase `Lot`) |
| ISO-8601 UTC strings | every timestamp inside `/matches.csv` |
| `YYYY-MM-DD` | `Usage.per_day[].day`, `FxRates.date` |

Passing a millisecond field to a constructor that expects seconds lands you in the year 57,000. Passing a seconds field to one that expects milliseconds lands you in 1970. Both fail silently. **Divide by 1000 by field name; never guess by magnitude.**

```js
const saleDate = lot.auctionDateUTC == null ? null : new Date(lot.auctionDateUTC);   // ms
const archived = new Date(row.archived_at * 1000);                                   // s
```

## Booleans

On `InventoryLot`, two forms sit side by side:

- `make_offer`, `wholesale_only`, `former_rental` and `offsite` are JSON `true` / `false` / `null`.
- `has_keys`, `drives` and `starts` are **integers** `0` / `1` / `null`.

`null` means the source didn't say. It doesn't mean `false`. These types are frozen for v1, and v2 will make all seven booleans.

## Casing

- `/lots/search` and `/lots/{source}/{lot_key}` return the raw normalized `Lot`, in **camelCase** (`stockNum`, `odometerReading`, `primaryDamage`, `imageUrl`, `auctionDateUTC`).
- Every other endpoint returns **snake_case**.

## Money

- `current_bid` and `buy_now` are **display strings** and can contain symbols and separators.
- `buy_now_value`, `high_prebid_value`, `est_retail_value` and `acv` are numbers. Sort and compare on those.
- Each lot is in its source's currency (USD, CAD, GBP or EUR). Only `/stats/market` normalizes to USD.

## Versioning

- **Additive changes** (new fields, optional params, endpoints) ship without notice and bump the minor version. **Your client must ignore unknown fields.**
- **Breaking changes** never happen inside v1. They go to v2, on its own path, and both versions are served in parallel.
- Fields bound for removal are marked `deprecated: true` in the spec first.
- `x-changelog` in [`openapi.json`](../openapi/openapi.json) lists every version, newest first.
