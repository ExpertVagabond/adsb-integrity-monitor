# ADS-B Integrity Report

- **Area:** 100 NM around Atlantic City (ACY): Philadelphia, Atlantic City and New York approaches
- **Window:** 2026-09-25 16:49:07 UTC to 2026-09-25 17:48:53 UTC (240 snapshots)
- **Aircraft:** 812 (direct ADS-B and ADS-R reports)
- **Excluded:** 37 (adsb_other: 2, adsr_other: 1, mlat: 4, mode_s: 2, surface vehicle: 2, tisb_icao: 3, tisb_other: 9, tisb_trackfile: 14)

> Source data is crowdsourced ADS-B from adsb.lol volunteer receivers. Results describe what public receivers decoded during the capture window. They are not an FAA compliance determination, and a single missing or degraded report can have many causes. Aircraft identities are replaced with stable pseudonyms.

## Summary against 14 CFR 91.227(c)(1)

| Verdict | Aircraft |
|---|---|
| All five indicators meet the minimum | 801 |
| At least one indicator below the minimum | 5 |
| No failures, but at least one indicator not reported | 2 |
| Not evaluable: pre-DO-260B transmitter | 4 |

| Indicator | Requirement | Pass | Fail | Not reported | Excluded (ADS-R converter) |
|---|---|---|---|---|---|
| nac_p | 91.227(c)(1)(i): NACp < 0.05 NM (NACp >= 8) | 803 | 3 | 2 | 0 |
| nac_v | 91.227(c)(1)(ii): NACv < 10 m/s (NACv >= 1) | 799 | 1 | 0 | 8 |
| nic | 91.227(c)(1)(iii): NIC < 0.2 NM (NIC >= 7) | 799 | 1 | 0 | 8 |
| sda | 91.227(c)(1)(iv): SDA <= 1e-5/flight hour (SDA >= 2) | 805 | 0 | 3 | 0 |
| sil | 91.227(c)(1)(v): SIL <= 1e-7 (SIL = 3) | 803 | 3 | 2 | 0 |

**Rule applicability (14 CFR 91.225(d)):** 765 of 812 aircraft were in airspace where ADS-B Out is required at some point in the window; 3 of the 5 below a minimum were among them.

## Aircraft below a 91.227(c)(1) minimum

| Aircraft | ICAO | Finding |
|---|---|---|
| B39M [on ground] | AC-D773E1 | sil = 2, needs SIL <= 1e-7 (SIL = 3) (91.227(c)(1)(v)) **unstable: value alternated, low confidence** · in 91.225(d)(2) airspace |
| [on ground] | AC-F235DF | nac_p = 0, needs NACp < 0.05 NM (NACp >= 8) (91.227(c)(1)(i)) **unstable: value alternated, low confidence** · not seen in 91.225(d) airspace |
| [on ground] | AC-F235DF | nic = 0, needs NIC < 0.2 NM (NIC >= 7) (91.227(c)(1)(iii)) · not seen in 91.225(d) airspace |
| C182 [on ground] | AC-E4D49F | nac_p = 0, needs NACp < 0.05 NM (NACp >= 8) (91.227(c)(1)(i)) · not seen in 91.225(d) airspace |
| C182 [on ground] | AC-E4D49F | sil = 2, needs SIL <= 1e-7 (SIL = 3) (91.227(c)(1)(v)) · not seen in 91.225(d) airspace |
| C172 | AC-5B65DF | nac_p = 0, needs NACp < 0.05 NM (NACp >= 8) (91.227(c)(1)(i)) **unstable: value alternated, low confidence** · in 91.225(d)(1) airspace |
| C172 | AC-5B65DF | sil = 0, needs SIL <= 1e-7 (SIL = 3) (91.227(c)(1)(v)) **unstable: value alternated, low confidence** · in 91.225(d)(1) airspace |
| CL30 | AC-3BEB9D | nac_v = 0, needs NACv < 10 m/s (NACv >= 1) (91.227(c)(1)(ii)) · in 91.225(d)(4) airspace |

## Emergency indications (91.227(d)(9))

None in this window.

## Track continuity (dropout threshold 20 s, jump limit 1,000 kt)

