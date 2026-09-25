# Concept of Operations: ADS-B Integrity Monitor

| | |
|---|---|
| Document | ConOps, v0.1 |
| Date | 2026-09-25 |
| Author | Matthew Karsten |
| Status | Draft for review |

## 1. Purpose

Since January 1, 2020, aircraft operating in most controlled U.S. airspace must broadcast ADS-B Out (14 CFR 91.225).
The quality of each broadcast matters as much as its presence. Controllers and automation systems can only use a
position report if its accuracy and integrity meet the minimums in 14 CFR 91.227(c)(1).

The ADS-B Integrity Monitor (AIM) is a small, open tool that watches public ADS-B data for a chosen area and reports
which aircraft are broadcasting quality indicators below those minimums, which are signalling an emergency, and where
tracks drop out or jump. It is a working demonstration of the systems engineering lifecycle on real surveillance data:
this ConOps, [requirements](02-Requirements.md), [architecture and interfaces](03-Architecture-ICD.md),
a [data-source trade study](04-Trade-Study.md), and a [traceability matrix](RTM.md) generated from the tests.

## 2. Current situation and shortfall

The FAA already monitors ADS-B Out performance with its own ground infrastructure and issues Public ADS-B
Performance Reports to operators. That data is authoritative but not open for independent analysis.

Public, crowdsourced ADS-B networks now decode the same broadcasts, including the quality indicators, and publish
them freely. What's missing is a transparent, repeatable way to turn that raw feed into findings tied to the
regulation, with every result traceable to a requirement and every requirement traceable to a test.

## 3. Proposed system

AIM runs in three steps:

1. **Collect.** Poll the adsb.lol API for a circular area on a fixed interval and record every response as a
   timestamped snapshot. Captures are replayable, so any finding can be reproduced later from the same data.
2. **Analyze.** For each aircraft seen in direct ADS-B or ADS-R reports, compare its NACp, NACv, NIC, SDA and SIL
   against 91.227(c)(1). Flag emergency codes (91.227(d)(9)). Across snapshots, flag dropouts and physically
   impossible position jumps.
3. **Report.** Produce a Markdown report that cites the paragraph behind every failure, a CSV for spreadsheet
   work, and a self-contained HTML page with a track map. Summarize results by aircraft category, altitude band and
   ADS-B version, and check each aircraft's two altitudes against the area trend.

## 4. Users and scenarios

| User | Scenario |
|---|---|
| Surveillance systems engineer | Captures an hour around a terminal area to see how many aircraft broadcast degraded integrity, and which indicators fail most. |
| Test engineer | Replays a stored capture after a code change and confirms the findings are unchanged. |
| Program analyst | Loads the CSV into Excel to summarize findings by aircraft type or operator. |

## 5. Operational constraints

- **Not authoritative.** Public receivers miss messages, and one missing indicator is reported as "not reported",
  never as a failure. Reports say so explicitly. AIM does not make compliance determinations.
- **Coverage limits.** Volunteer receivers cluster near cities. Dropouts can reflect receiver coverage, not the aircraft.
- **Good citizenship.** AIM never polls the public API faster than once every 5 seconds.
- **Privacy.** ADS-B is public, but a report that names an owner's aircraft as below a federal minimum is a
  different thing. Published reports use redaction mode, which replaces identities with stable pseudonyms.
- **Aircraft only.** Airport surface vehicles also broadcast ADS-B; they are excluded because 91.227 governs aircraft.
  Transmitters older than DO-260B are listed but not scored, because their quality values are synthesized by decoders.
- **Scope.** AIM checks the five 91.227(c)(1) indicators and emergency codes. It does not check broadcast latency
  (91.227(c)(2)-(3)) or the full (d) message set, because public aggregated feeds don't expose per-message timing.

## 6. Future work

- Add the FAA SWIM Cloud Distribution Service as an authoritative second source and compare the two.
- Validate positions against an independent measurement (radar or multilateration, e.g. via FAA SWIM). A second public
  ADS-B network such as OpenSky is not independent: it decodes the same self-reported broadcasts, so agreement
  between the two would prove nothing about the aircraft.
