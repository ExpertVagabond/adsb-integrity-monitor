# System Requirements: ADS-B Integrity Monitor

Each requirement has a unique ID, a verification method (**T**est, **A**nalysis, **I**nspection, **D**emonstration)
and its source. Tests cite the requirements they verify with a `verifies: SYS-xxx` tag, and
`python -m aim rtm` builds the [traceability matrix](RTM.md) from those tags. The build fails if any requirement
is left unverified.

## Ingest

| ID | Requirement | Method | Source |
|---|---|---|---|
| SYS-001 | The system shall retrieve ADS-B state data for a circular area defined by a center latitude/longitude and a radius of up to 250 NM from the adsb.lol v2 API. | D | ConOps 3.1 |
| SYS-002 | The system shall store each poll as one timestamped JSON Lines record so analysis can be replayed offline. | T | ConOps 3.1 |
| SYS-003 | The system shall not poll the public API more often than once every 5 seconds. | T | ConOps 5 |
| SYS-004 | The system shall continue a capture when an individual poll fails, logging the failure. | T | ConOps 5 |
| SYS-005 | The system shall read captures stored either as plain JSON Lines or gzip-compressed (.jsonl.gz). | T | Architecture 4 |
| SYS-006 | On HTTP 429, 5xx or a timeout, the system shall retry a poll up to twice with backoff (honoring a numeric Retry-After, capped at 30 s), and shall not retry other client errors. | T | Trade study risk: rate limiting |
| SYS-007 | During collect and watch, the system shall warn when a poll returns fewer than 20% of the median aircraft count of the previous 10 polls (after at least 3 polls). | T | Safety Risk Assessment HZ-8 |

## Performance checks (14 CFR 91.227(c)(1))

| ID | Requirement | Method | Source |
|---|---|---|---|
| SYS-010 | The system shall evaluate only direct 1090ES ADS-B (adsb_icao) and ADS-R (adsr_icao) reports, and shall count excluded report types (MLAT, TIS-B, Mode S) by type. | T | ConOps 3.2 |
| SYS-011 | The system shall flag a NACp below 8 (position accuracy not better than 0.05 NM). | T | 91.227(c)(1)(i) |
| SYS-012 | The system shall flag a NACv below 1 (velocity accuracy not better than 10 m/s). | T | 91.227(c)(1)(ii) |
| SYS-013 | The system shall flag a NIC below 7 (containment radius not less than 0.2 NM). | T | 91.227(c)(1)(iii) |
| SYS-014 | The system shall flag an SDA below 2 (design assurance worse than 1e-5 per flight hour). | T | 91.227(c)(1)(iv) |
| SYS-015 | The system shall flag a SIL below 3 (integrity worse than 1e-7). | T | 91.227(c)(1)(v) |
| SYS-016 | The system shall report a missing indicator as "not reported", distinct from a failure. | T | ConOps 5 |
| SYS-017 | The system shall not evaluate quality indicators from transmitters whose most frequently reported ADS-B version over the window is 0 or 1 (pre-DO-260B), and shall list them as "not evaluable" rather than failed. | T | 91.227(d); DO-260B |
| SYS-018 | The system shall exclude airport surface vehicles (emitter category C1 to C3, or type code SERV) from 91.227 evaluation and count them as excluded. | T | 91.227 applies to aircraft |
| SYS-019 | The system shall judge each indicator by its most frequent value over the capture window (ties go to the most recent value), shall note, as informational, indicators that switched between passing and failing values, and shall mark any failure that rests on such an indicator as low confidence. | T | Live-data finding: ADS-R NACv alternating 0/2 |
| SYS-021 | For ADS-R targets, the system shall exclude NACv and NIC from evaluation (reporting them as excluded, not failed), because UAT-to-1090 converters used by aggregator feeders insert default values for both; NACp, SIL and SDA shall still be evaluated. ADS-R targets shall not take part in the interference screen. | T | Source review: uat2esnt.c:410, :351-361; readsb track.c:2188 |

## Emergency and track checks

