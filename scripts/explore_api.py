"""One-off: print the raw shape of Travelpayouts responses (token never printed)."""
import json, os, sys, urllib.error, urllib.parse, urllib.request

TOKEN = os.environ["TRAVELPAYOUTS_TOKEN"]
BASE = "https://api.travelpayouts.com"
CALLS = [('v3 any-date PAR market=au', '/aviasales/v3/prices_for_dates', {'origin': 'SYD', 'destination': 'PAR', 'one_way': 'false', 'currency': 'aud', 'sorting': 'price', 'limit': 1000, 'market': 'au'}), ('v3 any-date PAR market=None', '/aviasales/v3/prices_for_dates', {'origin': 'SYD', 'destination': 'PAR', 'one_way': 'false', 'currency': 'aud', 'sorting': 'price', 'limit': 1000}), ('v3 any-date CDG market=au', '/aviasales/v3/prices_for_dates', {'origin': 'SYD', 'destination': 'CDG', 'one_way': 'false', 'currency': 'aud', 'sorting': 'price', 'limit': 1000, 'market': 'au'}), ('v3 any-date CDG market=None', '/aviasales/v3/prices_for_dates', {'origin': 'SYD', 'destination': 'CDG', 'one_way': 'false', 'currency': 'aud', 'sorting': 'price', 'limit': 1000}), ('v3 any-date ORY market=au', '/aviasales/v3/prices_for_dates', {'origin': 'SYD', 'destination': 'ORY', 'one_way': 'false', 'currency': 'aud', 'sorting': 'price', 'limit': 1000, 'market': 'au'}), ('v3 any-date ORY market=None', '/aviasales/v3/prices_for_dates', {'origin': 'SYD', 'destination': 'ORY', 'one_way': 'false', 'currency': 'aud', 'sorting': 'price', 'limit': 1000}), ('v3 get_latest_prices PAR year', '/aviasales/v3/get_latest_prices', {'origin': 'SYD', 'destination': 'PAR', 'currency': 'aud', 'period_type': 'year', 'one_way': 'false', 'sorting': 'price', 'limit': 1000}), ('v2 latest PAR', '/v2/prices/latest', {'origin': 'SYD', 'destination': 'PAR', 'currency': 'aud', 'period_type': 'year', 'one_way': 'false', 'limit': 1000, 'show_to_affiliates': 'false'})]
for label, path, params in CALLS:
    url = BASE + path + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"X-Access-Token": TOKEN, "Accept-Encoding": "identity"})
    print(f"\n===== {label}  {path}  {json.dumps(params)}")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            body = json.load(r)
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, e.read().decode(errors="replace")[:500]); continue
    except Exception as e:
        print("ERROR", repr(e)); continue
    print("top-level keys:", sorted(body) if isinstance(body, dict) else type(body).__name__)
    data = body.get("data") if isinstance(body, dict) else body
    items = list(data.values()) if isinstance(data, dict) else (data or [])
    print("currency:", body.get("currency") if isinstance(body, dict) else None, "| items:", len(items))
    import collections
    found=collections.Counter((i.get('found_at') or (i.get('link') or '').split('search_date=')[-1][:8])[:10] for i in items)
    print('found dates:', dict(sorted(found.items())[-6:]))
    for item in items[:0]:
        print(json.dumps(item, ensure_ascii=False)[:700])
