import unittest

from aim import interference, report


def ac(hx, lat, lon, nac_p=9, nic=8, **kw):
    a = {"hex": hx, "type": "adsb_icao", "version": 2, "t": "B738", "nac_p": nac_p, "nac_v": 2,
         "nic": nic, "sda": 2, "sil": 3, "lat": lat, "lon": lon, "alt_baro": 30000, "alt_geom": 31000, "seen_pos": 0}
    a.update(kw)
    return a


def snap(t, *aircraft):
    return {"polled_at": t, "feed_time": t, "ac": list(aircraft)}


def healthy_fleet(t, degrade=(), far=False):
    """Five aircraft near 39.5N 74.5W; `degrade` lists hexes whose NACp drops to 3 in this snapshot."""
    out = []
    for i in range(5):
        hx = f"a{i}"
        lat, lon = (39.5 + 0.05 * i, -74.5) if not far or i < 2 else (41.5 + i, -70.0)
        out.append(ac(hx, lat, lon, nac_p=3 if hx in degrade else 9))
    return snap(t, *out)


class InterferenceTests(unittest.TestCase):
    def test_simultaneous_nearby_drops_form_a_cluster(self):
        # verifies: SYS-034
        snaps = [healthy_fleet(t) for t in range(0, 60, 15)] + [healthy_fleet(60, degrade={"a0", "a1", "a2"})]
        r = interference.screen(snaps)
        self.assertEqual(r["events"], 3)
        self.assertEqual(len(r["clusters"]), 1)
        self.assertEqual(r["clusters"][0]["aircraft"], ["a0", "a1", "a2"])
        self.assertEqual(r["clusters"][0]["time"], 60)

    def test_scattered_or_separate_drops_do_not_cluster(self):
        # verifies: SYS-034
        # Three drops in the same poll but too far apart, and three nearby drops in different polls.
        spread = [healthy_fleet(t) for t in range(0, 60, 15)] + [healthy_fleet(60, degrade={"a0", "a3", "a4"}, far=True)]
        self.assertEqual(interference.screen(spread)["clusters"], [])
        staggered = [healthy_fleet(t) for t in range(0, 60, 15)] + [
            healthy_fleet(60, degrade={"a0"}), healthy_fleet(75, degrade={"a1"}), healthy_fleet(90, degrade={"a2"})]
        r = interference.screen(staggered)
        self.assertEqual((r["events"], r["clusters"]), (3, []))

    def test_chronic_failures_are_not_events(self):
        # verifies: SYS-034
        # An aircraft that is always below minimum is an equipment problem, not interference.
        snaps = [snap(t, ac("bad", 39.5, -74.5, nac_p=0, nic=0), ac("ok", 39.6, -74.5)) for t in range(0, 90, 15)]
        self.assertEqual(interference.screen(snaps)["events"], 0)

    def test_aircraft_on_the_ground_are_ignored(self):
        # verifies: SYS-034
        # Three airliners powering up at one airport in the same poll must not look like a jammer.
        def gate(t, zeros):
            return snap(t, *[ac(f"g{i}", 40.64 + 0.001 * i, -73.78, nac_p=0 if zeros else 9, nic=0 if zeros else 8,
                                alt_baro="ground") for i in range(3)])
        snaps = [gate(t, False) for t in range(0, 60, 15)] + [gate(60, True)]
        self.assertEqual(interference.screen(snaps)["events"], 0)

    def test_adsr_targets_are_ignored(self):
        # verifies: SYS-034, SYS-021
        snaps = [snap(t, *[ac(f"r{i}", 39.5 + 0.01 * i, -74.5, nic=0 if t == 60 else 8, type="adsr_icao")
                           for i in range(3)]) for t in range(0, 75, 15)]
        self.assertEqual(interference.screen(snaps)["events"], 0)

    def test_report_includes_screen(self):
        # verifies: SYS-034
        snaps = [healthy_fleet(t) for t in range(0, 60, 15)] + [healthy_fleet(60, degrade={"a0", "a1", "a2"})]
        md = report.to_markdown(report.analyze(snaps), "test")
        self.assertIn("## GNSS interference screen", md)
        self.assertIn("3 aircraft", md)


if __name__ == "__main__":
    unittest.main()
