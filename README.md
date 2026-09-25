# ADS-B Integrity Monitor

[![ci](https://github.com/ExpertVagabond/adsb-integrity-monitor/actions/workflows/ci.yml/badge.svg)](https://github.com/ExpertVagabond/adsb-integrity-monitor/actions/workflows/ci.yml)

Checks live, public ADS-B Out broadcasts against the performance minimums in
**[14 CFR 91.227(c)(1)](https://www.ecfr.gov/current/title-14/chapter-I/subchapter-F/part-91/subpart-C/section-91.227)**:
position accuracy (NACp), velocity accuracy (NACv), integrity containment (NIC), system design assurance (SDA)
and source integrity (SIL). It also checks each aircraft's two altitudes against the aircraft around it, screens
for GPS interference, flags emergency codes and track dropouts, and can run as a live monitor. Findings are
checked against independent sources: a weather model for the altitude physics, FAA airspace data for where the
rule applies, the FAA registry for aircraft age and certification, and the decoder's source code for how each
value is produced.

**Live map report:** [adsb-integrity-monitor.pages.dev](https://adsb-integrity-monitor.pages.dev/) (one hour, 812 aircraft; identities pseudonymized).

The project is built the way an FAA systems engineering program would build it, with the documents first and
every requirement traced to a test:

| Document | What it covers |
|---|---|
| [01 Concept of Operations](docs/01-ConOps.md) | Purpose, shortfall, users, operational constraints |
| [02 System Requirements](docs/02-Requirements.md) | 40 numbered "shall" statements with verification method and source |
| [03 Architecture and ICD](docs/03-Architecture-ICD.md) | Components, interface definitions, design decisions |
| [04 Trade Study](docs/04-Trade-Study.md) | Weighted comparison of five ADS-B data sources, with live measurements |
| [05 Shortfall Analysis](docs/05-Shortfall-Analysis.md) | Required vs observed ADS-B performance in the New York / Philadelphia area, from a one-hour capture |
| [06 Safety Risk Assessment](docs/06-Safety-Risk-Assessment.md) | Hazards from trusting the output wrongly, controls, residual risk |
| [07 Verification Plan](docs/07-Verification-Plan.md) | Test levels, independent validation, open verification gaps |
| [Traceability Matrix](docs/RTM.md) | Generated from test tags; CI fails if any requirement is unverified |
| [requirements.reqif](docs/requirements.reqif) | The same requirements and verification links as ReqIF 1.2, importable into DOORS Next, Jama or Polarion; CI validates it against the OMG schema |

### How this maps to FAA acquisition documents

FAA programs follow the Acquisition Management System (AMS). Each document here has an AMS counterpart; programs
tailor the exact templates.

| AMS artifact | This repository |
|---|---|
| Shortfall Analysis | [05 Shortfall Analysis](docs/05-Shortfall-Analysis.md) |
| Concept of Operations | [01 ConOps](docs/01-ConOps.md) |
| Preliminary and final Program Requirements (pPR, fPR) | [02 Requirements](docs/02-Requirements.md), exported as [ReqIF](docs/requirements.reqif) |
| Alternatives analysis | [04 Trade Study](docs/04-Trade-Study.md) |
| Interface Requirements and Control Documents (IRD, ICD) | [03 Architecture and ICD](docs/03-Architecture-ICD.md) |
| Safety Risk Management Document (SRMD) | [06 Safety Risk Assessment](docs/06-Safety-Risk-Assessment.md) |
| Test and Evaluation Master Plan (TEMP) and verification traceability (VRTM) | [07 Verification Plan](docs/07-Verification-Plan.md) and the generated [RTM](docs/RTM.md) |

## One hour over New York, Philadelphia and Atlantic City

240 polls at 15 s, 16:49–17:49 UTC on 2026-09-25, 100 NM around Atlantic City. Full
[Shortfall Analysis](docs/05-Shortfall-Analysis.md), [report](reports/nyphl-100nm-1h/report.md),
[map](reports/nyphl-100nm-1h/report.html), [CSV](reports/nyphl-100nm-1h/results.csv) and
[capture](captures/nyphl-100nm-1h.jsonl.gz). Identities are pseudonymized.

| Result | Aircraft |
|---|---|
| Evaluated | 812 |
| In airspace where 91.225(d) requires ADS-B, at some point | 765 |
| Meet all five 91.227(c)(1) minimums | 801 (98.6%) |
| Below a minimum | 5, of which **1 with high confidence inside rule airspace** (a business jet at NACv 0 for 112 polls) |
| Altitude off neighbors by more than 200 ft | 0 of 433 assessed |
| Weather model vs aircraft altitude trend | median disagreement 37 ft across 9 pressure levels |
| GNSS interference clusters | none |

A naive pass over the same hour (last-poll values, no ADS-R exclusion) reports 13 failures and 36 unevaluable
aircraft. The difference is measurement artifacts, which is the main finding: in public ADS-B data, the
measurement shortfall is larger than the equipment shortfall.

## What the live data changed

Every version of this tool passed its unit tests and was still wrong on real traffic. Each problem below was
found by running against live data, then fixed, tested, and written into the requirements.

| # | What real data showed | Fix | Req |
|---|---|---|---|
| 1 | One slow poll (20.5 s instead of 10 s) produced 69 false dropouts | Judge dropouts by the aggregator's own `seen_pos` clock | SYS-030 |
| 2 | Two airport service vehicles were scored against an aircraft rule | Exclude surface vehicles | SYS-018 |
| 3 | A 747 with a version-0 transmitter "failed" SIL on a value its transmitter never sends | List pre-DO-260B transmitters as not evaluable | SYS-017 |
| 4 | Landings were counted as dropouts | Report tracks that end separately | SYS-032 |
| 5 | An A320 dropped to NACp 0 for one 15 s poll, then recovered | Watch mode confirms a change over 2 polls and logs blips as TRANSIENT, to avoid alert fatigue | SYS-048 |
| 6 | A straight-line altitude model flagged two unrelated aircraft at 37,000 ft by the same +210 ft | Remove the trend, then compare each aircraft with its 8 nearest neighbors | SYS-033 |
| 7 | An E55P at 41,000 ft, the highest aircraft around, came out 222 ft off because every neighbor was below it | Only assess aircraft whose neighbors bracket them above and below | SYS-033 |
| 8 | A UAT aircraft's NACv alternated 0/2 poll to poll, so its verdict depended on which poll came last | Judge each indicator by its most frequent value; mark failures on unstable values as low confidence | SYS-019 |
| 9 | 36 airliners were set aside as "version 0"; 34 of them reported version 2 in most polls, but the last poll said 0 | Judge the ADS-B version by its most frequent value too | SYS-017 |
| 10 | Airliners powering up at the gate report zeros; three at one airport would look like a jammer | Interference screen covers airborne aircraft only | SYS-034 |
| 11 | ADS-R targets (UAT aircraft rebroadcast by FAA ground stations) failed far more often than direct transmitters | Read the decoder source: the UAT-to-1090 converter hard-codes NACv 0 (`uat2esnt.c:410`) and sends positions with NIC 0. Exclude those two fields on ADS-R | SYS-021 |
| 12 | The only high-confidence failure in the morning capture, a Cessna 210, was outside all airspace where 91.225(d) requires ADS-B | State rule applicability next to every finding, from FAA airspace data | SYS-036 |
| 13 | The aircraft-derived altitude trend needed checking against something the aircraft didn't report | Compare it with a weather model's pressure-level heights. It matched within a median of 42 to 84 ft across 9 levels. A ~100 ft offset in the first capture looked like the WGS-84 ellipsoid vs sea level (108 ft here), but a second capture didn't show it, so it stays unresolved rather than claimed | SYS-035 |

## Run it

Python 3.10+ and nothing else (standard library only).

```sh
# capture 5 minutes, 60 NM around ACY
python3 -m aim collect --lat 39.4576 --lon -74.5772 --radius 60 --polls 30 --interval 10 --out captures/acy.jsonl

# analyze: writes report.md, results.csv and report.html (map) to reports/
python3 -m aim analyze captures/acy.jsonl --redact --area "60 NM around ACY"

# optional enrichment (free, no keys): FAA airspace for rule applicability, FAA registry for year and
# certification (aircraft facts only), and a weather-model check of the altitude trend
python3 -m aim airspace --bbox=-76.9,37.8,-72.3,41.2 --out data/airspace-nyphl.json
python3 -m aim registry --out data/registry-aircraft.csv
python3 -m aim analyze captures/acy.jsonl --redact --weather --airspace data/airspace-nyphl.json \
  --registry data/registry-aircraft.csv --area "60 NM around ACY"

# live monitoring: alerts on emergencies and on integrity changes, until Ctrl-C
python3 -m aim watch --lat 39.4576 --lon -74.5772 --radius 60 --redact

# export requirements for a requirements database (ReqIF 1.2)
python3 -m aim reqif

# tests (set AIM_LIVE=1 to include the live-API test) and the traceability gate
python3 -m unittest discover -s tests
python3 -m aim rtm
```

Captures can be stored gzip-compressed (`.jsonl.gz`); `analyze` reads either form. A scheduled workflow
(`daily-capture`) records 30 minutes around ACY every day on GitHub's runners and keeps the capture and report as
a 90-day build artifact.

## Limits

Data comes from volunteer receivers aggregated by [adsb.lol](https://adsb.lol). Findings describe what those
receivers decoded, and are **not an FAA compliance determination**. Aircraft owners can get an authoritative
check from the FAA's free [Public ADS-B Performance Report](https://www.faa.gov/go/adsbpapr/). Published reports
replace aircraft identities with stable pseudonyms (`--redact`).

## License

Code: MIT. Captured data: adsb.lol, [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/).

Built by Matthew Karsten ([github.com/ExpertVagabond](https://github.com/ExpertVagabond)).
