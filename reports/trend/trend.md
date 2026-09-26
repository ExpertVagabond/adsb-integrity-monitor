# ADS-B Integrity Trend

3 captures, 1,511 aircraft evaluations, re-analyzed with the current rules. High-confidence failures: 3 (2.0 per 1,000 aircraft).

| Capture start (UTC) | Minutes | Area | Aircraft | Pass | High-confidence fails | ...in rule airspace | Low-confidence fails | Not evaluable | ADS-R | Interference clusters | Altitude outliers |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-25 13:55 | 5 | not recorded | 96 | 95.83% | 1 | 0 | 0 | 1 | 2 | 0 | 1 |
| 2026-09-25 16:49 | 60 | not recorded | 812 | 98.65% | 2 | 1 | 3 | 4 | 8 | 0 | 0 |
| 2026-09-25 17:53 | 30 | not recorded | 603 | 98.34% | 0 | 0 | 1 | 5 | 4 | 0 | 3 |

## Aircraft with a high-confidence failure

A failure that repeats across captures is stronger evidence than a single sighting.

| Aircraft | Type | Captures seen | Failed (high confidence) | Indicators | History |
|---|---|---|---|---|---|
| `AC-293978` | C210 | 1 | 1 | nac_p, sil | acy-2026-09-25.jsonl: fail (high confidence) |
| `AC-E4D49F` | C182 | 1 | 1 | nac_p, sil | nyphl-100nm-1h.jsonl.gz: fail (high confidence) |
| `AC-3BEB9D` | CL30 | 1 | 1 | nac_v | nyphl-100nm-1h.jsonl.gz: fail (high confidence) |

## Aircraft flagged by the altitude check

The altitude threshold stays fixed; a borderline flag that never repeats is expected noise. One that repeats across captures points to a real altimetry or GNSS-altitude problem.

| Aircraft | Type | Captures seen | Flagged | History |
|---|---|---|---|---|
| `AC-82CEE0` | GLF5 | 2 | 1 | nyphl-100nm-1h.jsonl.gz: seen, not flagged; capture-2026-09-25.jsonl.gz: altitude outlier |
| `AC-CE4E24` | CL30 | 2 | 1 | nyphl-100nm-1h.jsonl.gz: seen, not flagged; capture-2026-09-25.jsonl.gz: altitude outlier |
| `AC-293978` | C210 | 1 | 1 | acy-2026-09-25.jsonl: altitude outlier |
| `AC-89101E` | BE55 | 1 | 1 | capture-2026-09-25.jsonl.gz: altitude outlier |

> Source data is crowdsourced ADS-B from adsb.lol volunteer receivers. Results describe what public receivers decoded during the capture window. They are not an FAA compliance determination, and a single missing or degraded report can have many causes.
