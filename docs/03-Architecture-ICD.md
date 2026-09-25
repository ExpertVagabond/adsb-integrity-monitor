# Architecture and Interface Control: ADS-B Integrity Monitor

## 1. Context

```
 aircraft ──1090ES / UAT──► volunteer receivers ──► adsb.lol aggregator ──HTTPS/JSON (ICD-1)──► AIM
                                                                                              │
                                              captures/*.jsonl (ICD-2) ◄── collect ◄──────────┘
                                                     │
                                                     └──► analyze ──► reports/report.md, results.csv (ICD-3)
```

AIM never talks to aircraft or receivers. It consumes an aggregated public feed, which puts it downstream of
two independent failure points (receiver coverage and the aggregator). That's why reports are framed as
observations, not determinations (ConOps §5).

## 2. Components

| Component | Module | Responsibility | Requirements |
|---|---|---|---|
| Feed ingest | `aim/feed.py` | Poll the API, rate-limit, write snapshots, survive failed polls | SYS-001 to SYS-004 |
| Rules | `aim/rules.py` | 91.227(c)(1) indicator checks, report-type and surface-vehicle filters, pre-DO-260B handling, emergency codes | SYS-010 to SYS-020 |
| Tracks | `aim/tracks.py` | Rebuild per-aircraft position history; flag dropouts and jumps; separate lost tracks | SYS-030 to SYS-032 |
| Altitude | `aim/altitude.py` | Theil-Sen trend of geometric-minus-barometric altitude; flag outliers | SYS-033 |
| Interference screen | `aim/interference.py` | Same-poll, same-area integrity drops by normally healthy aircraft | SYS-034 |
| Watch | `aim/watch.py` | Live polling with per-aircraft state; alerts on emergencies and confirmed integrity changes | SYS-046 to SYS-048 |
| Rule airspace | `aim/airspace.py` | FAA Class B/C boundaries and Appendix D veils; which 91.225(d) paragraph applied to each aircraft | SYS-036 |
| Weather check | `aim/weather.py` | Compare the altitude trend with Open-Meteo pressure-level heights | SYS-035 |
| Registry | `aim/registry.py` | FAA registry to year built and certification basis (no owner data) | SYS-037 |
| Statistics | `aim/stats.py` | Results by emitter category, altitude band, ADS-B version, aircraft type | SYS-044 |
| Report | `aim/report.py` | Merge snapshots, run checks, write Markdown and CSV, redaction | SYS-040 to SYS-043 |
| HTML report | `aim/htmlreport.py` | Self-contained page with SVG track map colored by verdict | SYS-045 |
| Traceability | `aim/rtm.py` | Build docs/RTM.md from requirement IDs and test tags; fail on gaps | SYS-050 |
| CI | `.github/workflows/ci.yml` | Tests + traceability gate on Python 3.10/3.12/3.13 for every push | SYS-051 |
| CLI | `aim/__main__.py` | `collect`, `analyze`, `rtm` commands | all |

## 3. Interfaces

### ICD-1: adsb.lol v2 point query (external, inbound)

`GET https://api.adsb.lol/v2/point/{lat}/{lon}/{radius_nm}` returns JSON with `now` (epoch ms) and `ac` (array).
AIM depends only on the fields below. Any other field is ignored.

| Field | Type | Meaning | Used for |
|---|---|---|---|
| `hex` | string | ICAO 24-bit address | aircraft key |
| `type` | string | report source: `adsb_icao`, `adsr_icao`, `mlat`, `tisb_*`, `mode_s`, ... | SYS-010 filter |
| `category` | string | emitter category (A1 to A7 aircraft, C1 to C3 surface vehicles and obstacles) | SYS-018 filter |
| `alt_baro` | int or `"ground"` | barometric altitude (ft); `"ground"` when on the surface | SYS-033, SYS-044, label |
| `alt_geom` | int | geometric (GNSS) altitude (ft) | SYS-033 |
| `version` | int | ADS-B version (2 = DO-260B) | SYS-017 |
| `nac_p`, `nac_v`, `nic`, `sda`, `sil` | int | 91.227(c)(1) quality indicators (DO-260B category codes) | SYS-011 to SYS-015 |
| `squawk` | string | Mode A code | SYS-020 |
| `emergency` | string | emergency/priority status (`none`, `general`, `lifeguard`, `minfuel`, `nordo`, `unlawful`, `downed`) | SYS-020 |
| `lat`, `lon` | float | last position | SYS-030, SYS-031 |
| `seen_pos` | float | seconds since that position was received | fix time = `now - seen_pos` |
| `flight`, `r`, `t` | string | callsign, registration, type code (`SERV` = service vehicle) | labels; SYS-018 |

Indicator thresholds (from DO-260B category tables):

