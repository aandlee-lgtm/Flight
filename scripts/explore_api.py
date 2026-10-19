"""One-off: print the raw shape of Travelpayouts responses (token never printed)."""
import json, os, sys, urllib.error, urllib.parse, urllib.request

TOKEN = os.environ["TRAVELPAYOUTS_TOKEN"]
BASE = "https://api.travelpayouts.com"
CALLS = [
    ("v3 prices_for_dates month", "/aviasales/v3/prices_for_dates", dict(origin="SYD", destination="TYO", departure_at="2027-01", one_way="false", currency="aud", market="au", sorting="price", limit=3)),
    ("v3 prices_for_dates any date", "/aviasales/v3/prices_for_dates", dict(origin="SYD", destination="LON", one_way="false", currency="aud", market="au", sorting="price", limit=3)),
    ("v3 get_latest_prices", "/aviasales/v3/get_latest_prices", dict(origin="SYD", destination="TYO", currency="aud", period_type="year", one_way="false", sorting="price", limit=3)),
    ("v2 prices/latest", "/v2/prices/latest", dict(origin="SYD", destination="TYO", currency="aud", period_type="year", one_way="false", limit=3, show_to_affiliates="true")),
    ("v2 month-matrix", "/v2/prices/month-matrix", dict(origin="SYD", destination="TYO", currency="aud", month="2027-01-01", show_to_affiliates="true")),
    ("v3 grouped_prices", "/aviasales/v3/grouped_prices", dict(origin="SYD", destination="PAR", currency="aud", departure_at="2027-03", group_by="departure_at", market="au")),
]
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
    for item in items[:2]:
        print(json.dumps(item, ensure_ascii=False)[:1500])
