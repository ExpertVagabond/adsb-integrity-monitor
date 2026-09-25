"""Command line: python -m aim {collect,analyze,rtm} ..."""

import argparse
import pathlib
import sys

from . import feed, report, rtm


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

    sub.add_parser("rtm", help="regenerate docs/RTM.md; fails if any requirement is unverified")

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
        result = report.analyze(snaps, args.coast)
        if args.redact:
            report.redact(result)
        out = pathlib.Path(args.outdir)
        out.mkdir(parents=True, exist_ok=True)
        (out / "report.md").write_text(report.to_markdown(result, args.area), encoding="utf-8")
        report.to_csv(result, out / "results.csv")
        print(f"{len(result['aircraft'])} aircraft evaluated -> {out / 'report.md'}, {out / 'results.csv'}")
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
