import json
import pathlib
import tempfile
import unittest

from aim import watch


def ac(hx, **kw):
    a = {"hex": hx, "type": "adsb_icao", "version": 2, "t": "C172", "r": "N1", "flight": "TST1",
         "nac_p": 9, "nac_v": 2, "nic": 8, "sda": 2, "sil": 3, "squawk": "1200"}
    a.update(kw)
    return a


def snap(t, *aircraft):
    return {"polled_at": t, "feed_time": t, "ac": list(aircraft)}


class WatcherTests(unittest.TestCase):
    def test_steady_fleet_is_silent(self):
        # verifies: SYS-047
        w = watch.Watcher()
        for t in range(5):
            self.assertEqual(w.update(snap(t, ac("a1"), ac("a2"))), [])

    def test_degradation_and_recovery(self):
        # verifies: SYS-047, SYS-048
        w = watch.Watcher()
        self.assertEqual(w.update(snap(0, ac("a1"))), [])
        self.assertEqual(w.update(snap(15, ac("a1", nic=0))), [])  # first failing poll: pending
        alerts = w.update(snap(30, ac("a1", nic=0)))                # second: confirmed
        self.assertEqual([a["level"] for a in alerts], [watch.DEGRADED])
        self.assertIn("nic=0 (91.227(c)(1)(iii))", alerts[0]["message"])
        self.assertEqual(w.update(snap(45, ac("a1", nic=0))), [])  # no repeat while it stays failed
        self.assertEqual(w.update(snap(60, ac("a1"))), [])
        self.assertEqual([a["level"] for a in w.update(snap(75, ac("a1")))], [watch.RECOVERED])

    def test_single_poll_blip_is_transient_not_degraded(self):
        # verifies: SYS-048
        # Replays the first live run: an A320 at NACp 0 for one poll, then normal.
        w = watch.Watcher()
        w.update(snap(0, ac("a1", t="A320")))
        self.assertEqual(w.update(snap(15, ac("a1", t="A320", nac_p=0, nac_v=0))), [])
        alerts = w.update(snap(30, ac("a1", t="A320")))
        self.assertEqual([a["level"] for a in alerts], [watch.TRANSIENT])
        self.assertIn("below minimum for 1 poll(s)", alerts[0]["message"])
        self.assertIn("nac_p=0", alerts[0]["message"])

    def test_confirm_one_alerts_immediately(self):
        # verifies: SYS-048
        w = watch.Watcher(confirm_polls=1)
        w.update(snap(0, ac("a1")))
        self.assertEqual([a["level"] for a in w.update(snap(15, ac("a1", sil=1)))], [watch.DEGRADED])

    def test_fail_on_first_sight(self):
        # verifies: SYS-047
        alerts = watch.Watcher().update(snap(0, ac("a1", nac_p=0)))
        self.assertEqual([a["level"] for a in alerts], [watch.FIRST_FAIL])

    def test_fields_persist_between_polls(self):
        # verifies: SYS-047
        # A later poll without the indicators must not flip the aircraft to "not reported".
        w = watch.Watcher()
        w.update(snap(0, ac("a1")))
        bare = {"hex": "a1", "type": "adsb_icao", "lat": 39.4, "lon": -74.5}
        self.assertEqual(w.update(snap(15, bare)), [])

    def test_emergency_alerts_once_per_change(self):
        # verifies: SYS-046
        w = watch.Watcher()
        w.update(snap(0, ac("a1")))
        a = w.update(snap(15, ac("a1", squawk="7700")))
        self.assertEqual([x["level"] for x in a], [watch.EMERGENCY])
        self.assertIn("general emergency", a[0]["message"])
        self.assertEqual(w.update(snap(30, ac("a1", squawk="7700"))), [])
        self.assertEqual([x["level"] for x in w.update(snap(45, ac("a1", squawk="7600")))], [watch.EMERGENCY])

    def test_excluded_targets_never_alert(self):
        # verifies: SYS-046, SYS-047
        w = watch.Watcher()
        noisy = [ac("v1", t="SERV", nic=0, squawk="7700"), ac("m1", type="mlat", nic=0), ac("o1", version=0, nic=0)]
        self.assertEqual(w.update(snap(0, *noisy)), [])

    def test_redacted_alerts_hide_identity(self):
        # verifies: SYS-043, SYS-047
        a = watch.Watcher(redact=True).update(snap(0, ac("abc123", nic=0, r="N555", flight="SECRET")))[0]
        text = json.dumps(a)
        for ident in ("abc123", "N555", "SECRET"):
            self.assertNotIn(ident, text)
        self.assertTrue(a["id"].startswith("AC-"))


class RunTests(unittest.TestCase):
    def test_run_writes_alert_log_and_survives_failed_poll(self):
        # verifies: SYS-046, SYS-004
        bodies = [{"now": 0, "ac": [ac("a1")]}, None, {"now": 30000, "ac": [ac("a1", squawk="7500")]}]
        calls = {"n": 0}

        def fetcher(*_):
            body = bodies[calls["n"]]
            calls["n"] += 1
            if body is None:
                raise OSError("timeout")
            return body

        logs = []
        with tempfile.TemporaryDirectory() as d:
            out = pathlib.Path(d) / "alerts.jsonl"
            raised = watch.run(39, -74, 10, 3, 15, out, fetcher=fetcher, sleep=lambda s: None,
                               clock=lambda: 0.0, log=logs.append)
            lines = out.read_text().splitlines()
        self.assertEqual([a["level"] for a in raised], [watch.EMERGENCY])
        self.assertEqual(len(lines), 1)
        self.assertTrue(any("fetch failed" in m for m in logs))
        self.assertTrue(any("unlawful interference" in m for m in logs))


if __name__ == "__main__":
    unittest.main()
