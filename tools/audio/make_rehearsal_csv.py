#!/usr/bin/env python3
"""Generate <script>.rehearsal.csv — the firing script re-based onto the
audio/mix clock so the browser rehearsal syncs with the soundtrack.

Usage:
    python tools/audio/make_rehearsal_csv.py shows/<show>/cobra.csv --offset 8.0 \
        [--preshow "1,16,Strobe beacon (1 / 90s) - MANUAL pre-show"]

- --offset: seconds the script clock lags the mix (mix = script + offset);
  the same number passed to snap_cues.py --offset.
- --preshow: extra display-only rows injected at 00:00.00s (repeatable) —
  e.g. the manually-fired strobe, so the rehearsal shows it even though it
  is deliberately NOT in the real script.

Output is <script stem>.rehearsal.csv next to the input. NEVER load a
rehearsal CSV onto the controller — it is display-timed, not fire-timed.
"""
import argparse
import csv
import re
from pathlib import Path

TIME_RE = re.compile(r"^\d\d:\d\d\.\d\ds$")


def fmt(seconds: float) -> str:
    cs = round(seconds * 100)
    minutes, cs = divmod(cs, 6000)
    return f"{minutes:02d}:{cs / 100:05.2f}s"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("script", type=Path)
    ap.add_argument("--offset", type=float, required=True)
    ap.add_argument("--preshow", action="append", default=[],
                    help="'ch,cue,description' row injected at 00:00.00s")
    args = ap.parse_args()

    rows = list(csv.reader(args.script.open(encoding="utf-8")))
    out, injected = [], False
    for r in rows:
        if r and TIME_RE.match(r[0]):
            if not injected:
                for ps in args.preshow:
                    ch, cue, desc = ps.split(",", 2)
                    out.append(["00:00.00s", ch, cue, desc] + [""] * 7)
                injected = True
            m, s = r[0][:-1].split(":")
            r = [fmt(int(m) * 60 + float(s) + args.offset)] + r[1:]
        out.append(r)

    dest = args.script.with_suffix(".rehearsal.csv")
    with dest.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(out)
    print(f"wrote {dest} (+{args.offset}s, {len(args.preshow)} pre-show row(s))")


if __name__ == "__main__":
    main()
