// Mirror the archived catalogue with the keyset cursor, then pull deltas.
// State goes in ./mirror-state.json and rows in ./lots.ndjson. A real mirror
// would upsert into a database on (source, lot_key).
//
// Usage: node mirror-inventory.mjs [source] [maxPages]
import { readFileSync, writeFileSync, appendFileSync, existsSync } from 'node:fs';
import { client } from './client.mjs';

const [source = 'copart_de', maxPages = '5'] = process.argv.slice(2);
const STATE = './mirror-state.json';
const state = existsSync(STATE) ? JSON.parse(readFileSync(STATE, 'utf8')) : { hwm: null, cursor: '' };
const sa = client();

let pages = 0;
for (;;) {
  const qs = new URLSearchParams({ source, page_size: '100', cursor: state.cursor ?? '' });
  if (state.hwm) qs.set('updated_since', String(state.hwm));
  const { data, balance } = await sa('GET', `/inventory?${qs}`);

  for (const lot of data.lots) {
    appendFileSync('./lots.ndjson', JSON.stringify(lot) + '\n');
    state.nextHwm = Math.max(state.nextHwm ?? 0, lot.archived_at ?? 0); // archived_at is SECONDS
  }
  state.cursor = data.next_cursor;
  writeFileSync(STATE, JSON.stringify(state, null, 2));
  console.log(`+${data.lots.length} lots, balance ${balance}`);

  if (!data.next_cursor) {
    // Walk complete: next run asks only for what changed since.
    state.hwm = state.nextHwm ?? state.hwm;
    state.cursor = '';
    writeFileSync(STATE, JSON.stringify(state, null, 2));
    console.log(`up to date; next run uses updated_since=${state.hwm}`);
    break;
  }
  if (++pages >= Number(maxPages)) { console.log('page budget reached; rerun to resume'); break; }
}
