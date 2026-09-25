"""Analysis and reporting: turn a capture into per-aircraft results, a Markdown report and a CSV."""

import csv
import datetime as dt
import hashlib
import statistics
from collections import Counter

from . import airspace, altitude, interference, rules, stats, tracks

DISCLAIMER = (
    "Source data is crowdsourced ADS-B from adsb.lol volunteer receivers. Results describe "
    "what public receivers decoded during the capture window. They are not an FAA compliance "
    "determination, and a single missing or degraded report can have many causes."
)  # SYS-042


def merge_latest(snapshots):
    """Collapse all snapshots into one record per aircraft, keeping each field's latest value."""
    merged = {}
    for snap in snapshots:  # oldest first, so later values overwrite earlier ones
        for ac in snap["ac"]:
            hx = ac.get("hex")
            if not hx:
                continue
            rec = merged.setdefault(hx, {})
            for k, v in ac.items():
                if v is not None:
                    rec[k] = v
    return merged


def indicator_history(snapshots):
    """Every reported value of each 91.227(c)(1) indicator and the ADS-B version, per aircraft, in time order."""
    fields = [f for f, *_ in rules.PERFORMANCE_CHECKS] + ["version"]
    hist = {}
    for snap in snapshots:
        for ac in snap["ac"]:
            hx = ac.get("hex")
            if not hx:
                continue
            h = hist.setdefault(hx, {f: [] for f in fields})
            for f in fields:
                if isinstance(ac.get(f), int):
                    h[f].append(ac[f])
    return hist


def typical_value(values):
    """SYS-019: most frequent value; ties go to the most recent. None if never reported."""
    if not values:
        return None
    counts = Counter(values)
    top = max(counts.values())
    return next(v for v in reversed(values) if counts[v] == top)


def unstable_indicators(history, excluded=()):
    """Indicators that alternated between passing and failing values during the window."""
    notes = []
    for field, minimum, _para, _bound in rules.PERFORMANCE_CHECKS:
        if field in excluded:
            continue
        vals = history.get(field, [])
        flips = sum(1 for a, b in zip(vals, vals[1:]) if (a >= minimum) != (b >= minimum))
        if flips:
            notes.append(f"{field} alternated between {min(vals)} and {max(vals)} ({flips} change{'s' if flips > 1 else ''})")
    return notes


def highest_altitude(snapshots):
    """Highest barometric altitude seen per aircraft; "ground" if it was never airborne."""
    out = {}
    for snap in snapshots:
        for ac in snap["ac"]:
            hx, alt = ac.get("hex"), ac.get("alt_baro")
            if not hx or alt is None:
                continue
            prev = out.get(hx)
            if isinstance(alt, int):
                out[hx] = alt if not isinstance(prev, int) else max(prev, alt)
            elif prev is None:
                out[hx] = alt
    return out


