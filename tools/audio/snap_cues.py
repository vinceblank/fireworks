#!/usr/bin/env python3
"""Nudge firing-script event times onto musical beats/hits.

Usage:
    python tools/audio/snap_cues.py shows/2026-july-4/cobra.csv \
        shows/2026-july-4/audio/mix.mp3.analysis.json [--tolerance 1.5]

Reads a COBRA-style script CSV (or any CSV whose event rows start with an
#Event Time column formatted MM:SS.ss) plus an analysis JSON produced by
analyze_mix.py. For each event, finds the nearest big hit (preferred) or beat
within the tolerance window and proposes the snapped time.

Never modifies the input: writes <script>.snapped.csv and prints a report of
every proposed change for review.
"""

import argparse
import json
import re
import sys
from pathlib import Path

TIME_RE = re.compile(r"^(\d+):(\d{2}(?:\.\d+)?)s?$")


def parse_time(text: str):
    m = TIME_RE.match(text.strip())
    if not m:
        return None
    return int(m.group(1)) * 60 + float(m.group(2))


def fmt_time(seconds: float) -> str:
    m, s = divmod(seconds, 60.0)
    return f"{int(m):02d}:{s:05.2f}s"


def nearest(value: float, candidates: list, tolerance: float):
    best = None
    for c in candidates:
        d = abs(c - value)
        if d <= tolerance and (best is None or d < abs(best - value)):
            best = c
    return best


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("script", type=Path, help="firing script CSV")
    ap.add_argument("analysis", type=Path, help="analysis JSON from analyze_mix.py")
    ap.add_argument("--tolerance", type=float, default=1.5,
                    help="max seconds a cue may move (default 1.5)")
    args = ap.parse_args()

    analysis = json.loads(args.analysis.read_text())
    beats = analysis.get("beats", [])
    hits = [h["time"] for h in analysis.get("big_hits", [])]
    if not beats and not hits:
        sys.exit("analysis JSON has no beats or hits")

    lines = args.script.read_text().splitlines()
    out_lines, changes = [], []

    for line in lines:
        first = line.split(",", 1)[0]
        t = parse_time(first)
        if t is None or t == 0.0:  # headers, comments, and the 0:00 opener stay put
            out_lines.append(line)
            continue
        # Prefer a big hit; fall back to the beat grid.
        target = nearest(t, hits, args.tolerance)
        if target is None:
            target = nearest(t, beats, args.tolerance)
        if target is None or abs(target - t) < 0.05:
            out_lines.append(line)
            continue
        rest = line.split(",", 1)[1] if "," in line else ""
        out_lines.append(f"{fmt_time(target)},{rest}")
        desc = rest.split(",")[2] if rest.count(",") >= 2 else ""
        changes.append((fmt_time(t), fmt_time(target), round(target - t, 2), desc[:60]))

    out = args.script.with_suffix(".snapped.csv")
    out.write_text("\n".join(out_lines) + "\n")

    print(f"wrote {out}")
    if not changes:
        print("no cues needed snapping — everything already on the grid")
    for old, new, delta, desc in changes:
        sign = "+" if delta >= 0 else ""
        print(f"  {old} -> {new}  ({sign}{delta}s)  {desc}")
    print(f"\n{len(changes)} proposed change(s). Review, then replace the original if approved.")


if __name__ == "__main__":
    main()
