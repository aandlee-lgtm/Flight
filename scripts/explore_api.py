"""One-off: print the raw shape of Travelpayouts responses (token never printed)."""
import json, os, sys, urllib.error, urllib.parse, urllib.request

TOKEN = os.environ["TRAVELPAYOUTS_TOKEN"]
BASE = "https://api.travelpayouts.com"
CALLS = [
    ("v3 prices_for_dates trip_class=1", "/aviasales/v3/prices_for_dates", dict(origin="SYD", destination="LON", departure_at="2027-02", one_way="false", currency="aud", market="au", sorting="price", limit=5, trip_class=1)),
    ("v3 prices_for_dates trip_class=0 (control)", "/aviasales/v3/prices_for_dates", dict(origin="SYD", destination="LON", departure_at="2027-02", one_way="false", currency="aud", market="au", sorting="price", limit=5, trip_class=0)),
    ("v2 latest trip_class=1", "/v2/prices/latest", dict(origin="SYD", destination="LON", currency="aud", period_type="year", one_way="false", limit=5, trip_class=1, show_to_affiliates="true")),
    ("v1 cheap trip_class=1", "/v1/prices/cheap", dict(origin="SYD", destination="LON", currency="aud", trip_class=1)),
    ("v3 prices_for_dates trip_class=1 TYO", "/aviasales/v3/prices_for_dates", dict(origin="SYD", destination="TYO", one_way="false", currency="aud", market="au", sorting="price", limit=5, trip_class=1)),
    ("v3 prices_for_dates trip_class=2 (premium?)", "/aviasales/v3/prices_for_dates", dict(origin="SYD", destination="TYO", one_way="false", currency="aud", market="au", sorting="price", limit=5, trip_class=2)),
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
    for item in items[:3]:
        print(json.dumps(item, ensure_ascii=False)[:700])
