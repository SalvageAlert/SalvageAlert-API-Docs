# Postman collection

1. In Postman: **Import** → `SalvageAlert.postman_collection.json`.
2. Open the collection → **Variables** → set `apiKey` to your `sa_live_…` key ([get one](https://salvagealert.com/app/api)).
3. Send **Account → GET /me**. It's free and checks your setup.

Requests are grouped by tag. Optional query parameters are included but disabled, so tick the ones you need. The collection is generated from the spec by `scripts/build-postman.py`.
