# ADS-B Integrity Report

- **Area:** 60 NM around Atlantic City Intl (ACY), next to the FAA William J. Hughes Technical Center
- **Window:** 2026-09-25 13:55:30 UTC to 2026-09-25 14:00:21 UTC (29 snapshots)
- **Aircraft:** 96 (direct ADS-B and ADS-R reports)
- **Excluded:** 2 (surface vehicle: 2)

> Source data is crowdsourced ADS-B from adsb.lol volunteer receivers. Results describe what public receivers decoded during the capture window. They are not an FAA compliance determination, and a single missing or degraded report can have many causes. Aircraft identities are replaced with stable pseudonyms.

## Summary against 14 CFR 91.227(c)(1)

| Verdict | Aircraft |
|---|---|
| All five indicators meet the minimum | 92 |
| At least one indicator below the minimum | 1 |
| No failures, but at least one indicator not reported | 2 |
| Not evaluable: pre-DO-260B transmitter | 1 |

| Indicator | Requirement | Pass | Fail | Not reported | Excluded (ADS-R converter) |
|---|---|---|---|---|---|
| nac_p | 91.227(c)(1)(i): NACp < 0.05 NM (NACp >= 8) | 93 | 1 | 1 | 0 |
| nac_v | 91.227(c)(1)(ii): NACv < 10 m/s (NACv >= 1) | 92 | 0 | 1 | 2 |
| nic | 91.227(c)(1)(iii): NIC < 0.2 NM (NIC >= 7) | 93 | 0 | 0 | 2 |
| sda | 91.227(c)(1)(iv): SDA <= 1e-5/flight hour (SDA >= 2) | 92 | 0 | 3 | 0 |
| sil | 91.227(c)(1)(v): SIL <= 1e-7 (SIL = 3) | 93 | 1 | 1 | 0 |

**Rule applicability (14 CFR 91.225(d)):** 89 of 96 aircraft were in airspace where ADS-B Out is required at some point in the window; 0 of the 1 below a minimum were among them.

## Aircraft below a 91.227(c)(1) minimum

| Aircraft | ICAO | Finding |
|---|---|---|
| C210 | AC-293978 | nac_p = 0, needs NACp < 0.05 NM (NACp >= 8) (91.227(c)(1)(i)) · not seen in 91.225(d) airspace |
| C210 | AC-293978 | sil = 0, needs SIL <= 1e-7 (SIL = 3) (91.227(c)(1)(v)) · not seen in 91.225(d) airspace |

## Emergency indications (91.227(d)(9))

None in this window.

## Track continuity (dropout threshold 20 s, jump limit 1,000 kt)

- C560 [on ground] `AC-214CE0`: dropout: absent from 4 snapshot(s), 61 s between sightings
- GLF5 `AC-5CF0AB`: dropout: position went at least 20 s without a refresh, then reacquired (threshold 20 s)
- LJ45 [on ground] `AC-E9BA9D`: dropout: position went at least 35 s without a refresh, then reacquired (threshold 20 s)
- B744 [on ground] `AC-6E85BD`: dropout: position went at least 55 s without a refresh, then reacquired (threshold 20 s)
- B744 [on ground] `AC-6E85BD`: dropout: absent from 5 snapshot(s), 71 s between sightings
- B744 [on ground] `AC-6E85BD`: dropout: absent from 1 snapshot(s), 20 s between sightings
- C172 `AC-A1E418`: dropout: position went at least 51 s without a refresh, then reacquired (threshold 20 s)
- C700 [on ground] `AC-F8BEFC`: dropout: position went at least 51 s without a refresh, then reacquired (threshold 20 s)
- C700 [on ground] `AC-F8BEFC`: dropout: absent from 6 snapshot(s), 80 s between sightings
- A321 [on ground] `AC-2C1CB5`: dropout: absent from 1 snapshot(s), 20 s between sightings

## Altitude consistency (barometric vs geometric, threshold 200 ft)

Area trend from 80 airborne aircraft: geometric minus barometric = -163 ft +48.2 ft per 1,000 ft (Theil-Sen fit). 76 aircraft were then compared with their nearest neighbors (within 75 NM and 10,000 ft); 4 had too few neighbors and were not assessed.

- C210 `AC-293978`: altitude: geometric minus barometric is -75 ft at 6,400 ft, -226 ft off its 8 nearest neighbors (threshold 200 ft)

## Independent check: weather model

Open-Meteo geopotential heights near 39.86N 75.03W for 2026-09-25 14:00 UTC (the model hour nearest the capture midpoint). The model's true height minus pressure altitude should match the aircraft-derived trend of geometric minus barometric altitude.

| Level | Pressure altitude | Weather model | ADS-B trend | Difference |
|---|---|---|---|---|
| 925 hPa | 2,499 ft | +168 ft | -42 ft | -211 ft |
| 850 hPa | 4,779 ft | +211 ft | +68 ft | -143 ft |
| 700 hPa | 9,878 ft | +394 ft | +314 ft | -80 ft |
| 600 hPa | 13,795 ft | +549 ft | +502 ft | -47 ft |
| 500 hPa | 18,281 ft | +784 ft | +719 ft | -65 ft |
| 400 hPa | 23,564 ft | +1,070 ft | +974 ft | -97 ft |
| 300 hPa | 30,053 ft | +1,401 ft | +1,287 ft | -114 ft |
| 250 hPa | 33,985 ft | +1,561 ft | +1,476 ft | -84 ft |
| 200 hPa | 38,662 ft | +1,678 ft | +1,702 ft | +25 ft |

