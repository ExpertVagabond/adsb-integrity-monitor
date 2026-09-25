import unittest

from aim import rules


def ac(**kw):
    base = {"hex": "a00001", "type": "adsb_icao", "version": 2,
            "nac_p": 9, "nac_v": 2, "nic": 8, "sda": 2, "sil": 3, "squawk": "1200"}
    base.update(kw)
    return base


def status(a, field):
    return next(c["status"] for c in rules.check_performance(a) if c["field"] == field)


class ReportTypeTests(unittest.TestCase):
    def test_only_adsb_and_adsr_are_evaluated(self):
        # verifies: SYS-010
        self.assertTrue(rules.is_evaluated(ac(type="adsb_icao")))
        self.assertTrue(rules.is_evaluated(ac(type="adsr_icao")))
        for t in ("mlat", "tisb_icao", "tisb_trackfile", "mode_s", "adsb_other", None):
            self.assertFalse(rules.is_evaluated(ac(type=t)), t)


class PerformanceTests(unittest.TestCase):
    def test_compliant_aircraft_passes_all_five(self):
        # verifies: SYS-011, SYS-012, SYS-013, SYS-014, SYS-015
        self.assertTrue(all(c["status"] == rules.PASS for c in rules.check_performance(ac())))

    def test_nacp_boundary(self):
        # verifies: SYS-011
        self.assertEqual(status(ac(nac_p=8), "nac_p"), rules.PASS)
        self.assertEqual(status(ac(nac_p=7), "nac_p"), rules.FAIL)

    def test_nacv_boundary(self):
        # verifies: SYS-012
        self.assertEqual(status(ac(nac_v=1), "nac_v"), rules.PASS)
        self.assertEqual(status(ac(nac_v=0), "nac_v"), rules.FAIL)

    def test_nic_boundary(self):
        # verifies: SYS-013
        self.assertEqual(status(ac(nic=7), "nic"), rules.PASS)
        self.assertEqual(status(ac(nic=6), "nic"), rules.FAIL)

    def test_sda_boundary(self):
        # verifies: SYS-014
        self.assertEqual(status(ac(sda=2), "sda"), rules.PASS)
        self.assertEqual(status(ac(sda=1), "sda"), rules.FAIL)

    def test_sil_boundary(self):
        # verifies: SYS-015
        self.assertEqual(status(ac(sil=3), "sil"), rules.PASS)
        self.assertEqual(status(ac(sil=2), "sil"), rules.FAIL)

    def test_failures_cite_the_paragraph(self):
        # verifies: SYS-011, SYS-015
        checks = {c["field"]: c for c in rules.check_performance(ac(nac_p=5, sil=1))}
        self.assertEqual(checks["nac_p"]["para"], "91.227(c)(1)(i)")
        self.assertEqual(checks["sil"]["para"], "91.227(c)(1)(v)")

    def test_missing_indicator_is_not_a_failure(self):
        # verifies: SYS-016
        a = ac()
        del a["nic"]
        a["sda"] = None
        self.assertEqual(status(a, "nic"), rules.NOT_REPORTED)
        self.assertEqual(status(a, "sda"), rules.NOT_REPORTED)
        self.assertEqual(status(a, "nac_p"), rules.PASS)

    def test_pre_do260b_version_is_not_evaluated(self):
        # verifies: SYS-017
        self.assertTrue(rules.is_pre_do260b(ac(version=0)))
        self.assertTrue(rules.is_pre_do260b(ac(version=1)))
        self.assertFalse(rules.is_pre_do260b(ac(version=2)))
        self.assertFalse(rules.is_pre_do260b(ac(version=None)))
        self.assertIn("not evaluated", rules.check_version(ac(version=0)))
        self.assertIsNone(rules.check_version(ac(version=2)))

    def test_surface_vehicles_are_recognized(self):
        # verifies: SYS-018
        self.assertTrue(rules.is_surface_vehicle(ac(category="C1")))
        self.assertTrue(rules.is_surface_vehicle(ac(category="C2")))
        self.assertTrue(rules.is_surface_vehicle(ac(category=None, t="SERV")))
        self.assertFalse(rules.is_surface_vehicle(ac(category="A3", t="B738")))


class AdsrTests(unittest.TestCase):
    def test_adsr_nacv_and_nic_excluded_others_judged(self):
        # verifies: SYS-021
        checks = {c["field"]: c["status"] for c in rules.check_performance(ac(type="adsr_icao", nac_v=0, nic=0))}
        self.assertEqual(checks["nac_v"], rules.EXCLUDED)
        self.assertEqual(checks["nic"], rules.EXCLUDED)
        self.assertEqual(checks["nac_p"], rules.PASS)

    def test_adsr_still_fails_on_nacp_and_sil(self):
        # verifies: SYS-021
        # Replays the morning C210: NACp 0 and SIL 0 arrive via the FAA path and remain real failures.
        checks = {c["field"]: c["status"] for c in rules.check_performance(ac(type="adsr_icao", nac_p=0, nac_v=0, nic=0, sil=0))}
        self.assertEqual((checks["nac_p"], checks["sil"]), (rules.FAIL, rules.FAIL))

    def test_direct_adsb_nacv_zero_still_fails(self):
        # verifies: SYS-021, SYS-012
        checks = {c["field"]: c["status"] for c in rules.check_performance(ac(type="adsb_icao", nac_v=0))}
        self.assertEqual(checks["nac_v"], rules.FAIL)


class EmergencyTests(unittest.TestCase):
    def test_emergency_squawks(self):
        # verifies: SYS-020
        self.assertIn("unlawful interference", rules.check_emergency(ac(squawk="7500")))
        self.assertIn("radio communication failure", rules.check_emergency(ac(squawk="7600")))
        self.assertIn("general emergency", rules.check_emergency(ac(squawk="7700")))

    def test_emergency_status_field(self):
        # verifies: SYS-020
        self.assertIn("lifeguard", rules.check_emergency(ac(emergency="lifeguard")))
        self.assertIsNone(rules.check_emergency(ac(emergency="none")))
        self.assertIsNone(rules.check_emergency(ac()))


if __name__ == "__main__":
    unittest.main()