| ID | Requirement | Method | Source |
|---|---|---|---|
| SYS-020 | The system shall flag Mode A codes 7500, 7600 and 7700, and any non-"none" emergency status, with their meaning. | T | 91.227(d)(9) |
| SYS-030 | The system shall flag a dropout when the feed reports an aircraft's position as older than the coast threshold (default 20 s) and a newer position arrives later, or when the aircraft is absent from one or more snapshots between two sightings. Gaps between the monitor's own polls shall not count as dropouts. | T | ConOps 3.2 |
| SYS-031 | The system shall flag a position jump when consecutive positions imply a ground speed above 1,000 knots. | T | ConOps 3.2 |
| SYS-032 | The system shall report tracks whose position goes stale and is never refreshed within the capture separately, as informational, and shall not count them as dropouts. | T | ConOps 5 |
| SYS-033 | The system shall remove the area trend of geometric-minus-barometric altitude against barometric altitude (Theil-Sen fit over airborne aircraft at or above 1,000 ft, at least 10 aircraft), compare each aircraft's remainder with the median remainder of its 8 nearest neighbors within 75 NM and 10,000 ft (aircraft with fewer than 4 such neighbors, or whose neighbors are all above or all below them, are counted as not assessed and never flagged), and flag aircraft more than 200 ft (configurable) off. | T | ConOps 3.2 |
| SYS-034 | The system shall screen for possible GNSS interference by finding airborne, normally compliant aircraft (median NACp >= 8 and NIC >= 7 over the capture) that drop below those minimums in the same poll, and reporting groups of at least 3 such aircraft within 30 NM of each other. | T | FAA GNSS interference concern; ConOps 3.2 |
| SYS-035 | On request, the system shall compare the aircraft-derived altitude trend with an independent weather-model estimate (Open-Meteo geopotential height minus ICAO standard pressure altitude, at standard pressure levels inside the capture's altitude range) and report the disagreement at each level. | T | Independent validation of SYS-033 |
| SYS-036 | Given FAA airspace data, the system shall determine for each aircraft whether it was seen in airspace where 14 CFR 91.225(d) requires ADS-B Out (Class B/C; within 30 NM of an Appendix D Section 1 airport up to 10,000 ft MSL; above Class B/C ceilings within their lateral limits up to 10,000 ft MSL; at or above 10,000 ft MSL), cite the paragraph, and state it next to each finding. | T | 91.225(d); Part 91 Appendix D |
| SYS-037 | Given the FAA aircraft registry, the system shall build a lookup holding only Mode S address, year of manufacture, make, model and certification basis (never owner data), and shall break results out by certification basis and decade of manufacture. | T | Shortfall root-cause analysis |

## Reporting

| ID | Requirement | Method | Source |
|---|---|---|---|
| SYS-040 | The system shall produce a Markdown report that cites the regulation paragraph for every failed indicator. | T | ConOps 3.3 |
| SYS-041 | The system shall export one CSV row per evaluated aircraft. | T | ConOps 4 |
| SYS-042 | Every report shall state that the data is crowdsourced and is not an FAA compliance determination. | T | ConOps 5 |
| SYS-043 | The system shall offer a redaction mode that replaces ICAO address, callsign and registration with stable pseudonyms, and published sample reports shall use it. | T | ConOps 5 |
| SYS-044 | The system shall summarize results by emitter category, altitude band (surface, below 10,000 ft, 10,000 ft to FL180, FL180 and above, using each aircraft's highest altitude in the window) ADS-B version and report type (direct 1090ES vs ADS-R rebroadcast), and list aircraft types with at least one failure. | T | 91.225 airspace boundaries |
| SYS-045 | The system shall produce a self-contained HTML report (no external resources) with a map of every evaluated aircraft's track colored by verdict, honoring redaction mode. | T | ConOps 4 |
| SYS-046 | Watch mode shall alert when an evaluated aircraft first shows an emergency code or emergency status, or changes to a different one, and shall not repeat the alert while it is unchanged. | T | 91.227(d)(9) |
| SYS-047 | Watch mode shall alert when an aircraft's 91.227(c)(1) result changes from pass to fail or fail to pass, or fails when first seen; it shall stay silent for steady aircraft, excluded targets and incomplete records. | T | ConOps 6 |
| SYS-048 | Watch mode shall confirm a pass/fail change only after it holds for a configurable number of consecutive polls (default 2), and shall record a failure that clears before confirmation as a TRANSIENT event instead of discarding it. | T | Alert-fatigue finding, first live watch run |

## Engineering

| ID | Requirement | Method | Source |
|---|---|---|---|
| SYS-050 | The build shall generate the traceability matrix from test tags and fail if any requirement is unverified. | T | This document |
| SYS-051 | Continuous integration shall run the test suite and the traceability gate on every push, and fail if the committed RTM differs from the generated one. | T | This document |
| SYS-060 | The system shall use only the Python standard library at runtime. | I | Architecture 4 |