| Indicator | 91.227(c)(1) bound | Minimum code |
|---|---|---|
| NACp | EPU < 0.05 NM | 8 (EPU < 92.6 m) |
| NACv | < 10 m/s | 1 |
| NIC | Rc < 0.2 NM | 7 (Rc < 370.4 m) |
| SDA | ≤ 1e-5 per flight hour | 2 |
| SIL | ≤ 1e-7 | 3 |

### ICD-4: Open-Meteo forecast API (external, inbound, optional)

`GET https://api.open-meteo.com/v1/forecast?latitude&longitude&hourly=geopotential_height_{925..200}hPa&start_date&end_date&timezone=UTC`.
Free, no key. AIM reads only the hourly geopotential heights (m) for the hour nearest the capture midpoint.

### ICD-5: FAA ADDS open data (external, inbound, fetched once and committed)

ArcGIS REST, free, no key, `https://services6.arcgis.com/ssFJjBXIUyZDrSYZ/arcgis/rest/services/`:
`Class_Airspace/FeatureServer/0/query` (fields IDENT, NAME, CLASS, LOWER_VAL/UOM/CODE, UPPER_VAL/UOM/CODE, polygon
rings) filtered to CLASS B and C in the capture's bounding box, and `US_Airport/FeatureServer/0/query` for the
37 Appendix D Section 1 airports. Stored as `data/airspace-nyphl.json` so analysis is reproducible offline.

### ICD-6: FAA aircraft registry (external, inbound, local only)

`https://registry.faa.gov/database/ReleasableAircraft.zip` (about 73 MB; the server requires a browser-style
`Accept` header). AIM reads MASTER.txt columns MODE S CODE HEX, YEAR MFR and MFR MDL CODE, joined to ACFTREF.txt
MFR, MODEL and BUILD-CERT-IND. Owner fields are never extracted, and the lookup is git-ignored.

### ICD-2: capture file (internal)

JSON Lines, one object per poll: `{"polled_at": <epoch s>, "feed_time": <epoch s>, "ac": [<ICD-1 objects>]}`.
Append-only, so an interrupted capture keeps everything recorded so far. Stored captures may be gzip-compressed
(`.jsonl.gz`, SYS-005); a 1-hour, 100 NM capture shrinks by roughly 10x.

### ICD-3: outputs (internal, outbound)

- `report.md`: summary tables, failures with paragraph citations, emergencies, continuity findings, disclaimer.
- `results.csv`: one row per evaluated aircraft with the five indicator values, verdict, failed paragraphs,
  emergency, continuity, altitude, category, altitude band, unstable indicators and the number of polls the aircraft
  was seen in (brief sightings deserve less weight). Opens directly in Excel.
- `report.html`: the same findings plus a track map, in one offline file with no external resources.

## 4. Design decisions

| Decision | Rationale |
|---|---|
| Python standard library only (SYS-060) | Installs anywhere, including locked-down government workstations, with nothing to vet. |
| Store raw snapshots, analyze later | Findings are reproducible. A rule change can be re-run against old captures. |
| Missing indicator ≠ failure (SYS-016) | Public receivers miss messages. Treating absence as failure would overstate problems. |
| Pre-DO-260B transmitters not evaluated (SYS-017) | Version 0/1 transmitters don't broadcast NIC/NACp/SIL as DO-260B defines them; decoders synthesize values. The first live capture had a 747 "failing" SIL on a synthesized number. |
| Surface vehicles excluded (SYS-018) | The first live capture scored two airport service vehicles against an aircraft rule. |
| Lost tracks ≠ dropouts (SYS-032) | Most stale-and-gone tracks in the first capture were aircraft landing at PHL and ACY. Calling a landing a dropout would bury the real ones. |
| Latest value per field wins | Indicators come from different ADS-B message types, so one snapshot rarely holds all five. |
| Dropouts judged by the feed's own `seen_pos` clock (SYS-030) | The first version compared fix times across polls. On the first live capture, one slow poll (20.5 s instead of 10 s) produced 69 false dropouts. `seen_pos` measures reception, not our polling. |
| Altitude check: global trend, then local neighbors (SYS-033) | The geometric-minus-barometric difference rose about 45 ft per 1,000 ft on the capture day. A straight-line fit alone flagged two unrelated aircraft at 37,000 ft by the same +210 ft (model curvature). Comparing each aircraft's remainder with its neighbors' brought p99 to 134 to 144 ft. An E55P at 41,000 ft, the top of the traffic, still came out -222 ft because all its neighbors were below it, so aircraft are now assessed only when neighbors bracket them; p99 fell to 111 ft and the only aircraft above 200 ft is the one also broadcasting integrity zeros. |
| Altitude bands use highest altitude seen (SYS-044) | An aircraft that landed during the window would otherwise be counted as a surface target. |
