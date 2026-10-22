# Searching lots

`POST /lots/search` queries **one source** live and returns the normalized camelCase `Lot` object.

- **Cost:** 1 credit. A cache hit costs 0, and a cache hit is served even at a 0 balance.
- **Paging:** `page` (from 1) and `page_size` (1 to 100, default 25).

## Request body

| Field | Type | Notes |
|---|---|---|
| `source` | string, **required** | One of `copart_us`, `copart_ca`, `copart_uk`, `copart_de`, `iaai_us`, `iaai_ca`, `iaai_uk`, `govdeals_us` |
| `keyword` | string | Every word must appear in make, model or brand (AND) |
| `makes` / `models` | string[] | e.g. `["HONDA"]`, `["CIVIC"]`. Use [`/makes`](#reference-catalogues) and `/models` |
| `year_min` / `year_max` | integer | |
| `locations` | string[] | ISO codes (`US-FL`, `CA-QC`), OR-ed. See below |
| `title_types` | string[] | `clean`, `salvage`, `rebuilt`, `parts` |
| `buy_now_only` | boolean | |
| `min_buy_now` / `max_buy_now` | number | Source currency |
| `min_high_bid` / `max_high_bid` | number | Source currency |
| `min_odometer_km` / `max_odometer_km` | number | Always kilometres |
| `damage_keywords` | string[] | Matched against the damage fields |
| `page` / `page_size` | integer | |

### Locations

- US states and Canadian provinces: `US-FL`, `US-TX`, `CA-QC`, `CA-SK`…
- `iaai_ca` also accepts its regions (`QC`, `ON`, `AB`, `BC`, `ATL`, `PRAIRIES`) and numeric branch ids from `/yards`.
- `copart_uk` / `copart_de` take region codes from `/yards` (`UK-ENG`, `DE-BY`).
- `iaai_uk` is one national catalogue and accepts only `UK-ALL`.

If the source can't resolve a token, the request is **refused** with `400 invalid_location` and the token is listed in `unknown_locations`. We never silently widen the search.

## How filtering works

Each source applies the filters its own site supports, and then every page goes through the same local gate the SalvageAlert app uses. A filter the source can't apply still holds. Lots it removes are counted in `filtered_out`.

As a result, **a page can be short, or even empty, while `total_estimate` is large.** `total_estimate` is the source's count for the part of the query the source applied. Keep requesting the next `page` until a page returns no lots. Don't stop by comparing lots seen to `total_estimate`.

## Response

```json
{
  "source": "iaai_ca",
  "page": 1,
  "page_size": 25,
  "total_estimate": 318,
  "filtered_out": 2,
  "cached": false,
  "lots": [ { "stockNum": "…", "year": 2021, "make": "HONDA", "model": "CIVIC", "auctionDateUTC": 1765238400000, "…": "…" } ]
}
```

### Sale status from a `Lot`

| `auctionDateUTC` | `isAuctionClosed` | Status |
|---|---|---|
| `null` | `false` | Not yet assigned to a sale |
| in the future | `false` | Upcoming |
| in the past | any | Ended |
| any | `true` | Ended (sold on approval, awaiting relist) |

`auctionDateUTC` is in **milliseconds**.

## One lot

`GET /lots/{source}/{lot_key}` fetches one live lot by stock number for 1 credit. A lot that was withdrawn, or sold and removed, no longer exists at the source and answers `404 lot_not_found`. Use `/inventory/{source}/{lot_key}` to read our archived copy. `iaai_uk` and `govdeals_us` are only served through `/inventory/{source}/{lot_key}`.

## Photos

- `GET /lots/{source}/{lot_key}/images` returns every gallery URL (4 credits).
- `GET /lots/{source}/{lot_key}/images.zip` returns all photos as a ZIP (8 credits).

Both are supported on `iaai_us`, `iaai_ca`, `copart_us`, `copart_ca` and `copart_uk`.

## Reference catalogues

All of these are free:

- `GET /makes` lists makes.
- `GET /models?make_id=…` lists the models for a make.
- `GET /yards?source=…` lists yards and branches, with the codes `locations` accepts.
