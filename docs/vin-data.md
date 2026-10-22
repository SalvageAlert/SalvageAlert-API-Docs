# VIN data

## Relisting history: `GET /vin/{vin}/history`

This returns every distinct lot we've archived for a 17-character VIN, across every source, newest first. It shows the trail of a car that was sold, refused and relisted, or bought and flipped.

- **Cost:** 1 credit. An unknown VIN is a `404` and costs 0.
- Copart lots carry full VINs in all four countries. IAA lots carry a full VIN only where an authenticated crawl reached them.

```json
{
  "vin": "1HGCM82633A004352",
  "count": 2,
  "lots": [{
    "source": "copart_us", "source_label": "Copart USA", "lot_key": "58821234",
    "year": 2019, "make": "HONDA", "model": "ACCORD",
    "primary_damage": "FRONT END", "title_type": "Repairable",
    "sale_date_utc": 1765238400000, "sold_at": null,
    "high_prebid_value": 4200, "est_retail_value": 18750,
    "source_url": "https://www.copart.com/lot/58821234",
    "listing_url": "https://salvagealert.com/lots/copart-us-58821234-2019-honda-accord"
  }]
}
```

Each lot has a `listing_url` that points to its public page on SalvageAlert, which you can link to from your own product.

## Title check: `GET /vin/{vin}/title-check`

This returns a verdict: `found`, `salvage_record`, `branded`, `record_count`, `sources`, `title_types`, `damages`, `first_seen_utc` and `last_seen_utc`. It costs 1 credit.

> If we hold no record, that isn't proof of a clean title. It only means no salvage-auction listing was found in our data.

## Batch: `POST /vin/batch`

```json
{ "vins": ["1HGCM82633A004352", "JTEPU5JR8N6036225"] }
```

- Up to **50** VINs per call.
- Billed **1 credit per VIN that returned at least one lot**. VINs we have nothing for are free, and malformed VINs come back in `invalid` and aren't billed.
- Your balance is pre-authorized for the worst case, so you may get a `402` even when the real charge would have been lower.
- The response lists `requested`, `looked_up` and `billed`. `billed` matches `X-Credits-Charged`.

## Decode and vehicle data (0.2 credits each)

| Call | Returns |
|---|---|
| `GET /vehicles/vin/{vin}` | NHTSA vPIC decode: make, model, trim, engine, plant… |
| `GET /vehicles/safety?make=&model=&year=` | Recalls and crash-test ratings |
| `GET /vehicles/fuel-economy?make=&model=&year=[&trim=]` | EPA fuel economy |

## VIN watches

To be told when a specific vehicle shows up at auction, use `POST /vin-watches` instead of polling `/vin/{vin}/history`. See [webhooks](webhooks.md#vin-watches).
