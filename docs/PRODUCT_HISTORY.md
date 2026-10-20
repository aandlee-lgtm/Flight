# Sydney Flight Intelligence: product history, decisions and definitions

Running record of the owner's requests, the answers and decisions, and what shipped. Source for user
instructions, definitions and release notes. Open requests: [BACKLOG.md](BACKLOG.md).

---

## 1. History

### 2026-10-19 — Master build prompt; Phase 1 (provider feasibility)
**Asked for.** A production flight-intelligence service that finds genuinely bookable, well-priced
return fares from Sydney to Europe (priority 1, no transit through the Middle East or Turkey),
Japan (2) and China (3), 3–12 months ahead; explicit China Southern and Virgin Australia assessment
every cycle; verification before anything is recommended; history and scoring; a dashboard; a daily
email to two recipients. Start with Phase 1 and stop for approval on paid access and credentials.

**Found and explained.**
- Amadeus Self-Service was shut down on 17 July 2026; Kiwi Tequila, Skyscanner and direct GDS access
  need partner or agency contracts. Scraping booking sites is ruled out by their terms.
- Duffel (live mode) is the recommended primary source: priced, expiring offers with operating
  carrier, cabin, fare brand, baggage and taxes; China Southern and Virgin Australia reached via
  Travelport. Ignav as second source and for booking links; Travelpayouts (cached) for exploration
  only, always labelled Indicative.
- Virgin Australia's own Europe flights are operated by Qatar Airways via Doha, so they are excluded
  by the transit rule; "No practical fare found today" will be common for Virgin to Europe.
- Estimated running cost ≈ A$40–155 per month.
- This cloud session cannot reach api.duffel.com (network policy), so no live search could be run.

**Proposed (superseded the same day by the free-only decision below).** Duffel as primary source,
Python FastAPI + worker, PostgreSQL job queue, Next.js dashboard, Postmark or Resend. Egypt included in the excluded
transit list by default.

**Shipped.** Phase 1 report (revision 1); milestone-1 probe script for Duffel with transit check
and unit tests, in the PhotoSelect repository. No application build, version or release.

### 2026-10-19 — No paid access; own repository
**Asked for.** "I do not want to pay for any access", and the project goes into a new repository
(`aandlee-lgtm/Flight`).

**Explained.** No free, authorised source gives currently bookable, repriceable fares. The best
free source, the Travelpayouts / Aviasales Data API, gives cached prices that real users found in
the last 2–7 days, in AUD, with the airline and number of stops (not the connection airports) and
a link to a live search. So the free product is a fare *watch*: every price is Indicative, there
are no "Buy" labels, connecting routes are marked "routing not verified" unless the airline rules
them out, and the owner confirms the price on the live link before buying. Premium cabins,
baggage, fare class and loyalty earning cannot be confirmed for free.

**Decided.** Travelpayouts as the only data source; GitHub Actions for the schedule; SQLite on a
`data` branch for history; Gmail SMTP (app password) for email, reported as "accepted", never
"delivered"; dashboard runs locally; template-written explanations instead of a paid AI model.
Duffel probe removed. Running cost A$0.

**Shipped.** Repository set up with Phase 1 revision 2, the free probe
(`probe/indicative_search.py`, also runnable from Actions → Probe), transit tests and working
rules. No application build, version or release.

### 2026-10-19 — Google Flights, Trip.com and Booking.com instead of Travelpayouts
**Asked for.** Search Google Flights, Trip.com and Booking.com directly instead of opening a
Travelpayouts account; every result must link to where it was found; all prices in A$, checked
three times.

**Explained.**
- A program that automatically reads prices from these sites isn't allowed:
  - **Booking.com:** its terms ban robots, scrapers and even "automated assistants" without
    written permission (May 2026 terms). A US court found Booking.com itself liable for accessing
    Ryanair's site without permission.
  - **Google Flights:** no public API. Google's terms ban automated access that breaks its
    robots.txt rules or gets round its protections.
  - **Trip.com:** its terms could not be read from this session. Trip.com has a free affiliate
    programme (Awin, Involve Asia) with deep links; its data feed is confirmed only for hotels.
  - Doing it anyway would also break the master prompt's own rule against scraping in breach of
    terms, and these sites block bots, so it would fail often.
