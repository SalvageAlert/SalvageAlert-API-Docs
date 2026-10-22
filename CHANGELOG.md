# Changelog

Generated from `x-changelog` in [`openapi/openapi.json`](openapi/openapi.json). Newest first.
Additive changes bump the minor version; nothing in v1 is ever removed. See [conventions](docs/conventions.md#versioning).

## 1.7.0 — 2026-09-22

- New: GET, POST /api-keys and DELETE /api-keys/{id}. A key can be listed, minted and revoked one at a time over the API; /api-keys/rotate, which revokes every key, was the only key operation an integration had.
- /me states the contract: `plan`, `monthly_credits`, `max_watches` and `max_webhooks`. A 409 was the only way to learn a limit.
- /inventory/sources carries freshness per source: `newest_lot_at` and `newest_change_at` (Unix seconds) and a `stale` flag when nothing has changed for 48 hours, so a mirror can tell "no deltas" from "the crawler is down".
- New: GET /inventory/{source}/{lot_key} — one catalogue lot by identity, off the index, every source, 1 credit on a hit and nothing on a miss. The only per-lot read was the live /lots/{source}/{lot_key}, refused for iaai_uk and govdeals_us.
- New: GET and PATCH /matches/{id}. A match can be favorited, dismissed, annotated and priced over the API — max_bid_value, price_alert_value, notes, won and resale — which the web UI and the phones could do and an integration could not.
- /matches rows now carry the annotations and the fields the CSV had and the JSON dropped: max_bid_value, price_alert_value, notes, resale_price, pinned_at, lane, run_number, sale_event_status, uk_category, condition_text, odometer_value/unit, has_carfax, and listing_url. The row is typed as the Match schema; it was an untyped object.
- InventoryLot documents `damage_estimate_value` and `uk_category`, which /inventory has returned since 2026-09-04 and 2026-09-21 without a schema entry — a strict generated client dropped both.
- Webhooks: three new `lot.updated` kinds — `bid_changed` (a favorite's bid jumped inside the 48h approach window), `max_bid_crossed` (the live bid passed the ceiling set on a favorite) and `price_drop` (a Buy Now price fell to the target set on a favorite). Each was already a Telegram, push and email alert and reached no webhook; a subscriber to `lot.updated` receives them now.

## 1.6.0 — 2026-09-22

- New: /vin-watches — list, create, read, update, delete and run the per-VIN watches that send `vin_watch_match` deliveries. They were the one resource an API key could not touch; the two notes below that said so are superseded.
- New: GET /matches, the JSON pull path beside the CSV export, keyset-paged on `next_cursor`.
- New: GET /auctions, the IAA and Copart sale calendar the site and the apps already show, with each Copart sale's yard and our catalogue count there.
- New: POST /webhooks/{id}/deliveries/{deliveryId}/redeliver replays a failed or dead delivery.
- Webhooks: a reschedule is its own `kind`. A sale that had not run moving to another time (an hour or more) is delivered as `rescheduled`, with its own WebhookEventRescheduled schema; `relisted` stays for a sale that ran and a lot that came back.
- /inventory takes the catalog's remaining filters: buy_now, clean_title, title, runs_drives, has_keys, ending_within_hours, location, yard, state, and sale_terms.
- /vin/{vin}/history and /vin/batch: each lot carries `prior_sales`, the completed earlier auction cycles of that same lot number.

## 1.5.0 — 2026-09-21

- Webhooks: a relist is its own `kind`. A lot re-running under the same source and lot number was being delivered as `auction_result`, a shape that declares `result`, `before` and `after` required and carries none of them on a relist — so a receiver switching on `kind`, which is what the spec tells it to do, read `data.result` as undefined. It is `relisted` now, with its own WebhookEventRelisted schema.
- Webhooks: the SSRF refusal for an RFC1918 / loopback / 169.254 ADDRESS is `private_address`, which is what the code has always emitted. `private_host` fires only for a hostname (localhost, .local, .internal). The spec named `private_host` for both, so a client branching on it never fired for the case it was written for.
- /lots/{source}/{lot_key}/images and images.zip: copart_de is out of the `source` path enum. Both handlers refuse it and their own 400 descriptions said so — the enum offered an argument that always 400s.
- `Lot.keys` and `Lot.drives` are `nullable: true`, matching `Lot.starts` and the runtime: all three are `boolean | null`, and IAA UK and GovDeals never report any of them.
- Removed the "5 credits on a govdeals_us miss" clause from the three lot endpoints. It is unreachable: the single-lot route refuses govdeals before it queries, and neither image route serves it. The miss fee on those endpoints is 1 credit.
- A 429 now carries X-Credits-Charged and X-Credits-Balance, which this spec has always documented on it. A client tracking its balance was losing the reading at exactly the moment it was being throttled.
- Watch.active: corrected. Nothing on the server ever clears it — the VIN watches that stand themselves down once they find their vehicle are a separate resource (superseded: since 1.6.0 they are /vin-watches), so a `vin_watch_match` delivery does not come from a /watches filter set.
- /lots/{source}/{lot_key}/images: `limit` max and default are 50, not 100. The IAA enumeration walks a single prefix and stops at 50, so a higher value could never be honoured.
- images.zip: the archive holds up to 136 entries on IAA (100 photos plus up to 36 exterior-360 frames), and the `<stock>_<year>_<make>_<model>.zip` filename is IAA-only — the Copart path reads the gallery endpoint directly and never loads the lot, so it is `lot_<lot_key>.zip`.
- `WebhookEventVinWatchMatch.match_id` is not a column in /v1/matches.csv. Join a delivery to an export on (source, lot_key).
- `VinHistoryLot.vin` is nullable — IAA publishes a masked VIN on most lots and those rows carry null.
- The `Lot` schema declares the ~18 fields it was serializing and not documenting: ukCategory, isTimedAuction, the auction* identifiers, auctionBranch*, buyNowClosingDateUTC, stockBranchId, yardPhynumb, lane, runNumber, reserveStatus, hasCarfax, airbags, lossType and physicalCountry. Additive for anyone ignoring unknown keys; a generated model was missing a third of the lot.
- Every operation now declares the 429 it can return — only two of thirty-two did — plus the 404 on the five webhook-by-id operations, the 400 on /models, and the three 400s on POST /watches.
- /vehicles/vin/{vin}: the documented year range 1981-2100 is enforced. Out of range was reaching vPIC and coming back as a 502; it is a 400 `invalid_year`.

## 1.4.0 — 2026-09-17

- /inventory: `include_sold=true` now returns the ended lots our own staleness sweep had hidden — 307,896 across the seven sources, 223,298 of them Copart US. The gate could not tell our crawler's "we stopped seeing this" from a user hiding a lot inside their own account, and refused both; it now refuses only the second. Every one of those lots was already browsable on salvagealert.com/lots.
- /inventory: documented that a lot returned under `include_sold` may be ended with a NULL `sold_at` — a source can stop listing a lot without a sale we can record — so read a past `sale_date_utc` as ended too.

## 1.3.0 — 2026-09-04

- Added `x-conventions`: the timestamp units and the boolean representation, stated once at the top of the spec instead of only per-field.
- Documented `Lot.auctionDateUTC` as epoch MILLISECONDS. It had no unit at all, and every other integer timestamp on the camelCase Lot is seconds — so it read as seconds and is not.
- Documented that every timestamp inside the /matches.csv file is an ISO-8601 UTC string, including its `sale_date_utc` column.
- Documented the boolean/integer split on InventoryLot: `has_keys`, `drives` and `starts` are 0/1 integers while `make_offer`, `wholesale_only`, `former_rental` and `offsite` are booleans. Frozen for v1; all seven become booleans in v2.
- Added `x-deprecation-policy`: nothing is removed from v1, 90 days marked `deprecated` before a new major, 12 months of parallel support after it.
- Watches: added PATCH /watches/{id} `{active?, label?}`. Pausing a watch no longer requires DELETE + POST, so the watch id survives it.
- X-RateLimit-Remaining and X-RateLimit-Reset now describe a continuously refilling allowance: the limiter is a token bucket that survives a deploy, not a window that empties on restart. Retry-After is unchanged and is still the number to obey on a 429.

## 1.2.0 — 2026-09-04

- /inventory: added `updated_since` and `cursor` for stable keyset pagination and incremental sync; `page` is now capped at 500 and is documented as unsafe for bulk mirroring.
- /inventory: lots now carry `gallery_urls` (the full mirrored photo set, free) alongside `image_url`.
- Webhooks: every `data` payload now carries a `kind` discriminator, and all five payload shapes are documented as WebhookEvent* schemas.
- Webhooks: documented the auto-disable threshold, the retry/backoff schedule, and `format` — including that discord/slack deliveries are NOT HMAC-signed.
- Webhooks: the owner is now emailed when a subscription is auto-disabled.
- /webhooks/{id}/deliveries: `latency_ms` renamed to `queue_delay_ms` — it never measured the receiver, only queue wait.
- /vin/batch: VINs that return no lots are no longer billed, matching /vin/{vin}/history. Added `looked_up`.
- /yards: response is now a real oneOf per source instead of an untyped object.
- /api-keys/rotate: documented as account-wide and destructive; the owner is now emailed on rotation.
- Documented every error code, the X-Salvagealert-Warning header, /me's 404, and the read-only nature of Watch.active.

## 1.1.0 — 2026-09-02

- /inventory: lots gained acv, title_state, origin_country, sale_event_status, sale_light, autograde, make_offer, wholesale_only, former_rental, offsite/offsite_location, lane, run_number, airbags_status, loss_type, has_keys, drives, starts, trim, and later high_prebid_value, buy_now_value and sold_at.

## 1.0.0 — 2026-01-01

- Initial public contract.