- B788 [on ground] `AC-D9084D`: dropout: position went at least 53 s without a refresh, then reacquired (threshold 20 s)
- B788 [on ground] `AC-D9084D`: dropout: absent from 2 snapshot(s), 45 s between sightings
- B788 [on ground] `AC-D9084D`: dropout: absent from 1 snapshot(s), 30 s between sightings
- B77W [on ground] `AC-3C911C`: dropout: position went at least 49 s without a refresh, then reacquired (threshold 20 s)
- B77W [on ground] `AC-3C911C`: dropout: absent from 3 snapshot(s), 60 s between sightings
- A21N [on ground] `AC-ED7583`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- A21N [on ground] `AC-ED7583`: dropout: absent from 2 snapshot(s), 45 s between sightings
- A21N [on ground] `AC-ED7583`: dropout: absent from 2 snapshot(s), 45 s between sightings
- A21N [on ground] `AC-ED7583`: dropout: absent from 1 snapshot(s), 30 s between sightings
- CL60 [on ground] `AC-6C4178`: dropout: absent from 73 snapshot(s), 1111 s between sightings
- B772 [on ground] `AC-C5C883`: dropout: position went at least 53 s without a refresh, then reacquired (threshold 20 s)
- B772 [on ground] `AC-C5C883`: dropout: absent from 2 snapshot(s), 45 s between sightings
- GL7T [on ground] `AC-9A73B5`: dropout: position went at least 37 s without a refresh, then reacquired (threshold 20 s)
- B744 [on ground] `AC-094A9E`: dropout: position went at least 57 s without a refresh, then reacquired (threshold 20 s)
- B744 [on ground] `AC-094A9E`: dropout: absent from 1 snapshot(s), 30 s between sightings
- A333 [on ground] `AC-E94A99`: dropout: absent from 1 snapshot(s), 30 s between sightings
- A333 [on ground] `AC-372699`: dropout: absent from 1 snapshot(s), 31 s between sightings
- A333 [on ground] `AC-372699`: dropout: absent from 10 snapshot(s), 165 s between sightings
- B789 [on ground] `AC-29D938`: dropout: position went at least 51 s without a refresh, then reacquired (threshold 20 s)
- B789 [on ground] `AC-29D938`: dropout: absent from 17 snapshot(s), 270 s between sightings
- B77W [on ground] `AC-BC15C0`: dropout: position went at least 56 s without a refresh, then reacquired (threshold 20 s)
- B77W [on ground] `AC-BC15C0`: dropout: absent from 1 snapshot(s), 30 s between sightings
- B77W [on ground] `AC-BC15C0`: dropout: absent from 2 snapshot(s), 44 s between sightings
- A333 [on ground] `AC-EE1B96`: dropout: position went at least 54 s without a refresh, then reacquired (threshold 20 s)
- A333 [on ground] `AC-EE1B96`: dropout: absent from 11 snapshot(s), 180 s between sightings
- A339 [on ground] `AC-27A080`: dropout: position went at least 48 s without a refresh, then reacquired (threshold 20 s)
- A339 [on ground] `AC-27A080`: dropout: absent from 3 snapshot(s), 60 s between sightings
- GLEX `AC-096263`: dropout: position went at least 55 s without a refresh, then reacquired (threshold 20 s)
- GLEX `AC-096263`: dropout: absent from 4 snapshot(s), 76 s between sightings
- GLEX `AC-096263`: dropout: absent from 89 snapshot(s), 1350 s between sightings
- GLEX `AC-096263`: dropout: absent from 1 snapshot(s), 30 s between sightings
- GLEX `AC-096263`: dropout: absent from 1 snapshot(s), 30 s between sightings
- GLEX `AC-096263`: dropout: absent from 16 snapshot(s), 255 s between sightings
- GLEX `AC-096263`: dropout: absent from 2 snapshot(s), 44 s between sightings
- B748 [on ground] `AC-CE598F`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- B748 [on ground] `AC-CE598F`: dropout: absent from 6 snapshot(s), 106 s between sightings
- B748 [on ground] `AC-CE598F`: dropout: absent from 1 snapshot(s), 30 s between sightings
- B748 [on ground] `AC-CE598F`: dropout: absent from 17 snapshot(s), 270 s between sightings
- A388 [on ground] `AC-D20B08`: dropout: position went at least 60 s without a refresh, then reacquired (threshold 20 s)
- A388 [on ground] `AC-D20B08`: dropout: absent from 37 snapshot(s), 570 s between sightings
- A388 [on ground] `AC-D20B08`: dropout: absent from 3 snapshot(s), 60 s between sightings
- A388 [on ground] `AC-D20B08`: dropout: absent from 7 snapshot(s), 120 s between sightings
- B788 `AC-3D4082`: dropout: position went at least 53 s without a refresh, then reacquired (threshold 20 s)
- B788 `AC-3D4082`: dropout: absent from 2 snapshot(s), 45 s between sightings
- A35K [on ground] `AC-825583`: dropout: absent from 1 snapshot(s), 30 s between sightings
- B77W [on ground] `AC-31B73A`: dropout: position went at least 58 s without a refresh, then reacquired (threshold 20 s)
- B77W [on ground] `AC-31B73A`: dropout: absent from 1 snapshot(s), 30 s between sightings
- B77W [on ground] `AC-31B73A`: dropout: absent from 4 snapshot(s), 75 s between sightings
- B77W [on ground] `AC-31B73A`: dropout: absent from 2 snapshot(s), 44 s between sightings
- B77W [on ground] `AC-31B73A`: dropout: absent from 1 snapshot(s), 30 s between sightings
- A320 [on ground] `AC-F7E02B`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- A320 [on ground] `AC-F7E02B`: dropout: absent from 1 snapshot(s), 30 s between sightings
- C172 `AC-A755FF`: dropout: position went at least 44 s without a refresh, then reacquired (threshold 20 s)
- BCS1 [on ground] `AC-BBBCAD`: dropout: position went at least 57 s without a refresh, then reacquired (threshold 20 s)
- BCS1 [on ground] `AC-BBBCAD`: dropout: absent from 9 snapshot(s), 150 s between sightings
- BCS1 [on ground] `AC-BBBCAD`: dropout: absent from 78 snapshot(s), 1186 s between sightings
- unidentified `AC-DAB75B`: dropout: position went at least 60 s without a refresh, then reacquired (threshold 20 s)
- unidentified `AC-DAB75B`: dropout: absent from 3 snapshot(s), 60 s between sightings
- unidentified `AC-DAB75B`: dropout: absent from 1 snapshot(s), 31 s between sightings
- unidentified `AC-DAB75B`: dropout: absent from 15 snapshot(s), 240 s between sightings
- unidentified `AC-DAB75B`: dropout: absent from 1 snapshot(s), 29 s between sightings
- E75L [on ground] `AC-053414`: dropout: position went at least 55 s without a refresh, then reacquired (threshold 20 s)
- E75L [on ground] `AC-053414`: dropout: absent from 1 snapshot(s), 30 s between sightings
- E75L [on ground] `AC-053414`: dropout: absent from 1 snapshot(s), 31 s between sightings
- B78X [on ground] `AC-ACDE4A`: dropout: absent from 29 snapshot(s), 450 s between sightings
- PC12 `AC-5248B0`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- PC12 `AC-5248B0`: dropout: absent from 2 snapshot(s), 45 s between sightings
- S76 `AC-E2C661`: dropout: position went at least 57 s without a refresh, then reacquired (threshold 20 s)
- S76 `AC-E2C661`: dropout: absent from 15 snapshot(s), 240 s between sightings
- CRJ9 `AC-2C51E1`: dropout: position went at least 58 s without a refresh, then reacquired (threshold 20 s)
- CRJ9 `AC-2C51E1`: dropout: absent from 7 snapshot(s), 120 s between sightings
- EC35 `AC-C48D1D`: dropout: position went at least 60 s without a refresh, then reacquired (threshold 20 s)
- EC35 `AC-C48D1D`: dropout: absent from 14 snapshot(s), 225 s between sightings
- EC35 `AC-C48D1D`: dropout: absent from 58 snapshot(s), 885 s between sightings
- EC45 `AC-0B0656`: dropout: absent from 1 snapshot(s), 30 s between sightings
- EC45 `AC-0B0656`: dropout: absent from 49 snapshot(s), 750 s between sightings
- EC45 `AC-0B0656`: dropout: absent from 4 snapshot(s), 77 s between sightings
- A21N [on ground] `AC-4DB16A`: dropout: position went at least 55 s without a refresh, then reacquired (threshold 20 s)
- A21N [on ground] `AC-4DB16A`: dropout: absent from 3 snapshot(s), 60 s between sightings
- C172 `AC-131A97`: dropout: position went at least 52 s without a refresh, then reacquired (threshold 20 s)
- C172 `AC-131A97`: dropout: absent from 232 snapshot(s), 3496 s between sightings
- A321 [on ground] `AC-26AAFD`: dropout: position went at least 54 s without a refresh, then reacquired (threshold 20 s)
- A321 [on ground] `AC-26AAFD`: dropout: absent from 1 snapshot(s), 29 s between sightings
- P28A `AC-19C04A`: dropout: position went at least 54 s without a refresh, then reacquired (threshold 20 s)
- P28A `AC-19C04A`: dropout: absent from 1 snapshot(s), 30 s between sightings
- P28A `AC-19C04A`: dropout: absent from 166 snapshot(s), 2506 s between sightings
- P28A `AC-19C04A`: dropout: absent from 1 snapshot(s), 30 s between sightings
- B763 [on ground] `AC-C69662`: dropout: position went at least 29 s without a refresh, then reacquired (threshold 20 s)
- A321 [on ground] `AC-0A48A6`: dropout: position went at least 50 s without a refresh, then reacquired (threshold 20 s)
- B78X [on ground] `AC-70B8EF`: dropout: position went at least 50 s without a refresh, then reacquired (threshold 20 s)
- B78X [on ground] `AC-70B8EF`: dropout: absent from 2 snapshot(s), 44 s between sightings
- B752 `AC-2C44B2`: dropout: position went at least 58 s without a refresh, then reacquired (threshold 20 s)
- B752 `AC-2C44B2`: dropout: absent from 1 snapshot(s), 30 s between sightings
- B752 `AC-2C44B2`: dropout: absent from 6 snapshot(s), 105 s between sightings
- B763 [on ground] `AC-F6087C`: dropout: absent from 4 snapshot(s), 74 s between sightings
- B38M [on ground] `AC-B81F9B`: dropout: position went at least 54 s without a refresh, then reacquired (threshold 20 s)
- B38M [on ground] `AC-B81F9B`: dropout: absent from 2 snapshot(s), 44 s between sightings
- B38M [on ground] `AC-C9A2CE`: dropout: position went at least 60 s without a refresh, then reacquired (threshold 20 s)
- B38M [on ground] `AC-C9A2CE`: dropout: absent from 1 snapshot(s), 30 s between sightings
- B38M [on ground] `AC-C9A2CE`: dropout: absent from 2 snapshot(s), 46 s between sightings
- B38M [on ground] `AC-D177BB`: dropout: position went at least 54 s without a refresh, then reacquired (threshold 20 s)
- B38M [on ground] `AC-D177BB`: dropout: absent from 8 snapshot(s), 135 s between sightings
- B38M [on ground] `AC-D177BB`: dropout: absent from 3 snapshot(s), 60 s between sightings
- [on ground] `AC-8EEB8A`: dropout: absent from 2 snapshot(s), 45 s between sightings
- B763 `AC-45A5D0`: dropout: position went at least 53 s without a refresh, then reacquired (threshold 20 s)
- B763 `AC-45A5D0`: dropout: absent from 8 snapshot(s), 135 s between sightings
- B763 `AC-45A5D0`: dropout: absent from 3 snapshot(s), 60 s between sightings
- B39M `AC-0D3160`: dropout: position went at least 60 s without a refresh, then reacquired (threshold 20 s)
- B39M `AC-0D3160`: dropout: absent from 10 snapshot(s), 165 s between sightings
- B39M `AC-0D3160`: dropout: absent from 3 snapshot(s), 61 s between sightings
- B39M `AC-0D3160`: dropout: absent from 9 snapshot(s), 150 s between sightings
- S76 `AC-677043`: dropout: position went at least 54 s without a refresh, then reacquired (threshold 20 s)
- S76 `AC-677043`: dropout: absent from 88 snapshot(s), 1335 s between sightings
- [on ground] `AC-76866E`: dropout: absent from 5 snapshot(s), 89 s between sightings
- B38M `AC-C541FA`: dropout: position went at least 52 s without a refresh, then reacquired (threshold 20 s)
- B38M `AC-C541FA`: dropout: absent from 29 snapshot(s), 450 s between sightings
- B752 `AC-92C9A5`: dropout: position went at least 56 s without a refresh, then reacquired (threshold 20 s)
- B752 `AC-92C9A5`: dropout: absent from 12 snapshot(s), 194 s between sightings
- B752 `AC-92C9A5`: dropout: absent from 3 snapshot(s), 60 s between sightings
- CRJ9 [on ground] `AC-CEFB32`: dropout: position went at least 52 s without a refresh, then reacquired (threshold 20 s)
- CRJ9 [on ground] `AC-CEFB32`: dropout: absent from 7 snapshot(s), 120 s between sightings
- CRJ9 [on ground] `AC-CEFB32`: dropout: absent from 1 snapshot(s), 30 s between sightings
- CRJ9 `AC-5BF622`: dropout: position went at least 54 s without a refresh, then reacquired (threshold 20 s)
- CRJ9 `AC-5BF622`: dropout: absent from 9 snapshot(s), 150 s between sightings
- LJ60 `AC-D06001`: dropout: absent from 49 snapshot(s), 752 s between sightings
- B752 [on ground] `AC-77A78F`: dropout: position went at least 58 s without a refresh, then reacquired (threshold 20 s)
- B752 [on ground] `AC-77A78F`: dropout: absent from 6 snapshot(s), 105 s between sightings
- C172 `AC-C090F8`: dropout: position went at least 57 s without a refresh, then reacquired (threshold 20 s)
- C172 `AC-C090F8`: dropout: absent from 1 snapshot(s), 30 s between sightings
- E75L [on ground] `AC-487BC6`: dropout: position went at least 55 s without a refresh, then reacquired (threshold 20 s)
- E75L [on ground] `AC-487BC6`: dropout: absent from 1 snapshot(s), 30 s between sightings
- A21N [on ground] `AC-9A017F`: dropout: position went at least 49 s without a refresh, then reacquired (threshold 20 s)
- A21N [on ground] `AC-9A017F`: dropout: absent from 6 snapshot(s), 104 s between sightings
- E75L `AC-D71B58`: dropout: position went at least 47 s without a refresh, then reacquired (threshold 20 s)
- E75L `AC-D71B58`: dropout: absent from 1 snapshot(s), 30 s between sightings
- A21N [on ground] `AC-F64C78`: dropout: position went at least 32 s without a refresh, then reacquired (threshold 20 s)
- E75L `AC-F73FDA`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- E75L `AC-F73FDA`: dropout: absent from 8 snapshot(s), 135 s between sightings
- E75L `AC-F73FDA`: dropout: absent from 2 snapshot(s), 46 s between sightings
- E75L `AC-F73FDA`: dropout: absent from 8 snapshot(s), 136 s between sightings
- B06 `AC-C6A364`: dropout: position went at least 60 s without a refresh, then reacquired (threshold 20 s)
- B06 `AC-C6A364`: dropout: absent from 5 snapshot(s), 90 s between sightings
- B06 `AC-C6A364`: dropout: absent from 19 snapshot(s), 301 s between sightings
- B06 `AC-C6A364`: dropout: absent from 2 snapshot(s), 45 s between sightings
- B06 `AC-C6A364`: dropout: absent from 11 snapshot(s), 180 s between sightings
- B06 `AC-C6A364`: dropout: absent from 4 snapshot(s), 75 s between sightings
- B06 `AC-C6A364`: dropout: absent from 21 snapshot(s), 330 s between sightings
- TBM9 [on ground] `AC-C5DF94`: dropout: position went at least 31 s without a refresh, then reacquired (threshold 20 s)
- GLF4 `AC-E0A143`: dropout: position went at least 51 s without a refresh, then reacquired (threshold 20 s)
- GLF4 `AC-E0A143`: dropout: absent from 3 snapshot(s), 60 s between sightings
- GLF4 `AC-E0A143`: dropout: absent from 4 snapshot(s), 75 s between sightings
- GLF4 `AC-E0A143`: dropout: absent from 3 snapshot(s), 60 s between sightings
- GLF4 `AC-E0A143`: dropout: absent from 19 snapshot(s), 300 s between sightings
- E75L `AC-79A647`: dropout: position went at least 54 s without a refresh, then reacquired (threshold 20 s)
- E75L `AC-79A647`: dropout: absent from 3 snapshot(s), 60 s between sightings
- GLF5 [on ground] `AC-82CEE0`: dropout: absent from 1 snapshot(s), 31 s between sightings
- GLF5 [on ground] `AC-82CEE0`: dropout: absent from 2 snapshot(s), 45 s between sightings
- E75L [on ground] `AC-2656C6`: dropout: position went at least 53 s without a refresh, then reacquired (threshold 20 s)
- E75L [on ground] `AC-2656C6`: dropout: absent from 195 snapshot(s), 2941 s between sightings
- E75L [on ground] `AC-2656C6`: dropout: absent from 12 snapshot(s), 194 s between sightings
- B737 `AC-D9CF60`: dropout: position went at least 46 s without a refresh, then reacquired (threshold 20 s)
- B737 `AC-D9CF60`: dropout: absent from 12 snapshot(s), 195 s between sightings
- GLF6 [on ground] `AC-F91CE4`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- GLF6 [on ground] `AC-F91CE4`: dropout: absent from 2 snapshot(s), 45 s between sightings
- GLF6 [on ground] `AC-F91CE4`: dropout: absent from 8 snapshot(s), 135 s between sightings
- GLF6 [on ground] `AC-F91CE4`: dropout: absent from 80 snapshot(s), 1215 s between sightings
- B738 [on ground] `AC-F8148A`: dropout: absent from 4 snapshot(s), 76 s between sightings
- C172 `AC-7759CE`: dropout: position went at least 60 s without a refresh, then reacquired (threshold 20 s)
- S22T `AC-13A791`: dropout: position went at least 52 s without a refresh, then reacquired (threshold 20 s)
- S22T `AC-13A791`: dropout: absent from 59 snapshot(s), 901 s between sightings
- S22T `AC-13A791`: dropout: absent from 3 snapshot(s), 60 s between sightings
- unidentified `AC-D2A702`: dropout: absent from 26 snapshot(s), 405 s between sightings
- CRJ9 [on ground] `AC-986FAB`: dropout: position went at least 51 s without a refresh, then reacquired (threshold 20 s)
- CRJ9 [on ground] `AC-986FAB`: dropout: absent from 16 snapshot(s), 254 s between sightings
- C68A `AC-B0D6D3`: dropout: position went at least 48 s without a refresh, then reacquired (threshold 20 s)
- C68A `AC-B0D6D3`: dropout: absent from 2 snapshot(s), 45 s between sightings
- C68A `AC-B0D6D3`: dropout: absent from 7 snapshot(s), 120 s between sightings
- C68A `AC-B0D6D3`: dropout: absent from 3 snapshot(s), 60 s between sightings
- C68A `AC-B0D6D3`: dropout: absent from 1 snapshot(s), 28 s between sightings
- C68A `AC-B0D6D3`: dropout: absent from 7 snapshot(s), 120 s between sightings
- C68A `AC-B0D6D3`: dropout: absent from 7 snapshot(s), 123 s between sightings
- B38M `AC-F7C890`: dropout: absent from 7 snapshot(s), 121 s between sightings
- B737 `AC-8A4792`: dropout: position went at least 49 s without a refresh, then reacquired (threshold 20 s)
- B737 `AC-8A4792`: dropout: absent from 29 snapshot(s), 450 s between sightings
- B737 `AC-8A4792`: dropout: absent from 6 snapshot(s), 104 s between sightings
- G280 [on ground] `AC-CDDD18`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- G280 [on ground] `AC-CDDD18`: dropout: absent from 3 snapshot(s), 60 s between sightings
- G280 [on ground] `AC-CDDD18`: dropout: absent from 1 snapshot(s), 30 s between sightings
- G280 [on ground] `AC-CDDD18`: dropout: absent from 1 snapshot(s), 30 s between sightings
- B752 `AC-5ECFEC`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- B752 `AC-5ECFEC`: dropout: absent from 3 snapshot(s), 60 s between sightings
- B752 `AC-5ECFEC`: dropout: absent from 7 snapshot(s), 120 s between sightings
- PC24 `AC-576A3D`: dropout: position went at least 57 s without a refresh, then reacquired (threshold 20 s)
- PC24 `AC-576A3D`: dropout: absent from 115 snapshot(s), 1738 s between sightings
- CRJ9 `AC-7FE1A9`: dropout: position went at least 38 s without a refresh, then reacquired (threshold 20 s)
- CRJ9 [on ground] `AC-9EACC1`: dropout: position went at least 60 s without a refresh, then reacquired (threshold 20 s)
- CRJ9 [on ground] `AC-9EACC1`: dropout: absent from 25 snapshot(s), 391 s between sightings
- CRJ9 [on ground] `AC-9EACC1`: dropout: absent from 3 snapshot(s), 60 s between sightings
- CRJ9 [on ground] `AC-9EACC1`: dropout: absent from 8 snapshot(s), 136 s between sightings
- B789 `AC-603D80`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- B789 `AC-603D80`: dropout: absent from 23 snapshot(s), 360 s between sightings
- B789 `AC-603D80`: dropout: absent from 18 snapshot(s), 285 s between sightings
- BCS3 `AC-239FEA`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- BCS3 `AC-239FEA`: dropout: absent from 3 snapshot(s), 60 s between sightings
- BCS3 `AC-239FEA`: dropout: absent from 3 snapshot(s), 60 s between sightings
- BCS3 `AC-239FEA`: dropout: absent from 7 snapshot(s), 120 s between sightings
- P28A `AC-E413D2`: dropout: position went at least 54 s without a refresh, then reacquired (threshold 20 s)
- P28A `AC-E413D2`: dropout: absent from 58 snapshot(s), 885 s between sightings
- CRJ9 [on ground] `AC-0B1A0E`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- CRJ9 [on ground] `AC-0B1A0E`: dropout: absent from 7 snapshot(s), 120 s between sightings
- CRJ9 [on ground] `AC-0B1A0E`: dropout: absent from 1 snapshot(s), 30 s between sightings
- BCS3 [on ground] `AC-429264`: dropout: position went at least 57 s without a refresh, then reacquired (threshold 20 s)
- BCS3 [on ground] `AC-429264`: dropout: absent from 7 snapshot(s), 120 s between sightings
- BCS3 [on ground] `AC-429264`: dropout: absent from 1 snapshot(s), 30 s between sightings
- BCS3 [on ground] `AC-429264`: dropout: absent from 1 snapshot(s), 30 s between sightings
- B38M [on ground] `AC-51A03F`: dropout: position went at least 53 s without a refresh, then reacquired (threshold 20 s)
- B38M [on ground] `AC-51A03F`: dropout: absent from 4 snapshot(s), 75 s between sightings
- CL30 `AC-96CD5A`: dropout: position went at least 43 s without a refresh, then reacquired (threshold 20 s)
- CL30 `AC-8919B5`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- CL30 `AC-8919B5`: dropout: absent from 19 snapshot(s), 300 s between sightings
- CL30 `AC-8919B5`: dropout: absent from 2 snapshot(s), 46 s between sightings
- F2TH `AC-F82165`: dropout: position went at least 34 s without a refresh, then reacquired (threshold 20 s)
- B38M [on ground] `AC-D99017`: dropout: absent from 14 snapshot(s), 225 s between sightings
- BCS3 [on ground] `AC-515895`: dropout: position went at least 33 s without a refresh, then reacquired (threshold 20 s)
- AS50 `AC-C4B3EB`: dropout: position went at least 53 s without a refresh, then reacquired (threshold 20 s)
- AS50 `AC-C4B3EB`: dropout: absent from 6 snapshot(s), 105 s between sightings
- A20N `AC-9C84F4`: dropout: position went at least 53 s without a refresh, then reacquired (threshold 20 s)
- A20N `AC-9C84F4`: dropout: absent from 3 snapshot(s), 60 s between sightings
- BCS3 `AC-6E4340`: dropout: position went at least 51 s without a refresh, then reacquired (threshold 20 s)
- BCS3 `AC-6E4340`: dropout: absent from 3 snapshot(s), 60 s between sightings
- BCS3 [on ground] `AC-1A0B20`: dropout: position went at least 22 s without a refresh, then reacquired (threshold 20 s)
- BCS3 `AC-E62440`: dropout: position went at least 36 s without a refresh, then reacquired (threshold 20 s)
- A319 `AC-9AFDAF`: dropout: position went at least 51 s without a refresh, then reacquired (threshold 20 s)
- A319 `AC-9AFDAF`: dropout: absent from 3 snapshot(s), 60 s between sightings
- CRJ9 `AC-773E18`: dropout: position went at least 56 s without a refresh, then reacquired (threshold 20 s)
- CRJ9 `AC-773E18`: dropout: absent from 1 snapshot(s), 30 s between sightings
- CRJ9 `AC-773E18`: dropout: absent from 5 snapshot(s), 90 s between sightings
- CRJ9 `AC-773E18`: dropout: absent from 19 snapshot(s), 300 s between sightings
- unidentified `AC-F21DA3`: dropout: position went at least 28 s without a refresh, then reacquired (threshold 20 s)
- B38M [on ground] `AC-025591`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- B38M [on ground] `AC-025591`: dropout: absent from 1 snapshot(s), 30 s between sightings
- LJ60 [on ground] `AC-6101B5`: dropout: position went at least 60 s without a refresh, then reacquired (threshold 20 s)
- LJ60 [on ground] `AC-6101B5`: dropout: absent from 2 snapshot(s), 45 s between sightings
- LJ60 [on ground] `AC-6101B5`: dropout: absent from 1 snapshot(s), 29 s between sightings
- LJ60 [on ground] `AC-6101B5`: dropout: absent from 8 snapshot(s), 135 s between sightings
- LJ60 [on ground] `AC-6101B5`: dropout: absent from 34 snapshot(s), 526 s between sightings
- LJ60 [on ground] `AC-6101B5`: dropout: absent from 6 snapshot(s), 105 s between sightings
- E55P [on ground] `AC-C35AED`: dropout: position went at least 52 s without a refresh, then reacquired (threshold 20 s)
- E55P [on ground] `AC-C35AED`: dropout: absent from 31 snapshot(s), 480 s between sightings
- GLF5 `AC-E55039`: dropout: position went at least 53 s without a refresh, then reacquired (threshold 20 s)
- GLF5 `AC-E55039`: dropout: absent from 1 snapshot(s), 29 s between sightings
- GLF5 `AC-E55039`: dropout: absent from 3 snapshot(s), 60 s between sightings
- GLF5 `AC-E55039`: dropout: absent from 9 snapshot(s), 151 s between sightings
- GLF5 `AC-E55039`: dropout: absent from 6 snapshot(s), 105 s between sightings
- GLF5 `AC-E55039`: dropout: absent from 2 snapshot(s), 45 s between sightings
- M20P `AC-75A843`: dropout: position went at least 41 s without a refresh, then reacquired (threshold 20 s)
- B38M `AC-9F2CF2`: dropout: position went at least 54 s without a refresh, then reacquired (threshold 20 s)
- B38M `AC-9F2CF2`: dropout: absent from 19 snapshot(s), 300 s between sightings
- B38M `AC-9F2CF2`: dropout: absent from 10 snapshot(s), 165 s between sightings
- B738 `AC-CD9C2C`: dropout: position went at least 24 s without a refresh, then reacquired (threshold 20 s)
- B39M [on ground] `AC-D773E1`: dropout: position went at least 54 s without a refresh, then reacquired (threshold 20 s)
- B39M [on ground] `AC-D773E1`: dropout: absent from 16 snapshot(s), 255 s between sightings
- B39M [on ground] `AC-D773E1`: dropout: absent from 7 snapshot(s), 120 s between sightings
- B39M `AC-603376`: dropout: position went at least 54 s without a refresh, then reacquired (threshold 20 s)
- B39M `AC-603376`: dropout: absent from 14 snapshot(s), 225 s between sightings
- B39M `AC-603376`: dropout: absent from 14 snapshot(s), 226 s between sightings
- B39M `AC-603376`: dropout: absent from 3 snapshot(s), 60 s between sightings
- E55P [on ground] `AC-8F52F3`: dropout: position went at least 56 s without a refresh, then reacquired (threshold 20 s)
- E55P [on ground] `AC-8F52F3`: dropout: absent from 1 snapshot(s), 31 s between sightings
- E55P [on ground] `AC-8F52F3`: dropout: absent from 3 snapshot(s), 60 s between sightings
- E55P [on ground] `AC-8F52F3`: dropout: absent from 1 snapshot(s), 30 s between sightings
- E55P [on ground] `AC-8F52F3`: dropout: absent from 3 snapshot(s), 60 s between sightings
- E55P [on ground] `AC-8F52F3`: dropout: absent from 1 snapshot(s), 30 s between sightings
- B407 `AC-45FBD0`: dropout: position went at least 58 s without a refresh, then reacquired (threshold 20 s)
- B407 `AC-45FBD0`: dropout: absent from 112 snapshot(s), 1696 s between sightings
- A139 `AC-B222D0`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- A139 `AC-B222D0`: dropout: absent from 92 snapshot(s), 1396 s between sightings
- A20N `AC-F372B9`: dropout: position went at least 46 s without a refresh, then reacquired (threshold 20 s)
- A20N `AC-F372B9`: dropout: absent from 3 snapshot(s), 60 s between sightings
- C172 [on ground] `AC-F2D8D9`: dropout: absent from 5 snapshot(s), 90 s between sightings
- B739 [on ground] `AC-1FDAF7`: dropout: position went at least 55 s without a refresh, then reacquired (threshold 20 s)
- B739 [on ground] `AC-1FDAF7`: dropout: absent from 7 snapshot(s), 121 s between sightings
- A321 [on ground] `AC-D584B1`: dropout: absent from 1 snapshot(s), 30 s between sightings
- C510 [on ground] `AC-E03623`: dropout: position went at least 57 s without a refresh, then reacquired (threshold 20 s)
- C510 [on ground] `AC-E03623`: dropout: absent from 5 snapshot(s), 90 s between sightings
- A139 `AC-2BD16B`: dropout: position went at least 57 s without a refresh, then reacquired (threshold 20 s)
- [on ground] `AC-14E64C`: dropout: position went at least 53 s without a refresh, then reacquired (threshold 20 s)
- [on ground] `AC-14E64C`: dropout: absent from 2 snapshot(s), 45 s between sightings
- [on ground] `AC-14E64C`: dropout: absent from 2 snapshot(s), 46 s between sightings
- unidentified `AC-059236`: dropout: position went at least 50 s without a refresh, then reacquired (threshold 20 s)
- unidentified `AC-059236`: dropout: absent from 156 snapshot(s), 2356 s between sightings
- B407 `AC-02E195`: dropout: position went at least 53 s without a refresh, then reacquired (threshold 20 s)
- B407 `AC-02E195`: dropout: absent from 9 snapshot(s), 150 s between sightings
- B407 `AC-02E195`: dropout: absent from 9 snapshot(s), 150 s between sightings
- B407 `AC-02E195`: dropout: absent from 4 snapshot(s), 73 s between sightings
- B407 `AC-02E195`: dropout: absent from 5 snapshot(s), 89 s between sightings
- B407 `AC-02E195`: dropout: absent from 5 snapshot(s), 90 s between sightings
- B407 `AC-02E195`: dropout: absent from 3 snapshot(s), 60 s between sightings
- B407 `AC-02E195`: dropout: absent from 13 snapshot(s), 210 s between sightings
- E75L [on ground] `AC-1DA1A5`: dropout: position went at least 49 s without a refresh, then reacquired (threshold 20 s)
- E55P `AC-C9F30C`: dropout: position went at least 43 s without a refresh, then reacquired (threshold 20 s)
- E75L `AC-EE4DB7`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- E75L `AC-EE4DB7`: dropout: absent from 3 snapshot(s), 60 s between sightings
- E75L `AC-EE4DB7`: dropout: absent from 7 snapshot(s), 120 s between sightings
- E75L `AC-EE4DB7`: dropout: absent from 1 snapshot(s), 30 s between sightings
- E75L `AC-EE4DB7`: dropout: absent from 6 snapshot(s), 104 s between sightings
- AS50 `AC-821597`: dropout: position went at least 60 s without a refresh, then reacquired (threshold 20 s)
- AS50 `AC-821597`: dropout: absent from 17 snapshot(s), 271 s between sightings
- AS50 `AC-821597`: dropout: absent from 42 snapshot(s), 646 s between sightings
- E75L `AC-D76E81`: dropout: position went at least 52 s without a refresh, then reacquired (threshold 20 s)
- E75L `AC-D76E81`: dropout: absent from 7 snapshot(s), 120 s between sightings
- E75L `AC-D76E81`: dropout: absent from 8 snapshot(s), 135 s between sightings
- E75L `AC-BE8B1C`: dropout: position went at least 60 s without a refresh, then reacquired (threshold 20 s)
- E75L `AC-BE8B1C`: dropout: absent from 4 snapshot(s), 74 s between sightings
- E75L `AC-BE8B1C`: dropout: absent from 1 snapshot(s), 30 s between sightings
- E545 [on ground] `AC-6C9BC0`: dropout: position went at least 54 s without a refresh, then reacquired (threshold 20 s)
- E545 [on ground] `AC-6C9BC0`: dropout: absent from 3 snapshot(s), 60 s between sightings
- E545 [on ground] `AC-6C9BC0`: dropout: absent from 5 snapshot(s), 91 s between sightings
- C25C `AC-9E3A97`: dropout: position went at least 60 s without a refresh, then reacquired (threshold 20 s)
- C25C `AC-9E3A97`: dropout: absent from 1 snapshot(s), 30 s between sightings
- E75L [on ground] `AC-A33347`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- E75L [on ground] `AC-A33347`: dropout: absent from 4 snapshot(s), 75 s between sightings
- E75L [on ground] `AC-A33347`: dropout: absent from 4 snapshot(s), 75 s between sightings
- E75L [on ground] `AC-BFC2D5`: dropout: position went at least 54 s without a refresh, then reacquired (threshold 20 s)
- E75L [on ground] `AC-BFC2D5`: dropout: absent from 4 snapshot(s), 75 s between sightings
- B737 `AC-6740E5`: dropout: absent from 7 snapshot(s), 120 s between sightings
- A339 `AC-5C8369`: dropout: position went at least 58 s without a refresh, then reacquired (threshold 20 s)
- A339 `AC-5C8369`: dropout: absent from 18 snapshot(s), 287 s between sightings
- G280 [on ground] `AC-85AB06`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- C25B `AC-ADE715`: dropout: position went at least 55 s without a refresh, then reacquired (threshold 20 s)
- C25B `AC-ADE715`: dropout: absent from 122 snapshot(s), 1846 s between sightings
- C172 `AC-0B4496`: dropout: absent from 1 snapshot(s), 30 s between sightings
- CL35 `AC-FCA497`: dropout: absent from 16 snapshot(s), 255 s between sightings
- A21N [on ground] `AC-C848E0`: dropout: absent from 1 snapshot(s), 31 s between sightings
- A21N [on ground] `AC-C848E0`: dropout: absent from 2 snapshot(s), 45 s between sightings
- [on ground] `AC-F235DF`: dropout: absent from 2 snapshot(s), 45 s between sightings
- P28A `AC-387253`: dropout: position went at least 55 s without a refresh, then reacquired (threshold 20 s)
- P28A `AC-387253`: dropout: absent from 22 snapshot(s), 345 s between sightings
- P28A `AC-2C7A82`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- P28A `AC-2C7A82`: dropout: absent from 2 snapshot(s), 45 s between sightings
- P28A `AC-2C7A82`: dropout: absent from 7 snapshot(s), 121 s between sightings
- P28A `AC-2C7A82`: dropout: absent from 14 snapshot(s), 225 s between sightings
- P28A `AC-2C7A82`: dropout: absent from 12 snapshot(s), 195 s between sightings
- P28A `AC-2C7A82`: dropout: absent from 5 snapshot(s), 90 s between sightings
- B38M `AC-4E2C62`: dropout: position went at least 58 s without a refresh, then reacquired (threshold 20 s)
- B38M `AC-4E2C62`: dropout: absent from 14 snapshot(s), 225 s between sightings
- B38M `AC-4E2C62`: dropout: absent from 7 snapshot(s), 119 s between sightings
- B38M `AC-4E2C62`: dropout: absent from 11 snapshot(s), 180 s between sightings
- B39M [on ground] `AC-01FFA5`: dropout: position went at least 47 s without a refresh, then reacquired (threshold 20 s)
- B39M [on ground] `AC-01FFA5`: dropout: absent from 2 snapshot(s), 46 s between sightings
- B39M `AC-0551CD`: dropout: absent from 6 snapshot(s), 105 s between sightings
- B39M `AC-0551CD`: dropout: absent from 1 snapshot(s), 30 s between sightings
- EC45 `AC-E2E3E9`: dropout: position went at least 50 s without a refresh, then reacquired (threshold 20 s)
- EC45 `AC-E2E3E9`: dropout: absent from 1 snapshot(s), 30 s between sightings
- EC45 `AC-E2E3E9`: dropout: absent from 215 snapshot(s), 3241 s between sightings
- E55P `AC-3F5BFD`: dropout: position went at least 56 s without a refresh, then reacquired (threshold 20 s)
- E55P `AC-3F5BFD`: dropout: absent from 8 snapshot(s), 135 s between sightings
- E55P `AC-3F5BFD`: dropout: absent from 4 snapshot(s), 75 s between sightings
- H500 `AC-35241A`: dropout: position went at least 49 s without a refresh, then reacquired (threshold 20 s)
- H500 `AC-35241A`: dropout: absent from 5 snapshot(s), 90 s between sightings
- H500 `AC-35241A`: dropout: absent from 88 snapshot(s), 1336 s between sightings
- C68A [on ground] `AC-3AD13F`: dropout: position went at least 56 s without a refresh, then reacquired (threshold 20 s)
- B738 `AC-8BD5F9`: dropout: position went at least 58 s without a refresh, then reacquired (threshold 20 s)
- B738 `AC-8BD5F9`: dropout: absent from 16 snapshot(s), 256 s between sightings
- B738 `AC-8BD5F9`: dropout: absent from 7 snapshot(s), 121 s between sightings
- C172 `AC-E9BE20`: dropout: position went at least 58 s without a refresh, then reacquired (threshold 20 s)
- C172 `AC-E9BE20`: dropout: absent from 3 snapshot(s), 60 s between sightings
- P28A `AC-95749D`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- P28A `AC-95749D`: dropout: absent from 198 snapshot(s), 2986 s between sightings
- CRJ7 `AC-483812`: dropout: position went at least 54 s without a refresh, then reacquired (threshold 20 s)
- CRJ7 `AC-483812`: dropout: absent from 1 snapshot(s), 30 s between sightings
- CRJ7 `AC-483812`: dropout: absent from 3 snapshot(s), 60 s between sightings
- C337 `AC-240853`: dropout: position went at least 40 s without a refresh, then reacquired (threshold 20 s)
- CRJ7 [on ground] `AC-5F6732`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- CRJ7 [on ground] `AC-5F6732`: dropout: absent from 10 snapshot(s), 165 s between sightings
- CRJ7 `AC-108741`: dropout: position went at least 56 s without a refresh, then reacquired (threshold 20 s)
- CRJ7 `AC-108741`: dropout: absent from 12 snapshot(s), 195 s between sightings
- CRJ7 `AC-108741`: dropout: absent from 1 snapshot(s), 29 s between sightings
- T28 `AC-DE2EA2`: dropout: absent from 4 snapshot(s), 75 s between sightings
- [on ground] `AC-B90592`: dropout: absent from 7 snapshot(s), 120 s between sightings
- GA5C `AC-5AD882`: dropout: position went at least 24 s without a refresh, then reacquired (threshold 20 s)
- C172 [on ground] `AC-646CDA`: dropout: position went at least 55 s without a refresh, then reacquired (threshold 20 s)
- C172 [on ground] `AC-646CDA`: dropout: absent from 4 snapshot(s), 75 s between sightings
- B739 `AC-7D8EDD`: dropout: absent from 9 snapshot(s), 150 s between sightings
- C25A `AC-F5998D`: dropout: absent from 1 snapshot(s), 30 s between sightings
- C25A `AC-F5998D`: dropout: absent from 10 snapshot(s), 166 s between sightings
- C25A `AC-F5998D`: dropout: absent from 1 snapshot(s), 30 s between sightings
- F2TH [on ground] `AC-AA3091`: dropout: absent from 1 snapshot(s), 30 s between sightings
- CRJ7 `AC-D1AFC2`: dropout: position went at least 54 s without a refresh, then reacquired (threshold 20 s)
- CRJ7 `AC-D1AFC2`: dropout: absent from 3 snapshot(s), 60 s between sightings
- CRJ7 `AC-D1AFC2`: dropout: absent from 11 snapshot(s), 180 s between sightings
- CRJ7 [on ground] `AC-209ED1`: dropout: position went at least 53 s without a refresh, then reacquired (threshold 20 s)
- CRJ7 [on ground] `AC-209ED1`: dropout: absent from 2 snapshot(s), 45 s between sightings
- CRJ7 [on ground] `AC-658326`: dropout: position went at least 53 s without a refresh, then reacquired (threshold 20 s)
- CRJ7 [on ground] `AC-658326`: dropout: absent from 2 snapshot(s), 45 s between sightings
- CRJ7 [on ground] `AC-658326`: dropout: absent from 10 snapshot(s), 165 s between sightings
- K100 `AC-46C4DA`: dropout: position went at least 52 s without a refresh, then reacquired (threshold 20 s)
- K100 `AC-46C4DA`: dropout: absent from 30 snapshot(s), 466 s between sightings
- C56X `AC-3E6BBD`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- C56X `AC-3E6BBD`: dropout: absent from 8 snapshot(s), 135 s between sightings
- C56X `AC-3E6BBD`: dropout: absent from 1 snapshot(s), 30 s between sightings
- B38M [on ground] `AC-E63EA3`: dropout: absent from 2 snapshot(s), 45 s between sightings
- B738 `AC-4A862C`: dropout: position went at least 47 s without a refresh, then reacquired (threshold 20 s)
- B738 `AC-4A862C`: dropout: absent from 9 snapshot(s), 150 s between sightings
- [on ground] `AC-E842A4`: dropout: position went at least 60 s without a refresh, then reacquired (threshold 20 s)
- GLF4 `AC-B39CEB`: dropout: position went at least 57 s without a refresh, then reacquired (threshold 20 s)
- GLF4 `AC-B39CEB`: dropout: absent from 165 snapshot(s), 2490 s between sightings
- CL35 `AC-FD19E5`: dropout: position went at least 36 s without a refresh, then reacquired (threshold 20 s)
- A320 [on ground] `AC-B86FB5`: dropout: position went at least 60 s without a refresh, then reacquired (threshold 20 s)
- A320 [on ground] `AC-B86FB5`: dropout: absent from 44 snapshot(s), 675 s between sightings
- A320 [on ground] `AC-B86FB5`: dropout: absent from 27 snapshot(s), 419 s between sightings
- A320 [on ground] `AC-B86FB5`: dropout: absent from 2 snapshot(s), 46 s between sightings
- CRJ9 [on ground] `AC-D8C051`: dropout: absent from 1 snapshot(s), 31 s between sightings
- CL60 `AC-C0EBBD`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- CL60 `AC-C0EBBD`: dropout: absent from 22 snapshot(s), 345 s between sightings
- CL60 `AC-C0EBBD`: dropout: absent from 3 snapshot(s), 61 s between sightings
- E550 `AC-A00EC7`: dropout: position went at least 27 s without a refresh, then reacquired (threshold 20 s)
- GA6C `AC-CB28F1`: dropout: position went at least 60 s without a refresh, then reacquired (threshold 20 s)
- GA6C `AC-CB28F1`: dropout: absent from 6 snapshot(s), 105 s between sightings
- GA6C `AC-CB28F1`: dropout: absent from 3 snapshot(s), 60 s between sightings
- GA6C `AC-CB28F1`: dropout: absent from 16 snapshot(s), 255 s between sightings
- B609 `AC-3A8766`: dropout: position went at least 55 s without a refresh, then reacquired (threshold 20 s)
- GLEX [on ground] `AC-AFD6AB`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- GLEX [on ground] `AC-AFD6AB`: dropout: absent from 3 snapshot(s), 60 s between sightings
- GLEX [on ground] `AC-AFD6AB`: dropout: absent from 2 snapshot(s), 46 s between sightings
- GLEX [on ground] `AC-AFD6AB`: dropout: absent from 1 snapshot(s), 30 s between sightings
- GLEX [on ground] `AC-AFD6AB`: dropout: absent from 13 snapshot(s), 210 s between sightings
- GLEX [on ground] `AC-AFD6AB`: dropout: absent from 2 snapshot(s), 45 s between sightings
- GLEX [on ground] `AC-AFD6AB`: dropout: absent from 1 snapshot(s), 30 s between sightings
- GLEX [on ground] `AC-AFD6AB`: dropout: absent from 1 snapshot(s), 30 s between sightings
- GLEX [on ground] `AC-AFD6AB`: dropout: absent from 8 snapshot(s), 135 s between sightings
- GLEX [on ground] `AC-AFD6AB`: dropout: absent from 6 snapshot(s), 104 s between sightings
- GLEX [on ground] `AC-AFD6AB`: dropout: absent from 4 snapshot(s), 74 s between sightings
- GLEX [on ground] `AC-AFD6AB`: dropout: absent from 2 snapshot(s), 45 s between sightings
- GLEX [on ground] `AC-AFD6AB`: dropout: absent from 11 snapshot(s), 180 s between sightings
- GLEX [on ground] `AC-AFD6AB`: dropout: absent from 7 snapshot(s), 120 s between sightings
- GLEX [on ground] `AC-AFD6AB`: dropout: absent from 16 snapshot(s), 256 s between sightings
- H25B [on ground] `AC-8CFE55`: dropout: position went at least 54 s without a refresh, then reacquired (threshold 20 s)
- H25B [on ground] `AC-8CFE55`: dropout: absent from 1 snapshot(s), 30 s between sightings
- H25B [on ground] `AC-8CFE55`: dropout: absent from 1 snapshot(s), 30 s between sightings
- A21N [on ground] `AC-C0B040`: dropout: position went at least 58 s without a refresh, then reacquired (threshold 20 s)
- A21N [on ground] `AC-C0B040`: dropout: absent from 5 snapshot(s), 90 s between sightings
- C172 `AC-5B65DF`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- C172 `AC-5B65DF`: dropout: absent from 4 snapshot(s), 75 s between sightings
- A21N `AC-3C9203`: dropout: position went at least 60 s without a refresh, then reacquired (threshold 20 s)
- A21N `AC-3C9203`: dropout: absent from 3 snapshot(s), 60 s between sightings
- A21N `AC-3C9203`: dropout: absent from 1 snapshot(s), 30 s between sightings
- A21N `AC-3C9203`: dropout: absent from 5 snapshot(s), 90 s between sightings
- A21N `AC-3C9203`: dropout: absent from 4 snapshot(s), 75 s between sightings
- A21N `AC-3C9203`: dropout: absent from 1 snapshot(s), 30 s between sightings
- A21N `AC-3C9203`: dropout: absent from 3 snapshot(s), 63 s between sightings
- A21N `AC-3C9203`: dropout: absent from 4 snapshot(s), 75 s between sightings
- A21N `AC-3C9203`: dropout: absent from 9 snapshot(s), 150 s between sightings
- A21N `AC-3C9203`: dropout: absent from 1 snapshot(s), 30 s between sightings
- A21N `AC-3C9203`: dropout: absent from 1 snapshot(s), 30 s between sightings
- A21N `AC-3C9203`: dropout: absent from 4 snapshot(s), 75 s between sightings
- A21N `AC-3C9203`: dropout: absent from 1 snapshot(s), 30 s between sightings
- A21N `AC-3C9203`: dropout: absent from 5 snapshot(s), 90 s between sightings
- A21N `AC-3C9203`: dropout: absent from 1 snapshot(s), 31 s between sightings
- A320 `AC-022E01`: dropout: position went at least 52 s without a refresh, then reacquired (threshold 20 s)
- A320 `AC-022E01`: dropout: absent from 4 snapshot(s), 75 s between sightings
- E170 `AC-B49C74`: dropout: position went at least 52 s without a refresh, then reacquired (threshold 20 s)
- E170 `AC-B49C74`: dropout: absent from 11 snapshot(s), 180 s between sightings
- E170 `AC-B49C74`: dropout: absent from 6 snapshot(s), 105 s between sightings
- E170 `AC-B49C74`: dropout: absent from 14 snapshot(s), 226 s between sightings
- B763 [on ground] `AC-C7C09A`: dropout: absent from 5 snapshot(s), 89 s between sightings
- B764 [on ground] `AC-146C0D`: dropout: absent from 7 snapshot(s), 120 s between sightings
- A21N [on ground] `AC-44AF2D`: dropout: absent from 12 snapshot(s), 195 s between sightings
- B739 `AC-C49863`: dropout: position went at least 57 s without a refresh, then reacquired (threshold 20 s)
- B739 `AC-C49863`: dropout: absent from 17 snapshot(s), 270 s between sightings
- E550 `AC-7CCD62`: dropout: position went at least 35 s without a refresh, then reacquired (threshold 20 s)
- E145 [on ground] `AC-691336`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- E145 [on ground] `AC-691336`: dropout: absent from 12 snapshot(s), 195 s between sightings
- B739 [on ground] `AC-13C1EE`: dropout: position went at least 58 s without a refresh, then reacquired (threshold 20 s)
- B739 [on ground] `AC-13C1EE`: dropout: absent from 25 snapshot(s), 390 s between sightings
- A321 [on ground] `AC-98AA6B`: dropout: position went at least 31 s without a refresh, then reacquired (threshold 20 s)
- B752 `AC-18030B`: dropout: position went at least 51 s without a refresh, then reacquired (threshold 20 s)
- B752 `AC-18030B`: dropout: absent from 15 snapshot(s), 240 s between sightings
- C700 `AC-BC9F46`: dropout: position went at least 60 s without a refresh, then reacquired (threshold 20 s)
- C700 `AC-BC9F46`: dropout: absent from 6 snapshot(s), 105 s between sightings
- C700 `AC-BC9F46`: dropout: absent from 3 snapshot(s), 60 s between sightings
- H25B [on ground] `AC-DB5B25`: dropout: position went at least 56 s without a refresh, then reacquired (threshold 20 s)
- H25B [on ground] `AC-DB5B25`: dropout: absent from 99 snapshot(s), 1500 s between sightings
- E75L [on ground] `AC-B10278`: dropout: position went at least 52 s without a refresh, then reacquired (threshold 20 s)
- E75L [on ground] `AC-B10278`: dropout: absent from 5 snapshot(s), 90 s between sightings
- E75L `AC-0C276A`: dropout: absent from 5 snapshot(s), 89 s between sightings
- EC35 `AC-B47CE6`: dropout: position went at least 49 s without a refresh, then reacquired (threshold 20 s)
- E75L [on ground] `AC-8319DE`: dropout: position went at least 55 s without a refresh, then reacquired (threshold 20 s)
- E75L [on ground] `AC-8319DE`: dropout: absent from 2 snapshot(s), 45 s between sightings
- C172 `AC-63A796`: dropout: absent from 31 snapshot(s), 480 s between sightings
- C208 [on ground] `AC-E23DDE`: dropout: position went at least 47 s without a refresh, then reacquired (threshold 20 s)
- C208 [on ground] `AC-E23DDE`: dropout: absent from 2 snapshot(s), 46 s between sightings
- E75L `AC-016101`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- E75L `AC-016101`: dropout: absent from 5 snapshot(s), 90 s between sightings
- E75L `AC-016101`: dropout: absent from 1 snapshot(s), 30 s between sightings
- E75L `AC-016101`: dropout: absent from 11 snapshot(s), 180 s between sightings
- E75L `AC-016101`: dropout: absent from 11 snapshot(s), 180 s between sightings
- E75L `AC-016101`: dropout: absent from 2 snapshot(s), 45 s between sightings
- E75L [on ground] `AC-7A44DB`: dropout: position went at least 51 s without a refresh, then reacquired (threshold 20 s)
- E75L [on ground] `AC-7A44DB`: dropout: absent from 1 snapshot(s), 30 s between sightings
- E75L [on ground] `AC-7A44DB`: dropout: absent from 1 snapshot(s), 30 s between sightings
- A319 [on ground] `AC-A5CEB7`: dropout: absent from 1 snapshot(s), 30 s between sightings
- B752 [on ground] `AC-B8A253`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- B752 [on ground] `AC-B8A253`: dropout: absent from 6 snapshot(s), 105 s between sightings
- E75L [on ground] `AC-A2E40B`: dropout: position went at least 55 s without a refresh, then reacquired (threshold 20 s)
- E75L [on ground] `AC-A2E40B`: dropout: absent from 1 snapshot(s), 30 s between sightings
- E75L [on ground] `AC-A2E40B`: dropout: absent from 3 snapshot(s), 60 s between sightings
- B739 `AC-3695C9`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- B739 `AC-3695C9`: dropout: absent from 21 snapshot(s), 330 s between sightings
- B739 `AC-3695C9`: dropout: absent from 9 snapshot(s), 150 s between sightings
- B739 `AC-90B421`: dropout: position went at least 50 s without a refresh, then reacquired (threshold 20 s)
- B739 `AC-90B421`: dropout: absent from 22 snapshot(s), 345 s between sightings
- FBA2 `AC-4667DA`: dropout: position went at least 26 s without a refresh, then reacquired (threshold 20 s)
- C172 `AC-FB4113`: dropout: position went at least 57 s without a refresh, then reacquired (threshold 20 s)
- C172 `AC-FB4113`: dropout: absent from 37 snapshot(s), 570 s between sightings
- S76 `AC-6BAF0C`: dropout: position went at least 48 s without a refresh, then reacquired (threshold 20 s)
- S76 `AC-6BAF0C`: dropout: absent from 26 snapshot(s), 405 s between sightings
- B764 [on ground] `AC-31120B`: dropout: position went at least 56 s without a refresh, then reacquired (threshold 20 s)
- B764 [on ground] `AC-31120B`: dropout: absent from 12 snapshot(s), 195 s between sightings
- S76 [on ground] `AC-2954D0`: dropout: position went at least 60 s without a refresh, then reacquired (threshold 20 s)
- S76 [on ground] `AC-2954D0`: dropout: absent from 14 snapshot(s), 225 s between sightings
- S76 [on ground] `AC-2954D0`: dropout: absent from 55 snapshot(s), 840 s between sightings
- S76 [on ground] `AC-2954D0`: dropout: absent from 28 snapshot(s), 434 s between sightings
- E75L `AC-CE9C66`: dropout: position went at least 57 s without a refresh, then reacquired (threshold 20 s)
- E75L `AC-CE9C66`: dropout: absent from 1 snapshot(s), 30 s between sightings
- E75L `AC-CE9C66`: dropout: absent from 6 snapshot(s), 105 s between sightings
- E75L `AC-1EBFDF`: dropout: position went at least 56 s without a refresh, then reacquired (threshold 20 s)
- E75L `AC-1EBFDF`: dropout: absent from 6 snapshot(s), 105 s between sightings
- E75L `AC-1EBFDF`: dropout: absent from 1 snapshot(s), 31 s between sightings
- GLF4 `AC-E6E554`: dropout: position went at least 33 s without a refresh, then reacquired (threshold 20 s)
- B38M `AC-D6BA82`: dropout: position went at least 58 s without a refresh, then reacquired (threshold 20 s)
- B38M `AC-D6BA82`: dropout: absent from 10 snapshot(s), 165 s between sightings
- B38M `AC-D6BA82`: dropout: absent from 1 snapshot(s), 30 s between sightings
- B38M `AC-D6BA82`: dropout: absent from 2 snapshot(s), 45 s between sightings
- B38M `AC-D6BA82`: dropout: absent from 47 snapshot(s), 721 s between sightings
- B39M [on ground] `AC-B67C1A`: dropout: absent from 1 snapshot(s), 30 s between sightings
- B39M `AC-35B789`: dropout: position went at least 60 s without a refresh, then reacquired (threshold 20 s)
- B39M `AC-35B789`: dropout: absent from 2 snapshot(s), 45 s between sightings
- B39M `AC-35B789`: dropout: absent from 5 snapshot(s), 88 s between sightings
- B39M `AC-35B789`: dropout: absent from 31 snapshot(s), 480 s between sightings
- E75L `AC-63A5AD`: dropout: position went at least 56 s without a refresh, then reacquired (threshold 20 s)
- E75L `AC-63A5AD`: dropout: absent from 3 snapshot(s), 60 s between sightings
- E75L `AC-63A5AD`: dropout: absent from 4 snapshot(s), 75 s between sightings
- B738 `AC-96B562`: dropout: position went at least 51 s without a refresh, then reacquired (threshold 20 s)
- B738 `AC-96B562`: dropout: absent from 2 snapshot(s), 45 s between sightings
- B738 `AC-96B562`: dropout: absent from 5 snapshot(s), 90 s between sightings
- E75L [on ground] `AC-9635BB`: dropout: position went at least 56 s without a refresh, then reacquired (threshold 20 s)
- E75L [on ground] `AC-9635BB`: dropout: absent from 5 snapshot(s), 90 s between sightings
- GLEX `AC-0AE109`: dropout: position went at least 24 s without a refresh, then reacquired (threshold 20 s)
- B737 `AC-4198A4`: dropout: position went at least 60 s without a refresh, then reacquired (threshold 20 s)
- B737 `AC-4198A4`: dropout: absent from 4 snapshot(s), 74 s between sightings
- B737 `AC-4198A4`: dropout: absent from 5 snapshot(s), 90 s between sightings
- B737 `AC-4198A4`: dropout: absent from 1 snapshot(s), 31 s between sightings
- B737 `AC-4198A4`: dropout: absent from 1 snapshot(s), 30 s between sightings
- B737 `AC-4198A4`: dropout: absent from 1 snapshot(s), 30 s between sightings
- B737 `AC-4198A4`: dropout: absent from 4 snapshot(s), 75 s between sightings
- B737 `AC-4198A4`: dropout: absent from 13 snapshot(s), 211 s between sightings
- B737 `AC-4198A4`: dropout: absent from 6 snapshot(s), 105 s between sightings
- B737 [on ground] `AC-4FF4B4`: dropout: position went at least 52 s without a refresh, then reacquired (threshold 20 s)
- B737 [on ground] `AC-4FF4B4`: dropout: absent from 1 snapshot(s), 30 s between sightings
- B737 [on ground] `AC-4FF4B4`: dropout: absent from 4 snapshot(s), 78 s between sightings
- B737 [on ground] `AC-4FF4B4`: dropout: absent from 1 snapshot(s), 30 s between sightings
- B737 [on ground] `AC-4FF4B4`: dropout: absent from 8 snapshot(s), 135 s between sightings
- B737 [on ground] `AC-4FF4B4`: dropout: absent from 1 snapshot(s), 30 s between sightings
- B737 [on ground] `AC-4FF4B4`: dropout: absent from 4 snapshot(s), 75 s between sightings
- B737 [on ground] `AC-4FF4B4`: dropout: absent from 18 snapshot(s), 284 s between sightings
- E75L [on ground] `AC-B8DFE1`: dropout: position went at least 56 s without a refresh, then reacquired (threshold 20 s)
- E75L [on ground] `AC-B8DFE1`: dropout: absent from 2 snapshot(s), 45 s between sightings
- E75L [on ground] `AC-B8DFE1`: dropout: absent from 1 snapshot(s), 30 s between sightings
- A320 [on ground] `AC-6538C6`: dropout: absent from 2 snapshot(s), 45 s between sightings
- C172 `AC-E24453`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- C172 `AC-E24453`: dropout: absent from 2 snapshot(s), 45 s between sightings
- C172 `AC-E24453`: dropout: absent from 11 snapshot(s), 180 s between sightings
- SF50 `AC-A4B3E6`: dropout: position went at least 34 s without a refresh, then reacquired (threshold 20 s)
- B738 `AC-8C67C0`: dropout: position went at least 57 s without a refresh, then reacquired (threshold 20 s)
- B738 `AC-8C67C0`: dropout: absent from 2 snapshot(s), 45 s between sightings
- B738 `AC-8C67C0`: dropout: absent from 5 snapshot(s), 90 s between sightings
- B738 `AC-8C67C0`: dropout: absent from 3 snapshot(s), 60 s between sightings
- E170 [on ground] `AC-B66743`: dropout: position went at least 53 s without a refresh, then reacquired (threshold 20 s)
- C172 `AC-2D6A6C`: dropout: position went at least 53 s without a refresh, then reacquired (threshold 20 s)
- C172 `AC-2D6A6C`: dropout: absent from 2 snapshot(s), 46 s between sightings
- E170 `AC-DCB1A0`: dropout: position went at least 60 s without a refresh, then reacquired (threshold 20 s)
- E170 `AC-DCB1A0`: dropout: absent from 12 snapshot(s), 195 s between sightings
- E170 `AC-DCB1A0`: dropout: absent from 4 snapshot(s), 75 s between sightings
- E170 `AC-DCB1A0`: dropout: absent from 7 snapshot(s), 120 s between sightings
- CRJ9 [on ground] `AC-B3BD49`: dropout: position went at least 57 s without a refresh, then reacquired (threshold 20 s)
- CRJ9 [on ground] `AC-B3BD49`: dropout: absent from 14 snapshot(s), 225 s between sightings
- C700 [on ground] `AC-A088D3`: dropout: position went at least 57 s without a refresh, then reacquired (threshold 20 s)
- C700 [on ground] `AC-A088D3`: dropout: absent from 18 snapshot(s), 285 s between sightings
- C700 [on ground] `AC-A088D3`: dropout: absent from 1 snapshot(s), 30 s between sightings
- C700 [on ground] `AC-A088D3`: dropout: absent from 13 snapshot(s), 210 s between sightings
- B738 `AC-113689`: dropout: position went at least 47 s without a refresh, then reacquired (threshold 20 s)
- B738 `AC-113689`: dropout: absent from 8 snapshot(s), 136 s between sightings
- C25B `AC-6C7687`: dropout: position went at least 49 s without a refresh, then reacquired (threshold 20 s)
- C25B `AC-6C7687`: dropout: absent from 1 snapshot(s), 30 s between sightings
- C700 [on ground] `AC-F68F68`: dropout: position went at least 53 s without a refresh, then reacquired (threshold 20 s)
- C700 [on ground] `AC-F68F68`: dropout: absent from 9 snapshot(s), 150 s between sightings
- E170 [on ground] `AC-343A0D`: dropout: position went at least 58 s without a refresh, then reacquired (threshold 20 s)
- E170 [on ground] `AC-343A0D`: dropout: absent from 181 snapshot(s), 2731 s between sightings
- E170 [on ground] `AC-343A0D`: dropout: absent from 11 snapshot(s), 180 s between sightings
- E170 [on ground] `AC-343A0D`: dropout: absent from 1 snapshot(s), 30 s between sightings
- E170 [on ground] `AC-343A0D`: dropout: absent from 2 snapshot(s), 45 s between sightings
- C700 [on ground] `AC-BB9791`: dropout: position went at least 42 s without a refresh, then reacquired (threshold 20 s)
- E170 `AC-0C594C`: dropout: position went at least 51 s without a refresh, then reacquired (threshold 20 s)
- E170 `AC-0C594C`: dropout: absent from 39 snapshot(s), 600 s between sightings
- E170 `AC-520CBA`: dropout: position went at least 51 s without a refresh, then reacquired (threshold 20 s)
- E170 `AC-520CBA`: dropout: absent from 2 snapshot(s), 45 s between sightings
- B738 `AC-0A9BFD`: dropout: absent from 8 snapshot(s), 135 s between sightings
- B739 [on ground] `AC-016D57`: dropout: position went at least 60 s without a refresh, then reacquired (threshold 20 s)
- B739 [on ground] `AC-016D57`: dropout: absent from 5 snapshot(s), 90 s between sightings
- B739 [on ground] `AC-016D57`: dropout: absent from 1 snapshot(s), 30 s between sightings
- E75L `AC-603612`: dropout: position went at least 57 s without a refresh, then reacquired (threshold 20 s)
- E75L `AC-603612`: dropout: absent from 11 snapshot(s), 182 s between sightings
- B738 `AC-080524`: dropout: position went at least 57 s without a refresh, then reacquired (threshold 20 s)
- B738 `AC-080524`: dropout: absent from 30 snapshot(s), 465 s between sightings
- C25B [on ground] `AC-45E13B`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- C25B [on ground] `AC-45E13B`: dropout: absent from 3 snapshot(s), 60 s between sightings
- C700 [on ground] `AC-F27F01`: dropout: position went at least 57 s without a refresh, then reacquired (threshold 20 s)
- C700 [on ground] `AC-F27F01`: dropout: absent from 22 snapshot(s), 345 s between sightings
- C700 [on ground] `AC-F27F01`: dropout: absent from 7 snapshot(s), 120 s between sightings
- C700 [on ground] `AC-F27F01`: dropout: absent from 25 snapshot(s), 390 s between sightings
- C700 [on ground] `AC-F27F01`: dropout: absent from 3 snapshot(s), 60 s between sightings
- C700 [on ground] `AC-F27F01`: dropout: absent from 9 snapshot(s), 150 s between sightings
- C700 [on ground] `AC-F27F01`: dropout: absent from 3 snapshot(s), 60 s between sightings
- C700 [on ground] `AC-F27F01`: dropout: absent from 2 snapshot(s), 45 s between sightings
- C700 [on ground] `AC-F27F01`: dropout: absent from 16 snapshot(s), 255 s between sightings
- C700 [on ground] `AC-F27F01`: dropout: absent from 2 snapshot(s), 45 s between sightings
- C700 [on ground] `AC-F27F01`: dropout: absent from 1 snapshot(s), 30 s between sightings
- B788 [on ground] `AC-313A8F`: dropout: absent from 13 snapshot(s), 210 s between sightings
- F2TH `AC-3FAE2C`: dropout: position went at least 54 s without a refresh, then reacquired (threshold 20 s)
- F2TH `AC-3FAE2C`: dropout: absent from 6 snapshot(s), 105 s between sightings
- SF50 [on ground] `AC-08C2A8`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- SF50 [on ground] `AC-08C2A8`: dropout: absent from 10 snapshot(s), 165 s between sightings
- SF50 [on ground] `AC-08C2A8`: dropout: absent from 4 snapshot(s), 75 s between sightings
- SF50 [on ground] `AC-08C2A8`: dropout: absent from 1 snapshot(s), 30 s between sightings
- C700 `AC-C7C5C1`: dropout: position went at least 54 s without a refresh, then reacquired (threshold 20 s)
- C700 `AC-C7C5C1`: dropout: absent from 5 snapshot(s), 90 s between sightings
- C700 `AC-C7C5C1`: dropout: absent from 10 snapshot(s), 165 s between sightings
- C700 `AC-C7C5C1`: dropout: absent from 1 snapshot(s), 30 s between sightings
- C700 `AC-C7C5C1`: dropout: absent from 5 snapshot(s), 90 s between sightings
- C700 `AC-C7C5C1`: dropout: absent from 2 snapshot(s), 47 s between sightings
- B38M [on ground] `AC-9FAEC6`: dropout: absent from 4 snapshot(s), 75 s between sightings
- B38M [on ground] `AC-929B36`: dropout: position went at least 55 s without a refresh, then reacquired (threshold 20 s)
- B38M [on ground] `AC-929B36`: dropout: absent from 4 snapshot(s), 75 s between sightings
- B38M [on ground] `AC-929B36`: dropout: absent from 99 snapshot(s), 1501 s between sightings
- CL30 [on ground] `AC-779BC8`: dropout: position went at least 38 s without a refresh, then reacquired (threshold 20 s)
- B38M `AC-04DFFF`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- B38M `AC-04DFFF`: dropout: absent from 8 snapshot(s), 135 s between sightings
- B38M `AC-04DFFF`: dropout: absent from 1 snapshot(s), 30 s between sightings
- B38M `AC-04DFFF`: dropout: absent from 3 snapshot(s), 60 s between sightings
- B38M `AC-04DFFF`: dropout: absent from 7 snapshot(s), 122 s between sightings
- B38M `AC-AD747D`: dropout: position went at least 58 s without a refresh, then reacquired (threshold 20 s)
- B38M `AC-AD747D`: dropout: absent from 14 snapshot(s), 225 s between sightings
- C700 `AC-1171DE`: dropout: position went at least 55 s without a refresh, then reacquired (threshold 20 s)
- C700 `AC-1171DE`: dropout: absent from 31 snapshot(s), 480 s between sightings
- B712 `AC-FF884F`: dropout: position went at least 57 s without a refresh, then reacquired (threshold 20 s)
- B712 `AC-FF884F`: dropout: absent from 1 snapshot(s), 30 s between sightings
- B712 `AC-FF884F`: dropout: absent from 1 snapshot(s), 30 s between sightings
- B712 `AC-FF884F`: dropout: absent from 7 snapshot(s), 122 s between sightings
- B38M [on ground] `AC-F95597`: dropout: position went at least 58 s without a refresh, then reacquired (threshold 20 s)
- B38M [on ground] `AC-F95597`: dropout: absent from 7 snapshot(s), 119 s between sightings
- B38M `AC-9F32A2`: dropout: position went at least 53 s without a refresh, then reacquired (threshold 20 s)
- B38M `AC-9F32A2`: dropout: absent from 3 snapshot(s), 60 s between sightings
- A319 `AC-3CEC31`: dropout: position went at least 56 s without a refresh, then reacquired (threshold 20 s)
- A319 `AC-3CEC31`: dropout: absent from 62 snapshot(s), 945 s between sightings
- B38M `AC-37D598`: dropout: position went at least 54 s without a refresh, then reacquired (threshold 20 s)
- B38M `AC-37D598`: dropout: absent from 9 snapshot(s), 150 s between sightings
- C68A `AC-9CFE35`: dropout: position went at least 56 s without a refresh, then reacquired (threshold 20 s)
- C68A `AC-9CFE35`: dropout: absent from 15 snapshot(s), 240 s between sightings
- C68A `AC-9CFE35`: dropout: absent from 3 snapshot(s), 60 s between sightings
- C68A `AC-9CFE35`: dropout: absent from 4 snapshot(s), 74 s between sightings
- C68A `AC-9CFE35`: dropout: absent from 3 snapshot(s), 60 s between sightings
- B38M [on ground] `AC-F1A53B`: dropout: absent from 1 snapshot(s), 33 s between sightings
- CRJ9 [on ground] `AC-4A7259`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- CRJ9 [on ground] `AC-4A7259`: dropout: absent from 18 snapshot(s), 285 s between sightings
- B738 [on ground] `AC-A9EC53`: dropout: absent from 1 snapshot(s), 30 s between sightings
- CRJ9 [on ground] `AC-C3ACFF`: dropout: absent from 1 snapshot(s), 30 s between sightings
- B739 [on ground] `AC-438EA6`: dropout: absent from 11 snapshot(s), 180 s between sightings
- CRJ9 [on ground] `AC-EFD29D`: dropout: position went at least 22 s without a refresh, then reacquired (threshold 20 s)
- B712 `AC-AA657E`: dropout: position went at least 48 s without a refresh, then reacquired (threshold 20 s)
- B712 `AC-AA657E`: dropout: absent from 8 snapshot(s), 136 s between sightings
- C172 `AC-88D6E4`: dropout: position went at least 54 s without a refresh, then reacquired (threshold 20 s)
- C172 `AC-88D6E4`: dropout: absent from 1 snapshot(s), 30 s between sightings
- C172 `AC-88D6E4`: dropout: absent from 2 snapshot(s), 45 s between sightings
- EN28 `AC-B7F366`: dropout: position went at least 55 s without a refresh, then reacquired (threshold 20 s)
- B738 [on ground] `AC-F30ECC`: dropout: position went at least 51 s without a refresh, then reacquired (threshold 20 s)
- E545 [on ground] `AC-6AB49F`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- E545 [on ground] `AC-6AB49F`: dropout: absent from 3 snapshot(s), 60 s between sightings
- E545 [on ground] `AC-6AB49F`: dropout: absent from 1 snapshot(s), 30 s between sightings
- E545 [on ground] `AC-6AB49F`: dropout: absent from 2 snapshot(s), 45 s between sightings
- E545 [on ground] `AC-6AB49F`: dropout: absent from 1 snapshot(s), 30 s between sightings
- E545 [on ground] `AC-6AB49F`: dropout: absent from 2 snapshot(s), 45 s between sightings
- E545 [on ground] `AC-6AB49F`: dropout: absent from 2 snapshot(s), 45 s between sightings
- A321 `AC-3B98AD`: dropout: position went at least 53 s without a refresh, then reacquired (threshold 20 s)
- A321 `AC-3B98AD`: dropout: absent from 7 snapshot(s), 120 s between sightings
- A321 `AC-3B98AD`: dropout: absent from 2 snapshot(s), 45 s between sightings
- A321 `AC-3B98AD`: dropout: absent from 4 snapshot(s), 75 s between sightings
- B739 `AC-19DA47`: dropout: position went at least 55 s without a refresh, then reacquired (threshold 20 s)
- B739 `AC-19DA47`: dropout: absent from 11 snapshot(s), 178 s between sightings
- C172 [on ground] `AC-C73E83`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- GLF6 `AC-A73751`: dropout: position went at least 55 s without a refresh, then reacquired (threshold 20 s)
- GLF6 `AC-A73751`: dropout: absent from 1 snapshot(s), 30 s between sightings
- GLF6 `AC-A73751`: dropout: absent from 1 snapshot(s), 30 s between sightings
- B738 `AC-BC0741`: dropout: position went at least 47 s without a refresh, then reacquired (threshold 20 s)
- S76 [on ground] `AC-576004`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- S76 [on ground] `AC-576004`: dropout: absent from 2 snapshot(s), 45 s between sightings
- S76 [on ground] `AC-576004`: dropout: absent from 2 snapshot(s), 45 s between sightings
- S76 [on ground] `AC-576004`: dropout: absent from 2 snapshot(s), 44 s between sightings
- G2CA `AC-C106AC`: dropout: absent from 1 snapshot(s), 30 s between sightings
- B738 `AC-28EB27`: dropout: position went at least 58 s without a refresh, then reacquired (threshold 20 s)
- B738 `AC-28EB27`: dropout: absent from 4 snapshot(s), 75 s between sightings
- B738 `AC-28EB27`: dropout: absent from 3 snapshot(s), 62 s between sightings
- B738 `AC-28EB27`: dropout: absent from 3 snapshot(s), 60 s between sightings
- BE20 `AC-AB8770`: dropout: absent from 64 snapshot(s), 975 s between sightings
- H60 `AC-10F5F2`: dropout: position went at least 57 s without a refresh, then reacquired (threshold 20 s)
- H60 `AC-10F5F2`: dropout: absent from 27 snapshot(s), 420 s between sightings
- B762 `AC-D02663`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- B762 `AC-D02663`: dropout: absent from 4 snapshot(s), 75 s between sightings
- B762 `AC-D02663`: dropout: absent from 5 snapshot(s), 90 s between sightings
- A320 [on ground] `AC-7E9A5C`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- A320 [on ground] `AC-7E9A5C`: dropout: absent from 3 snapshot(s), 60 s between sightings
- A320 [on ground] `AC-7E9A5C`: dropout: absent from 2 snapshot(s), 45 s between sightings
- A320 [on ground] `AC-7E9A5C`: dropout: absent from 1 snapshot(s), 30 s between sightings
- C25B [on ground] `AC-28D448`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- C25B [on ground] `AC-28D448`: dropout: absent from 4 snapshot(s), 76 s between sightings
- C25B [on ground] `AC-28D448`: dropout: absent from 2 snapshot(s), 45 s between sightings
- C25B [on ground] `AC-28D448`: dropout: absent from 9 snapshot(s), 150 s between sightings
- C25B [on ground] `AC-28D448`: dropout: absent from 139 snapshot(s), 2101 s between sightings
- C25B [on ground] `AC-28D448`: dropout: absent from 1 snapshot(s), 30 s between sightings
- C25B [on ground] `AC-28D448`: dropout: absent from 3 snapshot(s), 60 s between sightings
- DH8D [on ground] `AC-867ECE`: dropout: position went at least 57 s without a refresh, then reacquired (threshold 20 s)
- DH8D [on ground] `AC-867ECE`: dropout: absent from 1 snapshot(s), 30 s between sightings
- DH8D [on ground] `AC-867ECE`: dropout: absent from 1 snapshot(s), 30 s between sightings
- GL7T [on ground] `AC-508054`: dropout: position went at least 50 s without a refresh, then reacquired (threshold 20 s)
- GL7T `AC-F065AC`: dropout: position went at least 49 s without a refresh, then reacquired (threshold 20 s)
- BCS3 [on ground] `AC-D06AB9`: dropout: position went at least 59 s without a refresh, then reacquired (threshold 20 s)
- BCS3 [on ground] `AC-D06AB9`: dropout: absent from 3 snapshot(s), 60 s between sightings
- CL60 `AC-C61F2C`: dropout: position went at least 22 s without a refresh, then reacquired (threshold 20 s)

