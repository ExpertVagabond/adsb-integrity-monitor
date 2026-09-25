"""GNSS interference screening (SYS-034).

When a GPS jammer is active, the aircraft it reaches lose position accuracy together: their
NACp and NIC drop in the same poll, in the same area. One aircraft dipping is usually its own
equipment. Several normally-healthy aircraft dipping at once, close together, is the signature
worth a human look.

An event is one airborne aircraft in one snapshot with NACp < 8 or NIC < 7 while its median over the
whole capture meets both minimums (so chronically-failing aircraft don't count as events).
A cluster is a set of events from the same snapshot connected by distance <= radius_nm, with at
least min_aircraft distinct aircraft.

This is a screen, not a detector: the flag means "look here", nothing more.
"""

import statistics

from . import rules, tracks

DEFAULT_RADIUS_NM = 30.0
DEFAULT_MIN_AIRCRAFT = 3


def _eligible(ac):
    # Aircraft on the ground are excluded: avionics powering up at the gate report zeros until GPS
    # locks, and several aircraft doing that at one airport would look exactly like a jammer.
    # ADS-R targets are excluded too: their NIC can be a converter default (see rules.ADSR_UNRELIABLE).
    return (ac.get("alt_baro") != "ground" and ac.get("type") != "adsr_icao"
            and rules.is_evaluated(ac) and not rules.is_surface_vehicle(ac) and not rules.is_pre_do260b(ac)
            and isinstance(ac.get("nac_p"), int) and isinstance(ac.get("nic"), int)
            and "lat" in ac and "lon" in ac and "hex" in ac)


def degradation_events(snapshots):
    """Return [(feed_time, hex, lat, lon, alt_baro, nac_p, nic), ...] for transient degradations."""
    history = {}
    for snap in snapshots:
        for ac in snap["ac"]:
            if _eligible(ac):
                h = history.setdefault(ac["hex"], ([], []))
                h[0].append(ac["nac_p"])
                h[1].append(ac["nic"])
    usual_ok = {hx: statistics.median(p) >= 8 and statistics.median(n) >= 7 for hx, (p, n) in history.items()}

    events = []
    for snap in snapshots:
        for ac in snap["ac"]:
            if _eligible(ac) and usual_ok.get(ac["hex"]) and (ac["nac_p"] < 8 or ac["nic"] < 7):
                events.append((snap["feed_time"], ac["hex"], ac["lat"], ac["lon"], ac.get("alt_baro"), ac["nac_p"], ac["nic"]))
    return events


def clusters(events, radius_nm=DEFAULT_RADIUS_NM, min_aircraft=DEFAULT_MIN_AIRCRAFT):
    """Group same-snapshot events into distance-connected clusters of >= min_aircraft aircraft."""
    by_time = {}
    for e in events:
        by_time.setdefault(e[0], []).append(e)
    found = []
    for t, evs in sorted(by_time.items()):
        unseen = list(range(len(evs)))
        while unseen:
            stack, comp = [unseen.pop()], []
            while stack:
                i = stack.pop()
                comp.append(evs[i])
                near = [j for j in unseen
                        if tracks.haversine_nm(evs[i][2], evs[i][3], evs[j][2], evs[j][3]) <= radius_nm]
                for j in near:
                    unseen.remove(j)
                stack.extend(near)
            if len({e[1] for e in comp}) >= min_aircraft:
                found.append({
                    "time": t,
                    "aircraft": sorted({e[1] for e in comp}),
                    "center": (statistics.fmean(e[2] for e in comp), statistics.fmean(e[3] for e in comp)),
                    "events": comp,
                })
    return found


def screen(snapshots, radius_nm=DEFAULT_RADIUS_NM, min_aircraft=DEFAULT_MIN_AIRCRAFT):
    events = degradation_events(snapshots)
    return {
        "events": len(events),
        "aircraft": len({e[1] for e in events}),
        "clusters": clusters(events, radius_nm, min_aircraft),
        "radius_nm": radius_nm,
        "min_aircraft": min_aircraft,
    }
