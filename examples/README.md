# Examples

Every example reads your key from `SALVAGEALERT_KEY` and needs nothing beyond the language's standard library.

```bash
export SALVAGEALERT_KEY="sa_live_…"   # https://salvagealert.com/app/api
```

## cURL

```bash
./curl/me.sh
./curl/search.sh copart_uk BMW
./curl/vin-history.sh 1HGCM82633A004352
./curl/fees.sh
./curl/watch.sh https://example.com/hooks/salvagealert
```

## Node.js (18+)

```bash
cd node
node me.mjs
node search.mjs iaai_ca HONDA 2
node vin-history.mjs 1HGCM82633A004352
node mirror-inventory.mjs copart_de 5
SALVAGEALERT_WEBHOOK_SECRET=… node webhook-server.mjs
```

`client.mjs` is a small reusable wrapper (about 30 lines) that handles auth, typed errors and retries on `429`/`5xx`. You can copy it into your own project.

## Python (3.9+)

```bash
cd python
python me.py
python search.py copart_us TOYOTA 2
python vin_history.py 1HGCM82633A004352
python fees.py iaai_us 5000 FL
python mirror_inventory.py copart_de 5
SALVAGEALERT_WEBHOOK_SECRET=… python webhook_server.py
```

`salvagealert.py` is the same wrapper in Python.

## Testing webhooks locally

Expose port 8787 with a tunnel (`cloudflared tunnel --url http://localhost:8787` or `ngrok http 8787`). Register the https URL it gives you with `./curl/watch.sh <url>`, and the script fires a test delivery straight away.
