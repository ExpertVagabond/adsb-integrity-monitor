"""Command line: python -m aim {collect,analyze,rtm} ..."""

import argparse
import pathlib
import sys

from . import airspace, feed, htmlreport, registry, report, reqif, rtm, trend, watch, weather


def main(argv=None):
    p = argparse.ArgumentParser(prog="aim", description="ADS-B Integrity Monitor (14 CFR 91.227)")
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("collect", help="poll adsb.lol and append snapshots to a JSON Lines file")
    c.add_argument("--lat", type=float, required=True)
    c.add_argument("--lon", type=float, required=True)
    c.add_argument("--radius", type=float, default=40, help="radius in NM (max 250)")
    c.add_argument("--polls", type=int, default=12)
    c.add_argument("--interval", type=float, default=10, help=f"seconds between polls (min {feed.MIN_INTERVAL_S:.0f})")
    c.add_argument("--out", required=True)

    a = sub.add_parser("analyze", help="analyze a capture and write report.md + results.csv")
    a.add_argument("capture")
    a.add_argument("--coast", type=float, default=20, help="seconds without a position refresh that count as a dropout")
    a.add_argument("--area", default="unspecified area")
    a.add_argument("--outdir", default="reports")
    a.add_argument("--redact", action="store_true", help="replace ICAO address, callsign and registration with pseudonyms")
    a.add_argument("--alt-threshold", type=float, default=200, help="feet off the area altitude trend that count as a finding")
    a.add_argument("--weather", action="store_true", help="check the altitude trend against the Open-Meteo weather model (network)")
    a.add_argument("--airspace", help="airspace JSON from `aim airspace` to mark 91.225(d) rule applicability")
    a.add_argument("--registry", help="aircraft lookup CSV from `aim registry` (year built, certification basis)")

    w = sub.add_parser("watch", help="live monitoring: alert on emergencies and integrity changes")
    w.add_argument("--lat", type=float, required=True)
    w.add_argument("--lon", type=float, required=True)
    w.add_argument("--radius", type=float, default=40, help="radius in NM (max 250)")
    w.add_argument("--polls", type=int, default=0, help="number of polls; 0 = until Ctrl-C")
    w.add_argument("--interval", type=float, default=15, help=f"seconds between polls (min {feed.MIN_INTERVAL_S:.0f})")
    w.add_argument("--alerts", help="append alerts as JSON Lines to this file")
    w.add_argument("--redact", action="store_true", help="replace identities with pseudonyms in alerts")
    w.add_argument("--confirm", type=int, default=2, help="consecutive polls a change must hold before it alerts")

    sp = sub.add_parser("airspace", help="download FAA Class B/C boundaries and Appendix D airports for a bounding box")
    sp.add_argument("--bbox", required=True, help="west,south,east,north in degrees, e.g. -76.9,37.8,-72.3,41.2")
    sp.add_argument("--out", required=True)

    rg = sub.add_parser("registry", help="download the FAA registry and build an aircraft-facts lookup (no owner data)")
    rg.add_argument("--zip", help="use an already-downloaded ReleasableAircraft.zip instead of downloading")
    rg.add_argument("--out", required=True)

    tr = sub.add_parser("trend", help="re-analyze many captures and track results and repeat failures over time")
    tr.add_argument("inputs", nargs="+", help="capture files or directories (searched for *.jsonl and *.jsonl.gz)")
    tr.add_argument("--airspace", help="airspace JSON from `aim airspace`")
    tr.add_argument("--registry", help="aircraft lookup CSV from `aim registry`")
    tr.add_argument("--redact", action="store_true", help="pseudonymize aircraft in the output")
    tr.add_argument("--outdir", default="reports/trend")

    sub.add_parser("rtm", help="regenerate docs/RTM.md; fails if any requirement is unverified")
    sub.add_parser("reqif", help="export the requirements and verification links as ReqIF 1.2 (DOORS, Jama, Polarion)")

    args = p.parse_args(argv)

    if args.cmd == "collect":
        n = feed.collect(args.lat, args.lon, args.radius, args.polls, args.interval, args.out)
        print(f"wrote {n} snapshots to {args.out}")
        return 0 if n else 1

    if args.cmd == "analyze":
        snaps = feed.load_snapshots(args.capture)
        if not snaps:
            print("capture is empty", file=sys.stderr)
            return 1
        result = report.analyze(snaps, args.coast, args.alt_threshold,
                                airspace.load(args.airspace) if args.airspace else None,
                                registry.load(args.registry) if args.registry else None)
        if args.weather and result["alt_fit"]:
            mid = (result["window_start"] + result["window_end"]) / 2
            lat, lon = report.capture_center(snaps)
            try:
                check = weather.compare(result["alt_fit"], weather.fetch_heights(lat, lon, mid),
                                        (1000, result["alt_fit"]["max_alt_ft"]))
                result["weather"] = weather.to_markdown(check, mid, lat, lon)
                result["weather_check"] = check
            except Exception as exc:  # the check is optional; the report still stands without it
                print(f"weather check skipped: {exc}", file=sys.stderr)
        if args.redact:
            report.redact(result)
        out = pathlib.Path(args.outdir)
        out.mkdir(parents=True, exist_ok=True)
        (out / "report.md").write_text(report.to_markdown(result, args.area), encoding="utf-8")
        report.to_csv(result, out / "results.csv")
        (out / "report.html").write_text(htmlreport.to_html(result, snaps, args.area), encoding="utf-8")
        print(f"{len(result['aircraft'])} aircraft evaluated -> {out}/report.md, results.csv, report.html")
        return 0

    if args.cmd == "watch":
        watch.run(args.lat, args.lon, args.radius, args.polls, args.interval, args.alerts, args.redact, args.confirm)
        return 0

    if args.cmd == "airspace":
        d = airspace.fetch(tuple(float(v) for v in args.bbox.split(",")), args.out)
        print(f"{len(d['areas'])} Class B/C areas, {len(d['veil_airports'])} Appendix D airports -> {args.out}")
        return 0 if not d["veil_airports_missing"] else 1

    if args.cmd == "registry":
        zpath = args.zip
        if not zpath:
            zpath = args.out + ".zip"
            registry.download(zpath)
        print(f"{registry.build(zpath, args.out)} aircraft -> {args.out}")
        return 0

    if args.cmd == "reqif":
        path, n = reqif.write(".")
        print(f"{n} requirements -> {path}")
        return 0

    if args.cmd == "trend":
        paths = []
        for item in args.inputs:
            pth = pathlib.Path(item)
            paths += sorted(pth.rglob("*.jsonl")) + sorted(pth.rglob("*.jsonl.gz")) if pth.is_dir() else [pth]
        if not paths:
            print("no captures found", file=sys.stderr)
            return 1
        rows, recur, alt_recur = trend.build(paths, airspace.load(args.airspace) if args.airspace else None,
                                  registry.load(args.registry) if args.registry else None)
        out = pathlib.Path(args.outdir)
        out.mkdir(parents=True, exist_ok=True)
        (out / "trend.md").write_text(trend.to_markdown(rows, recur, args.redact, alt_recur), encoding="utf-8")
        (out / "trend.html").write_text(trend.to_html(rows, recur, args.redact, alt_recur), encoding="utf-8")
        trend.to_csv(rows, out / "trend.csv")
        print(f"{len(rows)} captures -> {out}/trend.md, trend.html, trend.csv")
        return 0

    if args.cmd == "rtm":
        reqs, unverified, unknown = rtm.run(".")
        print(f"{len(reqs) - len(unverified)}/{len(reqs)} requirements verified -> docs/RTM.md")
        for r in unverified:
            print(f"  UNVERIFIED: {r}", file=sys.stderr)
        for r in unknown:
            print(f"  UNKNOWN ID cited by a test: {r}", file=sys.stderr)
        return 1 if unverified or unknown else 0


if __name__ == "__main__":
    sys.exit(main())
