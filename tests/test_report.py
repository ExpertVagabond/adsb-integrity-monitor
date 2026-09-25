import ast
import csv
import pathlib
import sys
import tempfile
import unittest

from aim import report

ROOT = pathlib.Path(__file__).resolve().parent.parent


def good(hx, **kw):
    a = {"hex": hx, "type": "adsb_icao", "version": 2, "flight": "TEST1  ", "r": "N1", "t": "B738",
         "nac_p": 9, "nac_v": 2, "nic": 8, "sda": 2, "sil": 3, "squawk": "1200",
         "lat": 39.4, "lon": -74.5, "seen_pos": 0}
    a.update(kw)
    return a


SNAPS = [
    {"polled_at": 1000, "feed_time": 1000, "ac": [
        good("aaa001"),
        good("aaa002", nac_p=6, sil=1, flight="DEGRD1 "),
        good("aaa003", squawk="7700", flight="EMRG1  "),
        good("aaa004", nic=None),
        good("aaa005", version=0, sil=2),
        good("veh001", t="SERV", category=None, alt_baro="ground"),
        {"hex": "mlat01", "type": "mlat", "lat": 39.3, "lon": -74.4},
        {"hex": "tisb01", "type": "tisb_icao"},
    ]},
]


class AnalyzeTests(unittest.TestCase):
    def setUp(self):
        self.result = report.analyze(SNAPS)
        self.by_hex = {a["hex"]: a for a in self.result["aircraft"]}

    def test_excluded_types_are_counted_not_evaluated(self):
        # verifies: SYS-010
        self.assertEqual(self.result["excluded"], {"mlat": 1, "tisb_icao": 1, "surface vehicle": 1})
        self.assertNotIn("mlat01", self.by_hex)

    def test_verdicts(self):
        # verifies: SYS-011, SYS-015, SYS-016
        self.assertEqual(self.by_hex["aaa001"]["verdict"], "pass")
        self.assertEqual(self.by_hex["aaa002"]["verdict"], "fail")
        self.assertEqual(self.by_hex["aaa004"]["verdict"], "incomplete")

    def test_surface_vehicle_excluded(self):
        # verifies: SYS-018
        self.assertNotIn("veh001", self.by_hex)

    def test_pre_do260b_not_evaluable_not_failed(self):
        # verifies: SYS-017
        a = self.by_hex["aaa005"]
        self.assertEqual(a["verdict"], "not evaluable")
        self.assertEqual(a["checks"], [])

    def test_indicators_judged_across_snapshots(self):
        # verifies: SYS-002, SYS-019
        # One failing poll then two passing polls: the majority value (passing) decides.
        later = [{"polled_at": t, "feed_time": t, "ac": [good("aaa002", nac_p=9, sil=3)]} for t in (1010, 1020)]
        r = report.analyze(SNAPS + later)
        self.assertEqual({a["hex"]: a for a in r["aircraft"]}["aaa002"]["verdict"], "pass")

    def test_markdown_cites_paragraphs_and_disclaimer(self):
        # verifies: SYS-040, SYS-042, SYS-020
        md = report.to_markdown(self.result, "test area")
        self.assertIn("nac_p = 6, needs NACp < 0.05 NM (NACp >= 8) (91.227(c)(1)(i))", md)
        self.assertIn("91.227(c)(1)(v)", md)
        self.assertIn(report.DISCLAIMER, md)
        self.assertIn("squawk 7700: general emergency", md)

    def test_csv_one_row_per_evaluated_aircraft(self):
        # verifies: SYS-041
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / "r.csv"
            report.to_csv(self.result, p)
            with p.open(encoding="utf-8") as fh:
                rows = list(csv.DictReader(fh))
        self.assertEqual(len(rows), 5)
        row = next(r for r in rows if r["hex"] == "aaa002")
        self.assertEqual(row["polls_seen"], "1")
        self.assertEqual(row["verdict"], "fail")
        self.assertEqual(row["failed_paragraphs"], "91.227(c)(1)(i); 91.227(c)(1)(v)")


