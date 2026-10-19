"""Milestone 1 (free): real SYD return fares from the Travelpayouts Data API, labelled Indicative.

Standard library only. Needs TRAVELPAYOUTS_TOKEN (free account).

    python3 probe/indicative_search.py --dest TYO --month 2027-04

The prices are cached: real Aviasales users found them recently, but they may no longer be
available. Every field printed comes from the API response; nothing is invented. Each fare gets
a transit check and a live-search link where the current price can be seen before buying.
"""

import argparse
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

from transit import cached_route_check

API = "https://api.travelpayouts.com/aviasales/v3/prices_for_dates"
EUROPE = {"PAR", "CDG", "ORY", "LON", "LHR", "LGW", "AMS", "FRA", "MUC", "ROM", "FCO", "MIL",
          "MXP", "MAD", "BCN", "ZRH"}


def fetch(params, token):
    url = API + "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers={"X-Access-Token": token, "Accept-Encoding": "identity"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = json.load(response)
    except urllib.error.HTTPError as error:
        sys.exit(f"Travelpayouts failed: HTTP {error.code}\n{error.read().decode(errors='replace')[:2000]}")
    except urllib.error.URLError as error:
        sys.exit(f"Could not reach Travelpayouts: {error.reason}")
    if not body.get("success", False):
        sys.exit(f"Travelpayouts returned an error: {json.dumps(body)[:2000]}")
    return body


def nights(item):
    try:
        out = dt.date.fromisoformat(item["departure_at"][:10])
        back = dt.date.fromisoformat(item["return_at"][:10])
    except (KeyError, TypeError, ValueError):
        return None
    return (back - out).days


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--origin", default="SYD")
    parser.add_argument("--dest", required=True, help="IATA city or airport code, e.g. TYO, PAR, CAN")
    parser.add_argument("--month", required=True, help="departure month YYYY-MM")
    parser.add_argument("--min-nights", type=int, default=12)
    parser.add_argument("--max-nights", type=int, default=17)
    parser.add_argument("--airline", help="keep only this IATA airline code, e.g. CZ or VA")
    parser.add_argument("--show", type=int, default=5)
    args = parser.parse_args()

    token = os.environ.get("TRAVELPAYOUTS_TOKEN", "")
    if not token:
        sys.exit("Set TRAVELPAYOUTS_TOKEN (free Travelpayouts account) first.")

    body = fetch({
        "origin": args.origin, "destination": args.dest,
        "departure_at": args.month, "one_way": "false", "direct": "false",
        "currency": "aud", "market": "au", "sorting": "price", "limit": 1000,
    }, token)
    currency = (body.get("currency") or "").upper()
    if currency != "AUD":
        sys.exit(f"Provider answered in {currency or 'an unlabelled currency'}, not AUD; refusing to show prices as A$.")

    asked_at = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    items = body.get("data") or []
    print(f"Asked {asked_at}: {args.origin} <-> {args.dest}, departing {args.month}, "
          f"{args.min_nights}-{args.max_nights} nights. {len(items)} cached fares returned.")

    to_europe = args.dest.upper() in EUROPE
    shown = rejected = 0
    for item in items:
        length = nights(item)
        if length is None or not args.min_nights <= length <= args.max_nights:
            continue
        if args.airline and item.get("airline") != args.airline.upper():
            continue
        status, reason = cached_route_check(item.get("airline"), item.get("transfers"),
                                            item.get("return_transfers"), to_europe)
        if status == "rejected":
            rejected += 1
            continue
        link = item.get("link")
        print()
        print(f"  A${item['price']}  (1 adult, return, economy — INDICATIVE, cached price)")
        print(f"  {item.get('origin_airport')} {item['departure_at']} -> {item.get('destination_airport')}"
              f", back {item['return_at']}  ({length} nights)")
        print(f"  Airline {item.get('airline')} {item.get('flight_number') or ''}; "
              f"stops out {item.get('transfers')}, back {item.get('return_transfers')}; "
              f"duration out {item.get('duration_to')} min, back {item.get('duration_back')} min")
        print(f"  Routing: {status} — {reason}")
        print(f"  View fare (live search, current price may differ): "
              f"{'https://www.aviasales.com' + link if link else 'no link returned'}")
        shown += 1
        if shown >= args.show:
            break
    print()
    print(f"Rejected for Middle East / Turkey transit: {rejected}.")
    if not shown:
        sys.exit("No practical fare found today for this search.")


if __name__ == "__main__":
    main()
