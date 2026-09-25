import csv
import pathlib
import tempfile
import unittest
import zipfile

from aim import registry, report

MASTER = (
    "N-NUMBER,SERIAL NUMBER,MFR MDL CODE,ENG MFR MDL,YEAR MFR,TYPE REGISTRANT,NAME,STREET,STREET2,CITY,STATE,"
    "ZIP CODE,REGION,COUNTY,COUNTRY,LAST ACTION DATE,CERT ISSUE DATE,CERTIFICATION,TYPE AIRCRAFT,TYPE ENGINE,"
    "STATUS CODE,MODE S CODE,FRACT OWNER,AIR WORTH DATE,OTHER NAMES(1),OTHER NAMES(2),OTHER NAMES(3),"
    "OTHER NAMES(4),OTHER NAMES(5),EXPIRATION DATE,UNIQUE ID,KIT MFR, KIT MODEL,MODE S CODE HEX,\n"
    "12345,S1,MDL01,E1,1978,1,JANE PRIVATE OWNER,1 SECRET LANE,,TOWN,NJ,08000,1,1,US,,,1,4,1,V,50000000,,,,,,,,,1,,"
    ",A0B1C2    ,\n"
    "67890,S2,MDL02,E2,2019,1,JOHN PRIVATE OWNER,2 HIDDEN RD,,CITY,PA,19000,1,1,US,,,1,4,1,V,50000001,,,,,,,,,2,,"
    ",A0B1C3    ,\n"
)
ACFTREF = ("CODE,MFR,MODEL,TYPE-ACFT,TYPE-ENG,AC-CAT,BUILD-CERT-IND,NO-ENG,NO-SEATS,AC-WEIGHT,SPEED,TC-DATA-SHEET,TC-DATA-HOLDER,\n"
           "MDL01,CESSNA,172N,4,1,1,0,1,4,CLASS 1,0,,,\n"
           "MDL02,VANS,RV-7,4,1,1,1,1,2,CLASS 1,0,,,\n")


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = pathlib.Path(self.tmp.name)
        self.zip = d / "ReleasableAircraft.zip"
        with zipfile.ZipFile(self.zip, "w") as zf:
            zf.writestr("MASTER.txt", "" + MASTER)
            zf.writestr("ACFTREF.txt", "" + ACFTREF)
        self.out = d / "lookup.csv"

    def tearDown(self):
        self.tmp.cleanup()

    def test_build_keeps_aircraft_facts_only(self):
        # verifies: SYS-037
        self.assertEqual(registry.build(self.zip, self.out), 2)
        text = self.out.read_text()
        for private in ("JANE", "JOHN", "SECRET", "HIDDEN", "12345"):
            self.assertNotIn(private, text)
        rows = {r["icao_hex"]: r for r in csv.DictReader(self.out.open())}
        self.assertEqual(rows["a0b1c2"]["year_mfr"], "1978")
        self.assertEqual(rows["a0b1c2"]["build_cert"], "Type certificated")
        self.assertEqual(rows["a0b1c3"]["build_cert"], "Not type certificated (experimental)")
        self.assertEqual(rows["a0b1c3"]["model"], "RV-7")

    def test_analysis_breaks_out_certification_and_decade(self):
        # verifies: SYS-037
        registry.build(self.zip, self.out)
        lookup = registry.load(self.out)

        def ac(hx, **kw):
            a = {"hex": hx, "type": "adsb_icao", "version": 2, "t": "C172", "nac_p": 9, "nac_v": 2, "nic": 8,
                 "sda": 2, "sil": 3, "lat": 39.4, "lon": -74.5, "seen_pos": 0}
            a.update(kw)
            return a

        snaps = [{"polled_at": 0, "feed_time": 0, "ac": [ac("a0b1c2"), ac("a0b1c3", nac_p=0), ac("c0ffee")]}]
        r = report.analyze(snaps, registry_data=lookup)
        by = {x["hex"]: x for x in r["aircraft"]}
        self.assertEqual((by["a0b1c3"]["year_mfr"], by["a0b1c3"]["build_cert"]), ("2019", "Not type certificated (experimental)"))
        self.assertEqual(by["c0ffee"]["build_cert"], "")  # not a US-registered aircraft
        certs = {row[0]: row for row in r["stats"]["by_build_cert"]}
        self.assertEqual(certs["Not type certificated (experimental)"][2], 1)
        md = report.to_markdown(r, "t")
        self.assertIn("### By certification basis (FAA registry)", md)
        self.assertIn("| 1970s |", md)
        self.assertNotIn("JANE", md)


if __name__ == "__main__":
    unittest.main()