## Altitude consistency (barometric vs geometric, threshold 200 ft)

Area trend from 493 airborne aircraft: geometric minus barometric = -113 ft +46.1 ft per 1,000 ft (Theil-Sen fit). 433 aircraft were then compared with their nearest neighbors (within 75 NM and 10,000 ft); 60 had too few neighbors and were not assessed.

No aircraft off the area trend.

## Independent check: weather model

Open-Meteo geopotential heights near 40.44N 74.54W for 2026-09-25 17:00 UTC (the model hour nearest the capture midpoint). The model's true height minus pressure altitude should match the aircraft-derived trend of geometric minus barometric altitude.

| Level | Pressure altitude | Weather model | ADS-B trend | Difference |
|---|---|---|---|---|
| 925 hPa | 2,499 ft | +145 ft | +3 ft | -143 ft |
| 850 hPa | 4,779 ft | +188 ft | +108 ft | -80 ft |
| 700 hPa | 9,878 ft | +335 ft | +343 ft | +8 ft |
| 600 hPa | 13,795 ft | +487 ft | +524 ft | +37 ft |
| 500 hPa | 18,281 ft | +715 ft | +731 ft | +16 ft |
| 400 hPa | 23,564 ft | +997 ft | +975 ft | -23 ft |
| 300 hPa | 30,053 ft | +1,327 ft | +1,274 ft | -53 ft |
| 250 hPa | 33,985 ft | +1,492 ft | +1,455 ft | -37 ft |
| 200 hPa | 38,662 ft | +1,617 ft | +1,671 ft | +54 ft |

