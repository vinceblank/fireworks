# 2026 Show — Mortar Rack Plan (v2 model: GENERIC shells, as-wired timing)

**Model change (user, 2026-07-03):** mortar types are intermixed — all 85
loaded shells are treated as **generic mortars**. Groups are defined by
**rack + actual wiring**, not shell type. Timing comes from the real fuse
runs below, not nominal paces. (86 shells on hand → 85 loaded, 1 spare.)

**Rack fleet:** 3×6 fan (18), 4×4 square (16), 3×7 fan (21), 1×9 straight
(9), 1×21 straight (21) = 85 tubes.

**Universal shell timing:** e-match/fuse lights the shell's leader → burns
down the tube → lift: **tap-ignition → break ≈ 5.5 s** (≈3.5 s leader +
2 s lift, owner-verified).

## As-wired groups (one cue each)

| Rack | Shells | Fuse (type · rate · length) | Wiring layout | Timing (cue → sky) |
|------|--------|------------------------------|---------------|--------------------|
| **4×4 square** | 16 | **yellow** 1.5 s/ft · 9" (~1.1 s) + **green** 27 s/ft · ~44" (~99 s) | 3 shells tapped on the yellow, 13 on the green; e-match at tap 1 | first break ≈ 5.5 s → **3-shell burst within ~1.1 s** → one break every ~8.3 s. **Bang-then-simmer, ~1:45** |
| **1×21 straight** | 21 | **green** 27 s/ft · 43" (~96.8 s) | all 21 tapped along one run (~2.15"/tap); e-match at tap 1 | first break ≈ 5.5 s → one break every ~4.8 s. **Steady bed, ~1:40** |
| **3×7 fan** | 21 | **green** 27 s/ft · 15" per row (~33.75 s each) + **yellow** bridges between rows | 3 rows × 7 shells; rows yellow-bridged to ONE e-match → parallel **(CONFIRMED)** | first break ≈ 5.5 s → **3 fanned breaks every ~5.6 s for ~34 s — barrage wall** |
| **1×9 straight** | 9 | **pink** 2.5 s/ft · 18" (~3.75 s) | all 9 tapped along one run; e-match at tap 1 | first break ≈ 5.5 s → **all 9 within ~4 s — rapid volley**. RESERVED: exclamation mark on the final chord |
| **3×6 fan** | 18 | **green** 27 s/ft · 15" per row (~33.75 s each) + **yellow** row bridges | 3 rows × 6, bridged to ONE e-match → all rows parallel **(CONFIRMED)** | first break ≈ 5.5 s → **3 fanned breaks land together, then every ~6.75 s for ~34 s** — fan wall; opening triple lands ON the OIA final choruses |

Universal constant: **e-match sits at the first shell's tap** — every group's
first break is ≈ 5.5 s after the cue (≈3.5 s shell leader burning down the
tube + ≈2 s lift). Main-fuse length/type only sets the shell-to-shell pace.

## Final fire times (mix clock; from `cobra.csv` FINAL)

| Group | Cue fires | First break | Sky role |
|-------|-----------|-------------|----------|
| 4×4 | **1:36.5** | burst ~1:42 (AK chorus 2) | simmer bridges songs 1→2 until ~3:23 |
| 3×6 fan | **3:53.3** | triple ~3:58.8 (OIA final choruses) | fan wall to ~4:33 |
| 1×21 bed | **7:25.0** | ~7:30.5 | crown under ALL of Thunderstruck, ends ~9:07 (before the 9:12 fade) |
| 3×7 fan | **8:28** | ~8:33.5 | CROWN barrage over the false-finale climax; dies with the bed ~9:07 |
| 1×9 | **10:27.3** | ~10:32.8 | 🔒 all nine ON the final chord |

## Fuse reference

- yellow 1.5 s/ft · pink 2.5 s/ft · **green 27 s/ft**
- Cheat math: seconds ÷ rate = length. Green: 1" ≈ 2.25 s. Yellow: 1" ≈ 0.125 s. Pink: 1" ≈ 0.21 s.
- **MANDATORY: test-burn a 43" green sample from the actual batch** — the 1×21 bed ends ~5 s before the false-finale fade; a >3% slow batch erodes that margin (contingency: fire the bed 3 s earlier or tap the last shell short). Same batch check covers the 3×6/3×7 rows.

## Safety (non-negotiable)

- Continuity-test every cue before arming; all tubes loaded/fused/inspected
  before the audience arrives; no reloading (nobody downrange).
- Fan racks angled AWAY from the audience; stake/brace every rack.
- Any misfire stays untouched until the 15-minute post-show wait.