Median disagreement 84 ft, largest 211 ft.

## GNSS interference screen

Brief drops below NACp 8 or NIC 7 by normally compliant aircraft: 0 aircraft-polls from 0 aircraft. A cluster needs at least 3 aircraft dropping in the same poll within 30 NM of each other.

No clustered drops. Nothing in this window looks like area-wide GNSS interference.

## Informational: unstable indicators

Verdicts use each indicator's most frequent value over the window. These aircraft had an indicator that switched between passing and failing values, so their verdict carries lower confidence.

- Plus 3 aircraft on the ground (listed in results.csv). All-zero moments on the ground are consistent with avionics acquiring GPS at the gate.

## Fleet statistics

### By emitter category

| Category | Aircraft | Fail | Not reported | Not evaluable | Fail rate |
|---|---|---|---|---|---|
| A3 Large (75,000-300,000 lb) | 55 | 0 | 2 | 0 | 0.0% |
| A2 Small (15,500-75,000 lb) | 20 | 0 | 0 | 1 | 0.0% |
| A1 Light (< 15,500 lb) | 13 | 1 | 0 | 0 | 7.7% |
| A4 High-vortex large (e.g. B757) | 3 | 0 | 0 | 0 | 0.0% |
| A7 Rotorcraft | 3 | 0 | 0 | 0 | 0.0% |
| A5 Heavy (> 300,000 lb) | 2 | 0 | 0 | 0 | 0.0% |

### By altitude band (91.225 boundaries)

| Band | Aircraft | Fail | Not reported | Not evaluable | Fail rate |
|---|---|---|---|---|---|
| Surface | 6 | 0 | 1 | 1 | 0.0% |
| Below 10,000 ft | 32 | 1 | 1 | 0 | 3.1% |
| 10,000 ft to FL180 | 25 | 0 | 0 | 0 | 0.0% |
| FL180 and above | 33 | 0 | 0 | 0 | 0.0% |

### By ADS-B version

| Version | Aircraft | Fail | Not reported | Not evaluable | Fail rate |
|---|---|---|---|---|---|
| version 2 | 93 | 0 | 2 | 0 | 0.0% |
| not reported | 2 | 1 | 0 | 0 | 50.0% |
| version 0 | 1 | 0 | 0 | 1 | 0.0% |

### By report type

| Report type | Aircraft | Fail | Not reported | Not evaluable | Fail rate |
|---|---|---|---|---|---|
| Direct 1090ES ADS-B | 94 | 0 | 2 | 1 | 0.0% |
| ADS-R (UAT rebroadcast by FAA ground station) | 2 | 1 | 0 | 0 | 50.0% |

### By certification basis (FAA registry)

| Certification | Aircraft | Fail | Not reported | Not evaluable | Fail rate |
|---|---|---|---|---|---|
| Type certificated | 89 | 1 | 2 | 1 | 1.1% |
| not in US registry | 7 | 0 | 0 | 0 | 0.0% |

### By decade of manufacture (FAA registry)

| Built | Aircraft | Fail | Not reported | Not evaluable | Fail rate |
|---|---|---|---|---|---|
| 1960s | 1 | 0 | 0 | 0 | 0.0% |
| 1970s | 3 | 0 | 0 | 0 | 0.0% |
| 1980s | 1 | 0 | 0 | 0 | 0.0% |
| 1990s | 11 | 0 | 1 | 0 | 0.0% |
| 2000s | 29 | 0 | 1 | 0 | 0.0% |
| 2010s | 22 | 0 | 0 | 1 | 0.0% |
| 2020s | 17 | 0 | 0 | 0 | 0.0% |
| unknown | 12 | 1 | 0 | 0 | 8.3% |

### Aircraft types with at least one failure

| Type | Aircraft | Fail | Not reported | Not evaluable | Fail rate |
|---|---|---|---|---|---|
| C210 | 1 | 1 | 0 | 0 | 100.0% |

## Informational: tracks lost and not reacquired

Usually a landing, taxiing out of receiver range, or leaving the area. Not counted as dropouts.

- C560 [on ground] `AC-214CE0`: last position 58 s old when last seen; not reacquired in the window
- E75L `AC-58B492`: last position 57 s old when last seen; not reacquired in the window
- M20P `AC-5A09A6`: last position 59 s old when last seen; not reacquired in the window
- A319 `AC-326F3E`: last position 23 s old when last seen; not reacquired in the window
- A319 [on ground] `AC-511BF4`: last position 59 s old when last seen; not reacquired in the window
- C700 `AC-127E43`: last position 52 s old when last seen; not reacquired in the window
- A321 [on ground] `AC-2C1CB5`: last position 54 s old when last seen; not reacquired in the window

## Informational: pre-DO-260B transmitters

- C560 [on ground] `AC-214CE0`: ADS-B version 0 (pre-DO-260B): quality indicators not evaluated
