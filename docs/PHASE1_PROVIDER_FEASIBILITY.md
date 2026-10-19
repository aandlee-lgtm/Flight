# Sydney Flight Intelligence — Phase 1: provider feasibility and architecture

> **Update (1.0.0, 19 Oct 2026):** email was dropped in favour of a daily web page at
> https://aandlee-lgtm.github.io, and the scan follows the owner's own watchlist. See
> [RELEASES.md](RELEASES.md). The provider findings below still apply.

Revision 2, 2026-10-19: **no paid access** (the owner's decision). Revision 1 recommended Duffel
(paid per search); it is kept in the history only. Nothing in this document is a fare.

---

## 1. Summary — what "free only" means

**There is no free, authorised source of currently bookable, repriceable airfares in 2026.**
Every source that returns a price you can buy at that moment either charges per search (Duffel,
Ignav after a trial) or needs a commercial contract (Amadeus Enterprise, Sabre, Travelport,
Skyscanner, Kiwi). Scraping Google Flights or booking sites breaks their terms and is ruled out.

The best free, authorised source is the **Travelpayouts / Aviasales Data API**: free token, AUD
supported, prices that real Aviasales users found in the last 2–7 days, each with a link that
opens a live Aviasales search for the same route and dates.

Consequences for the product (prompt principles 2 and 8 applied honestly):

| Prompt requirement | Free-only reality |
|---|---|
| Confirmed, currently bookable fare | **Not possible automatically.** Every fare is **Indicative** (found by someone else, up to days ago). |
| Stage C repricing | Not available; the link opens a live search where the current price is shown. |
| Stage D corroboration | Partly: compare with the Aviasales month matrix and our own history; no second live supplier. |
| Transit restriction (no Middle East / Turkey) | Cached data gives the airline and **number** of stops, not the connection airports. Direct flights comply; Middle Eastern and Turkish carriers are rejected; everything else is shown as **routing not verified**. |
| Operating carrier, cabin, fare family, booking class, baggage | **Not available** in cached data (economy only; airline code only). |
| Purchase labels (Exceptional, Strong Buy…) | Not used, because nothing is verified. Reports use **Watch** labels ("Unusually low — check now"), with the price age stated. |
| Loyalty (Velocity, Sky Pearl) | Only general statements by airline; earning cannot be confirmed without the fare class. |
| Premium Economy / Business | Not reliably available free; the Premium cabin table will usually say "No free data source". |

**So the free product is a fare *watch*, not a fare *verifier*:** it finds unusually low prices
early, tracks trends, and hands you a one-click live search to check and buy. The check-and-buy
step stays with you. If you ever want automatic confirmation, adding a paid provider (Duffel,
≈ US$30–40/month) later needs no redesign: the provider layer is built for it.

---

## 2. Free provider comparison

| Source | Free? | Authorised? | Data | Use |
|---|---|---|---|---|
| **Travelpayouts Data API** (`/aviasales/v3/prices_for_dates`, month matrix, latest prices) | ✅ free token | ✅ documented affiliate API | Cached prices from user searches (2–7 days), AUD, airline, stops count, dates, link to live search | **Primary** |
| Aviasales live search links | ✅ | ✅ | Opens a live search for the route/dates | **Booking path** ("View fare" = search link, labelled so) |
| Google Flights search URL | ✅ | ✅ (a link, no data taken) | Opens Google Flights for route/dates/cabin | Second booking path |
| Ignav | First 1,000 requests free, then US$2 / 1,000 (not clear if monthly) | ✅ | Live search + booking links | Optional spot-check of top deals only while free; dropped if it would bill |
| Travelpayouts live Flights Search API (new version) | Approval; reportedly needs ~50k monthly users | ✅ | Live | Not available to us |
| Duffel live | ❌ US$0.005 per search when nothing is booked | ✅ | Live, repriceable | Paid upgrade path only |
| Amadeus Self-Service | ❌ shut down 17 Jul 2026 | — | — | — |
| Kiwi Tequila, Skyscanner | ❌ partner approval | — | — | — |
| SerpApi (Google Flights) | 100 searches/month free | ⚠️ scrapes Google; Google is suing SerpApi | Live | **Not used** (terms) |

---

## 3. Free architecture

```mermaid
flowchart LR
  TP[Travelpayouts Data API<br/>free, cached, AUD] --> W
  subgraph GH["GitHub Actions (scheduled, free)"]
    W[Python worker<br/>planner · adapter · normaliser ·<br/>checks · scoring · report]
  end
  W <--> DB[(SQLite file<br/>on a 'data' branch)]
  W --> SMTP[Gmail SMTP<br/>app password, free] --> R1[leeawc@me.com]
  SMTP --> R2[Rhianhughes@me.com]
  W --> REP[HTML report + run log<br/>committed per run]
  DB --> UI[Local dashboard on your Mac<br/>opened when wanted]
```

| Part | Free choice | Why / limit |
|---|---|---|
| Scheduler | GitHub Actions cron in this repo | 2,000 free minutes/month on a private repo; a daily run takes a few minutes. Runs independently of any chat tool. Run logs kept by GitHub. |
| Database | SQLite file kept on a `data` branch | No account, no server; full history in git. PostgreSQL can replace it later without changing the rest. |
| Email | Gmail SMTP with an app password (or Brevo free plan, 300/day) | Free; two separate sends. Limit: SMTP only tells us "accepted"; bounces come back as emails, so "delivered" can't be confirmed — the report states "accepted by Gmail", never "delivered". |
| Dashboard | Runs locally on your Mac reading the database; every report is also committed as HTML | GitHub Pages for a private repo needs a paid plan, so no hosted dashboard. |
| AI summaries | Deterministic, template-written explanations from the stored numbers | The Claude API is paid. Templates can't invent data, which also suits principle 1. |
| Secrets | GitHub Actions secrets (`TRAVELPAYOUTS_TOKEN`, `SMTP_USER`, `SMTP_APP_PASSWORD`) | Never in the repo or the browser. |

**Monthly cost: A$0**, within the free limits above.

---

## 4. Search strategy within free limits

Travelpayouts allows roughly 200 requests per hour per token without approval (to confirm on
sign-up).

1. **Month matrix** per destination city × next 12 months (~35 cities × 12 = 420 calls, spread over
   the day or rotated across 3 days).
2. **Prices for dates** on the cheapest months, trip lengths 12–17 nights first, then 8–11 /
   18–24 / 28–42.
3. **Mandatory carriers:** filter results by airline `CZ` (China Southern) and `VA` (Virgin
   Australia) every run; report "No practical fare found today" when none qualify.
4. **Trend history** only from the same route + month + trip-length band + airline, and only once
   enough observations exist ("not enough history yet" until then).

---

## 5. Risks

| # | Risk | Mitigation |
|---|---|---|
| R1 | All prices are cached and may be gone | Show the price age; label everything Indicative/Watch; never "Buy" |
| R2 | Connection airports unknown → a Doha/Istanbul/Dubai connection could slip through | Reject Middle Eastern and Turkish carriers; mark other connecting itineraries "routing not verified"; the live link shows the routing before you buy |
| R3 | Virgin Australia's own Europe flights are operated by Qatar Airways via Doha | VA + Europe + connection is rejected as "likely via Doha"; VA assessed mainly for Japan/China |
| R4 | Sparse data far ahead (9–12 months) and for less-searched cities | Report coverage gaps per destination instead of filling them |
| R5 | Travelpayouts terms (affiliate programme) and limits change | Adapter isolated; check terms on sign-up; record every API error in the run log |
| R6 | Gmail sending limits/deliverability | 2 emails a day is far below limits; Brevo as fallback |

---

## 6. Accounts needed (all free)

1. **Travelpayouts** account → API token → add as repository secret `TRAVELPAYOUTS_TOKEN`
   (GitHub → Flight → Settings → Secrets and variables → Actions).
2. **Gmail app password** for the sending account (needs 2-step verification) → secrets
   `SMTP_USER` and `SMTP_APP_PASSWORD`. Needed in Phase 5 only.
3. Confirm **Egypt** stays in the excluded transit list (default: yes).

---

## 7. Milestone 1 (revised)

The prompt's milestone — a *currently priced, bookable* fare — **cannot be met without paying**.
The free milestone is: **one real SYD return fare from the Travelpayouts API, in A$, with dates,
airline, stops, transit check result, and a working live-search link, labelled Indicative.**

Run it on GitHub (the Claude cloud session's network blocks the provider): Actions → **Probe** →
Run workflow, with destination and month. Or on a Mac:

```
export TRAVELPAYOUTS_TOKEN=...
python3 probe/indicative_search.py --dest TYO --month 2027-04
```

---

## Sources

- Amadeus Self-Service shutdown: [PhocusWire](https://www.phocuswire.com/amadeus-shut-down-self-service-apis-portal-developers), [AirLabs](https://airlabs.co/amadeus-self-service-api-shutdown)
- Duffel fees: [Excess search](https://help.duffel.com/hc/en-gb/articles/4412912264466-What-is-Excess-Search), [pricing listing](https://apis.io/plans/duffel/duffel-plans-pricing/)
- Travelpayouts: [Data API](https://support.travelpayouts.com/hc/en-us/articles/203956163), [readthedocs](https://travelpayouts-data-api.readthedocs.io/), [old live search API retired](https://support.travelpayouts.com/hc/en-us/articles/203956173-API), [roundup incl. 50k MAU requirement](https://thunderbit.com/es/blog/best-flight-api-with-free-tiers)
- Ignav: [FAQ](https://ignav.com/docs/faq)
- SerpApi: [pricing](https://serpapi.com/pricing), [free plan](https://costbench.com/software/web-scraping/serpapi/free-plan/)
- Kiwi / Skyscanner access: [Vervotech](https://www.vervotech.com/hub/integrations/tequila-api/), [Skyscanner](https://www.skyscanner.jp/news/partnerships/skyscanner-travel-api)
- Virgin Australia via Doha: [Australian Aviation](https://australianaviation.com.au/?p=1414526); China Southern–Virgin codeshare: [AeroRoutes](https://www.aeroroutes.com/eng/260420-czvacodeshare)

The Travelpayouts field names used by the probe follow its published v3 documentation but have not
yet been exercised against the live API from this repository.
