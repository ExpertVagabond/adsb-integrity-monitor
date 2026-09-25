"""Self-contained HTML report with an SVG track map (SYS-045).

No external scripts, fonts, or tiles: the file opens offline and can be emailed as-is.
Tracks are drawn from the same position fixes the continuity checks use, colored by verdict.
"""

import html
import math

from . import report, stats, tracks

COLORS = {"pass": "var(--pass)", "fail": "var(--fail)", "incomplete": "var(--warn)", "not evaluable": "var(--info)"}
W, H, PAD = 900, 620, 24

CSS = """
:root { --bg:#fbfbf9; --fg:#1b1d21; --muted:#5d6470; --line:#d9dcd6; --panel:#ffffff;
        --pass:#9aa39a; --fail:#d0342c; --warn:#d88a00; --info:#2f6fb3; --grid:#e8eae4; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
        --bg:#14161a; --fg:#e8e9ea; --muted:#9aa1ab; --line:#2c3037; --panel:#1b1e23;
        --pass:#5f6b62; --fail:#ff5a4f; --warn:#f0a531; --info:#5c9ce6; --grid:#23272d; } }
* { box-sizing: border-box; }
body { margin:0; background:var(--bg); color:var(--fg); font:15px/1.5 -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; }
main { max-width: 960px; margin: 0 auto; padding: 24px 16px 48px; }
h1 { font-size: 24px; margin: 0 0 4px; } h2 { font-size: 17px; margin: 28px 0 8px; }
.meta { color: var(--muted); font-size: 13px; margin: 0 0 16px; }
.note { border-left: 3px solid var(--line); padding: 4px 12px; color: var(--muted); font-size: 13px; }
.tiles { display:grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin: 16px 0; }
.tile { background: var(--panel); border:1px solid var(--line); border-radius: 8px; padding: 10px 12px; }
.tile b { display:block; font-size: 22px; } .tile span { color: var(--muted); font-size: 12px; }
.map { background: var(--panel); border:1px solid var(--line); border-radius: 8px; overflow:hidden; }
svg { display:block; width:100%; height:auto; }
.legend { display:flex; flex-wrap:wrap; gap: 14px; font-size: 13px; color: var(--muted); margin: 8px 2px; }
.legend i { display:inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 6px; vertical-align: middle; }
.scroll { overflow-x: auto; } table { border-collapse: collapse; width: 100%; font-size: 13px; }
th, td { text-align: left; padding: 6px 8px; border-bottom: 1px solid var(--line); vertical-align: top; }
th { color: var(--muted); font-weight: 600; }
code { font-size: 12px; }
"""


def _project(bounds):
    """Equirectangular projection scaled by cos(latitude), fitted into the SVG box."""
    lat0, lat1, lon0, lon1 = bounds
    k = math.cos(math.radians((lat0 + lat1) / 2))
    span_x, span_y = max((lon1 - lon0) * k, 1e-6), max(lat1 - lat0, 1e-6)
    scale = min((W - 2 * PAD) / span_x, (H - 2 * PAD) / span_y)
    ox = (W - span_x * scale) / 2
    oy = (H - span_y * scale) / 2

    def xy(lat, lon):
        return ox + (lon - lon0) * k * scale, H - (oy + (lat - lat0) * scale)
    return xy


