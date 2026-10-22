// Minimal webhook receiver that verifies X-Salvagealert-Signature.
// Usage: SALVAGEALERT_WEBHOOK_SECRET=... node webhook-server.mjs   (listens on :8787)
import { createServer } from 'node:http';
import { createHmac, timingSafeEqual } from 'node:crypto';

const SECRET = process.env.SALVAGEALERT_WEBHOOK_SECRET;
if (!SECRET) throw new Error('Set SALVAGEALERT_WEBHOOK_SECRET (returned once by POST /webhooks)');
const seen = new Set(); // use a database in production, keyed on the delivery id

export function verify(rawBody, header, secret, toleranceSec = 300) {
  if (!header) return false;
  const parts = Object.fromEntries(header.split(',').map((p) => p.trim().split('=')));
  const t = Number(parts.t);
  if (!t || Math.abs(Date.now() / 1000 - t) > toleranceSec) return false;
  const expected = createHmac('sha256', secret).update(`${t}.${rawBody}`).digest('hex');
  const a = Buffer.from(expected);
  const b = Buffer.from(parts.v1 ?? '');
  return a.length === b.length && timingSafeEqual(a, b);
}

createServer((req, res) => {
  const chunks = [];
  req.on('data', (c) => chunks.push(c));
  req.on('end', () => {
    const raw = Buffer.concat(chunks).toString('utf8'); // the RAW body, before JSON.parse
    if (!verify(raw, req.headers['x-salvagealert-signature'], SECRET)) {
      res.writeHead(401).end('bad signature');
      return;
    }
    const id = req.headers['x-salvagealert-delivery-id'];
    res.writeHead(200).end('ok'); // answer fast, then do the work
    if (seen.has(id)) return;     // deliveries can repeat
    seen.add(id);

    const { event, data } = JSON.parse(raw);
    switch (data.kind) {
      case 'watch_match':
        console.log(`[${event}] watch ${data.watch_id}: ${data.lot.year} ${data.lot.make} ${data.lot.model} ${data.lot.detailUrl}`);
        break;
      case 'auction_result':
        console.log(`[${event}] ${data.source} ${data.result}${data.final_price != null ? ` at ${data.final_price}` : ''}`);
        break;
      case 'test':
        console.log('test delivery received');
        break;
      default:
        console.log(`[${event}] ${data.kind}`, data);
    }
  });
}).listen(8787, () => console.log('listening on http://localhost:8787'));
