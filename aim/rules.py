"""14 CFR 91.227 checks on a single aircraft report.

Regulatory text (eCFR, retrieved 2026-09-25):
  (c)(1)(i)   NACp must be less than 0.05 nautical miles
  (c)(1)(ii)  NACv must be less than 10 meters per second
  (c)(1)(iii) NIC must be less than 0.2 nautical miles
  (c)(1)(iv)  SDA must be less than or equal to 1e-5 per flight hour
  (c)(1)(v)   SIL must be less than or equal to 1e-7 per flight hour or per sample
  (d)(9)      indication if the flightcrew has identified an emergency,
              radio communication failure, or unlawful interference

The DO-260B category codes that satisfy each bound are the thresholds below.
"""

# Report types we evaluate (SYS-010). Everything else is excluded and counted.
#   adsb_icao  = direct 1090ES ADS-B from a transponder with an ICAO address
#   adsr_icao  = ADS-R rebroadcast (usually a UAT aircraft seen on 1090)
EVALUATED_TYPES = ("adsb_icao", "adsr_icao")

# SYS-018: airport surface vehicles broadcast ADS-B too, but 91.227 applies to aircraft.
# Emitter categories C1-C3 are surface emergency vehicles, surface service vehicles and obstacles;
# "SERV" is the type code aggregators assign to service vehicles that don't send a category.
SURFACE_CATEGORIES = ("C1", "C2", "C3")
SURFACE_TYPE_CODES = ("SERV",)

# field, minimum category code, regulation paragraph, plain-English bound
PERFORMANCE_CHECKS = (
    ("nac_p", 8, "91.227(c)(1)(i)", "NACp < 0.05 NM (NACp >= 8)"),     # SYS-011
    ("nac_v", 1, "91.227(c)(1)(ii)", "NACv < 10 m/s (NACv >= 1)"),     # SYS-012
    ("nic", 7, "91.227(c)(1)(iii)", "NIC < 0.2 NM (NIC >= 7)"),        # SYS-013
    ("sda", 2, "91.227(c)(1)(iv)", "SDA <= 1e-5/flight hour (SDA >= 2)"),  # SYS-014
    ("sil", 3, "91.227(c)(1)(v)", "SIL <= 1e-7 (SIL = 3)"),            # SYS-015
)

# SYS-020: Mode A codes with a fixed emergency meaning, and the feed's emergency field values.
EMERGENCY_SQUAWKS = {
    "7500": "unlawful interference",
    "7600": "radio communication failure",
    "7700": "general emergency",
}

PASS, FAIL, NOT_REPORTED = "pass", "fail", "not reported"


def is_evaluated(ac):
    return ac.get("type") in EVALUATED_TYPES


def is_surface_vehicle(ac):
    """SYS-018."""
    return ac.get("category") in SURFACE_CATEGORIES or ac.get("t") in SURFACE_TYPE_CODES


def is_pre_do260b(ac):
    """SYS-017: version 0/1 transmitters predate the NIC/NACp/SIL definitions in DO-260B.

    Decoders synthesize those values from older fields, so comparing them to 91.227(c)(1)
    would judge an aircraft on numbers it never actually broadcast.
    """
    version = ac.get("version")
    return isinstance(version, int) and version < 2


def check_performance(ac):
    """Return one result per 91.227(c)(1) indicator.

    A missing indicator is NOT_REPORTED, never FAIL (SYS-016): public receivers
    don't always decode the message that carries it.
    """
    results = []
    for field, minimum, para, bound in PERFORMANCE_CHECKS:
        value = ac.get(field)
        if not isinstance(value, int):
            status = NOT_REPORTED
        else:
            status = PASS if value >= minimum else FAIL
        results.append({"field": field, "value": value, "status": status, "para": para, "bound": bound})
    return results


def check_version(ac):
    """SYS-017: describe a pre-DO-260B transmitter, else None."""
    if is_pre_do260b(ac):
        return f"ADS-B version {ac['version']} (pre-DO-260B): quality indicators not evaluated"
    return None


def check_emergency(ac):
    """SYS-020: return a description if the aircraft is signalling an emergency, else None."""
    squawk = str(ac.get("squawk") or "")
    if squawk in EMERGENCY_SQUAWKS:
        return f"squawk {squawk}: {EMERGENCY_SQUAWKS[squawk]}"
    emergency = ac.get("emergency")
    if emergency and emergency != "none":
        return f"emergency status: {emergency}"
    return None