- Allowed, free options:
  - **(A) Link-only:** each run builds exact search links on all three sites (route, dates,
    1 adult, cabin, AUD) and the email lists them. The live price appears when you click. The app
    shows no prices of its own, so it can't rank deals or track trends.
  - **(B) Trip.com affiliate:** join for free; deep links are allowed, but a flight price feed is
    not confirmed.
  - **(C) Free price source plus links:** a free API (Travelpayouts was the only one found)
    finds the cheap dates, and every result carries links to Google Flights, Trip.com and
    Booking.com for exactly those dates, in AUD.
- A$ triple check designed (backlog F12).

**Decided.** Waiting for the owner's choice between A, B and C.

### 2026-10-19 — Travelpayouts requires a website
**Asked.** The owner found that using a Travelpayouts account means having a website and adding
code to its header.

**Explained.** Correct: Travelpayouts asks partners to confirm they own a website before giving
API access, by placing a verification snippet in the site's `<head>`. A free way to do that is
a one-page site on GitHub Pages. Pages is free only for public repositories, so it would go in
a separate public repository, keeping the Flight repository private. The page should be a real,
small fare-watch page; Travelpayouts may review it. The verification snippet isn't a secret and
can be pasted into the page. The alternative is option A (links only, no accounts, no automatic
prices).

**Decided.** Waiting for the owner.

### 2026-10-19 — Free website chosen
**Decided.** The owner chose the free GitHub Pages website (`aandlee-lgtm.github.io`) for
Travelpayouts verification and asked for step-by-step instructions, which were given: create the
public repository, check Pages settings, give the Claude GitHub App access, register the site in
Travelpayouts, send the verification snippet, then store the API token as a Flight secret.

### 2026-10-19 — Website published
The owner created `aandlee-lgtm.github.io` but couldn't find the GitHub App installations page
(step 8). That step wasn't needed: the Claude app already had access. A one-page "Sydney Fare
Watch" site was published there (destinations, how it works, no prices yet), with a marked place
in its `<head>` for the Travelpayouts verification snippet.

### 2026-10-19 — Travelpayouts verification code added
The owner supplied the Travelpayouts verification code: Travelpayouts' "Drive" script, which
loads from `emrldco.com`. It was placed in the `<head>` of https://aandlee-lgtm.github.io. Drive
can also turn travel links on that page into Travelpayouts affiliate links. It doesn't touch
the Flight app or the emails.

### 2026-10-19 — Milestone 1 (free version) reached
The owner saved `TRAVELPAYOUTS_TOKEN` but could not find the Probe workflow on GitHub, so Claude
started it directly. Results:
- SYD–TYO, departing April 2027: the API answered in AUD with **0 cached fares**, as did SYD–PAR
  for February 2027. Far-ahead months and less-searched routes have little or no cached data
  (risk R4).
- SYD–TYO, departing January 2027: 13 cached fares. The cheapest within 12–17 nights was
  **A$1,719 return, China Eastern (MU), 3 → 20 January 2027 (17 nights), 1 stop each way**,
  routing marked "unverified". It was found by an Aviasales user on 17 October 2026 and carries
  a live Aviasales search link. Three more China Eastern fares followed at A$1,790–1,968.
- A$ checks seen in this result: the API answered in AUD, and the link itself says
  `expected_price_currency=aud` with the same amount (`expected_price=1719`).
- Found for later: the Aviasales link encodes the airports flown (e.g. `SYDPVGNRT`, via Shanghai
  Pudong). That could let the transit check confirm connection airports instead of saying
  "unverified". The format isn't documented, so it needs testing first.

### 2026-10-19 — "Maybe we did this all incorrectly": the purpose restated
**Said.** The owner wants a daily check that looks for the best *real* flights well into the
future, so an exceptional fare prompts them to plan a holiday for those dates. They want to enter
their own key cities, and the results must be real.

