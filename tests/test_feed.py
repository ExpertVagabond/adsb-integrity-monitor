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

    def test_rate_limit_is_retried_with_backoff(self):
        # verifies: SYS-006
        import urllib.error
        calls, waits = {"n": 0}, []

        def limited(*a):
            calls["n"] += 1
            if calls["n"] < 3:
                raise urllib.error.HTTPError("u", 429, "Too Many Requests", {"Retry-After": "7"}, None)
            return {"ac": []}

        self.assertEqual(feed.fetch_with_retry(limited, 1, 2, 3, sleep=waits.append), {"ac": []})
        self.assertEqual(waits, [7.0, 7.0])

    def test_gives_up_after_retries_and_never_retries_client_errors(self):
        # verifies: SYS-006
        import urllib.error
        waits = []

        def down(*a):
            raise urllib.error.HTTPError("u", 503, "Unavailable", {}, None)

        with self.assertRaises(urllib.error.HTTPError):
            feed.fetch_with_retry(down, sleep=waits.append)
        self.assertEqual(waits, list(feed.RETRY_DELAYS_S))

        calls = {"n": 0}

        def bad(*a):
            calls["n"] += 1
            raise urllib.error.HTTPError("u", 400, "Bad Request", {}, None)

        with self.assertRaises(urllib.error.HTTPError):
            feed.fetch_with_retry(bad, sleep=lambda s: None)
        self.assertEqual(calls["n"], 1)

    def test_feed_health_warns_on_collapse(self):
        # verifies: SYS-007
        h = feed.FeedHealth()
        self.assertEqual([h.check(n) for n in (250, 255, 248)], [None, None, None])  # building history
        self.assertIsNone(h.check(240))                                             # normal variation
        self.assertIn("0 aircraft this poll vs a recent median of 250", h.check(0))
        self.assertIn("feed health", h.check(30))

    def test_collect_logs_feed_health_warning(self):
        # verifies: SYS-007
        counts = iter([200, 210, 205, 0])
        logs = []
        clock = FakeClock()
        feed.collect(39, -74, 10, 4, 10, self.out, fetcher=lambda *a: {"ac": [{"hex": "x"}] * next(counts)},
                     sleep=clock.sleep, clock=clock.time, log=logs.append)
        self.assertTrue(any("feed health" in m for m in logs), logs)

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
