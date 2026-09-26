"""Trends across captures (SYS-053, SYS-054).

One capture is a snapshot; the Shortfall Analysis's first recommendation is a multi-day baseline. This
module re-analyzes every capture with the current rules (so older captures are judged exactly like new
ones), produces one summary row per capture, and follows aircraft across captures: a failure that
recurs on different days is much stronger evidence than a single sighting.

Pseudonyms are the same hash used by report.redact, so recurrence works on redacted output too.
"""

import csv
import datetime as dt
import hashlib
import html
import pathlib

from . import feed, report, rules

FIELDS = ("capture", "start_utc", "minutes", "area", "snapshots", "aircraft", "pass", "pass_pct", "fail", "fail_high_conf",
          "fail_high_conf_in_rule", "incomplete", "not_evaluable", "adsr", "interference_events",
          "interference_clusters", "altitude_outliers")


def _alias(hx):
    return "AC-" + hashlib.sha256(hx.encode()).hexdigest()[:6].upper()


def high_confidence(a):
    """A failure counts as high confidence when none of its failing indicators alternated (SYS-019)."""
    if a["verdict"] != "fail":
        return False
    failed = [c["field"] for c in a["checks"] if c["status"] == rules.FAIL]
    return not any(report._is_unstable(a, f) for f in failed)


def summarize(path, airspace_data=None, registry_data=None):
    """Analyze one capture; return (summary row, {real hex: per-aircraft facts})."""
    snaps = feed.load_snapshots(path)
    r = report.analyze(snaps, airspace_data=airspace_data, registry_data=registry_data)
    ac = r["aircraft"]
    n = len(ac)
    count = lambda pred: sum(1 for a in ac if pred(a))
    area = snaps[0].get("area") if snaps else None
    row = {
        "capture": pathlib.Path(path).name,
        "area": f"{area['radius_nm']:g} NM around {area['lat']:.2f}N {abs(area['lon']):.2f}W" if area else "not recorded",
        "start_utc": dt.datetime.fromtimestamp(r["window_start"], dt.timezone.utc).strftime("%Y-%m-%d %H:%M"),
        "minutes": round((r["window_end"] - r["window_start"]) / 60),
        "snapshots": r["snapshots"],
        "aircraft": n,
        "pass": count(lambda a: a["verdict"] == "pass"),
        "fail": count(lambda a: a["verdict"] == "fail"),
        "fail_high_conf": count(high_confidence),
        "fail_high_conf_in_rule": (count(lambda a: high_confidence(a) and a["rule_airspace"])
                                   if r.get("airspace_checked") else ""),
        "incomplete": count(lambda a: a["verdict"] == "incomplete"),
        "not_evaluable": count(lambda a: a["verdict"] == "not evaluable"),
        "adsr": count(lambda a: a["report_type"] == "adsr_icao"),
        "interference_events": r["interference"]["events"],
        "interference_clusters": len(r["interference"]["clusters"]),
        "altitude_outliers": count(lambda a: a["altitude"]),
    }
    row["pass_pct"] = round(100.0 * row["pass"] / n, 2) if n else 0.0
    facts = {a["key"]: {
        "type": a["type_code"],
        "verdict": a["verdict"],
        "high_conf": high_confidence(a),
        "failed": sorted(c["field"] for c in a["checks"] if c["status"] == rules.FAIL),
        "rule": a["rule_airspace"],
        "altitude": bool(a["altitude"]),
    } for a in ac}
    return row, facts


def recurrence(per_capture, flag="high_conf"):
    """Aircraft flagged (by default: a high-confidence failure) in at least one capture, and their record in every capture.

    per_capture: [(capture name, {hex: facts}), ...] in time order. flag: "high_conf" or "altitude".
    Returns [{"hex", "type", "seen", "failed_high_conf", "fields", "history"}], most-flagged first.
    """
    flagged = {hx for _, facts in per_capture for hx, f in facts.items() if f[flag]}
    out = []
    for hx in flagged:
        hist = [(name, facts[hx]) for name, facts in per_capture if hx in facts]
        fails = [(name, f) for name, f in hist if f[flag]]
        out.append({
            "hex": hx,
            "type": next((f["type"] for _, f in hist if f["type"]), ""),
            "seen": len(hist),
            "failed_high_conf": len(fails),
            "fields": sorted({x for _, f in fails for x in f["failed"]}),
            "history": [(name, ("fail (high confidence)" if flag == "high_conf" else "altitude outlier") if f[flag]
                         else ("seen, not flagged" if flag == "altitude" else f["verdict"])) for name, f in hist],
        })
    out.sort(key=lambda d: (-d["failed_high_conf"], -d["seen"], d["hex"]))
    return out


def build(paths, airspace_data=None, registry_data=None, log=print):
    rows, per_capture = [], []
    for p in paths:
        row, facts = summarize(p, airspace_data, registry_data)
        log(f"{row['capture']}: {row['aircraft']} aircraft, {row['fail_high_conf']} high-confidence failures")
        rows.append(row)
        per_capture.append((row["capture"], facts))
    order = sorted(range(len(rows)), key=lambda i: rows[i]["start_utc"])
    rows = [rows[i] for i in order]
    per_capture = [per_capture[i] for i in order]
    return rows, recurrence(per_capture), recurrence(per_capture, flag="altitude")


def to_csv(rows, path):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)


