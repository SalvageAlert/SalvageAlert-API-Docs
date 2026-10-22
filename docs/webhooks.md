# Webhooks

Instead of polling `/lots/search`, save your filters as a **watch** and register a **webhook**. When a lot matches, we POST the event to you.

```
watch (what to look for)  ──▶  event  ──▶  webhook (where to send it)
```

Watches, VIN watches and webhooks are all free to create and receive.

## 1. Register an endpoint

```bash
curl -X POST https://salvagealert.com/api/v1/webhooks \
  -H "Authorization: Bearer $SALVAGEALERT_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com/hooks/salvagealert","events":["lot.matched","lot.updated","lot.sold"],"label":"prod","format":"generic"}'
```

The response contains `secret`, **which is only shown once**. Store it, because you'll need it to verify signatures.

The URL must be absolute `https`. Private, loopback and cloud-metadata addresses, unresolvable hosts and URLs that contain `user:pass@` are refused. We check this when you create the webhook **and again on every delivery**.

## 2. Create a watch

```bash
curl -X POST https://salvagealert.com/api/v1/watches \
  -H "Authorization: Bearer $SALVAGEALERT_KEY" \
  -H "Content-Type: application/json" \
  -d '{"source":"copart_us","label":"Tacomas 2018+","filters":{"makes":["TOYOTA"],"models":["TACOMA"],"year_min":2018}}'
```

- `filters` takes the same shape as `/lots/search` and is capped at 4 KB.
- `source` and `filters` can't be changed after creation. To change what a watch looks for, create a new watch.
- To pause a watch, send `PATCH /watches/{id}` with `{"active": false}`. The id is kept.

## 3. Test it

`POST /webhooks/{id}/test` sends a synchronous `webhook.test` delivery with `data.kind = "test"`. It's limited to 6 per minute per webhook.

## Delivery format (`format: generic`)

```http
POST /hooks/salvagealert HTTP/1.1
Content-Type: application/json
User-Agent: SalvageAlert-Webhook/1.0
X-Salvagealert-Event: lot.matched
X-Salvagealert-Delivery-Id: 918273
X-Salvagealert-Signature: t=1761062400,v1=5f2b9c0e…

{ "event": "lot.matched", "created_at": 1761062400, "data": { "kind": "watch_match", "source": "copart_us", "watch_id": "…", "lot": { … } } }
```

`created_at` is Unix **seconds**. `data.lot` is the full camelCase `Lot`.

### Events and `data.kind`

**Switch on `data.kind`.** Don't infer the event type from which fields are present.

| `event` | `data.kind` | When it fires |
|---|---|---|
| `lot.matched` | `watch_match` | A watch matched a newly crawled lot |
| `lot.matched` | `vin_watch_match` | A VIN watch found its vehicle (carries `vin_watch_id`) |
| `lot.updated` | `closing_soon` | Bid movement on a tracked lot just before its sale |
| `lot.updated` | `auction_result` | The sale concluded: `result` is `sold`/`unsold`, plus `final_price` |
| `lot.updated` | `relisted` | Same lot number, new sale date after the sale ran |
| `lot.updated` | `rescheduled` | A sale that hadn't run yet moved by an hour or more |
| `lot.updated` | `bid_changed` | The bid on a favorited lot jumped within 48 hours of the sale |
| `lot.updated` | `max_bid_crossed` | The live bid passed the ceiling you set |
| `lot.updated` | `price_drop` | A Buy Now price fell to your target |
| `lot.sold` | `delisted` | The lot left its source feed. "Sold" is our inference, not a confirmed sale |
| `webhook.test` | `test` | A test fire |

## Verifying signatures

The header is `t=<unix seconds>,v1=<hex>`, where `v1 = HMAC-SHA256(secret, "<t>.<raw body>")`.

1. Read the **raw** body bytes before any JSON parsing. A re-serialized body won't match.
2. Recompute the HMAC and compare it in constant time.
3. Reject a `t` more than about 5 minutes away from your clock, to block replays.

Working receivers: [Node](../examples/node/webhook-server.mjs) · [Python](../examples/python/webhook_server.py).

> **Discord and Slack aren't signed.** A URL on `discord.com/api/webhooks/*` or `hooks.slack.com/services/*` is auto-detected and gets native message formatting, with **no** signature. If you need the HMAC, send `"format": "generic"` explicitly.

## Retries and auto-disable

| | |
|---|---|
| Timeout | 15 seconds |
| Success | Any `2xx` |
| Redirects | Not followed. A `3xx` counts as a failure |
| Permanent refusal | Any `4xx` except `408` and `429`. Not retried |
| Retry schedule | Up to 7 attempts: after 1 min, 5 min, 30 min, 2 h, 8 h, 24 h (about 35 h total), then `dead` |
| Auto-disable | After **20 consecutive** failures, `active` becomes `false`, queued deliveries are dropped, and the account owner is emailed |

Deliveries **aren't ordered and may arrive more than once**, so make your handler idempotent, keyed on `X-Salvagealert-Delivery-Id`. To re-enable a disabled webhook, send `PATCH /webhooks/{id}` with `{"active": true}`. Events from the time it was off aren't backfilled.

Inspect past deliveries with `GET /webhooks/{id}/deliveries` and replay one with `POST /webhooks/{id}/deliveries/{deliveryId}/redeliver`.

## VIN watches

`POST /vin-watches` with `{"vin": "…"}` watches **one vehicle** on every source, whatever its lot number. Every ingested lot is checked against the VIN. If you add `region` (`us`, `ca`, `uk`, `eu`) and `sources`, the VIN is also searched actively every 48 hours, or immediately with `POST /vin-watches/{id}/run`. A hit is delivered as `lot.matched`, kind `vin_watch_match`.

Limits: one watch per VIN (`409 duplicate`), 200 VIN watches per account (`429 too_many_watches`). The feature is plan-gated (`403 plan_gate`).