Median disagreement 37 ft, largest 143 ft.

## GNSS interference screen

Brief drops below NACp 8 or NIC 7 by normally compliant aircraft: 23 aircraft-polls from 7 aircraft. A cluster needs at least 3 aircraft dropping in the same poll within 30 NM of each other.

No clustered drops. Nothing in this window looks like area-wide GNSS interference.

## Informational: unstable indicators

Verdicts use each indicator's most frequent value over the window. These aircraft had an indicator that switched between passing and failing values, so their verdict carries lower confidence.

- GLEX `AC-096263`: sil alternated between 2 and 3 (2 changes)
- B788 `AC-64F925`: sil alternated between 2 and 3 (1 change)
- unidentified `AC-DAB75B`: sil alternated between 2 and 3 (2 changes)
- C340 `AC-137B7C`: sil alternated between 2 and 3 (1 change)
- PC12 `AC-5248B0`: sil alternated between 2 and 3 (2 changes)
- S76 `AC-E2C661`: sil alternated between 2 and 3 (2 changes)
- B752 `AC-2C44B2`: sil alternated between 2 and 3 (3 changes)
- B763 `AC-45A5D0`: sil alternated between 2 and 3 (2 changes)
- B39M `AC-0D3160`: sil alternated between 2 and 3 (2 changes)
- S76 `AC-677043`: nac_p alternated between 0 and 10 (1 change); nic alternated between 0 and 8 (1 change); sil alternated between 0 and 3 (1 change)
- B38M `AC-C541FA`: sil alternated between 2 and 3 (2 changes)
- B752 `AC-92C9A5`: sil alternated between 2 and 3 (4 changes)
- E75L `AC-D71B58`: sil alternated between 2 and 3 (1 change)
- E75L `AC-F73FDA`: sil alternated between 2 and 3 (4 changes)
- B06 `AC-C6A364`: nac_p alternated between 0 and 10 (4 changes); nic alternated between 4 and 9 (4 changes); sil alternated between 0 and 3 (10 changes)
- B06 `AC-763E36`: nic alternated between 0 and 9 (1 change)
- GLF4 `AC-E0A143`: sil alternated between 2 and 3 (4 changes)
- E75L `AC-79A647`: sil alternated between 2 and 3 (2 changes)
- B737 `AC-D9CF60`: sil alternated between 2 and 3 (1 change)
- C172 `AC-7759CE`: sil alternated between 2 and 3 (3 changes)
- S22T `AC-13A791`: nac_p alternated between 0 and 10 (8 changes); nic alternated between 0 and 9 (6 changes); sil alternated between 2 and 3 (8 changes)
- unidentified `AC-D2A702`: sil alternated between 2 and 3 (1 change)
- B752 `AC-5ECFEC`: sil alternated between 2 and 3 (2 changes)
- B789 `AC-603D80`: nac_v alternated between 0 and 2 (2 changes); sil alternated between 2 and 3 (4 changes)
- BCS3 `AC-239FEA`: sil alternated between 2 and 3 (6 changes)
- P28A `AC-E413D2`: nac_p alternated between 0 and 9 (1 change); nic alternated between 0 and 9 (1 change); sil alternated between 2 and 3 (1 change)
- FA50 `AC-FCFC39`: nac_p alternated between 0 and 10 (1 change); nac_v alternated between 0 and 1 (1 change); nic alternated between 0 and 8 (1 change); sil alternated between 0 and 3 (1 change)
- CL30 `AC-8919B5`: sil alternated between 2 and 3 (4 changes)
- AS50 `AC-C4B3EB`: sil alternated between 2 and 3 (1 change)
- CRJ9 `AC-773E18`: sil alternated between 2 and 3 (6 changes)
- P28A `AC-5842C4`: sil alternated between 2 and 3 (1 change)
- GLF5 `AC-E55039`: sil alternated between 2 and 3 (4 changes)
- M20P `AC-75A843`: nac_p alternated between 0 and 10 (1 change); nac_v alternated between 0 and 2 (1 change); nic alternated between 0 and 8 (1 change); sil alternated between 0 and 3 (1 change)
- B38M `AC-9F2CF2`: sil alternated between 2 and 3 (2 changes)
- B39M `AC-603376`: sil alternated between 2 and 3 (4 changes)
- B407 `AC-02E195`: sil alternated between 2 and 3 (4 changes)
- E75L `AC-EE4DB7`: sil alternated between 2 and 3 (4 changes)
- AS50 `AC-821597`: sil alternated between 2 and 3 (2 changes)
- E75L `AC-D76E81`: nac_p alternated between 0 and 10 (4 changes); nac_v alternated between 0 and 2 (4 changes); nic alternated between 0 and 8 (4 changes); sil alternated between 2 and 3 (2 changes)
- E75L `AC-BE8B1C`: sil alternated between 2 and 3 (2 changes)
- A339 `AC-5C8369`: sil alternated between 2 and 3 (4 changes)
- C172 `AC-0B4496`: nac_p alternated between 0 and 10 (2 changes); nic alternated between 6 and 9 (2 changes); sil alternated between 0 and 3 (2 changes)
- E55P `AC-DD093E`: sil alternated between 2 and 3 (1 change)
- P28A `AC-387253`: sil alternated between 2 and 3 (2 changes)
- P28A `AC-2C7A82`: sil alternated between 2 and 3 (4 changes)
- B39M `AC-0551CD`: nac_v alternated between 0 and 2 (1 change); sil alternated between 2 and 3 (2 changes)
- E55P `AC-3F5BFD`: sil alternated between 2 and 3 (2 changes)
- C402 `AC-792307`: sil alternated between 2 and 3 (1 change)
- B738 `AC-8BD5F9`: sil alternated between 2 and 3 (3 changes)
- P28A `AC-95749D`: sil alternated between 2 and 3 (2 changes)
- CRJ7 `AC-483812`: sil alternated between 2 and 3 (3 changes)
- CRJ7 `AC-108741`: sil alternated between 2 and 3 (1 change)
- GA5C `AC-5AD882`: nac_p alternated between 0 and 10 (2 changes); sil alternated between 2 and 3 (2 changes)
- C25A `AC-F5998D`: sil alternated between 2 and 3 (3 changes)
- CRJ7 `AC-D1AFC2`: sil alternated between 2 and 3 (4 changes)
- K100 `AC-46C4DA`: nic alternated between 0 and 9 (3 changes)
- C56X `AC-3E6BBD`: sil alternated between 2 and 3 (2 changes)
- BE95 `AC-D2435C`: nac_p alternated between 0 and 10 (1 change); nac_v alternated between 0 and 1 (1 change); nic alternated between 0 and 8 (1 change); sil alternated between 0 and 3 (1 change)
- GLF4 `AC-B39CEB`: nac_p alternated between 0 and 10 (1 change); nac_v alternated between 0 and 2 (1 change); nic alternated between 0 and 8 (1 change); sil alternated between 0 and 3 (1 change)
- GA6C `AC-CB28F1`: nac_v alternated between 0 and 2 (1 change); sil alternated between 2 and 3 (7 changes)
- EC45 `AC-3B85D9`: sil alternated between 2 and 3 (1 change)
- C172 `AC-5B65DF`: nac_p alternated between 0 and 9 (1 change); sil alternated between 0 and 3 (1 change)
- A21N `AC-3C9203`: sil alternated between 2 and 3 (8 changes)
- E170 `AC-B49C74`: nac_p alternated between 0 and 10 (2 changes); nic alternated between 0 and 8 (2 changes); sil alternated between 2 and 3 (3 changes)
- B739 `AC-C49863`: sil alternated between 2 and 3 (2 changes)
- E145 `AC-A6670B`: sil alternated between 2 and 3 (1 change)
- B752 `AC-18030B`: sil alternated between 2 and 3 (2 changes)
- C700 `AC-BC9F46`: sil alternated between 2 and 3 (2 changes)
- unidentified `AC-B67B73`: sil alternated between 2 and 3 (1 change)
- E75L `AC-016101`: sil alternated between 2 and 3 (4 changes)
- B739 `AC-3695C9`: sil alternated between 2 and 3 (2 changes)
- B739 `AC-90B421`: sil alternated between 2 and 3 (3 changes)
- E75L `AC-CE9C66`: sil alternated between 2 and 3 (2 changes)
- E75L `AC-1EBFDF`: sil alternated between 2 and 3 (2 changes)
- B38M `AC-D6BA82`: sil alternated between 2 and 3 (6 changes)
- B39M `AC-35B789`: sil alternated between 2 and 3 (2 changes)
- E75L `AC-63A5AD`: sil alternated between 2 and 3 (2 changes)
- B737 `AC-4198A4`: sil alternated between 2 and 3 (7 changes)
- C172 `AC-E24453`: sil alternated between 2 and 3 (4 changes)
- B738 `AC-8C67C0`: sil alternated between 2 and 3 (4 changes)
- E170 `AC-DCB1A0`: sil alternated between 2 and 3 (2 changes)
- B738 `AC-FA0DEF`: sil alternated between 2 and 3 (1 change)
- PC12 `AC-26BD99`: sil alternated between 2 and 3 (1 change)
- C700 `AC-C7C5C1`: sil alternated between 2 and 3 (2 changes)
- B38M `AC-04DFFF`: sil alternated between 2 and 3 (4 changes)
- C700 `AC-1171DE`: sil alternated between 2 and 3 (2 changes)
- B712 `AC-FF884F`: sil alternated between 2 and 3 (3 changes)
- B38M `AC-37D598`: sil alternated between 2 and 3 (3 changes)
- C68A `AC-9CFE35`: sil alternated between 2 and 3 (4 changes)
- C172 `AC-88D6E4`: sil alternated between 2 and 3 (1 change)
- A139 `AC-A3F79A`: nac_p alternated between 0 and 10 (1 change); nac_v alternated between 0 and 2 (1 change); nic alternated between 0 and 8 (1 change); sil alternated between 0 and 3 (1 change)
- A321 `AC-3B98AD`: sil alternated between 2 and 3 (2 changes)
- B739 `AC-19DA47`: nac_p alternated between 0 and 10 (2 changes); nic alternated between 0 and 8 (2 changes); sil alternated between 2 and 3 (2 changes)
- GLF6 `AC-A73751`: sil alternated between 2 and 3 (2 changes)
- G2CA `AC-C106AC`: sil alternated between 2 and 3 (1 change)
- unidentified `AC-A73586`: nic alternated between 0 and 9 (1 change)
- B738 `AC-28EB27`: nac_p alternated between 0 and 9 (2 changes); nac_v alternated between 0 and 1 (2 changes); nic alternated between 0 and 8 (2 changes)
- PC12 `AC-DB8771`: nac_p alternated between 0 and 10 (1 change); nac_v alternated between 0 and 2 (1 change); nic alternated between 0 and 8 (1 change); sil alternated between 0 and 3 (1 change)
- H500 `AC-2B1187`: nac_p alternated between 0 and 10 (2 changes); nac_v alternated between 0 and 2 (2 changes); nic alternated between 0 and 9 (2 changes); sil alternated between 0 and 3 (2 changes)
- H60 `AC-10F5F2`: sil alternated between 2 and 3 (1 change)
- B762 `AC-D02663`: sil alternated between 2 and 3 (3 changes)
- A320 `AC-705368`: nac_p alternated between 0 and 9 (1 change); nic alternated between 0 and 8 (1 change); sil alternated between 0 and 3 (1 change)
- GL7T `AC-F065AC`: sil alternated between 2 and 3 (3 changes)
- Plus 100 aircraft on the ground (listed in results.csv). All-zero moments on the ground are consistent with avionics acquiring GPS at the gate.

