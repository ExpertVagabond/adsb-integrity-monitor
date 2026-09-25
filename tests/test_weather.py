import os
import unittest

from aim import weather


class PressureAltitudeTests(unittest.TestCase):
    def test_matches_icao_standard_atmosphere(self):
        # verifies: SYS-035
        for hpa, table_ft in ((1013.25, 0), (850, 4781), (500, 18289), (250, 33999), (200, 38662)):
            self.assertAlmostEqual(weather.pressure_altitude_ft(hpa), table_ft, delta=20, msg=f"{hpa} hPa")


class ModelHourTests(unittest.TestCase):
    def test_rounds_to_nearest_hour(self):
        # verifies: SYS-035
        import datetime as dt
        base = dt.datetime(2026, 9, 25, 13, 0, tzinfo=dt.timezone.utc).timestamp()
        self.assertEqual(weather.model_hour(base + 29 * 60).hour, 13)
        self.assertEqual(weather.model_hour(base + 57 * 60).hour, 14)


class CompareTests(unittest.TestCase):
    # Open-Meteo values actually returned for 39.46N 74.58W, 2026-09-25 17:00 UTC.
    HEIGHTS = {850: 1496.0, 500: 5783.0, 250: 10811.43, 200: 12300.0}

    def test_matching_trend_has_small_disagreement(self):
        # verifies: SYS-035
        fit = {"intercept_ft": -66.0, "slope_ft_per_1000": 43.6}
        check = weather.compare(fit, self.HEIGHTS, (1000, 36000))
        levels = [r[0] for r in check["rows"]]
        self.assertEqual(levels, [850, 500, 250])  # 200 hPa (38,662 ft) is above the aircraft
        self.assertLess(check["max_abs_ft"], 100)
        model_500 = next(r[2] for r in check["rows"] if r[0] == 500)
        self.assertAlmostEqual(model_500, 5783.0 * 3.28084 - weather.pressure_altitude_ft(500), places=6)

    def test_wrong_trend_shows_large_disagreement(self):
        # verifies: SYS-035
        flat = {"intercept_ft": 0.0, "slope_ft_per_1000": 0.0}  # a model that ignores temperature
        self.assertGreater(weather.compare(flat, self.HEIGHTS, (1000, 36000))["max_abs_ft"], 1000)

    def test_markdown_table(self):
        # verifies: SYS-035
        check = weather.compare({"intercept_ft": -66.0, "slope_ft_per_1000": 43.6}, self.HEIGHTS, (1000, 36000))
        md = weather.to_markdown(check, 1790355600, 39.46, -74.58)
        self.assertIn("## Independent check: weather model", md)
        self.assertIn("| 500 hPa |", md)

    @unittest.skipUnless(os.environ.get("AIM_LIVE") == "1", "set AIM_LIVE=1 to hit Open-Meteo")
    def test_live_fetch(self):
        # verifies: SYS-035
        h = weather.fetch_heights(39.46, -74.58, 1790355600)
        self.assertTrue(5000 < h[500] < 6200, h)


if __name__ == "__main__":
    unittest.main()