def analyze(snapshots, coast_s=tracks.DEFAULT_COAST_S, alt_threshold_ft=altitude.DEFAULT_THRESHOLD_FT, airspace_data=None,
            registry_data=None):
    """Return the full analysis dict used by every report writer."""
    merged = merge_latest(snapshots)
    continuity = tracks.continuity_findings(snapshots, coast_s)
    track_ends = tracks.lost_tracks(snapshots, coast_s)
    highest = highest_altitude(snapshots)
    history = indicator_history(snapshots)
    seen = Counter(ac.get("hex") for snap in snapshots for ac in snap["ac"])
    rule = airspace.classify(snapshots, airspace_data) if airspace_data else None

    excluded = Counter()
    aircraft = []
    for hx, ac in sorted(merged.items()):
        if not rules.is_evaluated(ac):
            excluded[ac.get("type", "unknown")] += 1
            continue
        if rules.is_surface_vehicle(ac):
            excluded["surface vehicle"] += 1
            continue
        unstable = []
        h = history.get(hx, {})
        judged = dict(ac)
        # SYS-017/SYS-019: the ADS-B version is judged like the indicators, by its most frequent value.
        # On the 1-hour capture, 34 of 36 aircraft whose *last* poll said version 0 said version 2 in most polls.
        judged["version"] = typical_value(h.get("version", [])) if h.get("version") else ac.get("version")
        ac = judged
        if rules.is_pre_do260b(judged):
            checks, verdict = [], "not evaluable"
        else:
            for field, *_ in rules.PERFORMANCE_CHECKS:
                judged[field] = typical_value(h.get(field, []))
            checks = rules.check_performance(judged)
            unstable = unstable_indicators(h, excluded=rules.ADSR_UNRELIABLE if ac.get("type") == "adsr_icao" else ())
            fails = [c for c in checks if c["status"] == rules.FAIL]
            missing = [c for c in checks if c["status"] == rules.NOT_REPORTED]
            verdict = "fail" if fails else ("incomplete" if missing else "pass")
        aircraft.append({
            "key": hx,  # stays the real address after redaction; never written to outputs
            "hex": hx,
            "flight": (ac.get("flight") or "").strip(),
            "reg": ac.get("r", ""),
            "type_code": ac.get("t", ""),
            "report_type": ac.get("type"),
            "version": ac.get("version"),
            "checks": checks,
            "on_ground": ac.get("alt_baro") == "ground",
            "verdict": verdict,
            "version_note": rules.check_version(ac),
            "emergency": rules.check_emergency(ac),
            "continuity": continuity.get(hx, []),
            "track_end": track_ends.get(hx),
            "category": ac.get("category"),
            "unstable": unstable,
            "polls_seen": seen.get(hx, 0),
            "rule_airspace": None if rule is None else rule.get(hx, ""),
            "year_mfr": (registry_data or {}).get(hx, {}).get("year_mfr", "") if registry_data else None,
            "build_cert": (registry_data or {}).get(hx, {}).get("build_cert", "") if registry_data else None,
            "alt_baro": highest.get(hx),
        })

    evaluated = {a["key"]: merged[a["key"]] for a in aircraft}
    alt_findings, alt_fit = altitude.altitude_findings(evaluated, alt_threshold_ft)
    for a in aircraft:
        a["altitude"] = alt_findings.get(a["key"])

    times = [s["feed_time"] for s in snapshots]
    return {
        "window_start": min(times) if times else None,
        "window_end": max(times) if times else None,
        "snapshots": len(snapshots),
        "coast_s": coast_s,
        "aircraft": aircraft,
        "excluded": dict(excluded),
        "alt_fit": alt_fit,
        "alt_threshold_ft": alt_threshold_ft,
        "stats": stats.fleet_stats(aircraft, with_registry=registry_data is not None),
        "interference": interference.screen(snapshots),
        "airspace_checked": rule is not None,
    }


def redact(result):
    """SYS-043: replace ICAO address, callsign and registration with a stable pseudonym.

    The same aircraft always gets the same pseudonym, so findings stay linkable across
    reports without naming the owner. Aircraft type is kept; it identifies no one.
    """
    for a in result["aircraft"]:
        alias = "AC-" + hashlib.sha256(a["hex"].encode()).hexdigest()[:6].upper()
        a["hex"], a["flight"], a["reg"] = alias, "", ""
    result["redacted"] = True
    return result


def _is_unstable(a, field):
    return any(note.startswith(field + " ") for note in a.get("unstable", []))


