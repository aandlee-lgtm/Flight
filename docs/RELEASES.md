# Sydney Fare Watch — release notes

## 1.0.0 — 19 October 2026

The first working version: a page that updates itself every morning with the best real fares
from Sydney to your cities.

**Where:** https://aandlee-lgtm.github.io (rebuilt daily at about 6:17 am Sydney time).

**What it does**
- Checks every city on your watchlist (Paris, London, Tokyo, Osaka/Kyoto, Shanghai, Guangzhou,
  Hong Kong) for every departure month from now to 12 months ahead, for trips of 1–6 weeks.
- **"Worth a holiday?"** at the top: up to three fares under your target price, best first.
- One table per city: the cheapest real fare for each month, with dates, nights, airline,
  connection airports and how recently it was found. Rows under your target are highlighted.
- Every fare has two links: **View fare** (a live Aviasales search for the same flights) and
  **Google Flights** (the same dates there, in A$).

**What "real" means here**
- Only fares that real travellers' searches found in the **last 3 days** are shown; older prices
  are dropped, never shown.
- **A$ checked three times:** the source must price it in AUD, the booking link must carry the
  same AUD amount, and the amount must be plausible. Any failure drops the fare.
- **No connections in the Middle East or Türkiye:** the connection airports are read from the
  booking link and checked by country; airlines based there are excluded. "(check)" marks a
  fare whose connection airports could not all be confirmed.
- A month with no recent real fare says so. Nothing is filled in or guessed.
- "How this was checked" at the bottom lists, per city, how many fares were found and why the
  others were not shown.

**Limits**
- Prices come from other travellers' recent searches (Travelpayouts / Aviasales data, free).
  A fare can change or sell out before you click, so the link is the final check.
- Far-ahead months on quieter routes often have no recent fare.
- The 30-day low for each city appears once 14 days of scans are recorded.

**Changing your cities or prices:** edit `watchlist.toml` in the `aandlee-lgtm.github.io`
repository (pencil icon, then Commit). The next morning's page uses it.
