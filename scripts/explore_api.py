"""One-off: print the raw shape of Travelpayouts responses (token never printed)."""
import json, os, sys, urllib.error, urllib.parse, urllib.request

TOKEN = os.environ["TRAVELPAYOUTS_TOKEN"]
BASE = "https://api.travelpayouts.com"
CALLS = [
    ("one-way SYD-ADL 24 Nov, all airlines", "/aviasales/v3/prices_for_dates", dict(origin="SYD", destination="ADL", departure_at="2026-11-24", one_way="true", direct="false", currency="aud", market="au", sorting="price", limit=50)),
    ("one-way SYD-ADL 24 Nov, unique=false", "/aviasales/v3/prices_for_dates", dict(origin="SYD", destination="ADL", departure_at="2026-11-24", one_way="true", currency="aud", market="au", sorting="price", unique="false", limit=50)),
    ("one-way SYD-ADL Nov 2026", "/aviasales/v3/prices_for_dates", dict(origin="SYD", destination="ADL", departure_at="2026-11", one_way="true", currency="aud", market="au", sorting="price", limit=100)),
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
    for item in items[:40]:
        print({k: item.get(k) for k in ('departure_at','airline','flight_number','price','transfers','gate')}, (item.get('link') or '')[:120])
