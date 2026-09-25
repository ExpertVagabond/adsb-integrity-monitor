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
| SYS-017 | The system shall not evaluate quality indicators from transmitters reporting ADS-B version 0 or 1 (pre-DO-260B), and shall list them as "not evaluable" rather than failed. | T | 91.227(d); DO-260B |
| SYS-018 | The system shall exclude airport surface vehicles (emitter category C1 to C3, or type code SERV) from 91.227 evaluation and count them as excluded. | T | 91.227 applies to aircraft |

## Emergency and track checks

| ID | Requirement | Method | Source |
|---|---|---|---|
| SYS-020 | The system shall flag Mode A codes 7500, 7600 and 7700, and any non-"none" emergency status, with their meaning. | T | 91.227(d)(9) |
| SYS-030 | The system shall flag a dropout when the feed reports an aircraft's position as older than the coast threshold (default 20 s) and a newer position arrives later, or when the aircraft is absent from one or more snapshots between two sightings. Gaps between the monitor's own polls shall not count as dropouts. | T | ConOps 3.2 |
| SYS-031 | The system shall flag a position jump when consecutive positions imply a ground speed above 1,000 knots. | T | ConOps 3.2 |
| SYS-032 | The system shall report tracks whose position goes stale and is never refreshed within the capture separately, as informational, and shall not count them as dropouts. | T | ConOps 5 |

## Reporting

| ID | Requirement | Method | Source |
|---|---|---|---|
| SYS-040 | The system shall produce a Markdown report that cites the regulation paragraph for every failed indicator. | T | ConOps 3.3 |
| SYS-041 | The system shall export one CSV row per evaluated aircraft. | T | ConOps 4 |
| SYS-042 | Every report shall state that the data is crowdsourced and is not an FAA compliance determination. | T | ConOps 5 |
| SYS-043 | The system shall offer a redaction mode that replaces ICAO address, callsign and registration with stable pseudonyms, and published sample reports shall use it. | T | ConOps 5 |

## Engineering

| ID | Requirement | Method | Source |
|---|---|---|---|
| SYS-050 | The build shall generate the traceability matrix from test tags and fail if any requirement is unverified. | T | This document |
| SYS-060 | The system shall use only the Python standard library at runtime. | I | Architecture 4 |
