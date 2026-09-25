# Trade Study: ADS-B Data Source

| | |
|---|---|
| Decision | Primary data source for AIM v0.1 |
| Date | 2026-09-25 |
| Result | **adsb.lol v2 API selected.** Own receiver recommended as a v0.2 cross-check; FAA SWIM to be evaluated once an account is approved. |

## 1. Need

AIM must compare each aircraft's NACp, NACv, NIC, SDA and SIL against 14 CFR 91.227(c)(1). A source that doesn't
carry those five indicators can't perform the core function, whatever its other strengths.

## 2. Alternatives

| ID | Source | How evaluated (2026-09-25) |
|---|---|---|
| A | adsb.lol v2 API | Live calls: HTTP 200 on 3 of 3, 0.67 to 1.71 s. 56 aircraft within 40 NM of PHL and 90 within 60 NM of ACY, each with `nac_p`, `nac_v`, `nic`, `sda`, `sil`. |
| B | OpenSky Network REST API (anonymous) | Live call: HTTP 200, 0.73 s, 97 aircraft in a box around ACY. Each state vector has 18 fields, none of them integrity indicators. |
| C | airplanes.live API | Live calls: HTTP 403 twice. The response asks developers to email for access. |
| D | FAA SWIM Cloud Distribution Service (SCDS) | Not evaluated hands-on; needs an approved SCDS account. |
| E | Own receiver (RTL-SDR dongle + readsb decoder) | Not built. readsb decodes all five indicators from raw 1090 MHz messages. |

## 3. Criteria and weights

| # | Criterion | Weight | Why |
|---|---|---|---|
| 1 | Carries all five 91.227(c)(1) indicators | 35% | Core function; without it AIM can't check the rule. |
| 2 | Access without approval or purchase | 20% | Anyone reviewing this work should be able to rerun it today. |
| 3 | Coverage of a terminal area | 15% | Enough aircraft in one capture to say something. |
| 4 | Authority / provenance | 15% | How much weight a finding can bear. |
| 5 | License clarity | 15% | Captures are committed to a public repo. |

## 4. Scores (1 = poor, 5 = excellent; blank = not verifiable yet)

| Criterion | A adsb.lol | B OpenSky | C airplanes.live | D SWIM SCDS | E Own receiver |
|---|---|---|---|---|---|
| 1 Indicators (35%) | 5 | 1 | | | 5 |
| 2 Access (20%) | 5 | 4 | 1 | 2 | 3 |
| 3 Coverage (15%) | 4 | 4 | | 5 | 2 |
| 4 Authority (15%) | 2 | 2 | 2 | 5 | 3 |
| 5 License (15%) | 5 (ODbL 1.0) | 3 (research terms) | 2 (by request) | | 5 (own data) |
| **Weighted** | **4.40** | **2.50** | not scored | not scored | **3.85** |

C and D are not scored: the criteria that matter most can't be verified without access, and inventing scores for
them would make the table look more certain than it is.

## 5. Result and rationale

**A (adsb.lol)** is selected. It's the only source verified today that carries all five indicators with no
approval step, and its ODbL license permits publishing captures with attribution.

**B (OpenSky)** is rejected as a primary source because it can't perform the core function, but it remains useful
for position cross-checks.

**E (own receiver)** is the strongest alternative. It trades coverage for first-hand data and removes the
aggregator as a failure point. Recommended for v0.2 as an independent cross-check near a single airport.

**D (SWIM)** is the authoritative option and the right long-term comparison. It requires an SCDS account, and its
products need to be checked for which quality indicators they carry before it can be scored.

## 6. Risks with the selected source

| Risk | Mitigation |
|---|---|
| Volunteer coverage gaps show up as dropouts | Findings are framed as observations (SYS-042); dropouts use the feed's own staleness clock (SYS-030). |
| API changes shape without notice | ICD-1 lists every field AIM depends on; the live test (`AIM_LIVE=1`) checks those fields still exist. |
| Rate limiting or service outage | Polls no faster than every 5 s (SYS-003); a failed poll doesn't end the capture (SYS-004). |