## Fleet statistics

### By emitter category

| Category | Aircraft | Fail | Not reported | Not evaluable | Fail rate |
|---|---|---|---|---|---|
| A3 Large (75,000-300,000 lb) | 393 | 1 | 0 | 1 | 0.3% |
| A2 Small (15,500-75,000 lb) | 181 | 1 | 0 | 2 | 0.6% |
| A1 Light (< 15,500 lb) | 115 | 3 | 2 | 1 | 2.6% |
| A5 Heavy (> 300,000 lb) | 69 | 0 | 0 | 0 | 0.0% |
| A7 Rotorcraft | 40 | 0 | 0 | 0 | 0.0% |
| A4 High-vortex large (e.g. B757) | 7 | 0 | 0 | 0 | 0.0% |
| unknown | 4 | 0 | 0 | 0 | 0.0% |
| A0 | 1 | 0 | 0 | 0 | 0.0% |
| A6 High performance | 1 | 0 | 0 | 0 | 0.0% |
| D0 | 1 | 0 | 0 | 0 | 0.0% |

### By altitude band (91.225 boundaries)

| Band | Aircraft | Fail | Not reported | Not evaluable | Fail rate |
|---|---|---|---|---|---|
| Surface | 68 | 2 | 0 | 2 | 2.9% |
| Below 10,000 ft | 286 | 2 | 2 | 2 | 0.7% |
| 10,000 ft to FL180 | 109 | 0 | 0 | 0 | 0.0% |
| FL180 and above | 349 | 1 | 0 | 0 | 0.3% |

