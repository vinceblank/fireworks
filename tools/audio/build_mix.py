"""Assemble a show mix from a recipe JSON.

Usage: python tools/audio/build_mix.py <recipe.json>

The recipe is the committable source of truth for the mix (audio files are
gitignored); anyone with the source tracks can rebuild the exact mix.

Recipe format:
{
  "output": "shows/<show>/audio/mix.wav",
  "sample_rate": 44100,
  "target_rms_db": -14.0,     // per-segment loudness match; null disables
  "items": [                   // the main chain, placed at absolute times
    {"name": "...", "file": "music/tracks/x.mp3",
     "src_start": 0.0, "src_end": 123.4,   // cut points in the source file
     "at": 0.0,                             // placement in the mix
     "gain_db": 0.0,                        // extra gain after RMS match
     "fade_in": 0.0, "fade_out": 0.5,       // seconds (equal-power curves)
     "rms_match": true}                     // false for SFX kept at natural level
  ],
  "overlays": [ ... same fields ... ]       // layered on top (rumble, drops)
}
All paths are relative to the repo root (the recipe file's grandparent dirs
are searched upward for a marker; simplest: run from repo root).
"""
import json
import sys
import numpy as np
import librosa
import soundfile as sf


def load_stereo(path, sr):
    y, _ = librosa.load(path, sr=sr, mono=False)
    if y.ndim == 1:
        y = np.stack([y, y])
    return y


def fmt(t):
    return f"{int(t // 60)}:{t % 60:05.2f}"


def render(recipe_path):
    recipe = json.load(open(recipe_path, encoding="utf-8"))
    sr = recipe.get("sample_rate", 44100)
    target_rms_db = recipe.get("target_rms_db", -14.0)

    def prepare(item):
        y = load_stereo(item["file"], sr)
        s0 = int(item.get("src_start", 0.0) * sr)
        s1 = int(item["src_end"] * sr) if "src_end" in item else y.shape[1]
        seg = y[:, s0:s1].copy()
        if target_rms_db is not None and item.get("rms_match", True):
            rms = np.sqrt(np.mean(seg ** 2))
            if rms > 1e-9:
                seg *= 10 ** (target_rms_db / 20) / rms
        seg *= 10 ** (item.get("gain_db", 0.0) / 20)
        fi = int(item.get("fade_in", 0.0) * sr)
        fo = int(item.get("fade_out", 0.0) * sr)
        if fi > 0:
            seg[:, :fi] *= np.sqrt(np.linspace(0, 1, fi))[None, :]
        if fo > 0:
            seg[:, -fo:] *= np.sqrt(np.linspace(1, 0, fo))[None, :]
        return seg

    items = recipe["items"] + recipe.get("overlays", [])
    total = max(it["at"] + (it["src_end"] - it.get("src_start", 0.0)) for it in items)
    master = np.zeros((2, int((total + 1.0) * sr)), dtype=np.float64)

    print(f"{'item':<28} {'mix start':>9} {'mix end':>9}")
    for it in recipe["items"]:
        seg = prepare(it)
        a = int(it["at"] * sr)
        master[:, a:a + seg.shape[1]] += seg
        print(f"{it['name']:<28} {fmt(it['at']):>9} {fmt(it['at'] + seg.shape[1] / sr):>9}")
    for it in recipe.get("overlays", []):
        seg = prepare(it)
        a = int(it["at"] * sr)
        master[:, a:a + seg.shape[1]] += seg
        print(f"{'(overlay) ' + it['name']:<28} {fmt(it['at']):>9} {fmt(it['at'] + seg.shape[1] / sr):>9}")

    peak = np.abs(master).max()
    if peak > 0:
        master *= 0.95 / peak
    out = recipe["output"]
    sf.write(out, master.T, sr, subtype="PCM_16")
    print(f"\nwrote {out}  ({fmt(master.shape[1] / sr)}, peak-normalized from {20*np.log10(peak):.1f} dBFS)")
    mp3 = out.rsplit(".", 1)[0] + ".mp3"
    try:
        sf.write(mp3, master.T, sr, format="MP3")
        print(f"wrote {mp3}")
    except Exception as e:
        print(f"(mp3 export unavailable: {e})")


if __name__ == "__main__":
    render(sys.argv[1])