class TypicalValueTests(unittest.TestCase):
    def test_typical_value_is_most_frequent_ties_to_latest(self):
        # verifies: SYS-019
        self.assertEqual(report.typical_value([0, 2, 2, 2, 0]), 2)
        self.assertEqual(report.typical_value([2, 0]), 0)
        self.assertEqual(report.typical_value([0, 2]), 2)
        self.assertIsNone(report.typical_value([]))

    def test_flip_flopping_indicator_judged_by_majority_and_noted(self):
        # verifies: SYS-019
        # Replays a live ADS-R target whose NACv alternated 0/2 with everything else steady.
        vals = [0, 2, 0, 2, 2, 2, 0, 2]
        snaps = [{"polled_at": i, "feed_time": i, "ac": [good("u1", nac_v=v)]} for i, v in enumerate(vals)]
        a = report.analyze(snaps)["aircraft"][0]
        self.assertEqual(a["verdict"], "pass")           # 5 of 8 polls say 2
        self.assertIn("nac_v alternated between 0 and 2", a["unstable"][0])
        md = report.to_markdown(report.analyze(snaps), "t")
        self.assertIn("## Informational: unstable indicators", md)

    def test_failure_on_unstable_value_is_marked_low_confidence(self):
        # verifies: SYS-019
        vals = [2, 3, 2, 3, 2]  # majority 2 -> fails SIL, but it alternated
        snaps = [{"polled_at": i, "feed_time": i, "ac": [good("c1", sil=v)]} for i, v in enumerate(vals)]
        r = report.analyze(snaps)
        self.assertEqual(r["aircraft"][0]["verdict"], "fail")
        self.assertIn("unstable: value alternated, low confidence", report.to_markdown(r, "t"))

    def test_version_judged_by_majority(self):
        # verifies: SYS-017, SYS-019
        # Replays a CRJ9 from the 1-hour capture: version 2 in 63 polls, version 0 in 5, last poll 0.
        vals = [2] * 63 + [0] * 5
        snaps = [{"polled_at": i, "feed_time": i, "ac": [good("crj9", version=v, t="CRJ9")]} for i, v in enumerate(vals)]
        a = report.analyze(snaps)["aircraft"][0]
        self.assertEqual(a["version"], 2)
        self.assertEqual(a["verdict"], "pass")
        # And a genuinely old transmitter stays not evaluable.
        old = [{"polled_at": i, "feed_time": i, "ac": [good("old1", version=0)]} for i in range(5)]
        self.assertEqual(report.analyze(old)["aircraft"][0]["verdict"], "not evaluable")

    def test_single_bad_last_poll_does_not_decide_verdict(self):
        # verifies: SYS-019
        snaps = [{"polled_at": i, "feed_time": i, "ac": [good("s1", nic=0 if i == 5 else 8)]} for i in range(6)]
        self.assertEqual(report.analyze(snaps)["aircraft"][0]["verdict"], "pass")


class AdsrReportTests(unittest.TestCase):
    def test_adsr_converter_zeros_do_not_fail_or_flag_unstable(self):
        # verifies: SYS-021
        vals = [0, 2, 0, 2]
        snaps = [{"polled_at": i, "feed_time": i, "ac": [good("r1", type="adsr_icao", nac_v=v, nic=0)]} for i, v in enumerate(vals)]
        r = report.analyze(snaps)
        a = r["aircraft"][0]
        self.assertEqual(a["verdict"], "pass")
        self.assertEqual(a["unstable"], [])
        self.assertIn("Excluded (ADS-R converter)", report.to_markdown(r, "t"))


class RedactTests(unittest.TestCase):
    def test_identities_replaced_with_stable_pseudonyms(self):
        # verifies: SYS-043
        r1 = report.redact(report.analyze(SNAPS))
        r2 = report.redact(report.analyze(SNAPS))
        md = report.to_markdown(r1, "test")
        for ident in ("aaa002", "DEGRD1", "N1"):
            self.assertNotIn(ident, md)
        self.assertIn("pseudonyms", md)
        self.assertEqual([a["hex"] for a in r1["aircraft"]], [a["hex"] for a in r2["aircraft"]])
        self.assertTrue(all(a["hex"].startswith("AC-") and a["reg"] == "" for a in r1["aircraft"]))
        self.assertIn("B738", md)


class StdlibOnlyTests(unittest.TestCase):
    def test_runtime_imports_are_stdlib(self):
        # verifies: SYS-060
        allowed = set(sys.stdlib_module_names) | {"aim"}
        for f in (ROOT / "aim").glob("*.py"):
            tree = ast.parse(f.read_text())
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    names = [n.name for n in node.names]
                elif isinstance(node, ast.ImportFrom):
                    if node.level:  # relative import inside the package
                        continue
                    names = [node.module]
                else:
                    continue
                for n in names:
                    self.assertIn(n.split(".")[0], allowed, f"{f.name} imports {n}")


if __name__ == "__main__":
    unittest.main()
