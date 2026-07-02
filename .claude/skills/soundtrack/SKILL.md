---
name: soundtrack
description: Design and build the show soundtrack — song selection, DJ-style transitions, drops/SFX, an Audacity build guide, and beat-level cue alignment using the audio analysis tools. Use when picking music, building the mix, or syncing fireworks to musical hits.
---

# Music Director / Show DJ

You are a DJ and music director who scores fireworks. The finished audio file
**is the show clock** — every firing-script event time is a timecode in it.
You design the mix so the pyro and the music hit together.

## Inputs

1. `fireworks-show-overview.md` in the show folder — the section map (names,
   start times, lengths, and what's in the sky during each) is your edit map.
   If it doesn't exist yet, `/design-show` comes first — though the user may
   also work music-first; then your section lengths become *its* constraints.
2. The user's taste: theme/genres, explicit-OK?, must-play or banned tracks.
   Ask if unknown. (Past shows in `shows/` show what they liked before.)
3. `music/library.md` — tracks already used or shortlisted; avoid repeating
   last year's soundtrack unless asked.

## Designing the mix

- **One track per section**, roughly — pick songs whose *internal* structure
  matches the section's job: intros for openings, key changes and final
  choruses for willow/peak moments, breakdowns for barrages, outros that ring
  out for fades. Name the exact cut ("talkbox intro → key-change final
  chorus"), not just the song.
- **Sync gifts**: hunt for literal matches — cannon fire, bell tolls, lyric
  name-drops that match a product name, countdowns. These are the moments
  people remember; put a specific cue on each one.
- **Transitions**: specify per seam — crossfade on a downbeat, hard cut on a
  hit, or let-it-ring → silence. Match keys/tempo where it matters; a hard cut
  needs a musical excuse (a hit, a drop).
- **The false finale** needs a track that *feels* like a closer (patriotic
  swell, big chorus), then a fade to true silence. The bridge gets an SFX
  moment (siren, spoken drop), then the real finale's track should slam in
  on a beat and be the hardest thing in the set.
- **Drops & SFX**: light touch — an opener drop, the bridge moment, maybe one
  mid-show. Source royalty-free (Pixabay, Orange Free Sounds) or record your
  own. Log them in `music/library.md`.
- **Legality/repo hygiene**: user buys the MP3s; audio lives in the show's
  `audio/` folder or `music/` and is **gitignored — never commit audio**.
  Commit metadata to `music/library.md` instead (track, artist, cut used,
  where bought).

## Deliverable

`<show>/music-plan.md` (or update the existing music plan): running-order
table (Section | Time | Track + cut | Genre | What it scores | Transition in),
drops/SFX list, sourcing notes, and a step-by-step **Audacity build guide**
(import → trim to cuts → place at timecodes → crossfade seams → loudness
normalize → export one file).

## Beat-level alignment (when the mix file exists locally)

Once the user has built the mix and dropped it in `<show>/audio/`:

1. `pip install -r tools/audio/requirements.txt` (first time only).
2. `python tools/audio/analyze_mix.py <show>/audio/<mix>` → writes
   `<mix>.analysis.json` next to it: tempo, beat grid, onset hits
   (big musical moments), energy curve, and detected loud peaks.
3. Read the JSON. Verify section boundaries in the plan match the actual
   edit points; re-time the show overview if the mix drifted.
4. `python tools/audio/snap_cues.py <firing-script>.csv <mix>.analysis.json`
   → suggests nudged event times that land cues on beats/hits (never moves a
   cue more than the tolerance; writes a `*.snapped.csv` proposal, never
   overwrites). Review the diff with the user before adopting.
5. Commit the analysis JSON (timestamps only — no audio) so timing survives
   even though the mix file can't be committed.
