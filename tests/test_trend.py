import gzip
import json
import pathlib
import tempfile
import unittest

from aim import feed, trend


def ac(hx, **kw):
    a = {"hex": hx, "type": "adsb_icao", "version": 2, "t": "C172", "category": "A1", "nac_p": 9, "nac_v": 2,
         "nic": 8, "sda": 2, "sil": 3, "lat": 39.4, "lon": -74.5, "alt_baro": 5000, "seen_pos": 0}
    a.update(kw)
    return a


def write_capture(path, start, aircraft_by_poll, area=(39.46, -74.58, 100)):
    with gzip.open(path, "wt") as fh:
        for i, fleet in enumerate(aircraft_by_poll):
            rec = feed.to_record({"now": (start + 15 * i) * 1000, "ac": fleet}, start + 15 * i, area)
            fh.write(json.dumps(rec) + "\n")


class TrendTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = pathlib.Path(self.tmp.name)
        day = 86400
        # Day 1: "bad1" fails steadily; "blip" fails once in a single poll (majority passes).
        write_capture(d / "day1.jsonl.gz", 1790000000, [[ac("bad1", nac_v=0), ac("ok1"), ac("blip", nic=0 if i == 2 else 8)]
                                                         for i in range(4)])
        # Day 2: "bad1" fails again; "once" fails only today.
        write_capture(d / "day2.jsonl.gz", 1790000000 + day, [[ac("bad1", nac_v=0), ac("ok1"), ac("once", sil=1)]
                                                               for i in range(4)])
        self.paths = [d / "day2.jsonl.gz", d / "day1.jsonl.gz"]  # deliberately out of order

    def tearDown(self):
        self.tmp.cleanup()

    def test_one_row_per_capture_in_time_order(self):
        # verifies: SYS-053
        rows, _, _ = trend.build(self.paths, log=lambda *_: None)
        self.assertEqual([r["capture"] for r in rows], ["day1.jsonl.gz", "day2.jsonl.gz"])
        self.assertEqual([(r["aircraft"], r["fail"], r["fail_high_conf"]) for r in rows], [(3, 1, 1), (3, 2, 2)])
        self.assertEqual(rows[0]["area"], "100 NM around 39.46N 74.58W")
        self.assertEqual(rows[0]["pass_pct"], round(100 * 2 / 3, 2))

    def test_recurring_failure_ranks_first(self):
        # verifies: SYS-054
        _, recur, _ = trend.build(self.paths, log=lambda *_: None)
        self.assertEqual([d["hex"] for d in recur], ["bad1", "once"])
        self.assertEqual((recur[0]["seen"], recur[0]["failed_high_conf"], recur[0]["fields"]), (2, 2, ["nac_v"]))
        self.assertNotIn("blip", [d["hex"] for d in recur])  # a single-poll blip never counts

    def test_markdown_redacts_and_reports_rate(self):
        # verifies: SYS-053, SYS-054, SYS-043
        rows, recur, alt = trend.build(self.paths, log=lambda *_: None)
        md = trend.to_markdown(rows, recur, redact=True, alt_recur=alt)
        self.assertNotIn("bad1", md)
        self.assertIn(trend._alias("bad1"), md)
        self.assertIn("3 (500.0 per 1,000 aircraft)", md)
        page = trend.to_html(rows, recur, redact=True, alt_recur=alt)
        self.assertIn("<svg", page)
        self.assertNotIn("bad1", page)

    def test_captures_record_their_area(self):
        # verifies: SYS-002
        rec = feed.to_record({"now": 1000, "ac": []}, 1.0, (39.5, -74.5, 60))
        self.assertEqual(rec["area"], {"lat": 39.5, "lon": -74.5, "radius_nm": 60})
        self.assertNotIn("area", feed.to_record({"now": 1000, "ac": []}, 1.0))

    def test_old_captures_without_area_still_work(self):
        # verifies: SYS-053
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / "old.jsonl"
            p.write_text(json.dumps({"polled_at": 1, "feed_time": 1, "ac": [ac("x")]}) + "\n")
            rows, _, _ = trend.build([p], log=lambda *_: None)
        self.assertEqual(rows[0]["area"], "not recorded")


if __name__ == "__main__":
    unittest.main()
