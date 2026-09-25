"""Fleet statistics: where do the failures concentrate? (SYS-044)

Altitude bands follow the 14 CFR 91.225 airspace boundaries: ADS-B Out is required in
Class A (FL180 and above) and in Class E above 10,000 ft MSL, so those are the natural cuts.
"""

from collections import Counter, defaultdict

CATEGORY_NAMES = {
    "A1": "Light (< 15,500 lb)",
    "A2": "Small (15,500-75,000 lb)",
    "A3": "Large (75,000-300,000 lb)",
    "A4": "High-vortex large (e.g. B757)",
    "A5": "Heavy (> 300,000 lb)",
    "A6": "High performance",
    "A7": "Rotorcraft",
    "B1": "Glider",
    "B2": "Lighter than air",
    "B4": "Ultralight",
    "B6": "Unmanned aircraft",
}

REPORT_TYPES = {
    "adsb_icao": "Direct 1090ES ADS-B",
    "adsr_icao": "ADS-R (UAT rebroadcast by FAA ground station)",
}

BANDS = ("Surface", "Below 10,000 ft", "10,000 ft to FL180", "FL180 and above", "Unknown")


def altitude_band(alt_baro):
    if alt_baro == "ground":
        return "Surface"
    if not isinstance(alt_baro, int):
        return "Unknown"
    if alt_baro < 10000:
        return "Below 10,000 ft"
    if alt_baro < 18000:
        return "10,000 ft to FL180"
    return "FL180 and above"


def _tally(aircraft, key):
    groups = defaultdict(Counter)
    for a in aircraft:
        groups[key(a)][a["verdict"]] += 1
    return groups


def decade(year):
    return f"{year[:3]}0s" if year and year.isdigit() and len(year) == 4 else "unknown"


def fleet_stats(aircraft, with_registry=False):
    """Return {"by_category", "by_band", "by_version", "by_report_type", "failing_types"}: lists of rows.

    Each row: (label, total, fail, incomplete, not_evaluable, fail_rate_percent).
    """
    def rows(groups, order=None):
        labels = order or sorted(groups, key=lambda k: (-sum(groups[k].values()), str(k)))
        out = []
        for label in labels:
            c = groups.get(label)
            if not c:
                continue
            total = sum(c.values())
            out.append((label, total, c["fail"], c["incomplete"], c["not evaluable"],
                        round(100.0 * c["fail"] / total, 1)))
        return out

    by_cat = _tally(aircraft, lambda a: a.get("category") or "unknown")
    by_band = _tally(aircraft, lambda a: altitude_band(a.get("alt_baro")))
    by_ver = _tally(aircraft, lambda a: f"version {a['version']}" if isinstance(a.get("version"), int) else "not reported")
    by_type = _tally(aircraft, lambda a: a.get("type_code") or "unknown")
    by_source = _tally(aircraft, lambda a: REPORT_TYPES.get(a.get("report_type"), a.get("report_type") or "unknown"))

    registry_rows = {}
    if with_registry:
        registered = [a for a in aircraft if a.get("build_cert") is not None]
        registry_rows["by_build_cert"] = rows(_tally(registered, lambda a: a.get("build_cert") or "not in US registry"))
        registry_rows["by_decade"] = sorted(rows(_tally(registered, lambda a: decade(a.get("year_mfr")))), key=lambda r: r[0])

    failing_types = [r for r in rows(by_type) if r[2] > 0]
    failing_types.sort(key=lambda r: (-r[2], -r[1], r[0]))
    return {
        "by_category": [(f"{r[0]} {CATEGORY_NAMES.get(r[0], '')}".strip(),) + r[1:] for r in rows(by_cat)],
        "by_band": rows(by_band, order=list(BANDS)),
        "by_version": rows(by_ver),
        "by_report_type": rows(by_source),
        "failing_types": failing_types,
        **registry_rows,
    }


def to_markdown(stats):
    lines = ["## Fleet statistics", ""]
    head = "| {} | Aircraft | Fail | Not reported | Not evaluable | Fail rate |\n|---|---|---|---|---|---|"
    for title, key, col in (("By emitter category", "by_category", "Category"),
                            ("By altitude band (91.225 boundaries)", "by_band", "Band"),
                            ("By ADS-B version", "by_version", "Version"),
                            ("By report type", "by_report_type", "Report type")):
        lines += [f"### {title}", "", head.format(col)]
        lines += [f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]}% |" for r in stats[key]]
        lines.append("")
    for title, key, col in (("By certification basis (FAA registry)", "by_build_cert", "Certification"),
                            ("By decade of manufacture (FAA registry)", "by_decade", "Built")):
        if key in stats:
            lines += [f"### {title}", "", head.format(col)]
            lines += [f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]}% |" for r in stats[key]]
            lines.append("")
    lines += ["### Aircraft types with at least one failure", ""]
    if stats["failing_types"]:
        lines.append(head.format("Type"))
        lines += [f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]}% |" for r in stats["failing_types"]]
    else:
        lines.append("None in this window.")
    lines.append("")
    return "\n".join(lines)
