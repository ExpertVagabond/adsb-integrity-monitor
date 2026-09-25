import pathlib
import re
import unittest
import xml.etree.ElementTree as ET

from aim import reqif, rtm

ROOT = pathlib.Path(__file__).resolve().parent.parent
NS = {"r": reqif.NS}


class ReqifTests(unittest.TestCase):
    def setUp(self):
        self.text, self.n = reqif.build(ROOT)
        self.doc = ET.fromstring(self.text.split("\n", 1)[1])
        self.reqs = rtm.read_requirements(ROOT / "docs" / "02-Requirements.md")

    def test_every_requirement_exported_in_order(self):
        # verifies: SYS-052
        self.assertEqual(reqif.parse_ids(self.text), list(self.reqs))
        self.assertEqual(self.n, len(self.reqs))

    def test_identifiers_unique_and_references_resolve(self):
        # verifies: SYS-052
        ids = [e.get("IDENTIFIER") for e in self.doc.iter() if e.get("IDENTIFIER")]
        self.assertEqual(len(ids), len(set(ids)), "duplicate IDENTIFIER")
        for ident in ids:  # xs:ID must be an NCName: can't start with a digit
            self.assertRegex(ident, r"^[A-Za-z_][\w.-]*$")
        refs = [e.text for e in self.doc.iter() if e.tag.endswith("-REF")]
        self.assertTrue(refs)
        missing = sorted(set(refs) - set(ids))
        self.assertEqual(missing, [], "dangling references")

    def test_attribute_values_carry_requirement_content(self):
        # verifies: SYS-052
        obj = self.doc.find(".//r:SPEC-OBJECT[@IDENTIFIER='SYS-011']", NS)
        values = {v.find("r:DEFINITION/r:ATTRIBUTE-DEFINITION-STRING-REF", NS).text: v.get("THE-VALUE")
                  for v in obj.find("r:VALUES", NS)}
        self.assertEqual(values["ad-id"], "SYS-011")
        self.assertIn("NACp below 8", values["ad-text"])
        self.assertEqual(values["ad-method"], "Test")
        self.assertEqual(values["ad-section"], "Performance checks (14 CFR 91.227(c)(1))")
        self.assertIn("tests/test_rules.py::test_nacp_boundary", values["ad-verified"])

    def test_export_is_deterministic_and_committed_copy_is_current(self):
        # verifies: SYS-052
        self.assertEqual(self.text, reqif.build(ROOT)[0])
        committed = (ROOT / "docs" / "requirements.reqif").read_text(encoding="utf-8")
        self.assertEqual(committed, self.text, "run `python -m aim reqif` and commit the result")

    def test_header_declares_reqif_1_0_content(self):
        # verifies: SYS-052
        self.assertEqual(self.doc.find(".//r:REQ-IF-VERSION", NS).text, "1.0")
        self.assertTrue(re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", self.doc.find(".//r:CREATION-TIME", NS).text))


if __name__ == "__main__":
    unittest.main()