### By ADS-B version

| Version | Aircraft | Fail | Not reported | Not evaluable | Fail rate |
|---|---|---|---|---|---|
| version 2 | 801 | 3 | 1 | 0 | 0.4% |
| not reported | 7 | 2 | 1 | 0 | 28.6% |
| version 0 | 4 | 0 | 0 | 4 | 0.0% |

### By report type

| Report type | Aircraft | Fail | Not reported | Not evaluable | Fail rate |
|---|---|---|---|---|---|
| Direct 1090ES ADS-B | 804 | 3 | 1 | 4 | 0.4% |
| ADS-R (UAT rebroadcast by FAA ground station) | 8 | 2 | 1 | 0 | 25.0% |

### By certification basis (FAA registry)

| Certification | Aircraft | Fail | Not reported | Not evaluable | Fail rate |
|---|---|---|---|---|---|
| Type certificated | 735 | 4 | 2 | 4 | 0.5% |
| not in US registry | 63 | 0 | 0 | 0 | 0.0% |
| Not type certificated (experimental) | 14 | 1 | 0 | 0 | 7.1% |

### By decade of manufacture (FAA registry)

| Built | Aircraft | Fail | Not reported | Not evaluable | Fail rate |
|---|---|---|---|---|---|
| 1950s | 2 | 0 | 0 | 0 | 0.0% |
| 1960s | 6 | 0 | 1 | 0 | 0.0% |
| 1970s | 25 | 0 | 0 | 0 | 0.0% |
| 1980s | 12 | 0 | 0 | 0 | 0.0% |
| 1990s | 54 | 0 | 1 | 1 | 0.0% |
| 2000s | 231 | 3 | 0 | 2 | 1.3% |
| 2010s | 190 | 1 | 0 | 0 | 0.5% |
| 2020s | 194 | 1 | 0 | 0 | 0.5% |
| unknown | 98 | 0 | 0 | 1 | 0.0% |

