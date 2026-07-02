#!/usr/bin/env python3
"""Analyze a show soundtrack: beat grid, big hits, energy curve, silences.

Usage:
    python tools/audio/analyze_mix.py shows/2026-july-4/audio/mix.mp3

Writes <audio>.analysis.json next to the input file (commit the JSON; the
audio itself is gitignored). The JSON is what /soundtrack and snap_cues.py
consume to align firing cues to the music.
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np

try:
    import librosa
except ImportError:
    sys.exit("librosa not installed — run: pip install -r tools/audio/requirements.txt")

HOP = 512


def mmss(seconds: float) -> str:
    # Integer centiseconds so 119.997 becomes 2:00.00, never 1:60.00.
    cs = round(seconds * 100)
    m, cs = divmod(cs, 6000)
    return f"{m}:{cs / 100:05.2f}"


def analyze(path: Path) -> dict:
    y, sr = librosa.load(path, sr=None, mono=True)
    duration = float(len(y) / sr)

    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr, hop_length=HOP)
    beats = librosa.frames_to_time(beat_frames, sr=sr, hop_length=HOP)

    # Onset strength: big spikes = musical hits (drum slams, cannon shots,
    # drops) — prime targets for firing cues.
    onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=HOP)
    onset_frames = librosa.onset.onset_detect(
        onset_envelope=onset_env, sr=sr, hop_length=HOP, backtrack=False
    )
    onset_times = librosa.frames_to_time(onset_frames, sr=sr, hop_length=HOP)
    onset_strengths = onset_env[onset_frames]
    # Keep the strongest hits (top quartile), they matter for choreography.
    if len(onset_strengths):
        threshold = float(np.percentile(onset_strengths, 75))
        big_hits = [
            {"time": float(t), "clock": mmss(t), "strength": round(float(s), 2)}
            for t, s in zip(onset_times, onset_strengths)
            if s >= threshold
        ]
    else:
        big_hits = []

    # RMS energy per second — the show's intensity curve.
    rms = librosa.feature.rms(y=y, hop_length=HOP)[0]
    rms_times = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=HOP)
    step = max(1, int(round(sr / HOP)))  # ~1 s buckets
    energy = [
        {"time": round(float(rms_times[i]), 1), "rms": round(float(np.mean(rms[i : i + step])), 4)}
        for i in range(0, len(rms), step)
    ]

    # Silences / near-silences >= 1.5 s — edit seams, fades, the siren bridge.
    silence_threshold = float(np.percentile(rms, 5)) * 1.5
    silences, start = [], None
    for i, v in enumerate(rms):
        if v <= silence_threshold and start is None:
            start = rms_times[i]
        elif v > silence_threshold and start is not None:
            if rms_times[i] - start >= 1.5:
                silences.append(
                    {"start": mmss(start), "end": mmss(rms_times[i]),
                     "start_s": round(float(start), 2), "end_s": round(float(rms_times[i]), 2)}
                )
            start = None
    if start is not None and duration - start >= 1.5:
        silences.append({"start": mmss(start), "end": mmss(duration),
                         "start_s": round(float(start), 2), "end_s": round(float(duration), 2)})

    # Loudest moments — candidate finale peaks / false-finale climax.
    order = np.argsort(rms)[::-1]
    peaks, taken = [], []
    for i in order:
        t = float(rms_times[i])
        if all(abs(t - u) > 10.0 for u in taken):  # min 10 s apart
            peaks.append({"time": t, "clock": mmss(t), "rms": round(float(rms[i]), 4)})
            taken.append(t)
        if len(peaks) >= 8:
            break
    peaks.sort(key=lambda p: p["time"])

    return {
        "file": path.name,
        "duration_seconds": round(duration, 2),
        "duration_clock": mmss(duration),
        "tempo_bpm": round(float(np.atleast_1d(tempo)[0]), 1),
        "beat_count": int(len(beats)),
        "beats": [round(float(b), 3) for b in beats],
        "big_hits": big_hits,
        "loudest_moments": peaks,
        "silences": silences,
        "energy_curve": energy,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("audio", type=Path, help="path to the mixed show soundtrack")
    ap.add_argument("-o", "--output", type=Path, help="output JSON path (default: <audio>.analysis.json)")
    args = ap.parse_args()

    if not args.audio.exists():
        sys.exit(f"not found: {args.audio}")

    result = analyze(args.audio)
    out = args.output or args.audio.with_suffix(args.audio.suffix + ".analysis.json")
    out.write_text(json.dumps(result, indent=2))

    print(f"wrote {out}")
    print(f"  duration : {result['duration_clock']}  tempo ~{result['tempo_bpm']} bpm")
    print(f"  beats    : {result['beat_count']}   big hits: {len(result['big_hits'])}")
    print(f"  silences : " + (", ".join(f"{s['start']}–{s['end']}" for s in result["silences"]) or "none"))
    print("  loudest  : " + ", ".join(p["clock"] for p in result["loudest_moments"]))


if __name__ == "__main__":
    main()
