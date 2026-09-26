# Verification Plan: ADS-B Integrity Monitor

| | |
|---|---|
| Document | Verification Plan, v0.2 |
| Date | 2026-09-25 |
| Traces to | [System Requirements](02-Requirements.md), [Traceability Matrix](RTM.md), [Safety Risk Assessment](06-Safety-Risk-Assessment.md) |

## 1. Verification methods

Each requirement names one method. Almost all are **Test**, because a test can be rerun on every change.

| Method | How it is performed here |
|---|---|
| **Test (T)** | Automated `unittest` cases. Each case carries a `verifies: SYS-xxx` tag, and the RTM is generated from those tags. |
| **Demonstration (D)** | A live run against the real service: `AIM_LIVE=1` enables the live-API tests (adsb.lol, Open-Meteo). |
| **Inspection (I)** | Reading an artifact. Where possible, inspections are automated too: SYS-060 parses every import, and SYS-051 reads the CI workflow file. |
| **Analysis (A)** | Reasoned comparison against an independent source. Used for the validation activities in section 4. |

## 2. Test levels

| Level | What it covers | Where |
|---|---|---|
| Unit | Each rule, threshold and boundary: every 91.227(c)(1) indicator tested at the value that passes and one below | `tests/test_rules.py`, `test_tracks.py`, `test_v2.py` |
| Replay regression | Every defect found on live data becomes a test that replays that situation: the slow poll (SYS-030), the version-0 747 (SYS-017), the A320 one-poll blip (SYS-048), the flip-flopping NACv (SYS-019), the E55P at the top of the traffic (SYS-033), gate power-up zeros (SYS-034), ADS-R converter defaults (SYS-021) | the tests named for each case |
| Integration | Capture file → analysis → Markdown, CSV and HTML, including redaction end to end | `tests/test_report.py`, `test_v2.py` |
| Live demonstration | Real API calls; checks the fields the ICD depends on still exist | `AIM_LIVE=1 python -m unittest discover -s tests` |

## 3. Environments and pass criteria

- **Python 3.10, 3.12 and 3.13** on GitHub-hosted Ubuntu runners, on every push (SYS-051), plus 3.11 and 3.14
  locally.
- A build passes only when:
  1. every test passes;
  2. `python -m aim rtm` reports every requirement verified;
  3. the committed `docs/RTM.md` matches the regenerated one.
  A requirement without a test fails the build. It can't silently go unverified.

## 4. Independent validation (beyond tests)

Tests prove the code does what the requirements say. Validation asks whether the requirements measure the
real world correctly. That needs sources the code didn't produce.

| Question | Independent source | Result so far |
|---|---|---|
| Is the altitude trend physically right? (SYS-033) | Open-Meteo weather model: true height of standard pressure levels minus ICAO pressure altitude (SYS-035) | 2026-09-25: the slope matches in both captures. 60 NM capture: median disagreement 84 ft, with a steady ~80 to 110 ft offset at mid levels. First 33 minutes of the 100 NM capture: median 42 ft, with no steady offset. The first offset matched the WGS-84 ellipsoid-to-sea-level separation (GEOID18, -32.8 m / -108 ft, NOAA NGS), but the second capture contradicts it, so the offset is **unresolved** (VG-5). |
| Are ADS-R NACv/NIC values real? (SYS-021) | Source code of the decoder chain (readsb, uat2esnt) | Converter hard-codes NACv 0 (`uat2esnt.c:410`) and sends positions as type codes 18/22 (NIC 0); readsb clears the version for ADS-R (`track.c:2188`). Values excluded. |
| Which aircraft does the rule bind? (SYS-036) | FAA ADDS airspace data; eCFR text of 91.225(d) and Appendix D | Sanity points verified: PHL surface (d)(1), ACY Class C at 3,000 ft (d)(1), EWR area at 8,000 ft (d)(3), FL350 (d)(4), rural NJ at 2,000 ft outside. |
| Will the requirements load into a requirements database? (SYS-052) | OMG ReqIF 1.2 schema and its 23 imported schemas, stored in `schemas/reqif/` and validated offline (`xmllint --nonet` with an XML catalog) in CI | Validates. Negative check: an export with an invalid identifier is rejected, so the validator is really checking. The schema doesn't check cross-references, so a test verifies every reference resolves. |
| Are the 91.227(c)(1) thresholds right? | eCFR text of 91.227 (fetched via the eCFR API) | Bounds transcribed into `rules.py` with paragraph citations. |

## 5. Verification gaps (open)

| ID | Gap | What would close it | Cost |
|---|---|---|---|
| VG-1 | No per-aircraft ground truth: findings rest on the aircraft's own reports | Own 1090 MHz + 978 MHz receivers (RTL-SDR, about $30 to $40 each) to see raw messages; or an owner-requested FAA PAPR for a flight we also captured | Hardware, or an owner's cooperation |
| VG-2 | ADS-R conclusion rests on source review, not observation | A 978 MHz receiver to compare the UAT broadcast with its 1090 rebroadcast | Hardware |
| VG-3 | Interference screen never exercised on a real event | Replay of a public capture that contains a documented interference event | Data availability |
| VG-5 | Whether fleet geometric altitude is referenced to the ellipsoid (DO-260B) or sea level: two captures disagree | More captures with the weather check (daily workflow), split by aircraft type, to see if the offset belongs to certain avionics | Time |
| VG-4 | One area, one afternoon | Daily 30-minute captures by the `daily-capture` workflow (free on GitHub) build a multi-day baseline | Time |
