// Relisting trail for a VIN. Usage: node vin-history.mjs 1HGCM82633A004352
import { client, SalvageAlertError } from './client.mjs';

const vin = process.argv[2];
if (!vin) throw new Error('usage: node vin-history.mjs <VIN>');
try {
  const { data } = await client()('GET', `/vin/${encodeURIComponent(vin)}/history`);
  console.log(`${data.count} lot(s) for ${data.vin}`);
  for (const l of data.lots) {
    console.log(`  ${l.source_label} #${l.lot_key}  ${l.year} ${l.make} ${l.model}  ${l.primary_damage ?? ''}  ${l.title_type ?? ''}  ${l.listing_url}`);
  }
} catch (e) {
  if (e instanceof SalvageAlertError && e.status === 404) console.log('No auction history for this VIN (not billed).');
  else throw e;
}
