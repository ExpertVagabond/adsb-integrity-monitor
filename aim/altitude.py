"""Altitude consistency: barometric vs geometric (GNSS) altitude (SYS-033).

Every ADS-B aircraft reports two altitudes: barometric (what the altimeter and ATC use)
and geometric (from GNSS). Their difference isn't constant. It grows with height because
the real atmosphere is warmer or colder than the standard one, and it shifts with local
weather. An aircraft is only suspicious if it disagrees with the air it is flying in.

Two stages:
  1. Global trend. Fit difference = a + b * altitude across all airborne aircraft with
     Theil-Sen (median of pairwise slopes), which ignores the outliers we're hunting.
  2. Local comparison. Take each aircraft's leftover from that trend and subtract the median
     leftover of its neighbors: the 8 aircraft nearest in altitude within 75 NM and 10,000 ft.
     This absorbs weather gradients across the area and curvature the straight line misses.

Why two stages: on a 100 NM capture the straight line alone flagged a B789 and an LJ60 at
37,000 ft, both +207/+214 ft, i.e. the model, not the aircraft. Neighbors alone either drop
aircraft (narrow window) or re-inherit the altitude slope (wide window).

Aircraft are only assessed when their neighbors bracket them (some above, some below). At the top
or bottom of the traffic every neighbor sits on one side, so any curvature the line missed turns
into a bias: an E55P at 41,000 ft came out -222 ft off before this rule.

Calibration (threshold 200 ft): morning 60 NM capture p99 144 ft, max 226 ft, the one aircraft
also broadcasting NACp/NIC/SIL = 0. First 15 minutes of the 100 NM capture: 215 of 237 assessed,
p99 111 ft, max 128 ft, nothing flagged.
"""

import statistics

from . import tracks

DEFAULT_THRESHOLD_FT = 200
MIN_ALTITUDE_FT = 1000     # below this, ground effects and rounding dominate
MIN_AIRCRAFT = 10          # too few aircraft and the fit means nothing
NEIGHBORS = 8
NEIGHBOR_RADIUS_NM = 75.0
NEIGHBOR_ALT_FT = 10000
MIN_NEIGHBORS = 4          # fewer than this: not assessed (a sparse comparison would re-admit weather)


def theil_sen(points):
    """Robust line fit. points: [(x, y), ...]. Returns (intercept, slope)."""
    slopes = [
        (y2 - y1) / (x2 - x1)
        for i, (x1, y1) in enumerate(points)
        for (x2, y2) in points[i + 1:]
        if x2 != x1
    ]
    if not slopes:
        raise ValueError("need at least two distinct x values")
    slope = statistics.median(slopes)
    intercept = statistics.median(y - slope * x for x, y in points)
    return intercept, slope


def altitude_findings(merged, threshold_ft=DEFAULT_THRESHOLD_FT, min_aircraft=MIN_AIRCRAFT):
    """Return (findings, fit).

    findings: {hex: description} for aircraft more than threshold_ft off their neighbors.
    fit: {"intercept_ft", "slope_ft_per_1000", "n", "local"} or None when there's too little data.
    """
    pts = {}
    for hx, ac in merged.items():
        baro, geom = ac.get("alt_baro"), ac.get("alt_geom")
        if isinstance(baro, int) and isinstance(geom, int) and baro >= MIN_ALTITUDE_FT:
            pts[hx] = (baro, geom - baro, ac.get("lat"), ac.get("lon"))
    if len(pts) < min_aircraft:
        return {}, None
    a, b = theil_sen([(p[0], p[1]) for p in pts.values()])
    trend = {hx: p[1] - (a + b * p[0]) for hx, p in pts.items()}

    findings, local_count = {}, 0
    for hx, (baro, diff, lat, lon) in pts.items():
        near = []
        if lat is not None and lon is not None:
            near = [
                (abs(q[0] - baro), other) for other, q in pts.items()
                if other != hx and abs(q[0] - baro) <= NEIGHBOR_ALT_FT and q[2] is not None and q[3] is not None
                and tracks.haversine_nm(lat, lon, q[2], q[3]) <= NEIGHBOR_RADIUS_NM
            ]
        near = [other for _, other in sorted(near)[:NEIGHBORS]]
        if len(near) < MIN_NEIGHBORS:
            continue  # not assessed: too few aircraft sharing its air to compare against
        if not (any(pts[o][0] > baro for o in near) and any(pts[o][0] < baro for o in near)):
            continue  # not assessed: at the top or bottom of the traffic, neighbors on one side only
        local_count += 1
        residual = trend[hx] - statistics.median(trend[o] for o in near)
        if abs(residual) > threshold_ft:
            findings[hx] = (
                f"altitude: geometric minus barometric is {diff:+,} ft at {baro:,} ft, "
                f"{residual:+,.0f} ft off its {len(near)} nearest neighbors (threshold {threshold_ft:.0f} ft)"
            )
    return findings, {"intercept_ft": a, "slope_ft_per_1000": b * 1000, "n": len(pts),
                      "local": local_count, "not_assessed": len(pts) - local_count,
                      "max_alt_ft": max(p[0] for p in pts.values())}
