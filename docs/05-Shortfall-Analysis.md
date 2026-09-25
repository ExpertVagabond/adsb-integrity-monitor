# Shortfall Analysis: ADS-B Out Performance in the New York–Philadelphia–Atlantic City Area

| | |
|---|---|
| Document | Shortfall Analysis, v0.2 |
| Date | 2026-09-25 |
| Author | Matthew Karsten |
| Data | 240 snapshots at 15 s, 16:49–17:49 UTC, 100 NM around Atlantic City International (ACY): [capture](../captures/nyphl-100nm-1h.jsonl.gz), [report](../reports/nyphl-100nm-1h/report.md), [CSV](../reports/nyphl-100nm-1h/results.csv) |
| Status | Draft. One hour of data; findings are screening results, not compliance determinations |

## 1. Purpose

Measure the gap between the ADS-B Out performance the regulations require and the performance actually observed
in one of the busiest terminal areas in the NAS. Then separate genuine equipment problems from artifacts of how
the data was collected, and recommend proportionate next steps.

## 2. Required capability

| Requirement | Source |
|---|---|
| NACp ≥ 8 (position accuracy better than 0.05 NM) | 14 CFR 91.227(c)(1)(i) |
| NACv ≥ 1 (velocity accuracy better than 10 m/s) | 91.227(c)(1)(ii) |
| NIC ≥ 7 (containment radius under 0.2 NM) | 91.227(c)(1)(iii) |
| SDA ≥ 2 (design assurance 1e-5 per flight hour or better) | 91.227(c)(1)(iv) |
| SIL = 3 (source integrity 1e-7 or better) | 91.227(c)(1)(v) |
| These bind aircraft in Class B/C, within 30 NM of Appendix D airports (JFK, LGA, EWR, PHL here) below 10,000 ft, above Class B/C ceilings up to 10,000 ft, and at or above 10,000 ft MSL | 91.225(d) |

## 3. Method

Captured public ADS-B from adsb.lol and evaluated every aircraft against the requirements above, using the
controls developed while building the tool (each is a tested requirement):

- Each indicator and the ADS-B version is judged by its **most frequent value** over the hour, not the last poll
  (SYS-017, SYS-019). Failures that rest on a value that flipped between passing and failing are marked **low
  confidence**.
- **Excluded from judgment:** ADS-R NACv and NIC, which UAT-to-1090 converters fill with defaults (SYS-021);
  pre-DO-260B transmitters (SYS-017); airport surface vehicles (SYS-018); MLAT, TIS-B and Mode S-only targets
  (SYS-010).
- **Rule applicability** from FAA airspace data, stated for every finding (SYS-036).
- **Independent checks:** altitude consistency against neighbors (SYS-033) and against a weather model (SYS-035);
  GNSS interference screen (SYS-034); FAA registry for year and certification basis (SYS-037).

## 4. Observed capability

| | Aircraft |
|---|---|
| Evaluated (direct ADS-B and ADS-R) | **812** (median 70 of 240 polls each) |
| Seen in 91.225(d) rule airspace at some point | **765** (94%) |
| Meet all five minimums | **801** (98.6%) |
| Below at least one minimum | **5** |
| No failures, but an indicator never reported | 2 |
| Not evaluable (genuinely pre-DO-260B) | 4 |
| Excluded non-aircraft and non-ADS-B targets | 37 |

**Where the five fall:**

| Aircraft (pseudonym) | Class | Source | Indicators below minimum | Confidence | Rule airspace? |
|---|---|---|---|---|---|
| CL30 `AC-3BEB9D` | A2, built 2007 | direct 1090ES | NACv = 0 | **High**: steady over 112 polls | **Yes**, (d)(4) above 10,000 ft |
| C172 `AC-5B65DF` | A1, built 2008 | ADS-R | NACp = 0, SIL = 0 | Low: both values flipped | Yes, (d)(1) |
| B39M `AC-D773E1` | A3, registered experimental (consistent with a manufacturer test aircraft) | direct 1090ES | SIL = 2 | Low: flipped | Yes, (d)(2), on the ground |
| C182 `AC-E4D49F` | A1, built 2001 | ADS-R | NACp = 0, SIL = 2 | High: steady | No; on the ground outside rule airspace |
| unknown type `AC-F235DF` | A1, built 2025 | direct 1090ES | NACp = 0, NIC = 0 | Low for NACp | No; on the ground outside rule airspace |

**By class:** 0 of 469 large and heavy aircraft (A3–A5) failed with high confidence; the one A3 failure is the
low-confidence test aircraft. Light aircraft (A1) carry 3 of the 5 failures (2.6% of 115).

