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
| Report | `aim/report.py` | Merge snapshots, run checks, write Markdown and CSV | SYS-040 to SYS-042 |
| Traceability | `aim/rtm.py` | Build docs/RTM.md from requirement IDs and test tags; fail on gaps | SYS-050 |
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
| `alt_baro` | int or `"ground"` | barometric altitude; `"ground"` when on the surface | report label |
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

### ICD-2: capture file (internal)

JSON Lines, one object per poll: `{"polled_at": <epoch s>, "feed_time": <epoch s>, "ac": [<ICD-1 objects>]}`.
Append-only, so an interrupted capture keeps everything recorded so far.

### ICD-3: outputs (internal, outbound)

- `report.md`: summary tables, failures with paragraph citations, emergencies, continuity findings, disclaimer.
- `results.csv`: one row per evaluated aircraft with the five indicator values, verdict, failed paragraphs,
  emergency and continuity notes. Opens directly in Excel.

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