def to_markdown(rows, recur, redact=False, alt_recur=()):
    total = sum(r["aircraft"] for r in rows)
    hc = sum(r["fail_high_conf"] for r in rows)
    lines = [
        "# ADS-B Integrity Trend", "",
        f"{len(rows)} captures, {total:,} aircraft evaluations, re-analyzed with the current rules. "
        f"High-confidence failures: {hc} ({(1000.0 * hc / total) if total else 0:.1f} per 1,000 aircraft).", "",
        "| Capture start (UTC) | Minutes | Area | Aircraft | Pass | High-confidence fails | ...in rule airspace | Low-confidence fails | "
        "Not evaluable | ADS-R | Interference clusters | Altitude outliers |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(f"| {r['start_utc']} | {r['minutes']} | {r['area']} | {r['aircraft']} | {r['pass_pct']}% | {r['fail_high_conf']} | "
                     f"{r['fail_high_conf_in_rule'] if r['fail_high_conf_in_rule'] != '' else 'n/a'} | "
                     f"{r['fail'] - r['fail_high_conf']} | {r['not_evaluable']} | {r['adsr']} | "
                     f"{r['interference_clusters']} | {r['altitude_outliers']} |")
    lines += ["", "## Aircraft with a high-confidence failure", "",
              "A failure that repeats across captures is stronger evidence than a single sighting.", ""]
    if recur:
        lines += ["| Aircraft | Type | Captures seen | Failed (high confidence) | Indicators | History |", "|---|---|---|---|---|---|"]
        for d in recur:
            who = _alias(d["hex"]) if redact else d["hex"]
            hist = "; ".join(f"{name}: {v}" for name, v in d["history"])
            lines.append(f"| `{who}` | {d['type'] or '?'} | {d['seen']} | {d['failed_high_conf']} | {', '.join(d['fields'])} | {hist} |")
    else:
        lines.append("None.")
    lines += ["", "## Aircraft flagged by the altitude check", "",
              "The altitude threshold stays fixed; a borderline flag that never repeats is expected noise. One that repeats "
              "across captures points to a real altimetry or GNSS-altitude problem.", ""]
    if alt_recur:
        lines += ["| Aircraft | Type | Captures seen | Flagged | History |", "|---|---|---|---|---|"]
        for d in alt_recur:
            who = _alias(d["hex"]) if redact else d["hex"]
            lines.append(f"| `{who}` | {d['type'] or '?'} | {d['seen']} | {d['failed_high_conf']} | "
                         + "; ".join(f"{name}: {v}" for name, v in d["history"]) + " |")
    else:
        lines.append("None.")
    lines += ["", f"> {report.DISCLAIMER}", ""]
    return "\n".join(lines)


def to_html(rows, recur, redact=False, alt_recur=()):
    """A small self-contained page: high-confidence failures per 1,000 aircraft, one bar per capture."""
    w, h, pad = 760, 240, 40
    rates = [(1000.0 * r["fail_high_conf"] / r["aircraft"]) if r["aircraft"] else 0.0 for r in rows]
    top = max(rates + [1.0])
    bw = (w - 2 * pad) / max(len(rows), 1)
    bars = []
    for i, (r, v) in enumerate(zip(rows, rates)):
        bh = (h - 2 * pad) * v / top
        x, y = pad + i * bw + bw * 0.15, h - pad - bh
        bars.append(f'<g><title>{html.escape(r["start_utc"])} UTC: {v:.1f} per 1,000 ({r["fail_high_conf"]} of {r["aircraft"]})</title>'
                    f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw * 0.7:.1f}" height="{bh:.1f}" fill="var(--fail)"/>'
                    f'<text x="{x + bw * 0.35:.1f}" y="{h - pad + 14}" font-size="10" text-anchor="middle" fill="var(--muted)">'
                    f'{html.escape(r["start_utc"][5:10])}</text></g>')
    svg = (f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="High-confidence failures per 1,000 aircraft by capture">'
           f'<line x1="{pad}" y1="{h - pad}" x2="{w - pad}" y2="{h - pad}" stroke="var(--line)"/>'
           f'<text x="{pad}" y="{pad - 12}" font-size="11" fill="var(--muted)">high-confidence failures per 1,000 aircraft (max {top:.1f})</text>'
           + "".join(bars) + "</svg>")
    md = to_markdown(rows, recur, redact, alt_recur)
    table = "".join(f"<tr><td>{html.escape(r['start_utc'])}</td><td>{r['aircraft']}</td><td>{r['pass_pct']}%</td>"
                    f"<td>{r['fail_high_conf']}</td><td>{r['fail'] - r['fail_high_conf']}</td></tr>" for r in rows)
    css = (":root{--bg:#fbfbf9;--fg:#1b1d21;--muted:#5d6470;--line:#d9dcd6;--fail:#d0342c}"
           "@media (prefers-color-scheme: dark){:root:not([data-theme='light']){--bg:#14161a;--fg:#e8e9ea;--muted:#9aa1ab;--line:#2c3037;--fail:#ff5a4f}}"
           "body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 -apple-system,'Segoe UI',Helvetica,Arial,sans-serif}"
           "main{max-width:820px;margin:0 auto;padding:24px 16px}svg{width:100%;height:auto}"
           "table{border-collapse:collapse;width:100%;font-size:13px}td,th{text-align:left;padding:6px 8px;border-bottom:1px solid var(--line)}"
           ".scroll{overflow-x:auto}.muted{color:var(--muted);font-size:13px}")
    return ("<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>"
            f"<title>ADS-B Integrity Trend</title><style>{css}</style></head><body><main><h1>ADS-B Integrity Trend</h1>"
            f"<p class='muted'>{html.escape(md.splitlines()[2])}</p>{svg}"
            "<div class='scroll'><table><tr><th>Capture (UTC)</th><th>Aircraft</th><th>Pass</th><th>High-confidence fails</th>"
            f"<th>Low-confidence fails</th></tr>{table}</table></div>"
            f"<p class='muted'>{html.escape(report.DISCLAIMER)}</p></main></body></html>")
