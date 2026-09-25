import pathlib
import tempfile
import unittest

from aim import rtm

ROOT = pathlib.Path(__file__).resolve().parent.parent


class RtmTests(unittest.TestCase):
    def test_every_requirement_in_this_repo_is_verified(self):
        # verifies: SYS-050
        reqs = rtm.read_requirements(ROOT / "docs" / "02-Requirements.md")
        tags = rtm.read_tags(ROOT / "tests")
        _, unverified, unknown = rtm.build(reqs, tags)
        self.assertGreaterEqual(len(reqs), 20)
        self.assertEqual(unverified, [])
        self.assertEqual(unknown, [])

    def test_unverified_requirement_is_reported(self):
        # verifies: SYS-050
        with tempfile.TemporaryDirectory() as d:
            d = pathlib.Path(d)
            (d / "docs").mkdir()
            (d / "tests").mkdir()
            (d / "docs" / "02-Requirements.md").write_text(
                "| SYS-900 | Covered. | T | x |\n| SYS-901 | Not covered. | T | x |\n")
            # Tag assembled at runtime so this file's own source doesn't cite the fake ID.
            tag = "verif" + "ies: SYS-900"
            (d / "tests" / "test_x.py").write_text(f"def test_a():\n    # {tag}\n    pass\n")
            _, unverified, unknown = rtm.run(d)
            self.assertEqual(unverified, ["SYS-901"])
            self.assertEqual(unknown, [])
            self.assertIn("**NOT VERIFIED**", (d / "docs" / "RTM.md").read_text())


if __name__ == "__main__":
    unittest.main()