def _svg(result, fixes):
    keys = {a["key"]: a for a in result["aircraft"]}
    pts = [(la, lo) for k, f in fixes.items() if k in keys for _, la, lo in f]
    if not pts:
        return "<p>No positions in this capture.</p>"
    lats, lons = [p[0] for p in pts], [p[1] for p in pts]
    xy = _project((min(lats), max(lats), min(lons), max(lons)))

    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Map of aircraft tracks colored by result">']
    for g in range(math.floor(min(lats)), math.ceil(max(lats)) + 1):   # latitude grid
        x1, y = xy(g, min(lons)); x2, _ = xy(g, max(lons))
        out.append(f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y:.1f}" stroke="var(--grid)"/>'
                   f'<text x="{x1 + 4:.1f}" y="{y - 4:.1f}" font-size="11" fill="var(--muted)">{g}°N</text>')
    for g in range(math.floor(min(lons)), math.ceil(max(lons)) + 1):   # longitude grid
        x, y1 = xy(min(lats), g); _, y2 = xy(max(lats), g)
        out.append(f'<line x1="{x:.1f}" y1="{y1:.1f}" x2="{x:.1f}" y2="{y2:.1f}" stroke="var(--grid)"/>'
                   f'<text x="{x + 4:.1f}" y="{y1 - 4:.1f}" font-size="11" fill="var(--muted)">{abs(g)}°W</text>')

    # passing aircraft first so problems draw on top
    order = sorted(keys.values(), key=lambda a: a["verdict"] != "pass")
    for a in order:
        f = fixes.get(a["key"])
        if not f:
            continue
        color = COLORS[a["verdict"]]
        width = 1.2 if a["verdict"] == "pass" else 2.4
        tip = html.escape(f"{report._label(a)} {a['hex']} - {a['verdict']}")
        path = " ".join(f"{x:.1f},{y:.1f}" for x, y in (xy(la, lo) for _, la, lo in f))
        x, y = xy(f[-1][1], f[-1][2])
        out.append(f'<g><title>{tip}</title>'
                   f'<polyline points="{path}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>'
                   f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{2.5 if a["verdict"] == "pass" else 4.5}" fill="{color}"/></g>')
    out.append("</svg>")
    return "".join(out)


def _row(*cells):
    return "<tr>" + "".join(f"<td>{html.escape(str(c))}</td>" for c in cells) + "</tr>"


def to_html(result, snapshots, area_desc):
    ac = result["aircraft"]
    n = {v: sum(1 for a in ac if a["verdict"] == v) for v in COLORS}
    fixes = tracks.position_fixes(snapshots)

    def where(a):
        if a.get("rule_airspace"):
            return f"in {a['rule_airspace']} airspace"
        return "not seen in 91.225(d) airspace" if a.get("rule_airspace") == "" else ""

    fail_rows = [_row(report._label(a), a["hex"],
                      f"{c['field']} = {c['value']}" + (" (unstable, low confidence)" if report._is_unstable(a, c["field"]) else ""),
                      c["para"], where(a))
                 for a in ac if a["verdict"] == "fail" for c in a["checks"] if c["status"] == "fail"]
    other_rows = [_row(report._label(a), a["hex"], note) for a in ac
                  for note in ([a["emergency"]] if a["emergency"] else []) + ([a["altitude"]] if a["altitude"] else []) + a["continuity"]]
    other_rows += [_row(f"{len(c['aircraft'])} aircraft", report._utc(c["time"]),
                        f"possible GNSS interference: dropped together near {c['center'][0]:.2f}N {abs(c['center'][1]):.2f}W")
                   for c in result["interference"]["clusters"]]
    type_rows = [_row(*r[:3], f"{r[5]}%") for r in result["stats"]["failing_types"]]
    redacted = " Aircraft identities are replaced with stable pseudonyms." if result.get("redacted") else ""

    parts = [
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>",
        "<meta name='viewport' content='width=device-width, initial-scale=1'>",
        "<title>ADS-B Integrity Report</title>", f"<style>{CSS}</style></head><body><main>",
        "<h1>ADS-B Integrity Report</h1>",
        f"<p class='meta'>{html.escape(area_desc)} · {report._utc(result['window_start'])} to {report._utc(result['window_end'])} "
        f"· {result['snapshots']} snapshots</p>",
        "<div class='tiles'>",
        f"<div class='tile'><b>{len(ac)}</b><span>aircraft evaluated</span></div>",
        f"<div class='tile'><b>{n['pass']}</b><span>meet all five 91.227(c)(1) minimums</span></div>",
        f"<div class='tile'><b>{n['fail']}</b><span>below at least one minimum</span></div>",
        f"<div class='tile'><b>{n['incomplete'] + n['not evaluable']}</b><span>incomplete or not evaluable</span></div>",
        "</div>",
        "<div class='map'>", _svg(result, fixes), "</div>",
        "<div class='legend'>",
        "<span><i style='background:var(--pass)'></i>meets all minimums</span>",
        "<span><i style='background:var(--fail)'></i>below a minimum</span>",
        "<span><i style='background:var(--warn)'></i>indicator not reported</span>",
        "<span><i style='background:var(--info)'></i>pre-DO-260B, not evaluable</span>",
        "</div>",
        "<h2>Below a 14 CFR 91.227(c)(1) minimum</h2>",
        "<div class='scroll'><table><tr><th>Aircraft</th><th>ID</th><th>Indicator</th><th>Paragraph</th><th>Rule applies?</th></tr>"
        + ("".join(fail_rows) or "<tr><td colspan='5'>None in this window.</td></tr>") + "</table></div>",
        "<h2>Other findings</h2>",
        "<div class='scroll'><table><tr><th>Aircraft</th><th>ID</th><th>Finding</th></tr>"
        + ("".join(other_rows) or "<tr><td colspan='3'>None in this window.</td></tr>") + "</table></div>",
        "<h2>Aircraft types with failures</h2>",
        "<div class='scroll'><table><tr><th>Type</th><th>Aircraft</th><th>Fail</th><th>Fail rate</th></tr>"
        + ("".join(type_rows) or "<tr><td colspan='4'>None in this window.</td></tr>") + "</table></div>",
        f"<h2>About this data</h2><p class='note'>{html.escape(report.DISCLAIMER)}{redacted}</p>",
        "</main></body></html>",
    ]
    return "\n".join(parts)