**Explained.** Nothing built so far is wasted: the website, token and probe are the plumbing for
exactly this. What changes is the focus:
- **The owner's watchlist** replaces the fixed destination priorities.
- **"Compelling fare" alerts** replace the full comparison report.
- **"Real" means:** the fare was actually found by a real search, recently. Prices older than 3
  days are dropped, every fare carries a link that opens a live search for the same flights and
  dates, and the A$ checks apply.
- **What free data can't do:** guarantee the fare is still there when the link is opened. The
  link is the final check. Guaranteed live prices need a paid source, which the owner has ruled
  out.
- **Expected gaps:** far-ahead months on quieter routes will often have no recent real fare.
  The email says so rather than guessing.

**Decided.** Backlog F14 records the design. Waiting for the owner's city list and target prices.

### 2026-10-19 — Watchlist and target prices
**Given.** Paris and London under A$1,300; Tokyo and Osaka or Kyoto under A$1,000; Shanghai,
Guangzhou or Hong Kong under A$1,000. ("fr $1000" was read as "for A$1,000", to be confirmed.)

**Explained.** Kyoto has no airport, so it is covered by Osaka's Kansai and Itami airports, the
usual way in. Hong Kong is added to the China group. For reference, the first real fare found
(Tokyo A$1,719, January) would not have met the A$1,000 target, so it would have been listed but
not flagged as compelling.

**Shipped.** `watchlist.toml` in the repository, for the owner to edit. Nothing built yet
(waiting for `build_new`).

### 1.0.0 — build_new: daily web page instead of email (19 October 2026)
**Asked for.** Trip lengths of 1–6 weeks confirmed. "Maybe not an email, just a static html that
I can look at myself from the web." Then `build_new`.

**Explained and decided.**
- **Where it lives:** free GitHub Pages only works for public repositories, so the scanner, the
  watchlist and the daily workflow live in the public `aandlee-lgtm.github.io` repository, and
  the page is its home page. This private repository keeps the history, backlog, release notes
  and diagnostics workflows. The page and the watchlist are therefore publicly visible; no
  personal details are on them.
- **Checking the source first:** an exploration run showed that each fare's link carries the
  date the fare was found (`search_date`), the AUD amount it was priced at, and the airports
  flown on each leg. The scanner uses all three, so freshness, the A$ check and the no-Middle-East
  rule rest on the fare itself rather than on guesses.
- **Rules in 1.0.0:**
  - Real fares only: found in the last 3 days.
  - Three A$ checks: the source's currency, the link's currency and amount, and a plausible range.
  - Trips of 1–6 weeks, up to 12 months ahead.
  - No connection airport in the Middle East or Türkiye, and no airline based there.
  - Cheapest fare per city per month; up to three highlights, one per city, under the target price.
  - The 30-day low appears after 14 days of history.
- **First real scan (preview, 19 Oct, 93 requests):** fares found for Guangzhou (A$789 return,
  27 Oct–5 Nov, China Eastern), Tokyo (A$927, 1–13 Nov, China Southern via Guangzhou), Hong Kong
  (A$920, November, Scoot via Singapore), and London (A$1,420, February, China Southern via
  Guangzhou). Paris had only one recent fare (A$2,224); many cached prices were older than 3
  days and were dropped.
- **Owner action needed:** add the same `TRAVELPAYOUTS_TOKEN` secret to the
  `aandlee-lgtm.github.io` repository so the daily run there can search.

**Shipped (1.0.0).** See [RELEASES.md](RELEASES.md). The second preview scan (19 Oct, 9:56 pm
Sydney) was published as the first live page. Its output is unchanged from the scanner; nothing
was edited by hand. Tests passed on GitHub and locally (14 unit tests, synthetic fixtures). A
`v1.0.0` git tag could not be pushed from the Claude session (blocked by the proxy), so the
release is recorded in RELEASES.md only.

