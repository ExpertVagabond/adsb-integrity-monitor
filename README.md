# ADS-B Integrity Monitor

Checks live, public ADS-B Out broadcasts against the performance minimums in
**[14 CFR 91.227(c)(1)](https://www.ecfr.gov/current/title-14/chapter-I/subchapter-F/part-91/subpart-C/section-91.227)**:
position accuracy (NACp), velocity accuracy (NACv), integrity containment (NIC), system design assurance (SDA)
and source integrity (SIL). It also flags emergency codes and track dropouts.

The project is built the way an FAA systems engineering program would build it, with the documents first and
every requirement traced to a test:

| Document | What it covers |
|---|---|
| [01 Concept of Operations](docs/01-ConOps.md) | Purpose, shortfall, users, operational constraints |
| [02 System Requirements](docs/02-Requirements.md) | 23 numbered "shall" statements with verification method and source |
| [03 Architecture and ICD](docs/03-Architecture-ICD.md) | Components, interface definitions, design decisions |
| [04 Trade Study](docs/04-Trade-Study.md) | Weighted comparison of five ADS-B data sources, with live measurements |
| [Traceability Matrix](docs/RTM.md) | Generated from test tags; the build fails if any requirement is unverified |

## First live capture: 60 NM around Atlantic City (ACY), 2026-09-25

Five minutes of data around the FAA William J. Hughes Technical Center, 29 snapshots
([full report](reports/acy-2026-09-25/report.md), [CSV](reports/acy-2026-09-25/results.csv); aircraft identities
are pseudonymized with `--redact`):

| Result | Aircraft |
|---|---|
| All five indicators meet 91.227(c)(1) | 91 |
| At least one indicator below the minimum | 2 |
| Indicator not reported, no failures | 2 |
| Pre-DO-260B transmitter, not evaluable | 1 |
| Surface vehicles excluded | 2 |

One Cessna 210 broadcast NACp, NACv, NIC and SIL all at 0, the usual signature of a transponder that isn't
receiving a position source.

## What the live data changed

The first version passed every unit test and was still wrong on real data. Running it against the capture
exposed four problems, each now fixed, tested and written into the requirements:

1. **Polling artifacts looked like dropouts.** One slow poll (20.5 s instead of 10 s) produced 69 false
   dropouts. Dropouts are now judged by the aggregator's own `seen_pos` clock (SYS-030).
2. **Ground vehicles were scored as aircraft.** Two airport service vehicles broadcast ADS-B. They're now
   excluded, since 91.227 governs aircraft (SYS-018).
3. **An old transmitter was "failed" on synthesized values.** A 747 broadcasting ADS-B version 0 showed SIL = 2,
   but version 0 doesn't carry SIL; the decoder derived it. Pre-DO-260B transmitters are now listed, not
   scored (SYS-017).
4. **Landings were counted as dropouts.** Tracks that go stale and never return are now reported separately
   (SYS-032).

## Run it

Python 3.10+ and nothing else (standard library only, SYS-060).

```sh
# capture 5 minutes, 60 NM around ACY
python3 -m aim collect --lat 39.4576 --lon -74.5772 --radius 60 --polls 30 --interval 10 --out captures/acy.jsonl

# analyze: writes reports/report.md and reports/results.csv
python3 -m aim analyze captures/acy.jsonl --area "60 NM around ACY"

# tests (set AIM_LIVE=1 to include the live-API test)
python3 -m unittest discover -s tests

# regenerate the traceability matrix; exits 1 if any requirement is unverified
python3 -m aim rtm
```

## Limits

Data comes from volunteer receivers aggregated by [adsb.lol](https://adsb.lol). Findings describe what those
receivers decoded, and are **not an FAA compliance determination**. Aircraft owners can get an authoritative
check from the FAA's free [Public ADS-B Performance Report](https://www.faa.gov/go/adsbpapr/).

## License

Code: MIT. Captured data: adsb.lol, [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/).

Built by Matthew Karsten ([github.com/ExpertVagabond](https://github.com/ExpertVagabond)).
