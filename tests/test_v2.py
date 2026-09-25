import gzip
import json
import pathlib
import re
import tempfile
import unittest

from aim import altitude, feed, htmlreport, report, stats

ROOT = pathlib.Path(__file__).resolve().parent.parent


def ac(hx, baro, diff, **kw):
    a = {"hex": hx, "type": "adsb_icao", "version": 2, "t": "B738", "category": "A3",
         "nac_p": 9, "nac_v": 2, "nic": 8, "sda": 2, "sil": 3,
         "alt_baro": baro, "alt_geom": None if diff is None else baro + diff,
         "lat": 39.4, "lon": -74.5, "seen_pos": 0}
    a.update(kw)
    return a


def trend_fleet(n=15, outlier=None):
    """Aircraft whose geometric-baro difference follows 50 ft per 1,000 ft, plus an optional outlier."""
    fleet = {f"a{i:05d}": ac(f"a{i:05d}", 2000 + 2500 * i, int(-150 + 0.05 * (2000 + 2500 * i))) for i in range(n)}
    if outlier:
        fleet[outlier[0]] = ac(outlier[0], outlier[1], outlier[2])
    return fleet


class GzipTests(unittest.TestCase):
    def test_gzip_capture_loads_like_plain(self):
        # verifies: SYS-005
        recs = [{"polled_at": 2, "feed_time": 2, "ac": []}, {"polled_at": 1, "feed_time": 1, "ac": [{"hex": "x"}]}]
        with tempfile.TemporaryDirectory() as d:
            plain, packed = pathlib.Path(d) / "c.jsonl", pathlib.Path(d) / "c.jsonl.gz"
            body = "".join(json.dumps(r) + "\n" for r in recs)
            plain.write_text(body)
            with gzip.open(packed, "wt") as fh:
                fh.write(body)
            self.assertEqual(feed.load_snapshots(plain), feed.load_snapshots(packed))
            self.assertEqual([s["feed_time"] for s in feed.load_snapshots(packed)], [1, 2])


class AltitudeTests(unittest.TestCase):
    def test_theil_sen_recovers_line_despite_outlier(self):
        # verifies: SYS-033
        pts = [(x, 10 + 2 * x) for x in range(10)] + [(5, 500)]
        a, b = altitude.theil_sen(pts)
        self.assertAlmostEqual(b, 2.0, places=6)
        self.assertAlmostEqual(a, 10.0, places=6)

    def test_trend_following_fleet_is_clean(self):
        # verifies: SYS-033
        findings, fit = altitude.altitude_findings(trend_fleet())
        self.assertEqual(findings, {})
        self.assertAlmostEqual(fit["slope_ft_per_1000"], 50.0, delta=1)

    def test_outlier_flagged(self):
        # verifies: SYS-033
        # At 20,000 ft the trend predicts +850 ft; this aircraft reports +300 ft, 550 ft off.
        findings, _ = altitude.altitude_findings(trend_fleet(outlier=("bad001", 20000, 300)))
        self.assertEqual(list(findings), ["bad001"])
        self.assertIn("-550 ft off its 8 nearest neighbors", findings["bad001"])

    def test_regional_weather_shift_is_not_flagged(self):
        # verifies: SYS-033
        # A whole second region 150 NM away runs +300 ft (different weather): no flags.
        fleet = trend_fleet()
        for i in range(10):
            hx = f"w{i:02d}"
            baro = 3000 + 3000 * i
            fleet[hx] = ac(hx, baro, int(-150 + 0.05 * baro) + 300, lat=41.9, lon=-74.5)
        findings, fit = altitude.altitude_findings(fleet)
        self.assertEqual(findings, {})
        # The top and bottom aircraft of each group aren't bracketed by neighbors: not assessed, never flagged.
        self.assertEqual((fit["local"], fit["not_assessed"]), (21, 4))

    def test_top_of_traffic_is_not_assessed(self):
        # verifies: SYS-033
        # Replays the E55P case: the highest aircraft, well off the straight line, has neighbors only below.
        fleet = trend_fleet(outlier=("top001", 41000, int(-150 + 0.05 * 41000) - 250))
        findings, fit = altitude.altitude_findings(fleet)
        self.assertNotIn("top001", findings)

    def test_ground_and_missing_altitudes_ignored(self):
        # verifies: SYS-033
        fleet = trend_fleet()
        fleet["gnd"] = ac("gnd", "ground", None)
        fleet["low"] = ac("low", 500, 900)       # below MIN_ALTITUDE_FT
        fleet["nogeo"] = ac("nogeo", 12000, None)
        findings, fit = altitude.altitude_findings(fleet)
        self.assertEqual(findings, {})
        self.assertEqual(fit["n"], 15)
        self.assertEqual(fit["not_assessed"], 2)  # lowest and highest of the stack

    def test_too_few_aircraft_no_fit(self):
        # verifies: SYS-033
        findings, fit = altitude.altitude_findings(trend_fleet(n=5))
        self.assertEqual((findings, fit), ({}, None))


