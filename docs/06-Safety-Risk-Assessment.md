# Safety Risk Assessment: ADS-B Integrity Monitor

| | |
|---|---|
| Document | Safety Risk Assessment, v0.2 |
| Date | 2026-09-25 |
| Author | Matthew Karsten |
| Method | Adapted from the FAA Safety Risk Management steps: describe the system, identify hazards, analyze and assess risk, control it, track residual risk |

## 1. System description and boundary

AIM reads public, crowdsourced ADS-B data and produces reports and live alerts. It is **not** part of the
National Airspace System, is not used for separation or any air traffic service, and has no path to an aircraft
or a controller. Its hazards are therefore not direct flight hazards. They come from people acting on its output:
trusting a wrong finding, missing a real one, or exposing someone's data.

## 2. Severity and likelihood scales

| Severity | Meaning here |
|---|---|
| Minor | Wasted analyst time; a finding has to be re-checked |
| Moderate | A specific owner or operator is wrongly suspected, or a real problem goes unreported for a while |
| Major | Public, lasting harm to a named individual, or reliance on AIM in place of an authoritative source |

| Likelihood | Meaning here |
|---|---|
| Remote | Needs several independent failures or deliberate misuse |
| Occasional | Expected in some captures |
| Frequent | Expected in most captures without the control |

Risk is **Low** (acceptable), **Medium** (acceptable with controls tracked), or **High** (not acceptable).

## 3. Hazards

| ID | Hazard | Causes | Effect | Controls (requirement) | Residual |
|---|---|---|---|---|---|
| HZ-1 | **False failure:** aircraft reported below a minimum when its equipment is fine | Converter default values on ADS-R (NACv, NIC); decoder-synthesized values on pre-DO-260B transmitters; values flip-flopping between messages; single-poll glitches | An owner is wrongly suspected (Moderate) | ADS-R NACv/NIC excluded (SYS-021); pre-DO-260B not evaluable (SYS-017); majority value plus low-confidence marking (SYS-019); missing ≠ failed (SYS-016); redaction (SYS-043) | **Low**: Remote × Moderate |
| HZ-2 | **Missed failure:** degraded equipment not reported | Receivers miss the status messages; intermittent faults masked by the majority rule; aircraft outside coverage | A real problem goes unreported (Moderate) | "Not reported" and "incomplete" kept visible (SYS-016); unstable indicators listed (SYS-019); TRANSIENT events in watch mode (SYS-048). AIM supplements, and never replaces, FAA monitoring and PAPR | **Medium**: Occasional × Moderate; tracked |
| HZ-3 | **Missed GNSS interference** | Screen thresholds (3 aircraft, 30 NM, same poll); sparse coverage; interference weaker than the NACp/NIC minimums | No early indication of a jamming event (Moderate) | Documented as a screen, not a detector (SYS-034); parameters exposed; FAA and pilot reports remain the primary channel | **Medium**: tracked |
| HZ-4 | **False interference alarm** | Gate power-up zeros; ADS-R converter NIC 0; clustered equipment faults | Needless alarm and escalation (Minor) | Airborne only; ADS-R excluded; normally-healthy aircraft only (SYS-034, SYS-021) | **Low** |
| HZ-5 | **Privacy harm:** a named aircraft publicly tied to a failed minimum | Publishing unredacted reports | Public, lasting harm to an individual (Major) | Redaction mode with stable pseudonyms (SYS-043); all published samples redacted; the internal key never written to outputs | **Low**: Remote × Major, with redaction the default for anything published |
| HZ-6 | **Misuse as a compliance determination** | Reading "below minimum" as "violation" | Wrongful accusation, or reliance in place of PAPR (Major) | Disclaimer in every report (SYS-042); rule applicability stated next to each finding (SYS-036); the wording never says "non-compliant"; the README points owners to PAPR | **Low** |
| HZ-7 | **Emergency not alerted in time** | 15 s polling; aggregator delay; outages | A watcher learns of an emergency late (Moderate) | Emergency alerts fire at once, with no confirmation delay (SYS-046); AIM is documented as non-operational | **Low** for its intended, non-operational use |
| HZ-8 | **Silent data failure:** API shape changes or empty feed | Upstream change; outage | Reports show fewer aircraft or nothing, and look healthy (Moderate) | Failed polls logged (SYS-004); retry with backoff (SYS-006); feed-health warning when the aircraft count collapses (SYS-007); ICD lists every field depended on; live test (SYS-001) | **Low** (was Medium; closed by OI-1) |
| HZ-9 | **Burden on a free public service** | Aggressive polling | Service degraded for others (Minor) | 5 s minimum interval (SYS-003); backoff honoring Retry-After (SYS-006) | **Low** |

## 4. Open items

| ID | Item | Plan |
|---|---|---|
| OI-1 | No alert when the feed returns zero aircraft or loses most of them between polls (HZ-8) | **Closed 2026-09-25:** feed-health warning added (SYS-007), with tests |
| OI-2 | No independent ground truth for per-aircraft findings (HZ-1, HZ-2) | Validate against a 978 MHz / 1090 MHz receiver of our own, or an owner-requested PAPR. See the Verification Plan |
| OI-3 | Interference screen sensitivity unknown (HZ-3) | Replay a documented interference event if a public capture of one becomes available |

## 5. Conclusion

With the listed controls, no hazard is rated High. Two are Medium and tracked (HZ-2, HZ-3); HZ-8 was Medium until this assessment produced SYS-007. The largest
residual risk is not a software fault but misuse. That's why redaction, the disclaimer and rule-applicability
labeling are requirements with tests, not documentation notes.
