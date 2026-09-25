import json
import os
import pathlib
import tempfile
import unittest

from aim import feed


class FakeClock:
    def __init__(self):
        self.t = 1000.0
        self.sleeps = []

    def time(self):
        return self.t

    def sleep(self, s):
        self.sleeps.append(s)
        self.t += s


class CollectTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.out = pathlib.Path(self.tmp.name) / "cap.jsonl"

    def tearDown(self):
        self.tmp.cleanup()

    def test_each_poll_is_one_replayable_record(self):
        # verifies: SYS-002
        clock = FakeClock()
        body = {"now": 1_700_000_000_000, "ac": [{"hex": "abc"}]}
        n = feed.collect(39, -74, 10, 3, 10, self.out, fetcher=lambda *a: body,
                         sleep=clock.sleep, clock=clock.time, log=lambda *_: None)
        self.assertEqual(n, 3)
        lines = self.out.read_text().splitlines()
        self.assertEqual(len(lines), 3)
        rec = json.loads(lines[0])
        self.assertEqual(rec["feed_time"], 1_700_000_000.0)
        self.assertEqual(rec["ac"], [{"hex": "abc"}])
        self.assertEqual(len(feed.load_snapshots(self.out)), 3)

    def test_interval_is_clamped_to_minimum(self):
        # verifies: SYS-003
        self.assertEqual(feed.effective_interval(1), feed.MIN_INTERVAL_S)
        self.assertEqual(feed.effective_interval(0), feed.MIN_INTERVAL_S)
        self.assertEqual(feed.effective_interval(12), 12)
        clock = FakeClock()
        feed.collect(39, -74, 10, 4, 0.5, self.out, fetcher=lambda *a: {"ac": []},
                     sleep=clock.sleep, clock=clock.time, log=lambda *_: None)
        self.assertTrue(all(s >= feed.MIN_INTERVAL_S for s in clock.sleeps), clock.sleeps)

    def test_failed_poll_does_not_stop_capture(self):
        # verifies: SYS-004
        calls = {"n": 0}
        logs = []

        def flaky(*a):
            calls["n"] += 1
            if calls["n"] == 2:
                raise OSError("timeout")
            return {"ac": []}

        clock = FakeClock()
        n = feed.collect(39, -74, 10, 3, 10, self.out, fetcher=flaky,
                         sleep=clock.sleep, clock=clock.time, log=logs.append)
        self.assertEqual(n, 2)
        self.assertTrue(any("fetch failed" in m for m in logs))

    def test_area_validation(self):
        # verifies: SYS-001
        with self.assertRaises(ValueError):
            feed.fetch(95, 0, 10)
        with self.assertRaises(ValueError):
            feed.fetch(39, -74, 300)

    @unittest.skipUnless(os.environ.get("AIM_LIVE") == "1", "set AIM_LIVE=1 to hit the live API")
    def test_live_fetch_returns_aircraft_with_quality_fields(self):
        # verifies: SYS-001
        body = feed.fetch(39.4576, -74.5772, 60)
        self.assertIn("ac", body)
        adsb = [a for a in body["ac"] if a.get("type") == "adsb_icao"]
        self.assertTrue(adsb, "no ADS-B aircraft in the area right now")
        self.assertTrue(any("nic" in a and "sil" in a for a in adsb))


if __name__ == "__main__":
    unittest.main()
