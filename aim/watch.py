"""Live monitoring: alert on emergencies and on integrity changes during flight (SYS-046, SYS-047).

The batch report answers "what happened in this window". Watch mode answers "what is
happening now": it keeps per-aircraft state across polls and only speaks when something
changes, so a steady fleet produces no output.
"""

import hashlib
import json
import time

from . import feed, rules

EMERGENCY, DEGRADED, RECOVERED, FIRST_FAIL = "EMERGENCY", "DEGRADED", "RECOVERED", "FAIL-ON-FIRST-SIGHT"
TRANSIENT = "TRANSIENT"

# SYS-048: a change must hold this many consecutive polls before DEGRADED/RECOVERED fires.
# The first live run showed an A320 at NACp 0 for one 15 s poll, then back to normal; alerting on
# every flicker trains people to ignore alerts. Blips are still recorded, as TRANSIENT.
DEFAULT_CONFIRM_POLLS = 2


def _alias(hx):
    return "AC-" + hashlib.sha256(hx.encode()).hexdigest()[:6].upper()


class Watcher:
    """Feed it snapshots in time order; it returns the alerts each one produces."""

    def __init__(self, redact=False, confirm_polls=DEFAULT_CONFIRM_POLLS):
        self.redact = redact
        self.confirm_polls = max(1, int(confirm_polls))
        self.known = {}      # hex -> merged record (fields persist between polls)
        self.verdict = {}    # hex -> confirmed verdict
        self.pending = {}    # hex -> (candidate verdict, consecutive polls seen, detail of first failing poll)
        self.emergency = {}  # hex -> last emergency description (or None)

    def _who(self, hx, ac):
        if self.redact:
            return f"{_alias(hx)} {ac.get('t', '')}".strip()
        flight = (ac.get("flight") or "").strip()
        return " ".join(x for x in (flight, ac.get("r", ""), ac.get("t", ""), hx) if x)

    def update(self, snapshot):
        alerts = []
        t = snapshot["feed_time"]
        for raw in snapshot["ac"]:
            hx = raw.get("hex")
            if not hx:
                continue
            ac = self.known.setdefault(hx, {})
            ac.update({k: v for k, v in raw.items() if v is not None})
            if not rules.is_evaluated(ac) or rules.is_surface_vehicle(ac):
                continue
            who = self._who(hx, ac)

            # SYS-046: emergencies, alerted when they first appear or change.
            emerg = rules.check_emergency(ac)
            if emerg and emerg != self.emergency.get(hx):
                alerts.append(self._alert(t, EMERGENCY, hx, who, emerg))
            self.emergency[hx] = emerg

            # SYS-047: integrity transitions. Pre-DO-260B and incomplete records never alert.
            if rules.is_pre_do260b(ac):
                continue
            checks = rules.check_performance(ac)
            failed = [c for c in checks if c["status"] == rules.FAIL]
            if any(c["status"] == rules.NOT_REPORTED for c in checks) and not failed:
                continue
            verdict = "fail" if failed else "pass"
            detail = ", ".join(f"{c['field']}={c['value']} ({c['para']})" for c in failed)
            alerts.extend(self._transition(t, hx, who, verdict, detail))
        return alerts

    def _transition(self, t, hx, who, verdict, detail):
        confirmed = self.verdict.get(hx)
        if confirmed is None:  # first sighting sets the baseline immediately
            self.verdict[hx] = verdict
            return [self._alert(t, FIRST_FAIL, hx, who, detail)] if verdict == "fail" else []
        if verdict == confirmed:
            pend = self.pending.pop(hx, None)
            if pend and pend[0] == "fail":  # dipped below minimum, came back before confirmation
                return [self._alert(t, TRANSIENT, hx, who, f"below minimum for {pend[1]} poll(s), then back: {pend[2]}")]
            return []
        cand, n, first_detail = self.pending.get(hx, (verdict, 0, detail))
        n = n + 1 if cand == verdict else 1
        self.pending[hx] = (verdict, n, first_detail if cand == verdict else detail)
        if n < self.confirm_polls:
            return []
        self.pending.pop(hx)
        self.verdict[hx] = verdict
        if verdict == "fail":
            return [self._alert(t, DEGRADED, hx, who, detail)]
        return [self._alert(t, RECOVERED, hx, who, "all five indicators back at or above minimum")]

    def _alert(self, t, level, hx, who, message):
        return {"time": t, "level": level, "aircraft": who, "id": _alias(hx) if self.redact else hx, "message": message}


def format_alert(a):
    stamp = time.strftime("%H:%M:%S", time.gmtime(a["time"]))
    return f"{stamp}Z {a['level']:<19} {a['aircraft']}: {a['message']}"


def run(lat, lon, radius_nm, polls, interval_s, out_path=None, redact=False,
        confirm_polls=DEFAULT_CONFIRM_POLLS, fetcher=feed.fetch, sleep=time.sleep, clock=time.time, log=print):
    """Poll and alert. polls=0 runs until interrupted. Returns the list of alerts raised."""
    interval = feed.effective_interval(interval_s)
    w, raised, i = Watcher(redact=redact, confirm_polls=confirm_polls), [], 0
    health = feed.FeedHealth()
    out = open(out_path, "a", encoding="utf-8") if out_path else None
    try:
        while polls == 0 or i < polls:
            started = clock()
            try:
                snap = feed.to_record(feed.fetch_with_retry(fetcher, lat, lon, radius_nm, sleep=sleep), started)
            except Exception as exc:  # a failed poll is logged, never fatal (SYS-004)
                log(f"poll {i + 1}: fetch failed: {exc}")
            else:
                warning = health.check(len(snap["ac"]))
                if warning:
                    log(warning)
                for a in w.update(snap):
                    raised.append(a)
                    log(format_alert(a))
                    if out:
                        out.write(json.dumps(a) + "\n")
                        out.flush()
            i += 1
            if polls == 0 or i < polls:
                sleep(max(0.0, interval - (clock() - started)))
    except KeyboardInterrupt:
        log(f"stopped after {i} polls, {len(raised)} alerts")
    finally:
        if out:
            out.close()
    return raised