### 20 October 2026 — first automatic run
The scheduled 6:42 am run (GitHub started it 25 minutes late) and a manual retry failed: the
website repository had no `TRAVELPAYOUTS_TOKEN` yet, because each repository keeps its own
secrets. The page was correctly left unchanged. After the owner added the secret, the 8:12 am
run succeeded and published the page by itself, also starting the price history (20 fares
recorded). Highlights: Guangzhou A$789, Hong Kong A$858 (Scoot via Singapore, 1 Nov–6 Dec),
Tokyo A$906 (China Southern via Guangzhou, 1–13 Nov). Paris now shows A$1,355 for 9–17 November,
just above the A$1,300 target.

### 20 October 2026 — Velocity and Sky Pearl badges requested
**Asked for.** "I am a Velocity frequent flyer as well as a member of the China Southern loyalty
program, please call out fares that will contribute to these programs with a small indicator."

**Explained.**
- The free data says which airlines sell each fare (from the booking link). It doesn't say the
  fare class, and both programmes set points by fare class; some of the cheapest classes earn
  little or nothing. So a badge can honestly say "may earn", not "will earn".
- Partner lists came from the programmes' own pages and FAQs found by search. Neither official
  site could be opened from the Claude session, so Sky Pearl's partner list in particular should
  be re-checked. Scoot does not appear among Velocity's partners, so Scoot fares get no badge.
- Examples from today's page that would get a Sky Pearl badge: Tokyo A$906 and Paris A$1,355
  (both China Southern). Fares sold only partly by an earning airline show "(part)".

**Decided.** Built and tested (19 unit tests) on a branch; the live page is unchanged until the
owner says `build_new`, per the working rules.

### 1.1.0 — build_new: badges published (21 October 2026)
**Asked for.** "Can you re-run for today please, build_new."

**Done.** The loyalty badges were merged as 1.1.0 and today's scan was re-run (9:27 am). Checking
the result showed a flaw: a London fare listed as Virgin Australia carried only a Sky Pearl
badge. On trips involving several airlines, the listed airline (here Virgin Australia,
Sydney–Bali) and the airline in the booking link (Xiamen Airlines, onward) differ. The badge now
considers both, so that fare shows "Velocity (part)" and "Sky Pearl (part)". A regression test
was added (22 tests), and the scan was run again at 9:29 am. Re-running replaced today's history
rows instead of duplicating them.

**Badges on today's page:**
- Sky Pearl: Tokyo A$786 (Xiamen Airlines, 29 Oct–16 Nov) and A$906 (China Southern, 1–13 Nov);
  Paris A$1,355 and London A$1,420 (China Southern).
- Velocity (part): London A$1,937, Guangzhou A$1,690 (Virgin Australia plus other airlines), and
  Tokyo A$1,093 (Singapore Airlines plus another airline).

---

## 2. Definitions

- **Confirmed** — priced by an authorised API, repriced just before publishing, not expired.
- **Indicative** — a price that cannot be shown to be currently bookable (cached, unrepriced or
  unconfirmed); never used in purchase recommendations.
- **Expired / Unavailable / Rejected** — offer past its expiry / no longer returned on repricing /
  failed a verification rule (e.g. excluded transit).
- **Excluded transit** — any airport (segment endpoint or technical stop) in UAE, Qatar, Bahrain,
  Saudi Arabia, Oman, Kuwait, Jordan, Lebanon, Israel, Iran, Iraq, Syria, Yemen, Türkiye or Egypt;
  with cached data, any fare sold by an airline based there.
- **Watch** — the label for an indicative fare that is unusually low against comparable history;
  it means "check the live link now", never "buy".
- **Routing not verified** — a connecting itinerary whose connection airports the free source
  does not give; it may still connect in an excluded country, so check before buying.
- **Compelling fare** — a real fare at or below the owner's target price for that city, or
  among the cheapest seen for that city and month once enough history exists.
- **Real (free version)** — found by a real search within the last 3 days, priced in A$, with a
  link that reproduces it. Older prices are dropped.
- **Loyalty badge** — "Velocity" or "Sky Pearl" beside a fare: the airline(s) selling it earn
  with that programme. Points still depend on the fare class; "(part)" means only some flights do.
- **Search link** — a URL that reproduces the route, dates and cabin, not the exact fare; labelled
  as such.