**Independent checks all came back clean:**

- Weather model vs aircraft altitude trend: median disagreement **37 ft** across 9 pressure levels.
- Altitude consistency: **0** of 433 assessed aircraft off their neighbors by more than 200 ft (60 at the edges of
  the traffic not assessed).
- GNSS interference: 23 brief drops by 7 normally-healthy aircraft, **no clusters**.
- Emergencies: none.

## 5. The shortfall

**Inside the airspace where the rule applies, the observed shortfall is one aircraft out of 765 (0.13%) at high
confidence:** a business jet broadcasting NACv 0 steadily at altitude. A NACv of 0 means "velocity accuracy
unknown or worse than 10 m/s". Every other value from that aircraft was healthy, which points to a configuration
or source-wiring issue for velocity rather than a failed GPS.

Two more rule-airspace failures exist at **low confidence** (values flipping), and two further aircraft fell short
only while on the ground outside rule airspace.

The more important result is what the shortfall is **not**. A naive pass over the same hour, using each
aircraft's last-poll values and no ADS-R exclusion, reports **13** aircraft below a minimum and sets aside **36**
as not evaluable. With the controls, **5** fall below a minimum, **4** are not evaluable, and **1** fails with high
confidence inside rule airspace.

Every difference traces to the measurement chain, not the aircraft:
- converter defaults on ADS-R;
- transient version-0 readings on airliners that report version 2 most of the time;
- values that flip between messages.

Earlier captures showed the same pattern: ADS-R failing at 100%, a 747 "failing" SIL, and 69 false dropouts from
one slow poll. **In public ADS-B data, the measurement shortfall is larger than the equipment shortfall.**

## 6. Root-cause hypotheses

| # | Hypothesis | Evidence | How to confirm |
|---|---|---|---|
| H1 | The CL30's velocity source isn't feeding NACv to the transponder, or it's configured to report 0 | NACv 0 steady for 112 polls while NACp 9, NIC 8, SIL 3 and SDA 2 are healthy | Owner-requested PAPR for that flight; an avionics shop's ramp test |
| H2 | Steady NACp/SIL zeros on light aircraft are unconnected or uncertified position sources | C182 steady NACp 0 / SIL 2; the morning capture's C210 steady NACp 0 / SIL 0 | PAPR; installation records |
| H3 | Flip-flopping values on ground aircraft are avionics acquiring GPS, or mixed-source aggregation | Zeros at the gate; alternation stops once airborne | Own receiver near an airport; compare raw messages |
| H4 | Transient version-0 readings come from aggregation or decoding, not the transmitter | 34 of 36 "version 0" aircraft reported version 2 in most polls | Own receiver: check the raw operational-status messages |

## 7. Alternatives

| Alt | Description | Cost | Benefit | Risk |
|---|---|---|---|---|
| A0 | Do nothing; rely on FAA monitoring and PAPR | None | FAA already monitors authoritatively | Public data's value as an early screen is unused |
| A1 | Owner outreach for high-confidence findings in rule airspace only, pointing owners to the free PAPR | Low | Targets the one credible case; PAPR confirms or clears it | Low; the confidence and applicability filters keep false accusations out |
| A2 | Continuous screening with this tool (the daily capture workflow), trending results over weeks | Free (GitHub runners) | Turns a one-hour snapshot into a baseline; resolves H3, H4 and VG-5 over time | Must stay a screen, never an enforcement input (Safety Risk Assessment HZ-6) |
| A3 | Validate the measurement chain with our own 1090 MHz and 978 MHz receivers | About $60–80 in hardware | Closes the biggest open question: which zeros are real | Coverage limited to one receiver site |

## 8. Recommendation

1. **A2 now:** keep the daily capture running for at least four weeks before drawing trend conclusions. One hour
   is a snapshot.
2. **A3 next:** buy the two receivers. Most of what this analysis couldn't settle (H3, H4, the ADS-R question,
   VG-5) comes down to seeing raw messages.
3. **A1 only for high-confidence, rule-airspace findings,** and only as a pointer to the FAA's own PAPR, never as
   a finding in itself.

## 9. Limitations

- One hour, one afternoon, one region. Crowdsourced receivers miss low-altitude traffic away from cities.
- Barometric altitude stands in for MSL when judging rule airspace.
- Broadcast latency (91.227(c)(2)–(3)) and the full message set (d) aren't checked.
- No per-aircraft ground truth yet (Verification Plan VG-1).
