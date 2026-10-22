// Live search, paging until a page comes back empty.
// Usage: node search.mjs [source] [make] [maxPages]
import { client } from './client.mjs';

const [source = 'copart_us', make = 'TOYOTA', maxPages = '2'] = process.argv.slice(2);
const sa = client();

for (let page = 1; page <= Number(maxPages); page++) {
  const { data, charged, balance } = await sa('POST', '/lots/search', {
    source, makes: [make], year_min: 2018, page, page_size: 25,
  });
  console.log(`page ${page}: ${data.lots.length} lots (est. ${data.total_estimate}), charged ${charged}, balance ${balance}${data.cached ? ' [cached]' : ''}`);
  for (const lot of data.lots) {
    // auctionDateUTC is MILLISECONDS
    const when = lot.auctionDateUTC ? new Date(lot.auctionDateUTC).toISOString().slice(0, 16) : 'not assigned';
    console.log(`  ${lot.year} ${lot.make} ${lot.model}  ${lot.primaryDamage ?? ''}  sale ${when}  ${lot.detailUrl}`);
  }
  // A short page doesn't mean the end (see docs/searching-lots.md). An empty one does.
  if (data.lots.length === 0) break;
}
