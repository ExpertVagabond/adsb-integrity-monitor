import pathlib
import unittest

from aim import airspace, report

ROOT = pathlib.Path(__file__).resolve().parent.parent

# A square "Class B" 1,500-7,000 ft around (39.9N, 75.2W) and one veil airport at (40.7N, 74.2W).
DATA = {
    "areas": [{"ident": "TST", "name": "TEST CLASS B", "class": "B", "lower_ft": 1500.0, "upper_ft": 7000.0,
               "rings": [[[-75.4, 39.7], [-75.0, 39.7], [-75.0, 40.1], [-75.4, 40.1], [-75.4, 39.7]]]}],
    "veil_airports": {"VEL": {"name": "Veil Intl", "lat": 40.7, "lon": -74.2}},
}


class RuleBasisTests(unittest.TestCase):
    def test_each_91_225_d_paragraph(self):
        # verifies: SYS-036
        self.assertEqual(airspace.rule_basis(39.9, -75.2, 3000, DATA), "91.225(d)(1)")   # inside Class B
        self.assertEqual(airspace.rule_basis(39.9, -75.2, 8000, DATA), "91.225(d)(3)")   # above its ceiling
        self.assertEqual(airspace.rule_basis(40.7, -74.4, 2000, DATA), "91.225(d)(2)")   # ~9 NM from veil airport
        self.assertEqual(airspace.rule_basis(38.0, -76.0, 12000, DATA), "91.225(d)(4)")  # Class E above 10,000
        self.assertEqual(airspace.rule_basis(38.0, -76.0, 35000, DATA), "91.225(d)(4)")  # Class A

    def test_outside_rule_airspace(self):
        # verifies: SYS-036
        self.assertIsNone(airspace.rule_basis(38.0, -76.0, 2000, DATA))    # rural, low
        self.assertIsNone(airspace.rule_basis(39.9, -75.2, 1000, DATA))    # under the Class B shelf floor
        self.assertIsNone(airspace.rule_basis(41.3, -74.2, 5000, DATA))    # 36 NM from the veil airport
        self.assertIsNone(airspace.rule_basis(40.7, -74.4, 10500 - 1000, {"areas": [], "veil_airports": {}}))

    def test_ground_is_surface(self):
        # verifies: SYS-036
        self.assertEqual(airspace.rule_basis(40.7, -74.2, "ground", DATA), "91.225(d)(2)")

    def test_polygon_with_hole(self):
        # verifies: SYS-036
        rings = [[[0, 0], [10, 0], [10, 10], [0, 10], [0, 0]], [[4, 4], [6, 4], [6, 6], [4, 6], [4, 4]]]
        self.assertTrue(airspace._inside(2, 2, rings))
        self.assertFalse(airspace._inside(5, 5, rings))

    def test_report_marks_rule_applicability(self):
        # verifies: SYS-036
        def a(hx, lat, lon, alt, **kw):
            d = {"hex": hx, "type": "adsb_icao", "version": 2, "t": "C172", "nac_p": 9, "nac_v": 2, "nic": 8,
                 "sda": 2, "sil": 3, "lat": lat, "lon": lon, "alt_baro": alt, "seen_pos": 0}
            d.update(kw)
            return d
        snaps = [{"polled_at": 0, "feed_time": 0, "ac": [a("in1", 39.9, -75.2, 3000, nac_p=0), a("out1", 38.0, -76.0, 2000, nac_p=0)]}]
        r = report.analyze(snaps, airspace_data=DATA)
        by = {x["hex"]: x["rule_airspace"] for x in r["aircraft"]}
        self.assertEqual(by, {"in1": "91.225(d)(1)", "out1": ""})
        md = report.to_markdown(r, "t")
        self.assertIn("in 91.225(d)(1) airspace", md)
        self.assertIn("not seen in 91.225(d) airspace", md)
        self.assertIn("1 of 2 aircraft were in airspace where ADS-B Out is required", md)


class ShippedDataTests(unittest.TestCase):
    def test_committed_airspace_file_is_complete(self):
        # verifies: SYS-036
        d = airspace.load(ROOT / "data" / "airspace-nyphl.json")
        self.assertEqual(d["veil_airports_missing"], [])
        self.assertEqual(len(d["veil_airports"]), len(airspace.APPENDIX_D_SECTION_1))
        idents = {a["ident"] for a in d["areas"]}
        self.assertTrue({"PHL", "JFK", "ACY"} <= idents)
        # Philadelphia International's surface is Class B.
        self.assertEqual(airspace.rule_basis(39.872, -75.241, "ground", d), "91.225(d)(1)")


if __name__ == "__main__":
    unittest.main()