def _utc(ts):
    return dt.datetime.fromtimestamp(ts, dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC") if ts else "n/a"


def _label(a):
    parts = (a["flight"], f"({a['reg']})" if a["reg"] else "", a["type_code"], "[on ground]" if a.get("on_ground") else "")
    return " ".join(x for x in parts if x) or "unidentified"


def capture_center(snapshots):
    """Median position of every aircraft report: the center used for the weather check."""
    lats = [ac["lat"] for snap in snapshots for ac in snap["ac"] if "lat" in ac]
    lons = [ac["lon"] for snap in snapshots for ac in snap["ac"] if "lon" in ac]
    return statistics.median(lats), statistics.median(lons)


def to_markdown(result, area_desc):
    """SYS-040: human-readable report. Every failure cites its regulation paragraph."""
    ac = result["aircraft"]
    verdicts = Counter(a["verdict"] for a in ac)
    lines = [
        "# ADS-B Integrity Report",
        "",
        f"- **Area:** {area_desc}",
        f"- **Window:** {_utc(result['window_start'])} to {_utc(result['window_end'])} ({result['snapshots']} snapshots)",
        f"- **Aircraft:** {len(ac)} (direct ADS-B and ADS-R reports)",
        f"- **Excluded:** {sum(result['excluded'].values())}"
        + (" (" + ", ".join(f"{k}: {v}" for k, v in sorted(result["excluded"].items())) + ")" if result["excluded"] else " (no MLAT, TIS-B, Mode S-only or surface-vehicle targets in the window)"),
        "",
        f"> {DISCLAIMER}" + (" Aircraft identities are replaced with stable pseudonyms." if result.get("redacted") else ""),
        "",
        "## Summary against 14 CFR 91.227(c)(1)",
        "",
        "| Verdict | Aircraft |",
        "|---|---|",
        f"| All five indicators meet the minimum | {verdicts.get('pass', 0)} |",
        f"| At least one indicator below the minimum | {verdicts.get('fail', 0)} |",
        f"| No failures, but at least one indicator not reported | {verdicts.get('incomplete', 0)} |",
        f"| Not evaluable: pre-DO-260B transmitter | {verdicts.get('not evaluable', 0)} |",
        "",
        "| Indicator | Requirement | Pass | Fail | Not reported | Excluded (ADS-R converter) |",
        "|---|---|---|---|---|---|",
    ]
    for field, _, para, bound in rules.PERFORMANCE_CHECKS:
        c = Counter(ch["status"] for a in ac for ch in a["checks"] if ch["field"] == field)
        lines.append(f"| {field} | {para}: {bound} | {c.get(rules.PASS, 0)} | {c.get(rules.FAIL, 0)} | "
                     f"{c.get(rules.NOT_REPORTED, 0)} | {c.get(rules.EXCLUDED, 0)} |")

    if result.get("airspace_checked"):
        in_rule = [a for a in ac if a["rule_airspace"]]
        fail_in = [a for a in ac if a["verdict"] == "fail" and a["rule_airspace"]]
        lines += ["", f"**Rule applicability (14 CFR 91.225(d)):** {len(in_rule)} of {len(ac)} aircraft were in airspace where "
                  f"ADS-B Out is required at some point in the window; {len(fail_in)} of the "
                  f"{sum(1 for a in ac if a['verdict'] == 'fail')} below a minimum were among them."]

    fails = [a for a in ac if a["verdict"] == "fail"]
    lines += ["", "## Aircraft below a 91.227(c)(1) minimum", ""]
    if fails:
        lines += ["| Aircraft | ICAO | Finding |", "|---|---|---|"]
        for a in fails:
            for ch in a["checks"]:
                if ch["status"] == rules.FAIL:
                    shaky = " **unstable: value alternated, low confidence**" if _is_unstable(a, ch["field"]) else ""
                    if a.get("rule_airspace"):
                        shaky += f" · in {a['rule_airspace']} airspace"
                    elif a.get("rule_airspace") == "":
                        shaky += " · not seen in 91.225(d) airspace"
                    lines.append(f"| {_label(a)} | {a['hex']} | {ch['field']} = {ch['value']}, needs {ch['bound']} ({ch['para']}){shaky} |")
    else:
        lines.append("None in this window.")

    emerg = [a for a in ac if a["emergency"]]
    lines += ["", "## Emergency indications (91.227(d)(9))", ""]
    lines += [f"- {_label(a)} `{a['hex']}`: {a['emergency']}" for a in emerg] or ["None in this window."]

    cont = [a for a in ac if a["continuity"]]
    lines += ["", f"## Track continuity (dropout threshold {result['coast_s']:.0f} s, jump limit {tracks.MAX_PLAUSIBLE_KT:,.0f} kt)", ""]
    if cont:
        for a in cont:
            for f in a["continuity"]:
                lines.append(f"- {_label(a)} `{a['hex']}`: {f}")
    else:
        lines.append("No dropouts or position jumps in this window.")

    alt = [a for a in ac if a["altitude"]]
    fit = result["alt_fit"]
    lines += ["", f"## Altitude consistency (barometric vs geometric, threshold {result['alt_threshold_ft']} ft)", ""]
    if fit:
        lines += [f"Area trend from {fit['n']} airborne aircraft: geometric minus barometric = "
                  f"{fit['intercept_ft']:+.0f} ft {fit['slope_ft_per_1000']:+.1f} ft per 1,000 ft (Theil-Sen fit). "
                  f"{fit['local']} aircraft were then compared with their nearest neighbors (within 75 NM and 10,000 ft); "
                  f"{fit['not_assessed']} had too few neighbors and {'was' if fit['not_assessed'] == 1 else 'were'} not assessed.", ""]
        lines += [f"- {_label(a)} `{a['hex']}`: {a['altitude']}" for a in alt] or ["No aircraft off the area trend."]
    else:
        lines.append("Too few airborne aircraft with both altitudes to fit an area trend.")

    if result.get("weather"):
        lines += ["", result["weather"].rstrip()]

    gi = result["interference"]
    lines += ["", "## GNSS interference screen", "",
              f"Brief drops below NACp 8 or NIC 7 by normally compliant aircraft: {gi['events']} aircraft-polls "
              f"from {gi['aircraft']} aircraft. A cluster needs at least {gi['min_aircraft']} aircraft dropping in the "
              f"same poll within {gi['radius_nm']:.0f} NM of each other.", ""]
    if gi["clusters"]:
        for c in gi["clusters"]:
            lines.append(f"- {_utc(c['time'])}: {len(c['aircraft'])} aircraft near "
                         f"{c['center'][0]:.2f}N {abs(c['center'][1]):.2f}W dropped together. Worth a human look.")
    else:
        lines.append("No clustered drops. Nothing in this window looks like area-wide GNSS interference.")

    unst = [a for a in ac if a["unstable"]]
    lines += ["", "## Informational: unstable indicators", "",
              "Verdicts use each indicator's most frequent value over the window. These aircraft had an indicator "
              "that switched between passing and failing values, so their verdict carries lower confidence.", ""]
    airborne = [a for a in unst if not a["on_ground"]]
    grounded = [a for a in unst if a["on_ground"]]
    lines += [f"- {_label(a)} `{a['hex']}`: {'; '.join(a['unstable'])}" for a in airborne]
    if grounded:
        lines.append(f"- Plus {len(grounded)} aircraft on the ground (listed in results.csv). All-zero moments on the "
                     "ground are consistent with avionics acquiring GPS at the gate.")
    if not unst:
        lines.append("None in this window.")

    lines += ["", stats.to_markdown(result["stats"]).rstrip()]

    ended = [a for a in ac if a["track_end"]]
    lines += ["", "## Informational: tracks lost and not reacquired", "",
              "Usually a landing, taxiing out of receiver range, or leaving the area. Not counted as dropouts.", ""]
    lines += [f"- {_label(a)} `{a['hex']}`: {a['track_end']}" for a in ended] or ["None in this window."]

    legacy = [a for a in ac if a["version_note"]]
    lines += ["", "## Informational: pre-DO-260B transmitters", ""]
    lines += [f"- {_label(a)} `{a['hex']}`: {a['version_note']}" for a in legacy] or ["None in this window."]
    lines.append("")
    return "\n".join(lines)


CSV_FIELDS = ["hex", "flight", "reg", "type_code", "report_type", "version", "verdict",
              "nac_p", "nac_v", "nic", "sda", "sil", "failed_paragraphs", "emergency", "continuity", "track_end", "altitude", "category", "altitude_band", "unstable", "polls_seen", "rule_airspace", "year_mfr", "build_cert"]


def to_csv(result, path):
    """SYS-041: one row per evaluated aircraft."""
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=CSV_FIELDS)
        w.writeheader()
        for a in result["aircraft"]:
            vals = {ch["field"]: ch["value"] for ch in a["checks"]}
            w.writerow({
                "hex": a["hex"], "flight": a["flight"], "reg": a["reg"], "type_code": a["type_code"],
                "report_type": a["report_type"], "version": a["version"], "verdict": a["verdict"],
                **{f: vals.get(f) for f in ("nac_p", "nac_v", "nic", "sda", "sil")},
                "failed_paragraphs": "; ".join(ch["para"] for ch in a["checks"] if ch["status"] == rules.FAIL),
                "emergency": a["emergency"] or "",
                "continuity": "; ".join(a["continuity"]),
                "track_end": a["track_end"] or "",
                "altitude": a["altitude"] or "",
                "category": a["category"] or "",
                "altitude_band": stats.altitude_band(a["alt_baro"]),
                "unstable": "; ".join(a["unstable"]),
                "polls_seen": a["polls_seen"],
                "rule_airspace": "" if a["rule_airspace"] is None else (a["rule_airspace"] or "no"),
                "year_mfr": a["year_mfr"] or "",
                "build_cert": a["build_cert"] or "",
            })
