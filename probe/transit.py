"""Transit restriction: no itinerary may touch an airport in the Middle East or Turkey.

Checked by airport country (not by airline), on every segment endpoint and every technical stop,
outbound and inbound, so codeshares and overnight connections are covered.
"""

# ISO 3166-1 alpha-2 codes. Egypt is included by default (owner to confirm).
EXCLUDED_COUNTRIES = {
    "AE": "United Arab Emirates",
    "QA": "Qatar",
    "BH": "Bahrain",
    "SA": "Saudi Arabia",
    "OM": "Oman",
    "KW": "Kuwait",
    "JO": "Jordan",
    "LB": "Lebanon",
    "IL": "Israel",
    "IR": "Iran",
    "IQ": "Iraq",
    "SY": "Syria",
    "YE": "Yemen",
    "TR": "Türkiye",
    "EG": "Egypt",
}


def _airports(segment):
    yield segment["origin"]
    yield segment["destination"]
    for stop in segment.get("stops") or []:
        yield stop["airport"]


def transit_violations(offer):
    """Return the excluded airports an offer touches, e.g. ["DOH (Qatar)"]; empty if it complies.

    `offer` is a Duffel offer (slices -> segments -> origin/destination/stops, each airport carrying
    iata_code and iata_country_code). An airport without a country code is reported as a violation,
    because compliance cannot be proven.
    """
    found = []
    for slice_ in offer["slices"]:
        for segment in slice_["segments"]:
            for airport in _airports(segment):
                country = airport.get("iata_country_code")
                code = airport.get("iata_code", "?")
                if country is None:
                    label = f"{code} (country unknown)"
                elif country in EXCLUDED_COUNTRIES:
                    label = f"{code} ({EXCLUDED_COUNTRIES[country]})"
                else:
                    continue
                if label not in found:
                    found.append(label)
    return found


# Carriers based in the excluded region: any itinerary they sell connects in their hub.
EXCLUDED_CARRIERS = {
    "EK": "Emirates", "FZ": "flydubai", "QR": "Qatar Airways", "EY": "Etihad", "G9": "Air Arabia",
    "GF": "Gulf Air", "WY": "Oman Air", "SV": "Saudia", "XY": "flynas", "KU": "Kuwait Airways",
    "J9": "Jazeera Airways", "RJ": "Royal Jordanian", "ME": "Middle East Airlines", "LY": "El Al",
    "IR": "Iran Air", "W5": "Mahan Air", "IA": "Iraqi Airways", "TK": "Turkish Airlines",
    "PC": "Pegasus", "XQ": "SunExpress", "MS": "EgyptAir",
}


def cached_route_check(airline, transfers, return_transfers, to_europe):
    """Transit check for cached fares, which give the airline and stop counts but no airports.

    Returns (status, reason) with status "complies", "rejected" or "unverified".
    """
    if airline in EXCLUDED_CARRIERS:
        return "rejected", f"{EXCLUDED_CARRIERS[airline]} connects through its home hub"
    if transfers == 0 and return_transfers == 0:
        return "complies", "non-stop both ways"
    if airline == "VA" and to_europe:
        # Virgin Australia's own Europe flights are operated by Qatar Airways via Doha.
        return "rejected", "Virgin Australia to Europe connects via Doha (Qatar Airways-operated)"
    return "unverified", "connection airports not given by the cached source — check before buying"
