"""Independent check of the altitude trend against a weather model (SYS-035).

A barometric altimeter set to 29.92 inHg reads *pressure altitude*: the height a pressure level
would have in the ICAO standard atmosphere. 500 hPa, for example, always reads 18,289 ft. The real
atmosphere puts that level higher on warm days and lower on cold ones. A weather model gives the
actual height of each pressure level, so for every level:

    true height - pressure altitude  ~=  geometric altitude - barometric altitude

The right-hand side is exactly what aim/altitude.py measures from aircraft. If the aircraft-derived
trend matches the weather model, the altitude check is confirmed by physics, not just by internal
consistency. Source: Open-Meteo (free, no key), geopotential height at standard pressure levels.

Two approximations: geopotential height is used for true height (differs by well under 1% below
45,000 ft), and ADS-B geometric altitude is compared as if it were above mean sea level. DO-260B
defines it above the WGS-84 ellipsoid, which around New Jersey sits 32.8 m (108 ft) above sea level
(NOAA GEOID18). If the whole fleet followed that definition, the aircraft trend would sit a steady
~108 ft below the model. The first capture showed an offset of that size; a second, larger capture
showed almost none. So the offset is unresolved, and the check is judged on shape and median agreement.
"""

import datetime as dt
import json
import math
import statistics
import urllib.parse
import urllib.request

API = "https://api.open-meteo.com/v1/forecast"
LEVELS_HPA = (925, 850, 700, 600, 500, 400, 300, 250, 200)
M_TO_FT = 3.28084


def pressure_altitude_ft(hpa):
    """ICAO standard atmosphere pressure altitude (valid in the troposphere and up to ~65,000 ft)."""
    if hpa >= 226.32:  # troposphere, below 36,089 ft
        return 145366.45 * (1.0 - (hpa / 1013.25) ** 0.190284)
    # isothermal lower stratosphere
    return 36089.24 + 20805.8 * math.log(226.32 / hpa)


def model_hour(when_utc):
    """The whole UTC hour nearest `when_utc`: the model output actually compared."""
    t = dt.datetime.fromtimestamp(when_utc, dt.timezone.utc)
    return t.replace(minute=0, second=0, microsecond=0) + dt.timedelta(hours=1 if t.minute >= 30 else 0)


def fetch_heights(lat, lon, when_utc, timeout=20):
    """Return {hPa: geopotential height in metres} for the hour nearest `when_utc` (epoch seconds)."""
    day = dt.datetime.fromtimestamp(when_utc, dt.timezone.utc).strftime("%Y-%m-%d")
    params = {
        "latitude": f"{lat:.3f}", "longitude": f"{lon:.3f}", "timezone": "UTC",
        "start_date": day, "end_date": day,
        "hourly": ",".join(f"geopotential_height_{p}hPa" for p in LEVELS_HPA),
    }
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "adsb-integrity-monitor/0.2"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = json.load(resp)
    hourly = body["hourly"]
    stamp = model_hour(when_utc).strftime("%Y-%m-%dT%H:00")
    i = hourly["time"].index(stamp) if stamp in hourly["time"] else 0
    return {p: hourly[f"geopotential_height_{p}hPa"][i] for p in LEVELS_HPA
            if hourly.get(f"geopotential_height_{p}hPa") and hourly[f"geopotential_height_{p}hPa"][i] is not None}


def compare(fit, heights_m, alt_range_ft):
    """Compare the ADS-B trend (from altitude.altitude_findings) with the weather model.

    Only levels inside the altitude range the aircraft actually covered are compared.
    Returns {"rows": [(hPa, pressure_alt_ft, model_ft, adsb_ft, disagreement_ft)], "median_abs_ft", "max_abs_ft"}.
    """
    lo, hi = alt_range_ft
    rows = []
    for hpa, z_m in sorted(heights_m.items(), reverse=True):
        pa = pressure_altitude_ft(hpa)
        if not lo <= pa <= hi:
            continue
        model = z_m * M_TO_FT - pa
        adsb = fit["intercept_ft"] + fit["slope_ft_per_1000"] * pa / 1000.0
        rows.append((hpa, pa, model, adsb, adsb - model))
    if not rows:
        return {"rows": [], "median_abs_ft": None, "max_abs_ft": None}
    dis = [abs(r[4]) for r in rows]
    return {"rows": rows, "median_abs_ft": statistics.median(dis), "max_abs_ft": max(dis)}


def to_markdown(check, when_utc, lat, lon):
    lines = ["## Independent check: weather model", "",
             f"Open-Meteo geopotential heights near {lat:.2f}N {abs(lon):.2f}W for "
             f"{model_hour(when_utc):%Y-%m-%d %H:00} UTC (the model hour nearest the capture midpoint). "
             "The model's true height minus pressure altitude should match the aircraft-derived trend of "
             "geometric minus barometric altitude.", ""]
    if not check["rows"]:
        lines.append("No pressure levels fell inside the altitude range of this capture.")
        return "\n".join(lines) + "\n"
    lines += ["| Level | Pressure altitude | Weather model | ADS-B trend | Difference |", "|---|---|---|---|---|"]
    lines += [f"| {h} hPa | {pa:,.0f} ft | {m:+,.0f} ft | {a:+,.0f} ft | {d:+,.0f} ft |" for h, pa, m, a, d in check["rows"]]
    lines += ["", f"Median disagreement {check['median_abs_ft']:.0f} ft, largest {check['max_abs_ft']:.0f} ft.", ""]
    return "\n".join(lines)
