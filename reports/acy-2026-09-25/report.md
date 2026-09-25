# ADS-B Integrity Report

- **Area:** 60 NM around Atlantic City Intl (ACY), next to the FAA William J. Hughes Technical Center
- **Window:** 2026-09-25 13:55:30 UTC to 2026-09-25 14:00:21 UTC (29 snapshots)
- **Aircraft:** 96 (direct ADS-B and ADS-R reports)
- **Excluded:** 2 (surface vehicle: 2)

> Source data is crowdsourced ADS-B from adsb.lol volunteer receivers. Results describe what public receivers decoded during the capture window. They are not an FAA compliance determination, and a single missing or degraded report can have many causes. Aircraft identities are replaced with stable pseudonyms.

## Summary against 14 CFR 91.227(c)(1)

| Verdict | Aircraft |
|---|---|
| All five indicators meet the minimum | 91 |
| At least one indicator below the minimum | 2 |
| No failures, but at least one indicator not reported | 2 |
| Not evaluable: pre-DO-260B transmitter | 1 |

| Indicator | Requirement | Pass | Fail | Not reported |
|---|---|---|---|---|
| nac_p | 91.227(c)(1)(i): NACp < 0.05 NM (NACp >= 8) | 93 | 1 | 1 |
| nac_v | 91.227(c)(1)(ii): NACv < 10 m/s (NACv >= 1) | 92 | 2 | 1 |
| nic | 91.227(c)(1)(iii): NIC < 0.2 NM (NIC >= 7) | 93 | 2 | 0 |
| sda | 91.227(c)(1)(iv): SDA <= 1e-5/flight hour (SDA >= 2) | 92 | 0 | 3 |
| sil | 91.227(c)(1)(v): SIL <= 1e-7 (SIL = 3) | 93 | 1 | 1 |

## Aircraft below a 91.227(c)(1) minimum

| Aircraft | ICAO | Finding |
|---|---|---|
| C210 | AC-293978 | nac_p = 0, needs NACp < 0.05 NM (NACp >= 8) (91.227(c)(1)(i)) |
| C210 | AC-293978 | nac_v = 0, needs NACv < 10 m/s (NACv >= 1) (91.227(c)(1)(ii)) |
| C210 | AC-293978 | nic = 0, needs NIC < 0.2 NM (NIC >= 7) (91.227(c)(1)(iii)) |
| C210 | AC-293978 | sil = 0, needs SIL <= 1e-7 (SIL = 3) (91.227(c)(1)(v)) |
| C172 | AC-C3174A | nac_v = 0, needs NACv < 10 m/s (NACv >= 1) (91.227(c)(1)(ii)) |
| C172 | AC-C3174A | nic = 0, needs NIC < 0.2 NM (NIC >= 7) (91.227(c)(1)(iii)) |

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

- B744 [on ground] `AC-6E85BD`: ADS-B version 0 (pre-DO-260B): quality indicators not evaluated
