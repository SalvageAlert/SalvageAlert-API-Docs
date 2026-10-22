# Errors

Every non-2xx response from `/v1` has this shape:

```json
{
  "error": { "code": "rate_limit", "message": "…" },
  "request_id": "6f1c2a7e-3b0d-4d7e-9a51-2f7f0c1b9e44"
}
```

**Switch on `error.code`.** `message` is prose and its wording may change. `request_id` is also sent as `X-Request-Id`, so quote it when you contact support.

## Authentication (401)

| Code | Meaning | What to do |
|---|---|---|
| `missing_credentials` | No `Authorization` header, or it's malformed | Send `Authorization: Bearer sa_live_…` |
| `invalid_credentials` | The key is unknown or revoked | Use a current key |
| `account_inactive` | The account behind the key isn't active | Contact support |
| `key_revoked_missing_project_url` | The key was swept because no project URL was set | Set the URL at `/app/api`, then rotate |

## Access (403)

| Code | Meaning |
|---|---|
| `api_disabled` | API access isn't enabled for this account |
| `plan_gate` | Your plan doesn't include this feature (for example, VIN watches) |

## Quota (402 / 429)

| Code | Meaning | What to do |
|---|---|---|
| `insufficient_credits` | The call was pre-authorized against your balance and refused | Top up or upgrade. The body includes `balance`, `credits_url`, `plan_url` and `hint` |
| `rate_limit` | You're over your per-minute allowance | Wait `Retry-After` seconds |
| `too_many_watches` | The VIN watch cap (200) was reached | Delete one first |

## Request shape (400, never billed)

| Code | Where |
|---|---|
| `invalid_source`, `unsupported_source` | Any endpoint that takes a source |
| `invalid_location` (+ `unknown_locations`) | `/lots/search` |
| `invalid_title_type` | `/lots/search` |
| `invalid_sort`, `invalid_cursor`, `invalid_updated_since` | `/inventory` |
| `invalid_json`, `missing_vins`, `no_valid_vins`, `too_many_vins` | `/vin/batch` (max 50) |
| `invalid_make_id` | `/models` |
| `invalid_year` | `/vehicles/vin/{vin}` (1981 to 2100) |
| `invalid_bid`, `invalid_tax_region` | `/fees/estimate` |
| `watch_filters_too_large`, `invalid_filters`, `invalid_body`, `invalid_active`, `invalid_label` | `/watches` |
| `invalid_url`, `credentials_in_url`, `private_address`, `private_host`, `dns_unresolvable`, `non_https`, `invalid_events` | `/webhooks` |

## Not found (404)

| Code | Billed? |
|---|---|
| `not_found` (a webhook, watch or match that isn't yours or doesn't exist) | No |
| `lot_not_found` | A live query still ran, so a **reduced miss fee** is charged |
| `no_photos`, `no_anchor_image` | The miss fee |
| `no_data` (`/stats/market`) | No |
| Unknown VIN on `/vin/{vin}/history` | No |

## Conflict (409)

`duplicate`: you already have a VIN watch for that VIN.

## Upstream and server (5xx)

| Code | Meaning |
|---|---|
| `upstream_unavailable` (502) | NHTSA, the FX source or another third party failed. Retry with back-off |
| `internal_error` (500) | Our fault. Never billed. Report it with the `request_id` |
| `no_photos_fetched` (500) | Every photo download failed. Free; retry |

## A retry policy that works

```text
429                -> sleep Retry-After, retry
500 / 502 / 503    -> exponential back-off (1s, 2s, 4s, … max 60s), max 5 tries
400 / 401 / 403    -> don't retry; fix the request
402                -> don't retry; top up
```
