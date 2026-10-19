# Sydney Flight Intelligence

A free-to-run fare watch for return flights from Sydney (SYD) to Europe, Japan and China, 3–12
months ahead. It finds unusually low prices, tracks trends, explicitly checks China Southern and
Virgin Australia, rejects routings through the Middle East or Turkey, and emails a daily summary
with links to a live search where you confirm the price and book.

**Status:** Phase 1 (provider feasibility) complete — see
[docs/PHASE1_PROVIDER_FEASIBILITY.md](docs/PHASE1_PROVIDER_FEASIBILITY.md). The application is not
built yet.

**Important limit:** with no paid data source, all prices are *indicative* (cached prices other
travellers found recently). The app never presents them as confirmed or bookable; always check
the live link before buying.

## First test (milestone 1)

1. Create a free Travelpayouts account and copy its API token.
2. In GitHub: **Settings → Secrets and variables → Actions → New repository secret**,
   name `TRAVELPAYOUTS_TOKEN`.
3. **Actions → Probe → Run workflow**, e.g. destination `TYO`, month `2027-04`.

Or locally: `TRAVELPAYOUTS_TOKEN=... python3 probe/indicative_search.py --dest TYO --month 2027-04`

## Documents

- [Backlog](docs/BACKLOG.md) · [Product history and definitions](docs/PRODUCT_HISTORY.md)