### Aircraft types with at least one failure

| Type | Aircraft | Fail | Not reported | Not evaluable | Fail rate |
|---|---|---|---|---|---|
| unknown | 29 | 1 | 0 | 0 | 3.4% |
| C172 | 22 | 1 | 0 | 0 | 4.5% |
| B39M | 13 | 1 | 0 | 0 | 7.7% |
| CL30 | 6 | 1 | 0 | 0 | 16.7% |
| C182 | 4 | 1 | 0 | 0 | 25.0% |

## Informational: tracks lost and not reacquired

Usually a landing, taxiing out of receiver range, or leaving the area. Not counted as dropouts.

- CL60 [on ground] `AC-6C4178`: last position 58 s old when last seen; not reacquired in the window
- B772 [on ground] `AC-A63007`: last position 57 s old when last seen; not reacquired in the window
- A333 [on ground] `AC-E94A99`: last position 53 s old when last seen; not reacquired in the window
- A333 [on ground] `AC-372699`: last position 58 s old when last seen; not reacquired in the window
- A332 [on ground] `AC-B5ED55`: last position 51 s old when last seen; not reacquired in the window
- B77W [on ground] `AC-0083E3`: last position 57 s old when last seen; not reacquired in the window
- A35K [on ground] `AC-825583`: last position 58 s old when last seen; not reacquired in the window
- A321 [on ground] `AC-D0B4A5`: last position 54 s old when last seen; not reacquired in the window
- E75L [on ground] `AC-7CD8CD`: last position 46 s old when last seen; not reacquired in the window
- GLEX [on ground] `AC-7FC2C0`: last position 50 s old when last seen; not reacquired in the window
- A139 `AC-F14FD8`: last position 57 s old when last seen; not reacquired in the window
- B78X [on ground] `AC-ACDE4A`: last position 52 s old when last seen; not reacquired in the window
- A321 [on ground] `AC-4DC58B`: last position 49 s old when last seen; not reacquired in the window
- E75L [on ground] `AC-6FED6A`: last position 49 s old when last seen; not reacquired in the window
- E75L [on ground] `AC-2E16F4`: last position 56 s old when last seen; not reacquired in the window
- E75L [on ground] `AC-25373D`: last position 28 s old when last seen; not reacquired in the window
- C650 [on ground] `AC-A81AD9`: last position 56 s old when last seen; not reacquired in the window
- A321 [on ground] `AC-D58E89`: last position 45 s old when last seen; not reacquired in the window
- E75L [on ground] `AC-C6A241`: last position 57 s old when last seen; not reacquired in the window
- EC35 `AC-EC7182`: last position 55 s old when last seen; not reacquired in the window
- A321 [on ground] `AC-4D37D4`: last position 52 s old when last seen; not reacquired in the window
- CRJ9 [on ground] `AC-8A55C0`: last position 60 s old when last seen; not reacquired in the window
- SR20 [on ground] `AC-8E3EF3`: last position 56 s old when last seen; not reacquired in the window
- EC45 `AC-0B0656`: last position 60 s old when last seen; not reacquired in the window
- B763 [on ground] `AC-E55343`: last position 53 s old when last seen; not reacquired in the window
- A321 [on ground] `AC-F27376`: last position 55 s old when last seen; not reacquired in the window
- B763 [on ground] `AC-F6087C`: last position 53 s old when last seen; not reacquired in the window
- [on ground] `AC-8EEB8A`: last position 55 s old when last seen; not reacquired in the window
- [on ground] `AC-76866E`: last position 58 s old when last seen; not reacquired in the window
- B763 [on ground] `AC-47BBC6`: last position 58 s old when last seen; not reacquired in the window
- [on ground] `AC-42CD32`: last position 49 s old when last seen; not reacquired in the window
- SR20 `AC-357184`: last position 53 s old when last seen; not reacquired in the window
- B737 `AC-47CC1E`: last position 53 s old when last seen; not reacquired in the window
- B06 `AC-7B16E3`: last position 53 s old when last seen; not reacquired in the window
- E75L [on ground] `AC-4E2DCE`: last position 53 s old when last seen; not reacquired in the window
- E75L [on ground] `AC-5701E2`: last position 51 s old when last seen; not reacquired in the window
- BE55 [on ground] `AC-F73028`: last position 56 s old when last seen; not reacquired in the window
- C182 `AC-7FF973`: last position 48 s old when last seen; not reacquired in the window
- P28A [on ground] `AC-EBA4D8`: last position 47 s old when last seen; not reacquired in the window
- C172 `AC-0069A1`: last position 51 s old when last seen; not reacquired in the window
- B06 `AC-763E36`: last position 56 s old when last seen; not reacquired in the window
- unidentified `AC-99A475`: last position 46 s old when last seen; not reacquired in the window
- GLF5 [on ground] `AC-82CEE0`: last position 59 s old when last seen; not reacquired in the window
- C150 `AC-EAB93E`: last position 52 s old when last seen; not reacquired in the window
- SR20 `AC-28B4A5`: last position 59 s old when last seen; not reacquired in the window
- B738 [on ground] `AC-F8148A`: last position 49 s old when last seen; not reacquired in the window
- unidentified `AC-D2A702`: last position 59 s old when last seen; not reacquired in the window
- C25B [on ground] `AC-D5ED23`: last position 56 s old when last seen; not reacquired in the window
- FA50 [on ground] `AC-075F47`: last position 46 s old when last seen; not reacquired in the window
- C560 `AC-ADD993`: last position 58 s old when last seen; not reacquired in the window
- CRJ9 [on ground] `AC-EF3FB5`: last position 60 s old when last seen; not reacquired in the window
- A21N [on ground] `AC-792591`: last position 49 s old when last seen; not reacquired in the window
- BCS3 [on ground] `AC-05932D`: last position 46 s old when last seen; not reacquired in the window
- S22T [on ground] `AC-E13C19`: last position 56 s old when last seen; not reacquired in the window
- B38M [on ground] `AC-D99017`: last position 53 s old when last seen; not reacquired in the window
- C172 [on ground] `AC-3D34C3`: last position 33 s old when last seen; not reacquired in the window
- CRJ9 [on ground] `AC-960B0B`: last position 46 s old when last seen; not reacquired in the window
- CRJ9 [on ground] `AC-76BA3D`: last position 53 s old when last seen; not reacquired in the window
- CRJ9 [on ground] `AC-AC3CE3`: last position 57 s old when last seen; not reacquired in the window
- A321 `AC-564EE1`: last position 57 s old when last seen; not reacquired in the window
- A319 [on ground] `AC-24B81E`: last position 58 s old when last seen; not reacquired in the window
- GLF6 [on ground] `AC-7FC742`: last position 55 s old when last seen; not reacquired in the window
- C172 [on ground] `AC-F2D8D9`: last position 51 s old when last seen; not reacquired in the window
- A321 [on ground] `AC-D584B1`: last position 57 s old when last seen; not reacquired in the window
- C680 [on ground] `AC-076A01`: last position 55 s old when last seen; not reacquired in the window
- E75L [on ground] `AC-3CD0FF`: last position 49 s old when last seen; not reacquired in the window
- GLF5 [on ground] `AC-77A9F8`: last position 50 s old when last seen; not reacquired in the window
- A339 [on ground] `AC-707F42`: last position 48 s old when last seen; not reacquired in the window
- C172 `AC-0B4496`: last position 59 s old when last seen; not reacquired in the window
- E75L [on ground] `AC-379E4F`: last position 52 s old when last seen; not reacquired in the window
- B737 [on ground] `AC-A1E34E`: last position 57 s old when last seen; not reacquired in the window
- A21N [on ground] `AC-C848E0`: last position 58 s old when last seen; not reacquired in the window
- GLF4 `AC-8CE9C9`: last position 57 s old when last seen; not reacquired in the window
- EC35 `AC-CB8DAE`: last position 49 s old when last seen; not reacquired in the window
- [on ground] `AC-F235DF`: last position 60 s old when last seen; not reacquired in the window
- B39M `AC-0551CD`: last position 59 s old when last seen; not reacquired in the window
- C182 `AC-D65B6A`: last position 56 s old when last seen; not reacquired in the window
- CRJ9 [on ground] `AC-9FE7C7`: last position 54 s old when last seen; not reacquired in the window
- GLF4 [on ground] `AC-AADF63`: last position 58 s old when last seen; not reacquired in the window
- B06 `AC-E87FE2`: last position 56 s old when last seen; not reacquired in the window
- P28A `AC-84FC29`: last position 51 s old when last seen; not reacquired in the window
- [on ground] `AC-10B0F2`: last position 48 s old when last seen; not reacquired in the window
- SR22 `AC-E99093`: last position 46 s old when last seen; not reacquired in the window
- C68A `AC-BC1A64`: last position 50 s old when last seen; not reacquired in the window
- GL5T `AC-5CD576`: last position 52 s old when last seen; not reacquired in the window
- G280 `AC-FF9F07`: last position 58 s old when last seen; not reacquired in the window
- A321 [on ground] `AC-C0E2EB`: last position 49 s old when last seen; not reacquired in the window
- C182 [on ground] `AC-E4D49F`: last position 58 s old when last seen; not reacquired in the window
- T28 `AC-DE2EA2`: last position 48 s old when last seen; not reacquired in the window
- [on ground] `AC-B90592`: last position 57 s old when last seen; not reacquired in the window
- C25A `AC-F5998D`: last position 54 s old when last seen; not reacquired in the window
- CL35 [on ground] `AC-68049D`: last position 54 s old when last seen; not reacquired in the window
- F2TH [on ground] `AC-AA3091`: last position 59 s old when last seen; not reacquired in the window
- A321 [on ground] `AC-697CC1`: last position 53 s old when last seen; not reacquired in the window
- A21N [on ground] `AC-F513E9`: last position 53 s old when last seen; not reacquired in the window
- CRJ7 [on ground] `AC-8BA49F`: last position 46 s old when last seen; not reacquired in the window
- C750 [on ground] `AC-B1AC72`: last position 59 s old when last seen; not reacquired in the window
- CRJ9 `AC-9C069E`: last position 49 s old when last seen; not reacquired in the window
- B38M [on ground] `AC-E63EA3`: last position 56 s old when last seen; not reacquired in the window
- M20P [on ground] `AC-F5B2B5`: last position 48 s old when last seen; not reacquired in the window
- [on ground] `AC-22A798`: last position 56 s old when last seen; not reacquired in the window
- A320 [on ground] `AC-0AD17A`: last position 58 s old when last seen; not reacquired in the window
- PA46 `AC-6C7264`: last position 51 s old when last seen; not reacquired in the window
- C210 `AC-F0583E`: last position 54 s old when last seen; not reacquired in the window
- LJ60 [on ground] `AC-873896`: last position 53 s old when last seen; not reacquired in the window
- CRJ9 [on ground] `AC-D8C051`: last position 57 s old when last seen; not reacquired in the window
- P28A `AC-85C423`: last position 56 s old when last seen; not reacquired in the window
- P28A `AC-CAB770`: last position 52 s old when last seen; not reacquired in the window
- EC45 `AC-3B85D9`: last position 52 s old when last seen; not reacquired in the window
- BL8 `AC-78D9CF`: last position 47 s old when last seen; not reacquired in the window
- BE40 [on ground] `AC-C07973`: last position 48 s old when last seen; not reacquired in the window
- unidentified `AC-96BFF9`: last position 52 s old when last seen; not reacquired in the window
- E170 [on ground] `AC-45A2B0`: last position 55 s old when last seen; not reacquired in the window
- B763 [on ground] `AC-C7C09A`: last position 57 s old when last seen; not reacquired in the window
- B764 [on ground] `AC-146C0D`: last position 58 s old when last seen; not reacquired in the window
- [on ground] `AC-6B6C0F`: last position 55 s old when last seen; not reacquired in the window
- A21N [on ground] `AC-44AF2D`: last position 55 s old when last seen; not reacquired in the window
- B763 [on ground] `AC-E88654`: last position 46 s old when last seen; not reacquired in the window
- PC12 [on ground] `AC-5D2827`: last position 47 s old when last seen; not reacquired in the window
- SF50 `AC-44A7B4`: last position 51 s old when last seen; not reacquired in the window
- CL60 [on ground] `AC-7AFABB`: last position 54 s old when last seen; not reacquired in the window
- G280 [on ground] `AC-62FF88`: last position 54 s old when last seen; not reacquired in the window
- CL35 `AC-650792`: last position 52 s old when last seen; not reacquired in the window
- unidentified `AC-B67B73`: last position 51 s old when last seen; not reacquired in the window
- C208 [on ground] `AC-CFF4AD`: last position 59 s old when last seen; not reacquired in the window
- C172 `AC-8334D3`: last position 56 s old when last seen; not reacquired in the window
- C700 [on ground] `AC-D527A2`: last position 46 s old when last seen; not reacquired in the window
- A319 [on ground] `AC-A5CEB7`: last position 53 s old when last seen; not reacquired in the window
- A320 [on ground] `AC-669860`: last position 48 s old when last seen; not reacquired in the window
- B39M [on ground] `AC-B67C1A`: last position 61 s old when last seen; not reacquired in the window
- B737 `AC-6A5F5B`: last position 48 s old when last seen; not reacquired in the window
- B737 [on ground] `AC-3C9E5E`: last position 53 s old when last seen; not reacquired in the window
- E75L [on ground] `AC-8EF0D5`: last position 52 s old when last seen; not reacquired in the window
- A320 [on ground] `AC-6538C6`: last position 54 s old when last seen; not reacquired in the window
- C25B [on ground] `AC-0E7B8D`: last position 50 s old when last seen; not reacquired in the window
- LJ31 `AC-09D346`: last position 57 s old when last seen; not reacquired in the window
- H25B [on ground] `AC-A23249`: last position 48 s old when last seen; not reacquired in the window
- A333 [on ground] `AC-123F64`: last position 48 s old when last seen; not reacquired in the window
- P32R `AC-083C75`: last position 47 s old when last seen; not reacquired in the window
- EC35 `AC-F0668D`: last position 55 s old when last seen; not reacquired in the window
- C700 `AC-53E74B`: last position 45 s old when last seen; not reacquired in the window
- B788 `AC-279F8D`: last position 49 s old when last seen; not reacquired in the window
- B764 [on ground] `AC-3D4F93`: last position 53 s old when last seen; not reacquired in the window
- B58T `AC-92BD77`: last position 52 s old when last seen; not reacquired in the window
- CRJ9 [on ground] `AC-AE2410`: last position 58 s old when last seen; not reacquired in the window
- B738 `AC-7173E8`: last position 60 s old when last seen; not reacquired in the window
- F900 [on ground] `AC-AC31A3`: last position 55 s old when last seen; not reacquired in the window
- B738 [on ground] `AC-B260DA`: last position 55 s old when last seen; not reacquired in the window
- E170 [on ground] `AC-A64A33`: last position 54 s old when last seen; not reacquired in the window
- B788 `AC-7A200D`: last position 52 s old when last seen; not reacquired in the window
- B788 [on ground] `AC-313A8F`: last position 59 s old when last seen; not reacquired in the window
- BE36 `AC-20DDE3`: last position 47 s old when last seen; not reacquired in the window
- B38M `AC-9A93FB`: last position 60 s old when last seen; not reacquired in the window
- BE95 [on ground] `AC-D7A934`: last position 54 s old when last seen; not reacquired in the window
- B38M [on ground] `AC-9FAEC6`: last position 47 s old when last seen; not reacquired in the window
- B738 `AC-31EC9D`: last position 49 s old when last seen; not reacquired in the window
- B38M [on ground] `AC-DC1743`: last position 51 s old when last seen; not reacquired in the window
- B38M [on ground] `AC-1D8EE6`: last position 46 s old when last seen; not reacquired in the window
- B38M [on ground] `AC-F1A53B`: last position 59 s old when last seen; not reacquired in the window
- A319 `AC-7DA1A3`: last position 52 s old when last seen; not reacquired in the window
- E145 `AC-78EC55`: last position 60 s old when last seen; not reacquired in the window
- B738 [on ground] `AC-A9EC53`: last position 54 s old when last seen; not reacquired in the window
- CRJ9 [on ground] `AC-C3ACFF`: last position 58 s old when last seen; not reacquired in the window
- CRJ9 [on ground] `AC-8A1682`: last position 57 s old when last seen; not reacquired in the window
- B739 [on ground] `AC-438EA6`: last position 56 s old when last seen; not reacquired in the window
- B407 `AC-C7A4E3`: last position 58 s old when last seen; not reacquired in the window
- B429 `AC-7A295D`: last position 46 s old when last seen; not reacquired in the window
- CRJ9 [on ground] `AC-EF3924`: last position 52 s old when last seen; not reacquired in the window
- CRJ9 [on ground] `AC-CF2FF0`: last position 54 s old when last seen; not reacquired in the window
- B737 [on ground] `AC-676D19`: last position 50 s old when last seen; not reacquired in the window
- B738 [on ground] `AC-F48FE9`: last position 47 s old when last seen; not reacquired in the window
- G2CA `AC-C106AC`: last position 53 s old when last seen; not reacquired in the window
- C208 `AC-8865F3`: last position 59 s old when last seen; not reacquired in the window
- C182 `AC-64183F`: last position 48 s old when last seen; not reacquired in the window
- AS65 `AC-FCCC83`: last position 53 s old when last seen; not reacquired in the window
- E545 [on ground] `AC-E8B4F8`: last position 55 s old when last seen; not reacquired in the window
- DH8D [on ground] `AC-25DC57`: last position 49 s old when last seen; not reacquired in the window
- B763 [on ground] `AC-00EDA9`: last position 48 s old when last seen; not reacquired in the window

## Informational: pre-DO-260B transmitters

- CRJ7 [on ground] `AC-5F6732`: ADS-B version 0 (pre-DO-260B): quality indicators not evaluated
- CRJ7 [on ground] `AC-8BA49F`: ADS-B version 0 (pre-DO-260B): quality indicators not evaluated
- C208 [on ground] `AC-CFF4AD`: ADS-B version 0 (pre-DO-260B): quality indicators not evaluated
- E75L [on ground] `AC-8EF0D5`: ADS-B version 0 (pre-DO-260B): quality indicators not evaluated
