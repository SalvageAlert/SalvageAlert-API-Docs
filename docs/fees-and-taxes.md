# Fees and taxes

`GET /fees/estimate` turns a hammer price into an itemized, all-in cost. It's a pure calculation, with no scraping. **0.2 credits.**

It uses the same fee engine as the [SalvageAlert fee calculator](https://salvagealert.com/calculator).

## Parameters

| Param | Values | Default |
|---|---|---|
| `source` **required** | `iaai_ca`, `iaai_us`, `iaai_uk`, `copart_ca`, `copart_us`, `copart_uk`, `copart_de`, `govdeals_us` | |
| `bid` **required** | 0 to 10,000,000, in the source currency | |
| `tax_region` | A CA province (`QC`, `ON`, `AB`, `BC`, `MB`, `SK`, `NB`, `NS`, `NL`, `PE`) or a US state (`FL`, `TX`, … `DC`) | `QC` for Canada, none for the US |
| `include_taxes` | `0` / `1` | `1` |
| `buyer_tier` | `standard`, `highVolume` | `standard` |
| `bid_type` | `preBid`, `liveBid`, `buyNow` | `preBid` |
| `vehicle_category` | `standard`, `heavy` | `standard` |
| `recreational` | boolean (motorcycle, ATV, boat, RV…) | `false` |

The UK and German markets charge a flat VAT and **don't take** a `tax_region`. Passing one returns `invalid_tax_region`. A region that doesn't match the source's country is refused the same way.

Send `bid_type=buyNow` when pricing a Buy Now lot. No internet-bid fee applies to those, so leaving the default overstates the cost.

## Example

```bash
curl "https://salvagealert.com/api/v1/fees/estimate?source=iaai_ca&bid=7500&tax_region=QC" \
  -H "Authorization: Bearer $SALVAGEALERT_KEY"
```

```json
{
  "source": "iaai_ca",
  "market": "iaa_ca",
  "currency": "CAD",
  "bid_amount": 7500,
  "fee_lines": [
    { "key": "buy_fee", "label": "Buy fee", "amount": 725, "detail": "< 25 units / yr", "detail_key": "units_under_25" },
    { "key": "pull_fee", "label": "Pull fee", "amount": 79, "detail": null, "detail_key": null },
    { "key": "online_fee", "label": "Online fee", "amount": 139, "detail": null, "detail_key": null },
    { "key": "digital_sales_fee", "label": "Digital sales fee", "amount": 50, "detail": "1% of bid, min $5, max $50", "detail_key": "one_pct_bid" },
    { "key": "environmental_fee", "label": "Environmental fee", "amount": 10, "detail": null, "detail_key": null },
    { "key": "carfax_fee", "label": "Carfax CVHR", "amount": 41.55, "detail": null, "detail_key": null },
    { "key": "non_dealer_fee", "label": "Non-dealer fee", "amount": 50, "detail": null, "detail_key": null }
  ],
  "total_fees": 1094.55,
  "pst": 109.19,
  "gst": 429.73,
  "tax_breakdown": [
    { "kind": "qst", "field": "pst", "label": "Quebec QST", "rate": 0.09975, "basis": "fees", "amount": 109.19 },
    { "kind": "gst", "field": "gst", "label": "GST", "rate": 0.05, "basis": "bid_and_fees", "amount": 429.73 }
  ],
  "total_without_taxes": 8594.55,
  "total_with_taxes": 9133.47,
  "note": "IAA Canada official buyer fee schedule (effective July 13, 2026)."
}
```

## Reading the taxes

`pst` and `gst` keep their Canadian names for compatibility, but between them they carry five different taxes:

- `pst` holds Quebec QST.
- `gst` holds GST, Ontario HST, US state sales tax, UK VAT or German MwSt.

**Use `tax_breakdown` instead.** For each tax it gives the `kind`, the `rate`, the `basis` (`fees` or `bid_and_fees`) and the `amount`. For US states it applies the state rate only, with no county or local addition.

## Currency

`GET /fx?base=USD&symbols=CAD,EUR,GBP` returns daily reference rates for 0.2 credits.