class StatsTests(unittest.TestCase):
    def test_altitude_bands_follow_91_225(self):
        # verifies: SYS-044
        self.assertEqual(stats.altitude_band("ground"), "Surface")
        self.assertEqual(stats.altitude_band(9999), "Below 10,000 ft")
        self.assertEqual(stats.altitude_band(10000), "10,000 ft to FL180")
        self.assertEqual(stats.altitude_band(18000), "FL180 and above")
        self.assertEqual(stats.altitude_band(None), "Unknown")

    def test_breakdowns_and_failing_types(self):
        # verifies: SYS-044
        snaps = [{"polled_at": 1, "feed_time": 1, "ac": [
            ac("p1", 35000, 1500), ac("p2", 36000, 1550),
            ac("f1", 4000, 50, t="C172", category="A1", nic=0),
            ac("p3", 5000, 90, t="C172", category="A1"),
        ]}]
        s = report.analyze(snaps)["stats"]
        cats = {r[0]: r for r in s["by_category"]}
        self.assertEqual(cats["A1 Light (< 15,500 lb)"][1:3], (2, 1))
        self.assertEqual(cats["A1 Light (< 15,500 lb)"][5], 50.0)
        bands = {r[0]: r for r in s["by_band"]}
        self.assertEqual(bands["FL180 and above"][1:3], (2, 0))
        self.assertEqual(s["failing_types"][0][:3], ("C172", 2, 1))
        self.assertEqual(s["by_report_type"][0][:3], ("Direct 1090ES ADS-B", 4, 1))
        self.assertIn("### By altitude band", stats.to_markdown(s))

    def test_band_uses_highest_altitude_seen(self):
        # verifies: SYS-044
        snaps = [{"polled_at": 1, "feed_time": 1, "ac": [ac("x", 24000, 1000)]},
                 {"polled_at": 2, "feed_time": 2, "ac": [ac("x", "ground", None)]}]
        a = report.analyze(snaps)["aircraft"][0]
        self.assertEqual(stats.altitude_band(a["alt_baro"]), "FL180 and above")


class HtmlTests(unittest.TestCase):
    def setUp(self):
        self.snaps = [{"polled_at": 1, "feed_time": 1, "ac": [
            ac("abc123", 30000, 1300, flight="SECRET1 ", r="N12345", lat=39.5, lon=-74.6),
            ac("def456", 4000, 50, t="C172", category="A1", nic=0, r="N99999", lat=39.2, lon=-74.2),
        ]}]

    def test_html_is_self_contained_with_map(self):
        # verifies: SYS-045
        page = htmlreport.to_html(report.analyze(self.snaps), self.snaps, "test")
        self.assertIn("<svg", page)
        self.assertEqual(page.count("<polyline"), 2)
        self.assertIn("var(--fail)", page)
        self.assertIsNone(re.search(r'(src|href)\s*=\s*["\']https?://', page), "external resource found")
        self.assertIn("91.227(c)(1)(iii)", page)

    def test_html_respects_redaction(self):
        # verifies: SYS-045, SYS-043
        result = report.redact(report.analyze(self.snaps))
        page = htmlreport.to_html(result, self.snaps, "test")
        for ident in ("abc123", "def456", "SECRET1", "N12345", "N99999"):
            self.assertNotIn(ident, page)
        self.assertEqual(page.count("<polyline"), 2)  # tracks still drawn via the internal key
        self.assertIn("pseudonyms", page)

    def test_csv_never_leaks_internal_key(self):
        # verifies: SYS-043
        result = report.redact(report.analyze(self.snaps))
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / "r.csv"
            report.to_csv(result, p)
            text = p.read_text()
        self.assertNotIn("abc123", text)
        self.assertNotIn("def456", text)


class CiTests(unittest.TestCase):
    def test_ci_runs_tests_and_traceability_gate(self):
        # verifies: SYS-051
        wf = (ROOT / ".github" / "workflows" / "ci.yml").read_text()
        self.assertIn("python -m unittest discover -s tests", wf)
        self.assertIn("python -m aim rtm", wf)
        self.assertIn("git diff --exit-code docs/RTM.md", wf)


if __name__ == "__main__":
    unittest.main()
