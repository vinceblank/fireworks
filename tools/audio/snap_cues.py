#!/usr/bin/env python3
"""Nudge firing-script event times onto musical beats/hits.

Usage:
    python tools/audio/snap_cues.py shows/2026-july-4/cobra.csv \
        shows/2026-july-4/audio/mix.mp3.analysis.json [--tolerance 1.5]

Reads a COBRA-style script CSV (event rows whose first column is a time like
MM:SS.ss, HH:MM:SS.ss, or bare seconds, optionally with a trailing "s") plus
an analysis JSON produced by analyze_mix.py. For each event, finds the
nearest big hit (preferred) or beat within the tolerance window and proposes
the snapped time. Snapped output is kept chronological — a snap that would
reorder events is reverted (COBRA rejects out-of-order scripts, Error 21).

STEP scripts: times after a STEP row are relative to the STEP press, not the
audio timeline, so snapping stops at the first STEP row.

Never modifies the input: writes <script>.snapped.csv and prints a report of
every proposed change for review.
"""

import argparse
import json
import re
import sys
from pathlib import Path

TIME_RE = re.compile(r"^(?:(\d+):)?(\d+):(\d{2}(?:\.\d+)?)s?$")
BARE_SECONDS_RE = re.compile(r"^\d+\.\d+s?$")  # COBRA requires the decimal


def parse_time(text: str):
    text = text.strip()
    m = TIME_RE.match(text)
    if m:
        hours = int(m.group(1)) if m.group(1) else 0
        return hours * 3600 + int(m.group(2)) * 60 + float(m.group(3))
    if BARE_SECONDS_RE.match(text):
        return float(text.rstrip("s"))
    return None


def fmt_time(seconds: float) -> str:
    # Integer centiseconds so 119.997 becomes 02:00.00s, never 01:60.00s.
    cs = round(seconds * 100)
    minutes, cs = divmod(cs, 6000)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{cs / 100:05.2f}s"
    return f"{minutes:02d}:{cs / 100:05.2f}s"


def nearest(value: float, candidates: list, tolerance: float):
    best = None
    for c in candidates:
        d = abs(c - value)
        if d <= tolerance and (best is None or d < abs(best - value)):
            best = c
    return best


def looks_like_event(line: str, first: str) -> bool:
    # Time-like first field (has : or .) — bare integers are script-header
    # rows (trigger channel), not event times.
    return (
        (":" in first or "." in first)
        and not first.startswith("#")
        and first.strip().lower() not in ("end", "step", "alternate", "alternate2")
        and line.count(",") >= 2
    )


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("script", type=Path, help="firing script CSV")
    ap.add_argument("analysis", type=Path, help="analysis JSON from analyze_mix.py")
    ap.add_argument("--tolerance", type=float, default=1.5,
                    help="max seconds a cue may move (default 1.5)")
    ap.add_argument("--offset", type=float, default=0.0,
                    help="seconds the script clock lags the audio clock "
                         "(mix time = script time + offset); use when the "
                         "script trigger is pressed mid-song, e.g. 38.0 for "
                         "the 2026 show's 0:38 sync press")
    args = ap.parse_args()

    analysis = json.loads(args.analysis.read_text())
    # Shift the musical grid into the script's clock so proposals stay in
    # script time (analysis JSON is always on the audio/mix clock).
    beats = [b - args.offset for b in analysis.get("beats", [])]
    hits = [h["time"] - args.offset for h in analysis.get("big_hits", [])]
    if not beats and not hits:
        sys.exit("analysis JSON has no beats or hits")

    lines = args.script.read_text().splitlines()
    out_lines, changes, warnings = [], [], []
    last_time = 0.0
    past_step = False

    for lineno, line in enumerate(lines, 1):
        first = line.split(",", 1)[0]
        if first.strip().upper() == "STEP" and not past_step:
            past_step = True
            warnings.append(
                f"line {lineno}: STEP row — times after it are STEP-relative, "
                "not on the audio timeline; snapping stopped here"
            )
        t = parse_time(first)
        if past_step or t is None or t == 0.0:  # headers, STEP-relative tail, 0:00 opener
            if t is None and not past_step and looks_like_event(line, first):
                warnings.append(f"line {lineno}: unrecognized time {first!r} — row left untouched")
            out_lines.append(line)
            continue
        # Prefer a big hit; fall back to the beat grid.
        target = nearest(t, hits, args.tolerance)
        if target is None:
            target = nearest(t, beats, args.tolerance)
        if target is not None and target < last_time:
            warnings.append(
                f"line {lineno}: snap {fmt_time(t)} -> {fmt_time(target)} reverted — "
                "it would reorder events (COBRA Error 21)"
            )
            target = None
        if target is None or abs(target - t) < 0.05:
            last_time = max(last_time, t)
            out_lines.append(line)
            continue
        rest = line.split(",", 1)[1] if "," in line else ""
        out_lines.append(f"{fmt_time(target)},{rest}")
        desc = rest.split(",")[2] if rest.count(",") >= 2 else ""
        changes.append((fmt_time(t), fmt_time(target), round(target - t, 2), desc[:60]))
        last_time = max(last_time, target)

    out = args.script.with_suffix(".snapped.csv")
    out.write_text("\n".join(out_lines) + "\n")

    print(f"wrote {out}")
    for w in warnings:
        print(f"  WARNING: {w}")
    if not changes:
        print("no cues snapped — nothing within tolerance was off the grid")
    for old, new, delta, desc in changes:
        sign = "+" if delta >= 0 else ""
        print(f"  {old} -> {new}  ({sign}{delta}s)  {desc}")
    print(f"\n{len(changes)} proposed change(s). Review, fold into the show overview, then re-export.")


if __name__ == "__main__":
    main()
