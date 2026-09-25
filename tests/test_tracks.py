import unittest

from aim import tracks


def snap(t, *aircraft):
    return {"polled_at": t, "feed_time": t, "ac": list(aircraft)}


def pos(hx, lat, lon=-74.5, seen_pos=0.0):
    return {"hex": hx, "lat": lat, "lon": lon, "seen_pos": seen_pos}


class DropoutTests(unittest.TestCase):
    def test_stale_then_reacquired_is_a_dropout(self):
        # verifies: SYS-030
        snaps = [snap(1000, pos("abc", 39.40)), snap(1035, pos("abc", 39.40, seen_pos=35)),
                 snap(1045, pos("abc", 39.52, seen_pos=0.5))]
        f = tracks.continuity_findings(snaps, coast_s=20)
        self.assertEqual(len(f["abc"]), 1)
        self.assertIn("at least 35 s without a refresh, then reacquired", f["abc"][0])

    def test_stale_and_never_reacquired_is_a_lost_track_not_a_dropout(self):
        # verifies: SYS-032
        snaps = [snap(1000, pos("abc", 39.40)), snap(1010, pos("abc", 39.40, seen_pos=10)),
                 snap(1040, pos("abc", 39.40, seen_pos=40))]
        self.assertEqual(tracks.continuity_findings(snaps, coast_s=20), {})
        self.assertIn("40 s old", tracks.lost_tracks(snaps, coast_s=20)["abc"])
        self.assertEqual(tracks.lost_tracks([snap(1000, pos("ok", 39.4))], coast_s=20), {})

    def test_disappearance_is_a_dropout(self):
        # verifies: SYS-030
        snaps = [snap(1000, pos("abc", 39.40)), snap(1010), snap(1020), snap(1030, pos("abc", 39.45))]
        f = tracks.continuity_findings(snaps, coast_s=20)
        self.assertIn("absent from 2 snapshot(s), 30 s between sightings", f["abc"][0])

    def test_slow_poll_is_not_a_dropout(self):
        # verifies: SYS-030
        # Regression: our own poll gap (20.5 s) must not be blamed on the aircraft.
        snaps = [snap(1000, pos("abc", 39.40, seen_pos=0.4)), snap(1020.5, pos("abc", 39.48, seen_pos=0.6))]
        self.assertEqual(tracks.continuity_findings(snaps, coast_s=20), {})

    def test_steady_track_is_clean(self):
        # verifies: SYS-030, SYS-031
        snaps = [snap(1000 + 10 * i, pos("abc", 39.40 + 0.01 * i)) for i in range(6)]
        self.assertEqual(tracks.continuity_findings(snaps, coast_s=20), {})

    def test_seen_pos_backdates_the_fix(self):
        # verifies: SYS-030
        # Same position reported 10 s later but seen_pos says it is 10 s old: one fix.
        snaps = [snap(1000, pos("abc", 39.40)), snap(1010, pos("abc", 39.40, seen_pos=10))]
        self.assertEqual(len(tracks.position_fixes(snaps)["abc"]), 1)


class JumpTests(unittest.TestCase):
    def test_position_jump_detected(self):
        # verifies: SYS-031
        # 1 degree of latitude (60 NM) in 10 s = 21,600 kt.
        snaps = [snap(1000, pos("bad", 39.0)), snap(1010, pos("bad", 40.0))]
        f = tracks.continuity_findings(snaps, coast_s=20)
        self.assertIn("position jump", f["bad"][0])

    def test_airliner_speed_is_not_a_jump(self):
        # verifies: SYS-031
        # 500 kt for 10 s = 1.39 NM, about 0.0231 degrees of latitude.
        snaps = [snap(1000, pos("ok", 39.0)), snap(1010, pos("ok", 39.0231))]
        self.assertEqual(tracks.continuity_findings(snaps, coast_s=20), {})

    def test_haversine_one_degree_latitude(self):
        # verifies: SYS-031
        self.assertAlmostEqual(tracks.haversine_nm(39, -74.5, 40, -74.5), 60.04, places=1)


if __name__ == "__main__":
    unittest.main()
