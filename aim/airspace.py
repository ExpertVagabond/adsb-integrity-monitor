"""Where the rule applies: 14 CFR 91.225(d) airspace (SYS-036).

91.227's minimums bind aircraft that are required to broadcast ADS-B Out, and 91.225(d) says where
that is (eCFR text, retrieved 2026-09-25):
  (1) Class B and Class C airspace;
  (2) within 30 NM of an Appendix D, Section 1 airport, from the surface up to 10,000 ft MSL;
  (3) above the ceiling and within the lateral boundaries of Class B or C, up to 10,000 ft MSL;
  (4) Class E at and above 10,000 ft MSL in the 48 states, excluding at and below 2,500 ft AGL.
(5), the Gulf of Mexico, doesn't touch the areas this project captures.

Data (free, no key): Class B/C boundaries from the FAA's ADDS open-data Class_Airspace layer, and
Appendix D airport reference points from the FAA US_Airport layer. `fetch` saves both to one JSON
file so analysis is reproducible offline.

Approximations, stated rather than hidden:
  * Barometric (pressure) altitude stands in for MSL altitude. They differ by the local altimeter
    setting, typically under a few hundred feet, which only matters right at a boundary.
  * (4) is applied as "at or above 10,000 ft"; the 2,500 ft AGL exclusion never binds in this
    region, where terrain is far below 7,500 ft.
  * Aircraft on the ground are placed at the surface (0 ft).
  * Class A (FL180 and above) is inside (4)'s altitude test, so it needs no separate check.
"""

import json
import urllib.parse
import urllib.request

from . import tracks

ADDS = "https://services6.arcgis.com/ssFJjBXIUyZDrSYZ/arcgis/rest/services"
VEIL_NM = 30.0
VEIL_TOP_FT = 10000
CLASS_E_FLOOR_FT = 10000

# Appendix D, Section 1 (eCFR 2026-09-01), by FAA location identifier.
APPENDIX_D_SECTION_1 = (
    "ATL", "BWI", "BOS", "ADW", "IAD", "CLT", "ORD", "CLE", "CVG", "DFW", "DEN", "DTW", "HNL", "IAH",
    "HOU", "MCI", "LAS", "LAX", "MEM", "MIA", "MSP", "EWR", "MSY", "JFK", "LGA", "MCO", "PHL", "PHX",
    "PIT", "STL", "SLC", "NKX", "SAN", "SFO", "SEA", "TPA", "DCA",
)


def _get(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": "adsb-integrity-monitor/0.2"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.load(resp)


def _feet(val, uom, code):
    if code == "SFC" or val is None:
        return 0.0
    return float(val) * (100.0 if uom == "FL" else 1.0)


def fetch(bbox, path):
    """Download Class B/C polygons inside bbox (west, south, east, north) and all Appendix D airports."""
    q = {
        "where": "CLASS IN ('B','C')",
        "geometry": ",".join(str(v) for v in bbox), "geometryType": "esriGeometryEnvelope",
        "inSR": "4326", "outSR": "4326", "spatialRel": "esriSpatialRelIntersects",
        "outFields": "IDENT,NAME,CLASS,LOWER_VAL,LOWER_UOM,LOWER_CODE,UPPER_VAL,UPPER_UOM,UPPER_CODE",
        "returnGeometry": "true", "f": "json",
    }
    areas = _get(f"{ADDS}/Class_Airspace/FeatureServer/0/query?" + urllib.parse.urlencode(q))
    idents = ",".join(f"'{i}'" for i in APPENDIX_D_SECTION_1)
    q2 = {"where": f"IDENT IN ({idents})", "outFields": "IDENT,NAME", "returnGeometry": "true", "outSR": "4326", "f": "json"}
    ports = _get(f"{ADDS}/US_Airport/FeatureServer/0/query?" + urllib.parse.urlencode(q2))

    data = {
        "source": "FAA ADDS open data: Class_Airspace and US_Airport layers",
        "bbox": list(bbox),
        "areas": [{
            "ident": f["attributes"]["IDENT"], "name": f["attributes"]["NAME"], "class": f["attributes"]["CLASS"],
            "lower_ft": _feet(f["attributes"]["LOWER_VAL"], f["attributes"]["LOWER_UOM"], f["attributes"]["LOWER_CODE"]),
            "upper_ft": _feet(f["attributes"]["UPPER_VAL"], f["attributes"]["UPPER_UOM"], f["attributes"]["UPPER_CODE"]),
            "rings": [[[round(x, 6), round(y, 6)] for x, y in ring] for ring in f["geometry"]["rings"]],
        } for f in areas.get("features", [])],
        "veil_airports": {f["attributes"]["IDENT"]: {"name": f["attributes"]["NAME"],
                                                    "lat": round(f["geometry"]["y"], 6), "lon": round(f["geometry"]["x"], 6)}
                          for f in ports.get("features", [])},
    }
    missing = sorted(set(APPENDIX_D_SECTION_1) - set(data["veil_airports"]))
    data["veil_airports_missing"] = missing
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, separators=(",", ":"))
    return data


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _inside(lon, lat, rings):
    """Even-odd ray casting across all rings, so holes work."""
    inside = False
    for ring in rings:
        n = len(ring)
        for i in range(n):
            x1, y1 = ring[i]
            x2, y2 = ring[(i + 1) % n]
            if (y1 > lat) != (y2 > lat) and lon < (x2 - x1) * (lat - y1) / (y2 - y1) + x1:
                inside = not inside
    return inside


def rule_basis(lat, lon, alt, data):
    """Return the 91.225(d) paragraph that requires ADS-B Out at this point, or None."""
    alt_ft = 0.0 if alt == "ground" else alt
    if not isinstance(alt_ft, (int, float)):
        return None
    if alt_ft >= CLASS_E_FLOOR_FT:
        return "91.225(d)(4)"
    for area in data["areas"]:
        if alt_ft >= area["lower_ft"] and _inside(lon, lat, area["rings"]):
            return "91.225(d)(1)" if alt_ft <= area["upper_ft"] else "91.225(d)(3)"
    for ap in data["veil_airports"].values():
        if alt_ft <= VEIL_TOP_FT and tracks.haversine_nm(lat, lon, ap["lat"], ap["lon"]) <= VEIL_NM:
            return "91.225(d)(2)"
    return None


def classify(snapshots, data):
    """{hex: paragraph} for every aircraft seen at least once inside 91.225(d) airspace."""
    out = {}
    for snap in snapshots:
        for ac in snap["ac"]:
            hx = ac.get("hex")
            if not hx or hx in out or "lat" not in ac or "lon" not in ac:
                continue
            basis = rule_basis(ac["lat"], ac["lon"], ac.get("alt_baro"), data)
            if basis:
                out[hx] = basis
    return out
