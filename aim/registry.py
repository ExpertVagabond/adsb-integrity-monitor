"""FAA aircraft registry enrichment (SYS-037): year built and certification basis, never owners.

Source: the FAA's public ReleasableAircraft.zip (registry.faa.gov/database). The server answers 503
to clients that don't send a browser-style Accept header; with one it serves the ~73 MB file.

Privacy: MASTER.txt includes owner names and addresses. `build` reads only the columns listed in
KEEP and writes a small aircraft-facts lookup. No owner field is ever read into memory beyond the
CSV parser's row, and the lookup is kept out of git (see .gitignore).

Builder certification codes (FAA ardata.pdf): 0 type certificated, 1 not type certificated
(experimental, including amateur-built), 2 light sport. Experimental aircraft may use GPS sources
that were never certified, which is one hypothesis for steady integrity zeros.
"""

import csv
import io
import urllib.request
import zipfile

URL = "https://registry.faa.gov/database/ReleasableAircraft.zip"
BUILD_CERT = {"0": "Type certificated", "1": "Not type certificated (experimental)", "2": "Light sport"}
FIELDS = ("icao_hex", "year_mfr", "mfr", "model", "build_cert")


def download(path, timeout=300):
    req = urllib.request.Request(URL, headers={
        "User-Agent": "Mozilla/5.0 (compatible; adsb-integrity-monitor/0.2)",
        "Accept": "text/html,application/zip,*/*",
    })
    with urllib.request.urlopen(req, timeout=timeout) as resp, open(path, "wb") as fh:
        while chunk := resp.read(1 << 20):
            fh.write(chunk)


def _rows(zf, name):
    with zf.open(name) as raw:
        reader = csv.reader(io.TextIOWrapper(raw, encoding="utf-8-sig", errors="replace"))
        header = [h.strip() for h in next(reader)]
        for row in reader:
            yield dict(zip(header, (c.strip() for c in row)))


def build(zip_path, out_path):
    """Write icao_hex, year_mfr, mfr, model, build_cert for every registered aircraft with a Mode S code."""
    with zipfile.ZipFile(zip_path) as zf:
        models = {r["CODE"]: r for r in _rows(zf, "ACFTREF.txt")}
        n = 0
        with open(out_path, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(FIELDS)
            for r in _rows(zf, "MASTER.txt"):
                hx = r.get("MODE S CODE HEX", "").lower()
                if not hx:
                    continue
                m = models.get(r.get("MFR MDL CODE", ""), {})
                w.writerow((hx, r.get("YEAR MFR", ""), m.get("MFR", ""), m.get("MODEL", ""),
                            BUILD_CERT.get(m.get("BUILD-CERT-IND", ""), "")))
                n += 1
    return n


def load(path):
    with open(path, encoding="utf-8") as fh:
        return {r["icao_hex"]: r for r in csv.DictReader(fh)}
