# Sydney Fare Watch — release notes

## 1.6.0 — 13 November 2026

**Middle East connections allowed.** Fares that connect in the UAE, Qatar or elsewhere in the
Middle East, and fares from airlines based there (Emirates, Etihad, Qatar Airways, …), are now
shown.
- **Still excluded:** Türkiye.
- **Editable:** the excluded list is the `excluded_transit_countries` setting in
  `watchlist.toml`, and "How this was checked" lists whichever countries are excluded.
- **Velocity badge:** Qatar Airways now gets one (it is a Velocity partner).

**Expect little change at first.** In the preview, the only extra fare was a Milan trip via Abu
Dhabi (A$2,292). Emirates, Etihad and Qatar fares from Sydney rarely appear in the free data.

## 1.5.0 — 13 November 2026

**More European cities.** The free data holds very few Sydney–Paris fares (2 for the whole next
year when checked). The page now also watches **Rome, Amsterdam, Frankfurt, Milan and
Barcelona**, each with a target of A$1,300 like Paris and London, so a good fare into Europe is
caught even when Paris is quiet.

**Live links on empty months.** Every "No recent fare" row now lists its months as links. Each
opens live Google Flights prices in A$ for return trips departing in that month.

## 1.4.0 — 13 November 2026

**"Lowest recorded" now means a fare you could still book.**
- **Trips still ahead only.** Each city's lowest recorded price in the last 30 days now ignores
  trips that have already departed. London had been showing A$1,133 for an 11 November flight.
- **The dates are shown**, and the line says whether that fare is still in today's list.
- **If it isn't,** the line says when the fare was last seen and that it may have sold out or
  changed price, with a link to the last-seen fare and a "Check these dates on Google Flights
  (A$)" link.

**Business & Premium Economy section.** The free fare data covers economy only, so the page shows
no premium prices. For each city, two links open live Premium Economy and Business prices in A$
on Google Flights, for the same dates as that city's cheapest economy trip.

**Back-up morning runs.** GitHub skipped the scheduled scan on 10 November. Two back-up times
(about 7:17 and 8:17 am Sydney) now scan only if that morning's page hasn't been built, so a
dropped run is made up the same morning.

## 1.3.0 — 24 October 2026

**Lookout: Sydney → Adelaide, Virgin Australia, one way, Tue 24 November 2026, leaving before
noon.** A new "Lookout" card at the top of the page:
- **When a real fare has been found:** the cheapest real Virgin Australia fare for that
  morning, with departure time, flight number, connections, a Velocity badge, how recently it
  was found, and a "View fare" link.
- **Always:** a "Search this morning on Google Flights (A$)" link, so the live price is one tap
  away even on days with no recorded fare.
- **Trend line:** built from the days a real fare was seen, ending with today's.
- **After 24 November** the card says the date has passed.
- **To change** the date, the airline or the "before noon" time, edit the `[[lookout]]` entry in
  `watchlist.toml`. More lookouts can be added the same way.

**Limitation:** the free data source holds few domestic one-way prices. When this was built
there was no fare at all for 24 November, and only three Sydney → Adelaide fares for all of
November. Expect the card to show "No real fare" on many days.

**Also:** domestic one-way fares use their own sanity floor (A$30). The international floor of
A$150 would have wrongly rejected real fares such as a Jetstar Sydney → Adelaide fare at A$124.

## 1.2.0 — 24 October 2026

**Price trend line in "Worth a holiday?".** Each highlighted city now has a small line showing
its cheapest real fare on each day the scan has run (recorded since 20 October), ending with
today's price.
- A faint dashed line marks your target price.
- Hover over a point to see its date and price.
- A caption gives the first price, today's price and the lowest so far.
- Each point is that city's cheapest fare on that day, whatever the dates or airline, so the
  line shows whether the city is getting cheaper overall.
- A city with fewer than two days of scans shows a short note instead.

## 1.1.0 — 21 October 2026

**Velocity and Sky Pearl badges.** Fares sold by an airline that earns with your programmes now
carry a small badge next to the airline name, in the "Worth a holiday?" cards and in each city
table:
- **Velocity**: Virgin Australia, Singapore Airlines, ANA, United, Air Canada, Hainan, Hong Kong
  Airlines, Tianjin, Beijing Capital.
- **Sky Pearl**: China Southern, Xiamen, Chongqing, Sichuan, and Sky Pearl partners (American,
  Aerolíneas Argentinas, Air Europa, Air France, China Airlines, Delta, KLM, Korean Air, Vietnam
  Airlines).
- **"(part)"** means only some of the airlines on the trip earn, e.g. Virgin Australia to Bali
  and then another airline onwards.

A badge means the fare **may** earn. Points depend on the fare class, which the free data does
not show, so check the fare rules before booking. Both airline lists are in `watchlist.toml` and
can be edited.

**Also:** running the scan twice on the same day no longer records that day's prices twice in
the history.

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
