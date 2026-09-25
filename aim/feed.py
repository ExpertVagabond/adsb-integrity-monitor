"""Feed ingest: poll the adsb.lol v2 API and record replayable JSON Lines snapshots.

Interface (see docs/03-Architecture-ICD.md, ICD-1):
  GET https://api.adsb.lol/v2/point/{lat}/{lon}/{radius_nm}
  -> {"now": <epoch ms>, "ac": [ {aircraft state}, ... ], ...}
"""

import json
import time
import urllib.request

API = "https://api.adsb.lol/v2/point/{lat}/{lon}/{radius}"
USER_AGENT = "adsb-integrity-monitor/0.1 (+https://github.com/ExpertVagabond/adsb-integrity-monitor)"

# SYS-003: never poll faster than this, whatever the caller asks for.
MIN_INTERVAL_S = 5.0
# adsb.lol caps the point query radius at 250 NM.
MAX_RADIUS_NM = 250


def fetch(lat, lon, radius_nm, timeout=20):
    """Fetch one snapshot. Returns the decoded JSON body."""
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        raise ValueError(f"invalid center {lat},{lon}")
    if not (0 < radius_nm <= MAX_RADIUS_NM):
        raise ValueError(f"radius must be in (0, {MAX_RADIUS_NM}] NM")
    url = API.format(lat=lat, lon=lon, radius=radius_nm)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.load(resp)


def to_record(body, polled_at):
    """Normalize one API body into the snapshot record we store (SYS-002)."""
    now = body.get("now")
    return {
        "polled_at": polled_at,
        "feed_time": now / 1000.0 if isinstance(now, (int, float)) else polled_at,
        "ac": body.get("ac") or [],
    }


def effective_interval(requested_s):
    """SYS-003: clamp the polling interval to the minimum."""
    return max(float(requested_s), MIN_INTERVAL_S)


def collect(lat, lon, radius_nm, polls, interval_s, out_path, fetcher=fetch, sleep=time.sleep, clock=time.time, log=print):
    """Poll `polls` times and append each snapshot to `out_path` as one JSON line.

    `fetcher`, `sleep` and `clock` are injectable so tests can run without the network.
    Returns the number of snapshots written.
    """
    interval = effective_interval(interval_s)
    written = 0
    with open(out_path, "a", encoding="utf-8") as fh:
        for i in range(polls):
            started = clock()
            try:
                body = fetcher(lat, lon, radius_nm)
            except Exception as exc:  # keep the capture going; a missed poll is itself data
                log(f"poll {i + 1}/{polls}: fetch failed: {exc}")
            else:
                rec = to_record(body, started)
                fh.write(json.dumps(rec, separators=(",", ":")) + "\n")
                fh.flush()
                written += 1
                log(f"poll {i + 1}/{polls}: {len(rec['ac'])} aircraft")
            if i < polls - 1:
                sleep(max(0.0, interval - (clock() - started)))
    return written


def load_snapshots(path):
    """Read a JSON Lines capture back, oldest first."""
    snaps = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                snaps.append(json.loads(line))
    snaps.sort(key=lambda s: s["feed_time"])
    return snaps
