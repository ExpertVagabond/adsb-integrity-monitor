"""Track continuity across snapshots: dropouts and implausible position jumps.

Dropouts are judged by the aggregator's own clock (`seen_pos`), never by the gap between
our polls. An early version compared fix times across polls, and a single slow poll
(20.5 s instead of 10 s) turned 69 healthy tracks into false dropouts.
"""

import math

EARTH_RADIUS_NM = 3440.065
# SYS-031: no aircraft in civil airspace covers ground this fast; anything above it is a bad position.
MAX_PLAUSIBLE_KT = 1000.0
# SYS-030: ADS-B Out broadcasts position about twice a second. A position that has gone
# unrefreshed for 20 s means the network lost reception, not a normal update cycle.
DEFAULT_COAST_S = 20.0


def haversine_nm(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * EARTH_RADIUS_NM * math.asin(math.sqrt(a))


def position_fixes(snapshots):
    """Group position reports by ICAO address: {hex: [(t, lat, lon), ...]} sorted by time.

    t = feed_time - seen_pos, the time the position was actually received.
    Repeated reports of the same fix (unchanged between polls) are collapsed.
    """
    fixes = {}
    for snap in snapshots:
        for ac in snap["ac"]:
            if "lat" not in ac or "lon" not in ac or "hex" not in ac:
                continue
            t = snap["feed_time"] - float(ac.get("seen_pos", 0.0))
            fixes.setdefault(ac["hex"], []).append((round(t, 1), ac["lat"], ac["lon"]))
    return {hx: sorted(set(pts)) for hx, pts in fixes.items()}


def _staleness(snapshots, coast_s):
    """Per aircraft, the worst `seen_pos` above threshold and whether a newer position arrived later.

    Returns {hex: (worst_age_s, reacquired_bool)}.
    """
    worst, stale_fix_t, latest_fix_t = {}, {}, {}
    for snap in snapshots:
        for ac in snap["ac"]:
            hx, age = ac.get("hex"), ac.get("seen_pos")
            if not hx or not isinstance(age, (int, float)):
                continue
            fix_t = snap["feed_time"] - age
            latest_fix_t[hx] = max(fix_t, latest_fix_t.get(hx, fix_t))
            if age > coast_s and age >= worst.get(hx, 0.0):
                worst[hx], stale_fix_t[hx] = age, fix_t
    # Reacquired = a position received more than a second after the stale one.
    return {hx: (age, latest_fix_t[hx] > stale_fix_t[hx] + 1.0) for hx, age in worst.items()}


def stale_positions(snapshots, coast_s):
    """SYS-030 (a): aircraft whose position went stale past the threshold and later refreshed."""
    return {hx: age for hx, (age, reacq) in _staleness(snapshots, coast_s).items() if reacq}


def lost_tracks(snapshots, coast_s=DEFAULT_COAST_S):
    """SYS-032: aircraft whose position went stale and never refreshed within the window.

    These are usually landings or aircraft leaving coverage, so they are reported
    separately and never counted as dropouts.
    """
    return {
        hx: f"last position {age:.0f} s old when last seen; not reacquired in the window"
        for hx, (age, reacq) in _staleness(snapshots, coast_s).items()
        if not reacq
    }


def disappearances(snapshots):
    """SYS-030 (b): aircraft missing from one or more snapshots between two appearances.

    Returns {hex: [(missing_count, seconds), ...]}; seconds spans the last snapshot
    before the gap to the first one after it.
    """
    seen_at = {}
    for i, snap in enumerate(snapshots):
        for ac in snap["ac"]:
            if "hex" in ac:
                seen_at.setdefault(ac["hex"], []).append(i)
    out = {}
    for hx, idx in seen_at.items():
        for a, b in zip(idx, idx[1:]):
            if b - a > 1:
                span = snapshots[b]["feed_time"] - snapshots[a]["feed_time"]
                out.setdefault(hx, []).append((b - a - 1, span))
    return out


def position_jumps(fixes, max_kt=MAX_PLAUSIBLE_KT):
    """SYS-031: consecutive fixes implying a ground speed above `max_kt`."""
    out = {}
    for hx, pts in fixes.items():
        for (t1, la1, lo1), (t2, la2, lo2) in zip(pts, pts[1:]):
            dt = t2 - t1
            if dt <= 0:
                continue
            speed_kt = haversine_nm(la1, lo1, la2, lo2) / (dt / 3600.0)
            if speed_kt > max_kt:
                out.setdefault(hx, []).append((speed_kt, dt))
    return out


def continuity_findings(snapshots, coast_s=DEFAULT_COAST_S, max_kt=MAX_PLAUSIBLE_KT):
    """Return {hex: [finding strings]} for dropouts (SYS-030) and position jumps (SYS-031)."""
    findings = {}
    for hx, age in stale_positions(snapshots, coast_s).items():
        findings.setdefault(hx, []).append(f"dropout: position went at least {age:.0f} s without a refresh, then reacquired (threshold {coast_s:.0f} s)")
    for hx, gaps in disappearances(snapshots).items():
        for missing, span in gaps:
            findings.setdefault(hx, []).append(f"dropout: absent from {missing} snapshot(s), {span:.0f} s between sightings")
    for hx, jumps in position_jumps(position_fixes(snapshots), max_kt).items():
        for speed_kt, dt in jumps:
            findings.setdefault(hx, []).append(f"position jump: implied {speed_kt:,.0f} kt over {dt:.1f} s")
    return findings
