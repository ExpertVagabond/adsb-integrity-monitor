"""Analysis and reporting: turn a capture into per-aircraft results, a Markdown report and a CSV."""

import csv
import datetime as dt
import hashlib
from collections import Counter

from . import rules, tracks

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


def analyze(snapshots, coast_s=tracks.DEFAULT_COAST_S):
    """Return the full analysis dict used by both report writers."""
    merged = merge_latest(snapshots)
    continuity = tracks.continuity_findings(snapshots, coast_s)
    track_ends = tracks.lost_tracks(snapshots, coast_s)

    excluded = Counter()
    aircraft = []
    for hx, ac in sorted(merged.items()):
        if not rules.is_evaluated(ac):
            excluded[ac.get("type", "unknown")] += 1
            continue
        if rules.is_surface_vehicle(ac):
            excluded["surface vehicle"] += 1
            continue
        if rules.is_pre_do260b(ac):
            checks, verdict = [], "not evaluable"
        else:
            checks = rules.check_performance(ac)
            fails = [c for c in checks if c["status"] == rules.FAIL]
            missing = [c for c in checks if c["status"] == rules.NOT_REPORTED]
            verdict = "fail" if fails else ("incomplete" if missing else "pass")
        aircraft.append({
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
        })

    times = [s["feed_time"] for s in snapshots]
    return {
        "window_start": min(times) if times else None,
        "window_end": max(times) if times else None,
        "snapshots": len(snapshots),
        "coast_s": coast_s,
        "aircraft": aircraft,
        "excluded": dict(excluded),
        "coast_s_used": coast_s,
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


def _utc(ts):
    return dt.datetime.fromtimestamp(ts, dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC") if ts else "n/a"


def _label(a):
    parts = (a["flight"], f"({a['reg']})" if a["reg"] else "", a["type_code"], "[on ground]" if a.get("on_ground") else "")
    return " ".join(x for x in parts if x) or "unidentified"


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
        "| Indicator | Requirement | Pass | Fail | Not reported |",
        "|---|---|---|---|---|",
    ]
    for field, _, para, bound in rules.PERFORMANCE_CHECKS:
        c = Counter(ch["status"] for a in ac for ch in a["checks"] if ch["field"] == field)
        lines.append(f"| {field} | {para}: {bound} | {c.get(rules.PASS, 0)} | {c.get(rules.FAIL, 0)} | {c.get(rules.NOT_REPORTED, 0)} |")

    fails = [a for a in ac if a["verdict"] == "fail"]
    lines += ["", "## Aircraft below a 91.227(c)(1) minimum", ""]
    if fails:
        lines += ["| Aircraft | ICAO | Finding |", "|---|---|---|"]
        for a in fails:
            for ch in a["checks"]:
                if ch["status"] == rules.FAIL:
                    lines.append(f"| {_label(a)} | {a['hex']} | {ch['field']} = {ch['value']}, needs {ch['bound']} ({ch['para']}) |")
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
              "nac_p", "nac_v", "nic", "sda", "sil", "failed_paragraphs", "emergency", "continuity", "track_end"]


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
            })
