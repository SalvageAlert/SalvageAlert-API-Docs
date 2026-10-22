# Credits and rate limits

## Credits

Each `/v1` call debits a fixed number of credits. Balances can be fractional, because some calls cost 0.2.

| Cost | Endpoints |
|:-:|---|
| **0** | `/me`, `/usage`, `/api-keys*`, `/makes`, `/models`, `/yards`, `/inventory/sources`, `/auctions`, `/matches*`, every `/watches`, `/vin-watches` and `/webhooks` call, **and any cache hit on `/lots/search`** |
| **0.2** | `/vehicles/vin/{vin}`, `/vehicles/safety`, `/vehicles/fuel-economy`, `/fees/estimate`, `/fx` |
| **1** | `/lots/search`, `/lots/{source}/{lot_key}`, `/inventory`, `/inventory/{source}/{lot_key}` (0 on miss), `/vin/{vin}/history` (0 if unknown), `/vin/{vin}/title-check`, `/stats/market` |
| **1 per VIN found** | `/vin/batch` |
| **4** | `/lots/{source}/{lot_key}/images` |
| **8** | `/lots/{source}/{lot_key}/images.zip` |

Calls are **pre-authorized**. If your balance can't cover the worst case, you get `402 insufficient_credits` before anything runs, and nothing is charged.

### Getting credits

| | Credits | Requests/min |
|---|:-:|:-:|
| Free account | 50 on signup | 60 |
| Starter ($19.99/mo) | 500 / month | 120 |
| Unlimited ($39.99/mo) | 5,000 / month | 300 |
| Credit packs (one-off) | 1,000 / 5,000 / 20,000 | |

You can buy packs and change plans in the [dashboard](https://salvagealert.com/app/api). Current prices are on the [pricing page](https://salvagealert.com/pricing).

## Response headers

| Header | Example | Meaning |
|---|---|---|
| `X-Credits-Charged` | `1` | Cost of this call |
| `X-Credits-Balance` | `48.8` | Balance after this call |
| `X-Credits-Warning` | `low` | Under 10% of your grant |
| `X-RateLimit-Limit` | `60` | Requests per minute on your plan |
| `X-RateLimit-Remaining` | `57` | Left in the current window |
| `X-RateLimit-Reset` | `1761062460` | When the window resets (Unix seconds) |
| `Retry-After` | `12` | On a `429` only |

The rate limit is a sliding window per key. `GET /usage?days=30` (free, up to 90 days) breaks your calls down by day and by endpoint.

## Spending fewer credits

- Repeat identical `/lots/search` queries within the cache window. Cache hits are free.
- Mirror with `/inventory?updated_since=` instead of re-walking the whole catalogue.
- Use watches and webhooks instead of polling. Deliveries are free.
- Batch VIN lookups. VINs with no history cost nothing.
