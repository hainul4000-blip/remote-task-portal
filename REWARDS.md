# Editing offer rewards

Offer reward details are edited in `data/offers.json`. Each offer has a `reward` object. Use one of these types:

- `cash` — for example `{"type":"cash","amount":10,"currency":"USD","unit":"task","label":"$10 / task","verified":true,"termsUrl":"https://provider.example/terms"}`
- `voucher` — set a customer-facing `label`, such as `"IDR 50,000 voucher"`
- `discount` — set a label such as `"15% discount"`
- `points` — set the points amount and a clear label
- `other` — any clearly described non-cash reward

The site shows `label` first. If there is no label but a cash amount is supplied, it formats the currency, amount, and unit for you. The task directory includes a reward-type filter.

Only set `verified: true` and link `termsUrl` when the provider's current terms clearly confirm that reward. Do not promise guaranteed payment when eligibility or approval conditions apply. Update `getlink` with the actual provider link before activating an offer; the current offers are examples and their buttons remain unavailable until those links are replaced.
