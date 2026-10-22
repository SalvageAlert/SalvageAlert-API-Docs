# Getting started

This guide goes from no account to a working search in about five minutes.

## 1. Create an account and a key

1. [Sign up at salvagealert.com](https://salvagealert.com/register). Your account gets **50 free API credits**, and no card is needed.
2. Open the [API dashboard](https://salvagealert.com/app/api) and copy your key. It looks like `sa_live_` followed by 32 base32 characters.
3. Set your project URL on that page. Keys that name no project URL are revoked; see [authentication](authentication.md).

Store the key in an environment variable. Never commit it.

```bash
export SALVAGEALERT_KEY="sa_live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

## 2. Make a free call

`GET /me` costs 0 credits, so it's the right way to check your setup:

```bash
curl -i https://salvagealert.com/api/v1/me \
  -H "Authorization: Bearer $SALVAGEALERT_KEY"
```

`-i` prints the headers. Look for these:

```
HTTP/2 200
x-request-id: 6f1c2a7e-3b0d-4d7e-9a51-2f7f0c1b9e44
x-credits-charged: 0
x-credits-balance: 50
x-ratelimit-limit: 60
x-ratelimit-remaining: 59
x-ratelimit-reset: 1761062460
```

## 3. Search

```bash
curl -X POST https://salvagealert.com/api/v1/lots/search \
  -H "Authorization: Bearer $SALVAGEALERT_KEY" \
  -H "Content-Type: application/json" \
  -d '{"source":"iaai_ca","makes":["HONDA"],"year_min":2019,"locations":["CA-QC"]}'
```

The response holds up to `page_size` lots (25 by default, at most 100) in the camelCase `Lot` shape. If you repeat the same request within the cache window, you get `"cached": true` and `X-Credits-Charged: 0`.

## 4. Next steps

- Learn every filter in [searching lots](searching-lots.md).
- Keep a local copy of the catalogue with [inventory and mirroring](inventory-and-mirroring.md).
- Stop polling and use [webhooks](webhooks.md) instead.
- Read the [field conventions](conventions.md) before you write a deserializer.
